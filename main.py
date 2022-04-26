
from flask import Flask,render_template

from wsgiref import simple_server

from flask import Flask, session, request, Response, jsonify



import atexit
import uuid
import os
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    # return "Flask app is running to good to go pankaj is chutiya"

@app.route('/Train_Profile_Report',methods=['GET','POST'])
def Train_profile_Report():
    return render_template("Train_Data_Profiling.html")



@app.route('/Test_Profile_Report',methods=['GET','POST'])
def Test_profile_Report():
    return render_template("Test_Data_Profiling.html")



port = int(os.getenv("PORT", 5001))

if __name__ == "__main__":
    host = '0.0.0.0'
    #app.run()
    httpd = simple_server.make_server(host=host, port=port, app=app)
    #httpd = simple_server.make_server(host='127.0.0.1', port=5000, app=app)
    # print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
