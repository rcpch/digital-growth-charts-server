### Running the Flask application
* Tell Flask you are in Development mode  
`$ export FLASK_ENV=development`
* Set up Flask so it knows what your app is called  
`$ export FLASK_APP=app.py`  
* Run Flask
`$ flask run`  

You should then see some messages from the Flask development server, which should look like
```
 * Serving Flask app "app.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx
```