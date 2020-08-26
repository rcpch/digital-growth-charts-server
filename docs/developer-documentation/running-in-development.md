### Running the API server application

Simply type 
`$ s/start-server` in the application root

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

If you need to vary any of the parameters passed to Flask, you can either modify the startup script or simply pass the commands to the shell manually.

Scripts are located in the `s/` folder in the application root.
