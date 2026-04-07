import flet as ft
import time
import threading

def main(page: ft.Page):
    page.title = "CPU Thermal Monitor"
    page.window_width = 400
    page.window_height = 250
    page.bgcolor = ft.colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # The big temperature display
    temp_text = ft.Text(
        value="--°C",
        size=90,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.GREEN,
    )

    page.add(
        ft.Column(
            [
                ft.Text("CPU TEMPERATURE (ESTIMATED)", color=ft.colors.GREY_500),
                temp_text,
                ft.Text("System: Active", color=ft.colors.GREY_800),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)