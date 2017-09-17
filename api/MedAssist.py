import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from itertools import combinations, product
import sys
import os
import string
import textrazor
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy as np
from keras.preprocessing import image
import json


class MedAssist:
	def __init__(self,mongo):
		self.db = mongo

		textrazor.api_key = "401073259520c14b27d39c351e20a6c15da13b0ed04b6872b3908567"
		self.client = textrazor.TextRazor(extractors=["entities", "topics"])
		
		self.bodyParts = []
		self.commonWords = []
		self.stop_words = set(stopwords.words('english'))
		with open('E:\\Internship\\body_parts.txt','r') as fp:
			for name in set(fp):
				self.bodyParts.append(name.strip())

		with open('E:\\Internship\\health_words.txt','r') as fp2:
			for name in set(fp2):
				self.commonWords.append(name.strip())

		

	def performTextAnalysis(self,text):
		response = self.client.analyze(text)
		for entity in response.entities():
			print(entity.freebase_types)
    
		return True
		
	def performImageAnalysis(self,filename):
		# load json and create model
		json_file = open('E:\\Internship\\model.json', 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		loaded_model = model_from_json(loaded_model_json)
		# load weights into new model
		loaded_model.load_weights("E:\\Internship\\model.h5")
		print("Loaded model from disk")
		
		# dimensions of our images
		img_width, img_height = 150, 150
		loaded_model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
		
		# predicting images
		img = image.load_img('E:\\Internship\\uploads\\'+filename, target_size=(img_width, img_height))
		x = image.img_to_array(img)
		x = np.expand_dims(x, axis=0)

		images = np.vstack([x])
		classes = loaded_model.predict_classes(images, batch_size=10)
		print(classes[0][0])
		if classes[0][0] == 0:
			return "Chickenpox"
		else:
			return "Skin Ulcer"
			
			
	def getData(self,name):
		dname = str(name)
		print(dname)
		res = self.db.disease.find_one({'disease_name':dname})
		if res!=None:
			result = {
			"dname": res['disease_name'],
			"causes":res['causes'],
			"symptoms":res['symptoms'],
			"treatment":res['treatment'],
			"desc":res['desc']
			}
		
			return json.dumps(result)
		return "no"
		

		
		#res = self.db.disease.find_one({'disease_name':str(word)})

	def process(self,text):
		text = str(text['problem'])
		diseasesFound = []

		# Step 1: Perform sentiment analysis and topic identification on input text

		# Step 2: If the topic belongs to medical/healthcare related
		if(self.performTextAnalysis(text)==True):
			# Step 3: Tokenize the words
			tokenizedText = nltk.word_tokenize(text)
			tokenizedText = [word for word in  tokenizedText if word.isalpha()]

			# Step 4: Refine the text by removing (RP: Partcle, PRP: Pronoun, CC: Conjuction, CD: Numeral)
			refined_text = []
			for pair in nltk.pos_tag(tokenizedText):
				if(pair[1]!='RP' and pair[1]!='PRP' and pair[1]!='CC' and pair[1]!='.'):
					refined_text.append(pair[0])

			# Remove stop words from the text
			refined_text = [w for w in refined_text if not w in self.stop_words]

			# Iterate over each word in refined text
			newPhrase = []
			for word in refined_text:
				#print(word)
				# Step 5: Search for any disease name containing in the refined text in the database
				res = self.db.disease.find_one({'disease_name':str(word)})
				if(res!=None):
					# Add the disease name,symptoms and its treatment/drug into the final result
					diseasesFound.append([word,res['causes'],res['symptoms'],res['treatment']])

				# Step 6: Check for body parts in the text
				if(word in self.bodyParts):
					newPhrase.append(word)

				# Step 7: Check in common health related words
				if(word in self.commonWords):
					newPhrase.append(word)
				else:
					newPhrase.append(word)

			searchStrings = []

			# Step 8: Now find combinations using each word in NewPhrase and search in UMLS
			for word in newPhrase:
				lists = [x for x in newPhrase if x!=word]
				for n in range(0, 2):
					for sublist in combinations(lists, n):
						basis = [word] + list(sublist)
						searchStrings.append(" ".join(basis))

			# Return the final results
			return diseasesFound


