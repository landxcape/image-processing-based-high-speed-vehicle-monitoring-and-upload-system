import cv2
import base64
import requests


# upload given image
def highspeed_upload(highspeed_image, vehicle_time):
    # convert numpy array to jpg format
    highspeed_jpg = cv2.imencode('.jpg', highspeed_image)[1].tostring()

    # encode in base64
    encoded_image = base64.b64encode(highspeed_jpg)
    payload = {'name': 'highspeed-detected-at-' + vehicle_time, 'image': encoded_image}
    r = requests.post('http://192.168.1.71/highspeed_upload/postRequestImage.php', data=payload)
