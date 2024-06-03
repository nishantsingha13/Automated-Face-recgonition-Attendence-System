import os
import face_recognition
import pickle
import cv2
#for storage in datbase upload images
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred,{

    'databaseURL':"https://face-attendance-realtime-d0675-default-rtdb.firebaseio.com/",
    'storageBucket':"face-attendance-realtime-d0675.appspot.com"
})




#imorting student images
folderPath="images"
PathList=os.listdir(folderPath)#images are stored in list
print(PathList)
imgList=[]
studentid=[]
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    #print(path)#by this we will get the id but jpeg also fo eg 1234.jpeg i.e image name
    #print(os.path.splitext(path)[0])#remove jpej it will come(2234,jpej),so we want 0th index
    studentid.append(os.path.splitext(path)[0])
#print(studentid)
#for database storage
    #it will create folder images and add all the images beacuse we have given path of the images
    fileName=f'{folderPath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(fileName)
    blob.upload_from_filename(fileName)



#findi the encoding of images

def findencodings(imgList):
    encodelist=[]
    for img in imgList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)#change color because facerecg library uses rgb
        encode=face_recognition.face_encodings(img)[0]#step2 is to find encodings we want first element thats why we use [0]
        encodelist.append(encode)#we have to store encoding in list

    return encodelist

print("encoding started ..")
encodelistknow=findencodings(imgList)
#print(encodelistknow)#it will give all 128 parameters of the images
encodelistwithid=[encodelistknow,studentid]#it will give student id with their encodeing
print("encoding completed")

file=open("encodefile.p","wb")#making the pickle file
pickle.dump(encodelistwithid,file)
file.close()
print("file saved")
