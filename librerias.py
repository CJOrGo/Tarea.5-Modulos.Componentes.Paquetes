# Ejercicio 1: Usar os y sys para información del sistema
import os
import sys
from colorama import Fore, Style, init, Back, Cursor
init(autoreset=True)

def info_sistema():
    """Recopila información del sistema."""
    # TODO: Implementar función que retorne diccionario con:
    info = {
    # - Sistema operativo
        "sistema_operativo": os.name,
    # - Versión de Python
        "version_python": sys.version,
    # - Directorio actual
        "directorio_actual": os.getcwd(),
    # - Variables de entorno importantes             
        "variables_entorno": str({key: os.environ[key] for key in ['PATH', 'HOME', 'USER'] if key in os.environ})
        }
    
#    for clave, valor in info.items():
#        print (f"{Fore.YELLOW + clave}: {Fore.RESET + valor}")
    return info
 
# Ejercicio 2: Procesamiento de fechas
from datetime import datetime, timedelta

def calcular_edad_dias(fecha_nacimiento: str):
    """Calcula edad en días desde fecha de nacimiento."""
    # TODO: Implementar cálculo de edad en días
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    hoy = datetime.now()
    edad_dias = hoy - fecha_nacimiento
    return edad_dias.days
    # Formato fecha: "YYYY-MM-DD"

def proximo_cumpleanos(fecha_nacimiento: str):
    """Calcula días hasta el próximo cumpleaños."""
    # TODO: Implementar cálculo
    fecha_actual = datetime.now().date()
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
    proximo_cumple = fecha_nacimiento.replace(year=fecha_actual.year)
    if proximo_cumple < fecha_actual:
        proximo_cumple = proximo_cumple.replace(year=fecha_actual.year + 1)
    dias_restantes = (proximo_cumple - fecha_actual).days
    if dias_restantes == 0:
        return "\U0001F389 ¡Feliz cumpleaños!"
    else:
        return dias_restantes