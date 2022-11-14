from tkinter import Image
# from xml.etree.ElementTree import tostring
# from itsdangerous import base64_encode
# from matplotlib.image import imsave
import numpy as np
import cv2
import os
# from matplotlib import pyplot as plt
# from skimage.io import imread
# from skimage.transform import resize
# from skimage import exposure
from skimage.metrics import structural_similarity as ssim
from skimage.feature import hog
from flask import Flask,request
from flask_restful import Resource,Api
from flask_cors import CORS

import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)

CORS(app)

api = Api(app)


class quality(Resource):
    imgformat = ""
    def check_color_consistency(self):
        c = 128
        n = 127

        img_ = "./imageToSave." + self.imgformat
        image_gray_scale = cv2.imread(img_, cv2.IMREAD_GRAYSCALE)

        # image_RGB = cv2.imread(img_)[:, :, ::-1]
        '''
        plt.figure(figsize=(50, 25))
        plt.subplot(1, 1, 1)
        plt.imshow(image_RGB)
        '''

        height, width = image_gray_scale.shape
        cols = int(width / c)
        rows = int(height / c)
        grey_matrix = np.zeros((rows, cols), np.uint8)

        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                center = 0
                center = np.mean(image_gray_scale[i * c:i * c + n, j * c:j * c + n])

                first = np.mean(image_gray_scale[(i - 1) * c:(i - 1) * c + n, (j - 1) * c:(j - 1) * c + n])
                second = np.mean(image_gray_scale[(i - 1) * c:(i - 1) * c + n, (j) * c:(j) * c + n])
                third = np.mean(image_gray_scale[(i - 1) * c:(i - 1) * c + n, (j + 1) * c:(j + 1) * c + n])
                fourth = np.mean(image_gray_scale[(i) * c:(i) * c + n, (j - 1) * c:(j - 1) * c + n])
                five = np.mean(image_gray_scale[(i) * c:(i) * c + n, (j + 1) * c:(j + 1) * c + n])
                six = np.mean(image_gray_scale[(i + 1) * c:(i + 1) * c + n, (j - 1) * c:(j - 1) * c + n])
                seven = np.mean(image_gray_scale[(i + 1) * c:(i + 1) * c + n, (j) * c:(j) * c + n])
                eight = np.mean(image_gray_scale[(i + 1) * c:(i + 1) * c + n, (j + 1) * c:(j + 1) * c + n])
                percentage = 0

                percentage += 100 * min(center, first) / max(center, first)
                percentage += 100 * min(center, second) / max(center, second)
                percentage += 100 * min(center, third) / max(center, third)
                percentage += 100 * min(center, fourth) / max(center, fourth)
                percentage += 100 * min(center, five) / max(center, five)
                percentage += 100 * min(center, six) / max(center, six)
                percentage += 100 * min(center, seven) / max(center, seven)
                percentage += 100 * min(center, eight) / max(center, eight)
                print(i, j)
                grey_matrix[i][j] = int(percentage / 8)

        grey_matrix = np.delete(grey_matrix, 0, 0)
        grey_matrix = np.delete(grey_matrix, 0, 1)
        grey_matrix = np.delete(grey_matrix, -1, 0)
        grey_matrix = np.delete(grey_matrix, -1, 1)

        '''
        for r in grey_matrix:
            for c in r:
                print(c, end=" ")
            print()
        '''

        Flatten_SSIM_Matrix = grey_matrix.flatten()
        list_set = set(Flatten_SSIM_Matrix)
        unique_list = (list(list_set))
        unique_list.sort()
        print("Unique % \t\t", unique_list)

        Repr_Flatten_SSIM_Matrix = repr(Flatten_SSIM_Matrix)
        count = []
        for i in unique_list:
            count.append(Repr_Flatten_SSIM_Matrix.count(str(i)))
        print("Count % \t\t", count)

        Z = [x for _, x in sorted(zip(count, unique_list))]
        print("Sorted % list \t\t", Z)
        # print("Color Consistency: ",np.mean(Z[-1:-4:-1]) , "%")

        last = np.sum(count[-1:-4:-1])
        all_sub_last = np.sum(count[-4::-1])
        all_ = np.sum(count[-1::-1])

        color_consistency = 100 * last / all_
        color_inconsistency = 100 * all_sub_last / all_

        # print("Color Consistency:\t", 100 * last / all_, "%")
        # print("Color Inconsistency:\t", 100 * all_sub_last / all_, "%")

        return color_consistency

    def check_dimensional_stability(self):
        c = 128
        n = 127
        img_ = "./imageToSave." + self.imgformat
        # image_RGB = cv2.imread(img_)[:, :, ::-1]
        image_gray_scale = cv2.imread(img_, cv2.IMREAD_GRAYSCALE)
        print(image_gray_scale.shape)
        (thresh, image_binary_thr) = cv2.threshold(image_gray_scale, n, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        x = cv2.adaptiveThreshold(image_gray_scale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        '''
        plt.figure(figsize=(50, 25))
        plt.subplot(1, 1, 1)
        plt.imshow(image_RGB)
        plt.figure(figsize=(50, 25))
        plt.subplot(1, 1, 1)
        plt.imshow(image_gray_scale, cmap="gray")
        plt.figure(figsize=(50, 25))
        plt.subplot(1, 1, 1)
        plt.imshow(c, cmap='binary')
        '''
        fd, hog_image = hog(x, orientations=3, pixels_per_cell=(c, c),
                            cells_per_block=(1, 1), visualize=True, multichannel=False)
        '''
        plt.figure(figsize=(50, 25))
        plt.subplot(1, 1, 1)
        plt.imshow(hog_image, cmap='binary')
        '''

        height, width = hog_image.shape
        cols = int(width / c)
        rows = int(height / c)
        SSIM_Matrix = np.zeros((rows, cols), np.uint8)
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                sum_val = 0

                sum_val += ssim(hog_image[i * c:i * c + n, j * c:j * c + n],
                                hog_image[(i - 1) * c:(i - 1) * c + n, (j - 1) * c:(j - 1) * c + n])
                sum_val += ssim(hog_image[i * c:i * c + n, j * c:j * c + n],
                                hog_image[(i - 1) * c:(i - 1) * c + n, (j) * c:(j) * c + n])
                sum_val += ssim(hog_image[i * c:i * c + n, j * c:j * c + n],
                                hog_image[(i - 1) * c:(i - 1) * c + n, (j + 1) * c:(j + 1) * c + n])

                sum_val += ssim(hog_image[i * c:i * c + n, j * c:j * c + n],
                                hog_image[(i) * c:(i) * c + n, (j - 1) * c:(j - 1) * c + n])
                sum_val += ssim(hog_image[i * c:i * c + n, j * c:j * c + n],
                                hog_image[(i) * c:(i) * c + n, (j + 1) * c:(j + 1) * c + n])

                sum_val += ssim(hog_image[i * c:i * c + n, j * c:j * c + n],
                                hog_image[(i + 1) * c:(i + 1) * c + n, (j - 1) * c:(j - 1) * c + n])
                sum_val += ssim(hog_image[i * c:i * c + n, j * c:j * c + n],
                                hog_image[(i + 1) * c:(i + 1) * c + n, (j) * c:(j) * c + n])
                sum_val += ssim(hog_image[i * c:i * c + n, j * c:j * c + n],
                                hog_image[(i + 1) * c:(i + 1) * c + n, (j + 1) * c:(j + 1) * c + n])

                SSIM_Matrix[i][j] = int(100 * sum_val / 8)

        SSIM_Matrix = np.delete(SSIM_Matrix, 0, 0)
        SSIM_Matrix = np.delete(SSIM_Matrix, 0, 1)
        SSIM_Matrix = np.delete(SSIM_Matrix, -1, 0)
        SSIM_Matrix = np.delete(SSIM_Matrix, -1, 1)

        for r in SSIM_Matrix:
            for c in r:
                print(c, end=" ")
            print()

        Flatten_SSIM_Matrix = SSIM_Matrix.flatten()
        list_set = set(Flatten_SSIM_Matrix)
        unique_list = (list(list_set))
        unique_list.sort()
        # print("Unique % occurence\t\t", unique_list)

        Repr_Flatten_SSIM_Matrix = repr(Flatten_SSIM_Matrix)
        count = []
        for i in unique_list:
            count.append(Repr_Flatten_SSIM_Matrix.count(str(i)))
        # print("Count % occurence\t\t", count)

        Z = [x for _, x in sorted(zip(count, unique_list))]
        # print("Sorted % list \t\t\t", Z)

        last = np.sum(count[-1:-2:-1])
        all_sub_last = np.sum(count[-2::-1])
        all_ = np.sum(count[-1::-1])

        dimensional_stability = 100 * last / all_
        dimensional_instability = 100 * all_sub_last / all_

        # print("Dimensional Stability:\t\t", 100 * last / all_, "%")
        # print("Dimensional Instability:\t", 100 * all_sub_last / all_, "%")

        return dimensional_stability
        # return jsonify(req)

    def check_fabric_dimension(self):
        c = 128
        n = 127
        img_ = "./imageToSave."+ self.imgformat

        img = cv2.imread(img_, 0)

        # image_RGB = cv2.imread(img_)[:, :, ::-1]
        '''
        plt.figure(figsize=(50, 25))
        plt.subplot(1, 1, 1)
        plt.imshow(image_RGB, cmap='gray')
        # cv2.imshow('Original Image',img)
        # cv2.waitKey(0)
        plt.figure(figsize=(50, 25))
        plt.subplot(1, 1, 1)
        plt.imshow(img, cmap='gray')
        # cv2.destroyAllWindows()
        '''

        # ------------------Equalized Otsu's thresholding-----------

        th3 = cv2.equalizeHist(img)
        # cv2.imshow('Applying Equalized Otsu Threshold',th3)
        # plt.figure(figsize=(50, 25))
        # plt.subplot(1, 1, 1)
        # plt.imshow(th3, cmap='binary')
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # ------------------Applying HOG method------------
        fd, hog_image = hog(th3, orientations=9, pixels_per_cell=(8, 8),
                            cells_per_block=(2, 2), visualize=True, multichannel=False)

        cv2.imwrite('Pic1.jpg', hog_image)
        image = cv2.imread('Pic1.jpg', 0)

        # plt.figure(figsize=(50, 25))
        # plt.subplot(1, 1, 1)
        # plt.imshow(image, cmap='gray')

        # cv2.imshow('hog',image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # --------------Dilution-1 times------------

        for i in range(0, 1):
            dilated = cv2.dilate(image.copy(), None, iterations=i + 1)
            # cv2.imshow("Dilated {} times".format(i + 1), dilated)
            # plt.figure(figsize=(50, 25))
            # plt.subplot(1, 1, 1)
            # plt.imshow(dilated, cmap='gray')

        # cv2.imwrite('Images/FD/Diluted 1 Times.jpg', dilated)
        # cv2.waitKey(0)

        # cv2.destroyAllWindows()

        # ------------------Adaptive Threshold---------------
        image = cv2.adaptiveThreshold(dilated, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        # cv2.imshow("Pattern ", image)
        cv2.imwrite('Images/FD/Pattern.jpg', dilated)
        # cv2.waitKey(0)



        img = cv2.imread("response.jpg" , 0)
        img = Image.fromarray(img.astype("uint8"))
        rawb = BytesIO()
        img.save(rawb , "PNG")
        rawb.seek(0)
        imgb64 = base64.b64encode(rawb.read())

        imgb64 = "data:image/jpeg;base64," + str(imgb64).split("\'")[1]
        return imgb64
        '''
        plt.figure(figsize=(50, 25))
        plt.subplot(1, 1, 1)
        plt.imshow(image, cmap='gray')
        '''
        # cv2.destroyAllWindows()

        # return jsonify([{'Message': 'Success_Module_FD', 'Output': [image]}])

    def generate_report(self , x):
        if (x == 1):
            return self.check_color_consistency()
        if (x == 2):
            return self.check_fabric_dimension()
        if (x == 3):
            return self.check_dimensional_stability()

    def post(self):
        req = (request.get_json())["image"]
        req = str(req)
        req = req.split(";base64,")
        self.imgformat = (req[0].split("image/"))[1]
        print(self.imgformat)
        image = base64.b64decode(req[1])
        with open("imageToSave." + self.imgformat, "wb") as fh:
            fh.write(image)


        x = req = (request.get_json())["fab"]
        print(x)

        return self.generate_report(x)



api.add_resource(quality,'/quality')



#api.add_resource(module_DS,'/module1')
#api.add_resource(module_FD,'/module2')
#api.add_resource(module_CC,'/module3')

# if __name__ == '__main__':
app.run(host='0.0.0.0')