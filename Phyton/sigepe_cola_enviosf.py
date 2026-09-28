"""
SIGEPE - Sistema de Gestión de Envíos y Paquetería Empresarial
Módulo: Cola de solicitudes de envío pendientes de asignación (FIFO)

Necesidad: las solicitudes llegan (antes por WhatsApp) y deben atenderse en el
orden en que llegaron. La primera solicitud en entrar es la primera en ser
asignada a un repartidor. Estructura lineal elegida: COLA.
"""

from collections import deque


class Solicitud:
    def __init__(self, id_envio, cliente, direccion, descripcion):
        self.id_envio = id_envio
        self.cliente = cliente
        self.direccion = direccion
        self.descripcion = descripcion
        self.estado = "Pendiente"  # Pendiente -> En Ruta -> Entregado / Cancelado

    def __str__(self):
        return (f"[{self.id_envio}] {self.cliente} | {self.direccion} | "
                f"{self.descripcion} | Estado: {self.estado}")


class ColaEnvios:
    """Cola FIFO de solicitudes pendientes."""

    def __init__(self):
        self._items = deque()

    # --- Operaciones principales ---
    def encolar(self, solicitud):
        """Enqueue: agrega una solicitud al final de la cola."""
        self._items.append(solicitud)

    def desencolar(self):
        """Dequeue: saca la solicitud del frente (la más antigua)."""
        if self.esta_vacia():
            raise IndexError("No hay solicitudes pendientes")
        return self._items.popleft()

    def frente(self):
        """Peek: consulta la siguiente solicitud sin sacarla."""
        if self.esta_vacia():
            raise IndexError("No hay solicitudes pendientes")
        return self._items[0]

    def esta_vacia(self):
        return len(self._items) == 0

    def tamanio(self):
        return len(self._items)

    def cancelar(self, id_envio):
        """Quita de la cola una solicitud cancelada por el cliente."""
        for s in self._items:
            if s.id_envio == id_envio:
                s.estado = "Cancelado"
                self._items.remove(s)
                return True
        return False

    def listar(self):
        return list(self._items)


def asignar_siguiente(cola, repartidor):
    """Toma la solicitud más antigua y la asigna a un repartidor."""
    solicitud = cola.desencolar()
    solicitud.estado = "En Ruta"
    return solicitud, repartidor


# --- Pruebas de funcionamiento ---
def ejecutar_pruebas():
    cola = ColaEnvios()
    assert cola.esta_vacia()

    # Prueba 1: encolar y tamaño
    cola.encolar(Solicitud(1, "Ana Pérez", "Altamira", "Paquete pequeño"))
    cola.encolar(Solicitud(2, "Luis Mora", "Villa Fontana", "Documentos"))
    cola.encolar(Solicitud(3, "Rosa Gómez", "Bello Horizonte", "Comida"))
    assert cola.tamanio() == 3
    print("Prueba 1 OK: 3 solicitudes encoladas")

    # Prueba 2: orden FIFO
    assert cola.frente().id_envio == 1
    s, r = asignar_siguiente(cola, "Repartidor 1")
    assert s.id_envio == 1 and s.estado == "En Ruta"
    print("Prueba 2 OK: se asignó primero la solicitud 1 ->", s)

    # Prueba 3: cancelar una solicitud intermedia
    assert cola.cancelar(3) is True
    assert cola.tamanio() == 1 and cola.frente().id_envio == 2
    print("Prueba 3 OK: solicitud 3 cancelada, frente = 2")

    # Prueba 4: cola vacía
    cola.desencolar()
    assert cola.esta_vacia()
    try:
        cola.desencolar()
        raise AssertionError("Debió lanzar error")
    except IndexError:
        print("Prueba 4 OK: cola vacía controlada")

    print("\nTodas las pruebas pasaron correctamente.")


# --- Menú interactivo ---
def pedir_texto(mensaje):
    """Pide un texto y no permite dejarlo vacío."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  El campo no puede estar vacío. Intenta de nuevo.")


def pedir_entero(mensaje):
    """Pide un número entero válido."""
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            return int(valor)
        print("  Ingresa un número válido.")


def mostrar_menu():
    print("\n===== SIGEPE - Cola de solicitudes de envío =====")
    print("1. Registrar nueva solicitud")
    print("2. Ver siguiente solicitud (frente)")
    print("3. Asignar siguiente solicitud a un repartidor")
    print("4. Cancelar una solicitud")
    print("5. Listar solicitudes pendientes")
    print("6. Ejecutar pruebas automáticas")
    print("0. Salir")


def main():
    cola = ColaEnvios()
    siguiente_id = 1

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            cliente = pedir_texto("Nombre del cliente: ")
            direccion = pedir_texto("Dirección de entrega: ")
            descripcion = pedir_texto("Descripción del paquete: ")
            cola.encolar(Solicitud(siguiente_id, cliente, direccion, descripcion))
            print(f"  Solicitud #{siguiente_id} registrada. "
                  f"Pendientes: {cola.tamanio()}")
            siguiente_id += 1

        elif opcion == "2":
            if cola.esta_vacia():
                print("  No hay solicitudes pendientes.")
            else:
                print("  Siguiente en la cola:", cola.frente())

        elif opcion == "3":
            if cola.esta_vacia():
                print("  No hay solicitudes pendientes.")
            else:
                repartidor = pedir_texto("Nombre del repartidor: ")
                solicitud, _ = asignar_siguiente(cola, repartidor)
                print(f"  Asignada a {repartidor}: {solicitud}")

        elif opcion == "4":
            if cola.esta_vacia():
                print("  No hay solicitudes pendientes.")
            else:
                id_envio = pedir_entero("ID de la solicitud a cancelar: ")
                if cola.cancelar(id_envio):
                    print(f"  Solicitud #{id_envio} cancelada.")
                else:
                    print("  No se encontró esa solicitud en la cola.")

        elif opcion == "5":
            pendientes = cola.listar()
            if not pendientes:
                print("  No hay solicitudes pendientes.")
            else:
                print(f"  Pendientes ({len(pendientes)}), en orden de atención:")
                for posicion, s in enumerate(pendientes, start=1):
                    print(f"  {posicion}. {s}")

        elif opcion == "6":
            print()
            ejecutar_pruebas()

        elif opcion == "0":
            print("Hasta luego.")
            break

        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    main()
