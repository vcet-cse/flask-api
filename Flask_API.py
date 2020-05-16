#using flask_restful
from flask_restful import Resource, Api
import os
import time
from PIL import Image
from io import StringIO
from flask import Flask, flash, request, redirect, url_for, session, jsonify, abort, render_template_string, send_from_directory, Response
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import pymongo
from pymongo import MongoClient
import MAIN

Client = MongoClient("mongodb://192.168.43.159:27017")
db = Client['Grain_Database']
collection = db["grain_data"]

UPLOAD_FOLDER = 'image'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# creating the flask app 
app = Flask(__name__) 
# creating an API object 
api = Api(app) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)

class Hello(Resource): 

	# is a GET request for this resource 
	def get(self): 
		#return jsonify({'data': "Hello"})
		return "Message FromServer"

	# Corresponds to POST request 
	def post(self): 
		#data = request.get_json()
		#return jsonify({'data': "Hello"})
		return "Message FromServer"

# another resource to calculate the square of a number 
class Get_Image(Resource): 
        
        def get(self, filename):
            #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            #response.headers['Pragma'] = 'no-cache'
            try:
                w = int(request.args['w'])
                h = int(request.args['h'])
            except (KeyError, ValueError):
                return send_from_directory('.', filename)

            try:
                im = Image.open(filename)
                im.thumbnail((w, h), Image.ANTIALIAS)
                io = StringIO.StringIO()
                im.save(io, format='JPG')
                return Response(io.getvalue(), mimetype='image/jpg')

            except IOError:
                abort(404)

            return send_from_directory('.', filename)

# Uploading files
class FileUpload(Resource): 
	def post(self):
		target=os.path.join(UPLOAD_FOLDER,'uploaded_img')
		if not os.path.isdir(target):
			os.mkdir(target)
		file = request.files['image']		
		filename = secure_filename(file.filename)
		rice_type = str(filename)
		destination="/".join([target, "input_image.jpg"])
		file.save(destination)
		session['uploadFilePath']=destination
		fd = MAIN.hi(rice_type)
		#print(fd)
		fd['Grain_Type'] = str(filename)
		collection.insert(fd)
		#print(fd)
		#return jsonify(fd)
		#time.sleep(60)
		return "Success"
		#return jsonify({'data': "Hello"})

# Uploading files
class FileUpload_Web(Resource): 
	def post(self):
		target=os.path.join(UPLOAD_FOLDER,'uploaded_img')
		if not os.path.isdir(target):
			os.mkdir(target)
		file = request.files['image']		
		filename = secure_filename(file.filename)
		rice_type = str(filename)
		destination="/".join([target, "input_image.jpg"])
		file.save(destination)
		session['uploadFilePath']=destination
		fd = MAIN.hi(rice_type)
		fd['Grain_Type'] = str(filename)
		#print(fd)
		return jsonify(fd)

class Get_Detailed_result(Resource): 
	def get(self):
		#cursor = collection.find().sort('_id', pymongo.DESCENDING).limit(1)[0]['_id']
		#cursor = collection.find().sort('_id', -1).limit(1)[0]['_id']
		cursor = list(collection.find().sort('_id', -1).limit(1))
		#print(cursor[0]['Data'][0])
		#time.sleep(60)
		return jsonify({'id':str(cursor[0]['_id']), 'result':str(cursor[0]['Result']), 'total':str(cursor[0]['Total']), 'damage':str(cursor[0]['Damage']), 'correct':str(cursor[0]['Correct']), 'grain_type':str(cursor[0]['Grain_Type'])})

# adding the defined resources along with their corresponding urls 
api.add_resource(Hello, '/') 
api.add_resource(Get_Image, '/get_images/<path:filename>')
api.add_resource(FileUpload, '/upload')
api.add_resource(FileUpload_Web, '/uploadWeb') 
api.add_resource(Get_Detailed_result, '/detailed_result')


# driver function 
if __name__ == '__main__':
    app.secret_key = os.urandom(24) 
    app.run(debug=True, host='192.168.43.159',port=3001)



