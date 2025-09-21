# visualizador_simple.py
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict


class VisualizadorDatos:
    """Componente para visualización simple de datos."""

    def __init__(self, estilo: str = "seaborn-v0_8"):
        # Configurar estilo de matplotlib
        plt.style.use(estilo)

    def grafico_barras(self, datos: Dict[str, float], titulo: str = ""):
        """Crea gráfico de barras con colores personalizados."""
        etiquetas = list(datos.keys())
        valores = list(datos.values())

        colores = plt.cm.viridis(np.linspace(0.2, 0.8, len(etiquetas)))

        plt.figure(figsize=(8, 5))
        plt.bar(etiquetas, valores, color=colores)
        plt.title(titulo, fontsize=14)
        plt.xlabel("Categorías")
        plt.ylabel("Valores")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def grafico_lineas(self, y: List, titulo: str = ""):
        """Crea gráfico de líneas con límite de X hasta n+1."""
        plt.figure(figsize=(8, 5))
        x = list(range(1, len(y) + 1))
        plt.plot(x, y, marker="o", linestyle="-", color="tab:blue")
        plt.title(titulo, fontsize=14)
        plt.xlabel("Eje X")
        plt.ylabel("Eje Y")
        plt.grid(True, linestyle="--", alpha=0.6)
        if len(y) > 0:
            plt.xlim([min(x), max(x)+1])
        plt.tight_layout()
        plt.show()

    def histograma(self, datos: List[float], bins = 'auto'):
        """Crea histograma con bins automáticos por defecto."""
        plt.figure(figsize=(8, 5))
        plt.hist(datos, bins=bins, color="tab:green", edgecolor="black", alpha=0.7)
        plt.title("Histograma", fontsize=14)
        plt.xlabel("Valores")
        plt.ylabel("Frecuencia")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()

    def guardar_figura(self, nombre: str):
        """Guarda la figura actual en archivo (PNG por defecto)."""
        plt.savefig(nombre, dpi=300, bbox_inches="tight")
        print(f"Figura guardada como {nombre}")


"""
ventas_mensuales = {
        "Enero": 15000, "Febrero": 18000, "Marzo": 22000,
        "Abril": 19000, "Mayo": 25000, "Junio": 28000
    }

temperaturas = [23, 25, 27, 24, 22, 26, 28, 30, 29, 27, 25, 24]
visor = VisualizadorDatos()

visor.grafico_barras(ventas_mensuales, titulo="Ventas Mensuales")
visor.grafico_lineas(temperaturas, titulo="Temperatura Promedio Mensual")
visor.histograma(temperaturas, bins=5)
"""