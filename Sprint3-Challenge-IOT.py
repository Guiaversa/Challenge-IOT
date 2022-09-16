from datetime import datetime
import requests
import os.path
import cv2
import time
import pyttsx3
import mediapipe as mp
import speech_recognition as sr



webcam = cv2.VideoCapture(0)

solucao_reconhecimento_rosto = mp.solutions.face_detection

reconhecedor_de_rostos = solucao_reconhecimento_rosto.FaceDetection()

desenho = mp.solutions.drawing_utils

while True:

    verificador, frame = webcam.read()

    if not verificador:
        break
    lista_rostos = reconhecedor_de_rostos.process(frame)

    if lista_rostos.detections:
        for rosto in lista_rostos.detections:
            desenho.draw_detection(frame, rosto)

        if lista_rostos.detections:
            time.sleep(3)
            print("Rosto reconhecido")
            break

    cv2.imshow("Rostos na Webcam", frame)

    if cv2.waitKey(5) == 27:
        break

webcam.release()
cv2.destroyAllWindows()

print("Iniciando FindVision")




def FindVision():
    mic = sr.Recognizer()

    with sr.Microphone() as source:
        mic.adjust_for_ambient_noise(source)
        print("fale:")

        audio = mic.listen(source)

        try:
            frase = mic.recognize_google(audio, language='pt').lower()
            print("Texto reconhecido: " + frase)

        except sr.UnknownValueError:
            print("Não entendi")
        return frase


def buscar_clima(cidade):
    API_KEY = "11c95aecdde84bed43cb10a7c167a494"  
    city = cidade  

    link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=pt_br"
    requisicao = requests.get(link)
    dados = requisicao.json()
    descricao = dados['weather'][0]['description']
    temp = round(dados['main']['temp'] - 273.00, 1)

    frase = "Hoje está {} na cidade {} e está fazendo {} graus".format(descricao, city, temp)

    return frase


def data_atual():
    meses = {1: "Janeiro", 2: "fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho",
             8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}

    dia = datetime.today().day

    if datetime.today().month in meses.keys():
        mes = meses.get(datetime.today().month)

    ano = datetime.today().year

    texto = "hoje é dia " + str(dia) + " do mês de " + str(mes) + " do ano " + str(ano)

   
    return texto


def horas():
    agora = datetime.now()

    hora = agora.hour
    minuto = agora.minute

    texto = "Agora são " + str(hora) + " horas e " + str(minuto) + " minutos"

    return texto

vision = pyttsx3.init()

vision.setProperty('voice', b'brasil')
vision.setProperty('rate', 250)
vision.setProperty('volume', 1)

while True:
    resultado = FindVision()

    if resultado == "vision" or resultado == "vision":
        vision.say("Ola como posso ajudar?")
        vision.runAndWait()

        while True:
            resp = FindVision()

            if resp == "cadastrar evento na agenda":
                with open("agenda.txt", 'a', encoding="utf-8") as f:
                    vision.say("Ok, qual evento devo cadastrar? ")
                    vision.runAndWait()

                    resp = FindVision()

                    f.write(resp)
                    f.write("\n")

                    vision.say("Evento cadastrado com sucesso! posso te ajudar em mais alguma coisa?")
                    vision.runAndWait()

                    resp = FindVision()

                    if resp == "ler agenda" or resp == "leia agenda":
                        with open("./agenda.txt", 'r', encoding="utf-8") as agendaCadastrada:
                            fala = ",".join(agendaCadastrada.readlines())
                            print(fala)
                            vision.say(fala)
                            vision.runAndWait()

                    elif resp == "não" or resp == "nao":
                        vision.say("Ok mestre tenha um bom dia!")
                        vision.runAndWait()
                        break
                    else:
                        vision.say("O comando cadastrar evento encerrou")
                        vision.runAndWait()
                        break

            
            if resp == "ler agenda" or resp == "leia agenda":

                if not os.path.exists("./agenda.txt"):
                    vision.say("o senhor ainda não cadastrou nenhum evento na agenda!")
                    vision.runAndWait()
                    break
                else:
                    with open("./agenda.txt", 'r', encoding="utf-8") as agendaCadastrada:
                        fala = ",".join(agendaCadastrada.readlines())
                        print(fala)
                        vision.say(fala)
                        vision.runAndWait()
                        break
         
            if resp == "que dia é hoje?" or resp == "que dia é hoje":
                texto = data_atual()
                vision.say(texto)
                vision.runAndWait()
                break

            
            if resp == "que horas são":
                texto = horas()
                vision.say(texto)
                vision.runAndWait()
                break

            
            if resp == "abra a calculadora" or resp == "abra calculadora":
                vision.say("A calculadora está aberta, oque deseja calcular?")
                vision.runAndWait()
                frase = FindVision()
                calcular = frase.split()
                if calcular[1] == 'x':
                    result = int(calcular[0]) * int(calcular[2])
                    vision.say("O resultado é: {}".format(result))
                    vision.runAndWait()
                elif calcular[1] == '+':
                    result = int(calcular[0]) + int(calcular[2])
                    vision.say("O resultado é: {}".format(result))
                    vision.runAndWait()
                elif calcular[1] == '-':
                    result = int(calcular[0]) - int(calcular[2])
                    vision.say("O resultado é: {}".format(result))
                    vision.runAndWait()
                else:
                    result = int(calcular[0]) / int(calcular[2])
                    vision.say("O resultado é: {}".format(result))
                    vision.runAndWait()
                break

            
            if resp == "qual a previsão de hoje":
                vision.say("De qual cidade deseja saber o clima?")
                vision.runAndWait()
                resp = FindVision()
                clima = buscar_clima(resp)
                vision.say(clima)
                vision.runAndWait()
                break

            
            if  resp == "cadê minhas chaves":
                vision.say("Esta em cima do movel da sala a sua direita")
                vision.runAndWait()
                resp = FindVision()
                break

            if  resp == "obrigado" or resp == "obrigada":
                vision.say("Imagina estou aqui para isso!")
                vision.runAndWait()
                resp = FindVision()
                break

    else:
        print("Não entendi o que voce disse")
