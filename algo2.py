# 1) find contours of the receipt
# 2) if there are more than 4 vertices, find those which 
# are the most likely to be receipt vertices, mark and show them
# and if there are any missing vertices - assign value [0,0]
import cv2
import numpy as np
import imutils

font = cv2.FONT_HERSHEY_SIMPLEX


# arguments: image to transform, path to
def transform_image(image):
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)

    gray2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (5, 5), 0)
    edged2 = cv2.Canny(gray2, 75, 200)

    # find contours; len(cnts) returns no of contours found
    (cnts, _) = cv2.findContours(edged2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # array of perimeters
    periArr = []
    for elem in cnts:
        peri = cv2.arcLength(elem, True)
        periArr.append(peri)
    print "peri arr: " + str(periArr)

    # sort from the longest perimeter to the smallest
    cntsSorted = sorted(cnts, key=lambda x: cv2.arcLength(x, True), reverse=True)
    # print "cnts sorted: " + str(cntsSorted)

    periArr2 = []
    for elem in cntsSorted:
        perii = cv2.arcLength(elem, True)
        periArr2.append(perii)
    print "peri sorted by length: " + str(periArr2)

    # length of the longest perimeter
    periMax = periArr2[0]
    print "peri max: " + str(periMax)
    # approxPolyDP returns coordinates of vertices of the longest perimeter
    approx2 = cv2.approxPolyDP(cntsSorted[0], 0.02 * periMax, True)
    print "no of vertices: " + str(len(approx2))

    # find vertices and put them into array all_vertices
    all_vertices = []
    for a in approx2:
        aa = a[0]
        x_coord = aa[0]
        y_coord = aa[1]
        two_vertices = [x_coord, y_coord]
        all_vertices.append(two_vertices)
    print "all vertices: " + str(all_vertices)

    # find vertices that are most likely to be receipt vertices
    br = ul = bl = ur = []
    max_sum = 0
    min_sum = 10000
    max_sub_x_y = 0
    max_sub_y_x = 0
    for elem in all_vertices:
        sum_x_and_y = elem[0] + elem[1]
        if sum_x_and_y > max_sum:
            max_sum = sum_x_and_y
            br = elem
        if sum_x_and_y < min_sum:
            min_sum = sum_x_and_y
            ul = elem

        if elem[0] - elem[1] > 0:
            if elem[0] - elem[1] > max_sub_x_y:
                max_sub_x_y = elem[0] - elem[1]
                ur = elem

        if elem[1] - elem[0] > 0:
            if elem[1] - elem[0] > max_sub_y_x:
                max_sub_y_x = elem[1] - elem[0]
                bl = elem

    print "ul: " + str(ul)
    print "ur: " + str(ur)
    print "br: " + str(br)
    print "bl: " + str(bl)

    contours = []
    contours.append(ul)
    contours.append(ur)
    contours.append(br)
    contours.append(bl)

    # if there are any empty vertices, assign its value to [0,0]
    for elem, val in enumerate(contours):
        if val == []:
            contours[elem] = [0, 0]

    print "coordinates of vertices ul, ur, br, bl: " + str(contours)

    # draw lines connecting vertices
    pts = np.array(contours, np.int32)
    # pts = pts.reshape((-1,1,2))
    cv2.polylines(image, [pts], True, (0, 255, 255), 2)

    # print vertices' coordinates
    for elem in contours:
        text2 = str(elem[0]) + " " + str(elem[1])
        cv2.putText(image, text2, (elem[0], elem[1]), font, 0.5, (255, 255, 0), 2)

    cv2.imshow("contours", image)

    # just for testing purposes, show info
    # for c in cnts:
    #     # how many vertices are found
    #     print "\nno of points: " + str(len(c))
    #
    #     area = cv2.contourArea(c)
    #     print "area: " + str(area)
    #     peri = cv2.arcLength(c, True)
    #     print "perimeter: " + str(peri)
    #     approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    #     print "len of approx: " + str(len(approx))
    #
    #     peri2 = cv2.arcLength(c, False)
    #     print "perimeter2: " + str(peri2)
    #     approx2 = cv2.approxPolyDP(c, 0.02 * peri2, False)
    #     print "len of approx2: " + str(len(approx2))

    cv2.waitKey(0)   
    cv2.destroyAllWindows()


def main():
    image_name = "IMAG0061.jpg"
    image = cv2.imread(image_name)
    transform_image(image)

if __name__ == "__main__":
    main()
