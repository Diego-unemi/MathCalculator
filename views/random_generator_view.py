import flet as ft
from utils.random_generator import CongruentialGenerator

class RandomGeneratorView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.generator = CongruentialGenerator()
        
        # Campos de entrada
        self.seed_input = ft.TextField(
            label="Semilla inicial",
            value="12345",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=150,
            text_size=16,
        )
        
        self.a_input = ft.TextField(
            label="Multiplicador (a)",
            value="1664525",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=150,
            text_size=16,
        )
        
        self.c_input = ft.TextField(
            label="Incremento (c)",
            value="1013904223",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=150,
            text_size=16,
        )
        
        self.m_input = ft.TextField(
            label="Módulo (m)",
            value="4294967296",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=150,
            text_size=16,
        )
        
        self.n_input = ft.TextField(
            label="Cantidad de números",
            value="10",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            width=150,
            text_size=16,
        )
        
        # Contenedor para resultados
        self.result_container = ft.Container(
            content=ft.Column([], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.all(20),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_400),
            width=600,
            height=200,
        )
        
    def generate_numbers(self, e):
        try:
            # Obtener valores de los campos
            seed = int(self.seed_input.value)
            a = int(self.a_input.value)
            c = int(self.c_input.value)
            m = int(self.m_input.value)
            n = int(self.n_input.value)
            
            # Crear nuevo generador con los parámetros
            self.generator = CongruentialGenerator(seed=seed, a=a, c=c, m=m)
            
            # Generar números
            numbers = self.generator.generate_sequence(n)
            
            # Mostrar resultados
            result_text = ft.Text(
                f"Números generados:\n{', '.join([f'{x:.6f}' for x in numbers])}",
                color=ft.Colors.WHITE,
                size=16,
            )
            
            self.result_container.content = result_text
            self.page.update()
            
        except ValueError as e:
            self.result_container.content = ft.Text(
                f"Error: Por favor ingrese valores numéricos válidos.\n{str(e)}",
                color=ft.Colors.RED,
                size=16,
            )
            self.page.update()
    
    def show(self):
        # Título de la página
        title = ft.Text(
            "Generador Congruencial Lineal",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )
        
        # Botón de generar
        generate_button = ft.ElevatedButton(
            text="Generar números",
            on_click=self.generate_numbers,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            width=150,
            height=45,
        )
        
        # Layout principal
        self.page.controls[0].controls[1].content.controls = [
            ft.Column(
                [
                    # Título
                    ft.Container(
                        padding=ft.padding.only(left=40, top=20, right=40, bottom=20),
                        content=ft.Row(
                            [title],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ),
                    
                    # Panel de configuración
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=40, vertical=10),
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Configuración del generador:",
                                    color=ft.Colors.WHITE,
                                    size=16,
                                ),
                                ft.Row(
                                    [self.seed_input, self.a_input],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20,
                                ),
                                ft.Row(
                                    [self.c_input, self.m_input],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20,
                                ),
                                ft.Row(
                                    [self.n_input],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Container(
                                    content=generate_button,
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