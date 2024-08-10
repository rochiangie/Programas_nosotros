import tkinter as tk
import random

# Lista de frases sin sentido
frases = [
    "La luna es de queso pero no se come.",
    "Los elefantes bailan tango bajo la lluvia.",
    "Las nubes son algodón de azúcar que se derritió.",
    "Los relojes tienen miedo de los gatos.",
    "El agua del mar es en realidad sopa de letras.",
    "Los árboles hablan en susurros cuando no los ves.",
    "Las montañas son tortugas gigantes dormidas.",
    "Las hormigas organizan conciertos de rock por la noche."
]

# Función para generar una frase aleatoria
def generar_frase():
    frase.set(random.choice(frases))

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Generador de Frases Sin Sentido")
ventana.configure(bg="light blue")

# Variable para almacenar la frase
frase = tk.StringVar()
frase.set("Presiona el botón para generar una frase sin sentido.")

# Etiqueta para mostrar la frase
etiqueta_frase = tk.Label(ventana, textvariable=frase, bg="light blue", wraplength=300, font=("Helvetica", 12))
etiqueta_frase.pack(pady=20)

# Botón para generar una nueva frase
boton_generar = tk.Button(ventana, text="Generar Frase", command=generar_frase, bg="white", font=("Helvetica", 12))
boton_generar.pack(pady=20)

# Ejecutar el bucle principal de la aplicación
ventana.mainloop()
