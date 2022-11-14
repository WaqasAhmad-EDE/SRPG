from tkinter import Image
from xml.etree.ElementTree import tostring
from itsdangerous import base64_encode
from matplotlib.image import imsave
import numpy as np
import cv2
import os
import jsonpickle
from matplotlib import pyplot as plt
from skimage.io import imread
from skimage.transform import resize
from skimage import exposure
from skimage.metrics import structural_similarity as ssim
from skimage.feature import hog
from flask import Flask, make_response,request,jsonify, send_file
from flask_restful import Resource,Api
from flask_cors import CORS

import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)

CORS(app)

api = Api(app)


class module_DS(Resource):
    def post(self):
        req = (request.get_json())["image"]
        req =str(req)
        req = req.split(";base64,")
        imgformat = (req[0].split("image/"))[1]
        print(imgformat)
        image = base64.b64decode(req[1])
        with open("imageToSave." + imgformat, "wb") as fh:
            fh.write(image)

        img_ = "./imageToSave."+imgformat
        image_RGB = cv2.imread(img_)[:, :, ::-1]
        image_gray_scale = cv2.imread(img_, cv2.IMREAD_GRAYSCALE)
        print(image_gray_scale.shape)
        (thresh, image_binary_thr) = cv2.threshold(image_gray_scale, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        c = cv2.adaptiveThreshold(image_gray_scale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
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
        fd, hog_image = hog(c, orientations=3, pixels_per_cell=(128, 128),
                            cells_per_block=(1, 1), visualize=True, multichannel=False)
        '''
        plt.figure(figsize=(50, 25))
        plt.subplot(1, 1, 1)
        plt.imshow(hog_image, cmap='binary')
        '''

        height, width = hog_image.shape
        cols = int(width / 128)
        rows = int(height / 128)
        SSIM_Matrix = np.zeros((rows, cols), np.uint8)
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                sum_val = 0

                sum_val += ssim(hog_image[i * 128:i * 128 + 127, j * 128:j * 128 + 127],
                                hog_image[(i - 1) * 128:(i - 1) * 128 + 127, (j - 1) * 128:(j - 1) * 128 + 127])
                sum_val += ssim(hog_image[i * 128:i * 128 + 127, j * 128:j * 128 + 127],
                                hog_image[(i - 1) * 128:(i - 1) * 128 + 127, (j) * 128:(j) * 128 + 127])
                sum_val += ssim(hog_image[i * 128:i * 128 + 127, j * 128:j * 128 + 127],
                                hog_image[(i - 1) * 128:(i - 1) * 128 + 127, (j + 1) * 128:(j + 1) * 128 + 127])

                sum_val += ssim(hog_image[i * 128:i * 128 + 127, j * 128:j * 128 + 127],
                                hog_image[(i) * 128:(i) * 128 + 127, (j - 1) * 128:(j - 1) * 128 + 127])
                sum_val += ssim(hog_image[i * 128:i * 128 + 127, j * 128:j * 128 + 127],
                                hog_image[(i) * 128:(i) * 128 + 127, (j + 1) * 128:(j + 1) * 128 + 127])

                sum_val += ssim(hog_image[i * 128:i * 128 + 127, j * 128:j * 128 + 127],
                                hog_image[(i + 1) * 128:(i + 1) * 128 + 127, (j - 1) * 128:(j - 1) * 128 + 127])
                sum_val += ssim(hog_image[i * 128:i * 128 + 127, j * 128:j * 128 + 127],
                                hog_image[(i + 1) * 128:(i + 1) * 128 + 127, (j) * 128:(j) * 128 + 127])
                sum_val += ssim(hog_image[i * 128:i * 128 + 127, j * 128:j * 128 + 127],
                                hog_image[(i + 1) * 128:(i + 1) * 128 + 127, (j + 1) * 128:(j + 1) * 128 + 127])

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
        #print("Unique % occurence\t\t", unique_list)

        Repr_Flatten_SSIM_Matrix = repr(Flatten_SSIM_Matrix)
        count = []
        for i in unique_list:
            count.append(Repr_Flatten_SSIM_Matrix.count(str(i)))
        #print("Count % occurence\t\t", count)

        Z = [x for _, x in sorted(zip(count, unique_list))]
        #print("Sorted % list \t\t\t", Z)

        last = np.sum(count[-1:-2:-1])
        all_sub_last = np.sum(count[-2::-1])
        all_ = np.sum(count[-1::-1])

        dimensional_stability = 100*last/all_
        dimensional_instability = 100*all_sub_last/all_

        #print("Dimensional Stability:\t\t", 100 * last / all_, "%")
        #print("Dimensional Instability:\t", 100 * all_sub_last / all_, "%")

        return dimensional_stability
        # return jsonify(req)

class module_FD(Resource):
    def post(self):
        req = (request.get_json())["image"]
        req =str(req)
        req = req.split(";base64,")
        imgformat = (req[0].split("image/"))[1]
        print(imgformat)
        image = base64.b64decode(req[1])
        with open("imageToSave." + imgformat, "wb") as fh:
            fh.write(image)

        img_ = "./imageToSave."+imgformat

        img = cv2.imread(img_, 0)

        image_RGB = cv2.imread(img_)[:, :, ::-1]
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
        #plt.figure(figsize=(50, 25))
        #plt.subplot(1, 1, 1)
        #plt.imshow(th3, cmap='binary')
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # ------------------Applying HOG method------------
        fd, hog_image = hog(th3, orientations=9, pixels_per_cell=(8, 8),
                            cells_per_block=(2, 2), visualize=True, multichannel=False)

        cv2.imwrite('Pic1.jpg', hog_image)
        image = cv2.imread('Pic1.jpg', 0)

        #plt.figure(figsize=(50, 25))
        #plt.subplot(1, 1, 1)
        #plt.imshow(image, cmap='gray')

        # cv2.imshow('hog',image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # --------------Dilution-1 times------------

        for i in range(0, 1):
            dilated = cv2.dilate(image.copy(), None, iterations=i + 1)
            # cv2.imshow("Dilated {} times".format(i + 1), dilated)
            #plt.figure(figsize=(50, 25))
            #plt.subplot(1, 1, 1)
            #plt.imshow(dilated, cmap='gray')

        # cv2.imwrite('diluted.jpg', dilated)
        # cv2.waitKey(0)
        # print(dilated.shape)

        # cv2.destroyAllWindows()

        # ------------------Adaptive Threshold---------------
        image = cv2.adaptiveThreshold(dilated, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        cv2.imwrite('response.jpg', image)


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



class module_CC(Resource):
    def post(self):
        req = (request.get_json())["image"]
        req =str(req)
        req = req.split(";base64,")
        imgformat = (req[0].split("image/"))[1]
        print(imgformat)
        image = base64.b64decode(req[1])
        with open("imageToSave." + imgformat, "wb") as fh:
            fh.write(image)

        img_ = "./imageToSave."+imgformat
        image_gray_scale = cv2.imread(img_, cv2.IMREAD_GRAYSCALE)

        image_RGB = cv2.imread(img_)[:, :, ::-1]
        '''
        plt.figure(figsize=(50, 25))
        plt.subplot(1, 1, 1)
        plt.imshow(image_RGB)
        '''

        height, width = image_gray_scale.shape
        cols = int(width / 128)
        rows = int(height / 128)
        grey_matrix = np.zeros((rows, cols), np.uint8)

        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                center = 0
                center = np.mean(image_gray_scale[i * 128:i * 128 + 127, j * 128:j * 128 + 127])

                first = np.mean(image_gray_scale[(i - 1) * 128:(i - 1) * 128 + 127, (j - 1) * 128:(j - 1) * 128 + 127])
                second = np.mean(image_gray_scale[(i - 1) * 128:(i - 1) * 128 + 127, (j) * 128:(j) * 128 + 127])
                third = np.mean(image_gray_scale[(i - 1) * 128:(i - 1) * 128 + 127, (j + 1) * 128:(j + 1) * 128 + 127])
                fourth = np.mean(image_gray_scale[(i) * 128:(i) * 128 + 127, (j - 1) * 128:(j - 1) * 128 + 127])
                five = np.mean(image_gray_scale[(i) * 128:(i) * 128 + 127, (j + 1) * 128:(j + 1) * 128 + 127])
                six = np.mean(image_gray_scale[(i + 1) * 128:(i + 1) * 128 + 127, (j - 1) * 128:(j - 1) * 128 + 127])
                seven = np.mean(image_gray_scale[(i + 1) * 128:(i + 1) * 128 + 127, (j) * 128:(j) * 128 + 127])
                eight = np.mean(image_gray_scale[(i + 1) * 128:(i + 1) * 128 + 127, (j + 1) * 128:(j + 1) * 128 + 127])
                percentage = 0

                percentage += 100 * min(center, first) / max(center, first)
                percentage += 100 * min(center, second) / max(center, second)
                percentage += 100 * min(center, third) / max(center, third)
                percentage += 100 * min(center, fourth) / max(center, fourth)
                percentage += 100 * min(center, five) / max(center, five)
                percentage += 100 * min(center, six) / max(center, six)
                percentage += 100 * min(center, seven) / max(center, seven)
                percentage += 100 * min(center, eight) / max(center, eight)
                grey_matrix[i][j] = int(percentage / 8)

        grey_matrix = np.delete(grey_matrix, 0, 0)
        grey_matrix = np.delete(grey_matrix, 0, 1)
        grey_matrix = np.delete(grey_matrix, -1, 0)
        grey_matrix = np.delete(grey_matrix, -1, 1)

        
        for r in grey_matrix:
            for c in r:
                print(c, end=" ")
            print()
        

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

        color_consistency = 100*last/all_
        color_inconsistency = 100*all_sub_last/all_

        #print("Color Consistency:\t", 100 * last / all_, "%")
        #print("Color Inconsistency:\t", 100 * all_sub_last / all_, "%")

        return color_consistency


api.add_resource(module_CC,'/module1')
api.add_resource(module_FD,'/module2')
api.add_resource(module_DS,'/module3')

# if __name__ == '__main__':
app.run(host='0.0.0.0')