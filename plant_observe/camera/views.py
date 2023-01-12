from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.decorators import gzip

from datetime import datetime
from django.utils import timezone
import os
import cv2
import threading
import sys
import schedule
import time

import logging
from .models import Image

logger = logging.getLogger("pybo")

directory = os.getcwd()
filePath = directory + '/plant_observe/templates/resources/images/'

logger.debug(filePath)


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode(".jpg", image)
        return jpeg.tobytes()

    def update(self):
        schedule.every(30).minutes.do(self.take_frame)
        while True:
            (self.grabbed, self.frame) = self.video.read()
            schedule.run_pending()
            time.sleep(0.02)

    def take_frame(self):
        now = datetime.now()
        fileName = filePath + now.strftime('%y%m%d_%H%M%S') + '.png'
        logger.debug(fileName)
        cv2.imwrite(fileName, self.frame)

        db = Image(image_name=now.strftime('%y%m%d_%H%M%S'), pub_date=timezone.now())
        db.save()


camera = VideoCamera()

def printtest():
    logger.debug("TEST")

# def take_frame2(self):
#     now = datetime.now()
#     fileName = filePath + now.strftime('%y%m%d_%H%M%S') + '.png'
#     logger.debug(fileName)
#     cv2.imwrite(fileName, self.frame)
#
#     db = Image(image_name=now.strftime('%y%m%d_%H%M%S'), pub_date=timezone.now())
#     db.save()

def gen(self):
    # schedule.every(10).seconds.do(camera.take_frame())
    # schedule.every(10).seconds.do(printtest)
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        # schedule.run_pending(self)


def stream(request):
    try:
        return StreamingHttpResponse(gen(()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass


class LivePlant(TemplateView):  # Live 화면
    template_name = 'camera/live.html'


# def live(request):
#     return HttpResponseRedirect('/live/')

class CapturePlant(TemplateView):  # 사진 캡쳐
    template_name = 'camera/live.html'

    def post(self, request, *args, **kwargs):
        logger.debug(request.method)
        camera.take_frame()
        return HttpResponseRedirect('/live/')

# def capture(request):
#     if request.method == 'POST':
#         camera.take_frame()
#     return render(request, 'camera/live.html')
