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

class GestionGastos:
    def _init_(self):
        # Variables principales
        self.archivo = "gastos.json"
        self.datos = self.cargar_datos()
        self.ventana = tk.Tk()
        self.ventana.title("Gestión de Gastos")

        # Construcción de la interfaz gráfica
        self.construir_interfaz()

        # Actualizar la lista al iniciar
        self.actualizar_lista()

        # Iniciar la ventana principal
        self.ventana.mainloop()

    # Función para cargar los datos desde un archivo JSON
    def cargar_datos(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r') as f:
                return json.load(f)
        else:
            return {}

    # Función para guardar los datos en un archivo JSON
    def guardar_datos(self):
        with open(self.archivo, 'w') as f:
            json.dump(self.datos, f, indent=4)

    # Función para agregar un gasto
    def agregar_gasto(self):
        dia = self.dia_entry.get()
        mes = self.mes_entry.get()
        año = self.año_entry.get()

        try:
            gasto = float(self.gasto_entry.get())
            if dia and mes and año:
                # Crear la fecha completa en formato año-mes-día
                fecha = f"{año}-{mes}-{dia}"
                if fecha not in self.datos:
                    self.datos[fecha] = gasto
                else:
                    messagebox.showwarning("Gasto Existente", f"Ya existe un gasto registrado para {fecha}.")
                self.guardar_datos()
                messagebox.showinfo("Éxito", f"Gasto de {gasto} pesos agregado en {fecha}.")
                self.actualizar_lista()
                # Limpiar los campos después de agregar el gasto
                self.dia_entry.delete(0, tk.END)
                self.mes_entry.delete(0, tk.END)
                self.año_entry.delete(0, tk.END)
                self.gasto_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Entrada inválida", "Debe ingresar día, mes y año.")
        except ValueError:
            messagebox.showwarning("Entrada inválida", "El gasto debe ser un número.")

    # Función para eliminar un gasto desde el listado
    def eliminar_gasto_desde_lista(self):
        seleccion = self.lista_gastos.curselection()  # Obtener el índice seleccionado en la lista
        if seleccion:
            item_seleccionado = self.lista_gastos.get(seleccion[0])
            # Extraer fecha y gasto del ítem seleccionado
            fecha, gasto = item_seleccionado.split(": ")
            # Eliminar el gasto correspondiente
            if fecha in self.datos:
                del self.datos[fecha]
                self.guardar_datos()
                messagebox.showinfo("Éxito", f"Gasto de {gasto} pesos eliminado en {fecha}.")
                self.actualizar_lista()
            else:
                messagebox.showwarning("Error", "No se pudo eliminar el gasto seleccionado.")
        else:
            messagebox.showwarning("Selección inválida", "Debe seleccionar un gasto de la lista.")

    # Función para mostrar los totales de los gastos
    def mostrar_totales(self):
        self.total_text.delete(1.0, tk.END)  # Limpiar el área de texto
        for fecha, gasto in self.datos.items():
            self.total_text.insert(tk.END, f"{fecha}: {gasto} pesos\n")

    # Función para actualizar la lista de gastos
    def actualizar_lista(self):
        self.lista_gastos.delete(0, tk.END)  # Limpiar la lista
        for fecha, gasto in self.datos.items():
            self.lista_gastos.insert(tk.END, f"{fecha}: {gasto} pesos")

    # Función para buscar un gasto filtrando por fecha
    def buscar_gasto(self):
        dia = self.dia_busqueda_entry.get()
        mes = self.mes_busqueda_entry.get()
        año = self.año_busqueda_entry.get()

        # Filtrar por día, mes y año
        resultado = []
        for fecha, gasto in self.datos.items():
            año_f, mes_f, dia_f = fecha.split('-')
            if (año == '' or año == año_f) and (mes == '' or mes == mes_f) and (dia == '' or dia == dia_f):
                resultado.append(f"{fecha}: {gasto} pesos")

        if resultado:
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(tk.END, "\n".join(resultado))
        else:
            messagebox.showinfo("Sin resultados", "No se encontraron gastos con los filtros seleccionados.")

    # Función para encontrar el mes con mayor gasto
    def mes_con_mayor_gasto(self):
        if not self.datos:
            messagebox.showinfo("Sin datos", "No hay gastos registrados.")
            return

        gastos_por_mes = {}
        for fecha, gasto in self.datos.items():
            año, mes, _ = fecha.split('-')
            clave_mes = f"{año}-{mes}"  # Clave para identificar un mes específico
            gastos_por_mes[clave_mes] = gastos_por_mes.get(clave_mes, 0) + gasto

        # Encontrar el mes con el mayor gasto
        mes_max = max(gastos_por_mes, key=gastos_por_mes.get)
        max_gasto = gastos_por_mes[mes_max]

        messagebox.showinfo("Mes con mayor gasto", f"El mes con el mayor gasto es: {mes_max} con {max_gasto} pesos")

    # Función para actualizar los campos con la fecha seleccionada del calendario
    def seleccionar_fecha(self):
        fecha_seleccionada = self.calendario.get_date()  # Obtener la fecha seleccionada
        dia, mes, año = fecha_seleccionada.split("/")  # Dividir la fecha en día, mes y año
        self.dia_entry.delete(0, tk.END)
        self.dia_entry.insert(0, dia)
        self.mes_entry.delete(0, tk.END)
        self.mes_entry.insert(0, mes)
        self.año_entry.delete(0, tk.END)
        self.año_entry.insert(0, año)

    def construir_interfaz(self):
        # Etiquetas y campos de entrada para agregar un gasto
        tk.Label(self.ventana, text="Día:").grid(row=0, column=0, padx=10, pady=5)
        self.dia_entry = tk.Entry(self.ventana)
        self.dia_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.ventana, text="Mes:").grid(row=1, column=0, padx=10, pady=5)
        self.mes_entry = tk.Entry(self.ventana)
        self.mes_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.ventana, text="Año:").grid(row=2, column=0, padx=10, pady=5)
        self.año_entry = tk.Entry(self.ventana)
        self.año_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.ventana, text="Gasto (Pesos):").grid(row=3, column=0, padx=10, pady=5)
        self.gasto_entry = tk.Entry(self.ventana)
        self.gasto_entry.grid(row=3, column=1, padx=10, pady=5)

        # Calendario
        tk.Label(self.ventana, text="Selecciona una fecha:").grid(row=4, column=0, columnspan=2, pady=5)
        self.calendario = Calendar(self.ventana, selectmode="day", date_pattern="dd/mm/yyyy")
        self.calendario.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.ventana, text="Seleccionar Fecha", command=self.seleccionar_fecha).grid(row=6, column=0, columnspan=2, pady=5)
        tk.Button(self.ventana, text="Agregar Gasto", command=self.agregar_gasto).grid(row=7, column=0, padx=10, pady=5)

        # Lista de gastos registrados
        tk.Label(self.ventana, text="Lista de Gastos Registrados:").grid(row=9, column=0, columnspan=2, pady=5)
        self.lista_gastos = tk.Listbox(self.ventana, height=10, width=40)
        self.lista_gastos.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.ventana, text="Eliminar Gasto Seleccionado", command=self.eliminar_gasto_desde_lista).grid(row=11, column=0, columnspan=2, pady=10)
        tk.Button(self.ventana, text="Mes con Mayor Gasto", command=self.mes_con_mayor_gasto).grid(row=12, column=0, columnspan=2, pady=10)

# Ejecutar la aplicación
GestionGastos()
