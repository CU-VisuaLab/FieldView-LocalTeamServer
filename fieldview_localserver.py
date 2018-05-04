import MySQLdb
import collections
import json
from flask import Flask, redirect, jsonify, send_file, request
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/home/pi/VisuaLab-LocalServer'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="fieldview_local") 

longitude = -105.2680
latitude = 40.00625

@app.route('/fieldview/getAllJson', methods=['GET'])
def get_all_json():
    cur = db.cursor()

    cur.execute("SELECT * FROM scorch_table")

    objects_list = []
    
    for row in cur.fetchall() :
        d = collections.OrderedDict()
        d['longitude'] = row[0].__str__()
        d['latitude'] = row[1].__str__()
        d['scorch_rate'] = row[2].__str__()
        d['image_url'] = row[3]
        d['user'] = row[4]
        objects_list.append(d)
        
    return json.dumps(objects_list)

@app.route('/fieldview/setLocation', methods=['GET', 'POST'])
def set_location():
    if request.method == 'POST':
        json_payload = request.get_json()
        print 'location set at (' + json_payload.get('latitude').__str__() + ', ' + json_payload.get('longitude').__str__() + ')'
        longitude = json_payload.get('longitude')
        latitude = json_payload.get('latitude')
        return 'SUCCESS'

@app.route('/fieldview/getLongitude', methods=['GET'])
def get_longitude():
    print longitude.__str__()
    return longitude.__str__()

@app.route('/fieldview/getLatitude', methods=['GET'])
def get_latitude():
    print latitude.__str__()
    return latitude.__str__()


@app.route('/fieldview/getImage/<path:image_url>', methods=['GET'])
def get_img_at(image_url):
    
    return send_file('/' + image_url)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/fieldview/add_image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print request.files['uploaded'].filename
        request.files['uploaded'].save(request.files['uploaded'].filename)
        return "SUCCESS"

@app.route('/fieldview/addDataPoint', methods=['GET', 'POST'])
def add_data_point():
    if request.method == 'POST':
        json_payload = request.get_json()
        scorch_rate = json_payload.get('scorch_rate').split(' ')[0]
        user = json_payload.get('scorch_rate').split(' ')[1]
        cur = db.cursor()
        insert_statement = (
            "INSERT INTO scorch_table (longitude, latitude, scorch_rate, image_url, user) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        
        data = (json_payload.get('longitude'), json_payload.get('latitude'), scorch_rate, json_payload.get('image_url'), user)
        cur.execute(insert_statement, data)
        db.commit()
        return 'SUCCESS'
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
