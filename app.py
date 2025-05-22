import os
import sys
import flet as ft
import matplotlib
matplotlib.use('Agg')  

# Agregar el directorio raíz al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar después de configurar matplotlib
from views.main_view import MainView

def main(page: ft.Page):
        # Configuración de la ventana
        page.window_width = 1200
        page.window_height = 800
        page.window_resizable = True
        page.title = "MathCalculator"
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = "#000000"  # Color negro en formato hexadecimal
        
        # Habilitar scroll para el contenido principal, pero no para toda la aplicación
        page.scroll = None        
        page.auto_scroll = False  

        # Inicializar la vista principal
        main_view = MainView(page)
        main_view.initialize()

if __name__ == "__main__":
        ft.app(target=main)