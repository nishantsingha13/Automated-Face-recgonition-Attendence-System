import os
import pickle
import cvzone
import numpy as np
import cv2
import face_recognition
import numpy as np
from datetime import datetime

#get the user data
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-attendance-realtime-d0675-default-rtdb.firebaseio.com/",
    'storageBucket': "face-attendance-realtime-d0675.appspot.com"
})
bucket = storage.bucket()

cap = cv2.VideoCapture(0)  # 1 Capturing the video (setting the webcam)
#giving width and height as to fit image in background frame
cap.set(3, 640)  #1 Sets the width of the captured video frame to 1280 pixels.
cap.set(4, 480)  #1 Sets the height of the captured video frame to 720 pixels.

imgBackground = cv2.imread('resources/background.png')  # from resource

# 2imorting the mode images into a list u can also do separately
folderModePath = "resources/Modes"
modePathList = os.listdir(folderModePath)  # images are stored in list
#print(modePathList)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
#print(len(imgModeList))

# load the encoding file
print("Loading encode file...")
file = open("encodefile.p", 'rb')
encodelistwithid = pickle.load(file)
file.close()
encodelistknow, studentid = encodelistwithid
#print(studentid)
print("Encode file Loaded...")

modetype = 0  # it will show active before detecting the face
# after detecting the face information will be downloaded and displayed on the screen
counter = 0
id = -1
imgstudent = []

while True:
    success, img = cap.read()  # 1 Running the webcam
    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    # we will find encoding of newfaces and encodings that we have have stored in database we will match with it
    facecurrentframe = face_recognition.face_locations(imgs)
    encodecurrentframe = face_recognition.face_encodings(imgs, facecurrentframe)

    imgBackground[162:162 + 480, 55:55 + 640] = img  # 2 to overlay the webcam image in background photo(weidth,height)
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]  # we have variable so according to the value of variable it will show image like present absent etc.
    if facecurrentframe:
        for encodeface, facelocation in zip(encodecurrentframe, facecurrentframe):
            matches = face_recognition.compare_faces(encodelistknow, encodeface)  # it will show matches[true,false,false]because first one is of my photo as it matches
            facedistance = face_recognition.face_distance(encodelistknow, encodeface)  # it will show distance of current image to all the stored images like [0.2324,0.8674,0.956]
            # print("matches",matches)
            # print("dis", facedistance)

            matchindex = np.argmin(facedistance)  # it will give us min facedistance
            # print("matchindex", matchindex)#it will give index[0]because i showed in front of camera and my data is in firstposition i.e image stored

            if matches[matchindex]:  # after finding the smallest distnce if same index has ture in match then image is detected
                # print("Known Face Detected")
                # print(studentid[matchindex]) we get the studentid
                y1, x2, y2, x1 = facelocation  # this is for rect on the face
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # because we resize the image
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)  # rt means rectangle thickness
                # printing the information of student while in contact with camera if detected
                id = studentid[matchindex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground,"Loading",(275,400))
                    cv2.imshow("Face Attendance",imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modetype = 1  # after getting the information we will change the mode

        if counter != 0:

            if counter == 1:
                # get the data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # get the image from storage

                blob = bucket.get_blob(f'images/{id}.jpeg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgstudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # update data of attendance only once
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])  # Update the data
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # update the last time of attendance
                else:
                    modetype = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]
            if modetype != 3:
                if 10 < counter <= 20:  # if attendance already marked
                    modetype = 2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]  # it will say marked

                if counter <= 10:  # when we need to update
                    cv2.putText(imgBackground, str(studentInfo["total_attendance"]), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo["major"]), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo["standing"]), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['Year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    # getting the name in center of everyname
                    (w, h), _ = cv2.getTextSize(studentInfo["name"], cv2.FONT_HERSHEY_COMPLEX, 1, 1)  # _because with width and height it will give another thing that is not needed
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo["name"]), (808 + offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (50, 50, 50), 1)

                    # Resize imgstudent to fit within the specified region
                    imgstudent_resized = cv2.resize(imgstudent, (216, 216))

                    # Assign the resized imgstudent to the specified region of imgBackground
                    imgBackground[175:175 + 216, 909:909 + 216] = imgstudent_resized

                counter += 1

                if counter >= 20:  # if new person comes then it will erase all about previous one and set to another frame
                  counter = 0
                  modetype = 0
                  studentInfo = []
                  imgstudent = []
                  imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]
    else:
        modetype=0
        counter=0
    # cv2.imshow("webcam", img)#1
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)  # 1
