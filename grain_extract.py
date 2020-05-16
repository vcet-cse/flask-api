#https://stackoverflow.com/questions/51249781/using-regionprops-in-python
from skimage.io import imread, imshow
from skimage.filters import gaussian, threshold_otsu
from skimage import measure, data, io
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
import cv2
import matplotlib.patches as mpatches
from skimage.color import label2rgb
from PIL import Image
import numpy as np
import shutil
import os
import glob
from skimage.exposure import rescale_intensity
from skimage.morphology import reconstruction
import numpy as np
import rotate_image

def grain_extract(img, rice_type):

	shutil.rmtree('extracted_grains')
	os.mkdir('extracted_grains')
	shutil.rmtree('extracted_grains_rgb')
	os.mkdir('extracted_grains_rgb')

	original = imread(img)

	gray_image = rgb2gray(original)

	thresh = threshold_otsu(gray_image)
	o = gray_image > thresh

	blurred = gaussian(o, sigma=.8)
	binary = blurred > threshold_otsu(blurred)

	seed = np.copy(binary)
	seed[1:-1, 1:-1] = binary.max()
	mask = binary
	filled = reconstruction(seed, mask, method='erosion')

	labels = measure.label(filled)
	props = measure.regionprops(labels)
	
	fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
	ax.imshow(original)
	#ax.subplots_adjust(left=0,right=4,bottom=5,top=10)
	ax.axis('tight')
	#ax.axis('off')

	file = open("img_count.txt", "r")  
	db_count = int(file.read())
	file.close()

	i = db_count

	for prop in props:
		if prop.area < 200 :
	    		continue
		#print('grain',i,': Size -> ',prop.area)
		a, b, c, d = prop.bbox
		#io.imshow(original[a:c, b:d])
		#plt.show()
		plt.imsave('extracted_grains/' + str(i) + '.jpg', prop.image, cmap=plt.cm.gray)
		plt.imsave('extracted_grains_rgb/' + str(i) + '.jpg', original[a:c, b:d], cmap=plt.cm.gray)
		plt.imsave('extracted_grains_for_database/' + str(i) + '.jpg', original[a:c, b:d], cmap=plt.cm.gray)
		
		
		minr, minc, maxr, maxc = (a-5, b-5, c+5, d+5)
		rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=0.5)
		ax.add_patch(rect)
		
		i += 1

	db_count = i
	file = open("img_count.txt", "w") 
	file.write(str(db_count))
	file.close()
	
	plt.axis('off')
	plt.savefig('image/Image_result/foo.png', bbox_inches='tight')

	fd = rotate_image.rotate_img(rice_type)
	return fd
	#plt.show()
