import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from core.integral_operations import IntegralOperations
import flet as ft
from io import BytesIO
import base64

class IntegralView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.integral_ops = IntegralOperations()
        
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
        
        # Tipo de integral (definida o indefinida)
        self.integral_type = ft.Dropdown(
            label="Tipo de integral",
            width=200,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            options=[
                ft.dropdown.Option("Indefinida"),
                ft.dropdown.Option("Definida"),
            ],
            value="Indefinida",
            on_change=self.toggle_bounds_visibility,
        )
        
        # Límites para la integral definida
        self.lower_bound = ft.TextField(
            label="Límite inferior",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=150,
            text_size=16,
            visible=False,
        )
        
        self.upper_bound = ft.TextField(
            label="Límite superior",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=150,
            text_size=16,
            visible=False,
        )
        
        # Panel de resultados
        self.result_container = ft.Container(
            content=ft.Column([], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.all(20),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            height=250,
            width=600,
        )
        
    def show(self):
        # Título de la página
        title = ft.Text(
            "Calculadora de Integrales",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )
        
        # Botón de calcular
        calculate_button = ft.ElevatedButton(
            text="Calcular Integral",
            on_click=self.calculate_integral,
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
                                    "Ingrese una función y seleccione el tipo de integral a calcular:",
                                    color=ft.Colors.WHITE,
                                    size=16,
                                ),
                                ft.Row(
                                    [self.function_input],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Row(
                                    [
                                        self.integral_type,
                                        self.lower_bound,
                                        self.upper_bound,
                                    ],
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
    
    def toggle_bounds_visibility(self, e):
        """Muestra u oculta los campos de límites según el tipo de integral seleccionado"""
        is_definite = self.integral_type.value == "Definida"
        self.lower_bound.visible = is_definite
        self.upper_bound.visible = is_definite
        self.page.update()
    
    def latex_to_image(self, latex_str, fontsize=22):
        try:
            fig, ax = plt.subplots(figsize=(0.01*len(latex_str)+2, 1.5))
            ax.axis('off')
            fig.patch.set_alpha(0)
            ax.text(0.5, 0.5, f'${latex_str}$', fontsize=fontsize, ha='center', va='center')
            buf = BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', transparent=True, pad_inches=0.2)
            plt.close(fig)
            buf.seek(0)
            img_str = base64.b64encode(buf.getvalue()).decode()
            print(f"[DEBUG] Imagen base64 generada: {img_str[:60]}...")
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            print(f"Error generando imagen LaTeX: {e}")
            # Intento generar una imagen mínima para depuración
            try:
                fig, ax = plt.subplots(figsize=(3, 1.5))
                ax.axis('off')
                ax.text(0.5, 0.5, 'Hola', fontsize=fontsize, ha='center', va='center')
                buf = BytesIO()
                plt.savefig(buf, format='png', bbox_inches='tight', transparent=True, pad_inches=0.2)
                plt.close(fig)
                buf.seek(0)
                img_str = base64.b64encode(buf.getvalue()).decode()
                print(f"[DEBUG] Imagen mínima base64 generada: {img_str[:60]}...")
                return f"data:image/png;base64,{img_str}"
            except Exception as e2:
                print(f"Error generando imagen mínima: {e2}")
                return None
    
    def calculate_integral(self, e):
        self.result_container.content.controls = []
        try:
            func_str = self.function_input.value
            if not func_str:
                self.show_error("Por favor ingrese una función.")
                return
            # Mostrar la función original en texto plano, usando ^ para potencias
            func_str_display = func_str.replace('**', '^').replace('^', '^')
            if self.integral_type.value == "Indefinida":
                result = self.integral_ops.compute_indefinite_integral(func_str)
                # Usar el símbolo de SymPy para integrar
                integral_expr = str(self.integral_ops.parse_function(func_str).integrate(self.integral_ops.x))
                integral_str = integral_expr.replace('**', '^') + ' + C'
                controls = [
                    ft.Text("Función original:", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"f(x) = {func_str_display}", color=ft.Colors.WHITE, size=20),
                    ft.Text("Integral indefinida:", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Integral: {integral_str}", color=ft.Colors.GREEN_400, size=22, weight=ft.FontWeight.BOLD),
                ]
                self.result_container.content.controls = [ft.Column(controls, spacing=10)]
            else:
                if not self.lower_bound.value or not self.upper_bound.value:
                    self.show_error("Por favor ingrese ambos límites para la integral definida.")
                    return
                result = self.integral_ops.compute_definite_integral(
                    func_str, 
                    self.lower_bound.value, 
                    self.upper_bound.value
                )
                expr_display = result['expression'].replace('**', '^')
                result_latex_display = str(result['result_latex']).replace('**', '^')
                controls = [
                    ft.Text("Función original:", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"f(x) = {expr_display}", color=ft.Colors.WHITE, size=20),
                    ft.Text("Integral definida:", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Integral definida: ∫({result['bounds'][0]})^({result['bounds'][1]}) {expr_display} dx = {result_latex_display}", color=ft.Colors.GREEN_400, size=22, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Resultado numérico: {result['result']}", color=ft.Colors.YELLOW_400, size=18, weight=ft.FontWeight.BOLD),
                ]
                self.result_container.content.controls = [ft.Column(controls, spacing=10)]
            self.result_container.update()
        except Exception as e:
            import traceback
            print('--- EXCEPCIÓN EN calculate_integral ---')
            traceback.print_exc()
            self.show_error(f"Error: {str(e)}")
        self.page.update()
    
    def show_error(self, message):
        self.result_container.content.controls = [
            ft.Text(
                message,
                color=ft.Colors.RED_400,
                size=16,
                weight=ft.FontWeight.BOLD,
            )
        ]
        self.result_container.update()
        self.page.update() 