import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense


class FoodClassificator:
    model = None

    @staticmethod
    def get_model():
        if FoodClassificator.model is not None:
            return FoodClassificator.model
        else:
            pre_model = tf.keras.applications.MobileNetV2(
                input_shape=(224, 224, 3),
                include_top=False,
                weights=None,
                pooling='avg',
                classes=101
            )
            x = pre_model.layers[-1].output
            output = Dense(101, activation='softmax')(x)
            model = Model(pre_model.input, output)
            model.load_weights('food-detect-mobinet-weights.h5')

            FoodClassificator.model = model
            return model

    @staticmethod
    def predict(images):
        model = FoodClassificator.get_model()

        return model.predict(images)
