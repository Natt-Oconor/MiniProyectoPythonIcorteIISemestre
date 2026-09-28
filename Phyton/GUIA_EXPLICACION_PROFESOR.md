# GUÍA DEFINITIVA PARA EXPLICAR EL PROYECTO AL PROFESOR
## Proyecto: SIGEPE (Sistema de Gestión de Envíos y Paquetería Empresarial)

> **Nota para ti como alumno:**  
> Esta guía está pensada para que entiendas el código **de forma 100% clara, sin rodeos y sin enredos técnicos**. Léela con calma. Al final encontrarás un **guión paso a paso** de qué decir frente al profesor y un **banco de preguntas típicas** que te pueden hacer, con la respuesta exacta que debes dar.

---

## ÍNDICE RÁPIDO
1. [¿De qué trata el proyecto en 30 segundos?](#1-de-qué-trata-el-proyecto-en-30-segundos)
2. [Las 3 Estructuras Lineales explicadas con ejemplos de la vida real](#2-las-3-estructuras-lineales-explicadas-con-ejemplos-de-la-vida-real)
3. [¿Cómo está organizado el código? (Arquitectura en Capas)](#3-cómo-está-organizado-el-código-arquitectura-en-capas)
4. [El secreto maestro del código: Clase Base y Polimorfismo](#4-el-secreto-maestro-del-código-clase-base-y-polimorfismo)
5. [Análisis detallado de cada estructura en el código](#5-análisis-detallado-de-cada-estructura-en-el-código)
6. [Guión paso a paso para tu presentación en vivo](#6-guión-paso-a-paso-para-tu-presentación-en-vivo)
7. [Banco de preguntas del profesor (y cómo responderlas con seguridad)](#7-banco-de-preguntas-del-profesor-y-cómo-responderlas-con-seguridad)
8. [Chuleta de conceptos clave (Glosario)](#8-chuleta-de-conceptos-clave-glosario)

---

## 1. ¿De qué trata el proyecto en 30 segundos?

* **El problema de negocio:**  
  Una empresa de logística y encomiendas recibía paquetes y pedidos (por ejemplo por WhatsApp). Los pedidos llegaban desordenados y necesitaban un sistema para administrarlos y asignarlos a los repartidores de forma ordenada y justa.

* **La solución en software:**  
  Desarrollamos **SIGEPE**, un sistema en Python que permite gestionar estas solicitudes utilizando y comparando **las tres estructuras de datos lineales fundamentales de la informática**:
  1. **COLA (FIFO):** Para atender en orden de llegada (el primero que entra, es el primero en ser atendido).
  2. **PILA (LIFO):** Para cuando la última petición o evento es lo prioritario (como el historial de movimientos).
  3. **LISTA:** Para cuando necesitamos buscar por ID, cambiar de posición o reordenar por urgencia/prioridad.

* **Un extra de calidad:**  
  El proyecto cuenta con **interfaz gráfica (Tkinter)**, **interfaz por consola (terminal)** y **67 pruebas unitarias automáticas (`unittest`)** que garantizan que todo funciona al 100%.

---

## 2. Las 3 Estructuras Lineales explicadas con ejemplos de la vida real

Para que nunca se te olvide frente al profesor, imagínatelas así:

| Estructura | Sigla / Concepto | Ejemplo de la vida real | ¿Cómo se comporta en el proyecto? |
| :--- | :--- | :--- | :--- |
| **COLA** | **FIFO** (*First In, First Out* - Primero en entrar, primero en salir) | **La fila de un banco o supermercado**: La persona que llegó primero es atendida primero. Nadie se cuela. | Es la estructura principal de despacho. Las solicitudes se asignan a los repartidores en estricto orden de llegada. |
| **PILA** | **LIFO** (*Last In, First Out* - Último en entrar, primero en salir) | **Una pila de platos sucios** o **Ctrl+Z (Deshacer)**: El último plato que pusiste arriba es el primero que lavas. | Se usa en el **Historial de asignaciones**: cuando abres el historial, lo primero que quieres ver es lo que acaba de pasar hace un segundo, no lo de la mañana. |
| **LISTA** | **Acceso flexible** (Por índice o posición) | **Una lista de compras o una libreta de contactos**: Puedes leer el tercer elemento, tachar el del medio, o mover un producto al inicio porque es urgente. | Permite buscar solicitudes por su ID, subir un paquete urgente a la primera posición o reordenar toda la bandeja por nivel de prioridad. |

---

## 3. ¿Cómo está organizado el código? (Arquitectura en Capas)

Uno de los puntos más fuertes que el profesor va a evaluar es que **el código NO está metido en un solo archivo gigante y desordenado**. Está dividido profesionalmente en **capas independientes** (Principio de Responsabilidad Única):

```text
D:\Phyton\
│
├── main.py                    --> Punto de arranque (detecta argumentos y abre la app)
├── iniciar.bat                --> Acceso directo con doble clic
├── instalar.bat               --> Comprueba Python, librerías y pruebas
│
├── modelos/                   --> 1. LOS DATOS PUROS
│   ├── solicitud.py           --> Clase Solicitud (cliente, dirección, paquete, prioridad, estado)
│   └── repartidor.py          --> Clase Repartidor (nombre, total de entregas)
│
├── estructura_datos/          --> 2. LAS ESTRUCTURAS DE DATOS
│   ├── base.py                --> Clase base abstracta 'EstructuraLineal' (el molde común)
│   ├── colas/cola_envios.py   --> Clase ColaEnvios (FIFO con collections.deque)
│   ├── pilas/pila_envios.py   --> Clase PilaEnvios (LIFO con listas)
│   └── listas/lista_solicitudes.py --> Clase ListaSolicitudes (acceso por posición y ordenamiento)
│
├── procesos/                  --> 3. LA LÓGICA DEL NEGOCIO
│   ├── registro.py            --> Crea y valida solicitudes nuevas
│   ├── asignacion.py          --> Saca la solicitud y se la entrega al repartidor
│   ├── cancelacion.py         --> Da de baja una solicitud si el cliente cancela
│   └── consulta.py            --> Filtra por estado/prioridad y genera resúmenes
│
├── utilidades/                --> 4. HERRAMIENTAS DE APOYO
│   ├── validacion.py          --> Revisa que los textos no vengan vacíos ni raros
│   └── formato.py             --> Dibuja las tablas bonitas en pantalla y consola
│
├── interfaz/                  --> 5. LO QUE VE EL USUARIO
│   ├── grafica/               --> Ventana moderna con pestañas y botones (Tkinter)
│   └── consola/               --> Menú de texto por números para la terminal
│
└── pruebas/                   --> 6. CONTROL DE CALIDAD
    └── test_estructuras.py    --> 67 pruebas automáticas (todas pasando OK)
```

### ¿Por qué se hizo así? (Frase para decirle al profesor)
> *"Profesor, separamos la lógica de la interfaz. Si mañana la empresa decide cambiar la ventana de escritorio por una aplicación web o una app móvil, los archivos de modelos, estructuras y procesos no sufren ningún cambio. Son 100% reutilizables."*

---

## 4. El secreto maestro del código: Clase Base y Polimorfismo

Si el profesor te pregunta: **"¿Dónde aplicaste Programación Orientada a Objetos avanzada?"**, háblale de `estructura_datos/base.py`.

### La Clase `EstructuraLineal`
En `base.py` creamos una clase base abstracta llamada `EstructuraLineal`:
* Obliga a que la Cola, la Pila y la Lista tengan 3 métodos estándar:
  1. `agregar(solicitud)`: Meter un elemento.
  2. `quitar()`: Sacar el elemento que corresponde según la regla de la estructura.
  3. `siguiente()`: Mirar cuál es el próximo en salir sin sacarlo (*peek*).
* Además, les regala métodos ya resueltos a las tres: `esta_vacia()`, `tamanio()`, `buscar(id)`, `listar()`.

### ¿Por qué esto es genial? (Polimorfismo en acción)
En la carpeta `procesos/asignacion.py`, hay una función llamada `asignar_siguiente(estructura, repartidor)`:
```python
def asignar_siguiente(estructura, repartidor, historial=None):
    solicitud = estructura.quitar()  # <--- ¡ESTO ES POLIMORFISMO!
    ...
```
A esa función no le importa si le pasas una Cola, una Pila o una Lista. Ella solo llama a `.quitar()`.
* Si le pasas una **Cola**, `.quitar()` saca el frente (el más viejo).
* Si le pasas una **Pila**, `.quitar()` saca la cima (el más nuevo).
* Si le pasas una **Lista**, `.quitar()` saca el primer elemento.
**El mismo código sirve para las 3 estructuras sin cambiar ni una sola línea.**

---

## 5. Análisis detallado de cada estructura en el código

### A) La Cola (`estructura_datos/colas/cola_envios.py`)
* **Mecanismo:** FIFO (*First In, First Out*).
* **Cómo se programó:** Usa `collections.deque` de Python.
* **Pregunta de examen:** *¿Por qué usar `deque` y no una lista común `[]`?*  
  **Respuesta:** En una lista normal de Python, si quitas el primer elemento con `pop(0)`, Python tiene que mover todos los demás elementos hacia la izquierda uno por uno (costo $O(n)$). En cambio, `deque` es una cola doblemente enlazada optimizada en C que inserta al final (`append`) y saca del frente (`popleft`) en tiempo constante instantáneo ($O(1)$).
* **Métodos principales:**
  * `encolar(solicitud)`: Inserta al fondo ($O(1)$).
  * `desencolar()`: Saca del frente ($O(1)$).
  * `frente()`: Inspecciona el frente sin remover ($O(1)$).
  * `cancelar(id_envio)`: Busca el ID y reconstruye la cola sin él ($O(n)$).

### B) La Pila (`estructura_datos/pilas/pila_envios.py`)
* **Mecanismo:** LIFO (*Last In, First Out*).
* **Cómo se programó:** Usa una lista estándar de Python (`list`).
* **Pregunta de examen:** *¿Por qué aquí sí una lista estándar es perfecta?*  
  **Respuesta:** Porque en una lista de Python, agregar al final (`append`) y quitar del final (`pop`) toma tiempo constante $O(1)$. No hay que mover elementos.
* **Métodos principales:**
  * `apilar(solicitud)`: Coloca el paquete en la cima.
  * `desapilar()`: Saca el paquete que está en la cima.
  * `cima()`: Consulta el elemento superior.
* **Uso real en el sistema:**  
  La clase `HistorialAsignaciones` (en `procesos/asignacion.py`) es una pila. Cada vez que se asigna un paquete, se apila. Al consultar el historial, las asignaciones se muestran en orden inverso: la más reciente primero.

### C) La Lista (`estructura_datos/listas/lista_solicitudes.py`)
* **Mecanismo:** Estructura flexible con acceso por índice (posición).
* **¿Cuándo se usa?:** Cuando el orden de llegada no es suficiente y hay reglas de negocio especiales (paquetes urgentes o cancelaciones específicas).
* **Métodos principales:**
  * `agregar_al_inicio(solicitud)`: Coloca el envío en el índice 0 para despacharlo de inmediato.
  * `agregar_en_posicion(solicitud, pos)`: Inserta en cualquier casilla.
  * `mover_a_inicio(id)`: Mueve una solicitud urgente al primer puesto.
  * `ordenar_por_prioridad()`: Ordena la lista poniendo primero los pedidos de prioridad *Urgente*, luego *Alta*, *Normal* y *Baja*, respetando la antigüedad entre iguales.

---

## 6. Guión paso a paso para tu presentación en vivo

Sigue este guión cuando expongas ante el profesor:

### Minuto 0:00 a 1:00 — Introducción clara
> *"Buenos días profesor. Hoy voy a presentar **SIGEPE**, un sistema desarrollado en Python para gestionar las solicitudes de envío de una empresa de paquetería.*  
> *El objetivo principal del proyecto fue implementar y comparar de forma práctica las tres estructuras de datos lineales clásicas: **Cola (FIFO)**, **Pila (LIFO)** y **Lista**, aplicadas a situaciones reales de despacho de paquetería."*

### Minuto 1:00 a 2:00 — Explicación de la arquitectura
> *"El proyecto está estructurado con una arquitectura modular en capas:*
> 1. *En `modelos/` tenemos las entidades puras: Solicitud y Repartidor.*
> 2. *En `estructura_datos/` creamos una clase base abstracta `EstructuraLineal` de la cual heredan la Cola, la Pila y la Lista, aplicando **polimorfismo**.*
> 3. *En `procesos/` está la lógica del negocio: registrar, asignar y cancelar, que funciona igual con cualquiera de las estructuras.*
> 4. *Y en `interfaz/` tenemos dos modalidades: una interfaz gráfica con Tkinter y una de consola."*

### Minuto 2:00 a 3:30 — Demostración práctica
1. **Ejecutar el programa:** Abre la consola y escribe `python main.py` (o haz doble clic en `iniciar.bat`).
2. **Cargar ejemplos:** En el menú superior ve a `Archivo > Cargar ejemplo de 5 solicitudes` (esto cargará 5 pedidos automáticamente).
3. **Demostrar la COLA (FIFO):**
   * Señala la pestaña **COLA**. Muestra que la fila resaltada en amarillo es el pedido **#1 (Carlos Perez)** porque fue el primero en registrarse.
   * Haz clic en **"Asignar siguiente a repartidor"**. Verás cómo sale el #1 y ahora el siguiente en salir es el #2. Explica: *"Profesor, aquí vemos el principio FIFO en acción."*
4. **Demostrar la PILA (LIFO):**
   * Pasa a la pestaña **PILA**.
   * Muestra cómo la fila resaltada es la **#5 (Pedro Gomez)** porque fue la última en entrar.
   * Haz clic en **"Asignar siguiente a repartidor"**. Saldrá la #5. Explica: *"En la pila, el último en entrar es el primero en salir."*
5. **Demostrar la LISTA:**
   * Pasa a la pestaña **LISTA**.
   * Selecciona una solicitud que esté al final y haz clic en **"Subir al inicio"** o presiona **"Ordenar por prioridad"**.
   * Explica: *"En la lista podemos reordenar elementos o asignar directamente por ID sin respetar únicamente el orden de llegada."*
6. **Mostrar el HISTORIAL:**
   * Señala la parte inferior de la ventana donde dice *Historial de Asignaciones*.
   * Explica: *"El historial está implementado internamente como una **Pila**, por eso la asignación que acabamos de hacer aparece arriba del todo."*

### Minuto 3:30 a 4:00 — Pruebas unitarias y cierre
* Abre la terminal y ejecuta:
  ```bash
  python main.py --pruebas
  ```
* Muestra la salida:
  ```text
  Ran 67 tests in 0.002s
  OK
  ```
> *"Para garantizar la confiabilidad del código, implementamos 67 pruebas automáticas con `unittest`. Las 67 pruebas pasan con éxito, validando que la cola es estrictamente FIFO, la pila LIFO, y que las validaciones y cancelaciones funcionan sin errores.*  
> *Quedo a su disposición para cualquier pregunta."*

---

## 7. Banco de preguntas del profesor (y cómo responderlas con seguridad)

### P1: "¿Por qué usaste `collections.deque` en la Cola en lugar de una lista normal?"
* **Tu respuesta:**  
  *"Porque en una lista normal de Python, la operación de sacar el primer elemento con `pop(0)` tiene una complejidad computacional de $O(n)$, ya que Python tiene que recorrer y desplazar todos los índices de memoria a la izquierda. En cambio, `deque` es una cola doblemente enlazada que permite extraer del frente con `popleft()` en tiempo constante $O(1)$, haciéndola muchísimo más eficiente."*

---

### P2: "¿Dónde está aplicado el Polimorfismo en tu código?"
* **Tu respuesta:**  
  *"En la clase base `EstructuraLineal` (`base.py`) y en la función `asignar_siguiente()` (`procesos/asignacion.py`). Todas las estructuras implementan el método obligatorio `.quitar()`. Por lo tanto, el proceso de asignación no necesita saber con qué estructura está trabajando: solo llama a `estructura.quitar()` y cada estructura ejecuta su propia lógica (la cola saca el frente, la pila saca la cima, y la lista saca el primer índice)."*

---

### P3: "¿Por qué separaste los modelos de los procesos y de la interfaz?"
* **Tu respuesta:**  
  *"Para seguir el principio de **Separación de Responsabilidades**. `Solicitud` solo contiene datos y estados. Las estructuras solo gestionan cómo se almacenan esos datos. Los procesos contienen las reglas del negocio, y la interfaz solo interactúa con el usuario. Así, si queremos cambiar Tkinter por una interfaz web o consola, no tenemos que reescribir ni una sola línea de la lógica."*

---

### P4: "¿Qué pasa si intentas sacar un elemento de una cola o pila que está vacía?"
* **Tu respuesta:**  
  *"Creamos una excepción personalizada llamada `EstructuraVaciaError` en `base.py` (que hereda de `IndexError`). Cuando la estructura detecta que su tamaño es 0 (`self.esta_vacia()`), lanza esta excepción. Los procesos y la interfaz capturan este error y le muestran al usuario un mensaje amigable indicando que no hay solicitudes pendientes, en lugar de que el programa se rompa."*

---

### P5: "¿Qué complejidad tiene cancelar un elemento en medio de la cola?"
* **Tu respuesta:**  
  *"Tiene complejidad $O(n)$. Mientras que encolar y desencolar son $O(1)$, para cancelar hay que buscar el `id_envio` a lo largo de la cola y reconstruirla sin ese elemento. Por eso, si el sistema requiere búsquedas y cancelaciones continuas en cualquier posición, la estructura adecuada para ese caso es la **Lista**."*

---

### P6: "¿Los datos se guardan en un archivo o base de datos cuando cierro el programa?"
* **Tu respuesta:**  
  *"En esta versión, los datos residen en **memoria RAM** mientras el programa está abierto, lo cual es el estándar para estudiar y medir la eficiencia de estructuras de datos lineales en tiempo de ejecución. Sin embargo, gracias a la arquitectura modular, agregar persistencia con SQLite o archivos JSON requeriría únicamente añadir un módulo de almacenamiento en la capa de datos sin tocar la lógica."*

---

### P7: "¿Qué diferencia hay entre `__str__` y `__repr__` en tu clase `Solicitud`?"
* **Tu respuesta:**  
  *"`__str__` se usa para mostrar una representación legible y amigable para el usuario (por ejemplo: `[#1] Carlos Perez | Calle 10 | Urgente`), mientras que `__repr__` se usa para depuración técnica de los programadores (mostrando `Solicitud(id=1, cliente='Carlos Perez', estado='Pendiente')`)."*

---

### P8: "¿Por qué el archivo `requirements.txt` está vacío?"
* **Tu respuesta:**  
  *"Porque el proyecto fue diseñado con estricto apego a la **librería estándar de Python**. No requiere instalar paquetes externos con `pip`: utiliza `collections` para la cola, `tkinter` para la interfaz gráfica y `unittest` para las pruebas. Se puede ejecutar en cualquier máquina con Python 3.9+ inmediatamente."*

---

## 8. Chuleta de conceptos clave (Glosario)

* **FIFO (*First In, First Out*):** Primero en entrar, primero en salir (Cola).
* **LIFO (*Last In, First Out*):** Último en entrar, primero en salir (Pila).
* **$O(1)$ (Tiempo Constante):** La operación tarda siempre exactamente lo mismo, sin importar si hay 5 elementos o 5 millones (ej: `append` o `popleft`).
* **$O(n)$ (Tiempo Lineal):** El tiempo que tarda la operación crece de forma proporcional a la cantidad de elementos, porque tiene que recorrerlos uno a uno (ej: buscar un elemento en una lista desordenada).
* **Clase Abstracta / ABC:** Una clase que no se puede instanciar directamente, sino que sirve de plantilla obligatoria para que otras clases hijas implementen sus métodos.
* **Polimorfismo:** La capacidad de objetos de distintas clases de responder a un mismo mensaje o método (`quitar()`, `agregar()`) con comportamientos propios de cada una.
* **Prueba Unitaria (`unittest`):** Un script que prueba una pequeña parte de código (un método o función) de forma automática con datos simulados para verificar que arroje el resultado esperado.

---

¡Mucho éxito en tu presentación! Si sigues esta guía y muestras el sistema funcionando y las pruebas en verde, tu profesor verá un proyecto estructurado, profesional y con dominio total de los conceptos.
