from flask import Flask

app = Flask('CloneTube')
app.secret_key = 'DEV_SECRET_KEY'
app.config['UPLOAD_FOLDER'] = 'upload/videos'
