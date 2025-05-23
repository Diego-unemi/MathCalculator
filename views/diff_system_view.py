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
        self.diff_sys_ops = DiffSystemOperations()
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
            label="Sistema de Ecuaciones",
            hint_text="Ingrese el sistema en formato:\ndx/dt = f(x,y)\ndy/dt = g(x,y)",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=350,
            height=100,
            multiline=True,
            min_lines=2,
            max_lines=2,
            text_size=16,
        )
        
        # Condiciones iniciales
        self.x0_input = ft.TextField(
            label="x(0) =",
            value="1",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=170,
            text_size=16,
        )
        
        self.y0_input = ft.TextField(
            label="y(0) =",
            value="1",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=170,
            text_size=16,
        )
        
        # Parámetros de integración
        self.t_total_input = ft.TextField(
            label="Tiempo total",
            value="5",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=170,
            text_size=16,
        )
        
        self.h_input = ft.TextField(
            label="Paso (h)",
            value="0.1",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=170,
            text_size=16,
        )
        
        # Contenedor para la gráfica
        self.graph_container = ft.Container(
            width=650,
            height=350,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK,
            padding=10,
            alignment=ft.alignment.center,
            content=ft.Text(
                "Ingrese un sistema de ecuaciones y haga clic en 'Resolver'",
                color=ft.Colors.WHITE60,
                text_align=ft.TextAlign.CENTER,
                size=16,
            )
        )
        
        # Panel para valores y vectores propios (texto)
        self.eigen_panel = ft.Container(
            width=320,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK87,
            padding=10,
            content=ft.Column([
                ft.Text("Valores y Vectores Propios", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                ft.Text("", color=ft.Colors.WHITE, size=14),
            ], scroll=ft.ScrollMode.AUTO)
        )
        
        # Panel para tabla de resultados
        self.results_table = ft.DataTable(
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
        
        # Panel de errores/mensajes
        self.message_display = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(name="info", color=ft.Colors.BLUE_400, size=20),
                    ft.Text(
                        "Ingrese un sistema de ecuaciones y haga clic en 'Resolver'",
                        color=ft.Colors.BLUE_400,
                        size=14,
                        weight=ft.FontWeight.BOLD
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.all(10),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            height=60,
            width=650,
            bgcolor=ft.Colors.BLACK87,
        )
    
    def load_example(self, e):
        if e.control.value in self.examples:
            self.system_input.value = self.examples[e.control.value]
            
            # Configurar parámetros adecuados según el ejemplo
            if e.control.value == "Sistema Lineal Simple":
                self.x0_input.value = "1"
                self.y0_input.value = "1"
                self.t_total_input.value = "5"
            elif e.control.value == "Oscilador Armónico":
                self.x0_input.value = "1"
                self.y0_input.value = "0"
                self.t_total_input.value = "10"
            elif e.control.value == "Sistema con Sumidero":
                self.x0_input.value = "1"
                self.y0_input.value = "1"
                self.t_total_input.value = "5"
            elif e.control.value == "Sistema con Fuente":
                self.x0_input.value = "1"
                self.y0_input.value = "1"
                self.t_total_input.value = "5"
            elif e.control.value == "Sistema de Masas Acopladas":
                self.x0_input.value = "1"
                self.y0_input.value = "0"
                self.t_total_input.value = "10"
            elif e.control.value == "Sistema de Circuito RLC":
                self.x0_input.value = "1"
                self.y0_input.value = "0"
                self.t_total_input.value = "10"
            
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
                        ft.Row([
                            self.x0_input,
                            self.y0_input,
                        ], spacing=10),
                    ], spacing=10),
                    margin=ft.margin.only(bottom=15)
                ),
                
                # Sección de parámetros
                ft.Container(
                    content=ft.Column([
                        ft.Text("Parámetros de integración", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            self.t_total_input,
                            self.h_input,
                        ], spacing=10),
                    ], spacing=10),
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Botón de resolver
                ft.Container(
                    content=solve_button,
                    alignment=ft.alignment.center,
                ),
                
                # Panel de valores y vectores propios
                ft.Container(
                    content=self.eigen_panel,
                    margin=ft.margin.only(top=20)
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
            content=ft.Column([
                ft.Text("Resultados", color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.BOLD),
                # Gráfica
                ft.Container(
                    content=self.graph_container,
                    margin=ft.margin.only(top=10, bottom=10)
                ),
                # Tabla de resultados
                ft.Container(
                    content=self.results_table,
                    margin=ft.margin.only(top=10, bottom=10)
                ),
                # Mensajes
                ft.Container(
                    content=self.message_display,
                    margin=ft.margin.only(top=5)
                ),
            ], spacing=5, scroll=ft.ScrollMode.AUTO)
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
            self.results_table.rows = []
            self.graph_container.content = ft.Text(
                "Calculando solución...",
                color=ft.Colors.WHITE60,
                text_align=ft.TextAlign.CENTER,
                size=16,
            )
            self.eigen_panel.content.controls[1] = ft.Text("", color=ft.Colors.WHITE, size=14)
            
            self.page.update()
            
            # Obtener valores de los campos
            system = self.system_input.value
            
            if not system:
                self.show_message("Por favor, ingrese un sistema de ecuaciones.")
                return
            
            # Validar formato del sistema
            if not system.count('\n') == 1:
                self.show_message("El sistema debe tener exactamente dos ecuaciones, una por línea.")
                return
                
            if not all('dx/dt' in eq or 'dy/dt' in eq for eq in system.split('\n')):
                self.show_message("Cada ecuación debe contener dx/dt o dy/dt.")
                return
            
            # Obtener condiciones iniciales
            try:
                x0 = float(self.x0_input.value) if self.x0_input.value else 1.0
                y0 = float(self.y0_input.value) if self.y0_input.value else 1.0
                t_total = float(self.t_total_input.value) if self.t_total_input.value else 5.0
                h = float(self.h_input.value) if self.h_input.value else 0.1
            except ValueError:
                self.show_message("Los valores numéricos no son válidos.")
                return
            
            # Validar parámetros
            if t_total <= 0:
                self.show_message("El tiempo total debe ser positivo.")
                return
            if h <= 0:
                self.show_message("El paso debe ser positivo.")
                return
            if h >= t_total:
                self.show_message("El paso debe ser menor que el tiempo total.")
                return
            
            # Crear diccionario de condiciones iniciales
            conditions = {
                "x(0)": x0,
                "y(0)": y0
            }
            
            # Resolver el sistema
            try:
                t, x, y, info = self.diff_sys_ops.resolver_sistema(system, conditions, t_total, h)
                
                if t is None or x is None or y is None:
                    self.show_message("No se pudo obtener una solución válida.")
                    return
                
                # Graficar la solución
                self.plot_solution(t, x, y, system)
                
                # Generar tabla de resultados
                self.generate_results_table(t, x, y)
                
                # Renderizar y mostrar valores y vectores propios como texto
                self.show_latex_eigen(info)
                
                # Mostrar mensaje de éxito
                self.show_message("Sistema resuelto correctamente.", is_error=False)
                
            except Exception as solve_error:
                error_msg = str(solve_error)
                if "Error al parsear las ecuaciones" in error_msg:
                    self.show_message("Error en el formato de las ecuaciones. Asegúrese de usar el formato correcto:\ndx/dt = f(x,y)\ndy/dt = g(x,y)")
                else:
                    self.show_message(f"Error al resolver el sistema: {error_msg}")
                return
            
        except Exception as e:
            self.show_message(f"Error general: {str(e)}")
    
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
            self.graph_container.content = ft.Image(
                src=temp_file,
                width=650,
                height=350,
                fit=ft.ImageFit.CONTAIN
            )
            
            self.page.update()
            
        except Exception as e:
            self.show_message(f"Error al graficar la solución: {str(e)}")
    
    def generate_results_table(self, t, x, y):
        try:
            self.results_table.rows = []
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
                self.results_table.rows.append(row)
            self.results_table.update()
            self.page.update()
        except Exception as e:
            self.show_message(f"Error al generar la tabla de resultados: {str(e)}")
    
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
    
    def show_latex_eigen(self, info):
        # Muestra los valores y vectores propios como texto
        if 'valores_propios' in info and 'vectores_propios' in info:
            eigen_text = ft.Text(
                f"{info['valores_propios']}\n\n{info['vectores_propios']}",
                color=ft.Colors.WHITE,
                size=14,
            )
            self.eigen_panel.content.controls[1] = eigen_text
            self.page.update() 