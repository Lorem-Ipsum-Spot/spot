import cv2
import pathlib


#cascade_path = pathlib.Path(cv2.__file__).parent.absolute( )/ "data/haarcascade_eye.xml"
cascade_path = pathlib.Path(cv2.__file__).parent.absolute( )/ "data/haarcascade_lowerbody.xml"
#cascade_path = pathlib.Path(cv2.__file__).parent.absolute( )/ "data/haarcascade_frontalface_default.xml"
print(cascade_path)

clf = cv2.CascadeClassifier(str(cascade_path))
camera = cv2.VideoCapture(1)

i = 0
while True:
    _,frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = clf.detectMultiScale(
        gray,
        scaleFactor= 1.1,
        minNeighbors=5,
        minSize=(30,30),
        flags= cv2.CASCADE_SCALE_IMAGE
    )
    for(x,y,width,height) in faces:
        cv2.rectangle(frame, (x,y),(x+width,y+height),(255,245,0),2)
        i+=1
        print(i)
    cv2.imshow("Faces", frame)
    if cv2.waitKey(1) == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()