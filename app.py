from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, make_response
from werkzeug.utils import secure_filename
import markdown
from os import path, listdir

from measurement_request import MeasurementForm
import json

import controllers as controllers

app = Flask(__name__)
app.config['SECRET_KEY'] = 'UK_WHO' #not very secret - this will need complicating and adding to config

from app import app

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=['GET', 'POST'])
def home():
    form = MeasurementForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            results = controllers.perform_calculations(form)
            return render_template('test_results.html', result=results)
        
        # form not validated. Need flash warning here
        return render_template('measurement_form.html', form = form)
    else:
        return render_template('measurement_form.html', form = form)

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
                # data = controllers.import_excel_sheet(file_to_save)
                return make_response('Upload Successful', 200)
        else:
            print(f'Chunk {current_chunk + 1} of {total_chunks} '
                    f'for file {file.filename} complete')

        return make_response("Chunk upload successful", 200)
            
    else:
        return render_template('import.html')

@app.route("/uploaded_data", methods=['GET'])
def uploaded_data():
    static_directory = path.join(path.abspath(path.dirname(__file__)), "static/uploaded_data/")
    for file_name in listdir(static_directory):
        file_path = path.join(static_directory, file_name)
        data_frame = controllers.import_excel_sheet(file_path)
    return render_template('uploaded_data.html', data=data_frame)

@app.route("/references", methods=['GET'])
def references():
    # starting with a hard-coded list, but as it grows probably belongs in database
    with open('./resource_data/growth_reference_repository.json') as json_file:
            data = json.load(json_file)
            json_file.close()
    return render_template('references.html', data=data)

if __name__ == '__main__':
    app.run()