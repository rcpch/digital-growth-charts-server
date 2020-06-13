# imports for API only
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, make_response, jsonify, session
from werkzeug.utils import secure_filename
from os import path, listdir, remove
from datetime import datetime
from pathlib import Path
from measurement_request import MeasurementForm

# imports for client only
import markdown
import requests

# imports for both
import json
import controllers as controllers


app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'UK_WHO' #not very secret - this will need complicating and adding to config

from app import app

"""
Uses session variables to store form or uploaded unique child data
These session variables are accessed when user wants to download the calculated data,
or chart them.
    session["results"] are the form data entered by the user or uploaded from excel
    session["serial_data"] is a boolean value flagging if data are single measurements 
    or serial unique patient data
"""  

"""
API DEFINITIONS SECTION
* The API is versioned in a hard-coded fashion for now, however in time the versioning
  will happen at the level of the API management layer, which will direct requests to the
  correct versioned server accordingly
* There are different endpoints for a simple JSON response and a more complex FHIR response
* Each API endpoint has a distinct Controller
"""

# HELLO WORLD
# this is a testing route and should be removed once we have everything working
@app.route("/api/v1/hello", methods=['GET'])
def api_hello():
    return jsonify( controllers.hello() )


"""
Centile Calculations API route. Expects query params as below:
  birth_date            STRING          date of birth of the patient in YYYY-MM-DD ISO8601 format (will be converted to Date)
  observation_date      STRING          date of the measurement in YYYY-MM-DD ISO8601 format (will be converted to Date)
  height_in_metres      FLOAT           the height in METRES NOT CENTIMETRES
  weight_in_kg          FLOAT           the weight in kilograms
  occipitofrontal_circ_in_cm  FLOAT     head circumference in CENTIMETRES
  sex                   STRING          either 'male or 'female'
  gestation_weeks       INTEGER         gestational age in completed weeks
  gestation_days        INTEGER         gestational age in completed days
"""
# JSON CALCULATION
@app.route("/api/v1/json/calculations", methods=['GET'])
def api_json_calculations():

    # check here for all the right query params, if not present raise error
    print(request.args)

    response = controllers.perform_calculations(
        birth_date=datetime.strptime(request.args['birth_date'], '%Y-%m-%d'),
        observation_date=datetime.strptime(request.args['observation_date'], '%Y-%m-%d'),
        height=float(request.args['height_in_metres']),
        weight=float(request.args['weight_in_kg']),
        ofc=float(request.args['occipitofrontal_circ_in_cm']),
        sex=str(request.args['sex']),
        gestation_weeks=int(request.args['gestation_weeks']),
        gestation_days=int(request.args['gestation_days'])
    )
    return jsonify(response)


# FHIR CALCULATION
@app.route("/api/v1/fhir", methods=['GET'])
def api_fhir():
    return jsonify({'path': '/api/v1/fhir'})


# API route
@app.route("/api/v1/json/references", methods=['GET'])

# API route
@app.route("/api/v1/json/documentation", methods=['GET'])

# API route
@app.route("/chart_data", methods=['GET'])
def chart_data():
    # Retrieve child data for charting
    results = session.get('results')
    # Retrieve source of data
    unique = session.get('serial_data')
    if unique:
        #data come from a table and are not formatted for the charts
        formatted_child_data = controllers.prepare_data_as_array_of_measurement_objects(results)
        
        # Prepare data from plotting
        child_data = controllers.create_data_plots(formatted_child_data)
        # Retrieve sex of child to select correct centile charts
        sex = formatted_child_data[0]['birth_data']['sex']
        
    else:
        # Prepare data from plotting
        child_data = controllers.create_data_plots(results)
        # Retrieve sex of child to select correct centile charts
        sex = results[0]['birth_data']['sex']

    # Create Centile Charts
    centiles = controllers.create_centile_values(sex)

    return jsonify({
        'sex': sex,
        'child_data': child_data,
        'centile_data': centiles
    })

# potentially an API route - serve instructions from README.md as MD or something else
@app.route("/instructions", methods=['GET'])
def instructions():
    #open README.md file
    this_directory = path.abspath(path.dirname(__file__))
    file = path.join(this_directory, 'README.md')
    with open(file) as markdown_file:

        #read contents of file
        content = markdown_file.read()

        #convert to HTML
        html = markdown.markdown(content)
    return render_template('instructions.html', fill=html)


"""
FLASK CLIENT ROUTES - TO BE REFACTORED OUT TO THEIR OWN REPO
"""

# client route
@app.route("/", methods=['GET', 'POST'])
def home():
    form = MeasurementForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            payload = {
                'birth_date': form.birth_date.data,
                'observation_date': form.obs_date.data,
                'height_in_metres': float(form.height.data),
                'weight_in_kg': float(form.weight.data),
                'occipitofrontal_circ_in_cm': float(form.ofc.data),
                'sex': str(form.sex.data),
                'gestation_weeks': int(form.gestation_weeks.data),
                'gestation_days': int(form.gestation_days.data)
            }
            # collect user form entries and perform date and SDS/Centile calculations
            response = requests.get(
                'http://localhost:5000/api/v1/json/calculations',
                params=payload
            )

            print(response.json())

            # store the results in a session for access by tables and charts later
            session['results'] = response.json()

            # flag to differentiate between individual plot and serial data plot
            session['serial_data'] = False

            return redirect(url_for('results', id='table'))

        # form not validated. Need flash warning here
        return render_template('measurement_form.html', form = form)
    else:
        # controllers.temp_test_functions.tim_tests_preterm()
        return render_template('measurement_form.html', form = form)

# client route
@app.route("/results/<id>", methods=['GET', 'POST'])
def results(id):
    results = session.get('results')
    if id == 'table':
        return render_template('test_results.html', result = results)
    if id == 'chart':
        return render_template('chart.html')

# client route
@app.route("/chart", methods=['GET'])
def chart():
    return render_template('chart.html')



# may need to be deprecated for MVP
@app.route("/import", methods=['GET', 'POST'])
def import_growth_data():
    if request.method == 'POST':
        ## can only receive .xls, .xlsx, or .csv files
        ## thanks to Chris Griffith, Code Calamity for this code - upload files, chunk if large
        file = request.files['file']
        static_directory = path.join(path.abspath(path.dirname(__file__)), "static/uploaded_data")
        file_to_save = path.join(static_directory, secure_filename(file.filename))
        current_chunk = int(request.form['dzchunkindex'])

        # If the file already exists it's ok if we are appending to it,
        # but not if it's new file that would overwrite the existing one
        if path.exists(file_to_save) and current_chunk == 0:
            # 400 and 500s will tell dropzone that an error occurred and show an error
            return make_response(('File already exists', 400))

        try:
            with open(file_to_save, 'ab') as f:
                f.seek(int(request.form['dzchunkbyteoffset']))
                f.write(file.stream.read())
        except OSError:
            # log.exception will include the traceback so we can see what's wrong 
            print('Could not write to file')
            return make_response(("Not sure why,"
                                " but we couldn't write the file to disk", 500))

        total_chunks = int(request.form['dztotalchunkcount'])

        if current_chunk + 1 == total_chunks:
            # This was the last chunk, the file should be complete and the size we expect
            if path.getsize(file_to_save) != int(request.form['dztotalfilesize']):
                assert(f"File {file.filename} was completed, "
                        f"but has a size mismatch."
                        f"Was {os.path.getsize(save_path)} but we"
                        f" expected {request.form['dztotalfilesize']} ")
                return make_response(('Size mismatch', 500))
            else:
                print(f'File {file.filename} has been uploaded successfully')
                # return make_response('Upload Successful', 200)
                return make_response('success', 200)
        else:
            print(f'Chunk {current_chunk + 1} of {total_chunks} '
                    f'for file {file.filename} complete')

        return make_response("Chunk upload successful", 200)
            
    else:
        return render_template('import.html')

# ?deprecate for MVP
@app.route("/uploaded_data/<id>", methods=['GET', 'POST'])
def uploaded_data(id):
    global requested_data
    if request.method == 'GET':
        static_directory = path.join(path.abspath(path.dirname(__file__)), "static/uploaded_data/")
        if id == 'example':
            ## Have requested to view the sample data
            file_path = path.join(static_directory, 'dummy_data.xlsx')
            loaded_data = controllers.import_excel_sheet(file_path, False) #false flag prevents deleting file once data imported
            data = json.loads(loaded_data['data'])
            """
            converts ISO8601 to UK readable dates
            """
            for i in data:
                if(i['birth_date']):
                    i['birth_date'] =  datetime.strftime(datetime.fromtimestamp(i['birth_date']/1000), '%d/%m/%Y')
                if(i['observation_date']):    
                    i['observation_date'] =  datetime.strftime(datetime.fromtimestamp(i['observation_date']/1000), '%d/%m/%Y')
                if(i['estimated_date_delivery']): 
                    i['estimated_date_delivery'] =  datetime.strftime(datetime.fromtimestamp(i['estimated_date_delivery']/1000), '%d/%m/%Y')
            # store the formatted data in a global variable
            requested_data = data
            ## this data is not from a unique patient - cannot graph or produce velocities
            return render_template('uploaded_data.html', data=data, unique=loaded_data['unique'], dynamic_calculations=None)
        if id == 'excel_sheet':
            for file_name in listdir(static_directory):
                if file_name != 'dummy_data.xlsx':
                    """
                    Loop through static/upload folder
                    Avoid the example sheet
                    Save there temporarily, import the data then delete
                    """
                    file_path = path.join(static_directory, file_name)
                    try:
                        # import the data from excel and validate, delete the file once imported (True flag)
                        child_data = controllers.import_excel_sheet(file_path, True)
                        # extract the dataframe
                        data_frame = child_data['data']
                    
                    except ValueError as e:
                        
                        """
                        Error handler - uploaded sheet is incompatible: missing essential data
                        """
                        print(e)
                        flash(f"{e}")
                        data=None
                        render_template('uploaded_data.html', data=data, unique=False, dynamic_calculations=None)

                    except LookupError as l:
                        
                        """
                        Error handler - uploaded sheet is incompatible: headings are missing or too many or misspelled
                        """

                        data=None
                        print(l)
                        flash(f"{l}")
                        data=None
                        render_template('uploaded_data.html', data=data, unique=False, dynamic_calculations=None)
                    
                    else:
                        """
                        Data is correct format
                        Load as JSON and report to table
                        If the imported data is all same patient (on basis of unique birth_date),
                        offer the opportunity to chart it, calculate velocity and acceleration of most recent parameters
                        """

                        #convert dataframe to JSON
                        data = json.loads(data_frame)

                        """
                        creates UK date strings from ISO8601
                        """
                        for i in data:
                            if(i['birth_date']):
                                i['birth_date'] =  datetime.strftime(datetime.fromtimestamp(i['birth_date']/1000), '%d/%m/%Y')
                            if(i['observation_date']):
                                i['observation_date'] =  datetime.strftime(datetime.fromtimestamp(i['observation_date']/1000), '%d/%m/%Y')
                            if(i['estimated_date_delivery']): 
                                i['estimated_date_delivery'] =  datetime.strftime(datetime.fromtimestamp(i['estimated_date_delivery']/1000), '%d/%m/%Y')
                        
                        # store the JSON in global variable for conversion back to excel format for download if requested
                        requested_data = data

                        # data is unique patient, calculate velocity
                        # data come from a table and need converting to Measurement class
                        formatted_child_data = controllers.prepare_data_as_array_of_measurement_objects(requested_data)
                        dynamic_calculations = controllers.calculate_velocity_acceleration(formatted_child_data)
                        
                        # if unique data(single child, not multiple children) store in session for access by chart if requested
                        session['results'] = requested_data
                        session['serial_data'] = True
                
            return render_template('uploaded_data.html', data=data, unique=child_data['unique'], dynamic_calculations = dynamic_calculations) #unique is a flag to indicate if unique child or multiple children
        
        if id=='get_excel': ##broken needs fix - file deleted so can't download
            excel_file = controllers.download_excel(requested_data)
            temp_directory = Path.cwd().joinpath("static").joinpath('uploaded_data').joinpath('temp')
            return send_from_directory(temp_directory, filename='output.xlsx', as_attachment=True)


# client route, generated from references list (references in separate GH repo eventually)
@app.route("/references", methods=['GET'])
def references():
    # starting with a hard-coded list, but as it grows probably belongs in database
    with open('./resource_data/growth_reference_repository.json') as json_file:
            data = json.load(json_file)
            json_file.close()
    return render_template('references.html', data=data)

if __name__ == '__main__':
    app.run()
