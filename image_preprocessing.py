from preprocessing import preprocessing

# set parameters
input_folder = "/home/glapr/projects/def-cbrown/glapr/ImagePreprocessing/Actin_dataset" # input path
output_folder = "/home/glapr/projects/def-cbrown/glapr/ImagePreprocessing/Processed_Actin_dataset"
crop_height = 256 # desired crop height
separate_channels = True # separating channels true or false
train_threshold = 0.7 # percentage of training images
test_threshold = 0.85 # 1 - percentage of testing images

cropper = preprocessing()

cropper.process_folder(input_folder, output_folder, crop_height, separate_channels, train_threshold, test_threshold)



"""
Assumes axes in the format CYX

Assumes channel 1 CLSM and channel 2 STED
"""
