import flet as ft
from core.derivative_operations import DerivativeOperations

class DerivativeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.derivative_ops = DerivativeOperations()
        
        self.function_input = ft.TextField(
            label="Función",
            width=300,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
        )
        
        self.order_input = ft.TextField(
            label="Orden de la derivada",
            width=100,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            value="1",
        )
        
        self.evaluate_at_input = ft.TextField(
            label="Evaluar en x =",
            width=100,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
        )
        
        self.result_display = ft.Container(
            width=650,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK,
            padding=10,
            content=ft.Text(
                "Ingrese una función y haga clic en 'Calcular'",
                color=ft.Colors.WHITE60,
                text_align=ft.TextAlign.CENTER,
                size=16,
            )
        )
        
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
            on_click=self.calculate_derivative,
            bgcolor=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
        )
        
        self.view = ft.Column([
            ft.Text("Derivadas", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Text(
                "Calcula derivadas de funciones matemáticas. Soporta funciones trigonométricas, exponenciales, logarítmicas y más.",
                color=ft.Colors.WHITE70,
                size=16,
            ),
            ft.Container(height=20),
            ft.Row([
                self.function_input,
                self.order_input,
                self.evaluate_at_input,
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=20),
            ft.Row([self.calculate_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=20),
            self.result_display,
            self.message_display,
        ])
    
    def calculate_derivative(self, e):
        try:
            func_str = self.function_input.value
            if not func_str:
                self.show_error("Por favor ingrese una función.")
                return
            
            try:
                order = int(self.order_input.value)
                if order < 1:
                    raise ValueError()
            except:
                self.show_error("El orden de la derivada debe ser un número entero positivo.")
                return
            
            evaluate_at = None
            if self.evaluate_at_input.value:
                try:
                    evaluate_at = float(self.evaluate_at_input.value)
                except:
                    self.show_error("El valor de evaluación debe ser un número.")
                    return
            
            result = self.derivative_ops.compute_derivative(func_str, order, evaluate_at)
            
            latex_expr = result['expression']
            if evaluate_at is not None:
                evaluated = result['evaluated']
                if isinstance(evaluated, (int, float)):
                    evaluated = f"{evaluated:.6f}"
                content = ft.Column([
                    ft.Text("Derivada:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"${latex_expr}$", size=20, color=ft.Colors.WHITE),
                    ft.Container(height=20),
                    ft.Text(f"Evaluada en x = {evaluate_at}:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"${evaluated}$", size=20, color=ft.Colors.WHITE),
                ])
            else:
                content = ft.Column([
                    ft.Text("Derivada:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"${latex_expr}$", size=20, color=ft.Colors.WHITE),
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