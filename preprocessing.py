import tifffile
import os

class preprocessing:

    # load image using tifffile library (specific to .TIFF files)
    def load_image(self, img_path):
        return tifffile.imread(img_path)

    # save image using tifffile library (specific to .TIFF files)
    def save_image(self, output_path, img):
        tifffile.imwrite(output_path, img)

    # filters out images with mean intensity of less than 1
    def filter_image(self, img):

        # get mean value of first channel of image
        mean = img[0].mean()

        # if mean value is less than 1
        if mean < 1:
            # return false
            return 0
        else:
            # else return true
            return 1

    # splits first two channels into CLSM and STED
    def split_channels(self, folder):
        # Create output folders
        clsm_folder = os.path.join(folder, "CLSM")
        sted_folder = os.path.join(folder, "STED")

        os.makedirs(clsm_folder, exist_ok=True)
        os.makedirs(sted_folder, exist_ok=True)

        #for image in folder
        for entry in os.scandir(folder):
            # skip entry if it is a directory
            if entry.is_dir():
                continue

            # get image name
            whole_image_name = self.get_label(entry.path)

            # set CLSM path
            clsm_out = os.path.join(clsm_folder, (whole_image_name + "_CLSM.tif"))

            # set STED path
            sted_out = os.path.join(sted_folder, (whole_image_name + "_STED.tif"))

            # load image
            img = self.load_image(entry.path)

            # set CLSM image
            CLSM = img[0,:,:]

            # set STED image
            STED = img[1,:,:]

            # save CLSM image
            self.save_image(clsm_out, CLSM)

            # save STED image
            self.save_image(sted_out, STED)

            os.remove(entry.path)

        return

    # split images into test train and validation sets
    def train_test_valid(self, input_folder, output_folder, train_threshold, test_threshold):

        # define entries, ensure they're sorted
        entries = sorted(
            [e for e in os.scandir(input_folder) if e.is_file()],
            key=lambda e: e.name
            )
        # get number of images in folder
        n = len(entries)

        # Create output folders
        train = os.path.join(output_folder, "train")
        test = os.path.join(output_folder, "test")
        valid = os.path.join(output_folder, "valid")

        os.makedirs(train, exist_ok=True)
        os.makedirs(test, exist_ok=True)
        os.makedirs(valid, exist_ok=True)

        # set image count to 0
        count = 0
        # for entry in folder
        for entry in entries:

            img = self.load_image(entry.path)
            filename = self.get_label(entry.path) + ".tif"

            # if image count is less than the % train threshold
            if count < int(train_threshold * n):
                # move image to train folder
                self.save_image(os.path.join(train, filename), img)
            # if image count is above the test threshold
            elif count > int(test_threshold * n):
                # move image to test folder
                self.save_image(os.path.join(test, filename), img)
            # if image count is between two thresholds
            else:
                # move image to validation folder
                self.save_image(os.path.join(valid, filename), img)

            # increase count
            count +=1

        return

    # get image name without file type
    def get_label(self, img_path):
        # get file name
        name = os.path.basename(img_path)
        # get file name length
        name_len = len(name)
        # remove file type (assuming .tif)
        name = name[0:name_len-4]
        # return name no file type
        return name

    # crop image
    def crop_image(self, crop_height, input_path, output_path):

        img = self.load_image(input_path)

        name = self.get_label(input_path)

        img_height = img.shape[1]
        h = crop_height

        count = 1
        x = 0 # set x start
        y = 0 # set y start
        x_edge = img_height # set x edge boundary
        y_edge = img_height # set y edge boundary

        while y < y_edge: # while the starting y coordinate is less than the edge value
            while x < x_edge: # while the starting x coordinate is less than the edge value

                crop = img[:,y:y+h,x:x+h] # crop image to specified height

                # filter image
                if self.filter_image(crop) == 1:
                    # save image
                    img_label = f"{name}_{count}.tif" # create label for image
                    self.save_image(os.path.join(output_path, img_label), crop)

                count += 1 # increase crop counter
                x += h # increase the starting x coordinate value

            x = 0 # reset the starting x coordinate value
            y += h # increase the starting y coordinate value

        os.remove(input_path)

        return


    def process_folder(self, input_folder, output_folder, crop_height, separate_channels, train_threshold, test_threshold):
        # 1. Split into train/test/valid
        self.train_test_valid(input_folder, output_folder, train_threshold, test_threshold)

        # Define split folder paths train/test/valid
        train_folder = os.path.join(output_folder, "train")
        test_folder = os.path.join(output_folder, "test")
        valid_folder = os.path.join(output_folder, "valid")

        # 2. Crop images inside each split
        for split in [train_folder, test_folder, valid_folder]:


            for entry in os.scandir(split):
                if entry.is_file():
                    self.crop_image(crop_height, entry.path, split)

            if separate_channels == True:
                self.split_channels(split)

