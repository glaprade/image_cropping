from preprocessing import preprocessing

# set parameters
input_folder = "/Users/genevievelaprade/Documents/thesis macros and scripts/tester copy" # input path
output_folder = "/Users/genevievelaprade/Documents/thesis macros and scripts/output"
crop_height = 1024 # desired crop height
separate_channels = False # separating channels true or false
train_threshold = 0.7 # percentage of training images
test_threshold = 0.85 # 1 - percentage of testing images

cropper = preprocessing()

cropper.process_folder(input_folder, output_folder, crop_height, separate_channels, train_threshold, test_threshold)



"""
Assumes axes in the format CYX

Assumes channel 1 CLSM and channel 2 STED
"""