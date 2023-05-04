from tkgpio import TkCircuit
from json import load
import requests
import data

chave = "lCUNZizgFrXAN3QPY-iSS1IkweQeK3HLKG3iUzAbspn"
estaLigada = False
numero = ""

with open("configuracoes.json", "r") as file:
  configuration = load(file)

circuit = TkCircuit(configuration)


@circuit.run
def main():

  from Adafruit_CharLCD import Adafruit_CharLCD
  from gpiozero import LED, Button, MotionSensor
  from lirc import init, nextcode
  from time import sleep

  def criar_leds():
    return {
      "ligada": LED(10),
      "1": LED(11),
      "2": LED(12),
      "3": LED(13),
      "4": LED(21),
      "5": LED(22),
      "6": LED(23),
      "7": LED(31),
      "8": LED(32),
      "9": LED(33),
    }

  def criar_botoes():
    return {"ligar": Button(8), "desligar": Button(9)}

  lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 5, 1)
  botoes = criar_botoes()
  leds = criar_leds()
  motion_sensor = MotionSensor(51)

  init("default")

  def ligar_maquina():
    mensagem = {
      "value1": "Ligada",
      "value2": "Processando",
      "value3": "Status"
    }
    print("Maquina ligada, cheque o status por email")
    evento = "ligar_maquina"
    endereco = "https://maker.ifttt.com/trigger/" + evento + "/with/key/" + chave
    resposta = requests.post(endereco, data=mensagem)
    global estaLigada

    estaLigada = True
    leds["ligada"].on()

  def desligar_maquina():
    global estaLigada
    global numero

    estaLigada = False
    lcd.clear()
    numero = ""
    for chave, valor in leds.items():
      valor.off()

  botoes["ligar"].when_pressed = ligar_maquina
  botoes["desligar"].when_pressed = desligar_maquina

  while True:
    global estaLigada
    global numero

    codigo = nextcode()
    if estaLigada == True and codigo != []:
      valor = (codigo[0])[4:]
      lcd.clear()
      lcd.message(valor)

      if valor == "CLEAR":
        sleep(2.0)
        lcd.clear()
        numero = ""
      elif valor == "OK":
        if numero in leds:
          lcd.clear()
          led = leds[numero]
          led.on()
          numero = ""
          motion_sensor.when_motion = led.off
        else:
          lcd.clear()
          lcd.message("ERROR")
          sleep(2.0)
          lcd.clear()
          numero = ""
      else:
        numero = numero + valor
    sleep(0.2)
