import flet as ft
from core.graph2d_operations import Graph2DOperations
import numpy as np
# Configurar backend no interactivo antes de importar pyplot
import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo
import matplotlib.pyplot as plt
import io
import os
import tempfile
import base64

class Graph2DView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.graph_ops = Graph2DOperations()
        self.temp_dir = tempfile.gettempdir()
        
        # Controles para la función
        self.function_input = ft.TextField(
            label="Función f(x)",
            hint_text="Ejemplo: x^2 + 2*x + 1",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=400,
            text_size=16,
        )
        
        # Controles para el rango de x
        self.x_min_input = ft.TextField(
            label="x mínimo",
            value="-10",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=100,
            text_size=16,
        )
        
        self.x_max_input = ft.TextField(
            label="x máximo",
            value="10",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=100,
            text_size=16,
        )
        
        # Contenedor para la imagen de la gráfica
        self.graph_image = ft.Image(
            width=600,
            height=400,
            fit=ft.ImageFit.CONTAIN,
        )
        
        # Contenedor para la gráfica
        self.graph_container = ft.Container(
            width=600,
            height=400,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK,
            padding=10,
            alignment=ft.alignment.center,
            content=ft.Text(
                "Ingrese una función y haga clic en 'Graficar función'",
                color=ft.Colors.WHITE60,
                text_align=ft.TextAlign.CENTER,
                size=16,
            )
        )
        
        # Panel de resultados/errores
        self.result_container = ft.Container(
            content=ft.Column([], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.all(10),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            height=60,
            width=600,
        )
    
    def show(self):
        # Título de la página
        title = ft.Text(
            "2D Function Grapher",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )
        
        # Botón de graficar
        plot_button = ft.ElevatedButton(
            text="Graficar función",
            on_click=self.plot_function,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        )
        
        # Layout principal
        self.page.controls[0].controls[1].content.controls = [
            ft.Column(
                [
                    # Título 
                    ft.Container(
                        padding=ft.padding.only(left=40, top=20, right=40, bottom=10),
                        content=ft.Row(
                            [title],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ),
                    
                    # Sección de entrada
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=40, vertical=10),
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Ingrese una función para graficar:",
                                    color=ft.Colors.WHITE,
                                    size=16,
                                ),
                                ft.Row(
                                    [self.function_input],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Row(
                                    [
                                        self.x_min_input,
                                        self.x_max_input,
                                        plot_button,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                        ),
                    ),
                    
                    # Sección de gráfica
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=40, vertical=10),
                        content=self.graph_container,
                        alignment=ft.alignment.center,
                    ),
                    
                    # Sección de resultados
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=40, vertical=10),
                        content=self.result_container,
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        ]
        
        self.page.update()
    
    def plot_function(self, e):
        """Grafica la función ingresada por el usuario utilizando matplotlib"""
        try:
            # Validar campos
            func_str = self.function_input.value
            if not func_str:
                self.show_error("Por favor ingrese una función.")
                return
            
            # Obtener rango de x
            try:
                x_min = float(self.x_min_input.value)
                x_max = float(self.x_max_input.value)
                if x_min >= x_max:
                    self.show_error("El valor mínimo de x debe ser menor que el máximo.")
                    return
            except ValueError:
                self.show_error("Los valores de rango deben ser números.")
                return
            
            # Crear mensaje de espera
            self.graph_container.content = ft.Text(
                "Generando gráfica...",
                color=ft.Colors.WHITE,
                size=16,
            )
            self.page.update()
            
            # Generar datos para la gráfica
            plot_data = self.graph_ops.generate_plot_data(func_str, x_min, x_max, points=500)
            
            # Crear la figura de matplotlib con backend Agg
            plt.figure(figsize=(6, 4), dpi=100)
            plt.style.use('dark_background')
            
            # Filtrar valores NaN
            valid_indices = ~np.isnan(plot_data['y'])
            x_valid = [plot_data['x'][i] for i in range(len(plot_data['x'])) if valid_indices[i]]
            y_valid = [plot_data['y'][i] for i in range(len(plot_data['y'])) if valid_indices[i]]
            
            # Graficar la función
            plt.plot(x_valid, y_valid, color='#2196f3', linewidth=2, label=f"f(x) = {plot_data['latex']}")
            
            # Configurar los ejes
            plt.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
            plt.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
            plt.grid(True, alpha=0.3)
            
            # Etiquetas y leyenda
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f"Gráfica de f(x) = {plot_data['latex']}")
            plt.legend(loc='upper right')
            
            # Ajustar los límites de la gráfica
            plt.xlim(x_min, x_max)
            if len(y_valid) > 0:
                y_range = max(y_valid) - min(y_valid)
                if y_range < 1e-10:
                    y_range = 10
                plt.ylim(min(y_valid) - y_range * 0.1, max(y_valid) + y_range * 0.1)
            
            # Guardar la figura en un buffer de memoria en lugar de un archivo
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', facecolor='#000000')
            buf.seek(0)
            
            # Cerrar la figura para liberar memoria
            plt.close()
            
            # Generar un nombre de archivo único para evitar problemas de caché
            plot_filename = f"graph_plot_{hash(func_str)}_{hash(x_min)}_{hash(x_max)}.png"
            plot_path = os.path.join(self.temp_dir, plot_filename)
            
            # Guardar el buffer en un archivo
            with open(plot_path, 'wb') as f:
                f.write(buf.read())
            
            # Mostrar la imagen en el contenedor
            self.graph_container.content = ft.Image(
                src=plot_path,
                width=580,
                height=380,
                fit=ft.ImageFit.CONTAIN,
            )
            
            # Mostrar información
            self.result_container.content.controls = [
                ft.Text(
                    f"Función: f(x) = {plot_data['latex']}",
                    color=ft.Colors.WHITE,
                    size=14,
                )
            ]
            
            # Actualizar la página
            self.page.update()
            
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def show_error(self, message):
        """Muestra un mensaje de error"""
        self.result_container.content.controls = [
            ft.Text(
                message,
                color=ft.Colors.RED_400,
                size=14,
            )
        ]
        self.page.update() 