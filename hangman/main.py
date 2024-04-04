import csv
import random

class Hangman:
    def __init__(self):
        # Inicializa la lista de palabras
        self.palabras = []

    def load(self, filename):
        # Método para cargar las palabras desde el archivo CSV
        with open(filename, 'r') as file:
            # Abrir el archivo CSV
            reader = csv.reader(file)
            next(reader)  # Saltar la primera fila que contiene el encabezado
            # Leer las palabras del archivo y almacenarlas en la lista de palabras
            self.palabras = [row[0] for row in reader]

    def get_number_of_words(self):
        # Método para verificar si se han cargado suficientes palabras
        if len(self.palabras) == 30:
            print("Palabras listas, ¡adelante!")
            return True
        else:
            print("Vaya, parece que no encontramos todas las palabras necesarias, no podemos dar comienzo al juego")
            return False

    def obtener_palabra_aleatoria(self):
        # Método para obtener una palabra aleatoria de la lista de palabras
        return random.choice(self.palabras)

if __name__ == "__main__":
    # Bloque principal del programa

    # Crear una instancia de la clase Hangman
    hangman = Hangman()
    # Cargar las palabras desde el archivo CSV
    hangman.load('words.csv')
    # Verificar si se han cargado suficientes palabras
    if hangman.get_number_of_words():
        print("Todo listo para comenzar el juego.")
