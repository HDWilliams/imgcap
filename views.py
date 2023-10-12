from imgcap import app
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

@app.route("/")
def home():
    return render_template('index.html')



if __name__ == '__main__':
   app.run()

