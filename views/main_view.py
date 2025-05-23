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
        
        # Inicializar todas las vistas
        self.derivative_view = DerivativeView(page)
        self.vector_view = VectorView(page)
        self.matrix_view = MatrixView(page)
        self.diff_system_view = DiffSystemView(page)
        self.monte_carlo_view = MonteCarloView(page)
        self.equation_view = EquationView(page)
        self.integral_view = IntegralView(page)
        self.graph2d_view = Graph2DView(page)
        self.graph3d_view = Graph3DView(page)
        self.diff_equation_view = DiffEquationView(page)
        self.population_models_view = PopulationModelsView(page)
        self.random_generator_view = RandomGeneratorView(page)
        self.poisson_view = PoissonView(page)
        
        # Diccionario de vistas
        self.views = {
            "matrices": self.matrix_view,
            "vectores": self.vector_view,
            "ecuaciones": self.equation_view,
            "integrales": self.integral_view,
            "derivadas": self.derivative_view,
            "grafica_2d": self.graph2d_view,
            "grafica_3d": self.graph3d_view,
            "ecuaciones_diferenciales": self.diff_equation_view,
            "sistemas_diferenciales": self.diff_system_view,
            "modelos_poblacionales": self.population_models_view,
            "generador_aleatorio": self.random_generator_view,
            "monte_carlo": self.monte_carlo_view,
            "poisson": self.poisson_view
        }
        
        self.navigation_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(name="calculate"),
                    label="Derivadas",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(name="arrow_forward"),
                    label="Vectores",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(name="grid_4x4"),
                    label="Matrices",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(name="trending_up"),
                    label="Sistemas Diferenciales",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(name="casino"),
                    label="Monte Carlo",
                ),
            ],
            on_change=self.change_view,
        )
        
        self.view = ft.Row(
            [
                self.navigation_rail,
                ft.VerticalDivider(width=1),
                ft.Column(
                    [
                        ft.Container(
                            content=self.derivative_view.view,
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )
    
    def change_view(self, e):
        index = e.control.selected_index
        if index == 0:
            self.current_view = self.derivative_view
        elif index == 1:
            self.current_view = self.vector_view
        elif index == 2:
            self.current_view = self.matrix_view
        elif index == 3:
            self.current_view = self.diff_system_view
        elif index == 4:
            self.current_view = self.monte_carlo_view
        
        self.view.controls[2].content.controls[0].content = self.current_view.view
        self.page.update()

    def initialize(self):
        title = ft.Text(
            "MathCalculator",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )

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
            ft.Container(
                content=ft.Divider(color=ft.Colors.BLUE_400),
                padding=ft.padding.symmetric(vertical=10),
            ),
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
            height=self.page.window_height,
        )

        self.content_area = ft.Container(
            expand=True,
            bgcolor=ft.Colors.BLACK,
            content=ft.Column(
                [],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            ),
        )

        main_layout = ft.Row(
            [
                self.side_panel,
                self.content_area
            ],
            expand=True,
            scroll=None
        )
        
        self.page.add(main_layout)

        def on_resize(e):
            self.side_panel.height = self.page.window_height
            self.page.update()
            
        self.page.on_resize = on_resize
        
        self.navigate("matrices")

    def navigate(self, view_name):
        for item in self.nav_items:
            if isinstance(item.content, ft.Row) and len(item.content.controls) > 1:
                if view_name in item.content.controls[1].value.lower():
                    item.bgcolor = ft.Colors.BLUE_600
                else:
                    item.bgcolor = None

        if view_name in self.views:
            self.content_area.content.controls = []
            self.views[view_name].show()
            self.page.scroll_to(offset=0, duration=300)
            self.page.update() 