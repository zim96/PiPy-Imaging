source PiPyEnv/bin/activate
gunicorn --workers 1 --bind unix:pipy.sock -m 007 src:server
deactivate
