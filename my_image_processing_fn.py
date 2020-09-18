import numpy as np


# tracking
def object_tracker(live_centers, old_centers, boundary_high, boundary_low):
    dist_array = []
    print('live_centers = ', str(live_centers))
    print('old_centers = ', str(old_centers))

    if len(old_centers) > len(live_centers):
        old_centers.pop(0)
        print('old_centers.pop = ', str(old_centers))

    length_old_centers = len(old_centers)

    for i in range(length_old_centers):
        if boundary_high <= live_centers[i][1] <= boundary_low:
            # dist = (int(math.sqrt((live_centers[i][0] - old_centers[i][0]) ** 2 +
            #                       (live_centers[i][1] - old_centers[i][1]) ** 2))) - 1

            dist = live_centers[i][1] - old_centers[i][1] - 1
            dist_array.append(dist)
        else:
            dist_array.append(0)

    return dist_array


# grayscale conversion function
def grayScale(img):
    gray = np.uint8(0.12 * img[:, :, 0] + 0.59 * img[:, :, 1] + 0.29 * img[:, :, 2])
    return gray


# threshold function
# def thresholdImage(gray, val):
#     height, width = gray.shape
#     thres = np.zeros((height, width), np.uint8)
#     for y in range(height):
#         for x in range(width):
#             thres[y, x] = 255 if gray[y, x] > val else 0
#     return thres


# smoothing filter function
# def smoothingFilter(gray):
#     filterMatrix = np.array([[1, 2, 1],
#                              [2, 4, 2],
#                              [1, 2, 1]])
#     height, width = gray.shape
#     filteredImage = np.zeros((height, width), np.uint8)
#     for y in range(1, height - 1):
#         for x in range(1, width - 1):
#             filterVal = filterMatrix[0][0] * gray[y - 1, x - 1]
#             filterVal += filterMatrix[1][0] * gray[y - 1, x]
#             filterVal += filterMatrix[2][0] * gray[y - 1, x + 1]
#             filterVal += filterMatrix[0][1] * gray[y, x - 1]
#             filterVal += filterMatrix[1][1] * gray[y, x]
#             filterVal += filterMatrix[2][1] * gray[y, x + 1]
#             filterVal += filterMatrix[0][2] * gray[y + 1, x - 1]
#             filterVal += filterMatrix[1][2] * gray[y + 1, x]
#             filterVal += filterMatrix[2][2] * gray[y + 1, x + 1]
#
#             filterVal /= 16
#             filteredImage[y, x] = filterVal
#
#     return np.uint8(filteredImage)


# dilation function
# def dilation(thres):
#     filterMatrix = np.array([[0, 1, 0],
#                              [1, 1, 1],
#                              [0, 1, 0]])
#     height, width = thres.shape
#     filteredImage = np.zeros((height, width), np.uint8)
#     for y in range(1, height - 1):
#         for x in range(1, width - 1):
#             filterVal = filterMatrix[1][0] * thres[y - 1, x]
#             filterVal += filterMatrix[0][1] * thres[y, x - 1]
#             filterVal += filterMatrix[2][1] * thres[y, x + 1]
#             filterVal += filterMatrix[1][2] * thres[y + 1, x]
#
#             if filterVal > 0:
#                 filteredImage[y, x] = 255
#             else:
#                 filteredImage[y, x] = 0
#
#     return np.uint8(filteredImage)