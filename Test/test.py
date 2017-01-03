
import cv2
import os
import time
from PIL import Image
from PIL import ImageDraw

#import cv2.cv as cv

#xml = r'F:\opencv2\build\share\OpenCV\haarcascades\haarcascade_frontalface_alt.xml'
xml = r'F:\opencv3\sources\data\haarcascades\haarcascade_frontalface_alt.xml'
photos_dir = r'C:\Users\chenguitai\Desktop\face'

start_time = time.clock()
if os.path.exists(xml):
    face_cascade = cv2.CascadeClassifier(xml)
    for photo in os.listdir(photos_dir):
        photo_dir = photos_dir + '\\'+photo
        img = cv2.imread(photo_dir)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #gray_equalzeH = cv2.equalizeHist(gray)#equalizeHist
        faces = face_cascade.detectMultiScale(img_gray,minSize=(20,20))
        #faces = face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
        img = Image.open(photo_dir)
        draw_instance = ImageDraw.Draw(img)
        for num, (x,y,width,height) in enumerate(faces):
            #img.crop(face).save(photo.split('.')[0]+r'\faces\'+num+'.jpg)
            draw_instance.rectangle((x,y,x+width,y+height), outline=(255, 0,0))
            #cv2.imwrite(photo_dir.split('.')[0]+str(num)+r'face.jpg',cv2.imread(photo_dir)[y:y+height,x:x+width])
            #print x,x+width,y,y+height
            #print cv2.imread(photo_dir).shape
        img.save(photo_dir.split('.')[0]+r'_face_detect.jpg')
        #img.show()
        break
else:
    print 'Not Exits  ',xml

end_time = time.clock()
print "Running_time: %f s" % (end_time - start_time)




#recognize
photos_dire=[
    r'C:\Users\chenguitai\Desktop\face\face\100face.jpg',
    r'C:\Users\chenguitai\Desktop\face\face\101face.jpg',
    r'C:\Users\chenguitai\Desktop\face\face\110face.jpg',
    r'C:\Users\chenguitai\Desktop\face\face\111face.jpg',
    r'C:\Users\chenguitai\Desktop\face\face\80face.jpg',
    r'C:\Users\chenguitai\Desktop\face\face\82face.jpg',
    r'C:\Users\chenguitai\Desktop\face\face\84face.jpg',
]
images=[]
labels=[1,2,3,3,4,4,4]
for dire  in photos_dire:
    img = cv2.imread(dire)
    images.append(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

import numpy as np
recognizer = cv2.createLBPHFaceRecognizer()
recognizer.train(images[:-1],np.array(labels[:-1]))

pre,conf = recognizer.predict(images[-1])
print pre,conf