# -*- coding: utf-8-spanish

'''
Proyecto:   Codigo Morse
Autor:      Abdias Alvarado
'''
import os   # Importa la librería que contiene los comandos del sistema operativo.
import sys  # Importa las funciones del sistema.
import time # Importa la librería que maneja el tiempo y los hilos de ejecución.
from BaseDatos import engine, tabla_letras  # Importa nuestra base de datos.
from sqlalchemy import select, and_, update # Importa el módulo de comandos para SQL.
import pygame   # Importa la librería para gestionar el audio.
from pygame.locals import * # Importa módulos de pausa del sistema.

# Inicializa los métodos de pygame.
pygame.init()


class CodigoMorse(object):
    '''
    Es la clase principal del programa, permite las operaciones del mismo
    desde convertir de texto a morse como de morse a texto.
    '''
    # Definimos el constructor de la clase código morse.
    def __init__(self):
        # Evalúa en qué sistema está corriendo el programa.
        if sys.platform == 'linux':
            # Si está en linux, el comando para limpiar pantalla es "clear".
            self.limpiar = 'clear'
        else:
            # Si está en windows, el comando para limpiar pantalla es "cls".
            self.limpiar = 'cls'
            # Asigna el máximo de caracteres borrados
            os.system('mode con: cols=80 lines=30')

        # Crea un diccionario con las opciones del menú.
        self.opciones = {"1": self.Morse,
                         "2": self.Texto,
                         "3": self.Creditos,
                         "4": self.Salir}
        # Crea una lista para almacenar todo caracter que podrá
        # ser reconocido por el programa.
        self.listaNombres = ["A", "B",
                             "C", "D",
                             "E", "F",
                             "G", "H",
                             "I", "J",
                             "K", "L",
                             "M", "N",
                             "Ñ", "O",
                             "P", "Q",
                             "R", "S",
                             "T", "U",
                             "V", "W",
                             "X", "Y",
                             "Z", "0",
                             "1", "2",
                             "3", "4",
                             "5", "6",
                             "7", "8",
                             "9", ",",
                             ".", "?",
                             "!", ":",
                             "-", "/"]
        # Crea una lista con los códigos de tipo morse que pueden ser
        # reconocidos por el programa.
        self.listaMorse = [".-", "-...",
                           "-.-.", "-..",
                           ".", "..-.",
                           "--.", "....",
                           "..", ".---",
                           "-.-", ".-..",
                           "--", "-.",
                           "--.--", "---",
                           ".--.", "--.-",
                           ".-.", "...",
                           "-", "..-",
                           "...-", ".--",
                           "-..-", "-.--",
                           "--..", "-----",
                           ".----", "..---",
                           "...--", "....-",
                           ".....", "-....",
                           "--...", "---..",
                           "----.", "--..--",
                           ".-.-.-", "..--..",
                           "..--.", "---...",
                           "-....-", "-..-."]

    def presioneEnter(self):
        '''
        Método que hace una pausa y muestra un mensaje para que
        el programa no se ejecute de continuo y no de tiempo de
        visualizar la información.
        '''
        input('\nPresione ENTER para continuar...')

    def Morse(self):
        '''
        Método para manejar y validar el texto a convertir a código morse.
        '''
        # Limpia la pantalla
        os.system(self.limpiar)
        # Muestra la etiqueta encabezado del método.
        print(
"""
███▓▒░░ CONVIERTE A MORSE ░░▒▓███
""")
        # Almacena el texto a convertir en una variable string.
        listaTexto = input("INGRESE EL TEXTO A CONVERTIR\n")
        # Elimina los espacios en el texto y lo convierte a mayusculas.
        listaTexto = listaTexto.upper().replace(' ', '')
        # Convierte la string a formato lista.
        listaTexto = list(listaTexto)

        # Recorre el texto ingresado en busca de caracteres no reconocidos.
        for x in range(len(listaTexto)):
            # Si existe algún caracter no definido en la listaNombres
            # muestra un mensaje de error y vuelve a la función.
            if listaTexto[x] not in self.listaNombres:
                print("CARACTER NO VÁLIDO:", listaTexto[x])
                print("Volviendo...")
                # Espera dos segundos y luego vuelve a la función.
                time.sleep(2)
                self.Morse()
                return True
        # En caso de que no haya error llama a la función auxiliar
        # convertirAMorse y le envía el texto ingresado en formato
        # de lista.
        self.convertirAMorse(listaTexto)
        # Hace la pausa y espera el enter.
        self.presioneEnter()

    def Texto(self):
        '''
        Método para manejar y validar el código morse a convertir a texto.
        '''
        os.system(self.limpiar)
        print(
"""
███▓▒░░ CONVIERTE A TEXTO ░░▒▓███
""")
        # Almacena el código morse ingresado por el usuario en
        # una variable string.
        listaTexto = input("INGRESE CODIGO MORSE A CONVERTIR\n")
        # Convierte la variable string a lista.
        listaTexto = list(listaTexto)
        # Variable auxiliar para almacenar el código morse.
        listaMorse = list()

        # Almacenará símbolo a símbolo los conjuntos de n símbolos
        # Ej. --.- es un caracter.
        caracter = ""
        # Recorre la lista que contiene el código ingresado.
        for x in range(len(listaTexto)):
            # Si encuentra un espacio entiende que se acabó
            # la letra.
            if listaTexto[x] != " ":
                caracter += listaTexto[x]
            else:
                listaMorse.append(caracter)
                caracter = ""

        # Agrega el caracter a la lista auxiliar de código morse.
        listaMorse.append(caracter)

        # Evalúa que la listaMorse contenga sólo caracteres reconocidos.
        for x in range(len(listaMorse)):
            # Si encuentra algún caracter no listado muestra un mensaje
            # de error.
            if listaMorse[x] not in self.listaMorse:
                print("CÓDIGO NO VÁLIDO:", listaMorse[x])
                print("Volviendo...")
                time.sleep(2)
                self.Texto()
                return True
        # Llama al método convertirATexto para procesar la conversión.
        self.convertirATexto(listaMorse)
        self.presioneEnter()

    def Salir(self):
        '''
        Finaliza la ejecución del programa.
        '''
        exit()

    def inicializarBD(self):
        '''
        Realiza la conexión con la base de datos en SQLAlchemy.
        '''
        # Se declara la variable que contiene al objeto conexión.
        connection = engine.connect()
        # Por cada caracter disponible (reconocido) se inserta
        # su respectiva información en la base de datos.
        for x in range(len(self.listaNombres)):
            # Contiene un comando de inserción a la tabla_letras
            insertar = tabla_letras.insert(
                                             values=dict(
                                                         caracterTexto=self.listaNombres[x],
                                                         codigoMorse=self.listaMorse[x],
                                                         )
                                            )
            # Se ejecuta el query alojado en la variable "insertar" y
            # el resultado se almacena en "resultado"
            resultado = connection.execute(insertar)
        # Finaliza la conexión con la base de datos.
        connection.close()

    def Creditos(self):
        '''
        Despliega la información del programa.
        '''
        os.system(self.limpiar)
        print(
"""
█████▓▒░░ CREDITOS ░░▒▓█████

          UNICAH
 CAMPUS JESUS SACRAMENTADO
NUESTRA SEÑORA REINA DE PAZ
  PROYECTO CIENTIFICA I

    PROGRAMADO POR:
    Abdias Alvarado


""")
        self.presioneEnter()

    def run(self):
        '''
        Es el método principal del programa.
        '''
        # Mientras sea verdadero y el usuario no elija "Salir"
        # va a desplegar el menú y pedir la selección.
        while True:
            os.system(self.limpiar)
            self.desplegarMenu()
            eleccion = input("SELECCIONE UNA OPCIÓN: ")
            # Busca la opción el diccionario declarado anteriormente.
            accion = self.opciones.get(eleccion)
            # Si existe una acción, entonces ejecute el método que
            # corresponde a esa acción según el diccionario de datos.
            if accion:
                accion()
            else:
                # Si no hay una acción coicidente, muestra el error.
                print("{0}, NO ES UNA OPCIÓN VÁLIDA.", format(eleccion))

    def desplegarMenu(self):
        '''
        Despliega el menú principal de programa.
        '''
        print(
"""

,---.         |o              ,-.-.
|    ,---.,---|.,---.,---.    | | |,---.,---.,---.,---.
|    |   ||   |||   ||   |    | | ||   ||    `---.|---'
`---'`---'`---'``---|`---'    ` ' '`---'`    `---'`---'
                `---'

1. TEXTO A MORSE

2. MORSE A TEXTO

3. CRÉDITOS

4. SALIR

""")

    def convertirAMorse(self, listaTexto):
        '''
        Método que convierte a código morse una lista de texto
        ingresada por el usuario.
        '''
        # Funciona como lista temporal para almacenar desde
        # la base de datos cada conjunto de símbolos que representan
        # una letra en código morse.
        listaEnMorse = list()

        # Variables para concatener los puntos y guiones de un
        # caracter en morse.
        stringConcatenado = ""
        stringTexto = ""

        # Como se validó antes de llamar a este método que todos
        # los caracteres existieran en la base de datos, se utiliza
        # un ciclo para almacenar cada caracter en morse en la lista
        # temporal.
        for x in range(len(listaTexto)):
            listaEnMorse.append(self.buscarTextoEnBD(listaTexto[x]))

        # Prepara el texto y el código morse para imprimirlos en la
        # pantalla de forma paralela.
        for x in range(len(listaEnMorse)):
            stringTexto += listaTexto[x]
            stringTexto += ""
            stringConcatenado += listaEnMorse[x]
            stringConcatenado += "  "

        # Imprime los resultados.
        print("Texto:   {0}".format(stringTexto))
        print("Morse:   {0}".format(stringConcatenado))

        # Inicia la reproducción de cada caracter emitiendo un sonido
        # similar al del telégrafo.
        for x in range(len(listaTexto)):
            self.reproducir(listaTexto[x].lower())

    def reproducir(self, caracter):
        '''
        Realiza la reproducción de los archivos de audio
        correspondientes a cada caracter.
        '''
        # En caso de que el caracter sea especial se transforma
        # al nombre con que el que se llama al archivo de audio.
        if caracter == "/":
            caracter = "pleca"

        if caracter == ".":
            caracter = "punto"

        if caracter == ",":
            caracter = "coma"

        if caracter == ":":
            caracter = "dosPuntos"

        if caracter == "!":
            caracter = "admiracion"

        if caracter == "?":
            caracter = "interrogacion"

        if caracter == "-":
            caracter = "guion"

        # Reproduce el archivo con el nombre
        # asignado.
        ruta = "Recursos/" + caracter + ".mp3"
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play()
        time.sleep(1.5)
        pygame.mixer.music.stop()

    def convertirATexto(self, listaMorse):
        '''
        Convierte el código morse ingresado a texto.
        '''
        # Lista temporal para obtener desde la base datos
        # los caracteres correspondientes a un código.
        listaTexto = list()

        # Variables para concatenar el texto y el código morse
        # a buscar.
        stringTexto = ""
        stringMorse = ""

        # Extrae desde la base de datos los valores correspondientes
        # a cada código.
        for x in range(len(listaMorse)):
            listaTexto.append(self.buscarMorseEnBD(listaMorse[x]))

        # Prepara los resultados para mostrar.
        for x in range(len(listaMorse)):
            stringMorse += listaMorse[x]
            stringMorse += "  "
            stringTexto += listaTexto[x]
            stringTexto += " "

        # Muestra los resultados obtenidos.
        print("Texto:   {0}".format(stringTexto))
        print("Morse:   {0}".format(stringMorse))

        # Inicia la reproducción del audio.
        for x in range(len(listaTexto)):
            self.reproducir(listaTexto[x].lower())

    def buscarTextoEnBD(self, caracterABuscar):
        '''
        Realiza una consulta a la base de datos para
        verificar si existe o no un caracter específico.

        Retorna el código morse correspondiente.
        '''
        connection = engine.connect()
        seleccionar = select([tabla_letras],
                             and_(tabla_letras.c.caracterTexto == caracterABuscar))
        resultado = connection.execute(seleccionar)

        registros = [dict(row) for row in resultado]

        return registros[0]['codigoMorse']

    def buscarMorseEnBD(self, caracterABuscar):
        '''
        Realiza una consulta a la base de datos para
        verificar si existe o no un código morse específico.

        Retorna el caracter texto correspondiente.
        '''
        connection = engine.connect()
        seleccionar = select([tabla_letras],
                             and_(tabla_letras.c.codigoMorse == caracterABuscar))
        resultado = connection.execute(seleccionar)

        registros = [dict(row) for row in resultado]

        return registros[0]['caracterTexto']

# Inicia el programa.
if __name__ == "__main__":
    codigomorse = CodigoMorse()
    codigomorse.run()
