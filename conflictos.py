import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ConflictResolutionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramienta de Resolución de Conflictos")

        self.tipo_conflicto = tk.StringVar(value="")
        self.metodos_resolucion = self.cargar_metodos_resolucion()
        self.seleccionar_tipo_conflicto()

    def seleccionar_tipo_conflicto(self):
        self.tipo_conflicto.set("")  # Reiniciar el valor de tipo_conflicto
        self.limpiar_ventana()
        self.root.update_idletasks()

        tk.Label(self.root, text="Selecciona el tipo de conflicto:", font=("Arial", 16)).pack(pady=10)

        # Creación de los Radiobuttons
        tk.Radiobutton(self.root, text="Interpersonal", variable=self.tipo_conflicto, value="interpersonal").pack(anchor="w")
        tk.Radiobutton(self.root, text="De pareja", variable=self.tipo_conflicto, value="pareja").pack(anchor="w")

        tk.Button(self.root, text="Continuar", command=self.seleccionar_problema).pack(pady=20)

    def seleccionar_problema(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="¿Es tu problema uno de los escenarios predeterminados?", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Seleccionar de la lista", command=self.elegir_problema).pack(pady=5)
        tk.Button(self.root, text="Describir nuevo problema", command=self.nuevo_problema).pack(pady=5)

    def elegir_problema(self):
        self.limpiar_ventana()
        problemas = self.cargar_escenarios().get(self.tipo_conflicto.get(), [])

        if problemas:
            tk.Label(self.root, text="Selecciona un problema:", font=("Arial", 16)).pack(pady=10)

            frame_listbox = tk.Frame(self.root)
            frame_listbox.pack(fill=tk.BOTH, expand=True)

            self.problema_var = tk.StringVar(value=problemas)
            listbox = tk.Listbox(frame_listbox, listvariable=self.problema_var, height=10, selectmode="single")
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(frame_listbox, orient="vertical", command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.config(yscrollcommand=scrollbar.set)

            tk.Button(self.root, text="Continuar", command=lambda: self.obtener_problema_seleccionado(listbox)).pack(pady=20)

            self.root.update_idletasks()
            self.root.geometry(f"{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")
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
        self.limpiar_ventana()
        self.problema = simpledialog.askstring("Nuevo Problema", "Describe tu problema:")

        if self.problema:
            self.guardar_nuevo_problema(self.tipo_conflicto.get(), self.problema)
            self.elegir_metodo_resolucion()
        else:
            messagebox.showwarning("Advertencia", "No se describió ningún problema.")

    def guardar_nuevo_problema(self, tipo_conflicto, problema):
        escenarios = self.cargar_escenarios()
        if problema not in escenarios.get(tipo_conflicto, []):
            escenarios.setdefault(tipo_conflicto, []).append(problema)
            with open('escenarios.json', 'w', encoding='utf-8') as f:
                json.dump(escenarios, f, indent=4)

    def cargar_metodos_resolucion(self):
        try:
            with open('metodos_resolucion.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return ["Negociación", "Mediación", "Solución directa"]

    def guardar_metodos_resolucion(self):
        with open('metodos_resolucion.json', 'w', encoding='utf-8') as f:
            json.dump(self.metodos_resolucion, f, indent=4)

    def elegir_metodo_resolucion(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Elige uno o más métodos de resolución:", font=("Arial", 16)).pack(pady=10)

        frame_listbox = tk.Frame(self.root)
        frame_listbox.pack(fill=tk.BOTH, expand=True)

        self.metodo_var = tk.StringVar(value=self.metodos_resolucion)
        listbox = tk.Listbox(frame_listbox, listvariable=self.metodo_var, height=10, selectmode="multiple")
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame_listbox, orient="vertical", command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)

        tk.Button(self.root, text="Sugerir nuevo método", command=lambda: self.sugerir_nuevo_metodo(listbox)).pack(pady=5)
        tk.Button(self.root, text="Continuar", command=lambda: self.obtener_metodos_seleccionados(listbox)).pack(pady=20)

        self.root.update_idletasks()
        self.root.geometry(f"{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")

    def sugerir_nuevo_metodo(self, listbox):
        nuevo_metodo = simpledialog.askstring("Nuevo Método", "Describe tu método de resolución:")
        if nuevo_metodo and nuevo_metodo not in self.metodos_resolucion:
            self.metodos_resolucion.append(nuevo_metodo)
            self.guardar_metodos_resolucion()
            listbox.insert(tk.END, nuevo_metodo)
        elif not nuevo_metodo:
            messagebox.showwarning("Advertencia", "No se describió ningún método.")
        else:
            messagebox.showwarning("Advertencia", "Este método ya existe en la lista.")

    def obtener_metodos_seleccionados(self, listbox):
        selected_indices = listbox.curselection()
        self.metodos_seleccionados = [listbox.get(i) for i in selected_indices]

        if not self.metodos_seleccionados:
            messagebox.showwarning("Advertencia", "Por favor, selecciona al menos un método.")
        else:
            self.evaluar_resolucion()

    def evaluar_resolucion(self):
        self.limpiar_ventana()
        resolucion = f"Has elegido {', '.join(self.metodos_seleccionados)} para resolver el problema."
        exito = messagebox.askyesno("Evaluación", f"{resolucion}\n¿Te ayudó esta resolución?")

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.registrar_decision(self.tipo_conflicto.get(), self.problema, self.metodos_seleccionados, exito, fecha)
        self.mostrar_resultado(exito)

    def registrar_decision(self, tipo_conflicto, problema, metodos, exito, fecha):
        try:
            with open('retroalimentacion_usuario.json', 'r') as f:
                datos = json.load(f)
        except FileNotFoundError:
            datos = {}

        # Verificar e inicializar la estructura del diccionario si no existe
        if tipo_conflicto not in datos:
            datos[tipo_conflicto] = {}
        if problema not in datos[tipo_conflicto]:
            datos[tipo_conflicto][problema] = {'metodos': {}, 'exito': 0, 'total': 0, 'fechas': []}

        # Asegurarse de que la clave 'metodos' esté inicializada
        if 'metodos' not in datos[tipo_conflicto][problema]:
            datos[tipo_conflicto][problema]['metodos'] = {}

        # Registrar los métodos utilizados
        for metodo in metodos:
            if metodo not in datos[tipo_conflicto][problema]['metodos']:
                datos[tipo_conflicto][problema]['metodos'][metodo] = 0
            datos[tipo_conflicto][problema]['metodos'][metodo] += 1

        # Actualizar éxito y total
        datos[tipo_conflicto][problema]['exito'] += int(exito)
        datos[tipo_conflicto][problema]['total'] += 1
        datos[tipo_conflicto][problema]['fechas'].append({'fecha': fecha, 'exito': exito})

        with open('retroalimentacion_usuario.json', 'w') as f:
            json.dump(datos, f, indent=4)

    def mostrar_resultado(self, exito):
        resultado = "¡Qué bien!" if exito else "Lamentamos que no haya funcionado."
        tk.Label(self.root, text=resultado, font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Ver Gráficos", command=self.mostrar_ventana_graficos).pack(pady=10)
        tk.Button(self.root, text="Inicio", command=self.seleccionar_tipo_conflicto).pack(pady=10)

    def mostrar_ventana_graficos(self):
        ventana_graficos = tk.Toplevel(self.root)
        ventana_graficos.title("Gráficos")
        
        opciones_graficos = ["Total de éxitos y fracasos", "Distribución de métodos utilizados", "Evolución en el tiempo"]
        tk.Label(ventana_graficos, text="Selecciona un gráfico para mostrar:", font=("Arial", 14)).pack(pady=10)
        
        seleccion = tk.StringVar(value=opciones_graficos[0])
        tk.OptionMenu(ventana_graficos, seleccion, *opciones_graficos).pack(pady=10)
        
        tk.Button(ventana_graficos, text="Mostrar", command=lambda: self.mostrar_grafico(seleccion.get(), ventana_graficos)).pack(pady=10)

    def mostrar_grafico(self, opcion, ventana):
        with open('retroalimentacion_usuario.json', 'r') as f:
            datos = json.load(f)

        problema = self.problema
        tipo_conflicto = self.tipo_conflicto.get()

        if tipo_conflicto not in datos or problema not in datos[tipo_conflicto]:
            messagebox.showwarning("Advertencia", "No hay datos suficientes para mostrar este gráfico.")
            return

        data = datos[tipo_conflicto][problema]

        fig, ax = plt.subplots()

        if opcion == "Total de éxitos y fracasos":
            exito = data['exito']
            total = data['total']
            fracaso = total - exito

            ax.bar(['Éxitos', 'Fracasos'], [exito, fracaso])
            ax.set_title('Total de Éxitos y Fracasos')
            ax.set_ylabel('Cantidad')

        elif opcion == "Distribución de métodos utilizados":
            metodos = data['metodos']
            ax.bar(metodos.keys(), metodos.values())
            ax.set_title('Distribución de Métodos Utilizados')
            ax.set_ylabel('Frecuencia')

        elif opcion == "Evolución en el tiempo":
            fechas = [item['fecha'] for item in data['fechas']]
            exitos = [item['exito'] for item in data['fechas']]

            ax.plot(fechas, exitos, marker='o')
            ax.set_title('Evolución en el Tiempo')
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Éxito (1=Sí, 0=No)')
            ax.set_xticklabels(fechas, rotation=45, ha="right")

        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def cargar_escenarios(self):
        try:
            with open('escenarios.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConflictResolutionApp(root)
    root.mainloop()
