import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred,{

    'databaseURL':"https://face-attendance-realtime-d0675-default-rtdb.firebaseio.com/"
})


ref =db.reference("Students")#creating directory as the students in database

data={
    #this is the key and inside it all atre the values
"1234":#we have roo no of the student and have information insisde it
    {#these are the values
        "name":"Nishant Singhal",#name is the key and nishant singhal is the value
        "major":"AI/ML",
        "starting_year":2021,
        "total_attendance":6,
        "standing":"G",
        "Year":4,
        "last_attendance_time":"2024-5-30  00:54:34"
    },
"5434":
    {
        "name":"Kartik Sharma",
        "major":"ECE",
        "starting_year":2021,
        "total_attendance":9,
        "standing":"A+",
        "Year":4,
        "last_attendance_time":"2024-3-31  00:59:34"
    },
"6452":
    {
        "name":"Priyanka ",
        "major":"CSE-CORE",
        "starting_year":2021,
        "total_attendance":15,
        "standing":"0+",
        "Year":4,
        "last_attendance_time":"2024-3-31  00:51:34"
    }
}

for key,value in data.items():#we are sending the data to the database
    ref.child(key).set(value)#if u want to send data to specific directory then u use child