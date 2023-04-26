# Face-Recognition-using-FastAPI
This is a simple face recognition system that can be used to recognize faces in uploaded images using FastAPI. The system uses the face_recognition library to recognize faces, and it allows users to register their faces by uploading an image to the system.

# Installation
Clone the Repository:
git clone https://github.com/NiharikaSarma001/Face-Recognition-using-FastAPI
cd face-recognition-fastapi

Create a virtual environment:
python -m venv venv

Activate the virtual environment:
# Windows
venv\Scripts\activate.bat

# Unix/Linux
source venv/bin/activate

Install the dependencies:
pip install -r requirements.txt

# Usage
To start the FastAPI application, run:
uvicorn task:app --reload
The application will be available at http://localhost:8000.

# Registering Faces
To register a face, send a POST request to /Register_faces/ with an image file and a name. The image file should be in JPEG format. The name should be a string.

Example using curl:
curl -X POST -F "uploaded_file=@/path/to/image.jpg" -F "name=John Doe" http://localhost:8000/Register_faces/

# Recognising Faces
To recognize faces in an image, send a POST request to /Recognise_faces/ with an image file. The image file should be in JPEG format.

Example using curl:
curl -X POST -F "image_upload=@/path/to/image.jpg" http://localhost:8000/Recognise_faces/

The response will be a PNG image with the recognized faces highlighted in red and labeled with their names. If there are multiple faces in the image, each face will be labeled with its corresponding name.
