# problema:congestion o demora al pagar en lugares(mercados,restaurantes,centros comerciales)
# lenguaje:python
# planificacion:Agilizar o facilitar el proceso de pago en locaels que circulan muchos clientes.
#como doncicional no puede tener saldo negativo o menor a 0,para comprobar el gap
#matrices utlilice para los dias de la semana 
#como metodo de ordenamiento utilice comb sort.

import json
import os
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar  # Importar el calendario

# Función para cargar los datos desde un archivo JSON
def cargar_datos(archivo):
    if os.path.exists(archivo):
        with open(archivo, 'r') as f:
            return json.load(f)
    else:
        return {}

# Función para guardar los datos en un archivo JSON
def guardar_datos(archivo, datos):
    with open(archivo, 'w') as f:
        json.dump(datos, f, indent=4)

# Función para agregar un gasto
def agregar_gasto():
    dia = dia_entry.get()
    mes = mes_entry.get()
    año = año_entry.get()
    
    try:
        gasto = float(gasto_entry.get())
        if dia and mes and año:
            # Crear la fecha completa en formato año-mes-día
            fecha = f"{año}-{mes}-{dia}"
            if fecha not in datos:
                datos[fecha] = gasto
            else:
                messagebox.showwarning("Gasto Existente", f"Ya existe un gasto registrado para {fecha}.")
            guardar_datos(archivo, datos)
            messagebox.showinfo("Éxito", f"Gasto de {gasto} pesos agregado en {fecha}.")
            actualizar_lista()
            # Limpiar los campos después de agregar el gasto
            dia_entry.delete(0, tk.END)
            mes_entry.delete(0, tk.END)
            año_entry.delete(0, tk.END)
            gasto_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Entrada inválida", "Debe ingresar día, mes y año.")
    except ValueError:
        messagebox.showwarning("Entrada inválida", "El gasto debe ser un número.")

# Función para eliminar un gasto desde el listado
def eliminar_gasto_desde_lista():
    seleccion = lista_gastos.curselection()  # Obtener el índice seleccionado en la lista
    if seleccion:
        item_seleccionado = lista_gastos.get(seleccion[0])
        # Extraer fecha y gasto del ítem seleccionado
        fecha, gasto = item_seleccionado.split(": ")
        # Eliminar el gasto correspondiente
        if fecha in datos:
            del datos[fecha]
            guardar_datos(archivo, datos)
            messagebox.showinfo("Éxito", f"Gasto de {gasto} pesos eliminado en {fecha}.")
            actualizar_lista()
        else:
            messagebox.showwarning("Error", "No se pudo eliminar el gasto seleccionado.")
    else:
        messagebox.showwarning("Selección inválida", "Debe seleccionar un gasto de la lista.")

# Función para mostrar los totales de los gastos
def mostrar_totales():
    total_text.delete(1.0, tk.END)  # Limpiar el área de texto
    for fecha, gasto in datos.items():
        total_text.insert(tk.END, f"{fecha}: {gasto} pesos\n")

# Función para actualizar la lista de gastos
def actualizar_lista():
    lista_gastos.delete(0, tk.END)  # Limpiar la lista
    for fecha, gasto in datos.items():
        lista_gastos.insert(tk.END, f"{fecha}: {gasto} pesos")

# Función para buscar un gasto filtrando por fecha
def buscar_gasto():
    dia = dia_busqueda_entry.get()
    mes = mes_busqueda_entry.get()
    año = año_busqueda_entry.get()
    
    # Filtrar por día, mes y año
    resultado = []
    for fecha, gasto in datos.items():
        año_f, mes_f, dia_f = fecha.split('-')
        if (año == '' or año == año_f) and (mes == '' or mes == mes_f) and (dia == '' or dia == dia_f):
            resultado.append(f"{fecha}: {gasto} pesos")

    if resultado:
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, "\n".join(resultado))
    else:
        messagebox.showinfo("Sin resultados", "No se encontraron gastos con los filtros seleccionados.")

# Función para encontrar el mes con mayor gasto
def mes_con_mayor_gasto():
    mes_max = ""
    max_gasto = 0
    for fecha, gasto in datos.items():
        año, mes, _ = fecha.split('-')
        total_mes = sum(gasto for fecha, gasto in datos.items() if fecha.startswith(f"{año}-{mes}"))
        if total_mes > max_gasto:
            max_gasto = total_mes
            mes_max = mes
    messagebox.showinfo("Mes con mayor gasto", f"El mes con el mayor gasto es: {mes_max} con {max_gasto} pesos")

# Función para actualizar los campos con la fecha seleccionada del calendario
def seleccionar_fecha():
    fecha_seleccionada = calendario.get_date()  # Obtener la fecha seleccionada
    dia, mes, año = fecha_seleccionada.split("/")  # Dividir la fecha en día, mes y año
    dia_entry.delete(0, tk.END)
    dia_entry.insert(0, dia)
    mes_entry.delete(0, tk.END)
    mes_entry.insert(0, mes)
    año_entry.delete(0, tk.END)
    año_entry.insert(0, año)

# Interfaz gráfica con Tkinter
archivo = "gastos.json"
datos = cargar_datos(archivo)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Gastos")

# Etiquetas y campos de entrada para agregar un gasto
tk.Label(ventana, text="Día:").grid(row=0, column=0, padx=10, pady=5)
dia_entry = tk.Entry(ventana)
dia_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(ventana, text="Mes:").grid(row=1, column=0, padx=10, pady=5)
mes_entry = tk.Entry(ventana)
mes_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(ventana, text="Año:").grid(row=2, column=0, padx=10, pady=5)
año_entry = tk.Entry(ventana)
año_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(ventana, text="Gasto (Pesos):").grid(row=3, column=0, padx=10, pady=5)
gasto_entry = tk.Entry(ventana)
gasto_entry.grid(row=3, column=1, padx=10, pady=5)

# Calendario
tk.Label(ventana, text="Selecciona una fecha:").grid(row=4, column=0, columnspan=2, pady=5)
calendario = Calendar(ventana, selectmode="day", date_pattern="dd/mm/yyyy")
calendario.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Botón para actualizar los campos con la fecha seleccionada
tk.Button(ventana, text="Seleccionar Fecha", command=seleccionar_fecha).grid(row=6, column=0, columnspan=2, pady=5)

# Botones para agregar y mostrar totales
tk.Button(ventana, text="Agregar Gasto", command=agregar_gasto).grid(row=7, column=0, padx=10, pady=5)
tk.Button(ventana, text="Mostrar Totales", command=mostrar_totales).grid(row=8, column=0, padx=10, pady=5)
tk.Button(ventana, text="Buscar Gasto", command=buscar_gasto).grid(row=8, column=1, padx=10, pady=5)
tk.Button(ventana, text="Mes con Mayor Gasto", command=mes_con_mayor_gasto).grid(row=9, column=0, columnspan=2, pady=10)

# Campos de búsqueda
tk.Label(ventana, text="Buscar por Día:").grid(row=10, column=0, padx=10, pady=5)
dia_busqueda_entry = tk.Entry(ventana)
dia_busqueda_entry.grid(row=10, column=1, padx=10, pady=5)

tk.Label(ventana, text="Buscar por Mes:").grid(row=11, column=0, padx=10, pady=5)
mes_busqueda_entry = tk.Entry(ventana)
mes_busqueda_entry.grid(row=11, column=1, padx=10, pady=5)

tk.Label(ventana, text="Buscar por Año:").grid(row=12, column=0, padx=10, pady=5)
año_busqueda_entry = tk.Entry(ventana)
año_busqueda_entry.grid(row=12, column=1, padx=10, pady=5)

# Listbox para mostrar los gastos registrados
tk.Label(ventana, text="Lista de Gastos Registrados:").grid(row=13, column=0, columnspan=2, pady=5)
lista_gastos = tk.Listbox(ventana, height=10, width=40)
lista_gastos.grid(row=14, column=0, columnspan=2, padx=10, pady=5)

# Botón para eliminar un gasto seleccionado de la lista
tk.Button(ventana, text="Eliminar Gasto Seleccionado", command=eliminar_gasto_desde_lista).grid(row=15, column=0, columnspan=2, pady=10)

# Área de texto para mostrar los resultados de búsqueda
tk.Label(ventana, text="Resultados de la Búsqueda:").grid(row=16, column=0, columnspan=2, pady=5)
resultado_text = tk.Text(ventana, height=10, width=40)
resultado_text.grid(row=17, column=0, columnspan=2, padx=10, pady=5)

# Actualizar la lista de gastos cuando la ventana se abre
actualizar_lista()

# Ejecutar la interfaz gráfica
ventana.mainloop()
