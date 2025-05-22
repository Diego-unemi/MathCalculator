import flet as ft
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class PopulationModelsView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.title = "Modelo de Crecimiento Poblacional de Aedes aegypti"
        # Contenedores para gráfica y resumen
        self.plot = ft.Image(
            width=600,
            height=400,
            fit=ft.ImageFit.CONTAIN,
            src_base64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
        )
        self.plot_container = ft.Container(
            content=self.plot,
            padding=10,
            bgcolor=ft.Colors.BLACK87,
            border_radius=8,
            alignment=ft.alignment.center,
        )
        self.resumen_container = ft.Container(
            content=ft.Text(""),
            padding=0,
            bgcolor=ft.Colors.BLACK87,
            border_radius=8,
            alignment=ft.alignment.center,
        )

    def show(self):
        # Campos de entrada
        self.n0_input = ft.TextField(
            label="Población inicial de mosquitos (N₀)",
            value="100",
            width=200,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            hint_text="Ej: 100",
            helper_text="Número inicial de mosquitos"
        )
        self.r_input = ft.TextField(
            label="Tasa de crecimiento (r)",
            value="0.1",
            width=200,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            hint_text="Ej: 0.1",
            helper_text="Tasa de crecimiento por día"
        )
        self.k_input = ft.TextField(
            label="Capacidad de carga (K)",
            value="1000",
            width=200,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            hint_text="Ej: 1000",
            helper_text="Número máximo de mosquitos sostenibles"
        )
        self.t_input = ft.TextField(
            label="Tiempo final (días)",
            value="50",
            width=200,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            hint_text="Ej: 50",
            helper_text="Período de simulación en días"
        )
        self.mu_input = ft.TextField(
            label="Mortalidad natural (μ)",
            value="0.01",
            width=200,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            hint_text="Ej: 0.01",
            helper_text="Tasa de muerte natural por día"
        )
        self.c_input = ft.TextField(
            label="Eficiencia de control (c)",
            value="0.0",
            width=200,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            hint_text="Ej: 0.0",
            helper_text="Tasa de reducción por control"
        )
        self.A_input = ft.TextField(
            label="Amplitud estacional (A)",
            value="0.0",
            width=200,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            hint_text="Ej: 0.0",
            helper_text="0 = sin estacionalidad"
        )
        self.T_input = ft.TextField(
            label="Periodo estacional (T, días)",
            value="365",
            width=200,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            hint_text="Ej: 365",
            helper_text="Días en un año"
        )

        # Botón de cálculo
        self.calculate_button = ft.ElevatedButton(
            "Calcular",
            on_click=self.calculate_growth,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            width=200,
            height=45,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )

        # Resultados
        self.results = ft.Text(
            color=ft.Colors.WHITE,
            size=16,
            value="Ingrese los parámetros y presione 'Calcular' para ver los resultados."
        )

        # Tarjeta de parámetros
        parametros_card = ft.Container(
            content=ft.Column([
                ft.Text("Modelo de Crecimiento Poblacional de Aedes aegypti", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400, text_align=ft.TextAlign.CENTER),
                ft.Text("Parámetros del Modelo", color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.BOLD),
                ft.Column([
                    self.n0_input,
                    self.r_input,
                    self.k_input,
                    self.mu_input,
                    self.c_input,
                    self.A_input,
                    self.T_input,
                    self.t_input,
                ], spacing=12),
                ft.Container(
                    content=self.calculate_button,
                    padding=10,
                    alignment=ft.alignment.center,
                ),
            ], spacing=18, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=24,
            border=ft.border.all(1, ft.Colors.BLUE_100),
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=16, color=ft.Colors.BLUE_100, offset=ft.Offset(0, 6)),
            bgcolor=ft.Colors.BLACK87,
            width=380,
            alignment=ft.alignment.center,
        )

        # Panel de gráfica
        panel_grafica = ft.Container(
            content=ft.Column([
                ft.Text("Gráfica de la Simulación", color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.BOLD),
                self.plot_container,
            ], spacing=18, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=24,
            border=ft.border.all(1, ft.Colors.BLUE_100),
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=16, color=ft.Colors.BLUE_100, offset=ft.Offset(0, 6)),
            bgcolor=ft.Colors.BLACK87,
            expand=True,
            alignment=ft.alignment.center,
        )

        # Panel de resumen visual (tarjetitas)
        panel_resumen = ft.Container(
            content=ft.Column([
                ft.Text("Resumen de la Simulación", color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.BOLD),
                self.resumen_container,
            ], spacing=18, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=24,
            border=ft.border.all(1, ft.Colors.BLUE_100),
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=16, color=ft.Colors.BLUE_100, offset=ft.Offset(0, 6)),
            bgcolor=ft.Colors.BLACK87,
            expand=True,
            alignment=ft.alignment.center,
        )

        # Layout principal
        main_content = ft.Row([
            parametros_card,
            ft.Column([
                panel_grafica,
                panel_resumen
            ], spacing=40, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        ], spacing=40, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START, expand=True)

        # Establecer el contenido
        self.page.controls[0].controls[1].content.controls = [main_content]
        self.page.update()

    def calculate_growth(self, e):
        try:
            N0 = float(self.n0_input.value)
            r = float(self.r_input.value)
            K = float(self.k_input.value)
            mu = float(self.mu_input.value)
            c = float(self.c_input.value)
            A = float(self.A_input.value)
            T = float(self.T_input.value)
            t_final = float(self.t_input.value)
            t = np.linspace(0, t_final, 1000)
            dt = t[1] - t[0]
            N = np.zeros_like(t)
            N[0] = N0
            for i in range(1, len(t)):
                r_est = r * (1 + A * np.sin(2 * np.pi * t[i-1] / T))
                dNdt = r_est * N[i-1] * (1 - N[i-1]/K) - mu*N[i-1] - c*N[i-1]
                N[i] = max(N[i-1] + dNdt * dt, 0)
            plt.figure(figsize=(8, 6), facecolor='#212121')
            plt.plot(t, N, 'b-', label='Población de mosquitos', linewidth=2)
            plt.axhline(y=K, color='r', linestyle='--', label='Capacidad de carga')
            plt.xlabel('Tiempo (días)', color='white', fontsize=12)
            plt.ylabel('Población de mosquitos', color='white', fontsize=12)
            plt.title('Crecimiento Poblacional de Aedes aegypti', color='white', fontsize=14)
            plt.grid(True, alpha=0.3)
            plt.legend(facecolor='#303030', edgecolor='white', labelcolor='white')
            plt.gca().set_facecolor('#303030')
            plt.gca().tick_params(colors='white')
            plt.gca().spines['bottom'].set_color('white')
            plt.gca().spines['top'].set_color('white')
            plt.gca().spines['left'].set_color('white')
            plt.gca().spines['right'].set_color('white')
            buf = BytesIO()
            plt.savefig(buf, format='png', facecolor='#212121', bbox_inches='tight', dpi=100)
            buf.seek(0)
            plt.close()
            self.plot.src_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            t_90 = t[np.where(N >= 0.9*K)[0][0]] if np.any(N >= 0.9*K) else float('inf')
            # Panel de resumen visual por tarjetas
            resumen = ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Text("Parámetros del modelo", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                        ft.Text(f"Población inicial (N₀): {N0}", color=ft.Colors.WHITE),
                        ft.Text(f"Tasa de crecimiento (r): {r}", color=ft.Colors.WHITE),
                        ft.Text(f"Capacidad de carga (K): {K}", color=ft.Colors.WHITE),
                        ft.Text(f"Mortalidad natural (μ): {mu}", color=ft.Colors.WHITE),
                        ft.Text(f"Eficiencia de control (c): {c}", color=ft.Colors.WHITE),
                        ft.Text(f"Estacionalidad: A={A}, T={T} días", color=ft.Colors.WHITE),
                    ], spacing=2),
                    bgcolor=ft.Colors.BLACK87,
                    border=ft.border.all(1, ft.Colors.BLUE_100),
                    border_radius=8,
                    padding=10,
                    margin=ft.margin.only(bottom=8)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Resultados numéricos", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
                        ft.Text(f"Población final: {N[-1]:.2f} mosquitos", color=ft.Colors.WHITE),
                        ft.Text(f"Tiempo para 90% de K: {t_90:.2f} días", color=ft.Colors.WHITE),
                        ft.Text(f"Máximo alcanzado: {np.max(N):.2f} mosquitos", color=ft.Colors.WHITE),
                    ], spacing=2),
                    bgcolor=ft.Colors.BLACK87,
                    border=ft.border.all(1, ft.Colors.GREEN_100),
                    border_radius=8,
                    padding=10,
                    margin=ft.margin.only(bottom=8)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Interpretación biológica", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_400),
                        ft.Text(
                            "El modelo simula el crecimiento poblacional de Aedes aegypti considerando capacidad de carga, mortalidad, control y estacionalidad. "
                            "El control y la mortalidad reducen la población, mientras que la estacionalidad puede causar oscilaciones anuales.",
                            color=ft.Colors.WHITE70,
                            size=14
                        ),
                    ]),
                    bgcolor=ft.Colors.BLACK87,
                    border=ft.border.all(1, ft.Colors.YELLOW_100),
                    border_radius=8,
                    padding=10,
                    margin=ft.margin.only(bottom=8)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Referencia", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200),
                        ft.Text(
                            "Un modelo de crecimiento poblacional de Aedes aegypti con capacidad de carga Logística. Rev. Mat [online]. 2018, vol.25, n.1",
                            color=ft.Colors.WHITE60,
                            size=13
                        ),
                        ft.Text(
                            "https://www.scielo.sa.cr/pdf/rmta/v25n1/1409-2433-rmta-25-01-79.pdf",
                            color=ft.Colors.BLUE_200,
                            size=13,
                            selectable=True
                        )
                    ]),
                    bgcolor=ft.Colors.BLACK87,
                    border=ft.border.all(1, ft.Colors.BLUE_100),
                    border_radius=8,
                    padding=10
                )
            ], spacing=0)
            self.plot_container.content = self.plot
            self.resumen_container.content = resumen
            self.page.update()
        except Exception as ex:
            error_card = ft.Container(
                content=ft.Text(f"Error: {str(ex)}", color=ft.Colors.RED_200, size=15),
                bgcolor=ft.Colors.BLACK87,
                border=ft.border.all(1, ft.Colors.RED_200),
                border_radius=8,
                padding=10,
                margin=ft.margin.only(bottom=8)
            )
            self.resumen_container.content = ft.Column([error_card])
            self.page.update() 