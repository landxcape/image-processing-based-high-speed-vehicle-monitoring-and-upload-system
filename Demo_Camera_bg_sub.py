import cv2
import numpy as np
import datetime

import my_image_processing_fn as myfn
import highspeed_upload as hu


# start video capture
cap = cv2.VideoCapture(0)

_, frame = cap.read()  # read captured data in frames
h, w, c = frame.shape  # get height, width, and column of the frame

r_image = np.zeros((h, w), np.uint8)  # create a blank reference image of same dimensions as frame

kernel = np.ones((9, 9), np.uint8)  # Taking a matrix as the kernel for dilation and erosion

# initial values
live_centers = []
old_centers = []
object_speed = 0
FPS = cap.get(cv2.CAP_PROP_FPS)
max_speed_allowed = 40  # kmph

total_area = h * w
min_detection_area = total_area / 530

# define boundaries for measurement of speed
boundary_high = 126
boundary_low = 177

measured_distance_meters = 4.5  # in meters
measured_distance_pixels = boundary_low - boundary_high  # in pixels
meters_per_pixel = measured_distance_meters / measured_distance_pixels

# roi = cv2.imread('ROI2.png', 0)  # get region of interest

x_end = len(frame[0])

while True:
    ret, frame = cap.read()
    if ret == 0:
        break

    image = myfn.grayScale(frame)

    # image = roi * image_gray

    bg_sub = cv2.subtract(image, r_image) + cv2.subtract(r_image, image)
    # bg_sub = cv2.absdiff(image, r_image)

    blur = cv2.GaussianBlur(bg_sub, (15, 15), 0)
    _, thres = cv2.threshold(blur, 15, 255, cv2.THRESH_BINARY)
    img_dilation = cv2.dilate(thres, kernel, iterations=1)
    img_erosion = cv2.erode(img_dilation, kernel, iterations=1)

    # find contours of blobs
    _, live_contours, hierarchy = cv2.findContours(img_erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, live_contours, -1, (0, 0, 255), 2)

    # draw lines at the boundaries
    cv2.line(frame, (0, boundary_high), (x_end, boundary_high), (0, 255, 255), 1)
    cv2.line(frame, (0, boundary_low), (x_end, boundary_low), (0, 255, 255), 1)

    live_centers.clear()
    # print('.')
    # print('.')
    # print('.')

    for c in live_contours:
        if cv2.contourArea(c) < min_detection_area:
            continue

        y, x, h, w = cv2.boundingRect(c)  # get bounding rectangles on contours
        Y = int(y + h / 2)
        X = int(x + w / 2)

        cv2.rectangle(frame, (y, x), (y + h, x + w), (0, 255, 0), 2)
        cv2.line(frame, (Y, X), (Y, X), (255, 255, 0), 6)
        live_centers.append([Y, X, object_speed])  # append centers of each blobs to an array

    if live_centers:
        # get pixels displaced per frame by each center
        pixels_displaced_per_frame = myfn.object_tracker(live_centers, old_centers, boundary_high, boundary_low)
        # print('pixel displaced per frame = ', str(pixels_displaced_per_frame))

        # pixels_per_second = pixels_displaced_per_frame * 30
        pixels_per_second = [i * FPS for i in pixels_displaced_per_frame]

        # meters_per_second = pixels_per_second * meters_per_pixel
        meters_per_second = [i * meters_per_pixel for i in pixels_per_second]

        # kmph = meters_per_second * 3.6
        kmph = [i * 3.6 for i in meters_per_second]
        kmph_int = list(map(int, kmph))

        # print('pixels per second = ', str(pixels_per_second))
        # print('meters per second = ', str(meters_per_second))
        # print('kmph = ', str(kmph_int))

        for i in range(len(old_centers)):
            # put speed data from speed array to respective centers
            live_centers[i][2] = kmph_int[i]

            # show speed only within the boundary
            if boundary_high <= live_centers[i][1] <= boundary_low:
                cv2.putText(frame, str(live_centers[i][2]) + 'km/h', (live_centers[i][0], live_centers[i][1]),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1)

            # upload when highspeed vehicle approaches lower boundary
            if live_centers[i][1] >= boundary_low - 8 and live_centers[i][2] > max_speed_allowed:
                # t += 1
                vehicle_time = datetime.datetime.now()
                time_string = vehicle_time.strftime('%Y-%m-%d_%Hh-%Mm-%Ss')

                hu.highspeed_upload(frame, time_string)
                # print('highspeed detected at ', time_string, i)

    old_centers = live_centers.copy()

    cv2.imshow('frame', frame)
    # cv2.imshow('image', image)
    # cv2.imshow('bg_sub', bg_sub)
    # cv2.imshow('blur', blur)
    # cv2.imshow('threshold', thres)
    # cv2.imshow('img_dilation', img_dilation)
    # cv2.imshow('img_erosion', img_erosion)

    r_image = image

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# show additional information at the end of the video (comment out when input is live camera)
print("video statistics ; before release of cap else no value")
print("Frame Count   : ", cap.get(cv2.CAP_PROP_FRAME_COUNT))
print("Format        : ", cap.get(cv2.CAP_PROP_FORMAT))
print("Height        : ", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("Width         : ", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print("Mode          : ", cap.get(cv2.CAP_PROP_MODE))
print("Brightness    : ", cap.get(cv2.CAP_PROP_BRIGHTNESS))
print("Fourcc        : ", cap.get(cv2.CAP_PROP_FOURCC))
print("Contrast      : ", cap.get(cv2.CAP_PROP_CONTRAST))
print("FrameperSec   : ", cap.get(cv2.CAP_PROP_FPS))

# Get duration of the video
FrameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
FrameperSecond = cap.get(cv2.CAP_PROP_FPS)
DurationSecond = FrameCount / FrameperSecond
if FrameperSecond > 0:
    print("FrameDuration : ", DurationSecond, "seconds")

cap.release()
cv2.destroyAllWindows()
