import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

class ConflictResolutionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramienta de Resolución de Conflictos")
        
        # Título
        self.label = tk.Label(root, text="Herramienta de Resolución de Conflictos", font=("Arial", 16))
        self.label.pack(pady=10)
        
        # Selección de tipo de conflicto
        self.tipo_label = tk.Label(root, text="Selecciona el tipo de conflicto:")
        self.tipo_label.pack()
        
        self.tipo_conflicto = tk.StringVar(value="interpersonal")
        tk.Radiobutton(root, text="Interpersonal", variable=self.tipo_conflicto, value="interpersonal").pack(anchor="w")
        tk.Radiobutton(root, text="De pareja", variable=self.tipo_conflicto, value="pareja").pack(anchor="w")
        
        # Descripción del problema
        self.problema_label = tk.Label(root, text="Describe el problema:")
        self.problema_label.pack()
        
        self.problema_entry = tk.Entry(root, width=50)
        self.problema_entry.pack(pady=5)
        
        # Método de resolución
        self.metodo_label = tk.Label(root, text="Elige un método de resolución:")
        self.metodo_label.pack()
        
        self.metodo = tk.StringVar(value="negociación")
        tk.Radiobutton(root, text="Negociación", variable=self.metodo, value="negociación").pack(anchor="w")
        tk.Radiobutton(root, text="Mediación", variable=self.metodo, value="mediación").pack(anchor="w")
        tk.Radiobutton(root, text="Solución directa", variable=self.metodo, value="directa").pack(anchor="w")
        
        # Botón de enviar
        self.submit_button = tk.Button(root, text="Enviar", command=self.resolver_conflicto)
        self.submit_button.pack(pady=10)
        
        # Botón para sugerir el mejor método
        self.best_method_button = tk.Button(root, text="Sugerir Mejor Método", command=self.sugerir_mejor_metodo)
        self.best_method_button.pack(pady=5)
        
    def resolver_conflicto(self):
        tipo_conflicto = self.tipo_conflicto.get()
        problema = self.problema_entry.get()
        metodo = self.metodo.get()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Aquí llamamos a la función que maneja la resolución basada en el flujo de decisión.
        resolucion = self.determinar_resolucion(tipo_conflicto, problema, metodo)
        
        # Mostrar la resolución
        messagebox.showinfo("Resolución", resolucion)
        
        # Registrar decisión - Simulación de éxito
        exito = messagebox.askyesno("Retroalimentación", "¿Te ayudó esta resolución?")
        self.registrar_decision(tipo_conflicto, metodo, exito, fecha)
    
    def determinar_resolucion(self, tipo_conflicto, problema, metodo):
        # Escenarios predefinidos simplificados
        if tipo_conflicto == "interpersonal":
            if metodo == "negociación":
                return "Se sugieren pasos de negociación para conflictos interpersonales."
            elif metodo == "mediación":
                return "Se sugieren pasos de mediación para conflictos interpersonales."
            else:
                return "Se sugiere una solución directa para conflictos interpersonales."
        elif tipo_conflicto == "pareja":
            if metodo == "negociación":
                return "Se sugieren pasos de negociación para conflictos de pareja."
            elif metodo == "mediación":
                return "Se sugieren pasos de mediación para conflictos de pareja."
            else:
                return "Se sugiere una solución directa para conflictos de pareja."
        return "No se encontró una resolución."
    
    def registrar_decision(self, tipo_conflicto, metodo, exito, fecha):
        try:
            with open('retroalimentacion_usuario.json', 'r') as f:
                datos = json.load(f)
        except FileNotFoundError:
            datos = {}
        
        if tipo_conflicto not in datos:
            datos[tipo_conflicto] = {}
        if metodo not in datos[tipo_conflicto]:
            datos[tipo_conflicto][metodo] = {'exito': 0, 'total': 0, 'fechas': []}
        
        datos[tipo_conflicto][metodo]['total'] += 1
        if exito:
            datos[tipo_conflicto][metodo]['exito'] += 1
        datos[tipo_conflicto][metodo]['fechas'].append(fecha)
        
        with open('retroalimentacion_usuario.json', 'w') as f:
            json.dump(datos, f, indent=4)

    def determinar_mejor_metodo(self, tipo_conflicto):
        try:
            with open('retroalimentacion_usuario.json', 'r') as f:
                datos = json.load(f)
        except FileNotFoundError:
            return "No hay datos disponibles."
        
        if tipo_conflicto in datos:
            mejor_metodo = max(datos[tipo_conflicto], key=lambda k: datos[tipo_conflicto][k]['exito'])
            return f"Basado en la retroalimentación previa, {mejor_metodo} tiene la mayor tasa de éxito."
        return "No hay datos disponibles."
    
    def sugerir_mejor_metodo(self):
        tipo_conflicto = self.tipo_conflicto.get()
        sugerencia = self.determinar_mejor_metodo(tipo_conflicto)
        messagebox.showinfo("Sugerencia de Mejor Método", sugerencia)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConflictResolutionApp(root)
    root.mainloop()

