from PIL import Image, ImageDraw, ImageFont
import face_recognition
import numpy as np
import pickle
import shutil
import os
import uvicorn
import pandas as pd

import io
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from typing import List


app = FastAPI()
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


# upload file to the registered_images folder
@app.post("/Register_faces/")
async def faces_registeration(uploaded_file: UploadFile = File(...), name: str = Form(...)):
    if name not in os.listdir('registered_images'):
        file_location = f"registered_images/{name}.jpg"
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}
            

# take the images uploaded by the user

@app.post("/Recognise_faces/")
async def faces_recognition(image_upload: UploadFile = File(...)):
    data = await image_upload.read()
    print(type(data))
    
    # Load the image
    image = Image.open(io.BytesIO(data))
    print(type(image))
    print(image.size)

    # training the dataset
    known_face_names = []
    known_face_encodings = []
    for face in os.listdir('registered_images'):
        known_face_names.append(os.path.splitext(face)[0])
        face_image = face_recognition.load_image_file('registered_images/' + face)
        face_encoding = face_recognition.face_encodings(face_image)[0]
        known_face_encodings.append(face_encoding)
        #converting it into DataFrames
        kfn=pd.DataFrame(known_face_names)
        kfe=pd.DataFrame(known_face_encodings)
        #merging the two DataFrames
        df=pd.concat([kfn,kfe],axis=0)
        #saving it into a csv format
        df.to_csv("attendance.csv")
    

    # Dump face names and encoding it to pickle
    # pickle.dump((known_face_names, known_face_encodings), open('faces.p', 'wb'))
    
    # # load the trained datasets
    # known_face_names, known_face_encodings = pickle.load(open('faces.p', 'rb'))

    print(len(known_face_encodings))
    # Detect the face(s) in the image and encode them
    face_locations = face_recognition.face_locations(np.array(image))
    face_encodings = face_recognition.face_encodings(np.array(image), face_locations)

    draw = ImageDraw.Draw(image)
    face_names = []

    # Recognize the face(s) in the image
    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        name = known_face_names[best_match_index]

        top, right, bottom, left = face_location
        draw.rectangle([left, top, right, bottom], outline='red' ,width=3)
        draw.text((left, top), name, font = ImageFont.truetype("arial.ttf", int(round(2/30*image.size[1]))))
        face_names.append(name)

    image_byte_arr = io.BytesIO()
    image.save(image_byte_arr, format='PNG')
    image_byte_arr = image_byte_arr.getvalue()
    return StreamingResponse(io.BytesIO(image_byte_arr), media_type='image/png')




    