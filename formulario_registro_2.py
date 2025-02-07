import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import re
from datetime import datetime

# Configuración de la base de datos
def inicializar_bd():
    conexion = sqlite3.connect("registro_congreso.db")
    cursor = conexion.cursor()
    # Crear tabla si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL UNIQUE,
        dia TEXT NOT NULL
    )
    """)
    conexion.commit()
    conexion.close()

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

    try:
        conexion = sqlite3.connect("registro_congreso.db")
        cursor = conexion.cursor()
        # Insertar registro en la base de datos
        cursor.execute("""
        INSERT INTO registros (fecha, nombre, correo, dia)
        VALUES (?, ?, ?, ?)
        """, (fecha_actual, nombre, correo, dia))
        conexion.commit()
        conexion.close()

        # Limpiar los campos
        entry_nombre.delete(0, tk.END)
        entry_correo.delete(0, tk.END)
        variable_dia.set("")
        messagebox.showinfo("Éxito", "Registro guardado exitosamente.")

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El correo ya está registrado. Use otro correo.")

# Función para mostrar los registros
def mostrar_registros():
    ventana_registros = tk.Toplevel()
    ventana_registros.title("Registros Guardados")
    ventana_registros.geometry("600x400")
    ventana_registros.resizable(False, False)

    # Conectar a la base de datos y obtener los datos
    conexion = sqlite3.connect("registro_congreso.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT fecha, nombre, correo, dia FROM registros")
    registros = cursor.fetchall()
    conexion.close()

    # Crear un Treeview para mostrar los datos
    tree = ttk.Treeview(ventana_registros, columns=("Fecha", "Nombre", "Correo", "Día"), show="headings")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Correo", text="Correo")
    tree.heading("Día", text="Día")
    tree.pack(fill="both", expand=True)

    # Insertar los registros en el Treeview
    for registro in registros:
        tree.insert("", tk.END, values=registro)

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Formulario de Registro del VI-CI-SoDoFi-2025\n Sociedad Dominicana de Física 2025")
ventana.geometry("500x400")
ventana.resizable(False, False)

# Inicializar la base de datos
inicializar_bd()

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

# Botones
btn_guardar = ttk.Button(ventana, text="Guardar Registro", command=guardar_datos)
btn_guardar.grid(row=3, column=0, pady=20, padx=10)

btn_mostrar = ttk.Button(ventana, text="Mostrar Registros", command=mostrar_registros)
btn_mostrar.grid(row=3, column=1, pady=20, padx=10)

# Etiqueta de información
ttk.Label(ventana, text="Nota: Los datos se guardarán con la fecha actual.", foreground="gray").grid(row=4, column=0, columnspan=2, pady=10)

# Ejecutar la aplicación
ventana.mainloop()
