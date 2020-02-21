import os
from flask import request, jsonify, Flask
import torch
import torch.nn as nn
from torchvision import models
import torchvision.transforms as transforms
import json

import wget
import io
from PIL import Image

app = Flask(__name__)

# loading my model

model_name = 'latestmodeldict.pth'
model_path = f'./ml/models/{model_name}'

if model_name not in os.listdir('./ml/models/'):
    print(f'downloading the trained model {model_name}')
    wget.download(
        "https://github.com/DhirenAtodaria/personal-project-1-ai/releases/download/1.0.0/latestmodeldict.pth",
        out=model_path
    )


model = models.resnet50(pretrained=False)
model.fc = nn.Sequential(
    nn.Linear(2048, 128),
    nn.ReLU(inplace=True),
    nn.Linear(128, 101))

<<<<<<< HEAD
# checking for GPU or CPU
=======
if model_name not in os.listdir('./ml/models/'):
    print(f'downloading the trained model {model_name}')
    wget.download(
        "https://github.com/DhirenAtodaria/personal-project-1-ai/releases/download/1.0.0/latestmodeldict.pth",
        out=model_path
    )

#checking for GPU or CPU
>>>>>>> 4a97a7539c2fb5169239bb2c618c9dfcb6dafc62
trained_weights = torch.load(model_path, map_location='cpu')

model.load_state_dict(trained_weights)
model.eval()
print('PyTorch model loaded !')


def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])])])

    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


<<<<<<< HEAD
class_names = ['apple_pie',
               'baby_back_ribs',
               'baklava',
               'beef_carpaccio',
               'beef_tartare',
               'beet_salad',
               'beignets',
               'bibimbap',
               'bread_pudding',
               'breakfast_burrito',
               'bruschetta',
               'caesar_salad',
               'cannoli',
               'caprese_salad',
               'carrot_cake',
               'ceviche',
               'cheese_plate',
               'cheesecake',
               'chicken_curry',
               'chicken_quesadilla',
               'chicken_wings',
               'chocolate_cake',
               'chocolate_mousse',
               'churros',
               'clam_chowder',
               'club_sandwich',
               'crab_cakes',
               'creme_brulee',
               'croque_madame',
               'cup_cakes',
               'deviled_eggs',
               'donuts',
               'dumplings',
               'edamame',
               'eggs_benedict',
               'escargots',
               'falafel',
               'filet_mignon',
               'fish_and_chips',
               'foie_gras',
               'french_fries',
               'french_onion_soup',
               'french_toast',
               'fried_calamari',
               'fried_rice',
               'frozen_yogurt',
               'garlic_bread',
               'gnocchi',
               'greek_salad',
               'grilled_cheese_sandwich',
               'grilled_salmon',
               'guacamole',
               'gyoza',
               'hamburger',
               'hot_and_sour_soup',
               'hot_dog',
               'huevos_rancheros',
               'hummus',
               'ice_cream',
               'lasagna',
               'lobster_bisque',
               'lobster_roll_sandwich',
               'macaroni_and_cheese',
               'macarons',
               'miso_soup',
               'mussels',
               'nachos',
               'omelette',
               'onion_rings',
               'oysters',
               'pad_thai',
               'paella',
               'pancakes',
               'panna_cotta',
               'peking_duck',
               'pho',
               'pizza',
               'pork_chop',
               'poutine',
               'prime_rib',
               'pulled_pork_sandwich',
               'ramen',
               'ravioli',
               'red_velvet_cake',
               'risotto',
               'samosa',
               'sashimi',
               'scallops',
               'seaweed_salad',
               'shrimp_and_grits',
               'spaghetti_bolognese',
               'spaghetti_carbonara',
               'spring_rolls',
               'steak',
               'strawberry_shortcake',
               'sushi',
               'tacos',
               'takoyaki',
               'tiramisu',
               'tuna_tartare',
               'waffles']
=======
class_names = json.load(open('./classes.json'))
>>>>>>> 4a97a7539c2fb5169239bb2c618c9dfcb6dafc62


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return class_names[predicted_idx]

print(class_names["0"])


@app.route('/predict', methods=['POST'])
def predict_rating():
    '''
    Endpoint to predict the image of the food
    '''
    if request.method == 'POST':
        file = request.files['file']
        image_bytes = file.read()
        prediction_name = get_prediction(image_bytes=image_bytes)
        return jsonify({'food_name': prediction_name})


if __name__ == '__main__':
    app.run(debug=True)
