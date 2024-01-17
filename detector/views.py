# Create your views here.
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        # Save the uploaded file to a specific location
        fs.save(uploaded_file.name, uploaded_file)
        # Process the file here or perform any further actions
        
        return render(request, 'main.html')
    return render(request, 'main.html')

def next_page(request):
  return render(request, 'next.html')  

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

import joblib
import numpy as np
from .models import FraudDetection
import json

model = joblib.load('G:/pu sallybus and releted stuff/Raj. policehackthon/New folder/frauddetector/detector/static/credit_fraud.pkl')

def running(request):
    note = """
    Credit Card Fraud Detection API 🙌🏻

    Note: add "/docs" to the URL to get the Swagger UI Docs or "/redoc"
    """
    return JsonResponse({"message": note})

def favicon(request):
    return JsonResponse({"message": "Favicon not implemented yet."})

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        data = json.loads(request.body)                
        features = np.array([
            [float(data['step']), int(data['types']), float(data['amount']),
             float(data['oldbalanceorig']), float(data['newbalanceorig']),
             float(data['oldbalancedest']), float(data['newbalancedest']),
             float(data['isflaggedfraud'])]
        ])
        predictions = model.predict(features)
        if predictions == 1:
            result = {"result": "fraudulent"}
        elif predictions == 0:
            result = {"result": "not fraudulent"}
        return JsonResponse(result)
    else:
        return JsonResponse({"error": "Invalid request method."})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.shortcuts import render
from PIL import Image
import cv2
import numpy as np
import io
import json
import tensorflow as tf
from .models import ImagePrediction  # Assuming you have a model for image predictions

# Load the image classification model
image_model = tf.keras.models.load_model('G:/pu sallybus and releted stuff/Raj. policehackthon/New folder/frauddetector/detector/static/model.h5')

@csrf_exempt
def classify_image(request):
    if request.method == 'POST':
        # Get the uploaded image from the request
        image_file = request.FILES.get('image')
        
        if not image_file:
            return JsonResponse({"error": "No image provided."})
        
        # Read the image and preprocess it for the model
        image = Image.open(image_file)
        # image = image.resize((256, 256))  # Adjust the size based on your model requirements
        image = image.convert('L')
        
        #image = cv2.imread(image_file)
        #image = cv2.imdecode(np.fromstring(image_file.read(),np.uint8),cv2.IMREAD_UNCHANGED)
        #resized_image =cv2.resize(image,(256,256))

        #gray_img = cv2.cvtColor(resized_image,cv2.COLOR_BGR2GRAY)


        #reshaped_img=np.expand_dims(image,axis =-1)
        image_array = np.asarray(image)  # Normalize the image
        image_array = image_array[np.newaxis,:,:,np.newaxis]
        
        # Reshape the image array to match the model input shape
        #image_array = np.reshape(image_array, (256, 256,1))

        # Perform predictions
        predictions = image_model.predict(image_array)
        class_index = np.argmax(predictions)
        class_label="e"        
        if(class_index == 0):
            class_label = "not fake"
        elif(class_index == 2):
            class_label = "not fake" 
        elif(class_index == 4):
            class_label = "fake"               
        elif(class_index == 3):
            class_label = "fake" 
        else:
            class_label=str(class_index)
            
         
        
        
        # Save the prediction in the database (adjust the model name in the import statement accordingly)
        ImagePrediction.objects.create(image=image_file, prediction=class_label)

        result = {"result": class_label}
        return JsonResponse(result)
    else:
        return JsonResponse({"error": "Invalid request method."})
