import cv2
# from deepface import DeepFace

emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture('static/videos/vid.mp4')

while True:
    ret, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#     try:
#       result = DeepFace.analyze(frame, 
#                           actions = ['emotion']) 
#       # print result 
#       emotion = result[0]['dominant_emotion']
#       print(emotion)
#       for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
#         cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
#         cv2.imshow('Real-time Emotion Detection', frame)
#       if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#     except:
#       print("An exception occurred")


cap.release()
cv2.destroyAllWindows()