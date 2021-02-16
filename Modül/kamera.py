import cv2
import os
import mmap
import pytesseract
#from picamera import PiCamera
from time import sleep

def goruntu():
    a = 1
    text_file = open("Output.txt", "w")
    text_file.write("QWÇ")
    text_file.close()
    text = []
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
    #arababulma = cv2.CascadeClassifier("cascade.xml")
    webcam = cv2.VideoCapture(0)
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH,1920);
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT,1080);
    while True:
        check, video = webcam.read()
        #cv2.waitKey(1000)
        if video is None:
            print("Hata, video yok")
            break
        #frame = imutils.rotate(frame, 180)
        # scale = 1
        # width = int(frame.shape[1] * scale)
        # height = int(frame.shape[0] * scale)
        # dimension = (width, height)
        # frame = cv2.resize(frame, dimension, interpolation=cv2.INTER_AREA)
        #print(check)  # prints true as long as the webcam is running
        # print(frame)  # prints matrix values of each framecd
        #video = imutils.resize(video, width=1350)

        cv2.imwrite(filename='test.png', img=video)

        image = cv2.imread('test.png')
        # image = imutils.resize(image, width=1350)
        # print(image.shape)
        #cv2.imshow("Original Image",image)
        #cv2.waitKey(1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("1- Grayscale Conversion",gray)
    #        cv2.waitKey(0)
        blur = cv2.bilateralFilter(gray, 11, 17, 17)
        #cv2.imshow("2- Bilateral Filter",gray)
        #cv2.waitKey(0)
        edges = cv2.Canny(blur, 30, 200)
        #cv2.imshow("3- Canny Edges",edges)
        #cv2.waitKey(0)
        _,cnts,_= cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        img1 = image.copy()
        cv2.drawContours(img1, cnts, -1, (0, 255, 0), 1)
        # cv2.imshow("4- All Contours",img1)
        # cv2.waitKey(0)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:15]  # conturları kenar belirleme keye göre sıralamaya sokuyor ve ilk onu alıyor

        img2 = image.copy()
        cv2.drawContours(img2, cnts, -1, (0, 255, 0), 1)
        # cv2.imshow("5- Top 30 Contours",img2)
        # cv2.waitKey(0)
        # NumberPlateCnt=None
        for c in cnts:
            uzunluk = cv2.arcLength(c, True)  # kontur cevresini ve eğrı uzunluğunu hesaaplar
            approx = cv2.approxPolyDP(c, 0.06 * uzunluk, True)  # 0.02 hata ile kaçgen olduklarını belirliyor
            if len(approx) == 4:
                # NumberPlateCnt=approx
                x, y, w, h = cv2.boundingRect(c)
                new_img = image[y:y + h, x:x + w]
                height, width, channels = new_img.shape
                oran = width / height
                if 3.5 < oran < 5:
                    print(str(a) + ".plaka oranı ", oran)
                    cv2.imwrite("plaka/" + str(a) + '.png', new_img)
                    Cropped_img_loc = cv2.imread("plaka/" + str(a) + ".png",0)  # şimdilik tek tek kaydetmeli olsun, proje sonunda tek tip yapıp yükten kurtarız.
                    a=a+1
                    text = pytesseract.image_to_string(Cropped_img_loc, lang='eng')
                    print("Plaka No: ",text)
                    text_file = open("Output.txt", "r+")
                    text_file.write(text)
                    text_file.close()
                    break
                break
            # cv2.drawContours(image, [NumberPlateCnt], -1, (0, 255, 0), 1)
            # cv2.imshow("Final image ",image)
            # cv2.waitKey(0)
            # print("Number is : ", text)
            # cv2.imshow("Number is: "+text,cv2.imread(Cropped_img_loc))
        with open('Output.txt', 'rb', 0) as file, \
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(b'06') != -1 and s.find(b'XE') != -1 and s.find(b'345') != -1:  # 1 başarılı
                print("\nDude")
                #break
            #else:
                #break
    os.remove("Output.txt")
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
