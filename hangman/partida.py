import csv
import uuid
from main import Hangman
from datetime import datetime


class Partida:
    def __init__(self, jugador):
        # Constructor de la clase Partida
        # Toma como parámetro el nombre del jugador

        # Guarda el nombre del jugador en el atributo 'jugador'
        self.jugador = jugador

        # Crea una instancia de la clase Hangman y la asigna al atributo 'hangman'
        # Esta instancia se utilizará para cargar las palabras y obtener palabras aleatorias
        self.hangman = Hangman()

        # Inicializa el número de intentos restantes para cada ronda del juego
        self.intentos_restantes = 6

        # Inicializa una cadena vacía para almacenar la palabra que el jugador debe adivinar en cada ronda
        self.palabra = ""

        # Inicializa una lista vacía que contendrá las letras adivinadas por el jugador en la palabra
        self.letras_adivinadas = []

        # Inicializa una lista vacía que contendrá las letras que el jugador ha intentado adivinar, tanto correctas como incorrectas
        self.letras_usadas = []

        # Inicializa el atributo 'puntuacion' con un valor de 0, que se usará para registrar la puntuación del jugador al finalizar la partida
        self.puntuacion = 0

        # Genera un identificador único (UUID) para la partida y lo guarda en el atributo 'game_id'
        # Este identificador se utilizará para identificar de manera única cada partida en el juego
        self.game_id = str(uuid.uuid4())

        # Define el número de rondas que tendrá la partida. En este caso, se establece en 3
        self.rondas = 3

        # Inicializa un contador para llevar el seguimiento de la ronda actual en la partida
        self.ronda_actual = 0

        # Inicializa un contador para contar las rondas ganadas por el jugador durante la partida
        self.rondas_ganadas = 0

    def iniciar_partida(self):
        # Método para iniciar una nueva partida

        # Carga las palabras desde el archivo 'words.csv' utilizando el método 'load' de la instancia de Hangman
        self.hangman.load('words.csv')

        # Verifica si se cargaron correctamente todas las palabras
        if not self.hangman.get_number_of_words():
            # Si no se cargaron todas las palabras, devuelve False y termina la partida
            return False

        # Si se cargaron todas las palabras correctamente, devuelve True para indicar que la partida puede comenzar
        return True

    def iniciar_ronda(self):
        # Método para iniciar una nueva ronda

        # Incrementa el número de la ronda actual en 1
        self.ronda_actual += 1

        # Restablece el número de intentos restantes para la nueva ronda
        self.intentos_restantes = 6

        # Obtiene una nueva palabra aleatoria utilizando el método 'obtener_palabra_aleatoria' de la instancia de Hangman
        self.palabra = self.hangman.obtener_palabra_aleatoria()

        # Inicializa la lista 'letras_adivinadas' con barras bajas (_) para representar las letras que se deben adivinar
        self.letras_adivinadas = ['_'] * len(self.palabra)

        # Inicializa la lista 'letras_usadas' como vacía para almacenar las letras que el jugador ha intentado adivinar en la nueva ronda
        self.letras_usadas = []

    def adivinar(self, letra):
        # Método para intentar adivinar una letra en la palabra

        # Verifica si la letra ya ha sido usada antes
        if letra in self.letras_usadas:
            print("Ya has intentado esta letra. Intenta con otra.")
            return

        # Agrega la letra a la lista de letras usadas
        self.letras_usadas.append(letra)

        # Verifica si la letra está en la palabra
        if letra in self.palabra:
            # Si la letra está en la palabra, actualiza las letras adivinadas con la nueva letra
            for i in range(len(self.palabra)):
                if self.palabra[i] == letra:
                    self.letras_adivinadas[i] = letra
        else:
            # Si la letra no está en la palabra, decrementa el número de intentos restantes
            self.intentos_restantes -= 1

    def imprimir_estado(self):
        print(self.dibujar_ahorcado())
        print("Palabra: ", " ".join(self.letras_adivinadas))
        print("Letras usadas: ", ", ".join(self.letras_usadas))
        print("Intentos restantes:", self.intentos_restantes)

    def dibujar_ahorcado(self):
        dibujo = [
            "------------",
            "|              |"
        ]
        if self.intentos_restantes < 3:
            dibujo.append("|              O")
        if self.intentos_restantes < 2:
            dibujo.append("|             \\|/")
        if self.intentos_restantes <= 1:
            dibujo.append("|	          / \\")
        dibujo.append("-----")
        return "\n".join(dibujo)

    def juego_terminado(self):
        # Método para verificar si el juego ha terminado

        # Verifica si no hay más barras bajas (_) en la lista de letras adivinadas
        if '_' not in self.letras_adivinadas:
            # Si no hay más barras bajas, significa que el jugador ha adivinado todas las letras de la palabra
            print("¡Felicidades! Has adivinado la palabra:", self.palabra)

            # Aumenta el contador de rondas ganadas
            self.rondas_ganadas += 1

            # Aumenta la puntuación si se completa la ronda
            self.puntuacion += 1

            # Devuelve True para indicar que el juego ha terminado
            return True

        # Verifica si se han agotado todos los intentos restantes
        elif self.intentos_restantes == 0:
            # Si se han agotado los intentos restantes, el jugador ha perdido
            print("¡Oh no! Has perdido. La palabra era:", self.palabra)

            # Devuelve True para indicar que el juego ha terminado
            return True

        # Si ninguna de las condiciones anteriores se cumple, el juego aún no ha terminado
        return False

    def registrar_puntuacion(self):
        # Método para registrar la puntuación y los detalles de la partida

        # Determinar si el jugador ha ganado todas las rondas
        victory = self.rondas_ganadas == self.rondas

        # Registrar la puntuación en games.csv
        with open('games.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # Escribir la fila de nombres de columnas si el archivo está vacío
            if file.tell() == 0:
                writer.writerow(["game_id", "username", "start_date", "end_date", "final_score"])
            # Obtener la fecha y hora actual
            start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Escribir la fila con los detalles de la partida en games.csv
            writer.writerow([self.game_id, self.jugador, start_date, end_date, self.puntuacion])

        # Registrar los detalles de la ronda en rounds_in_games.csv
        with open('rounds_in_games.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # Escribir la fila de nombres de columnas si el archivo está vacío
            if file.tell() == 0:
                writer.writerow(["game_id", "word", "username", "round_id", "user_trys", "victory"])
            # Escribir los detalles de cada ronda en rounds_in_games.csv
            for round_id, letra in enumerate(self.letras_usadas, start=1):
                victory = letra == self.palabra and self.puntuacion == 1
                writer.writerow(
                    [self.game_id, self.palabra, self.jugador, round_id, 6 - self.intentos_restantes, victory])


def main():
    # Función principal del juego

    # Solicitar al jugador que ingrese su nombre de usuario
    jugador = input("Por favor, ingresa tu nombre de usuario: ")
    # Crear una instancia de la clase Partida
    partida = Partida(jugador)

    # Iniciar la partida si se cumple la condición
    if partida.iniciar_partida():
        # Iterar sobre el número de rondas en la partida
        for _ in range(partida.rondas):
            # Iniciar una nueva ronda
            partida.iniciar_ronda()
            # Mientras la ronda no esté terminada
            while not partida.juego_terminado():
                # Imprimir el estado actual del juego
                partida.imprimir_estado()
                # Solicitar al jugador que ingrese una letra
                letra = input("Ingresa una letra: ").lower()
                # Validar la entrada del jugador
                if len(letra) != 1 or not letra.isalpha():
                    print("Por favor, ingresa una letra válida.")
                    continue
                # Procesar la letra ingresada por el jugador
                partida.adivinar(letra)
            # Imprimir el mensaje de fin de la ronda y la puntuación parcial
            print(f"Fin de la ronda {partida.ronda_actual}. Puntuación parcial: {partida.puntuacion}")

        # Registrar la puntuación final
        partida.registrar_puntuacion()


if __name__ == "__main__":
    # Esta condición verifica si el script se está ejecutando como el programa principal

    # Llama a la función main() para iniciar el juego
    main()

