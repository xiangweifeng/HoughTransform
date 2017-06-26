
import numpy as np
from scipy import ndimage as ndi
from skimage import feature
from PIL import Image


class ImageManager:
    def __init__(self,image):
        self.image= image
        
    def findEdges(self, sigma):
        self.image_filtered=feature.canny(self.image, sigma=sigma)
        
    def getShape(shape, image_dimensions, rotate, noise):
        im = np.zeros(image_dimensions)
        if shape== 'square':
            im[32:-32, 32:-32] = 1
        if rotate > 0:
            im = ndi.rotate(im, 30, mode='constant')
        im = ndi.gaussian_filter(im, 4)
        im += noise * np.random.random(im.shape)
        return im
    
    def arraytoimage(image):
        i=Image.fromarray((image*255).astype('uint8'))
        return i
    
