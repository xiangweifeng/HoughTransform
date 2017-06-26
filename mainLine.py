from ImageManager import ImageManager
from Hough import Hough
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D

import argparse

ax=None

def boole(w):
    if w==True:
        return True
    else:
        return False

parser=argparse.ArgumentParser()
parser.add_argument('--rhos', default=100, type=int)
parser.add_argument('--thetas', default=100, type=int)
parser.add_argument('--image', default=None)
parser.add_argument('--maxvoto', default=25, help='Massimo valore nell\'accumulatore', type=int)
parser.add_argument('--plot', default=True, help='Grafico')
parser.add_argument('--lines', default=True, help='Visualizzazione rette')
parser.add_argument('--accumulator', default=True, help='Visualizzazione accumulatore')
parser.add_argument('--times', default=2500,help='Punti da disegnare', type=int)
parser.add_argument('--imagevis', default=True, help='Visualizza l\'immageine')
parser.add_argument('--edgesvis', default=True, help='Visualizza gli edges')
parser.add_argument('--sigma',default=3, type=int)

args = parser.parse_args()
rhos= args.rhos
thetas=args.thetas
imagefile= args.image
maxvoto= args.maxvoto
plot=boole(args.plot)
accumulator=boole(args.accumulator)
lines= boole(args.lines)
times=args.times
imagevis=boole(args.imagevis)
edgesvis=boole(args.edgesvis)
sigma=args.sigma

p=None

if plot:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('rho')
    ax.set_ylabel('theta')
    ax.set_zlabel('occurences')


def plot_point(x,y,z,step): 
    color=[[0,0,1],]
       
    if z>0 and z<=maxvoto/4:
         color[0][2]=1
         color[0][1]=0  
         color[0][0]=0
    elif z>maxvoto/4 and z<=maxvoto/2:
         color[0][2]=1
         color[0][1]=1
         color[0][0]=0     
    elif z>maxvoto/2 and z<=maxvoto*0.75:
        color[0][2]=0
        color[0][1]=1
        color[0][0]=0
    elif z>maxvoto*0.75 and z<=maxvoto:
        color[0][2]=0
        color[0][1]=1
        color[0][0]=1
    elif z>maxvoto:
        color[0][2]=0
        color[0][1]=0
        color[0][0]=1
    ax.scatter(x,y,z,c=color)
    if step %times== 0:
        plt.pause(0.01)

if plot:
    p=plot_point

if imagefile==None:
    image = ImageManager(ImageManager.getShape('square',(100,100), 30, 0.2))
else:
    image= ImageManager(np.asarray(Image.open(imagefile).convert('L')))
    
if imagevis:
    ImageManager.arraytoimage(image.image).show()

image.findEdges(sigma= sigma)

if edgesvis:
    ImageManager.arraytoimage(image.image_filtered).show()


hough= Hough(image.image_filtered, rhos,thetas, p)

if plot:
    plt.ion()
    
if accumulator:    
    houghimage=hough.getHoughImage()
    houghimage=ImageManager.arraytoimage(houghimage)
    houghimage.show()
if lines:
    hi=hough.getPatternImage()
    hi.show()

