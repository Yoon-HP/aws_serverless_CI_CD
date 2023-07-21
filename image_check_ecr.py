import json
import cv2
import numpy
import boto3
import mediapipe as mp
import base64
from io import BytesIO
from PIL import Image
from botocore.exceptions import ClientError
from datetime import datetime, timedelta, timezone

def lambda_handler(event, context):
    # TODO implement
    # print(event)
    print(event)
    try:
        body=json.loads(event['body'])
        img_bin=body['image']
        img_bin=base64.b64decode(img_bin)
        temp=BytesIO(img_bin)
        img=Image.open(temp)
        # print(img.size)
        while (img.height>1024 or img.width>1024):
            img=img.resize((int(img.width/2),int(img.height/2)))
        img.save('/tmp/temp.png')
        
        # image cut process
        img = cv2.imread("/tmp/temp.png")
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        print("face_check :", faces)
        
        if len(faces)!=1:
            return {
                'statusCode': 400,
                'body': json.dumps('Bad Request')
            }
    except:
        print("image processing fail!!!")
        return {
            'statusCode': 400,
            'body': json.dumps('bad!')
        }
        
    return {
        'statusCode': 200,
        'body': json.dumps("Image checking OK!")
    }
