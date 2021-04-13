from Services.api_call_service import api_call
from Services.redis_service import get_val
from Services.type_sense.type_sense_crud_service import create_collection
from Services.type_sense.typesense_dic_generator import generate_typsns_data
from db_models.models.images_model import Image
from settings import IMAGE_RECOG_PROBABILITY_THRESHOLD, TYPESENSE_IMAGES_INDEX
from db_models.models.tags_model import TagModel


def index_image(file_data, url, notes_model_obj, content_length, user_obj, file_name):
    image_model_obj = Image()
    image_model_obj.url = url
    image_model_obj.image_size = content_length
    image_model_obj.user_id = user_obj
    image_model_obj.notes_id = notes_model_obj
    image_model_obj.save()
    ocr_results = str()
    image_labels_results_list = list()
    OCR_ENDPOINT = get_val(key="OCR_ENDPOINT")
    IMAGE_LABEL_ENPOINT = get_val("IMAGE_LABEL_ENPOINT")

    ocr_results_data = api_call(file_to_process=file_data, binary=True, end_point=OCR_ENDPOINT,
                                file_name=file_name, status=True, image=True)
    if ocr_results_data["status_code"] == 200:
        ocr_results_raw = ocr_results_data["response_data"]
        print(ocr_results_raw)
        for val_array in ocr_results_raw["text"]:
            for val in val_array:
                if len(val.strip()) != 0:
                    ocr_results = ocr_results + " " + val
        print(ocr_results)
    image_labels_results_data = api_call(file_to_process=file_data, binary=True, end_point=IMAGE_LABEL_ENPOINT,
                                         file_name=file_name, status=True, image=True)
    print(image_labels_results_data)
    if image_labels_results_data["status_code"] == 200:
        image_labels_results = image_labels_results_data["response_data"]
        print(image_labels_results)
        for val in image_labels_results["predictions"]:
            print(val["probability"])
            if val["probability"] > IMAGE_RECOG_PROBABILITY_THRESHOLD:
                print("in label threshhold")
                print(val["label"])
                image_labels_results_list.append(val["label"])
    print(image_labels_results_list)
    if ocr_results is None:
        ocr_results = ""
    print("ocr_results")
    print(ocr_results)
    print(type(ocr_results))
    tps_dic = generate_typsns_data(obj=image_model_obj, ocr_text=ocr_results, labels_list=image_labels_results_list)
    print("tps dic ocr")
    print(tps_dic["ocr"])
    print(type(tps_dic["ocr"]))
    print(tps_dic)
    create_collection(data=tps_dic, index=TYPESENSE_IMAGES_INDEX)
