import flet as ft
import numpy as np
from core.vector_operations import VectorOperations
import math

class VectorView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.vector_ops = VectorOperations()
        self.dimensions = ["2D", "3D"]
        self.current_dimension = "3D"
        
    def show(self):
        # Título de la página
        title = ft.Text(
            "Vector Calculator",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )
        
        # Selector de dimensiones
        dimension_selector = ft.Dropdown(
            width=100,
            text_size=16,
            value=self.current_dimension,
            options=[
                ft.dropdown.Option(dim) for dim in self.dimensions
            ],
            on_change=self.change_dimension,
        )
        
        # Campos para los vectores
        vector_a_label = ft.Text("Vector A:", color=ft.Colors.WHITE, size=16)
        self.vector_a_input = ft.TextField(
            value="1, 2, 3",
            width=300,
            bgcolor=ft.Colors.WHITE10,
            color=ft.Colors.WHITE,
            border_radius=10,
            hint_text="Ej: 1, 2, 3",
            border=ft.border.all(1, ft.Colors.BLUE_200),
        )
        
        vector_b_label = ft.Text("Vector B:", color=ft.Colors.WHITE, size=16)
        self.vector_b_input = ft.TextField(
            value="4, 5, 6",
            width=300,
            bgcolor=ft.Colors.WHITE10,
            color=ft.Colors.WHITE,
            border_radius=10,
            hint_text="Ej: 4, 5, 6",
            border=ft.border.all(1, ft.Colors.BLUE_200),
        )
        
        # Botones para operaciones básicas
        operations_row = ft.Row(
            [
                ft.ElevatedButton(
                    text="A + B",
                    on_click=lambda _: self.calculate_operation("add"),
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                ),
                ft.ElevatedButton(
                    text="A - B",
                    on_click=lambda _: self.calculate_operation("subtract"),
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                ),
                ft.ElevatedButton(
                    text="A · B",
                    tooltip="Producto Escalar",
                    on_click=lambda _: self.calculate_operation("dot"),
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                ),
                ft.ElevatedButton(
                    text="A × B",
                    tooltip="Producto Vectorial (Solo 3D)",
                    on_click=lambda _: self.calculate_operation("cross"),
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        # Botones para operaciones avanzadas
        advanced_operations_row = ft.Row(
            [
                ft.ElevatedButton(
                    text="|A|",
                    tooltip="Magnitud del vector A",
                    on_click=lambda _: self.calculate_operation("mag_a"),
                    bgcolor=ft.Colors.INDIGO_400,
                    color=ft.Colors.WHITE,
                ),
                ft.ElevatedButton(
                    text="|B|",
                    tooltip="Magnitud del vector B",
                    on_click=lambda _: self.calculate_operation("mag_b"),
                    bgcolor=ft.Colors.INDIGO_400,
                    color=ft.Colors.WHITE,
                ),
                ft.ElevatedButton(
                    text="Â",
                    tooltip="Vector unitario de A",
                    on_click=lambda _: self.calculate_operation("unit_a"),
                    bgcolor=ft.Colors.INDIGO_400,
                    color=ft.Colors.WHITE,
                ),
                ft.ElevatedButton(
                    text="B̂",
                    tooltip="Vector unitario de B",
                    on_click=lambda _: self.calculate_operation("unit_b"),
                    bgcolor=ft.Colors.INDIGO_400,
                    color=ft.Colors.WHITE,
                ),
                ft.ElevatedButton(
                    text="∠(A,B)",
                    tooltip="Ángulo entre vectores",
                    on_click=lambda _: self.calculate_operation("angle"),
                    bgcolor=ft.Colors.INDIGO_400,
                    color=ft.Colors.WHITE,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        # Botones para valores rápidos
        quick_values_a = ft.Row(
            [
                ft.Text("Vector A: ", color=ft.Colors.WHITE),
                ft.ElevatedButton(
                    text="i",
                    on_click=lambda _: self.set_quick_vector("A", "i"),
                    bgcolor=ft.Colors.BLUE_GREY_700,
                ),
                ft.ElevatedButton(
                    text="j",
                    on_click=lambda _: self.set_quick_vector("A", "j"),
                    bgcolor=ft.Colors.BLUE_GREY_700,
                ),
                ft.ElevatedButton(
                    text="k",
                    on_click=lambda _: self.set_quick_vector("A", "k"),
                    bgcolor=ft.Colors.BLUE_GREY_700,
                ),
                ft.ElevatedButton(
                    text="Zeros",
                    on_click=lambda _: self.set_quick_vector("A", "zeros"),
                    bgcolor=ft.Colors.BLUE_GREY_700,
                ),
                ft.ElevatedButton(
                    text="Random",
                    on_click=lambda _: self.set_quick_vector("A", "random"),
                    bgcolor=ft.Colors.BLUE_GREY_700,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        quick_values_b = ft.Row(
            [
                ft.Text("Vector B: ", color=ft.Colors.WHITE),
                ft.ElevatedButton(
                    text="i",
                    on_click=lambda _: self.set_quick_vector("B", "i"),
                    bgcolor=ft.Colors.BLUE_GREY_700,
                ),
                ft.ElevatedButton(
                    text="j",
                    on_click=lambda _: self.set_quick_vector("B", "j"),
                    bgcolor=ft.Colors.BLUE_GREY_700,
                ),
                ft.ElevatedButton(
                    text="k",
                    on_click=lambda _: self.set_quick_vector("B", "k"),
                    bgcolor=ft.Colors.BLUE_GREY_700,
                ),
                ft.ElevatedButton(
                    text="Zeros",
                    on_click=lambda _: self.set_quick_vector("B", "zeros"),
                    bgcolor=ft.Colors.BLUE_GREY_700,
                ),
                ft.ElevatedButton(
                    text="Random",
                    on_click=lambda _: self.set_quick_vector("B", "random"),
                    bgcolor=ft.Colors.BLUE_GREY_700,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        # Área de resultados
        result_label = ft.Text(
            "Resultado:",
            color=ft.Colors.WHITE,
            size=20,
            weight=ft.FontWeight.BOLD,
        )
        
        self.result_text = ft.Text(
            "",
            color=ft.Colors.WHITE,
            size=16,
        )
        
        result_container = ft.Container(
            content=self.result_text,
            padding=ft.padding.all(20),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            width=600,
            height=150,
        )
        
        # Layout principal
        self.page.controls[0].controls[1].content.controls = [
            ft.Column(
                [
                    # Título y selector de dimensiones
                    ft.Container(
                        padding=ft.padding.only(left=40, top=20, right=40, bottom=10),
                        content=ft.Row(
                            [title, dimension_selector],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ),
                    
                    # Inputs de vectores
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=40, vertical=10),
                        content=ft.Column(
                            [
                                ft.Row(
                                    [vector_a_label, self.vector_a_input],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                quick_values_a,
                                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                                ft.Row(
                                    [vector_b_label, self.vector_b_input],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                quick_values_b,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                    ),
                    
                    # Operaciones
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=40, vertical=10),
                        content=ft.Column(
                            [operations_row, advanced_operations_row],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                    ),
                    
                    # Resultados
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=40, vertical=20),
                        content=ft.Column(
                            [
                                result_label,
                                result_container,
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
    
    def change_dimension(self, e):
        self.current_dimension = e.control.value
        
        # Ajustar los valores de los vectores según la dimensión
        if self.current_dimension == "2D":
            # Si es 2D, asegurarse de que solo tengan 2 componentes
            try:
                vec_a = self.vector_ops.parse_vector(self.vector_a_input.value)
                vec_b = self.vector_ops.parse_vector(self.vector_b_input.value)
                
                if len(vec_a) > 2:
                    self.vector_a_input.value = f"{vec_a[0]}, {vec_a[1]}"
                if len(vec_b) > 2:
                    self.vector_b_input.value = f"{vec_b[0]}, {vec_b[1]}"
            except:
                # Si hay error en el parseo, establecer valores por defecto
                self.vector_a_input.value = "1, 2"
                self.vector_b_input.value = "3, 4"
        else:
            # Si es 3D, asegurarse de que tengan 3 componentes
            try:
                vec_a = self.vector_ops.parse_vector(self.vector_a_input.value)
                vec_b = self.vector_ops.parse_vector(self.vector_b_input.value)
                
                if len(vec_a) < 3:
                    self.vector_a_input.value = f"{vec_a[0]}, {vec_a[1]}, 0"
                if len(vec_b) < 3:
                    self.vector_b_input.value = f"{vec_b[0]}, {vec_b[1]}, 0"
            except:
                # Si hay error en el parseo, establecer valores por defecto
                self.vector_a_input.value = "1, 2, 3"
                self.vector_b_input.value = "4, 5, 6"
                
        self.page.update()
    
    def set_quick_vector(self, vector_label, preset):
        dimension = 3 if self.current_dimension == "3D" else 2
        
        if preset == "i":
            value = "1, 0" if dimension == 2 else "1, 0, 0"
        elif preset == "j":
            value = "0, 1" if dimension == 2 else "0, 1, 0"
        elif preset == "k":
            value = "0, 0, 1" if dimension == 3 else "0, 1"
        elif preset == "zeros":
            value = "0, 0" if dimension == 2 else "0, 0, 0"
        elif preset == "random":
            if dimension == 2:
                value = f"{np.random.randint(-10, 10)}, {np.random.randint(-10, 10)}"
            else:
                value = f"{np.random.randint(-10, 10)}, {np.random.randint(-10, 10)}, {np.random.randint(-10, 10)}"
        
        if vector_label == "A":
            self.vector_a_input.value = value
        else:
            self.vector_b_input.value = value
            
        self.page.update()
    
    def vector_to_str(self, vector):
        """Convierte un vector numpy a su representación en notación matemática"""
        if isinstance(vector, (int, float)):
            return str(vector)
            
        components = []
        for x in vector:
            if isinstance(x, int) or x.is_integer():
                components.append(str(int(x)))
            else:
                components.append(f"{x:.4f}")
                
        if len(vector) <= 3:
            # Para vectores 2D y 3D, usar notación (x, y, z)
            return f"({', '.join(components)})"
        else:
            # Para dimensiones mayores, usar notación [x, y, z, ...]
            return f"[{', '.join(components)}]"
    
    def calculate_operation(self, operation):
        try:
            vec_a = self.vector_ops.parse_vector(self.vector_a_input.value)
            vec_b = self.vector_ops.parse_vector(self.vector_b_input.value)
            
            if operation == "add":
                result = self.vector_ops.add_vectors(vec_a, vec_b)
                self.result_text.value = f"A + B = {self.vector_to_str(result)}"
            
            elif operation == "subtract":
                result = self.vector_ops.subtract_vectors(vec_a, vec_b)
                self.result_text.value = f"A - B = {self.vector_to_str(result)}"
            
            elif operation == "dot":
                result = self.vector_ops.dot_product(vec_a, vec_b)
                self.result_text.value = f"A · B = {result}"
            
            elif operation == "cross":
                if self.current_dimension != "3D":
                    self.result_text.value = "El producto vectorial solo está definido para vectores 3D"
                else:
                    result = self.vector_ops.cross_product(vec_a, vec_b)
                    self.result_text.value = f"A × B = {self.vector_to_str(result)}"
            
            elif operation == "mag_a":
                result = self.vector_ops.vector_magnitude(vec_a)
                self.result_text.value = f"|A| = {result:.4f}"
            
            elif operation == "mag_b":
                result = self.vector_ops.vector_magnitude(vec_b)
                self.result_text.value = f"|B| = {result:.4f}"
            
            elif operation == "unit_a":
                result = self.vector_ops.unit_vector(vec_a)
                self.result_text.value = f"Â = {self.vector_to_str(result)}"
            
            elif operation == "unit_b":
                result = self.vector_ops.unit_vector(vec_b)
                self.result_text.value = f"B̂ = {self.vector_to_str(result)}"
            
            elif operation == "angle":
                result_rad = self.vector_ops.angle_between_vectors(vec_a, vec_b)
                result_deg = result_rad * 180 / math.pi
                self.result_text.value = f"Ángulo entre A y B: {result_rad:.4f} radianes ({result_deg:.2f}°)"
        
        except Exception as e:
            self.result_text.value = f"Error: {str(e)}"
            
        self.page.update() 