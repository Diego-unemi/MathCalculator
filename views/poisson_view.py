import flet as ft
import matplotlib.pyplot as plt
import numpy as np
from modules.poisson_distribution import PoissonDistribution
import io
import base64

class PoissonView(ft.Control):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.lambda_input = ft.TextField(
            label="Parámetro lambda",
            value="5",
            width=180,
            text_align=ft.TextAlign.CENTER,
        )
        self.samples_input = ft.TextField(
            label="Número de muestras",
            value="1000",
            width=180,
            text_align=ft.TextAlign.CENTER,
        )
        self.error_message = ft.Text("", color=ft.Colors.RED_200, size=13, visible=False)
        self.generate_button = ft.ElevatedButton(
            text="Generar Distribución",
            on_click=self.generate_distribution,
            bgcolor=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            width=200,
        )
        self.plot_image = ft.Image(
            width=500,
            height=250,
            fit=ft.ImageFit.CONTAIN,
            visible=False
        )
        # Tabla de resultados
        self.results_table = ft.DataTable(
            width=500,
            border=ft.border.all(1, ft.Colors.BLUE_100),
            border_radius=8,
            bgcolor=ft.Colors.BLACK,
            data_row_max_height=32,
            heading_row_height=36,
            columns=[
                ft.DataColumn(ft.Text("k", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Frecuencia", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("P. empírica", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("P. teórica", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            visible=False
        )
        self.results_container = ft.Container(
            width=520,
            border=ft.border.all(1, ft.Colors.BLUE_100),
            border_radius=8,
            bgcolor=ft.Colors.BLACK87,
            padding=16,
            shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.BLUE_100, offset=ft.Offset(0, 4)),
            content=ft.Column([
                ft.Text("Tabla de resultados:", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                self.results_table,
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            alignment=ft.alignment.center,
            visible=False
        )
        self.no_data_message = ft.Text(
            "Genera una distribución para ver la gráfica y la tabla.",
            color=ft.Colors.WHITE60,
            size=15,
            text_align=ft.TextAlign.CENTER,
            visible=True
        )

    def build(self):
        # Tarjeta de entrada
        input_card = ft.Container(
            content=ft.Column([
                ft.Text("Distribución de Poisson", size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([
                    self.lambda_input,
                    self.samples_input
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=24),
                self.generate_button,
                self.error_message
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=18),
            width=540,
            padding=24,
            border=ft.border.all(1, ft.Colors.BLUE_100),
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=16, color=ft.Colors.BLUE_100, offset=ft.Offset(0, 6)),
            bgcolor=ft.Colors.BLACK87,
            alignment=ft.alignment.center,
            margin=ft.margin.only(bottom=30)
        )
        # Panel de resultados
        results_panel = ft.Column([
            self.plot_image,
            self.results_container,
            self.no_data_message
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=18)
        # Layout principal
        return ft.Column([
            ft.Row([
                ft.Container(content=input_card, alignment=ft.alignment.center, expand=True)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.Container(content=results_panel, alignment=ft.alignment.center, expand=True)
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)

    def show(self):
        self.page.controls[0].controls[1].content.controls = [self.build()]
        self.page.update()

    def generate_results_table(self, k_values, freqs, empirical_probs, theoretical_probs):
        self.results_table.rows = []
        for i in range(len(k_values)):
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f"{k_values[i]}", color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(f"{freqs[i]}", color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(f"{empirical_probs[i]:.4f}", color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(f"{theoretical_probs[i]:.4f}", color=ft.Colors.WHITE)),
                ]
            )
            self.results_table.rows.append(row)
        self.results_table.visible = True
        self.results_container.visible = True
        self.no_data_message.visible = False
        self.page.update()

    def generate_distribution(self, e):
        try:
            self.error_message.visible = False
            lambda_param = float(self.lambda_input.value)
            n_samples = int(self.samples_input.value)
            if lambda_param <= 0 or n_samples <= 0:
                raise ValueError("Lambda y muestras deben ser mayores que cero.")
            poisson = PoissonDistribution(lambda_param)
            samples = poisson.generate_poisson(n_samples)
            max_k = max(samples)
            k_values, theoretical_probs = poisson.get_theoretical_probabilities(max_k)
            freqs = [samples.count(k) for k in k_values]
            empirical_probs = [f / n_samples for f in freqs]
            # Crear histograma
            plt.figure(figsize=(7, 3))
            plt.hist(samples, bins=range(max_k + 2), density=True, alpha=0.7, label='Muestras generadas')
            plt.plot(k_values, theoretical_probs, 'ro-', label='Probabilidad teórica')
            plt.title(f'Distribución de Poisson (λ={lambda_param})')
            plt.xlabel('k')
            plt.ylabel('Probabilidad')
            plt.legend()
            plt.grid(True, alpha=0.3)
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100)
            buf.seek(0)
            plt.close()
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            self.plot_image.src_base64 = image_base64
            self.plot_image.visible = True
            self.results_table.visible = True
            self.results_container.visible = True
            self.no_data_message.visible = False
            self.plot_image.update()
            self.generate_results_table(k_values, freqs, empirical_probs, theoretical_probs)
        except Exception as e:
            self.error_message.value = f"Error: {str(e)}"
            self.error_message.visible = True
            self.plot_image.visible = False
            self.results_table.visible = False
            self.results_container.visible = False
            self.no_data_message.visible = True
            self.page.update() 