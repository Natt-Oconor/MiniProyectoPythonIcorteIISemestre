"""
Interfaz GRAFICA - Pestana de una estructura lineal.

Hay una pestana por estructura (COLA, PILA, LISTA). Cada una muestra la
tabla de solicitudes y los botones propios de su comportamiento:

    COLA   -> Asignar la del frente
    PILA   -> Asignar la de la cima
    LISTA  -> Asignar por ID, mover al inicio, ordenar por prioridad

La pestana no decide nada de negocio: pide el dato y se lo pasa a la
ventana principal, que es quien llama a los procesos.
"""

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, simpledialog
    TKINTER_DISPONIBLE = True
except ImportError:
    TKINTER_DISPONIBLE = False
    tk = None
    ttk = None
    messagebox = None
    simpledialog = None

from procesos import consulta
from interfaz.grafica.widgets import (
    crear_boton,
    crear_campo,
    crear_tabla,
    quitar_filas,
)

COLUMNAS = ("id", "cliente", "direccion", "descripcion", "prioridad", "estado")
TITULOS = ("ID", "Cliente", "Direccion", "Descripcion", "Prioridad", "Estado")
ANCHOS = (50, 160, 180, 200, 90, 110)

TEXTOS_BOTON = {
    "COLA": "Asignar la del frente (FIFO)",
    "PILA": "Asignar la de la cima (LIFO)",
    "LISTA": "Asignar por ID",
}


if TKINTER_DISPONIBLE:

    class PestanaEstructura(ttk.Frame):
        """Tabla de una estructura lineal y sus acciones."""

        def __init__(self, padre, nombre, estructura, on_asignar, on_cancelar,
                     on_entregar, on_recargar, on_log, **kwargs):
            super().__init__(padre, padding=10, **kwargs)
            self.nombre = nombre
            self.estructura = estructura
            self._on_asignar = on_asignar
            self._on_cancelar = on_cancelar
            self._on_entregar = on_entregar
            self._on_recargar = on_recargar
            self._on_log = on_log

            self.var_repartidor = tk.StringVar(value="Repartidor 1")
            self.var_resumen = tk.StringVar(value="")
            self.var_ayuda = tk.StringVar(value="")

            self._construir()

        # ---------- Construccion ----------

        def _construir(self):
            marco = ttk.Frame(self)
            marco.pack(fill="x", pady=(0, 8))
            ttk.Label(marco, textvariable=self.var_ayuda,
                      style="Rotulo.TLabel").pack(side="left")
            ttk.Label(marco, textvariable=self.var_resumen).pack(side="right")

            self.marco_tabla, self.tabla = crear_tabla(
                self, COLUMNAS, TITULOS, ANCHOS)
            self.marco_tabla.pack(fill="both", expand=True)

            acciones = ttk.LabelFrame(
                self, text=f"Acciones de la {self.nombre}", padding=10)
            acciones.pack(fill="x", pady=(10, 0))

            fila = ttk.Frame(acciones)
            fila.pack(fill="x", pady=(0, 8))
            crear_campo(fila, "Repartidor:", self.var_repartidor, ancho=24)

            botones = ttk.Frame(acciones)
            botones.pack(fill="x")

            crear_boton(botones, TEXTOS_BOTON.get(self.nombre, "Asignar"),
                        self.asignar,
                        estilo="Primario.TButton").pack(side="left", padx=(0, 6))
            crear_boton(botones, "Cancelar seleccionada", self.cancelar,
                        estilo="Peligro.TButton").pack(side="left", padx=(0, 6))
            crear_boton(botones, "Marcar entregado",
                        self.marcar_entregado).pack(side="left", padx=(0, 6))
            crear_boton(botones, "Actualizar",
                        self.actualizar).pack(side="left")

            if self.nombre == "LISTA":
                extra = ttk.Frame(botones)
                extra.pack(side="left", padx=(16, 0))
                crear_boton(extra, "Subir al inicio",
                            self.mover_al_inicio).pack(side="left", padx=(0, 6))
                crear_boton(extra, "Ordenar por prioridad",
                            self.ordenar_prioridad).pack(side="left")

        # ---------- Presentacion ----------

        def refrescar(self, estructura=None):
            """Vuelve a dibujar la tabla con el contenido actual."""
            if estructura is not None:
                self.estructura = estructura
            quitar_filas(self.tabla)

            for solicitud in self.estructura.listar():
                etiquetas = []
                if solicitud.prioridad == "Urgente":
                    etiquetas.append("urgente")
                elif solicitud.id_envio % 2 == 0:
                    etiquetas.append("par")
                self.tabla.insert("", "end", iid=str(solicitud.id_envio),
                                  values=solicitud.a_lista(),
                                  tags=tuple(etiquetas))

            siguiente = consulta.proxima(self.estructura)
            total = self.estructura.tamanio()
            detalle = ""
            if siguiente is not None:
                detalle = (f"   |   sale primero: #{siguiente.id_envio} "
                           f"{siguiente.cliente}")
            self.var_resumen.set(f"{total} solicitud(es) en espera{detalle}")
            self.var_ayuda.set(consulta.criterio_estructura(self.estructura))
            self._resaltar_turno(siguiente)

        def _resaltar_turno(self, siguiente):
            """Resalta la fila que sale primero segun el tipo de estructura."""
            id_turno = str(siguiente.id_envio) if siguiente is not None else None
            for item in self.tabla.get_children():
                etiquetas = list(self.tabla.item(item, "tags"))
                if "turno" in etiquetas and item != id_turno:
                    etiquetas.remove("turno")
                if item == id_turno and "turno" not in etiquetas:
                    etiquetas.append("turno")
                self.tabla.item(item, tags=tuple(etiquetas))

        # ---------- Lectura de la tabla ----------

        def id_seleccionado(self):
            """ID de la fila marcada, o None si no hay ninguna."""
            seleccion = self.tabla.selection()
            if not seleccion:
                return None
            return int(seleccion[0])

        def seleccionada(self, avisar=True):
            """Solicitud marcada en la tabla, o None."""
            id_envio = self.id_seleccionado()
            if id_envio is None:
                if avisar:
                    messagebox.showinfo(
                        "Selecciona una fila",
                        "Primero marca una fila de la tabla.",
                        parent=self)
                return None
            solicitud = self.estructura.buscar(id_envio)
            if solicitud is None and avisar:
                messagebox.showwarning(
                    "No encontrada",
                    f"La solicitud #{id_envio} ya no esta en la "
                    f"{self.nombre}.", parent=self)
            return solicitud

        def pedir_id(self):
            """Pide un ID por teclado. Se usa en la LISTA."""
            valor = simpledialog.askstring(
                "Asignar por ID", "ID de la solicitud a asignar:",
                parent=self, minvalue=1)
            if valor is None:
                return None
            try:
                return int(valor.strip())
            except (ValueError, AttributeError):
                messagebox.showerror(
                    "ID invalido", f"'{valor}' no es un numero valido.",
                    parent=self)
                return None

        # ---------- Acciones ----------

        def asignar(self):
            repartidor = self.var_repartidor.get().strip() or "Repartidor 1"
            if self.nombre == "LISTA":
                id_envio = self.pedir_id()
                if id_envio is None:
                    return
                self._on_asignar(self.nombre, repartidor, id_envio)
            else:
                self._on_asignar(self.nombre, repartidor, None)

        def cancelar(self):
            solicitud = self.seleccionada()
            if solicitud is None:
                return
            respuesta = messagebox.askyesno(
                "Cancelar solicitud",
                f"¿Cancelar la solicitud #{solicitud.id_envio} de "
                f"{solicitud.cliente}?\n\nQuedara fuera de la {self.nombre}.",
                parent=self)
            if respuesta:
                self._on_cancelar(self.nombre, solicitud.id_envio)

        def marcar_entregado(self):
            solicitud = self.seleccionada()
            if solicitud is None:
                return
            self._on_entregar(self.nombre, solicitud.id_envio)

        def mover_al_inicio(self):
            solicitud = self.seleccionada()
            if solicitud is None:
                return
            if self.estructura.mover_a_inicio(solicitud.id_envio):
                self._on_log(f"#{solicitud.id_envio} movido al inicio de la "
                             f"{self.nombre}.")
            else:
                messagebox.showinfo(
                    "Sin cambio",
                    "Esa solicitud ya ocupa la posicion 1.", parent=self)
            self._on_recargar()

        def ordenar_prioridad(self):
            self.estructura.ordenar_por_prioridad()
            self._on_log(f"{self.nombre} ordenada por prioridad, de mayor a menor.")
            self._on_recargar()

        def actualizar(self):
            self.refrescar()
            self._on_log(f"Tabla de la {self.nombre} actualizada.")

else:
    PestanaEstructura = None
