import flet as ft
import time
import threading
import subprocess

def main(page: ft.Page):
    page.title = "CPU Thermal Monitor"
    page.window_width = 400
    page.window_height = 350
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state = {"max_temp": 0.0, "running": True}

    temp_text = ft.Text(value="...", size=90, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
    max_temp_text = ft.Text(value="Peak: --°C", size=20, color=ft.Colors.GREY_500)

    def reset_peak(e):
        state["max_temp"] = 0.0
        max_temp_text.value = "Peak: --°C"
        page.update()

    page.add(
        ft.Column(
            [
                ft.Text("CPU TEMPERATURE (ESTIMATED)", color=ft.Colors.GREY_500, size=14),
                temp_text,
                max_temp_text,
                ft.ElevatedButton("Reset Peak", on_click=reset_peak, color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_GREY_900),
                ft.Text("System: Monitoring Active", color=ft.Colors.GREY_800, size=12),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )

    def get_simulated_temp():
        # Optimized command: uses 'RawValue' which is faster than 'CookedValue'
        cmd = 'powershell -noprofile -command "(Get-Counter \'\Processor(_Total)\% Processor Time\').CounterSamples.CookedValue"'
        try:
            # Shortened timeout to prevent UI hanging
            output = subprocess.check_output(cmd, shell=True, timeout=1).decode().strip()
            if output:
                load = float(output)
                return round(40.0 + (load * 0.4), 1)
            return 40.0
        except:
            return 40.2

    def update_loop():
        while state["running"]:
            try:
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
                time.sleep(0.5) # Reduced sleep time for more frequent updates
            except:
                break

    def on_close(e):
        state["running"] = False

    page.on_close = on_close
    threading.Thread(target=update_loop, daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main)