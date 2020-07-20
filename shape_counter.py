# Gerekli paketleri import edelim:

import argparse
import imutils
import cv2

# Argument parser oluşturalım --->>> ArgumentParser() fonksiyonu ile
ap = argparse.ArgumentParser()

# Yeni argumanlar ekleyelim --->>> add_argument() fonksiyonu ile
ap.add_argument("-i", "--input", required=True, help = "input image path pls!")
ap.add_argument("-o", "--output", required=True, help = "output image path pls!")

# ap'ye eklediğimiz argumanları pars edelim, parse_args() fonksiyonu ile --->>> ap.parse_args()
# daha sonra vars() fonksiyonu ile dictionary'e çevirelim --->>> vars(ap.parse_args())

args = vars(ap.parse_args())

# ismini girdiğimiz resmi okuyalım:
image = cv2.imread(args["input"])

# resmi (image) siyahbeyaza çevirelim:
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Gaussian filtresi gürültü azaltıcı bir yumuşatma filtresidir.
blurred = cv2.GaussianBlur(gray,(5,5), 0)

# Bilateral (İki taraflı) Filter kenar koruyucu ve gürültü azaltıcı bir yumuşatma filtresidir.
# Bilateral filtrelemenin iyi tarafı, kenarları koruduğu,
# Gaussian filtresinin ise her şeyi eşit bir şekilde düzleştirdiği yönündedir.
# cv2.bilateralFilter(img, 5, 70, 50)

# blurred resmimizin threshold değerini bulalım.
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# Artık şekillerin kenarlarını bulup çizebiliriz...
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    cv2.drawContours(image, [c], -1, (0, 0, 255), 2)

# Resimdeki toplam şekil sayısı:
text = print("we found {} total shapes.".format(len(cnts)))
cv2.putText(image, text, (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# işlenen resmin çıktısını yazdıralım:
cv2.imwrite(args["output"], image)