import cv2

cam = cv2.VideoCapture(0)
ret, frame = cam.read()
cam.release()

if ret:
    cv2.imwrite("./webcam.jpg", frame)
    print("captured!")
else:
    print("failed to capture!")