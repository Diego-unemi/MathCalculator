import flet as ft
import numpy as np
from core.matrix_operations import MatrixOperations
from fractions import Fraction

class MatrixView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.matrix_size_a = 3
        self.matrix_size_b = 3
        self.matrix_a = np.zeros((self.matrix_size_a, self.matrix_size_a))
        self.matrix_b = np.zeros((self.matrix_size_b, self.matrix_size_b))
        self.matrix_ops = MatrixOperations()
        self.result_matrix = None

    def fraction_to_str(self, value):
        """Convierte un valor (entero, float o Fraction) a string para mostrar"""
        if isinstance(value, Fraction):
            if value.denominator == 1:
                return str(value.numerator)
            return f"{value.numerator}/{value.denominator}"
        elif isinstance(value, (int, np.integer)):
            return str(value)
        elif isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            return str(value)
        return str(value)

    def create_matrix_inputs(self, size, initial_values=None):
        inputs = []
        for i in range(size):
            row = []
            for j in range(size):
                value = "1"
                if initial_values is not None and i < len(initial_values) and j < len(initial_values[i]):
                    value = self.fraction_to_str(initial_values[i][j])
                
                input_field = ft.TextField(
                    value=value,
                    width=60,
                    height=60,
                    text_align=ft.TextAlign.CENTER,
                    border_radius=10,
                    text_size=20,
                    bgcolor=ft.Colors.WHITE10,
                    color=ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.BLUE_200),
                    filled=True,
                )
                row.append(input_field)
            inputs.append(ft.Row(row, alignment=ft.MainAxisAlignment.CENTER))
        return ft.Column(inputs, spacing=10, alignment=ft.MainAxisAlignment.CENTER)

    def get_matrix_values(self, matrix_inputs):
        rows = len(matrix_inputs.controls)
        matrix = []
        for i in range(rows):
            row_controls = matrix_inputs.controls[i].controls
            matrix_row = []
            for j in range(len(row_controls)):
                try:
                    # Intentar procesar fracciones en formato "a/b"
                    value_str = row_controls[j].value.strip()
                    if '/' in value_str:
                        num, denom = value_str.split('/')
                        value = float(int(num)) / float(int(denom))
                    else:
                        value = float(value_str)
                except ValueError:
                    value = 0
                matrix_row.append(value)
            matrix.append(matrix_row)
        return np.array(matrix)

    def update_matrix_size(self, e, matrix_type):
        size = int(e.control.value.split(" × ")[0])
        if matrix_type == "A":
            self.matrix_size_a = size
            self.matrix_a_inputs = self.create_matrix_inputs(size, np.ones((size, size)))
            self.matrix_container_a.content = self.matrix_a_inputs
        else:
            self.matrix_size_b = size
            self.matrix_b_inputs = self.create_matrix_inputs(size, np.ones((size, size)))
            self.matrix_container_b.content = self.matrix_b_inputs
        self.page.update()

    def fill_matrix(self, matrix_type, fill_type):
        size = self.matrix_size_a if matrix_type == "A" else self.matrix_size_b
        matrix_inputs = self.matrix_a_inputs if matrix_type == "A" else self.matrix_b_inputs
        
        if fill_type == "random":
            values = np.random.randint(-9, 10, (size, size))
        elif fill_type == "zeros":
            values = np.zeros((size, size))
        elif fill_type == "ones":
            values = np.ones((size, size))
        
        # Actualizar campos de entrada
        for i in range(size):
            for j in range(size):
                matrix_inputs.controls[i].controls[j].value = str(int(values[i, j]))
        
        self.page.update()

    def calculate(self, operation):
        # Obtener valores de matrices
        matrix_a = self.get_matrix_values(self.matrix_a_inputs)
        matrix_b = self.get_matrix_values(self.matrix_b_inputs)
        
        try:
            if operation == "+":
                result = self.matrix_ops.add_matrices(matrix_a, matrix_b)
            elif operation == "-":
                result = self.matrix_ops.subtract_matrices(matrix_a, matrix_b)
            elif operation == "×":
                result = self.matrix_ops.multiply_matrices(matrix_a, matrix_b)
            elif operation == "det_a":
                det = self.matrix_ops.calculate_determinant(matrix_a)
                if det is not None:
                    self.result_text.value = f"Determinante de A = {self.fraction_to_str(det)}"
                else:
                    self.result_text.value = "Error al calcular el determinante"
                self.page.update()
                return
            elif operation == "det_b":
                det = self.matrix_ops.calculate_determinant(matrix_b)
                if det is not None:
                    self.result_text.value = f"Determinante de B = {self.fraction_to_str(det)}"
                else:
                    self.result_text.value = "Error al calcular el determinante"
                self.page.update()
                return
            elif operation == "inv_a":
                result = self.matrix_ops.calculate_inverse(matrix_a)
            elif operation == "inv_b":
                result = self.matrix_ops.calculate_inverse(matrix_b)
            
            # Mostrar resultados
            self.result_matrix = self.create_matrix_inputs(len(result), result)
            self.result_container.content = self.result_matrix
            self.result_text.value = ""
        except Exception as e:
            self.result_text.value = f"Error: {str(e)}"
        
        self.page.update()

    def show(self):
        # Título de la página
        title = ft.Text(
            "Matrix Calculator",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )

        # Controles para matriz A
        size_dropdown_a = ft.Dropdown(
            width=150,
            text_size=16,
            value="3 × 3",
            options=[
                ft.dropdown.Option("2 × 2"),
                ft.dropdown.Option("3 × 3"),
                ft.dropdown.Option("4 × 4"),
            ],
            on_change=lambda e: self.update_matrix_size(e, "A"),
        )

        # Botones para matriz A
        random_button_a = ft.ElevatedButton(
            text="Aleatorio",
            on_click=lambda _: self.fill_matrix("A", "random"),
            bgcolor=ft.Colors.BLUE_GREY_700,
            color=ft.Colors.WHITE,
        )

        zeros_button_a = ft.ElevatedButton(
            text="Ceros",
            on_click=lambda _: self.fill_matrix("A", "zeros"),
            bgcolor=ft.Colors.BLUE_GREY_700,
            color=ft.Colors.WHITE,
        )
        
        ones_button_a = ft.ElevatedButton(
            text="Unos",
            on_click=lambda _: self.fill_matrix("A", "ones"),
            bgcolor=ft.Colors.BLUE_GREY_700,
            color=ft.Colors.WHITE,
        )

        # Inicializar matriz A
        self.matrix_a_inputs = self.create_matrix_inputs(self.matrix_size_a, np.ones((self.matrix_size_a, self.matrix_size_a)))
        self.matrix_container_a = ft.Container(
            content=self.matrix_a_inputs,
            padding=ft.padding.all(20),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_400),
        )

        # Controles para matriz B
        size_dropdown_b = ft.Dropdown(
            width=150,
            text_size=16,
            value="3 × 3",
            options=[
                ft.dropdown.Option("2 × 2"),
                ft.dropdown.Option("3 × 3"),
                ft.dropdown.Option("4 × 4"),
            ],
            on_change=lambda e: self.update_matrix_size(e, "B"),
        )
        
        # Botones para matriz B
        random_button_b = ft.ElevatedButton(
            text="Aleatorio",
            on_click=lambda _: self.fill_matrix("B", "random"),
            bgcolor=ft.Colors.BLUE_GREY_700,
            color=ft.Colors.WHITE,
        )
        
        zeros_button_b = ft.ElevatedButton(
            text="Ceros",
            on_click=lambda _: self.fill_matrix("B", "zeros"),
            bgcolor=ft.Colors.BLUE_GREY_700,
            color=ft.Colors.WHITE,
        )
        
        ones_button_b = ft.ElevatedButton(
            text="Unos",
            on_click=lambda _: self.fill_matrix("B", "ones"),
            bgcolor=ft.Colors.BLUE_GREY_700,
            color=ft.Colors.WHITE,
        )

        # Inicializar matriz B
        self.matrix_b_inputs = self.create_matrix_inputs(self.matrix_size_b, np.ones((self.matrix_size_b, self.matrix_size_b)))
        self.matrix_container_b = ft.Container(
            content=self.matrix_b_inputs,
            padding=ft.padding.all(20),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_400),
        )

        # Botones de operaciones
        add_button = ft.ElevatedButton(
            text="+",
            on_click=lambda _: self.calculate("+"),
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                padding=ft.padding.all(15),
            ),
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        )
        
        subtract_button = ft.ElevatedButton(
            text="-",
            on_click=lambda _: self.calculate("-"),
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                padding=ft.padding.all(15),
            ),
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        )
        
        multiply_button = ft.ElevatedButton(
            text="×",
            on_click=lambda _: self.calculate("×"),
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                padding=ft.padding.all(15),
            ),
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        )

        # Botones de operaciones adicionales
        matrix_a_ops = ft.Row(
            [
                ft.ElevatedButton(
                    text="Inversa A",
                    on_click=lambda _: self.calculate("inv_a"),
                    bgcolor=ft.Colors.INDIGO_400,
                ),
                ft.ElevatedButton(
                    text="Determinante A",
                    on_click=lambda _: self.calculate("det_a"),
                    bgcolor=ft.Colors.INDIGO_400,
                ),
            ],
        )

        matrix_b_ops = ft.Row(
            [
                ft.ElevatedButton(
                    text="Inversa B",
                    on_click=lambda _: self.calculate("inv_b"),
                    bgcolor=ft.Colors.INDIGO_400,
                ),
                ft.ElevatedButton(
                    text="Determinante B",
                    on_click=lambda _: self.calculate("det_b"),
                    bgcolor=ft.Colors.INDIGO_400,
                ),
            ],
        )

        # Área de resultados
        self.result_text = ft.Text(
            "",
            color=ft.Colors.WHITE,
            size=16,
        )
        
        self.result_container = ft.Container(
            padding=ft.padding.all(20),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_400),
        )

        # Etiqueta de resultados
        result_label = ft.Text(
            "Resultado:",
            color=ft.Colors.WHITE,
            size=20,
            weight=ft.FontWeight.BOLD,
        )

        # Layout de la página
        self.page.controls[0].controls[1].content.controls = [
            ft.Column(
                [
                    ft.Container(
                        padding=ft.padding.only(left=40, top=20, right=40, bottom=10),
                        content=title,
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=40),
                        content=ft.Row(
                            [
                                # Columna matriz A
                                ft.Column(
                                    [
                                        ft.Row(
                                            [size_dropdown_a, random_button_a, zeros_button_a, ones_button_a],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                        self.matrix_container_a,
                                        matrix_a_ops,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                
                                # Columna operaciones
                                ft.Column(
                                    [add_button, subtract_button, multiply_button],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                
                                # Columna matriz B
                                ft.Column(
                                    [
                                        ft.Row(
                                            [size_dropdown_b, random_button_b, zeros_button_b, ones_button_b],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                        self.matrix_container_b,
                                        matrix_b_ops,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ),
                    
                    # Área resultados
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=40, vertical=20),
                        content=ft.Column(
                            [
                                result_label,
                                self.result_text,
                                self.result_container,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        ] 