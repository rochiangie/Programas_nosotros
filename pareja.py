import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import datetime

# Preguntas para el juego
preguntas = [
    "¿Cuál es tu recuerdo favorito?",
    "¿Qué te hace reír?",
    "¿Qué es lo que más valoras en una amistad?",
    "¿Cuál es tu mayor sueño?",
    "¿Qué te hace sentir amado/a?"
]

# Función para el juego de preguntas
def juego_preguntas():
    pregunta = random.choice(preguntas)
    respuesta = simpledialog.askstring("Juego de Preguntas", pregunta)
    
    if respuesta:
        with open("respuestas.txt", "a") as archivo:
            archivo.write(f"Pregunta: {pregunta}\nRespuesta: {respuesta}\nFecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        messagebox.showinfo("Gracias", "Tu respuesta ha sido guardada.")
    else:
        messagebox.showwarning("Sin Respuesta", "No se ha proporcionado ninguna respuesta.")

# Función para registrar emociones manualmente
def registrar_emocion():
    emocion = simpledialog.askstring("Registro de Emoción", "¿Cómo te sientes hoy?")
    
    if emocion:
        with open("emociones.txt", "a") as archivo:
            archivo.write(f"Emoción: {emocion}\nFecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        messagebox.showinfo("Emoción Guardada", "Tu estado de ánimo ha sido guardado.")
    else:
        messagebox.showwarning("Sin Emoción", "No se ha ingresado ningún estado de ánimo.")

# Función para agregar un recordatorio personalizado
def agregar_recordatorio():
    recordatorio = simpledialog.askstring("Nuevo Recordatorio", "Escribe el recordatorio:")
    fecha = simpledialog.askstring("Fecha del Recordatorio", "Ingresa la fecha (YYYY-MM-DD HH:MM):")
    
    if recordatorio and fecha:
        with open("recordatorios.txt", "a") as archivo:
            archivo.write(f"Recordatorio: {recordatorio}\nFecha: {fecha}\n\n")
        messagebox.showinfo("Recordatorio Guardado", "Tu recordatorio ha sido guardado.")
    else:
        messagebox.showwarning("Datos Incompletos", "Debes ingresar el recordatorio y la fecha.")

# Función para mostrar los recordatorios guardados
def mostrar_recordatorios():
    try:
        with open("recordatorios.txt", "r") as archivo:
            recordatorios = archivo.read()
        if recordatorios:
            messagebox.showinfo("Recordatorios", recordatorios)
        else:
            messagebox.showinfo("Recordatorios", "No hay recordatorios guardados aún.")
    except FileNotFoundError:
        messagebox.showinfo("Recordatorios", "No hay recordatorios guardados aún.")

# Función para guardar una nota
def guardar_nota():
    nota = entrada_nota.get("1.0", tk.END).strip()
    if nota:
        with open("notas.txt", "a") as archivo:
            archivo.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {nota}\n")
        entrada_nota.delete("1.0", tk.END)
        messagebox.showinfo("Nota Guardada", "Tu nota ha sido guardada.")
    else:
        messagebox.showwarning("Advertencia", "La nota no puede estar vacía.")

#TE AMOOOO

# Función para mostrar las notas guardadas
def mostrar_notas():
    try:
        with open("notas.txt", "r") as archivo:
            notas = archivo.read()
        if notas:
            messagebox.showinfo("Notas Guardadas", notas)
        else:
            messagebox.showinfo("Notas Guardadas", "No hay notas guardadas aún.")
    except FileNotFoundError:
        messagebox.showinfo("Notas Guardadas", "No hay notas guardadas aún.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Comunicación Mejorada")
ventana.configure(bg="light blue")

# Botones de las opciones
boton_preguntas = tk.Button(ventana, text="Juego de Preguntas", command=juego_preguntas, bg="white", font=("Helvetica", 12))
boton_preguntas.pack(pady=10)

boton_emociones = tk.Button(ventana, text="Registro de Emociones", command=registrar_emocion, bg="white", font=("Helvetica", 12))
boton_emociones.pack(pady=10)

boton_recordatorios = tk.Button(ventana, text="Agregar Recordatorio", command=agregar_recordatorio, bg="white", font=("Helvetica", 12))
boton_recordatorios.pack(pady=10)

boton_mostrar_recordatorios = tk.Button(ventana, text="Mostrar Recordatorios", command=mostrar_recordatorios, bg="white", font=("Helvetica", 12))
boton_mostrar_recordatorios.pack(pady=10)

# Entrada y botones para las notas
entrada_nota = tk.Text(ventana, height=5, width=40, font=("Helvetica", 12))
entrada_nota.pack(pady=10)

boton_guardar_nota = tk.Button(ventana, text="Guardar Nota", command=guardar_nota, bg="white", font=("Helvetica", 12))
boton_guardar_nota.pack(pady=5)

boton_mostrar_notas = tk.Button(ventana, text="Mostrar Notas Guardadas", command=mostrar_notas, bg="white", font=("Helvetica", 12))
boton_mostrar_notas.pack(pady=5)

# Ejecutar el bucle principal de la aplicación
ventana.mainloop()
