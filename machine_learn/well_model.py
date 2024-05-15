import tensorflow as tf


def predict_image(image_path: str, model5_path: str) -> str:
    # image_path = 'content/image_test/new_image.jpg'
    model = tf.keras.models.load_model('machine_learn/model.h5')
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(200, 200))
    image_array = tf.keras.preprocessing.image.img_to_array(img)
    image_array = tf.expand_dims(image_array, axis=0)
    predictions = model.predict(image_array)
    if predictions[0] > 0.5:
        # print("human")
        return "It's a human"
    else:
        # print("pinguin")
        return "It's a pinguin"


