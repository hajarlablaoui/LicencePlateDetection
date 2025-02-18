import cv2
import imutils
import numpy as np
import pytesseract
from dbCreation import plateToDB
import random
images=['images/2088.jpeg','images/audi.jpg','images/peugeot.jpg','images/skoda.jpeg','images/volvo.jpg']
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#--------------------------------------------------------------------------------------#
img = cv2.imread(random.choice(images),cv2.IMREAD_COLOR)

#redimensionnement + bg_gris
img = cv2.resize(img, (600,400) )
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#supression des détails indésirables (flou)
#gray = cv2.bilateralFilter (source_image, diamètre du pixel, sigmaColor, sigmaSpace)
gray = cv2.bilateralFilter(gray, 13, 15, 15)

#détection des bords
#edged = cv2.Canny (source_image, thresholdMin, thresholdMax)
edged = cv2.Canny(gray, 30, 200)

#recherche des contours + tri du plus grand au plus petit
contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None

#vérification (4 contours + fermé)
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)

    if len(approx) == 4:
        screenCnt = approx
        break

if screenCnt is None:
    detected = 0
    print ("No contour detected")
else:
     detected = 1

#dessiner un contour en rouge
if detected == 1:
    cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

#masquer l'image sauf "plate"
mask = np.zeros(gray.shape,np.uint8)
new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
new_image = cv2.bitwise_and(img,img,mask=mask)

#recadrage de l'image
(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
Cropped = gray[topx:bottomx+1, topy:bottomy+1]

#conversion to string
text = pytesseract.image_to_string(Cropped, config='--psm 11')
plateToDB(text)

print("--------------------------------------------")
print("La plaque détectée est :",text)
print("--------------------------------------------")

img = cv2.resize(img,(500,300))
Cropped = cv2.resize(Cropped,(400,200))

cv2.imshow('car',img)
cv2.imshow('Cropped',Cropped)

cv2.waitKey(0)
cv2.destroyAllWindows()