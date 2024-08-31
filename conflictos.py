import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime

class ConflictResolutionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramienta de Resolución de Conflictos")

        # Iniciar el flujo de la aplicación
        self.seleccionar_tipo_conflicto()

    def seleccionar_tipo_conflicto(self):
        # Ventana para seleccionar el tipo de conflicto
        self.limpiar_ventana()
        tk.Label(self.root, text="Selecciona el tipo de conflicto:", font=("Arial", 16)).pack(pady=10)

        self.tipo_conflicto = tk.StringVar()
        tk.Radiobutton(self.root, text="Interpersonal", variable=self.tipo_conflicto, value="interpersonal").pack(anchor="w")
        tk.Radiobutton(self.root, text="De pareja", variable=self.tipo_conflicto, value="pareja").pack(anchor="w")

        tk.Button(self.root, text="Continuar", command=self.seleccionar_problema).pack(pady=20)

    def seleccionar_problema(self):
        # Ventana para seleccionar o ingresar el problema
        self.limpiar_ventana()
        tk.Label(self.root, text="¿Es tu problema uno de los escenarios predeterminados?", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Seleccionar de la lista", command=self.elegir_problema).pack(pady=5)
        tk.Button(self.root, text="Describir nuevo problema", command=self.nuevo_problema).pack(pady=5)

    def elegir_problema(self):
        # Ventana para seleccionar un problema de la lista
        self.limpiar_ventana()
        problemas = self.cargar_escenarios().get(self.tipo_conflicto.get(), [])

        if problemas:
            tk.Label(self.root, text="Selecciona un problema:", font=("Arial", 16)).pack(pady=10)
            
            self.problema_var = tk.StringVar(value=problemas)
            listbox = tk.Listbox(self.root, listvariable=self.problema_var, height=10, selectmode="single")
            listbox.pack(pady=10)

            tk.Button(self.root, text="Continuar", command=lambda: self.obtener_problema_seleccionado(listbox)).pack(pady=20)
        else:
            messagebox.showinfo("Información", "No hay problemas predeterminados para este tipo de conflicto.")
            self.seleccionar_tipo_conflicto()

    def obtener_problema_seleccionado(self, listbox):
        try:
            self.problema = listbox.get(listbox.curselection())
            self.elegir_metodo_resolucion()
        except tk.TclError:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un problema de la lista.")

        def nuevo_problema(self):
            # Ingresar un nuevo problema
            self.limpiar_ventana()
            self.problema = simpledialog.askstring("Nuevo Problema", "Describe tu problema:")
            
            if self.problema:
                self.elegir_metodo_resolucion()
            else:
                messagebox.showwarning("Advertencia", "No se describió ningún problema.")

    def elegir_metodo_resolucion(self):
        # Ventana para seleccionar el método de resolución
        self.limpiar_ventana()
        tk.Label(self.root, text="Elige un método de resolución:", font=("Arial", 16)).pack(pady=10)

        self.metodo = tk.StringVar()
        tk.Radiobutton(self.root, text="Negociación", variable=self.metodo, value="negociación").pack(anchor="w")
        tk.Radiobutton(self.root, text="Mediación", variable=self.metodo, value="mediación").pack(anchor="w")
        tk.Radiobutton(self.root, text="Solución directa", variable=self.metodo, value="directa").pack(anchor="w")
        
        tk.Button(self.root, text="Sugerir nuevo método", command=self.sugerir_nuevo_metodo).pack(pady=5)
        tk.Button(self.root, text="Continuar", command=self.evaluar_resolucion).pack(pady=20)

    def sugerir_nuevo_metodo(self):
        nuevo_metodo = simpledialog.askstring("Nuevo Método", "Describe tu método de resolución:")
        if nuevo_metodo:
            self.metodo.set(nuevo_metodo)
        else:
            messagebox.showwarning("Advertencia", "No se describió ningún método.")

    def evaluar_resolucion(self):
        # Ventana para evaluar la resolución
        self.limpiar_ventana()
        resolucion = f"Has elegido {self.metodo.get()} para resolver el problema."
        exito = messagebox.askyesno("Evaluación", f"{resolucion}\n¿Te ayudó esta resolución?")
        
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.registrar_decision(self.tipo_conflicto.get(), self.problema, self.metodo.get(), exito, fecha)
        self.mostrar_resultado(exito)

    def mostrar_resultado(self, exito):
        # Mostrar el resultado final y dar opción de continuar
        self.limpiar_ventana()
        mensaje = "¡Gracias por tu retroalimentación!" if exito else "Lo sentimos, intentemos otro método."
        tk.Label(self.root, text=mensaje, font=("Arial", 16)).pack(pady=20)
        
        tk.Button(self.root, text="Reiniciar", command=self.seleccionar_tipo_conflicto).pack(pady=10)
        tk.Button(self.root, text="Salir", command=self.root.quit).pack(pady=10)

    def registrar_decision(self, tipo_conflicto, problema, metodo, exito, fecha):
        # Guardar la decisión en un archivo JSON
        try:
            with open('retroalimentacion_usuario.json', 'r') as f:
                datos = json.load(f)
        except FileNotFoundError:
            datos = {}
        
        if tipo_conflicto not in datos:
            datos[tipo_conflicto] = {}
        if problema not in datos[tipo_conflicto]:
            datos[tipo_conflicto][problema] = {'metodo': metodo, 'exito': 0, 'total': 0, 'fechas': []}

        datos[tipo_conflicto][problema]['total'] += 1
        if exito:
            datos[tipo_conflicto][problema]['exito'] += 1
        datos[tipo_conflicto][problema]['fechas'].append(fecha)
        
        with open('retroalimentacion_usuario.json', 'w') as f:
            json.dump(datos, f, indent=4)

    def cargar_escenarios(self):
        # Cargar escenarios de un archivo JSON
        try:
            with open('escenarios_conflictos.json', 'r') as f:
                escenarios = json.load(f)
            return escenarios
        except FileNotFoundError:
            return {"interpersonal": [], "pareja": []}

    def limpiar_ventana(self):
        # Limpiar la ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConflictResolutionApp(root)
    root.mainloop()
