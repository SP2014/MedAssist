from flask import Flask, render_template,abort, request 
import json
from api.MedAssist import MedAssist
import pymongo
from pymongo import MongoClient
from werkzeug import secure_filename
import os
import PIL
from PIL import Image

UPLOAD_FOLDER = 'E:\\Internship\\uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mongo =  MongoClient('localhost', 27017)

#print(mongo)

ma = MedAssist(mongo.MedAssist)

@app.route('/')
def index():
   return render_template('hello.html')


@app.route('/test')
def test():
	return render_template('index.html')



@app.route('/process', methods=['POST'])
def process():
	if not request.json:
		abort(400)

	res = ma.process(request.json)

	return json.dumps(res)
	
	
@app.route('/data/<dname>')
def getdata(dname):
	return ma.getData(dname)
	
	
@app.route('/imageProcess', methods=['POST'])
def imgProcess():
	file = request.files['file']
	filename = secure_filename(file.filename)
	file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
	print(file.filename)
	img = Image.open(UPLOAD_FOLDER+'\\'+file.filename)
	img = img.resize((150,150),Image.ANTIALIAS)
	img.save(os.path.join(app.config['UPLOAD_FOLDER'],filename),"JPEG",quality=100)
	res = ma.performImageAnalysis(file.filename)
	
	return json.dumps({'result':res})


if __name__ == '__main__':
   app.run(debug = True)
