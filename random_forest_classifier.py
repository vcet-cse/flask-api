import joblib
from csv import reader
import csv
import math

rice_type_int = {'BOILED_BASMATI':'1', 'BOILED_POLISHED_RED':'3'}

# Convert string column to float
def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())

def classify(rice_type):
	dataset = list()
	rice_type_int_select = rice_type_int[rice_type]
	#print(rice_type_int_select, rice_type)
	with open('extracted_features/test.csv', 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)

	for i in range(1,len(dataset[0])):
		str_column_to_float(dataset, i)

	result = []
	total_g = 0
	damage_g = 0
	correct_g = 0
	grade_result = "R"
	
	clf = joblib.load('trained_models/random_forest/'+rice_type_int_select+'/random_forest_model.pkl')

	for row in dataset:

		p = clf.predict([row[1:7]])
		#print(p[0])
		row[-1] = p[0]
		total_g += 1
		result_v = row[-1] - (math.floor(row[-1]))
		if(result_v < 0.55 and p[0] != 1.0):
			damage_g += 1
		else:
			correct_g += 1
        
		result.append(row)
    
	damage_per = (damage_g*100)/total_g
    
	if damage_g == 0:
		grade_result = "P"
	elif damage_per < 25:
		grade_result = "G_1"
	elif damage_per < 50:
		grade_result = "G_2"
	elif damage_per > 50:
		grade_result = "G_3"
        
	#print(damage_per)

	for i in result:
		with open('extracted_features/result.csv', 'a', newline='') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			spamwriter.writerow([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]])
        #print("WIDTH   ||  HEIGHT   ||   aspect_ratio   ||   AREA   ||   RADIUS  ||  PERIMETER   ||    LABLE")
	l = []
	for i in result:
		d = {'image':i[0], "width_":i[1],  "height_":i[2],  "aspect_ratio_":i[3],  "area_":i[4],  "radius_":i[5],  "perimeter_":i[6],  "result_":i[7]}
		l.append(d)
        
	fd = {"Data":l, "Result":grade_result, "Total":total_g, "Damage":damage_g, "Correct":correct_g}
	#print(fd)
	return fd
