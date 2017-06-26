from PIL import Image
import numpy as np
from ImageManager import ImageManager
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte
from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D

import argparse

parser=argparse.ArgumentParser()
parser.add_argument('--radiusmin', default=20, type=int)
parser.add_argument('--radiusmax', default=35, type=int)
parser.add_argument('--radiusteps', default=2, type=int)
parser.add_argument('--image', default=None)
parser.add_argument('--imagevis', default=True, help='Visualizza l\'immageine')
parser.add_argument('--edgesvis', default=True, help='Visualizza gli edges')
parser.add_argument('--sigma',default=3, type=int)

args = parser.parse_args()
radiusmin= args.radiusmin
radiusmax=args.radiusmax
radiusteps=args.radiusteps
imagefile= args.image
imagevis=args.imagevis
edgesvis=args.edgesvis
sigma=args.sigma

if imagefile==None:
   image = img_as_ubyte(data.coins()[160:230, 70:270])
else:
   image = img_as_ubyte(Image.open(imagefile).convert('L'))
    
edges = canny(image, sigma=sigma, low_threshold=10, high_threshold=50)

if edgesvis:
    ImageManager.arraytoimage(edges).show()

# Detect two radii
hough_radii = np.arange(radiusmin, radiusmax, radiusteps)
hough_res = hough_circle(edges, hough_radii)

# Select the most prominent 5 circles
accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                           total_num_peaks=3)

image = color.gray2rgb(image)

if imagevis:
    ImageManager.arraytoimage(image).show()
    
for center_y, center_x, radius in zip(cy, cx, radii):
    circy, circx = circle_perimeter(center_y, center_x, radius)
    image[circy, circx] = (220, 20, 20)

ImageManager.arraytoimage(image).show()

