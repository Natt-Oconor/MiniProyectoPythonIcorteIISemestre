"""
Interfaz GRAFICA - Widgets reutilizables (tkinter).

Funciones sueltas que arman los controles que se repiten en la ventana:
estilos, botones, campos de entrada, tablas y areas de texto.

El `import tkinter` va dentro de un try para que este modulo se pueda
importar aunque el sistema no tenga tkinter (por ejemplo, en Linux con
instalaciones minimas). En ese caso las funciones avisan el error.
"""

try:
    import tkinter as tk
    from tkinter import ttk
    TKINTER_DISPONIBLE = True
except ImportError:
    TKINTER_DISPONIBLE = False
    tk = None
    ttk = None

FUENTE_TITULO = ("Segoe UI", 17, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 10)
FUENTE_ROTULO = ("Segoe UI", 9, "bold")
FUENTE_TEXTO = ("Consolas", 9)

COLOR_FONDO = "#f4f6f8"
COLOR_PANEL = "#ffffff"
COLOR_ACENTO = "#1f6fb2"
COLOR_TABLA_ALT = "#eef3f8"
COLOR_TABLA_SEL = "#cfe4f7"
COLOR_URGENTE = "#d64545"


def exigir_tkinter():
    if not TKINTER_DISPONIBLE:
        raise RuntimeError(
            "tkinter no esta instalado. Instala Python marcando la opcion "
            "'tcl/tk and IDLE' o usa la version de consola: python main.py --consola")


# ---------------------------------------------------------------- estilos

def aplicar_estilos(raiz):
    """Configura el aspecto general de la aplicacion."""
    exigir_tkinter()
    estilo = ttk.Style()
    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass

    raiz.configure(background=COLOR_FONDO)
    estilo.configure(".", font=FUENTE_SUBTITULO, background=COLOR_FONDO)
    estilo.configure("Titulo.TLabel", font=FUENTE_TITULO,
                     foreground=COLOR_ACENTO, background=COLOR_FONDO)
    estilo.configure("Subtitulo.TLabel", font=FUENTE_SUBTITULO,
                     foreground="#444444", background=COLOR_FONDO)
    estilo.configure("Rotulo.TLabel", font=FUENTE_ROTULO,
                     foreground="#333333", background=COLOR_FONDO)
    estilo.configure("Estado.TLabel", font=("Segoe UI", 9),
                     foreground="#1a1a1a", background="#e2e8ee")
    estilo.configure("TLabel", background=COLOR_PANEL)
    estilo.configure("TLabelframe", background=COLOR_FONDO)
    estilo.configure("TLabelframe.Label", font=FUENTE_ROTULO,
                     foreground="#333333", background=COLOR_FONDO)
    estilo.configure("TButton", padding=(8, 5))
    estilo.configure("Primario.TButton", font=FUENTE_ROTULO)
    estilo.configure("Peligro.TButton", font=FUENTE_ROTULO,
                     foreground=COLOR_URGENTE)
    estilo.configure("TNotebook.Tab", padding=(16, 7), font=FUENTE_ROTULO)

    estilo.configure("Treeview", rowheight=24, font=("Segoe UI", 9),
                     background=COLOR_PANEL, fieldbackground=COLOR_PANEL)
    estilo.configure("Treeview.Heading", font=FUENTE_ROTULO,
                     background="#dde4ea", foreground="#1a1a1a",
                     relief="flat", padding=(4, 5))
    estilo.map("Treeview", background=[("selected", COLOR_TABLA_SEL)])
    return estilo


# ---------------------------------------------------------------- widgets

def crear_boton(parent, texto, comando, estilo=None, ancho=None):
    exigir_tkinter()
    opciones = {"text": texto, "command": comando}
    if estilo:
        opciones["style"] = estilo
    if ancho:
        opciones["width"] = ancho
    return ttk.Button(parent, **opciones)


def crear_campo(parent, etiqueta, variable, ancho=32, clave_mostrar="•"):
    """Crea una etiqueta + un campo de entrada enlazado a una variable.

    Devuelve el marco contenedor.
    """
    exigir_tkinter()
    marco = ttk.Frame(parent)
    marco.pack(fill="x", pady=4)
    ttk.Label(marco, text=etiqueta, width=13, anchor="w").pack(
        side="left", padx=(0, 6))
    entrada = ttk.Entry(marco, textvariable=variable, width=ancho)
    entrada.pack(side="left", fill="x", expand=True)
    return marco, entrada


def crear_selector(parent, etiqueta, variable, valores, ancho=16):
    """Crea una etiqueta + un combobox de solo lectura."""
    exigir_tkinter()
    marco = ttk.Frame(parent)
    marco.pack(fill="x", pady=4)
    ttk.Label(marco, text=etiqueta, width=13, anchor="w").pack(
        side="left", padx=(0, 6))
    combo = ttk.Combobox(marco, textvariable=variable, values=list(valores),
                         state="readonly", width=ancho)
    combo.pack(side="left", fill="x", expand=True)
    return marco, combo


def crear_tabla(parent, columnas, titulos, anchos):
    """Crea una Treeview con encabezados y barra de desplazamiento.

    columnas : lista de identificadores internos
    titulos  : lista de textos visibles
    anchos   : lista de anchos en pixeles
    Devuelve (marco, treeview).
    """
    exigir_tkinter()
    marco = ttk.Frame(parent)
    marco.columnconfigure(0, weight=1)
    marco.rowconfigure(0, weight=1)

    tree = ttk.Treeview(marco, columns=columnas, show="headings",
                        selectmode="browse")
    for indice, columna in enumerate(columnas):
        tree.heading(columna, text=titulos[indice])
        tree.column(columna, width=anchos[indice],
                    anchor="center" if columna in ("id", "prioridad", "estado")
                    else "w",
                    stretch=(columna not in ("id",)))

    barra = ttk.Scrollbar(marco, orient="vertical", command=tree.yview)
    horizontal = ttk.Scrollbar(marco, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=barra.set, xscrollcommand=horizontal.set)

    tree.grid(row=0, column=0, sticky="nsew")
    barra.grid(row=0, column=1, sticky="ns")
    horizontal.grid(row=1, column=0, sticky="ew")

    tree.tag_configure("par", background=COLOR_TABLA_ALT)
    tree.tag_configure("urgente", foreground=COLOR_URGENTE,
                       font=("Segoe UI", 9, "bold"))
    tree.tag_configure("turno", background="#ffe9a8",
                       font=("Segoe UI", 9, "bold"))
    return marco, tree


def crear_area_texto(parent, alto=6, fondo="#f7f7f7"):
    """Crea un area de texto de solo lectura con barra de desplazamiento.

    Devuelve (marco, widget_text).
    """
    exigir_tkinter()
    marco = ttk.Frame(parent)
    marco.columnconfigure(0, weight=1)
    marco.rowconfigure(0, weight=1)

    texto = tk.Text(marco, height=alto, wrap="word", state="disabled",
                    font=FUENTE_TEXTO, relief="flat", background=fondo,
                    highlightthickness=1, highlightbackground="#cccccc")
    barra = ttk.Scrollbar(marco, orient="vertical", command=texto.yview)
    texto.configure(yscrollcommand=barra.set)

    texto.grid(row=0, column=0, sticky="nsew")
    barra.grid(row=0, column=1, sticky="ns")
    return marco, texto


# ---------------------------------------------------------------- acciones

def escribir_log(widget, mensaje):
    """Agrega una linea con la hora al final de un area de texto."""
    from datetime import datetime
    hora = datetime.now().strftime("%H:%M:%S")
    widget.configure(state="normal")
    widget.insert("end", f"[{hora}] {mensaje}\n")
    widget.see("end")
    widget.configure(state="disabled")


def mostrar_texto(widget, lineas):
    """Reemplaza todo el contenido de un area de texto de solo lectura."""
    widget.configure(state="normal")
    widget.delete("1.0", "end")
    widget.insert("1.0", "\n".join(lineas))
    widget.configure(state="disabled")


def quitar_filas(tree):
    """Borra todas las filas de una tabla."""
    items = tree.get_children()
    if items:
        tree.delete(*items)


def id_seleccionado(tree):
    """Devuelve el ID de la fila seleccionada, o None."""
    seleccion = tree.selection()
    if not seleccion:
        return None
    return int(seleccion[0])
