"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas
Empresa: Software FJ
Curso: Programación 213023 - Fase 4
Estudiante: Daniel Stiven Estrada Mora
Grupo: 155
Tutor: Gustavo Adolfo Marun

Características principales:
- Abstracción, herencia, polimorfismo y encapsulación
- Manejo avanzado de excepciones (personalizadas, try/except/else/finally, chaining)
- Sin bases de datos (listas en memoria + archivo de logs)
- Simulación de más de 10 operaciones válidas e inválidas
"""

from abc import ABC, abstractmethod
from datetime import datetime
import os

# ==================== EXCEPCIONES PERSONALIZADAS ====================
class ErrorSistema(Exception):
    """Excepción base del sistema."""
    pass

class ValidacionError(ErrorSistema):
    pass

class ClienteError(ValidacionError):
    pass

class ServicioError(ValidacionError):
    pass

class ReservaError(ValidacionError):
    pass


# ==================== CLASE ABSTRACTA ====================
class EntidadBase(ABC):
    """Clase abstracta que representa entidades generales del sistema."""

    @abstractmethod
    def validar_datos(self):
        pass

    @abstractmethod
    def obtener_info(self):
        pass


# ==================== CLASE CLIENTE ====================
class Cliente(EntidadBase):
    def __init__(self, nombre, identificacion, telefono="", correo=""):
        self._nombre = ""
        self._identificacion = ""
        self._telefono = ""
        self._correo = ""
        self.nombre = nombre
        self.identificacion = identificacion
        self.telefono = telefono
        self.correo = correo
        self.validar_datos()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(str(valor).strip()) < 3:
            raise ClienteError("El nombre debe tener mínimo 3 caracteres.")
        self._nombre = str(valor).strip().title()

    @property
    def identificacion(self):
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor):
        valor_str = str(valor).strip()
        if not valor_str.isdigit() or len(valor_str) < 6:
            raise ClienteError("La identificación debe ser numérica y de al menos 6 dígitos.")
        self._identificacion = valor_str

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if valor and (not str(valor).isdigit() or len(str(valor)) < 7):
            raise ClienteError("Teléfono inválido (debe ser numérico y mínimo 7 dígitos).")
        self._telefono = str(valor).strip() if valor else ""

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if valor and ("@" not in valor or "." not in valor.split("@")[-1]):
            raise ClienteError("Formato de correo electrónico inválido.")
        self._correo = str(valor).strip().lower() if valor else ""

    def validar_datos(self):
        if not self.nombre or not self.identificacion:
            raise ClienteError("Nombre e identificación son campos obligatorios.")

    def obtener_info(self):
        return f"{self.nombre} | ID: {self.identificacion}"


# ==================== CLASE ABSTRACTA SERVICIO ====================
class Servicio(EntidadBase, ABC):
    def __init__(self, nombre, precio_base, activo=True):
        self.nombre = nombre
        self.precio_base = float(precio_base)
        self.activo = activo

    @abstractmethod
    def calcular_costo(self, cantidad=1, iva=0.19, descuento=0.0):
        """Cálculo de costo con parámetros opcionales (sobrecarga simulada)."""
        pass

    @abstractmethod
    def describir(self):
        pass

    def validar_datos(self):
        if self.precio_base <= 0:
            raise ServicioError(f"El precio de '{self.nombre}' debe ser mayor a cero.")
        if not self.activo:
            raise ServicioError(f"El servicio '{self.nombre}' no se encuentra disponible.")

    def obtener_info(self):
        return self.describir()


# ==================== SERVICIOS CONCRETOS ====================
class ReservaSala(Servicio):
    def calcular_costo(self, cantidad=1, iva=0.19, descuento=0.0):
        self.validar_datos()
        if cantidad <= 0:
            raise ReservaError("La cantidad/duración debe ser positiva.")
        base = self.precio_base * cantidad
        con_desc = base * (1 - descuento / 100)
        return round(con_desc * (1 + iva), 2)

    def describir(self):
        return f"Reserva de Sala - ${self.precio_base:.2f}/hora | Activo: {self.activo}"


class AlquilerEquipo(Servicio):
    def calcular_costo(self, cantidad=1, iva=0.19, descuento=0.0):
        self.validar_datos()
        if cantidad <= 0:
            raise ReservaError("La cantidad/duración debe ser positiva.")
        base = self.precio_base * cantidad
        con_desc = base * (1 - descuento / 100)
        return round(con_desc * (1 + iva), 2)

    def describir(self):
        return f"Alquiler de Equipo - ${self.precio_base:.2f}/día | Activo: {self.activo}"


class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, cantidad=1, iva=0.19, descuento=0.0):
        self.validar_datos()
        if cantidad <= 0:
            raise ReservaError("La cantidad/duración debe ser positiva.")
        base = self.precio_base * cantidad
        con_desc = base * (1 - descuento / 100)
        return round(con_desc * (1 + iva), 2)

    def describir(self):
        return f"Asesoría Especializada - ${self.precio_base:.2f}/hora | Activo: {self.activo}"


# ==================== CLASE RESERVA ====================
class Reserva:
    def __init__(self, cliente, servicio, cantidad, estado="Pendiente"):
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = estado
        self.costo_final = 0.0
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M")

    def confirmar(self, iva=0.19, descuento=0.0):
        try:
            self.costo_final = self.servicio.calcular_costo(self.cantidad, iva, descuento)
            self.estado = "Confirmada"
            return True
        except Exception as err:
            raise ReservaError(f"Error al confirmar reserva: {err}") from err

    def cancelar(self):
        if self.estado in ("Cancelada", "Procesada"):
            raise ReservaError("No se puede cancelar una reserva en este estado.")
        self.estado = "Cancelada"
        return True

    def procesar(self):
        if self.estado != "Confirmada":
            raise ReservaError("Solo las reservas confirmadas pueden procesarse.")
        self.estado = "Procesada"
        return True


# ==================== SISTEMA PRINCIPAL ====================
class GestorSoftwareFJ:
    def __init__(self):
        self.lista_clientes = []
        self.lista_servicios = []
        self.lista_reservas = []
        self.archivo_log = "registro_eventos.log"
        self._iniciar_log()

    def _iniciar_log(self):
        with open(self.archivo_log, "a", encoding="utf-8") as archivo:
            archivo.write(f"\n===== NUEVA SESIÓN: {datetime.now()} =====\n")

    def log(self, mensaje, error=False):
        nivel = "ERROR" if error else "INFO"
        texto = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{nivel}] {mensaje}"
        with open(self.archivo_log, "a", encoding="utf-8") as archivo:
            archivo.write(texto + "\n")
        print(texto)

    def agregar_cliente(self, nombre, identificacion, telefono="", correo=""):
        try:
            nuevo = Cliente(nombre, identificacion, telefono, correo)
            self.lista_clientes.append(nuevo)
            self.log(f"Cliente registrado correctamente: {nuevo.obtener_info()}")
            return nuevo
        except Exception as e:
            self.log(f"Error al registrar cliente: {e}", error=True)
            raise

    def agregar_servicio(self, tipo, nombre, precio, activo=True):
        try:
            tipo = tipo.lower().strip()
            if tipo == "sala":
                servicio = ReservaSala(nombre, precio, activo)
            elif tipo == "equipo":
                servicio = AlquilerEquipo(nombre, precio, activo)
            elif tipo == "asesoria":
                servicio = AsesoriaEspecializada(nombre, precio, activo)
            else:
                raise ServicioError("Tipo de servicio no válido.")
            servicio.validar_datos()
            self.lista_servicios.append(servicio)
            self.log(f"Servicio creado: {servicio.describir()}")
            return servicio
        except Exception as e:
            self.log(f"Error al crear servicio: {e}", error=True)
            raise

    def crear_reserva(self, id_cliente, nombre_servicio, cantidad, descuento=0.0):
        try:
            cliente = next((c for c in self.lista_clientes if c.identificacion == str(id_cliente)), None)
            if not cliente:
                raise ReservaError("Cliente no encontrado en el sistema.")

            servicio = next((s for s in self.lista_servicios if s.nombre.lower() == nombre_servicio.lower()), None)
            if not servicio:
                raise ServicioError("Servicio no encontrado.")

            reserva = Reserva(cliente, servicio, cantidad)
            reserva.confirmar(descuento=descuento)
            self.lista_reservas.append(reserva)
            self.log(f"Reserva confirmada - {cliente.nombre} → {servicio.nombre} | Costo: ${reserva.costo_final}")
            return reserva
        except Exception as e:
            self.log(f"Error al crear reserva: {e}", error=True)
            raise

    def mostrar_resumen(self):
        print("\n========== RESUMEN DEL SISTEMA ==========")
        print("CLIENTES:")
        for c in self.lista_clientes:
            print(f"  - {c.obtener_info()}")
        print("\nSERVICIOS:")
        for s in self.lista_servicios:
            print(f"  - {s.describir()}")
        print("\nRESERVAS:")
        for r in self.lista_reservas:
            print(f"  - {r.cliente.nombre} | {r.servicio.nombre} | {r.cantidad} | ${r.costo_final} | {r.estado}")


# ==================== SIMULACIÓN DE OPERACIONES ====================
def correr_simulacion():
    gestor = GestorSoftwareFJ()
    print("=== INICIANDO SIMULACIÓN DE OPERACIONES ===\n")

    pruebas = [
        ("Registro cliente válido", lambda: gestor.agregar_cliente("Laura Martínez", "1098765432", "3104567890", "laura@correo.com")),
        ("Cliente con nombre muy corto", lambda: gestor.agregar_cliente("Lu", "123456")),
        ("Cliente con ID no numérico", lambda: gestor.agregar_cliente("Pedro Gómez", "ID-ABC")),
        ("Servicio Sala válido", lambda: gestor.agregar_servicio("sala", "Sala Reuniones A", 75.0)),
        ("Servicio Equipo válido", lambda: gestor.agregar_servicio("equipo", "Proyector HD", 35.0)),
        ("Servicio Asesoría válido", lambda: gestor.agregar_servicio("asesoria", "Capacitación Python", 150.0)),
        ("Servicio con precio negativo", lambda: gestor.agregar_servicio("sala", "Sala Pequeña", -10)),
        ("Reserva exitosa", lambda: gestor.crear_reserva("1098765432", "Sala Reuniones A", 4, descuento=5)),
        ("Reserva cliente inexistente", lambda: gestor.crear_reserva("000000", "Proyector HD", 2)),
        ("Reserva servicio inexistente", lambda: gestor.crear_reserva("1098765432", "Servicio Inexistente", 1)),
        ("Reserva con cantidad cero", lambda: gestor.crear_reserva("1098765432", "Capacitación Python", 0)),
    ]

    for num, (descripcion, accion) in enumerate(pruebas, 1):
        print(f"\n--- Prueba {num}: {descripcion} ---")
        try:
            accion()
            print("Resultado: Correcto")
        except Exception as ex:
            print(f"Resultado: Error controlado → {ex}")
        else:
            print("(else) La operación se completó sin excepciones.")
        finally:
            print("(finally) Finalizó el manejo de la operación.")

    print("\n" + "="*60)
    gestor.mostrar_resumen()
    print(f"\nArchivo de logs generado en: {os.path.abspath(gestor.archivo_log)}")


# ==================== MENÚ ====================
def menu():
    gestor = GestorSoftwareFJ()
    while True:
        print("\n" + "="*55)
        print("  SISTEMA SOFTWARE FJ - Gestión de Clientes y Reservas")
        print("="*55)
        print("1. Registrar nuevo cliente")
        print("2. Crear servicio")
        print("3. Crear reserva")
        print("4. Ver resumen del sistema")
        print("5. Ejecutar simulación completa")
        print("0. Salir")
        op = input("\nOpción: ").strip()

        try:
            if op == "1":
                n = input("Nombre: ")
                i = input("Identificación: ")
                t = input("Teléfono (opcional): ")
                c = input("Correo (opcional): ")
                gestor.agregar_cliente(n, i, t, c)
            elif op == "2":
                t = input("Tipo (sala/equipo/asesoria): ")
                n = input("Nombre del servicio: ")
                p = float(input("Precio base: "))
                gestor.agregar_servicio(t, n, p)
            elif op == "3":
                idc = input("Identificación del cliente: ")
                noms = input("Nombre del servicio: ")
                cant = int(input("Cantidad/Duración: "))
                gestor.crear_reserva(idc, noms, cant)
            elif op == "4":
                gestor.mostrar_resumen()
            elif op == "5":
                correr_simulacion()
            elif op == "0":
                print("Cerrando sistema...")
                break
            else:
                print("Opción no reconocida.")
        except Exception as e:
            print(f"Error manejado: {e}")


if __name__ == "__main__":
    menu()
