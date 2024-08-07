import cv2

def redim(img, largura):  # função para redimensionar uma imagem
    alt = int(img.shape[0]/img.shape[1]*largura)
    img = cv2.resize(img, (largura, alt), interpolation=cv2.INTER_AREA)
    return img


df = cv2.CascadeClassifier(cv2.data.haarcascades + 
                           'haarcascade_frontalface_default.xml')

camera = cv2.VideoCapture('group.mp4')


while True:
    #read() retorna 1-Se houve sucesso e 2-O próprio frame
    (sucesso, frame) = camera.read()
    if not sucesso: #final do vídeo
        break
    #reduz tamanho do frame para acelerar processamento
    frame = redim(frame, 350)
    #converte para tons de cinza
    frame_pb = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #detecta as faces no frame
    faces = df.detectMultiScale(frame_pb, scaleFactor = 1.3,
                                minNeighbors=3, minSize=(20,20), flags=cv2.CASCADE_SCALE_IMAGE)
    frame_temp = frame.copy()
    count_frame = 0
    for (x, y, lar, alt) in faces:
        cv2.rectangle(frame_temp, (x, y), (x + lar, y + alt), (0,
                                                               255, 255), 2)
        cv2.imwrite("frame%d.jpg" % count_frame, frame_temp)
        count_frame += 1
    #Exibe um frame redimensionado (com perca de qualidade)
    cv2.imshow("Encontrando faces...", redim(frame_temp, 640))
    #Espera que a tecla 's' seja pressionada para sair
    if cv2.waitKey(1) & 0xFF == ord("s"):
        break


#fecha streaming
camera.release()
cv2.destroyAllWindows()