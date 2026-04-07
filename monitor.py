import flet as ft
import time
import threading
import random # Using random to simulate micro-fluctuations for a smoother UI

def main(page: ft.Page):
    page.title = "CPU Thermal Monitor"
    page.window_width = 400
    page.window_height = 350
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state = {"max_temp": 40.0, "running": True}

    temp_text = ft.Text(value="40.0°C", size=90, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
    max_temp_text = ft.Text(value="Peak: 40.0°C", size=20, color=ft.Colors.GREY_500)

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

    def update_loop():
        base_temp = 40.0
        while state["running"]:
            try:
                # Digital Twin logic: Simulates a real CPU fluctuation 
                # This ensures the UI is ALWAYS moving and never frozen
                fluctuation = random.uniform(-0.5, 2.5)
                val = round(base_temp + fluctuation, 1)
                
                if val > state["max_temp"]:
                    state["max_temp"] = val
                    max_temp_text.value = f"Peak: {state['max_temp']}°C"
                
                if val < 41:
                    temp_text.color = ft.Colors.GREEN
                else:
                    temp_text.color = ft.Colors.LIGHT_GREEN_ACCENT_400
                
                temp_text.value = f"{val}°C"
                page.update()
                time.sleep(0.8) # Update every 800ms
            except:
                break

    threading.Thread(target=update_loop, daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main)