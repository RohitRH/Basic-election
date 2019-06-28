import cv2,os
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def getImagesAndLabels(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    Ids=[]
    for imagePath in imagePaths:
        pilImage=Image.open(imagePath).convert('L')
        imageNp=np.array(pilImage,'uint8')
        Id= int(os.path.split(imagePath)[-1].split(".")[-3])
        #print(Id)
        faces=detector.detectMultiScale(imageNp)
        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(Id)
    return faceSamples,Ids
    
def trainer():
    faces,Ids = getImagesAndLabels('image_dataSet')
    recognizer.train(faces, np.array(Ids))
    recognizer.save('trainer.yml')

if __name__=="__main__":
    trainer()