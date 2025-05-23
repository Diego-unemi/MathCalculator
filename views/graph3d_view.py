import flet as ft
from core.graph3d_operations import Graph3DOperations
import numpy as np
# Configurar backend no interactivo antes de importar pyplot
import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import io
import os
import tempfile

class Graph3DView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.graph_ops = Graph3DOperations()
        self.temp_dir = tempfile.gettempdir()
        
        # Controles para la función
        self.function_input = ft.TextField(
            label="Función f(x,y)",
            hint_text="Ejemplo: x^2 + y^2",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=400,
            text_size=16,
        )
        
        # Controles para el rango de x
        self.x_min_input = ft.TextField(
            label="x mínimo",
            value="-5",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=80,
            text_size=16,
        )
        
        self.x_max_input = ft.TextField(
            label="x máximo",
            value="5",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=80,
            text_size=16,
        )
        
        # Controles para el rango de y
        self.y_min_input = ft.TextField(
            label="y mínimo",
            value="-5",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=80,
            text_size=16,
        )
        
        self.y_max_input = ft.TextField(
            label="y máximo",
            value="5",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=80,
            text_size=16,
        )
        
        # Selector de tipo de gráfica
        self.plot_type = ft.Dropdown(
            label="Tipo de gráfica",
            width=150,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            options=[
                ft.dropdown.Option("Superficie 3D"),
                ft.dropdown.Option("Mapa de contorno"),
                ft.dropdown.Option("Ambos")
            ],
            value="Superficie 3D",
        )
        
        # Contenedor para la gráfica
        self.graph_container = ft.Container(
            width=600,
            height=450,
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
            "3D Function Grapher",
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
                                    "Ingrese una función de dos variables para graficar:",
                                    color=ft.Colors.WHITE,
                                    size=16,
                                ),
                                ft.Row(
                                    [self.function_input],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Row(
                                    [
                                        ft.Column([
                                            ft.Text("Rango de X:", color=ft.Colors.WHITE),
                                            ft.Row([self.x_min_input, self.x_max_input], spacing=10)
                                        ]),
                                        ft.Column([
                                            ft.Text("Rango de Y:", color=ft.Colors.WHITE),
                                            ft.Row([self.y_min_input, self.y_max_input], spacing=10)
                                        ]),
                                        self.plot_type
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20,
                                ),
                                ft.Container(
                                    content=plot_button,
                                    alignment=ft.alignment.center,
                                    padding=ft.padding.only(top=10)
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
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
        """Grafica la función 3D ingresada por el usuario utilizando matplotlib"""
        try:
            # Validar campos
            func_str = self.function_input.value
            if not func_str:
                self.show_error("Por favor ingrese una función.")
                return
            
            # Obtener rango de x e y
            try:
                x_min = float(self.x_min_input.value)
                x_max = float(self.x_max_input.value)
                y_min = float(self.y_min_input.value)
                y_max = float(self.y_max_input.value)
                
                if x_min >= x_max:
                    self.show_error("El valor mínimo de x debe ser menor que el máximo.")
                    return
                    
                if y_min >= y_max:
                    self.show_error("El valor mínimo de y debe ser menor que el máximo.")
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
            plot_type = self.plot_type.value
            
            # Puntos para superficie 3D (menos para mejor rendimiento)
            points_3d = 30
            
            # Más puntos para mapa de contorno
            points_contour = 100
            
            if plot_type == "Superficie 3D" or plot_type == "Ambos":
                plot_data = self.graph_ops.generate_surface_data(
                    func_str, x_min, x_max, y_min, y_max, points=points_3d
                )
            else:
                plot_data = self.graph_ops.generate_contour_data(
                    func_str, x_min, x_max, y_min, y_max, points=points_contour
                )
            
            # Crear la figura de matplotlib con backend Agg
            if plot_type == "Ambos":
                # Crear figura con dos subplots
                fig = plt.figure(figsize=(10, 5), dpi=100)
                plt.style.use('dark_background')
                
                # Superficie 3D
                ax1 = fig.add_subplot(121, projection='3d')
                surf = ax1.plot_surface(
                    plot_data['X'], plot_data['Y'], plot_data['Z'],
                    cmap=cm.coolwarm, linewidth=0, antialiased=True
                )
                ax1.set_xlabel('X')
                ax1.set_ylabel('Y')
                ax1.set_zlabel('Z')
                ax1.set_title(f"Superficie: z = {plot_data['latex']}")
                
                # Mapa de contorno
                ax2 = fig.add_subplot(122)
                contour = ax2.contourf(
                    plot_data['X'], plot_data['Y'], plot_data['Z'],
                    20, cmap=cm.coolwarm
                )
                fig.colorbar(contour, ax=ax2)
                ax2.set_xlabel('X')
                ax2.set_ylabel('Y')
                ax2.set_title(f"Contorno: z = {plot_data['latex']}")
                
                plt.tight_layout()
                
            elif plot_type == "Superficie 3D":
                # Crear figura con superficie 3D
                fig = plt.figure(figsize=(8, 6), dpi=100)
                plt.style.use('dark_background')
                
                ax = fig.add_subplot(111, projection='3d')
                surf = ax.plot_surface(
                    plot_data['X'], plot_data['Y'], plot_data['Z'],
                    cmap=cm.coolwarm, linewidth=0, antialiased=True
                )
                
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_title(f"Superficie 3D: z = {plot_data['latex']}")
                
                fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
                
            else:  # Mapa de contorno
                # Crear figura con mapa de contorno
                fig = plt.figure(figsize=(8, 6), dpi=100)
                plt.style.use('dark_background')
                
                ax = fig.add_subplot(111)
                contour = ax.contourf(
                    plot_data['X'], plot_data['Y'], plot_data['Z'],
                    20, cmap=cm.coolwarm
                )
                
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_title(f"Mapa de contorno: z = {plot_data['latex']}")
                
                fig.colorbar(contour, ax=ax)
            
            # Guardar la figura en un buffer de memoria
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', facecolor='#000000')
            buf.seek(0)
            
            # Cerrar la figura para liberar memoria
            plt.close(fig)
            
            # Generar un nombre de archivo único para evitar problemas de caché
            plot_filename = f"graph3d_plot_{hash(func_str)}_{hash(x_min)}_{hash(y_min)}.png"
            plot_path = os.path.join(self.temp_dir, plot_filename)
            
            # Guardar el buffer en un archivo
            with open(plot_path, 'wb') as f:
                f.write(buf.read())
            
            # Mostrar la imagen en el contenedor
            self.graph_container.content = ft.Image(
                src=plot_path,
                width=580,
                height=430,
                fit=ft.ImageFit.CONTAIN,
            )
            
            # Mostrar información
            self.result_container.content.controls = [
                ft.Text(
                    f"Función: f(x,y) = {plot_data['latex']}",
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