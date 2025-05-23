import flet as ft
from core.derivative_operations import DerivativeOperations

class DerivativeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.derivative_ops = DerivativeOperations()
        
        # Crear controles para la función
        self.function_input = ft.TextField(
            label="Función f(x)",
            hint_text="Ejemplo: x^2 + 2*x + 1",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=400,
            text_size=16,
        )
        
        # Orden de la derivada
        self.order_input = ft.Dropdown(
            label="Orden de la derivada",
            width=200,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            options=[
                ft.dropdown.Option("1"),
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),
                ft.dropdown.Option("5"),
            ],
            value="1",
        )
        
        # Punto de evaluación (opcional)
        self.point_input = ft.TextField(
            label="Evaluar en x =",
            hint_text="Dejar vacío para no evaluar",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=200,
            text_size=16,
        )
        
        # Panel de resultados
        self.result_container = ft.Container(
            content=ft.Column([], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.all(20),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            height=200,
            width=600,
        )
        
    def show(self):
        # Título de la página
        title = ft.Text(
            "Derivatives Calculator",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )
        
        # Botón de calcular
        calculate_button = ft.ElevatedButton(
            text="Calcular Derivada",
            on_click=self.calculate_derivative,
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
                                    "Ingrese una función y los parámetros para calcular su derivada:",
                                    color=ft.Colors.WHITE,
                                    size=16,
                                ),
                                ft.Row(
                                    [self.function_input],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Row(
                                    [self.order_input, self.point_input],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Container(
                                    content=calculate_button,
                                    padding=ft.padding.symmetric(vertical=10),
                                    alignment=ft.alignment.center,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                        ),
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
        
        self.page.update()
    
    def calculate_derivative(self, e):
        # Limpiar resultados anteriores
        self.result_container.content.controls = []
        
        try:
            # Validar campos
            func_str = self.function_input.value
            if not func_str:
                self.show_error("Por favor ingrese una función.")
                return
            
            order = int(self.order_input.value)
            
            # Evaluar en un punto si se especifica
            point = None
            if self.point_input.value:
                try:
                    point = float(self.point_input.value)
                except ValueError:
                    self.show_error("El punto de evaluación debe ser un número.")
                    return
            
            # Obtener la función original en formato LaTeX
            original_latex = self.derivative_ops.get_function_latex(func_str)
            
            # Calcular la derivada
            result = self.derivative_ops.compute_derivative(func_str, order, point)
            
            # Mostrar resultados
            self.result_container.content.controls = [
                ft.Column(
                    [
                        ft.Text(
                            f"Función original: f(x) = {original_latex}",
                            color=ft.Colors.WHITE,
                            size=16,
                        ),
                        ft.Text(
                            f"Derivada {order}ª: f{self._get_order_prime(order)}(x) = {result['expression']}",
                            color=ft.Colors.WHITE,
                            size=16,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                )
            ]
            
            # Agregar el valor evaluado si se especificó un punto
            if 'evaluated' in result:
                self.result_container.content.controls[0].controls.append(
                    ft.Text(
                        f"Evaluado en x = {point}: f{self._get_order_prime(order)}({point}) = {result['evaluated']}",
                        color=ft.Colors.WHITE,
                        size=16,
                    )
                )
            
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
        
        self.page.update()
    
    def _get_order_prime(self, order):
        """Devuelve la notación adecuada para el orden de la derivada"""
        if order == 1:
            return "'"
        elif order == 2:
            return "''"
        elif order == 3:
            return "'''"
        else:
            return f"^({order})"
    
    def show_error(self, message):
        """Muestra un mensaje de error en el contenedor de resultados"""
        self.result_container.content.controls = [
            ft.Text(
                message,
                color=ft.Colors.RED_400,
                size=16,
            )
        ]
        self.page.update() 