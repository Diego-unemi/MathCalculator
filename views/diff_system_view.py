import flet as ft
from core.diff_system_operations import DiffSystemOperations
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tempfile
import os
import uuid
import io

class DiffSystemView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.diff_system_ops = DiffSystemOperations()
        self.temp_dir = tempfile.gettempdir()
        
        # Ejemplos predefinidos
        self.examples = {
            "Sistema Lineal Simple": "dx/dt = x + y\ndy/dt = -x + y",
            "Oscilador Armónico": "dx/dt = y\ndy/dt = -x",
            "Sistema con Sumidero": "dx/dt = -2*x + y\ndy/dt = x - 2*y",
            "Sistema con Fuente": "dx/dt = 2*x + y\ndy/dt = x + 2*y",
            "Sistema de Masas Acopladas": "dx/dt = y\ndy/dt = -2*x - y",
            "Sistema de Circuito RLC": "dx/dt = y\ndy/dt = -x - 0.5*y"
        }
        
        # Selector de ejemplos
        self.example_selector = ft.Dropdown(
            label="Ejemplos",
            width=350,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            options=[
                ft.dropdown.Option(example) for example in self.examples.keys()
            ],
            on_change=self.load_example
        )
        
        # Campo para el sistema de ecuaciones
        self.system_input = ft.TextField(
            label="Sistema de ecuaciones",
            width=650,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
        )
        
        # Condiciones iniciales
        self.initial_conditions_input = ft.TextField(
            label="Condiciones iniciales",
            width=650,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
        )
        
        # Parámetros de integración
        self.time_range_input = ft.TextField(
            label="Rango de tiempo",
            width=300,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            value="0, 10",
        )
        
        # Contenedor para la gráfica
        self.result_display = ft.Container(
            width=650,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK,
            padding=10,
            content=ft.Text(
                "Ingrese el sistema de ecuaciones y las condiciones iniciales",
                color=ft.Colors.WHITE60,
                text_align=ft.TextAlign.CENTER,
                size=16,
            )
        )
        
        # Panel de errores/mensajes
        self.message_display = ft.Container(
            width=650,
            border=ft.border.all(1, ft.Colors.RED_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK,
            padding=10,
            content=ft.Text(
                "",
                color=ft.Colors.RED_400,
                text_align=ft.TextAlign.CENTER,
                size=16,
            )
        )
        
        self.calculate_button = ft.ElevatedButton(
            text="Calcular",
            on_click=self.calculate_solution,
            bgcolor=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
        )
        
        self.view = ft.Column([
            ft.Text("Sistemas de Ecuaciones Diferenciales", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Text(
                "Resuelve sistemas de ecuaciones diferenciales ordinarias. Ingresa las ecuaciones en formato dy/dx = f(x,y).",
                color=ft.Colors.WHITE70,
                size=16,
            ),
            ft.Container(height=20),
            self.system_input,
            ft.Container(height=20),
            self.initial_conditions_input,
            ft.Container(height=20),
            self.time_range_input,
            ft.Container(height=20),
            ft.Row([self.calculate_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=20),
            self.result_display,
            self.message_display,
        ])
    
    def load_example(self, e):
        if e.control.value in self.examples:
            self.system_input.value = self.examples[e.control.value]
            
            # Configurar parámetros adecuados según el ejemplo
            if e.control.value == "Sistema Lineal Simple":
                self.initial_conditions_input.value = "1, 1"
                self.time_range_input.value = "0, 5"
            elif e.control.value == "Oscilador Armónico":
                self.initial_conditions_input.value = "1, 0"
                self.time_range_input.value = "0, 10"
            elif e.control.value == "Sistema con Sumidero":
                self.initial_conditions_input.value = "1, 1"
                self.time_range_input.value = "0, 5"
            elif e.control.value == "Sistema con Fuente":
                self.initial_conditions_input.value = "1, 1"
                self.time_range_input.value = "0, 5"
            elif e.control.value == "Sistema de Masas Acopladas":
                self.initial_conditions_input.value = "1, 0"
                self.time_range_input.value = "0, 10"
            elif e.control.value == "Sistema de Circuito RLC":
                self.initial_conditions_input.value = "1, 0"
                self.time_range_input.value = "0, 10"
            
            self.page.update()
    
    def calculate_solution(self, e):
        try:
            system_str = self.system_input.value
            if not system_str:
                self.show_error("Por favor ingrese el sistema de ecuaciones.")
                return
            
            initial_conditions_str = self.initial_conditions_input.value
            if not initial_conditions_str:
                self.show_error("Por favor ingrese las condiciones iniciales.")
                return
            
            time_range_str = self.time_range_input.value
            if not time_range_str:
                self.show_error("Por favor ingrese el rango de tiempo.")
                return
            
            try:
                t_start, t_end = map(float, time_range_str.split(","))
            except:
                self.show_error("El rango de tiempo debe ser dos números separados por coma.")
                return
            
            result = self.diff_system_ops.solve_system(system_str, initial_conditions_str, t_start, t_end)
            
            content = ft.Column([
                ft.Text("Solución:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(f"${result['solution']}$", size=20, color=ft.Colors.WHITE),
                ft.Container(height=20),
                ft.Text("Gráfica:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Image(
                    src=result['plot'],
                    width=600,
                    height=400,
                ),
            ])
            
            self.result_display.content = content
            self.message_display.content = ft.Text("", color=ft.Colors.RED_400)
            self.page.update()
            
        except Exception as e:
            self.show_error(str(e))
    
    def show_error(self, message: str):
        self.message_display.content = ft.Text(
            message,
            color=ft.Colors.RED_400,
            text_align=ft.TextAlign.CENTER,
            size=16,
        )
        self.page.update()
    
    def show(self):
        # Título de la página
        title = ft.Text(
            "Sistemas de Ecuaciones Diferenciales",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )
        
        # Botón de resolver
        solve_button = ft.ElevatedButton(
            text="Resolver",
            on_click=self.solve_system,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            width=150,
            height=45,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )
        
        # Panel de configuración - Lado izquierdo
        config_panel = ft.Container(
            width=400,
            padding=ft.padding.all(20),
            border=ft.border.all(1, ft.Colors.BLUE_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK54,
            content=ft.Column([
                # Sección de ejemplos
                ft.Container(
                    content=ft.Column([
                        ft.Text("Ejemplos predefinidos", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                        self.example_selector,
                    ], spacing=10),
                    margin=ft.margin.only(bottom=15)
                ),
                
                # Sección del sistema
                ft.Container(
                    content=ft.Column([
                        ft.Text("Sistema de ecuaciones", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                        self.system_input,
                    ], spacing=10),
                    margin=ft.margin.only(bottom=15)
                ),
                
                # Sección de condiciones iniciales
                ft.Container(
                    content=ft.Column([
                        ft.Text("Condiciones iniciales", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                        self.initial_conditions_input,
                    ], spacing=10),
                    margin=ft.margin.only(bottom=15)
                ),
                
                # Sección de parámetros
                ft.Container(
                    content=ft.Column([
                        ft.Text("Rango de tiempo", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                        self.time_range_input,
                    ], spacing=10),
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Botón de resolver
                ft.Container(
                    content=self.calculate_button,
                    alignment=ft.alignment.center,
                ),
            ], spacing=5)
        )
        
        # Panel de resultados - Lado derecho
        results_panel = ft.Container(
            expand=True,
            padding=ft.padding.all(20),
            border=ft.border.all(1, ft.Colors.BLUE_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK54,
            content=self.view
        )
        
        # Layout principal: dos paneles lado a lado
        main_layout = ft.Row(
            [
                config_panel,
                results_panel
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        
        # Contenedor principal con título y layout
        main_content = ft.Column(
            [
                # Título 
                ft.Container(
                    padding=ft.padding.only(left=40, top=20, right=40, bottom=20),
                    content=ft.Row(
                        [title],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
                
                # Layout principal
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=40),
                    content=main_layout,
                    expand=True,
                ),
                
                # Espacio adicional al final
                ft.Container(height=30),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        # Establecer el contenido con scroll
        self.page.controls[0].controls[1].content.controls = [main_content]
        self.page.update()
    
    def solve_system(self, e):
        try:
            # Limpiar contenedores y restablecer su estado inicial
            self.message_display.content = ft.Row(
                [
                    ft.Icon(name="hourglass_empty", color=ft.Colors.BLUE_400, size=20),
                    ft.Text(
                        "Resolviendo sistema...",
                        color=ft.Colors.BLUE_400,
                        size=14,
                        weight=ft.FontWeight.BOLD
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            )
            
            # Limpiar resultados anteriores
            self.result_display.content = ft.Text(
                "Calculando solución...",
                color=ft.Colors.WHITE60,
                text_align=ft.TextAlign.CENTER,
                size=16,
            )
            
            self.page.update()
            
            # Obtener valores de los campos
            system_str = self.system_input.value
            initial_conditions_str = self.initial_conditions_input.value
            time_range_str = self.time_range_input.value
            
            if not system_str:
                self.show_error("Por favor, ingrese un sistema de ecuaciones.")
                return
            
            if not initial_conditions_str:
                self.show_error("Por favor, ingrese las condiciones iniciales.")
                return
            
            if not time_range_str:
                self.show_error("Por favor, ingrese el rango de tiempo.")
                return
            
            # Validar formato del sistema
            if not system_str.count('\n') == 1:
                self.show_error("El sistema debe tener exactamente dos ecuaciones, una por línea.")
                return
                
            if not all('dx/dt' in eq or 'dy/dt' in eq for eq in system_str.split('\n')):
                self.show_error("Cada ecuación debe contener dx/dt o dy/dt.")
                return
            
            # Obtener condiciones iniciales
            try:
                x0, y0 = map(float, initial_conditions_str.split(","))
            except ValueError:
                self.show_error("Los valores numéricos no son válidos.")
                return
            
            # Validar rango de tiempo
            try:
                t_start, t_end = map(float, time_range_str.split(","))
            except ValueError:
                self.show_error("El rango de tiempo debe ser dos números separados por coma.")
                return
            
            # Crear diccionario de condiciones iniciales
            conditions = {
                "x(0)": x0,
                "y(0)": y0
            }
            
            # Resolver el sistema
            try:
                result = self.diff_system_ops.solve_system(system_str, initial_conditions_str, t_start, t_end)
                
                if result is None:
                    self.show_error("No se pudo obtener una solución válida.")
                    return
                
                # Mostrar la solución
                self.result_display.content = ft.Column([
                    ft.Text("Solución:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"${result['solution']}$", size=20, color=ft.Colors.WHITE),
                    ft.Container(height=20),
                    ft.Text("Gráfica:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Image(
                        src=result['plot'],
                        width=600,
                        height=400,
                    ),
                ])
                
                # Mostrar mensaje de éxito
                self.show_error("Sistema resuelto correctamente.")
                
            except Exception as solve_error:
                error_msg = str(solve_error)
                if "Error al parsear las ecuaciones" in error_msg:
                    self.show_error("Error en el formato de las ecuaciones. Asegúrese de usar el formato correcto:\ndx/dt = f(x,y)\ndy/dt = g(x,y)")
                else:
                    self.show_error(f"Error al resolver el sistema: {error_msg}")
                return
            
        except Exception as e:
            self.show_error(f"Error general: {str(e)}")
    
    def plot_solution(self, t, x, y, system):
        try:
            # Crear figura
            plt.figure(figsize=(6, 3.5), facecolor='#212121')
            
            # Graficar x(t) y y(t)
            plt.plot(t, x, 'o-', color='#3498db', linewidth=2, markersize=4, label='x(t)')
            plt.plot(t, y, 's-', color='#e74c3c', linewidth=2, markersize=4, label='y(t)')
            
            # Configuración básica
            plt.grid(True, alpha=0.5)
            plt.title("Solución del Sistema", color='white')
            plt.xlabel("t", color='white')
            plt.ylabel("x(t), y(t)", color='white')
            plt.legend(facecolor='#303030', edgecolor='white', labelcolor='white')
            
            # Configurar colores para modo oscuro
            plt.gca().set_facecolor('#303030')
            plt.gca().tick_params(colors='white')
            plt.gca().spines['bottom'].set_color('white')
            plt.gca().spines['top'].set_color('white')
            plt.gca().spines['left'].set_color('white')
            plt.gca().spines['right'].set_color('white')
            
            # Guardar la figura
            temp_filename = f"diff_sys_solution_{uuid.uuid4().hex[:8]}.png"
            temp_file = os.path.join(self.temp_dir, temp_filename)
            plt.savefig(temp_file, dpi=100, bbox_inches='tight', facecolor='#212121')
            plt.close()
            
            # Mostrar la imagen
            self.result_display.content = ft.Image(
                src=temp_file,
                width=650,
                height=350,
                fit=ft.ImageFit.CONTAIN
            )
            
            self.page.update()
            
        except Exception as e:
            self.show_error(f"Error al graficar la solución: {str(e)}")
    
    def generate_results_table(self, t, x, y):
        try:
            self.result_display.content = ft.Text(
                "Resultados",
                color=ft.Colors.WHITE,
                text_align=ft.TextAlign.CENTER,
                size=18,
                weight=ft.FontWeight.BOLD
            )
            
            # Crear tabla de resultados
            table_content = ft.DataTable(
                width=650,
                border=ft.border.all(1, ft.Colors.BLUE_400),
                border_radius=10,
                bgcolor=ft.Colors.BLACK,
                data_row_max_height=35,
                heading_row_height=40,
                columns=[
                    ft.DataColumn(ft.Text("t", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("x(t)", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("y(t)", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ],
                rows=[]
            )
            
            for i in range(len(t)):
                # Formatear t: sin decimales si es entero, 1 decimal si es fraccionario
                if float(t[i]).is_integer():
                    t_val = f"{int(t[i])}"
                else:
                    t_val = f"{t[i]:.1f}"
                # Formatear x(t) y y(t) con 3 decimales
                x_val = f"{x[i]:.3f}"
                y_val = f"{y[i]:.3f}"
                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(t_val, color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(x_val, color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(y_val, color=ft.Colors.WHITE)),
                    ]
                )
                table_content.rows.append(row)
            
            self.result_display.content = ft.Column([
                ft.Text("Resultados", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Container(height=10),
                table_content,
            ])
            
            self.page.update()
        except Exception as e:
            self.show_error(f"Error al generar la tabla de resultados: {str(e)}")
    
    def show_message(self, message, is_error=True):
        icon_name = "error" if is_error else "check_circle"
        icon_color = ft.Colors.RED_400 if is_error else ft.Colors.GREEN_400
        
        self.message_display.content = ft.Row([
            ft.Icon(name=icon_name, color=icon_color, size=20),
            ft.Text(
                message,
                color=icon_color,
                size=14,
                weight=ft.FontWeight.BOLD
            )
        ], alignment=ft.MainAxisAlignment.START)
        
        self.page.update() 