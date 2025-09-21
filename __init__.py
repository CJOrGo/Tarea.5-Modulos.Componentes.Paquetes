import flet as ft
from visualizador_simple import VisualizadorDatos
from system_Info import info_sistema, calcular_edad_dias, proximo_cumpleanos
from config_manager import ConfigManager

# Diccionario para mapear librerías y sus funciones con los parámetros requeridos
LIBRERIAS = {
    "VisualizadorDatos": {
        "grafico_barras": ["titulo (str)"],
        "grafico_lineas": ["titulo (str)"],
        "histograma": ["bins (int)"],
    },
    "SystemInfo": {
        "info_sistema": [],
        "calcular_edad_dias": ["fecha (YYYY-MM-DD)"],
        "proximo_cumpleanos": ["fecha (YYYY-MM-DD)"]
    },
    "ConfigManager": {
        "set": ["clave (str)", "valor"],
        "save": [],
        "load_from_env": ["diccionario_env (dict)"]
    }
}

def main(page: ft.Page):
    page.title = "Gestor de Librerías"
    page.scroll = "auto"

    # Dropdown de librerías
    libreria_dropdown = ft.Dropdown(
        label="Selecciona una librería",
        options=[ft.dropdown.Option(lib) for lib in LIBRERIAS.keys()],
        width=300
    )

    funciones_dropdown = ft.Dropdown(
        label="Selecciona una función",
        options=[],
        width=300
    )

    parametros_container = ft.Column()
    resultado_text = ft.Text("Resultado aparecerá aquí...", selectable=True)

    # Datos temporales para graficas
    datos_temporales = {"dict": {}, "list": []}

    # --- Funciones de UI ---
    def mostrar_funciones(e):
        funciones_dropdown.options = [
            ft.dropdown.Option(func) for func in LIBRERIAS[libreria_dropdown.value].keys()
        ]
        funciones_dropdown.value = None
        parametros_container.controls.clear()
        page.update()

    def agregar_elemento(e):
        if funciones_dropdown.value == "grafico_barras":
            clave = parametros_container.controls[0].value
            try:
                valor = float(parametros_container.controls[1].value)
            except:
                resultado_text.value = "⚠️ Valor debe ser numérico"
                page.update()
                return
            datos_temporales["dict"][clave] = valor
            resultado_text.value = f"Agregado {clave}: {valor}"
        elif funciones_dropdown.value in ["grafico_lineas", "histograma"]:
            try:
                valor = float(parametros_container.controls[0].value)
            except:
                resultado_text.value = "⚠️ Valor debe ser numérico"
                page.update()
                return
            datos_temporales["list"].append(valor)
            resultado_text.value = f"Agregado {valor}"
        page.update()

    def mostrar_parametros(e):
        parametros_container.controls.clear()
        if funciones_dropdown.value:
            # Mostrar campos para agregar elementos uno por uno
            if funciones_dropdown.value == "grafico_barras":
                parametros_container.controls.append(ft.TextField(label="Clave", width=150))
                parametros_container.controls.append(ft.TextField(label="Valor", width=150))
            elif funciones_dropdown.value in ["grafico_lineas", "histograma"]:
                parametros_container.controls.append(ft.TextField(label="Valor", width=150))
            else:
                # Para otras funciones: mostrar solo parámetros normales
                for p in LIBRERIAS[libreria_dropdown.value][funciones_dropdown.value]:
                    parametros_container.controls.append(ft.TextField(label=p, width=300))
        page.update()


    def ejecutar_funcion(e):
        libreria = libreria_dropdown.value
        funcion = funciones_dropdown.value
        if not libreria or not funcion:
            resultado_text.value = "⚠️ Selecciona librería y función primero."
            page.update()
            return

        # Obtener valores ingresados
        valores = [c.value for c in parametros_container.controls if isinstance(c, ft.TextField)]

        try:
            if libreria == "SystemInfo":
                if funcion == "info_sistema":
                    resultado_text.value = "\n".join(f"{k}: {v}" for k, v in info_sistema().items())
                elif funcion == "calcular_edad_dias":
                    resultado_text.value = str(calcular_edad_dias(valores[0]))
                elif funcion == "proximo_cumpleanos":
                    resultado_text.value = str(proximo_cumpleanos(valores[0]))

            elif libreria == "ConfigManager":
                config = ConfigManager("mi_config.json")
                if funcion == "set":
                    clave, valor = valores
                    config.set(clave, valor)
                    resultado_text.value = f"Set {clave}={valor}"
                elif funcion == "save":
                    config.save()
                    resultado_text.value = "Configuración guardada."
                elif funcion == "load_from_env":
                    resultado_text.value = "Cargar desde env aún no implementado."

            elif libreria == "VisualizadorDatos":
                visor = VisualizadorDatos()
                if funcion == "grafico_barras":
                    if datos_temporales["dict"]:
                        visor.grafico_barras(datos_temporales["dict"], titulo=valores[0] if valores else "")
                        resultado_text.value = f"Gráfica de barras generada con {datos_temporales['dict']}"
                    else:
                        resultado_text.value = "⚠️ No hay datos para graficar."
                elif funcion == "grafico_lineas":
                    if datos_temporales["list"]:
                        visor.grafico_lineas(datos_temporales["list"], titulo=valores[0] if valores else "")
                        resultado_text.value = f"Gráfica de líneas generada con {datos_temporales['list']}"
                    else:
                        resultado_text.value = "⚠️ No hay datos para graficar."
                elif funcion == "histograma":
                    if datos_temporales["list"]:
                        bins = int(valores[0]) if valores else 5
                        visor.histograma(datos_temporales["list"], bins=bins)
                        resultado_text.value = f"Histograma generado con {datos_temporales['list']}"
                    else:
                        resultado_text.value = "⚠️ No hay datos para graficar."

        except Exception as ex:
            resultado_text.value = f"❌ Error: {str(ex)}"

        page.update()

    # Botones
    ejecutar_btn = ft.ElevatedButton("Ejecutar", on_click=ejecutar_funcion)
    agregar_btn = ft.ElevatedButton("Agregar elemento", on_click=agregar_elemento)

    # Asignación de eventos
    libreria_dropdown.on_change = mostrar_funciones
    funciones_dropdown.on_change = mostrar_parametros

    # Layout
    page.add(
        ft.Column([
            libreria_dropdown,
            funciones_dropdown,
            parametros_container,
            ft.Row([agregar_btn, ejecutar_btn], spacing=10),
            resultado_text
        ], spacing=15)
    )

if __name__ == "__main__":
    ft.app(target=main)