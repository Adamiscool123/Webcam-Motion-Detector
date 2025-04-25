import cv2
from emailing import send_email
import glob
import os
from threading import Thread

video = cv2.VideoCapture(0)
first_frame = None
status_list = []
count = 1

def clean():
    images = glob.glob('images/*.png')
    for image in images:
        os.remove(image)

while True:
    status = 0
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_gua = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_gua

    delta_frame = cv2.absdiff(first_frame, gray_gua)

    ftrame = cv2.threshold(delta_frame,20, 225, cv2.THRESH_BINARY)[1]

    divframe = cv2.dilate(ftrame, None, iterations=2)

    cv2.imshow("My video", divframe)

    contours, check = cv2.findContours(divframe, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue

        x,y,w,h = cv2.boundingRect(contour)

        rectangle = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)

        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)

    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True

        email_thread.start()


    cv2.imshow("Video", frame)


    key = cv2.waitKey(1)

    if key == ord("q"):
        break

clean_thread = Thread(target=clean)
clean_thread.daemon = True
clean_thread.start()


video.release()



