from flask import Flask, request, render_template, send_file
import os
from PIL import Image
from io import BytesIO
from ultralytics import YOLO

app = Flask(__name__)

model = YOLO('yolov8n.pt')


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def get_box_position(xyxy, image_height):
    xmin, ymin, xmax, ymax = xyxy

    box_height = ymax - ymin

    box_center_y = ymin + box_height / 2

    if box_center_y < image_height / 3:
        vertical_position = 'top'
    elif box_center_y > 2 * image_height / 3:
        vertical_position = 'bottom'
    else:
        vertical_position = 'center'

    if xmin < image_height / 3:
        horizontal_position = 'left'
    elif xmax > 2 * image_height / 3:
        horizontal_position = 'right'
    else:
        horizontal_position = 'center'

    position = f"{vertical_position}-{horizontal_position}"

    return position


def yolo_result_to_sentence(yolo_result, image_height):
    sentences = []

    cls_list = yolo_result.boxes.cls.numpy()

    bbox_list = yolo_result.boxes.xyxy.squeeze().tolist()

    if len(cls_list) == 1:
        class_labels = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket',
                        39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}

        class_label = class_labels.get(cls_list[0], 'unknown class')
        sentence = f"There is a {class_label} with at position "
        sentence += f"{get_box_position(bbox_list, image_height)}."
        sentences.append(sentence)
        return sentences

    class_labels = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket',
                    39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}

    for cls, bbox in zip(cls_list, bbox_list):
        class_label = class_labels.get(cls, 'unknown class')

        sentence = f"There is a {class_label} with at position "
        sentence += f"{get_box_position(bbox, image_height)}."
        sentences.append(sentence)

    return sentences


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        if file.filename == '':
            return 'No selected file'

        if file:
            img = Image.open(file)

            results = model(img)

            if True:
                results[0].show()

            return yolo_result_to_sentence(results[0], img.height)
    return ["Error, Please try again later!"]


if __name__ == '__main__':
    app.run(debug=True)
