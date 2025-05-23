import flet as ft
from core.diff_equation_operations import DiffEquationOperations
import numpy as np
# Configurar backend no interactivo antes de importar pyplot
import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo
import matplotlib.pyplot as plt
import io
import tempfile
import os
import uuid

class DiffEquationView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.diff_eq_ops = DiffEquationOperations()
        self.temp_dir = tempfile.gettempdir()
        
        # Ejemplos predefinidos
        self.examples = {
            "Crecimiento exponencial": "dy/dx = y",
            "Decaimiento exponencial": "dy/dx = -0.5*y",
            "Oscilador armónico": "d2y/dx2 + y = 0",
            "Ecuación logística": "dy/dx = 0.1*y*(1-y/10)",
            "Ecuación de Bernoulli": "dy/dx = -2*x*y + y^3"
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
        
        # Controles para la ecuación diferencial
        self.equation_input = ft.TextField(
            label="Ecuación Diferencial",
            hint_text="Ejemplo: dy/dx = x + y",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=350,
            text_size=16,
        )
        
        # Control para la variable dependiente
        self.dependent_var = ft.TextField(
            label="Variable dependiente",
            value="y",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=170,
            text_size=16,
        )
        
        # Control para la variable independiente
        self.independent_var = ft.TextField(
            label="Variable independiente",
            value="x",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=170,
            text_size=16,
        )
        
        # Condiciones iniciales
        self.y0_input = ft.TextField(
            label="y(0) =",
            value="1",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=170,
            text_size=16,
        )
        
        self.x0_input = ft.TextField(
            label="x₀ =",
            value="0",
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
        
        # Selector de método
        self.method_selector = ft.Dropdown(
            label="Método de resolución",
            width=230,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            options=[
                ft.dropdown.Option("Metodo Analitico"),
                ft.dropdown.Option("Euler"),
                ft.dropdown.Option("Euler (Heun)"),
                ft.dropdown.Option("Runge-Kutta"),
                ft.dropdown.Option("Taylor (Orden 2)"),
                ft.dropdown.Option("Mínimos Cuadrados"),            ],
            value="Metodo Analitico",
        )
        
        # Comparación de métodos
        self.compare_methods = ft.Checkbox(
            label="Comparar métodos",
            value=False,
            fill_color=ft.Colors.BLUE_400,
            check_color=ft.Colors.WHITE,
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
                "Ingrese una ecuación diferencial y haga clic en 'Resolver'",
                color=ft.Colors.WHITE60,
                text_align=ft.TextAlign.CENTER,
                size=16,
            )
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
                ft.DataColumn(ft.Text(f"x", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text(f"y(x)", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
            ],
            rows=[]
        )
        
        self.results_container = ft.Container(
            width=650,
            height=200,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK87,
            padding=10,
            content=ft.Column([
                ft.Text("Tabla de resultados:", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.results_table,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ], scroll=ft.ScrollMode.AUTO)
        )
        
        # Panel de errores/mensajes
        self.message_display = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(name="info", color=ft.Colors.BLUE_400, size=20),
                    ft.Text(
                        "Ingrese una ecuación diferencial y haga clic en 'Resolver'",
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
            self.equation_input.value = self.examples[e.control.value]
            
            # Configurar parámetros adecuados según el ejemplo
            if e.control.value == "Crecimiento exponencial":
                self.y0_input.value = "1"
                self.t_total_input.value = "5"
            elif e.control.value == "Decaimiento exponencial":
                self.y0_input.value = "10"
                self.t_total_input.value = "8"
            elif e.control.value == "Oscilador armónico":
                self.y0_input.value = "0"
                self.method_selector.value = "Runge-Kutta"
                # Para el oscilador, necesitamos otra condición inicial
                # dy/dx(0) = 1
            elif e.control.value == "Ecuación logística":
                self.y0_input.value = "1"
                self.t_total_input.value = "50"
                self.h_input.value = "0.5"
            elif e.control.value == "Ecuación de Bernoulli":
                self.y0_input.value = "2"
                self.method_selector.value = "Runge-Kutta"
            
            self.page.update()
    
    def show(self):
        # Título de la página
        title = ft.Text(
            "Ecuaciones Diferenciales",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )
        
        # Botón de resolver
        solve_button = ft.ElevatedButton(
            text="Resolver",
            on_click=self.solve_equation,
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
                
                # Sección de ecuación
                ft.Container(
                    content=ft.Column([
                        ft.Text("Ecuación diferencial", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                        self.equation_input,
                    ], spacing=10),
                    margin=ft.margin.only(bottom=15)
                ),
                
                # Sección de variables
                ft.Container(
                    content=ft.Column([
                        ft.Text("Variables", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            self.dependent_var,
                            self.independent_var,
                        ], spacing=10),
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
                    margin=ft.margin.only(bottom=15)
                ),
                
                # Sección de método
                ft.Container(
                    content=ft.Column([
                        ft.Text("Método de resolución", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            self.method_selector,
                            self.compare_methods,
                        ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ], spacing=10),
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Botón de resolver
                ft.Container(
                    content=solve_button,
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
            content=ft.Column([
                # Título de resultados
                ft.Text("Resultados", color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.BOLD),
                
                # Gráfica
                ft.Container(
                    content=self.graph_container,
                    margin=ft.margin.only(top=10, bottom=10)
                ),
                
                # Tabla de resultados
                ft.Container(
                    content=self.results_container,
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
                
                # Espacio adicional al final para asegurar que se pueda hacer scroll hasta el final
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
    
    def solve_equation(self, e):
        # Limpiar contenedores y restablecer su estado inicial
        self.message_display.content = ft.Row(
            [
                ft.Icon(name="hourglass_empty", color=ft.Colors.BLUE_400, size=20),
                ft.Text(
                    "Resolviendo ecuación...",
                    color=ft.Colors.BLUE_400,
                    size=14,
                    weight=ft.FontWeight.BOLD
                )
            ],
            alignment=ft.MainAxisAlignment.START
        )
        
        self.results_table.rows = []
        self.page.update()  # Actualizar inmediatamente para mostrar el mensaje de "Resolviendo..."
        
        try:
            # Obtener valores de los campos
            equation = self.equation_input.value
            func_name = self.dependent_var.value
            indep_var = self.independent_var.value
            
            if not equation:
                self.show_message("Por favor, ingrese una ecuación diferencial.")
                return
            
            # Obtener condiciones iniciales
            try:
                x0 = float(self.x0_input.value) if self.x0_input.value else 0.0
                y0 = float(self.y0_input.value) if self.y0_input.value else 1.0
                t_total = float(self.t_total_input.value) if self.t_total_input.value else 5.0
                h = float(self.h_input.value) if self.h_input.value else 0.1
            except ValueError:
                self.show_message("Los valores numéricos no son válidos.")
                return
            
            # Crear diccionario de condiciones iniciales
            conditions = {
                f"{indep_var}(0)": x0,
                f"{func_name}(0)": y0
            }
            
            # Seleccionar método de resolución
            method = self.method_selector.value
            
            # Verificar si se quiere comparar métodos
            if self.compare_methods.value:
                # Obtener soluciones para todos los métodos
                try:
                    t_analitico, y_analitico, sol_analitico = self.diff_eq_ops.resolver_analitico(
                        equation, conditions, t_total, h, func_name, indep_var
                    )
                except Exception as ex:
                    t_analitico, y_analitico, sol_analitico = None, None, f"Error en método analítico: {str(ex)}"
                
                try:
                    t_euler, y_euler, _ = self.diff_eq_ops.resolver_euler(
                        equation, conditions, t_total, h
                    )
                except Exception as ex:
                    t_euler, y_euler = None, None
                
                try:
                    t_euler_heun, y_euler_heun, _ = self.diff_eq_ops.resolver_euler_heun(
                        equation, conditions, t_total, h
                    )
                except Exception as ex:
                    t_euler_heun, y_euler_heun = None, None
                
                try:
                    t_taylor, y_taylor, _ = self.diff_eq_ops.resolver_taylor_orden2(
                        equation, conditions, t_total, h
                    )
                except Exception as ex:
                    t_taylor, y_taylor = None, None
                
                try:
                    t_min_cuad, y_min_cuad, _ = self.diff_eq_ops.resolver_minimos_cuadrados(
                        equation, conditions, t_total, h
                    )
                except Exception as ex:
                    t_min_cuad, y_min_cuad = None, None
                
                try:
                    t_rk, y_rk, _ = self.diff_eq_ops.resolver_runge_kutta(
                        equation, conditions, t_total, h
                    )
                except Exception as ex:
                    t_rk, y_rk = None, None
                
                # Verificar si se obtuvo al menos una solución
                if (t_analitico is None and t_euler is None and t_euler_heun is None and 
                    t_taylor is None and t_min_cuad is None and t_rk is None):
                    self.show_message("No se pudo resolver la ecuación con ningún método.")
                    return
                
                # Graficar comparación
                solutions = []
                if t_analitico is not None and y_analitico is not None:
                    solutions.append((t_analitico, y_analitico, "Metodo Analitico"))
                if t_euler is not None and y_euler is not None:
                    solutions.append((t_euler, y_euler, "Euler"))
                if t_euler_heun is not None and y_euler_heun is not None:
                    solutions.append((t_euler_heun, y_euler_heun, "Euler (Heun)"))
                if t_taylor is not None and y_taylor is not None:
                    solutions.append((t_taylor, y_taylor, "Taylor (Orden 2)"))
                if t_min_cuad is not None and y_min_cuad is not None:
                    solutions.append((t_min_cuad, y_min_cuad, "Mínimos Cuadrados"))
                if t_rk is not None and y_rk is not None:
                    solutions.append((t_rk, y_rk, "Runge-Kutta"))
                
                self.plot_comparison(solutions, equation)
                
                # Usar los resultados disponibles para la tabla
                if t_analitico is not None and y_analitico is not None:
                    self.generate_results_table(t_analitico, y_analitico)
                elif t_rk is not None and y_rk is not None:
                    self.generate_results_table(t_rk, y_rk)
                elif t_euler_heun is not None and y_euler_heun is not None:
                    self.generate_results_table(t_euler_heun, y_euler_heun)
                elif t_taylor is not None and y_taylor is not None:
                    self.generate_results_table(t_taylor, y_taylor)
                elif t_min_cuad is not None and y_min_cuad is not None:
                    self.generate_results_table(t_min_cuad, y_min_cuad)
                elif t_euler is not None and y_euler is not None:
                    self.generate_results_table(t_euler, y_euler)
                
            else:
                # Resolver con el método seleccionado
                if method == "Metodo Analitico":
                    t, y, solution_latex = self.diff_eq_ops.resolver_analitico(
                        equation, conditions, t_total, h, func_name, indep_var
                    )
                elif method == "Euler":
                    t, y, solution_latex = self.diff_eq_ops.resolver_euler(
                        equation, conditions, t_total, h
                    )
                elif method == "Euler (Heun)":
                    t, y, solution_latex = self.diff_eq_ops.resolver_euler_heun(
                        equation, conditions, t_total, h
                    )
                elif method == "Taylor (Orden 2)":
                    t, y, solution_latex = self.diff_eq_ops.resolver_taylor_orden2(
                        equation, conditions, t_total, h
                    )
                elif method == "Mínimos Cuadrados":
                    t, y, solution_latex = self.diff_eq_ops.resolver_minimos_cuadrados(
                        equation, conditions, t_total, h
                    )
                elif method == "Runge-Kutta":
                    t, y, solution_latex = self.diff_eq_ops.resolver_runge_kutta(
                        equation, conditions, t_total, h
                    )
                
                # Verificar si se obtuvo una solución
                if t is None or y is None:
                    self.show_message(f"Error: {solution_latex}")
                    return
                
                # Graficar la solución
                self.plot_solution(t, y, equation, method)
                
                # Generar tabla de resultados
                self.generate_results_table(t, y)
            
        except Exception as e:
            self.show_message(f"Error al resolver la ecuación: {str(e)}")
    
    def plot_solution(self, t, y, equation, method):
        try:
            # Crear figura
            plt.figure(figsize=(6, 3.5), facecolor='#212121')
            
            # Determinar el color según el método
            if method == "Metodo Analitico":
                color = '#3498db'  # Azul
            elif method == "Euler":
                color = '#e74c3c'  # Rojo
            elif method == "Euler (Heun)":
                color = '#9b59b6'  # Morado para Heun
            elif method == "Taylor (Orden 2)":
                color = '#f1c40f'  # Amarillo para Taylor
            elif method == "Mínimos Cuadrados":
                color = '#e67e22'  # Naranja
            else:  # Runge-Kutta
                color = '#2ecc71'  # Verde
            
            # Graficar línea con puntos
            plt.plot(t, y, 'o-', color=color, linewidth=2, markersize=4)
            
            # Configuración básica
            plt.grid(True, alpha=0.5)
            plt.title(equation, color='white')
            plt.xlabel(f"{self.independent_var.value}", color='white')
            plt.ylabel(f"{self.dependent_var.value}", color='white')
            
            # Configurar colores para modo oscuro
            plt.gca().set_facecolor('#303030')
            plt.gca().tick_params(colors='white')
            plt.gca().spines['bottom'].set_color('white')
            plt.gca().spines['top'].set_color('white')
            plt.gca().spines['left'].set_color('white')
            plt.gca().spines['right'].set_color('white')
            
            # Guardar la figura en un archivo temporal con nombre único
            temp_filename = f"diff_eq_solution_{uuid.uuid4().hex[:8]}.png"
            temp_file = os.path.join(self.temp_dir, temp_filename)
            plt.savefig(temp_file, dpi=100, bbox_inches='tight', facecolor='#212121')
            plt.close()
            
            # Mostrar la imagen en el contenedor
            self.graph_container.content = ft.Image(
                src=temp_file,
                width=650,
                height=350,
                fit=ft.ImageFit.CONTAIN
            )
            
            # Mostrar mensaje de éxito
            self.show_message("Ecuación resuelta correctamente.", is_error=False)
            
            self.page.update()
            
        except Exception as e:
            self.show_message(f"Error al graficar la solución: {str(e)}")
    
    def plot_comparison(self, solutions, equation):
        try:
            # Verificar que hay soluciones válidas
            if not solutions:
                self.show_message("No hay soluciones válidas para comparar.")
                return
            
            # Crear figura
            plt.figure(figsize=(6, 3.5), facecolor='#212121')
            
            # Colores para cada método
            colors = {
                'Metodo Analitico': '#3498db',
                'Euler': '#e74c3c', 
                'Euler (Heun)': '#9b59b6',
                'Runge-Kutta': '#2ecc71',
                'Taylor (Orden 2)': '#f1c40f',
                'Mínimos Cuadrados': '#e67e22'
            }
            markers = {
                'Metodo Analitico': 'o',
                'Euler': 's',
                'Euler (Heun)': 'D',
                'Runge-Kutta': '^',
                'Taylor (Orden 2)': 'v',
                'Mínimos Cuadrados': 'p'
            }
            
            # Graficar cada solución
            for t, y, method in solutions:
                # Graficar línea con marcadores
                plt.plot(t, y, 
                         marker=markers.get(method, 'o'),
                         color=colors.get(method, '#3498db'),
                         linewidth=2,
                         markersize=4,
                         label=method)
            
            # Configuración básica
            plt.grid(True, alpha=0.5)
            plt.title(equation, color='white')
            plt.xlabel(f"{self.independent_var.value}", color='white')
            plt.ylabel(f"{self.dependent_var.value}", color='white')
            
            # Añadir leyenda simple
            plt.legend(facecolor='#303030', edgecolor='white', labelcolor='white')
            
            # Configurar colores para modo oscuro
            plt.gca().set_facecolor('#303030')
            plt.gca().tick_params(colors='white')
            plt.gca().spines['bottom'].set_color('white')
            plt.gca().spines['top'].set_color('white')
            plt.gca().spines['left'].set_color('white')
            plt.gca().spines['right'].set_color('white')
            
            # Guardar la figura en un archivo temporal con nombre único
            temp_filename = f"diff_eq_comparison_{uuid.uuid4().hex[:8]}.png"
            temp_file = os.path.join(self.temp_dir, temp_filename)
            plt.savefig(temp_file, dpi=100, bbox_inches='tight', facecolor='#212121')
            plt.close()
            
            # Mostrar la imagen en el contenedor
            self.graph_container.content = ft.Image(
                src=temp_file,
                width=650,
                height=350,
                fit=ft.ImageFit.CONTAIN
            )
            
            # Mostrar mensaje de éxito
            self.show_message("Comparación de métodos realizada correctamente.", is_error=False)
            
            self.page.update()
            
        except Exception as e:
            self.show_message(f"Error al comparar métodos: {str(e)}")
    
    def generate_results_table(self, t, y):
        try:
            # Limitar a 20 filas para no sobrecargar la tabla
            num_points = min(20, len(t))
            step = max(1, len(t) // num_points)
            
            # Limpiar filas existentes
            self.results_table.rows = []
            
            # Actualizar columnas de la tabla - solo X y Y
            self.results_table.columns = [
                ft.DataColumn(ft.Text(f"{self.independent_var.value}", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text(f"{self.dependent_var.value}({self.independent_var.value})", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
            ]
            
            # Crear filas de la tabla
            for i in range(0, len(t), step):
                if len(self.results_table.rows) >= num_points:
                    break
                
                # Crear la fila con los datos
                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{t[i]:.4f}", color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(f"{y[i]:.6f}", color=ft.Colors.WHITE)),
                    ]
                )
                
                # Añadir la fila a la tabla
                self.results_table.rows.append(row)
            
            # Actualizar el título de la tabla
            if len(self.results_container.content.controls) > 0:
                self.results_container.content.controls[0].value = f"Tabla de resultados ({len(self.results_table.rows)} puntos de {len(t)} totales):"
                self.results_container.content.controls[0].color = ft.Colors.WHITE
                self.results_container.content.controls[0].weight = ft.FontWeight.BOLD
            
            # Actualizar el contenedor de resultados
            self.results_container.content.controls = [
                self.results_container.content.controls[0],  # Título
                ft.Container(
                    content=self.results_table,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]
            
            # Actualizar la página
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