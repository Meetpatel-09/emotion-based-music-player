import cv2
# from deepface import DeepFace
import matplotlib.pyplot as plt


img = cv2.imread('static/images/3.jpg')

print(img)

plt.imshow(img[:, :, : : -1])
plt.show()


# result = DeepFace.analyze(img, actions = ['emotion'])

# # print result
# print(result[0]['dominant_emotion'])

# emotion = result[0]['dominant_emotion']

