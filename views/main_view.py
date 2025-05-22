import flet as ft
from views.matrix_view import MatrixView
from views.vector_view import VectorView
from views.equation_view import EquationView
from views.derivative_view import DerivativeView
from views.integral_view import IntegralView
from views.graph2d_view import Graph2DView
from views.graph3d_view import Graph3DView
from views.diff_equation_view import DiffEquationView
from views.diff_system_view import DiffSystemView
from views.population_models_view import PopulationModelsView
from views.random_generator_view import RandomGeneratorView
from views.monte_carlo_view import MonteCarloView
from views.poisson_view import PoissonView

class MainView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_view = None
        self.views = {
            "matrices": MatrixView(page),
            "vectores": VectorView(page),
            "ecuaciones": EquationView(page),
            "derivadas": DerivativeView(page),
            "integrales": IntegralView(page),
            "grafica_2d": Graph2DView(page),
            "grafica_3d": Graph3DView(page),
            "ecuaciones_diferenciales": DiffEquationView(page),
            "sistemas_diferenciales": DiffSystemView(page),
            "modelos_poblacionales": PopulationModelsView(page),
            "generador_aleatorio": RandomGeneratorView(page),
            "monte_carlo": MonteCarloView(page),
            "poisson": PoissonView(page)
        }

    def initialize(self):
        # Título principal
        title = ft.Text(
            "MathCalculator",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )

        # Crear el panel lateral con navegación
        self.nav_items = [
            ft.Container(
                content=ft.Row([
                    ft.Icon(name="grid_view", color=ft.Colors.BLUE_400),
                    ft.Text("Matrices", color=ft.Colors.WHITE, size=16)
                ]),
                padding=ft.padding.all(15),
                border_radius=10,
                bgcolor=ft.Colors.BLUE_600,
                on_click=lambda e: self.navigate("matrices"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Icon(name="arrow_forward"),
                    ft.Text("Vectores", color=ft.Colors.WHITE, size=16)
                ]),
                padding=ft.padding.all(15),
                border_radius=10,
                on_click=lambda e: self.navigate("vectores"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Icon(name="functions"),
                    ft.Text("Ecuaciones", color=ft.Colors.WHITE, size=16)
                ]),
                padding=ft.padding.all(15),
                border_radius=10,
                on_click=lambda e: self.navigate("ecuaciones"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Icon(name="integration_instructions"),
                    ft.Text("Integrales", color=ft.Colors.WHITE, size=16)
                ]),
                padding=ft.padding.all(15),
                border_radius=10,
                on_click=lambda e: self.navigate("integrales"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Icon(name="show_chart"),
                    ft.Text("Derivadas", color=ft.Colors.WHITE, size=16)
                ]),
                padding=ft.padding.all(15),
                border_radius=10,
                on_click=lambda e: self.navigate("derivadas"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Icon(name="stacked_line_chart"),
                    ft.Text("Gráficas 2D", color=ft.Colors.WHITE, size=16)
                ]),
                padding=ft.padding.all(15),
                border_radius=10,
                on_click=lambda e: self.navigate("grafica_2d"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Icon(name="view_in_ar"),
                    ft.Text("Gráficas 3D", color=ft.Colors.WHITE, size=16)
                ]),
                padding=ft.padding.all(15),
                border_radius=10,
                on_click=lambda e: self.navigate("grafica_3d"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Icon(name="analytics", color=ft.Colors.BLUE_400),
                    ft.Text("Ecuaciones Diferenciales", color=ft.Colors.WHITE, size=16)
                ]),
                padding=ft.padding.all(15),
                border_radius=10,
                on_click=lambda e: self.navigate("ecuaciones_diferenciales"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Icon(name="analytics", color=ft.Colors.BLUE_400),
                    ft.Text("Sistemas Diferenciales", color=ft.Colors.WHITE, size=16)
                ]),
                padding=ft.padding.all(15),
                border_radius=10,
                on_click=lambda e: self.navigate("sistemas_diferenciales"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Icon(name="trending_up", color=ft.Colors.BLUE_400),
                    ft.Text("Modelos Poblacionales", color=ft.Colors.WHITE, size=16)
                ]),
                padding=ft.padding.all(15),
                border_radius=10,
                on_click=lambda e: self.navigate("modelos_poblacionales"),
            ),
            # Separador visual
            ft.Container(
                content=ft.Divider(color=ft.Colors.BLUE_400),
                padding=ft.padding.symmetric(vertical=10),
            ),
            # Sección de métodos numéricos
            ft.Container(
                content=ft.Text(
                    "Métodos Numéricos",
                    color=ft.Colors.BLUE_400,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                padding=ft.padding.only(left=15, bottom=5),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Icon(name="shuffle", color=ft.Colors.BLUE_400),
                    ft.Text("Generador Aleatorio", color=ft.Colors.WHITE, size=16)
                ]),
                padding=ft.padding.all(15),
                border_radius=10,
                on_click=lambda e: self.navigate("generador_aleatorio"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Icon(name="casino", color=ft.Colors.BLUE_400),
                    ft.Text("Método de Monte Carlo", color=ft.Colors.WHITE, size=16)
                ]),
                padding=ft.padding.all(15),
                border_radius=10,
                on_click=lambda e: self.navigate("monte_carlo"),
            ),
            ft.Container(
                content=ft.Row([
                    ft.Icon(name="analytics", color=ft.Colors.BLUE_400),
                    ft.Text("Distribución de Poisson", color=ft.Colors.WHITE, size=16)
                ]),
                padding=ft.padding.all(15),
                border_radius=10,
                on_click=lambda e: self.navigate("poisson"),
            ),
        ]

        # Panel de navegación (Sidebar fijo que no se desplaza)
        self.side_panel = ft.Container(
            width=300,
            bgcolor=ft.Colors.BLUE_GREY_900,
            padding=ft.padding.all(15),
            content=ft.Column(
                [
                    title,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    *self.nav_items
                ],
                spacing=10,
                scroll=ft.ScrollMode.ALWAYS
            ),
            height=self.page.window_height,  # Altura fija igual a la ventana
        )

        # Área de contenido con soporte de scroll
        self.content_area = ft.Container(
            expand=True,
            bgcolor=ft.Colors.BLACK,
            content=ft.Column(
                [],
                expand=True,
                scroll=ft.ScrollMode.AUTO  # Habilitar el scroll vertical
            ),
        )

        # Layout principal como Stack para mantener el sidebar fijo
        main_layout = ft.Row(
            [
                self.side_panel,
                self.content_area
            ],
            expand=True,
            scroll=None  # Deshabilitar scroll en el Row principal
        )
        
        # Añadir el layout principal
        self.page.add(main_layout)

        # Ajustar sidebar cuando cambia el tamaño de la ventana
        def on_resize(e):
            self.side_panel.height = self.page.window_height
            self.page.update()
            
        self.page.on_resize = on_resize
        
        # Iniciar con la vista de matrices
        self.navigate("matrices")

    def navigate(self, view_name):
        # Actualizar estilo de navegación
        for item in self.nav_items:
            # Verificar si el item es un contenedor de navegación (tiene Row con controles)
            if isinstance(item.content, ft.Row) and len(item.content.controls) > 1:
                if view_name in item.content.controls[1].value.lower():
                    item.bgcolor = ft.Colors.BLUE_600
                else:
                    item.bgcolor = None

        # Mostrar vista si existe
        if view_name in self.views:
            # Limpiar el contenido actual
            self.content_area.content.controls = []
            # Agregar la nueva vista
            self.views[view_name].show()
            # Asegurar que se está en la parte superior de la vista
            self.page.scroll_to(offset=0, duration=300)
            self.page.update() 