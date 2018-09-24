import numpy as np
import h5py
import scipy.io as sio
import cv2


def create_dataset(dataset):

	if dataset == "nyu2":

		print "Loading mat file ..."

		f = h5py.File('nyu_depth_v2_labeled.mat')
		rgb_images = np.array([x for x in f["images"]])
		depth_images = np.array([x for x in f["depths"]]) 
		labels= np.array([x for x in f["labels"]])  

		mapping =  sio.loadmat("nyuv2_40class_mapping.mat")["mapping"][0]
		
		print "Mapping 894 class to 40 class..."

		for i,label in enumerate(labels):
			for j,row in enumerate(label):
				for k,value in enumerate(row):
					labels[i][j][k] = mapping[value-1]
		
		print "Resizing and scaling images and labels..."

		rgbs=[]
		depths=[]
		masks=[]

		max_depth,min_depth = np.max(depth_images),np.min(depth_images)

		for rgb_image in rgb_images:
			img = np.transpose(rgb_image,(1,2,0))
			img = cv2.resize(img,(224,224),interpolation=cv2.INTER_LINEAR)
			rgbs.append(rgbs)

		for depth_image in depth_images:
			depth_image = (depth_image - min_depth) / (1.*(max_depth-min_depth))*255
			depth_image = cv2.resize(depth_image,(224,224),interpolation=cv2.INTER_NEAREST)
			depths.append(depth_image.astype(int))

		for label in labels:
			label = cv2.resize(label,(224,224),interpolation=cv2.INTER_NEAREST)
			masks.append(label)

		d = { "rgb_images":rgb_images, "depth_images":depth_images, "masks":masks}

		print "Saving images and labels..."

		np.save("nyu2.npy", d)

		print "Finished !"

	else:
		print "Dataset {} is not implemented".format(dataset)

def main():
	create_dataset("nyu2")

if __name__ == '__main__':
	main()

