import cv2

videoCaptureObject = cv2.VideoCapture("http://192.168.43.1:8080/video")
result = True
while(result):
    ret,frame = videoCaptureObject.read()
    cv2.imwrite("NewPicture.jpg",frame)
    result = False
videoCaptureObject.release()
cv2.destroyAllWindows()