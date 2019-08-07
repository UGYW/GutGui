from GutGuiModules.utility import *

class Introduction:
    def __init__(self, introduction_frame):
        self.root = introduction_frame

        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.image4 = None
        self.image5 = None
        self.image6 = None
        self.image7 = None
        self.image8 = None
        self.image9 = None
        self.image10 = None
        self.image11 = None
        self.image12 = None
        self.image13 = None

        self.load_images()

    def load_images(self):
        # image 1
        image1_data = image_to_array('./image1.png')
        self.image1 = make_image(self.root, image1_data, row=0, column=0, columnspan=1, rowspan=1, lower_scale_value=0, upper_scale_value=0, color_rgb=PASTEL_PINK_RGB, figwidth=3, figheight=3, original=True)[1]

        # image 2
        image2_data = image_to_array('./image2.jpg')
        self.image2 = make_image(self.root, image2_data, row=1, column=0, columnspan=1, rowspan=1, lower_scale_value=0, upper_scale_value=0, color_rgb=PASTEL_PINK_RGB, figwidth=3, figheight=1, original=True)[1]

        # image 3
        image3_data = image_to_array('./image3.jpg')
        self.image3 = make_image(self.root, image3_data, row=2, column=0, columnspan=1, rowspan=1, lower_scale_value=0, upper_scale_value=0, color_rgb=PASTEL_PINK_RGB, figwidth=3, figheight=1, original=True)[1]

        # image 4
        image4_data = image_to_array('./image4.jpg')
        self.image4 = make_image(self.root, image4_data, row=3, column=0, columnspan=1, rowspan=1, lower_scale_value=0, upper_scale_value=0, color_rgb=PASTEL_PINK_RGB, figwidth=3, figheight=1, original=True)[1]

        # image 5
        image5_data = image_to_array('./image5.jpg')
        self.image5 = make_image(self.root, image5_data, row=4, column=0, columnspan=1, rowspan=1, lower_scale_value=0, upper_scale_value=0, color_rgb=PASTEL_PINK_RGB, figwidth=3, figheight=2, original=True)[1]