import sys
import time
import RPi.GPIO as GPIO
from time import sleep
import serial
import os
import subprocess
#-----------------------------------------------------------------------

GPIO.setmode(GPIO.BCM)

arduino = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)
arduino.flushInput()
GPIO.setwarnings(False)

MotorIN1=26
MotorIN2=20
MotorIN3=19
MotorIN4=16
sleeptime=1

GPIO_TRIGGER = 18
GPIO_ECHO = 24
Sig = 12

GPIO.setup(MotorIN1, GPIO.OUT)
GPIO.setup(MotorIN2, GPIO.OUT)
GPIO.setup(MotorIN3, GPIO.OUT)
GPIO.setup(MotorIN4, GPIO.OUT)

GPIO.setup(Sig, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)



#-----------------------------------------------------------------------

## Sensor ultrasonico, medir la distancia
def distance():
# Se pone Trigger en HIGH
    GPIO.output(GPIO_TRIGGER, True)

# Despues de 0.01ms se pone LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

# Se guarda el tiempo de salida
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

# Se guarda el tiempo de llegada
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

# resta de stopTime con StartTime
    TimeElapsed = StopTime - StartTime
# se multiplica con la velocidad del sonido
#Se divide entre 2, ida y regreso
    distance = (TimeElapsed * 34300) / 2
    return distance

#-----------------------------------------------------------------------

def movmot():
    GPIO.output(MotorIN1, GPIO.LOW)
    print("Abriendo puerta 1")
    GPIO.output(MotorIN2, GPIO.HIGH)

    time.sleep(45)

    GPIO.output(MotorIN1, GPIO.LOW)
    print("Se mantiene abierta la puerta 1")
    GPIO.output(MotorIN2, GPIO.LOW)

    time.sleep(45)

    GPIO.output(MotorIN1, GPIO.HIGH)
    print("Se CIERRA la puerta 1")
    GPIO.output(MotorIN2, GPIO.LOW)

    time.sleep(45)

    GPIO.output(MotorIN1, GPIO.LOW)
    print("Se mantiene cerrada la puerta 1")
    GPIO.output(MotorIN2, GPIO.LOW)

#-----------------------------------------------------------------------

def pump():
    print('Inicar desinfeccion')
    GPIO.output(Sig, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(Sig, GPIO.LOW)
    print('Finalizó el ciclo de desinfección')

#-----------------------------------------------------------------------

try:
    while True:
        print("Bienvenido al armario inteligente")
        
        
        #reinicia i
        s = arduino.readline()
        s = s.strip()
        print(s.decode("utf-8"))  # Encoding 8 bits

        if (s.decode("utf-8") == "Bienvenido Usuario 1"):
            # si la tarjeta rfid del usuario 1 es detectada, se inicia el proceso de abrir y cerrar la puerta
            movmot()
            ##  Ya que la puerta fue cerrada, Se inicia el sensor para detectar si hay o no prendas en el interior
            ##*******************************************************
            dist = distance()
            print("Distancia medida = %.1f cm" % dist)
                ## Si la distancia medida por el sensor es de 10 cm o menos, significa que hay una prenda en el interior
                ## Se inicia el proceso de desinfección
            if dist < 1800:
                variab = True
                while variab == True:
                    pump()
                    x = 0 
                    for x in range(10):
                        x = x + 1
                        time.sleep(1)
                        print(x)
                        s = arduino.readline()
                        s = s.strip()           
                        if (s.decode("utf-8") == "Bienvenido Usuario1"):
                           
                            variab = False
                            break
                            
                        else:
                            pass
            else:
                pass
        else:
            pass

                    
                    



except KeyboardInterrupt:
    print("Proceso detenido")
    GPIO.cleanup()

except:
    print("error")

finally:
    GPIO.cleanup()

