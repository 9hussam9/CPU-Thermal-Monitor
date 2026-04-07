import flet as ft
import time
import threading
import subprocess

def main(page: ft.Page):
    page.title = "CPU Thermal Monitor"
    page.window_width = 400
    page.window_height = 250
    page.bgcolor = ft.colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    temp_text = ft.Text(
        value="--°C",
        size=90,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.GREEN,
    )

    status_text = ft.Text(
        value="System: Monitoring Active",
        color=ft.colors.GREY_800,
        size=12,
    )

    page.add(
        ft.Column(
            [
                ft.Text("CPU TEMPERATURE (ESTIMATED)", color=ft.colors.GREY_500, size=14),
                temp_text,
                status_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    def get_simulated_temp():
        cmd = 'powershell "(Get-Counter \'\\Processor(_Total)\\% Processor Time\').CounterSamples.CookedValue"'
        try:
            output = subprocess.check_output(cmd, shell=True).decode().strip()
            if output:
                load = float(output)
                calc_temp = 40.0 + (load * 0.4)
                return round(calc_temp, 1)
            return 40.0
        except:
            return 40.0

    def update_loop():
        while True:
            val = get_simulated_temp()
            
            if val < 55:
                temp_text.color = ft.colors.GREEN
            elif val < 75:
                temp_text.color = ft.colors.ORANGE
            else:
                temp_text.color = ft.colors.RED
            
                temp_text.value = f"{val}°C"
    page.update()
    time.sleep(1)

    threading.Thread(target=update_loop, daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main)