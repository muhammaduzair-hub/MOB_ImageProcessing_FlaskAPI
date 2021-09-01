from flask import Flask, request
import cv2
import numpy as np
import base64
import io
from PIL import Image
import os


app = Flask(__name__)

uploadfolder = '/images'
app.config['uploadfolder'] = uploadfolder

@app.route('/count',methods=['Get'])
def index():
    Query = str(request.args['Query'])
    ans = count(Query)
    return str(ans)


def count(Query):
    # Read image.

    my_path = os.path.join(Query)#'C:\Users\Muhammad Uzair\Downloads',"1.jpg")
    img = cv2.imread(my_path)#'2.png', cv2.IMREAD_COLOR)

    # Convert to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))
    # kernel = np.ones((5,5),np.uint8)
    edges = cv2.Canny(gray_blurred, 130, 230)
    # closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("edge", edges)

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 20,
                                        param1=50, param2=15, minRadius=20, maxRadius=40)

    # Draw circles that are detected.
    cnt = 0
    if detected_circles is not None:

        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle.
            cv2.circle(img, (a, b), r, (0, 255, 0), 3)

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(img, (a, b), 1, (0, 255, 0), 3)
            cnt = cnt + 1
    return cnt

@app.route('/file', methods=['Post'])
def upload_image():
    if 'file' not in request.files:
        return "no File"
    file = request.files['file']
    if file.filename == '':
        return "No Image selected"
    if file(file.filename):
        file.save(os.path.join(app.config['uploadfolder'], file.filename))
        return "Image save successfully"


if __name__ == "__main__":
    app.run()