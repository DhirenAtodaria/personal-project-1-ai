import sys
import os
import random
from tqdm import tqdm

from flask import Blueprint, request, jsonify, Flask
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
import torchvision.transforms as transforms
import json

import wget
import io
from PIL import Image

app = Flask(__name__)

#loading my model

model_name = 'latestmodeldict.pth'
model_path = f'./ml/models/{model_name}'
model = models.resnet50(pretrained=False)
model.fc = nn.Sequential(
    nn.Linear(2048, 128),
    nn.ReLU(inplace=True),
    nn.Linear(128, 101))

if model_name not in os.listdir('./ml/models/'):
    print(f'downloading the trained model {model_name}')
    wget.download(
        "https://github.com/DhirenAtodaria/personal-project-1-ai/releases/download/1.0.0/latestmodeldict.pth",
        out=model_path
    )

#checking for GPU or CPU
trained_weights = torch.load(model_path, map_location='cpu')

model.load_state_dict(trained_weights)
model.eval()
print('PyTorch model loaded !')

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])])])
    
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


class_names = json.load(open('./classes.json'))


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
        return jsonify({'food_name' : prediction_name})

if __name__ == '__main__':
    app.run(debug=True)


