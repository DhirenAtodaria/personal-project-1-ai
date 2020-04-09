# AI - Food Image Classification App

This project is a food image classification web app. It allows the user to upload an image of a specific food item. Upon doing so, the image is then fed to an AI model and the prediction is returned along with certain information which is contained in a database.The project captures the power of image classification with PyTorch and connects to a backend API made using Flask alongside PlotLy Dash as the front end. The app is fully dockerized and deployed on AWS.

## Getting Started

Visit: ... To check out the app.

To use: Upload an image of any food items, the app will automatically predict what food item it is, and subsequently show the corresponding nutritional information for the app.


## Deployment

Deployed using docker to create an image of the app and subsequently deployed on AWS.

## Built With

* [PyTorch](https://pytorch.org//) - Dependency Management
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
* [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) - The cloud DB used
* [Dash](https://dash.plot.ly/) - Used to create the frontend - framework based on React

The first step in the process was to create and train an AI model using Pytorch which will be the basis of the whole app. This was done using a transfer learning approach using a pretrained ResNet-50 as the base. You can find the python notebook containing the code at 
/src/training/.

The second step was to create the backend API used to take the requests. The API connects to the ML model, which accepts incoming requests in the form of binary image data and subsequently goes to the model and returns the prediction. Once the prediction is served, the same response is used to query a MongoDB and retreive information pertaining to the prediction. The code can be found in 
/src/api/

Once the information is received it is sent to a Plotly Dash frontend, which is a data analytics framework based on React to create powerful visuals in Python. The code can be found in /src/dash/
