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

db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="test_database") 
    
@app.route('/image_location_server/getAllEntries', methods=['GET'])
def get_all_json():
    cur = db.cursor()

    cur.execute("SELECT * FROM simple_test_table")

    objects_list = []
    
    for row in cur.fetchall() :
        d = collections.OrderedDict()
        d['latitude'] = row[0]
        d['longitude'] = row[1]
        d['file_url'] = row[2]
        objects_list.append(d)
        
    return json.dumps(objects_list)

@app.route('/image_location_server/getImage/<path:image_url>', methods=['GET'])
def get_img_at(image_url):
    
    return send_file('/' + image_url)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/image_location_server/add_image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print request.files['uploaded'].filename
        request.files['uploaded'].save(request.files['uploaded'].filename)
        return "SUCCESS"

@app.route('/image_location_server/addDataPoint', methods=['GET', 'POST'])
def add_data_point():
    if request.method == 'POST':
        json_payload = request.get_json()
        print request.get_json().get('file_url')
        cur = db.cursor()
        insert_statement = (
            "INSERT INTO image_location_test (longitude, latitude, file_url) "
            "VALUES (%s, %s, %s)"
        )
        
        data = (json_payload.get('longitude'), json_payload.get('latitude'), json_payload.get('file_url'))
        cur.execute(insert_statement, data)
        db.commit()
        print 'HOORAY'
        return 'SUCCESS'
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
