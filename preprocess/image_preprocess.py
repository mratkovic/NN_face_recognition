import numpy as np
import sys
import dlib
import cv2

import constants 

__face_detector = dlib.get_frontal_face_detector()
__face_pose_predictor = dlib.shape_predictor(constants.PREDICTOR_MODEL)

def get_faces(image_name, output_folder, output_dimension=128, landmarkIndices=constants.OUTER_EYES_AND_NOSE):
	image = cv2.imread(image_name)

	detected_faces = __face_detector(image, 1)

	images = []
	for i, face_rect in enumerate(detected_faces):
		pose_landmarks = __face_pose_predictor(image, face_rect)
		
		landmarks = list(map(lambda p: (p.x, p.y), pose_landmarks.parts()))

		npLandmarks = np.float32(landmarks)
		npLandmarkIndices = np.array(landmarkIndices)

		H = cv2.getAffineTransform(npLandmarks[npLandmarkIndices],
		                           output_dimension * constants.MINMAX_TEMPLATE[npLandmarkIndices])
		alignedFace = cv2.warpAffine(image, H, (output_dimension, output_dimension))
		
		dot_index = image_name.rfind('.')
		dot_index = dot_index if dot_index != -1 else len(image_name)
		
		new_image_name = output_folder + "{}_{}.jpg".format(image_name[image_name.rfind("/")+1:dot_index],i)


		cv2.imwrite(new_image_name, alignedFace)		
		
		images.append(new_image_name)

	return images
