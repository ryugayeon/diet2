from .img_ObjectDetect import *
from .img_FoodClassify import *
from .img_FoodQuantity import *
from .img_GetDBinfo import *

class DLInference:
    def __init__(self, bytes_img):

        # bytes 데이터를 numpy 배열로 변환
        nparr = np.frombuffer(bytes_img, np.uint8)

        # numpy 배열을 이미지로 변환
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.binary_image = image_rgb


    def predict(self):

        # 객체 검출
        objectdetector = ObjectDetector(image=self.binary_image)
        layerOutputs = objectdetector.detect_objects()
        output_dict = objectdetector.crop_image(layerOutputs)

        # 그릇이나 동전이 탐지되지 않은 경우
        if output_dict in (3, 2):
            return output_dict, output_dict, output_dict, output_dict, output_dict, output_dict, output_dict

        # 음식 분류
        foodclassifier = FoodClassifier(dict=output_dict)
        foodnum = foodclassifier.menupredict()

        # 음식량 추정
        quantitypredictor = FoodQuantityPredictor(dict=output_dict)
        quantity_level = quantitypredictor.quantitypredict()

        # 음식 영양 정보 계산
        foodinfochecker = FoodInfoChecker(foodnum=foodnum, quantity_level=quantity_level)
        foodname, quantity, kcal, carbo, protein, prov = foodinfochecker.get_nutrition_info()

        # 별 문제 없으면 check=0
        check = 0


        return foodname, quantity, kcal, carbo, protein, prov, check
