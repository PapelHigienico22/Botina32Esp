import cv2
import numpy as np
import serial

#using python 3.8.3v
COM = 'COM3'
BAUD = 9600
ser = serial.Serial(COM, BAUD)

ANCHO_PANTALLA = 680
parte = ANCHO_PANTALLA / 7

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
azulBajo = np.array([90, 100, 50], np.uint8)
azulAlto = np.array([118, 255, 255], np.uint8)

while True:
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mascara = cv2.inRange(frameHSV, azulBajo, azulAlto)
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contornos, -1, (255, 0, 0), 4)

        for c in contornos:
            area = cv2.contourArea(c)
            if area > 200:
                M = cv2.moments(c)
                if M["m00"] == 0:
                    M["m00"] = 1
                x = int(M["m10"] / M["m00"])
                y = int(M['m01'] / M['m00'])
                cv2.circle(frame, (x, y), 7, (0, 0, 255), -1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
                nuevoContorno = cv2.convexHull(c)
                cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0), 3)

                if 0 < x <= parte:
                    print("Mover a la izquierda 100%")
                    ser.write(b"izq1\n")
                elif parte < x <= parte * 2:
                    print("Mover a la izquierda 60%")
                    ser.write(b"izq2\n")
                elif parte * 2 < x <= parte * 3:
                    print("Mover a la izquierda 30%")
                    ser.write(b"izq3\n")
                # Mover al centro
                elif parte * 3 < x <= parte * 4:
                    print("Mover al centro")
                    ser.write(b"ctr\n")
                elif parte * 4 <= x < parte * 5:
                    print("moviendo a la derecha 30%")
                    ser.write(b"der3\n")
                elif parte * 5 <= x < parte * 6:
                    print("moviendo a la derecha 60%")
                    ser.write(b"der2\n")
                elif x >= parte * 6:
                    print("Moviendo a la derecha 100%")
                    ser.write(b"der1\n")
                else:
                    print("no se detecto movimiento")
                    ser.write(b"parar\n")

        # cv2.imshow('mascaraAzul', mascara)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            ser.close()
            break
cap.release()
cv2.destroyAllWindows()
