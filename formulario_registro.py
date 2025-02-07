import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import re
from datetime import datetime

# Función para validar el formato del correo electrónico
def validar_correo(correo):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, correo)

# Función para guardar los datos
def guardar_datos():
    nombre = entry_nombre.get().strip()
    correo = entry_correo.get().strip()
    dia = variable_dia.get()
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    if not nombre or not correo or not dia:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        return

    if not validar_correo(correo):
        messagebox.showwarning("Advertencia", "Por favor, ingrese un correo electrónico válido.")
        return

    # Guardar datos en un archivo CSV
    with open("registro_congreso.csv", mode="a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([fecha_actual, nombre, correo, dia])

    # Limpiar los campos
    entry_nombre.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    variable_dia.set("")
    messagebox.showinfo("Éxito", "Registro guardado exitosamente.")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Formulario de Registro - Congreso SDF")
ventana.geometry("500x400")
ventana.resizable(False, False)

# Estilo para mejorar la apariencia
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TCombobox", font=("Arial", 12))

# Etiquetas y entradas
ttk.Label(ventana, text="Nombre completo:").grid(row=0, column=0, padx=10, pady=10, sticky="W")
entry_nombre = ttk.Entry(ventana, width=40)
entry_nombre.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(ventana, text="Correo electrónico:").grid(row=1, column=0, padx=10, pady=10, sticky="W")
entry_correo = ttk.Entry(ventana, width=40)
entry_correo.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(ventana, text="Seleccione el día:").grid(row=2, column=0, padx=10, pady=10, sticky="W")
variable_dia = tk.StringVar()
dias = ["Día 1", "Día 2", "Día 3"]
combo_dia = ttk.Combobox(ventana, textvariable=variable_dia, values=dias, state="readonly", width=37)
combo_dia.grid(row=2, column=1, padx=10, pady=10)

# Botón para guardar
btn_guardar = ttk.Button(ventana, text="Guardar Registro", command=guardar_datos)
btn_guardar.grid(row=3, column=0, columnspan=2, pady=20)

# Etiqueta de información
ttk.Label(ventana, text="Nota: Los datos se guardarán con la fecha actual.", foreground="gray").grid(row=4, column=0, columnspan=2, pady=10)

# Ejecutar la aplicación
ventana.mainloop()
