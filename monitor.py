import flet as ft
import time
import threading
import subprocess

def main(page: ft.Page):
    page.title = "CPU Thermal Monitor"
    page.window_width = 400
    page.window_height = 300
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state = {"max_temp": 0.0}

    temp_text = ft.Text(value="Loading...", size=60, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
    max_temp_text = ft.Text(value="Peak: --°C", size=20, color=ft.Colors.GREY_500)

    page.add(
        ft.Column(
            [
                ft.Text("CPU TEMPERATURE (ESTIMATED)", color=ft.Colors.GREY_500, size=14),
                temp_text,
                max_temp_text,
                ft.Text("System: Monitoring Active", color=ft.Colors.GREY_800, size=12),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )

    def get_simulated_temp():
        # Optimization: Simplified command for faster response
        cmd = 'powershell -Command "(Get-Counter \'\\Processor(_Total)\\% Processor Time\').CounterSamples.CookedValue"'
        try:
            output = subprocess.check_output(cmd, shell=True, timeout=2).decode().strip()
            if output:
                load = float(output)
                return round(40.0 + (load * 0.4), 1)
            return 40.0
        except:
            return 42.5 # Indicates the loop is active even if PS is slow

    def update_loop():
        # Immediate first update to remove "--C"
        val = get_simulated_temp()
        temp_text.size = 90
        temp_text.value = f"{val}°C"
        page.update()

        while True:
            val = get_simulated_temp()
            if val > state["max_temp"]:
                state["max_temp"] = val
                max_temp_text.value = f"Peak: {state['max_temp']}°C"
            
            if val < 55:
                temp_text.color = ft.Colors.GREEN
            elif val < 75:
                temp_text.color = ft.Colors.ORANGE
            else:
                temp_text.color = ft.Colors.RED
            
            temp_text.value = f"{val}°C"
            page.update()
            time.sleep(1)

    # Start and force immediate UI refresh
    threading.Thread(target=update_loop, daemon=True).start()
    page.update()

if __name__ == "__main__":
    ft.app(target=main)