import tkinter as tk
from tkinter import messagebox

# Función que se ejecuta cuando se presiona el botón
def mostrar_mensaje():
    messagebox.showinfo("Mensaje", "Te amo")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Ventana Roja")
ventana.geometry("300x200")
ventana.configure(bg="red")

# Crear un botón blanco en el centro
boton = tk.Button(ventana, text="Presióname", command=mostrar_mensaje, bg="white", fg="black")
boton.pack(expand=True)

# Iniciar el bucle principal de la ventana
ventana.mainloop()
