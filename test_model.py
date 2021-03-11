import numpy as np
from grabscreen import grab_screen
import cv2
import time
import keras
import random
import tensorflow as tf
from keras.models import load_model
from teclas import PressKey,ReleaseKey, W, A, S, D
from getkeys import key_check

w =  [1,0,0,0,0,0,0]
s =  [0,1,0,0,0,0,0]
a =  [0,0,1,0,0,0,0]
d =  [0,0,0,1,0,0,0]
wa = [0,0,0,0,1,0,0]
wd = [0,0,0,0,0,1,0]
nt = [0,0,0,0,0,0,1]

WIDTH=150
HEIGHT=100

def derecho():
    if random.randrange(0, 3) == 1: # 1/3 probabilidad de que no oprima nada, para controlar la velocidad
        ReleaseKey(W)
    else:
        PressKey(W)
        ReleaseKey(A)
        ReleaseKey(D)
        ReleaseKey(S)

def izquierda():
    ReleaseKey(W)
    PressKey(A)
    ReleaseKey(S)
    ReleaseKey(D)

def derecha():
    ReleaseKey(W)
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(S)

def reversa():
    PressKey(S)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)

def derecho_izquierda():
    PressKey(W)
    PressKey(A)
    ReleaseKey(D)
    ReleaseKey(S)

def derecho_derecha():
    PressKey(W)
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(S)
    
def no_tecla():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(S)
    ReleaseKey(D)

model = tf.keras.models.load_model('modelo.h5')

def main():
    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)
    mode_choice = 0
    pausa = False
    while(True):
        
        if not pausa:
            # 800x600 modo pantalla
            screen = grab_screen(region=(0,240,800,600))
            last_time = time.time()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (WIDTH,HEIGHT))

            prediction = model.predict([screen.reshape(-1,WIDTH,HEIGHT,1)])[0]
        
            #se multiplica para mejorar los resultados predichos.
            prediction = np.array(prediction)* np.array([5, 0.1, 0.4, 0.08, 0.8, 0.1, 0.2]) 
            #* np.array([4.5, 1, 1, 1, 1.5, 1.5, 0.5])
            #* np.array([4.5, 0.1, 0.2, 0.1, 0.5, 0.3, 0.2])
            print (prediction)

            mode_choice = np.argmax(prediction)
            print(mode_choice)
            
            #if np.argmax(prediction) == np.argmax(w):
            if prediction[0] > 0.65:
                derecho()
            elif np.argmax(prediction) == np.argmax(s):
                reversa()
            elif np.argmax(prediction) == np.argmax(a):
                izquierda()
            elif np.argmax(prediction) == np.argmax(d):
                derecha()
            elif np.argmax(prediction) == np.argmax(wa):
                derecho_izquierda()
            elif np.argmax(prediction) == np.argmax(wd):
                derecho_derecha()
            else: 
                no_tecla() 
                
        keys = key_check()

        # Pausar con P
        if 'P' in keys:
            if pausa:
                pausa = False
                time.sleep(1)
            else:
                pausa = True
                ReleaseKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
                time.sleep(1)

main()       




