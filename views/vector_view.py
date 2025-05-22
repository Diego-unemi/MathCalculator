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
        
        self.vector_a_input = ft.TextField(
            label="Vector A",
            width=300,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
        )
        
        self.vector_b_input = ft.TextField(
            label="Vector B",
            width=300,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
        )
        
        self.operation_selector = ft.Dropdown(
            label="Operación",
            width=200,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
                    color=ft.Colors.WHITE,
            options=[
                ft.dropdown.Option("Suma"),
                ft.dropdown.Option("Resta"),
                ft.dropdown.Option("Producto Escalar"),
                ft.dropdown.Option("Producto Vectorial"),
                ft.dropdown.Option("Magnitud"),
                ft.dropdown.Option("Vector Unitario"),
                ft.dropdown.Option("Ángulo entre Vectores"),
            ],
            value="Suma",
        )
        
        self.result_display = ft.Container(
            width=650,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            border_radius=10,
            bgcolor=ft.Colors.BLACK,
            padding=10,
            content=ft.Text(
                "Ingrese los vectores y seleccione una operación",
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
            on_click=self.calculate_operation,
            bgcolor=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
        )
        
        self.view = ft.Column([
            ft.Text("Operaciones con Vectores", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Text(
                "Realiza operaciones básicas con vectores: suma, resta, productos escalar y vectorial, magnitud, vector unitario y ángulo entre vectores.",
                color=ft.Colors.WHITE70,
                size=16,
            ),
            ft.Container(height=20),
            ft.Row([
                self.vector_a_input,
                self.vector_b_input,
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=20),
            ft.Row([
                self.operation_selector,
                self.calculate_button,
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=20),
            self.result_display,
            self.message_display,
        ])
    
    def calculate_operation(self, e):
        try:
            operation = self.operation_selector.value
            
            if operation in ["Magnitud", "Vector Unitario"]:
                vector_a = self.vector_ops.parse_vector(self.vector_a_input.value)
                vector_b = None
            else:
                vector_a = self.vector_ops.parse_vector(self.vector_a_input.value)
                vector_b = self.vector_ops.parse_vector(self.vector_b_input.value)
            
            result = None
            if operation == "Suma":
                result = self.vector_ops.add_vectors(vector_a, vector_b)
                content = ft.Column([
                    ft.Text("Resultado:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"A + B = {result}", size=20, color=ft.Colors.WHITE),
                ])
            elif operation == "Resta":
                result = self.vector_ops.subtract_vectors(vector_a, vector_b)
                content = ft.Column([
                    ft.Text("Resultado:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"A - B = {result}", size=20, color=ft.Colors.WHITE),
                ])
            elif operation == "Producto Escalar":
                result = self.vector_ops.dot_product(vector_a, vector_b)
                content = ft.Column([
                    ft.Text("Resultado:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"A · B = {result}", size=20, color=ft.Colors.WHITE),
                ])
            elif operation == "Producto Vectorial":
                result = self.vector_ops.cross_product(vector_a, vector_b)
                content = ft.Column([
                    ft.Text("Resultado:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"A × B = {result}", size=20, color=ft.Colors.WHITE),
                ])
            elif operation == "Magnitud":
                result = self.vector_ops.vector_magnitude(vector_a)
                content = ft.Column([
                    ft.Text("Resultado:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"|A| = {result}", size=20, color=ft.Colors.WHITE),
                ])
            elif operation == "Vector Unitario":
                result = self.vector_ops.unit_vector(vector_a)
                content = ft.Column([
                    ft.Text("Resultado:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"û = {result}", size=20, color=ft.Colors.WHITE),
                ])
            elif operation == "Ángulo entre Vectores":
                result = self.vector_ops.angle_between_vectors(vector_a, vector_b)
                content = ft.Column([
                    ft.Text("Resultado:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"θ = {result:.4f} radianes", size=20, color=ft.Colors.WHITE),
                    ft.Text(f"θ = {np.degrees(result):.4f} grados", size=20, color=ft.Colors.WHITE),
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