import flet as ft
import sympy as sp
from core.equation_operations import EquationOperations

class EquationView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.eq_ops = EquationOperations()
        self.eq_types = ["Lineal", "Cuadrática", "Sistema 2x2"]
        self.current_eq_type = "Lineal"
        self.coefficient_inputs = []
        
    def show(self):
        # Título de la página
        title = ft.Text(
            "Equation Solver",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )
        
        # Selector de tipo de ecuación
        equation_selector = ft.Dropdown(
            width=200,
            text_size=16,
            value=self.current_eq_type,
            options=[
                ft.dropdown.Option(eq_type) for eq_type in self.eq_types
            ],
            on_change=self.change_equation_type,
        )
        
        # Contenedor para los coeficientes
        self.coefficient_container = ft.Container(
            content=ft.Column([], alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.all(20),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_400),
        )
        
        # Contenedor para los resultados
        self.result_container = ft.Container(
            content=ft.Column([], alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.all(20),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            height=200,
        )
        
        # Botón de resolver
        solve_button = ft.ElevatedButton(
            text="Resolver",
            on_click=self.solve_equation,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        )
        
        # Layout principal
        self.page.controls[0].controls[1].content.controls = [
            ft.Column(
                [
                    # Título y selector de ecuación
                    ft.Container(
                        padding=ft.padding.only(left=40, top=20, right=40, bottom=10),
                        content=ft.Row(
                            [title, equation_selector],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ),
                    
                    # Sección de coeficientes
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=40, vertical=10),
                        content=ft.Column(
                            [
                                ft.Text("Coeficientes:", color=ft.Colors.WHITE, size=18),
                                self.coefficient_container,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                    ),
                    
                    # Botón de resolver
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=40, vertical=10),
                        content=solve_button,
                        alignment=ft.alignment.center,
                    ),
                    
                    # Sección de resultados
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=40, vertical=10),
                        content=ft.Column(
                            [
                                ft.Text("Resultados:", color=ft.Colors.WHITE, size=18),
                                self.result_container,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        ]
        
        # Inicializar con ecuación lineal
        self.update_equation_ui("Lineal")
    
    def update_equation_ui(self, eq_type):
        self.coefficient_container.content.controls = []
        self.coefficient_inputs = []
        
        if eq_type == "Lineal":
            # ax + b = 0
            layout = ft.Row(
                [
                    ft.Text("a:", color=ft.Colors.WHITE),
                    self.create_coef_input("1"),
                    ft.Text("x + b:", color=ft.Colors.WHITE),
                    self.create_coef_input("0"),
                    ft.Text("= 0", color=ft.Colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )
            self.coefficient_container.content.controls.append(layout)
            
        elif eq_type == "Cuadrática":
            # ax^2 + bx + c = 0
            layout = ft.Row(
                [
                    ft.Text("a:", color=ft.Colors.WHITE),
                    self.create_coef_input("1"),
                    ft.Text("x² + b:", color=ft.Colors.WHITE),
                    self.create_coef_input("0"),
                    ft.Text("x + c:", color=ft.Colors.WHITE),
                    self.create_coef_input("0"),
                    ft.Text("= 0", color=ft.Colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )
            self.coefficient_container.content.controls.append(layout)
            
        elif eq_type == "Sistema 2x2":
            # a1x + b1y = c1
            # a2x + b2y = c2
            layout1 = ft.Row(
                [
                    ft.Text("a₁:", color=ft.Colors.WHITE),
                    self.create_coef_input("1"),
                    ft.Text("x + b₁:", color=ft.Colors.WHITE),
                    self.create_coef_input("1"),
                    ft.Text("y = c₁:", color=ft.Colors.WHITE),
                    self.create_coef_input("0"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )
            
            layout2 = ft.Row(
                [
                    ft.Text("a₂:", color=ft.Colors.WHITE),
                    self.create_coef_input("1"),
                    ft.Text("x + b₂:", color=ft.Colors.WHITE),
                    self.create_coef_input("-1"),
                    ft.Text("y = c₂:", color=ft.Colors.WHITE),
                    self.create_coef_input("0"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )
            
            self.coefficient_container.content.controls.extend([layout1, layout2])
            
        self.page.update()
    
    def create_coef_input(self, default_value="0"):
        input_field = ft.TextField(
            value=default_value,
            width=70,
            height=40,
            bgcolor=ft.Colors.WHITE10,
            color=ft.Colors.WHITE,
            border_radius=10,
            text_align=ft.TextAlign.CENTER,
            border=ft.border.all(1, ft.Colors.BLUE_200),
        )
        self.coefficient_inputs.append(input_field)
        return input_field
    
    def change_equation_type(self, e):
        self.current_eq_type = e.control.value
        self.update_equation_ui(self.current_eq_type)
        self.clear_results()
    
    def clear_results(self):
        self.result_container.content.controls = []
        self.page.update()
    
    def solve_equation(self, e):
        try:
            coeffs = []
            for input_field in self.coefficient_inputs:
                try:
                    value = float(input_field.value)
                except:
                    value = 0
                coeffs.append(value)
                
            if self.current_eq_type == "Lineal":
                a, b = coeffs
                solutions = self.eq_ops.solve_linear_equation(a, b)
                eq_str = f"{a}x + {b} = 0"
                
            elif self.current_eq_type == "Cuadrática":
                a, b, c = coeffs
                solutions = self.eq_ops.solve_quadratic_equation(a, b, c)
                eq_str = f"{a}x² + {b}x + {c} = 0"
                
            elif self.current_eq_type == "Sistema 2x2":
                a1, b1, c1, a2, b2, c2 = coeffs
                result = self.eq_ops.solve_system_2x2(a1, b1, c1, a2, b2, c2)
                eq_str = f"{a1}x + {b1}y = {c1}\n{a2}x + {b2}y = {c2}"
                
                if isinstance(result, dict):
                    solutions = [f"x = {result['x']:.4f}, y = {result['y']:.4f}"]
                else:
                    solutions = [result]
                
            # Mostrar resultados
            self.show_results(eq_str, solutions)
            
        except Exception as e:
            self.show_error(str(e))
    
    def show_results(self, equation, solutions):
        self.result_container.content.controls = []
        
        # Mostrar la ecuación
        self.result_container.content.controls.append(
            ft.Text(f"Ecuación: {equation}", color=ft.Colors.WHITE, size=16)
        )
        
        # Mostrar soluciones
        if not solutions:
            self.result_container.content.controls.append(
                ft.Text("Sin soluciones", color=ft.Colors.RED, size=16)
            )
        else:
            for solution in solutions:
                self.result_container.content.controls.append(
                    ft.Text(str(solution), color=ft.Colors.GREEN, size=16)
                )
        
        self.page.update()
    
    def show_error(self, error_msg):
        self.result_container.content.controls = []
        self.result_container.content.controls.append(
            ft.Text(f"Error: {error_msg}", color=ft.Colors.RED, size=16)
        )
        self.page.update() 