import pymongo
from pymongo import MongoClient

mongo =  MongoClient('localhost', 27017)
db = mongo.MedAssist
doc = {'disease_name':'Chickenpox',
	    'symptoms':['Feeling tired and generally unwell',
					'A high temperature (fever) of 38C (100.4F) or over',
					'Feeling sick',
					'A headache',
					'Aching painful muscles',
					'Loss of appetite'],
		'causes':['Varicella-zoster virus (VZV)'],
		'treatment':['Chickenpox is extremely contagious. Keep your child at home until all of the blisters have burst and crusted over.'],
		'picture':'',
		'desc':'Chickenpox, also called varicella, is characterized by itchy red blisters that appear all over the body. A virus causes this condition. It often affects children, and was so common it was considered a childhood rite of passage.',
		'types':['Spots','Blisters','Scabs and Crusts'],
		'similar':'',
		'links':''
		}
db.disease.insert_one(doc)

'''pages = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
for p in pages:
	with open('D:\\Internship\\Dataset\\webmd_crawl\\'+p+'.txt','r') as fp:
		for t in fp:
			sd = t.strip().split('\t')
			links = []
			if(len(sd)>1):
				links.append(sd[1])
			doc = {
			 'disease_name':sd[0],
			 'symptoms':'',
			 'causes':'',
			 'treatment':'',
			 'picture':'',
			 'types':'',
			 'similar':'',
			 'links':links
			}
			db.disease.insert_one(doc)'''
'''db.disease.update_one({'disease_name':'Vaginal Itching'},{
	'$set':{

	'symptoms':['Itching',
'Swelling',
'Pelvic pain',
'Foul-smelling discharge',
'Green\, yellow\, or gray discharge',
'Foamy or clumpy (like cottage cheese) discharge'],

	'causes':['Yeast infection',
'Sexually transmitted diseases',
'Overgrowth of normal bacteria in the vagina called bacterial vaginosis',
'Menopause or low estrogen levels',
'Foreign objects left in the vagina such as a tampon',
'An intrauterine device (IUD) for birth control',
'Medications such as antibiotics and steroids',
'Damp or tight-fitting clothing',
'Skin conditions such as desquamative vaginitis or lichen planus',
'Poorly controlled diabetes',
'Cancer of the cervix or vagina'],

	'treatment':['Keeping your genital area clean and dry',
'Wearing loose-fitting clothing\, cotton underwear during the day\, and no underwear while sleeping to help your vagina breathe',
'Refraining from using soap\, and rinsing the area with water instead',
'Soaking in a warm (not hot) bath',
'Avoiding douches\, as they eliminate healthy bacteria that help fight infections',
'Not applying hygiene sprays\, fragrances\, or powders near the vagina',
'Using pads instead of tampons if you have an infection',
'Wiping from front to back when using the toilet',
'Keeping your blood glucose under control if you have diabetes']
	}
	})'''
