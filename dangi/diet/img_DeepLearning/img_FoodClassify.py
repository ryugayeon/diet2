import tensorflow as tf
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from .img_ModelPreloader import classify_model, foodclass

class FoodClassifier:
    def __init__(self, dict):
        self.images_dict = dict
        self.foodnames = foodclass

    def menupredict(self):

        # 이미지 전처리
        img = self.images_dict['dish']
        img_size = (224, 224)
        img = cv2.resize(img, img_size)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        bestmodel = classify_model

        # 모델 예측
        preds = bestmodel.predict(img)
        predicted_index = preds.argmax()

        foodmenu = self.foodnames.iloc[predicted_index]['Class Name']
        return foodmenu