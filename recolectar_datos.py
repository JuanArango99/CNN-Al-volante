import numpy as np
import cv2
import time
from grabscreen import grab_screen
from getkeys import key_check
import os

w =  [1,0,0,0,0,0,0]
s =  [0,1,0,0,0,0,0]
a =  [0,0,1,0,0,0,0]
d =  [0,0,0,1,0,0,0]
wa = [0,0,0,0,1,0,0]
wd = [0,0,0,0,0,1,0]
nt = [0,0,0,0,0,0,1]


valor_inicial = 1

while True:
    nombre_archivo = 'training_data-{}.npy'.format(valor_inicial)

    if os.path.isfile(nombre_archivo):
        print('El archivo existe, cargando data ',valor_inicial)
        valor_inicial += 1
    else:
        print('Archivo no existe',valor_inicial)
        break

def tecla_a_salida(teclas):
    #[W,S,A,D,WA,WD,NOTECLA]
    
    salida = [0,0,0,0,0,0,0]

    if 'W' in teclas and 'A' in teclas:
        salida = wa
    elif 'W' in teclas and 'D' in teclas:
        salida = wd
    elif 'A' in teclas:
        salida = a
    elif 'D' in teclas:
        salida = d
    elif 'S' in teclas:
        salida = s
    elif 'W' in teclas:
        salida = w
    else:
        salida = nt
        
    return salida

def main(nombre_archivo,valor_inicial): 
    nombre_archivo = nombre_archivo
    valor_inicial = valor_inicial
    training_data = []

    
    for i in list(range(2))[::-1]:
        print(i+1)
        time.sleep(1)

    tiempo = time.time()
    pausado = False

    while(True): 
        if not pausado:
            # Agarrar la imagen y mostrarla en una ventana
            # 800x600 
            # 40 por el titulo de la ventana.  
            pantalla =  grab_screen(region=(0,240,800,600))
            tiempo = time.time()
            pantalla = cv2.resize(pantalla,(150,100))
            pantalla = cv2.cvtColor(pantalla,cv2.COLOR_BGR2GRAY)
            teclas = key_check() # Funcion que guarda la tecla que se pulsó
            salida = tecla_a_salida(teclas)
        
            training_data.append([pantalla,salida])

            #print('ciclo tardó {} segundos'.format(time.time()-tiempo))
        
            if len(training_data) % 100 == 0:
                print(len(training_data))

            # Se guardan bloques de 2000 datos
            if len(training_data) == 5000:
                np.save(nombre_archivo,training_data)
                print("Guardado!!")
                training_data = []
                valor_inicial += 1
                nombre_archivo = 'training_data-{}.npy'.format(valor_inicial)
                
        keys = key_check()
        if 'P' in keys:
            if pausado:
                pausado = False
                print('despausado!')
                time.sleep(1)
            else:
                print('pausando!')
                pausado = True
                time.sleep(1)  


main(nombre_archivo,valor_inicial)

