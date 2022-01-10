from flask import Flask, request, Response, jsonify
import numpy as np
import cv2

from FoodClassificator import FoodClassificator

app = Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    health = FoodClassificator.get_model() is not None

    status = 200 if health else 404
    return Response(response="\n", status=status, mimetype="application/json")


@app.route('/invocations', methods=["POST"])
def food_classification():
    input_json = request.get_json(force=True)
    video = cv2.VideoCapture(input_json["videoUrl"])

    fps = video.get(cv2.CAP_PROP_FPS)

    success, image = video.read()
    count = 0
    count_image = 0
    images = np.zeros([int(video.get(cv2.CAP_PROP_FRAME_COUNT) // fps + 1), 224, 224, 3])

    while success:
        if count % fps == 0:
            image = cv2.resize(image, (224, 224))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            images[count_image] = image
            count_image += 1
        count += 1
        success, image = video.read()

    predict = FoodClassificator.predict(images)
    classify_array = (predict == predict.max(axis=1, keepdims=True)).astype(int)
    mask = np.expand_dims(1 / (1 + np.exp(4 - 7 * np.arange(0, len(classify_array)) / len(classify_array))), axis=-1)
    predict_video = np.sum(classify_array * mask, axis=0)
    video_vector = predict_video / np.sum(predict_video) * 10

    return jsonify({"vector": video_vector.tolist()})
