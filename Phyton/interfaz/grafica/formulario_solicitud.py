"""
Interfaz GRAFICA - Formulario de registro de solicitudes.

Es la parte de la pantalla donde se ingresan los datos que pide el sistema:
cliente, direccion, descripcion del paquete y prioridad.

La validacion la hace utilidades/validacion.py, el mismo modulo que usa
la interfaz de consola, para que las dos entradas den el mismo resultado.
"""

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    TKINTER_DISPONIBLE = True
except ImportError:
    TKINTER_DISPONIBLE = False
    tk = None
    ttk = None
    messagebox = None

from modelos.solicitud import PRIORIDADES_VALIDAS
from utilidades.validacion import validar_solicitud
from interfaz.grafica.widgets import (
    crear_boton,
    crear_campo,
    crear_selector,
)


TEXTO_AYUDA = (
    "COLA (FIFO)\n"
    "  La primera solicitud registrada es la primera en salir.\n"
    "  Ideal cuando el orden de llegada define la prioridad.\n\n"
    "PILA (LIFO)\n"
    "  La ultima solicitud registrada es la primera en salir.\n"
    "  Ideal para el historial de movimientos o para una peticion\n"
    "  urgente que llega al final.\n\n"
    "LISTA\n"
    "  Permite buscar por ID, insertar en cualquier posicion y\n"
    "  ordenar por prioridad."
)


if TKINTER_DISPONIBLE:

    class FormularioSolicitud(ttk.Frame):
        """Panel de ingreso de datos de una solicitud de envio."""

        def __init__(self, padre, on_registrar, **kwargs):
            super().__init__(padre, padding=0, **kwargs)
            self._on_registrar = on_registrar
            self._entradas = []

            self.var_cliente = tk.StringVar()
            self.var_direccion = tk.StringVar()
            self.var_descripcion = tk.StringVar()
            self.var_prioridad = tk.StringVar(value=PRIORIDADES_VALIDAS[1])

            self._construir()

        def _construir(self):
            caja = ttk.LabelFrame(
                self, text="Datos de la solicitud", padding=12)
            caja.pack(fill="x", pady=(0, 10))

            cuerpo = ttk.Frame(caja)
            cuerpo.pack(fill="both", expand=True)

            for etiqueta, variable in (
                ("Cliente:", self.var_cliente),
                ("Direccion:", self.var_direccion),
                ("Descripcion:", self.var_descripcion),
            ):
                _, entrada = crear_campo(cuerpo, etiqueta, variable)
                self._entradas.append(entrada)

            crear_selector(cuerpo, "Prioridad:", self.var_prioridad,
                           PRIORIDADES_VALIDAS)

            ttk.Label(
                cuerpo,
                text=("La prioridad solo se usa para ordenar en la "
                      "estructura LISTA; en la COLA y la PILA manda "
                      "el orden de insercion."),
                wraplength=280, foreground="#666666").pack(
                    fill="x", pady=(6, 8))

            botones = ttk.Frame(cuerpo)
            botones.pack(fill="x")
            crear_boton(botones, "Registrar", self.registrar,
                        estilo="Primario.TButton").pack(side="left", padx=(0, 6))
            crear_boton(botones, "Limpiar", self.limpiar).pack(side="left")

            ayuda = ttk.LabelFrame(
                self, text="Criterio de seleccion de estructura", padding=12)
            ayuda.pack(fill="both", expand=True)
            ttk.Label(ayuda, text=TEXTO_AYUDA, wraplength=290,
                      justify="left").pack(anchor="w")

            for entrada in self._entradas:
                entrada.bind("<Return>", lambda _evento: self.registrar())

        # ---------- Acciones ----------

        def datos(self):
            """Datos actuales del formulario, sin normalizar todavia."""
            return (self.var_cliente.get(), self.var_direccion.get(),
                    self.var_descripcion.get(), self.var_prioridad.get())

        def registrar(self):
            """Valida y envia los datos al proceso de registro."""
            cliente, direccion, descripcion, prioridad = self.datos()
            datos, errores = validar_solicitud(
                cliente, direccion, descripcion, prioridad)

            if errores:
                messagebox.showerror("Revise los datos", "\n".join(errores))
                self.enfocar_campo_invalido()
                return False

            if not self._on_registrar(datos):
                return False
            return True

        def enfocar_campo_invalido(self):
            """Pone el cursor en el primer campo vacio."""
            variables = (self.var_cliente, self.var_direccion,
                         self.var_descripcion)
            for indice, variable in enumerate(variables):
                if not variable.get().strip() and indice < len(self._entradas):
                    entrada = self._entradas[indice]
                    entrada.focus_set()
                    entrada.selection_range(0, "end")
                    return

        def limpiar(self):
            self.var_cliente.set("")
            self.var_direccion.set("")
            self.var_descripcion.set("")
            self.var_prioridad.set(PRIORIDADES_VALIDAS[1])
            if self._entradas:
                self._entradas[0].focus_set()

else:
    FormularioSolicitud = None
