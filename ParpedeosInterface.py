# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ParpedeosInterface.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import time
import dlib
import cv2
import  time
import sys
import threading
from PyQt5.QtCore import QThread,pyqtSignal
import bluetooth

#Clase de la interfaz gráfica
class Ui_MainWindow(object):
    #Función para inicializar la ventana
    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    def setupUi(self, MainWindow):
        MainWindow.resize(500, 600)
        MainWindow.setWindowTitle("Ventana")
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.firtScene()
        #Buscar el número de dispositivos
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        print("found %d devices" % len(nearby_devices))
        pos=0
        #Listar los dispositivos y buscar el arduino
        for addr, name in nearby_devices:
            print("  %s - %s" % (addr, name))
            if(name=='HC-06'):
                posBluArd = pos
            pos+=1
        port=1
        #Obtener la dirección del bluetooth
        bd_addr,ext = nearby_devices[posBluArd]
        print(bd_addr)
        #Se conecta al bluetooth del arduino
        self.sock.connect((bd_addr, port))
        #Se inicializa el hilo de deteccion de parpadeos
        self.my_thread = deteccionThread() 
        #Se conectado la señal del hilo con la función de mi clase en la ventana para recibir el valor
        #que envíe mi hilo(número de parpadeos)
        self.my_thread.senal.connect(self.senalValue)
        self.my_thread.start()



    ventanaActual = True
    #Función que recibe la señal de hilo de la función de detección de parpadeos
    def senalValue(self, value):
        if(self.ventanaActual):
            #Numero de parpadeos para ir a la segunda ventana
            if(value==2):
                self.secondScene()
                self.ventanaActual= False
        else:
            #Número de parpadeos para encender el foco
            if(value==2):
                self.encender()
            #Número de parpadeos para apagar el foco
            if(value==3):
                self.apagar()
            #Número de parpadeos para regresar a la ventana principal
            if(value==4):
                self.firtScene()
                self.ventanaActual= True
        



    #Vista 1
    def firtScene(self):
        #Widget inicial
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: #b4e9e2;")
        #Se agrega el grid al widget
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        #Configuración de los margenes de los grid
        self.gridLayout.setContentsMargins(50,0,50,0);
        #Creación de label
        self.Titulo = QtWidgets.QLabel("Detección de parpadeos", self.centralwidget);
        self.Titulo.setStyleSheet(" font-weight:bold;\
                                    font-size: 25px; \
                                    color: #309286;")
        #addWidget(*Widget, row, column, rowspan, colspan)
        self.gridLayout.addWidget(self.Titulo, 0, 0, 3, 1)
        #Creación de boton
        self.Button = QtWidgets.QPushButton("Luces",self.centralwidget)
        self.Button.setStyleSheet("font-weight:bold;\
                                    font-size: 20px; \
                            margin: 1px; padding: 10px; \
                            background-color: #32dbc6; \
                           color: #309286; \
                           border-style: solid; \
                           border-radius: 8px; border-width: 3px; \
                           border-color: #309286;")

        #Evento del botón
        self.Button.clicked.connect(self.secondScene)
        #Se agrega el botón a la cuadricula
        self.gridLayout.addWidget(self.Button, 2, 0, 3, 1)
        self.Button2 = QtWidgets.QPushButton("opcion 2",self.centralwidget)
        self.Button2.setStyleSheet("font-weight:bold;\
                                    font-size: 20px; \
                            margin: 1px; padding: 10px; \
                            background-color: #32dbc6; \
                           color: #309286; \
                           border-style: solid; \
                           border-radius: 8px; border-width: 3px; \
                           border-color: #309286;")
        self.gridLayout.addWidget(self.Button2, 4, 0, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)


    #Vista 2
    aviso = None
    FocoEncendido = False
    def secondScene(self):
        #widget segunda pantala
        self.secondwidget = QtWidgets.QWidget(MainWindow)
        self.secondwidget.setStyleSheet("background-color: #b4e9e2;")

        self.gridLayout = QtWidgets.QGridLayout(self.secondwidget)
        self.gridLayout.setContentsMargins(50,0,50,0);
        self.Titulo = QtWidgets.QLabel("Control de luces", self.secondwidget);
        self.Titulo.setStyleSheet(" font-weight:bold;\
                                    font-size: 25px; \
                                    color: #309286;")
        self.gridLayout.addWidget(self.Titulo, 0, 0, 1, 1)
        self.aviso = QtWidgets.QLabel("Foco encendido", self.secondwidget);
        self.aviso.setStyleSheet(" font-weight:bold;\
                                    font-size: 25px; \
                                    color: red;")
        self.gridLayout.addWidget(self.aviso, 1, 0, 1, 1)
        if(self.FocoEncendido):
            self.aviso.setVisible(True)
        else:
            self.aviso.setVisible(False)
        self.boton1 = QtWidgets.QPushButton("Encender",self.secondwidget)
        self.boton1.setStyleSheet("font-weight:bold;\
                                    font-size: 20px; \
                            margin: 1px; padding: 10px; \
                            background-color: #32dbc6; \
                           color: #309286; \
                           border-style: solid; \
                           border-radius: 8px; border-width: 3px; \
                           border-color: #309286;")
        self.boton1.clicked.connect(self.encender)
        self.gridLayout.addWidget(self.boton1, 2, 0, 3, 3)
        self.boton2 = QtWidgets.QPushButton("Apagar",self.secondwidget)
        self.boton2.setStyleSheet("font-weight:bold;\
                                    font-size: 20px; \
                            margin: 1px; padding: 10px; \
                            background-color: #32dbc6; \
                           color: #309286; \
                           border-style: solid; \
                           border-radius: 8px; border-width: 3px; \
                           border-color: #309286;")
        self.boton2.clicked.connect(self.apagar)
        self.gridLayout.addWidget(self.boton2, 4, 0, 3, 3)
        self.BotonAtras = QtWidgets.QPushButton("atrás",self.secondwidget)
        self.BotonAtras.setStyleSheet("font-weight:bold;\
                                    font-size: 20px; \
                            margin: 1px; padding: 10px; \
                            background-color: #32dbc6; \
                           color: #309286; \
                           border-style: solid; \
                           border-radius: 8px; border-width: 3px; \
                           border-color: #309286;")
        self.BotonAtras.clicked.connect(self.atrasEvento)
        self.gridLayout.addWidget(self.BotonAtras, 6, 2, 1, 1)
        MainWindow.setCentralWidget(self.secondwidget)
 
    def encender(self):
        print('Foco encendido')   
        data = '0'
        self.sock.send(data) 
        self.aviso.setVisible(True)
        self.FocoEncendido = True

    def apagar(self):
        print('Foco apagado')
        data = '1'
        self.sock.send(data) 
        self.aviso.setVisible(False)
        self.FocoEncendido = False
    

    def atrasEvento(self):
        self.firtScene()
       
#Clase hilo para la detección de parpadeos
class deteccionThread(QThread):
    #Señal para comunicarse entre clases
    senal = pyqtSignal(int)
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        #variable para que la relación de aspecto del ojo indique un 
        # parpadeo por debajo del umbral que se establece
        EYE_AR_UMBRAL = 0.3
        #variable para indicar el número de cuadros consecutivos que el ojo debe estar por debajo del umbral
        #Esta variable depende del procesamiento de cuadros del dispositivo
        EYE_AR_CONSEC_CUADROS = 3

        #Contador para los cuadros(Frames)
        CONTADOR = 0
        #Contador para el número total de parpadeos
        TOTAL = 0

        #Detector facial pre-entrenado para la libreria dlib
        RUTA_PREDICTOR = "shape_predictor_68_face_landmarks.dat"  
         



        #Inicialización del detector de caras
        #Cargar el detector pre-entrenado
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(RUTA_PREDICTOR)

        # Obtener los puntos de referencia faciales para el ojo derecho e izquierdo
        (IzqInicio, IzqFinal) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (DerInicio, DerFinal) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        #Cargar la cámara web
        video = VideoStream(src=0).start()
        time.sleep(1.0)

        #Ciclo de los cuadros de la secuencia del video de la cámara web
        inicio_de_tiempo = 0.0
        while True:

            # Guarda el fotograma de la secuencia, cambia a el tamaño que se le asigna
            frame = video.read()
            #frame = imutils.resize(frame, width=650)

            #Se convierte a escala de grise el fotograma
            grisVid = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #Ecualización adaptativa del fotograma para un mejor brillo
            ecuAdap = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            imgEcuAdap = ecuAdap.apply(grisVid)
            # Se detectan caras con el fotograma en escala de grises con el detector de dlib
            rects = detector(imgEcuAdap, 0)

            #Bucle de las detecciones realizadas
            for rect in rects:

                #Se determinan los puntos de referencia para la cara
                #Se convierte los puntos de referencia a coordenadas (x,y)
                shape = predictor(imgEcuAdap, rect)
                shape = face_utils.shape_to_np(shape)

                #Extracción de las coordenas de los ojos
                ojoIzq = shape[IzqInicio:IzqFinal]
                ojoDer = shape[DerInicio:DerFinal]
                #Paso de parametros para el cálculo de la relación de aspecto para cada ojo
                izqEAR = self.eye_aspect_ratio(ojoIzq)
                derEAR = self.eye_aspect_ratio(ojoDer)

                #promedio de la la relación de aspecto del ojo para los dos ojos
                ear = (izqEAR + derEAR) / 2.0
                # Cálculo de la envolvente convexa de cada uno de los ojos
                ojoIzqHull = cv2.convexHull(ojoIzq)
                ojoDerHull = cv2.convexHull(ojoDer)

                #Se verifica si la relación de aspecto del ojo está por debajo del umbral parpadeo
                #Incrementando el contador de cuadros de parpadeo si es así
                if ear < EYE_AR_UMBRAL:
                    CONTADOR += 1

                else:
                    #Si los ojos se cerraron durante un número suficiente de cuadros que se estableció al inicio,
                    #se aumenta el número total de parpadeos
                    if CONTADOR >= EYE_AR_CONSEC_CUADROS:
                        TOTAL += 1
                        if TOTAL == 1:
                            inicio_de_tiempo = time.time()

                        print("Total: ",TOTAL)

                    # Se reinicia el contador de cuadros
                    CONTADOR = 0    

                tiempo_final = time.time() 
                tiempo_transcurrido = tiempo_final - inicio_de_tiempo

                if tiempo_transcurrido>4:
                    #Envío de señal a otra clase
                    self.senal.emit(TOTAL)
                    if TOTAL >= 5:
                        print("Salir")
                        sys.exit()
                    inicio_de_tiempo = time.time()
                    TOTAL = 0

    def eye_aspect_ratio(self,eye):
        #calcular las distancias euclidianas entre los dos conjuntos 
        # de puntos de referencia verticales del ojo (x, y)
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

            #calcular la distancia euclidiana entre las coordenadas 
            # del punto de referencia horizontal del ojo (x, y)
        C = dist.euclidean(eye[0], eye[3])

            # Calculo de la relación de aspecto del ojo
        ear = (A + B) / (2.0 * C)

        return ear 



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

