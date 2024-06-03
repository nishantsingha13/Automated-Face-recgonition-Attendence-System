# Automated-Face-recgonition-Attendence-System
Face Recognition Attendence System
created a real-time Face Attendance system. Added graphical interface along with a live database to create a real-world system. 

Setup the Webcam:
Configure the webcam to capture live video feed.
Ensure the camera settings are optimized for clear facial recognition.

Setup the Graphical Interface:
Design and implement an elegant graphical user interface (GUI) for better user experience.
Integrate the GUI with the system to display live video feed and attendance status.

Encoding Generator:
Utilize the face recognition library to encode facial features.
Use 128 facial parameters to generate unique facial encodings for accurate identification.

working of Face-recognition "https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78"

Database Setup:
Set up a robust database to store student data and images.
Use Firebase for efficient and real-time data storage and retrieval.

Attendance Marking Logic:
Check if the user has already given attendance:
If yes, display "Attendance already marked."
If no, mark the attendance and update the database.

Implement a validation mechanism to ensure unregistered persons cannot mark attendance.
