import flet as ft
import numpy as np
from utils.monte_carlo import MonteCarlo
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
import tempfile
import threading
import uuid

class MonteCarloView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.monte_carlo = MonteCarlo()
        self.temp_dir = tempfile.gettempdir()
        
        # Campos de entrada para integración
        self.function_input = ft.TextField(
            label="Función f(x) (inferior)",
            value="x**2",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=200,
            text_size=16
        )
        
        self.function2_input = ft.TextField(
            label="Función g(x) (superior)",
            value="sqrt(x)",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=200,
            text_size=16,
            visible=False
        )
        
        self.a_input = ft.TextField(
            label="Límite inferior (a)",
            value="0",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=150,
            text_size=16
        )
        
        self.b_input = ft.TextField(
            label="Límite superior (b)",
            value="1",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=150,
            text_size=16
        )
        
        self.n_points_input = ft.TextField(
            label="Número de puntos",
            value="10000",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=150,
            text_size=16
        )
        
        self.seed_input = ft.TextField(
            label="Semilla (opcional)",
            value="",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=150,
            text_size=16
        )
        
        # Selector de método (solo dos opciones)
        self.method_selector = ft.Dropdown(
            label="Método",
            width=200,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            options=[
                ft.dropdown.Option("Estimación de área"),
                ft.dropdown.Option("Área entre Curvas")
            ],
            value="Estimación de área",
            on_change=self.update_input_fields
        )
        
        # Contenedor para resultados (más pequeño)
        self.result_container = ft.Container(
            content=ft.Text(
                "Resultado...",
                color=ft.Colors.WHITE,
                size=14,
            ),
            padding=ft.padding.all(10),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            width=320,
            height=60,
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
                "La gráfica se generará automáticamente al realizar un cálculo.",
                color=ft.Colors.WHITE60,
                text_align=ft.TextAlign.CENTER,
                size=16,
            )
        )
        
        # Tabla de resultados
        self.results_table = ft.DataTable(
            border=ft.border.all(1, ft.Colors.BLUE_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK,
            data_row_max_height=35,
            heading_row_height=40,
            columns=[
                ft.DataColumn(ft.Text("X", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("f(X)", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Y_aleatorio", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Interior", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
            ],
            rows=[]
        )
        self.results_container = ft.Container(
            height=300,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK87,
            padding=10,
            content=ft.Column([
                ft.Text("Tabla de resultados:", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                ft.Column(
                    controls=[self.results_table],
                    alignment=ft.alignment.center,
                    expand=True,
                    scroll=ft.ScrollMode.ALWAYS
                )
            ], scroll=ft.ScrollMode.AUTO, expand=True)
        )
        
    def update_input_fields(self, e=None):
        method = self.method_selector.value
        self.function2_input.visible = method == "Área entre Curvas"
        self.page.update()
    
    def evaluate_function(self, x: float) -> float:
        """Evalúa la función ingresada por el usuario."""
        try:
            # Permitir ^ como potencia
            func_str = self.function_input.value.replace("^", "**")
            # Crear un entorno seguro para eval
            safe_dict = {"x": x, "np": np, "sin": np.sin, "cos": np.cos, 
                        "tan": np.tan, "exp": np.exp, "log": np.log, 
                        "sqrt": np.sqrt, "pi": np.pi}
            return eval(func_str, {"__builtins__": {}}, safe_dict)
        except Exception as e:
            raise ValueError(f"Error al evaluar la función: {str(e)}")
    
    def calculate(self, e):
        try:
            n_points = int(self.n_points_input.value)
            if n_points <= 0:
                raise ValueError("El número de puntos debe ser mayor que cero.")
        except Exception as ex:
            self.result_container.content = ft.Text(
                f"Error: {str(ex)}",
                color=ft.Colors.RED,
                size=14,
            )
            self.graph_container.content = ft.Text(
                "Sin gráfica",
                color=ft.Colors.WHITE60,
                text_align=ft.TextAlign.CENTER,
                size=16,
            )
            self.results_table.rows = []
            self.results_container.content.controls[0].value = "Tabla de resultados:"
            self.page.update()
            return
        threading.Thread(target=self._calculate_thread, args=(e,)).start()

    def _calculate_thread(self, e):
        try:
            print("Iniciando cálculo...")
            # Obtener valores de los campos
            n_points = int(self.n_points_input.value)
            method = self.method_selector.value
            seed_value_str = self.seed_input.value
            seed = int(seed_value_str) if seed_value_str else None
            self.monte_carlo = MonteCarlo(seed=seed)
            print(f"Método seleccionado: {method}, Semilla: {seed}")
            if method == "Estimación de área":
                a = float(self.a_input.value)
                b = float(self.b_input.value)
                x_test = np.linspace(a, b, 100)
                y_test = [self.evaluate_function(x) for x in x_test]
                y_min = min(y_test) - 0.1 * (max(y_test) - min(y_test))
                y_max = max(y_test) + 0.1 * (max(y_test) - min(y_test))
                result, error = self.monte_carlo.estimate_area(
                    self.evaluate_function, a, b, y_min, y_max, n_points)
                x_points = [a + (b - a) * self.monte_carlo.generator.generate() for _ in range(n_points)]
                y_points = [y_min + (y_max - y_min) * self.monte_carlo.generator.generate() for _ in range(n_points)]
                f_values = [self.evaluate_function(x) for x in x_points]
                is_inside = [(y_points[i] <= f_values[i]) for i in range(n_points)]
                def update_ui():
                    self.result_container.content = ft.Text(
                        f"Área estimada: {result:.6f} ± {error:.6f}",
                        color=ft.Colors.WHITE,
                        size=14,
                    )
                    self.plot_area_estimation(a, b, y_min, y_max, n_points)
                    self.generate_results_table(x_points, y_points, f_values, None, is_inside, area_entre_curvas=False)
                update_ui()
            
            elif method == "Área entre Curvas":
                a = float(self.a_input.value)
                b = float(self.b_input.value)
                func1_str = self.function_input.value.replace("^", "**")
                func2_str = self.function2_input.value.replace("^", "**")
                f1 = lambda x: eval(func1_str, {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi})
                f2 = lambda x: eval(func2_str, {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi})
                result, error, xs, ys, is_in = self.monte_carlo.estimate_area_between_curves(f1, f2, a, b, n_points)
                f_values = [f1(x) for x in xs]
                g_values = [f2(x) for x in xs]
                def update_ui():
                    self.result_container.content = ft.Text(
                        f"Área entre curvas: {result:.6f} ± {error:.6f}",
                        color=ft.Colors.WHITE,
                        size=14,
                    )
                    self.plot_area_between_curves(func1_str, func2_str, a, b, xs, ys, is_in)
                    self.generate_results_table(xs, ys, f_values, g_values, is_in, area_entre_curvas=True)
                update_ui()
            
            # Mostrar resultados
            print("Actualizando resultados...")
            self.page.update()
            
            # Generar y mostrar gráfica después de actualizar resultados de texto
            # Esto es para que el usuario vea el resultado numérico incluso si la gráfica tarda o falla
            if method == "Estimación de área":
                print("Generando gráfica de estimación de área...")
                self.plot_area_estimation(a, b, y_min, y_max, n_points)
            elif method == "Área entre Curvas":
                print("Generando gráfica de área entre curvas...")
                self.plot_area_between_curves(self.function_input.value, self.function2_input.value, a, b, xs, ys, is_in)

            print("Cálculo completado.")
            
        except Exception as e:
            print(f"Error en el cálculo: {str(e)}")
            def update_error():
                self.result_container.content = ft.Text(
                    f"Error: {str(e)}",
                    color=ft.Colors.RED,
                    size=14,
                )
                self.page.update()
            update_error()
    
    def plot_integration(self, a: float, b: float, n_points: int):
        """Genera y muestra la gráfica para integración."""
        try:
            print("Creando figura de integración...")
            plt.figure(figsize=(8, 6))
            x = np.linspace(a, b, 1000)
            y = [self.evaluate_function(xi) for xi in x]
            
            plt.plot(x, y, 'b-', label='f(x)')
            plt.fill_between(x, y, alpha=0.3)
            plt.title('Integración por Monte Carlo')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.grid(True)
            plt.legend()
            
            print("Guardando gráfica en archivo temporal...")
            temp_file = os.path.join(self.temp_dir, "monte_carlo_integration.png")
            plt.savefig(temp_file, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            
            print("Actualizando contenedor de gráfica...")
            self.graph_container.content = ft.Image(
                src=temp_file,
                width=580,
                height=380,
                fit=ft.ImageFit.CONTAIN,
            )
            self.page.update()
            print("Gráfica de integración actualizada.")
            
        except Exception as e:
            print(f"Error al generar la gráfica de integración: {str(e)}")
            self.graph_container.content = ft.Text(
                f"Error al generar la gráfica: {str(e)}",
                color=ft.Colors.RED,
                size=16,
            )
            self.page.update()
    
    def plot_pi_estimation(self, n_points: int):
        """Genera y muestra la gráfica para la estimación de π."""
        try:
            print("Creando figura de estimación de π...")
            plt.figure(figsize=(8, 6))
            
            # Generar puntos usando el generador de la instancia de MonteCarlo (que ya tiene la semilla)
            x_points = [2 * self.monte_carlo.generator.generate() - 1 for _ in range(n_points)]
            y_points = [2 * self.monte_carlo.generator.generate() - 1 for _ in range(n_points)]
            
            # Separar puntos dentro y fuera del círculo
            in_circle = [(x, y) for x, y in zip(x_points, y_points) if x**2 + y**2 <= 1]
            out_circle = [(x, y) for x, y in zip(x_points, y_points) if x**2 + y**2 > 1]
            
            # Graficar puntos
            if in_circle:
                x_in, y_in = zip(*in_circle)
                plt.scatter(x_in, y_in, c='blue', alpha=0.5, label='Dentro')
            if out_circle:
                x_out, y_out = zip(*out_circle)
                plt.scatter(x_out, y_out, c='red', alpha=0.5, label='Fuera')
            
            # Graficar círculo
            circle = plt.Circle((0, 0), 1, fill=False, color='black')
            plt.gca().add_artist(circle)
            
            plt.title('Estimación de π por Monte Carlo')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.legend()
            plt.axis('equal')
            
            print("Guardando gráfica en archivo temporal...")
            temp_file = os.path.join(self.temp_dir, "monte_carlo_pi.png")
            plt.savefig(temp_file, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            
            print("Actualizando contenedor de gráfica...")
            self.graph_container.content = ft.Image(
                src=temp_file,
                width=580,
                height=380,
                fit=ft.ImageFit.CONTAIN,
            )
            self.page.update()
            print("Gráfica de estimación de π actualizada.")
            
        except Exception as e:
            print(f"Error al generar la gráfica de estimación de π: {str(e)}")
            self.graph_container.content = ft.Text(
                f"Error al generar la gráfica: {str(e)}",
                color=ft.Colors.RED,
                size=16,
            )
            self.page.update()
    
    def plot_area_estimation(self, a: float, b: float, y_min: float, y_max: float, n_points: int):
        """Genera y muestra la gráfica para la estimación de área."""
        try:
            print("Creando figura de estimación de área...")
            plt.figure(figsize=(8, 6))
            
            # Graficar la función
            x = np.linspace(a, b, 1000)
            y = [self.evaluate_function(xi) for xi in x]
            plt.plot(x, y, 'b-', label='f(x)')
            
            # Generar y graficar puntos aleatorios
            x_points = [a + (b - a) * self.monte_carlo.generator.generate() for _ in range(n_points)]
            y_points = [y_min + (y_max - y_min) * self.monte_carlo.generator.generate() for _ in range(n_points)]
            
            # Separar puntos bajo y sobre la curva
            under_curve = [(x, y) for x, y in zip(x_points, y_points) 
                          if y <= self.evaluate_function(x)]
            over_curve = [(x, y) for x, y in zip(x_points, y_points) 
                         if y > self.evaluate_function(x)]
            
            if under_curve:
                x_under, y_under = zip(*under_curve)
                plt.scatter(x_under, y_under, c='green', alpha=0.5, label='Bajo la curva')
            if over_curve:
                x_over, y_over = zip(*over_curve)
                plt.scatter(x_over, y_over, c='red', alpha=0.5, label='Sobre la curva')
            
            plt.title('Estimación de área por Monte Carlo')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.legend()
            
            print("Guardando gráfica en archivo temporal...")
            temp_file = os.path.join(self.temp_dir, f"monte_carlo_area_{uuid.uuid4().hex}.png")
            plt.savefig(temp_file, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            
            print("Actualizando contenedor de gráfica...")
            self.graph_container.content = ft.Image(
                src=temp_file,
                width=580,
                height=380,
                fit=ft.ImageFit.CONTAIN,
            )
            self.page.update()
            print("Gráfica de estimación de área actualizada.")
            
        except Exception as e:
            print(f"Error al generar la gráfica de estimación de área: {str(e)}")
            self.graph_container.content = ft.Text(
                f"Error al generar la gráfica: {str(e)}",
                color=ft.Colors.RED,
                size=16,
            )
            self.page.update()
    
    def plot_area_between_curves(self, func1_str, func2_str, a, b, xs, ys, is_in):
        try:
            print("Creando figura de área entre curvas...")
            plt.figure(figsize=(8, 6))
            
            x_func = np.linspace(a, b, 200)
            y_func1 = [self.evaluate_function(xi) for xi in x_func]
            y_func2 = [np.sqrt(xi) for xi in x_func]  # Función de ejemplo para la segunda curva
            
            plt.plot(x_func, y_func1, 'orange', label=f'f1(x) = {func1_str}')
            plt.plot(x_func, y_func2, 'blue', label=f'f2(x) = sqrt(x)')
            
            # Rellenar el área teórica entre las curvas
            plt.fill_between(x_func, y_func1, y_func2, where=[(y2 >= y1) for y1, y2 in zip(y_func1, y_func2)], interpolate=True, color='cyan', alpha=0.3, label='Área teórica')
            
            x_np = np.array(xs)
            y_np = np.array(ys)
            is_inside_np = np.array(is_in)
            
            plt.scatter(x_np[is_inside_np], y_np[is_inside_np], color='green', alpha=0.5, s=10, label='Puntos Interiores')
            plt.scatter(x_np[~is_inside_np], y_np[~is_inside_np], color='red', alpha=0.5, s=10, label='Puntos Exteriores')
            
            plt.title('Área entre Curvas por Monte Carlo')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.legend()
            
            print("Guardando gráfica en archivo temporal...")
            temp_file = os.path.join(self.temp_dir, f"monte_carlo_area_between_curves_{uuid.uuid4().hex}.png")
            plt.savefig(temp_file, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            
            print("Actualizando contenedor de gráfica...")
            self.graph_container.content = ft.Image(
                src=temp_file,
                width=580,
                height=380,
                fit=ft.ImageFit.CONTAIN,
            )
            self.page.update()
            print("Gráfica de área entre curvas actualizada.")
            
        except Exception as e:
            print(f"Error al generar la gráfica de área entre curvas: {str(e)}")
            self.graph_container.content = ft.Text(
                f"Error al generar la gráfica: {str(e)}",
                color=ft.Colors.RED,
                size=16,
            )
            self.page.update()
    
    def generate_results_table(self, x_points, y_points, f_values, g_values, is_inside, area_entre_curvas=False):
        self.results_table.rows = []
        # Muestra representativa: primeros 10, 10 del medio, 10 del final (o todos si <=30)
        total = len(x_points)
        if total <= 30:
            indices = list(range(total))
        else:
            first = list(range(10))
            middle = list(range(total//2 - 5, total//2 + 5))
            last = list(range(total-10, total))
            indices = first + middle + last
        if area_entre_curvas:
            self.results_table.columns = [
                ft.DataColumn(ft.Text("X", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("f(X)", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("g(X)", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Y_aleatorio", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Interior", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
            ]
            for i in indices:
                row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(f"{x_points[i]:.4f}", color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(f"{f_values[i]:.4f}", color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(f"{g_values[i]:.4f}", color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(f"{y_points[i]:.4f}", color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(f"{1 if is_inside[i] else 0}", color=ft.Colors.WHITE)),
                ])
                self.results_table.rows.append(row)
        else:
            self.results_table.columns = [
                ft.DataColumn(ft.Text("X", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("f(X)", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Y_aleatorio", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Interior", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
            ]
            for i in indices:
                row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(f"{x_points[i]:.4f}", color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(f"{f_values[i]:.4f}", color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(f"{y_points[i]:.4f}", color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(f"{1 if is_inside[i] else 0}", color=ft.Colors.WHITE)),
                ])
                self.results_table.rows.append(row)
        self.results_container.content.controls[0].value = f"Tabla de resultados (mostrando {len(indices)} de {len(x_points)} puntos totales):"
        self.page.update()
    
    def show(self):
        # Título de la página
        title = ft.Text(
            "Método de Monte Carlo",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )
        # Botón de calcular
        calculate_button = ft.ElevatedButton(
            text="Calcular",
            on_click=self.calculate,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            width=200,
            height=45,
        )
        # Panel izquierdo: configuración
        config_panel = ft.Container(
            width=270,
            padding=ft.padding.all(20),
            border=ft.border.all(1, ft.Colors.BLUE_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK54,
            content=ft.Column([
                ft.Text("Configuración:", color=ft.Colors.WHITE, size=16),
                self.method_selector,
                self.function_input,
                self.function2_input,
                self.a_input,
                self.b_input,
                self.n_points_input,
                self.seed_input,
                ft.Container(
                    content=calculate_button,
                    padding=ft.padding.symmetric(vertical=10),
                    alignment=ft.alignment.center,
                ),
                self.result_container,
            ], spacing=10)
        )
        # Panel derecho: resultados
        results_panel = ft.Container(
            expand=True,
            padding=ft.padding.all(20),
            border=ft.border.all(1, ft.Colors.BLUE_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK54,
            content=ft.Column([
                ft.Text("Resultados", color=ft.Colors.WHITE, size=20, weight=ft.FontWeight.BOLD),
                self.graph_container,
                self.results_container,
            ], spacing=10)
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
        # Contenido de la página
        self.page.controls[0].controls[1].content.controls = [
            ft.Column(
                [
                    ft.Container(
                        padding=ft.padding.only(left=40, top=20, right=40, bottom=20),
                        content=ft.Row(
                            [title],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=40),
                        content=main_layout,
                        expand=True,
                    ),
                    ft.Container(height=30),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
        ]
        self.page.update() 