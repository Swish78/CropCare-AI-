from PIL import Image
import numpy as np
from keras_preprocessing.image import load_img, img_to_array
import tensorflow
# Define paths to your model files
model_path_inception = '/Users/swayampatil/pdfchatbot/farmerchatbot/Banana/model_inception.keras'
model_path_resnet = '/Users/swayampatil/pdfchatbot/farmerchatbot/Banana/model_resnet.keras'
model_path_lenet = '/Users/swayampatil/pdfchatbot/farmerchatbot/Banana/model_lenet.keras'

# Load each model
# model_inception = load_model(model_path_inception)
model_resnet = tensorflow.keras.models.load_model(model_path_resnet)
model_lenet = tensorflow.keras.models.load_model(model_path_lenet)

# Mapping from class index to disease name
class_mapping = {
    0: "Banana Black Sigatoka Disease",
    1: "Banana Bract Mosaic Virus Disease",
    2: "Banana Healthy Leaf",
    3: "Banana Insect Pest Disease",
    4: "Banana Moko Disease",
    5: "Banana Panama Disease",
    6: "Banana Yellow Sigatoka Disease"
}

# Function to preprocess an image
def preprocess_image(image_path, target_size):
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize
    return img_array

# Function to predict using each model and aggregate predictions
def predict_with_voting(image_path):
    input_size = (128, 128, 3)

    # Preprocess the image for each model
    img_lenet = preprocess_image(image_path, input_size)
    img_resnet = preprocess_image(image_path, input_size)
    # img_inception = preprocess_image(image_path, input_size)

    # Step 1: Make predictions using each model
    pred_lenet = model_lenet.predict(img_lenet)
    pred_resnet = model_resnet.predict(img_resnet)
    # pred_inception = model_inception.predict(img_inception)

    # Step 2: Aggregate predicted probabilities (soft voting)
    # final_pred_prob = (pred_lenet + pred_resnet + pred_inception) / 3
    final_pred_prob = (pred_lenet + pred_resnet) / 2

    # Step 3: Predict class based on the aggregated probabilities
    final_pred_class = np.argmax(final_pred_prob, axis=1)

    # Map predicted class indices to disease names
    final_pred_disease = [class_mapping[class_index] for class_index in final_pred_class]

    return final_pred_disease

# Example usage
image_path = 'Banana/Augmented Banana Bract Mosaic Virus Disease (102).jpg'
predicted_class = predict_with_voting(image_path)
print("Predicted Class:", predicted_class)
