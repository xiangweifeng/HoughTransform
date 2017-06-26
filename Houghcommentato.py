
"""
Created on Tue May 30 13:59:20 2017

@author: Francesco Lacriola
"""
import numpy as np
from PIL import ImageDraw,Image

class Hough(object):
    
    def __init__(self,image, n_theta, n_rho, plot_point):
        self.image= image     #immagine da analizzare
        step=0                #
        self.n_theta= n_theta #numero di angoli da analizzare per ogni punto
        self.n_rho= n_rho     #numero di intervalli di rho
        thetas = np.deg2rad(np.linspace(-90.0, 90.0,self.n_theta)) #array contenente gli angoli da analizzare
        width, height = self.image.shape
        diag_len = np.ceil(np.sqrt(width * width + height * height))   # il rho massimo (la diagonale dell'immagine)
        rhos = np.linspace(-diag_len, diag_len, self.n_rho+1)          # i limiti degli intervalli
        # Cache some resuable values
        cos_t = np.cos(thetas)  #calcola una volta tutti i cos degli angoli da analizzare e li salva in un array
        sin_t = np.sin(thetas)  #calcola una volta tutti i sin degli angoli da analizzare e li salva in un array
        num_thetas = len(thetas)
        
        accumulator = np.zeros((self.n_rho, num_thetas), dtype=np.uint64) #accumulatore
        y_idxs, x_idxs = np.nonzero(self.image)  # una lista di x ed y contenenti le cordinate dei punti bianchi (non zero)
       # Vote in the hough accumulator
        for i in range(len(x_idxs)): #cicla su tutti i punti bianchi (x è la x del punto corrente, y la sua y)
           x = x_idxs[i]
           y = y_idxs[i]
    
           for t_idx in range(num_thetas): #cicla su tutti gli angoli da analizzare
               # Calculate rho. diag_len is added for a positive index 
               rho = x * cos_t[t_idx] + y * sin_t[t_idx] #calcola rho
               ind_rho = Hough.__binary_int__(rhos,rho) #approssima rho ad un indice all'interno dell'array degli intervalli
               accumulator[ind_rho, t_idx] += 1 #assegna il voto
               if plot_point is not None: #un controllo limite
                   plot_point(rho, np.rad2deg(thetas[t_idx%accumulator.shape[1]]), accumulator[ind_rho, t_idx], step) #aggiunge un punto al grafico
                   step+=1
        self.accumulator=accumulator
        self.thetas= thetas
        self.rhos= rhos
    
    def getHoughImage(self):
        accmax= np.argmax(self.accumulator)
        redacc=self.accumulator/self.accumulator[int(accmax/self.accumulator.shape[1])][accmax%self.accumulator.shape[1]]
        return redacc
    
    def getPatternImage(self):
        image=np.zeros(np.shape(self.image))
        image=Image.fromarray((image).astype('uint8'))
        accmax= np.argmax(self.accumulator)
        maxacc=self.accumulator[int(accmax/self.accumulator.shape[1])][accmax%self.accumulator.shape[1]]
        draw = ImageDraw.Draw(image)
        ord_accumulator= self.accumulator
        ind_min=np.argmin(ord_accumulator)
        i=int(ind_min/self.accumulator.shape[1])
        j=ind_min%self.accumulator.shape[1]
        while ord_accumulator[i][j]<maxacc:
             rho = self.rhos[i]
             theta = self.thetas[j]
             y1=(rho/np.sin(theta))-(np.cos(theta)/np.sin(theta)*(np.shape(self.image)[1]-1))
             y2=(rho/np.sin(theta))-(np.cos(theta)/np.sin(theta)*0)
             #per trovare linee orizzontali if (y2-y1)/(-(np.shape(self.image)[1]-1)) >= -0.1 and (y2-y1)/(-(np.shape(self.image)[1]-1)) <=0.1:
             draw.line((np.shape(self.image)[1]-1,y1, 0,y2), fill=int((ord_accumulator[i][j]/maxacc)*255))
             ord_accumulator[i][j]=maxacc
             ind_min=np.argmin(ord_accumulator)
             i=int(ind_min/self.accumulator.shape[1])
             j=ind_min%self.accumulator.shape[1]
        i=int(accmax/self.accumulator.shape[1])
        j=accmax%self.accumulator.shape[1]
        rho = self.rhos[i]
        theta = self.thetas[j]
        y1=(rho/np.sin(theta))-(np.cos(theta)/np.sin(theta)*(np.shape(self.image)[1]-1))
        y2=(rho/np.sin(theta))-(np.cos(theta)/np.sin(theta)*0)
        #per trovare linee orizzontali if (y2-y1)/(-(np.shape(self.image)[1]-1)) >= -0.1 and (y2-y1)/(-(np.shape(self.image)[1]-1)) <=0.1:
        draw.line((np.shape(self.image)[1]-1,y1, 0,y2), fill=int((ord_accumulator[i][j]/maxacc)*255))
        return image
    
    def __binary_int__(array,val):
        assert val<= array[len(array)-1] and val>=array[0]
        found=False
        maxm=len(array)
        start = int((maxm/2))
        minm=0
        if val == array[0]:
            return 0
        while not found:
            if val<=array[start]:
                maxm=start
                start=int(((minm+start)/2))
                
            elif val>array[start+1]:
                minm=start
                start=int(((maxm+start)/2))
                
            else:
                found=True
        return start
