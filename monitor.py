import flet as ft
import time
import threading
import random
import subprocess
import datetime
import urllib.request

def main(page: ft.Page):
    page.title = "System Dashboard Pro"
    page.window_width = 500
    page.window_height = 600
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state = {"running": True, "city": "Stockholm", "max_temp": 40.0} 

    clock_text = ft.Text(value="00:00:00", size=30, color=ft.Colors.CYAN_ACCENT)
    temp_text = ft.Text(value="40.0°C", size=70, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
    peak_text = ft.Text(value="Peak: 40.0°C", size=20, color=ft.Colors.GREY_500)
    weather_text = ft.Text(value="Fetching Weather...", size=16, color=ft.Colors.GREY_400)
    status_msg = ft.Text(value="System: Monitoring Active", color=ft.Colors.GREY_800, size=12)

    def reset_peak(e):
        state["max_temp"] = 0.0
        peak_text.value = "Peak: --°C"
        page.update()

    def clear_temp(e):
        status_msg.value = "Cleaning System Files..."
        status_msg.color = ft.Colors.AMBER
        page.update()
        clean_cmd = 'powershell -Command "Remove-Item -Path $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue"'
        subprocess.run(clean_cmd, shell=True)
        status_msg.value = "Success: Temporary Files Cleared!"
        status_msg.color = ft.Colors.GREEN_ACCENT_700
        page.update()

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    clock_text,
                    ft.Text("CPU THERMAL ENGINE", color=ft.Colors.GREY_500, size=12),
                    temp_text,
                    peak_text,
                    ft.Row([ft.Icon(ft.Icons.CLOUD_QUEUE), weather_text], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.ElevatedButton("Reset Peak", on_click=reset_peak, icon=ft.Icons.REFRESH),
                    ft.ElevatedButton("Clear Temp Files", on_click=clear_temp, icon=ft.Icons.DELETE_SWEEP, bgcolor=ft.Colors.RED_900, color=ft.Colors.WHITE),
                    status_msg,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            padding=30,
            border_radius=20,
            bgcolor=ft.Colors.GREY_900,
        )
    )

    def update_loop():
        last_weather_update = 0
        while state["running"]:
            # 1. Update Clock
            clock_text.value = datetime.datetime.now().strftime("%H:%M:%S")

            # 2. Update CPU Simulation
            val = round(40.0 + random.uniform(-0.5, 2.5), 1)
            temp_text.value = f"{val}°C"
            
            if val > state["max_temp"]:
                state["max_temp"] = val
                peak_text.value = f"Peak: {state['max_temp']}°C"

            # 3. Update Weather
            if time.time() - last_weather_update > 600:
                try:
                    url = f"https://wttr.in/{state['city']}?format=%C+%t"
                    with urllib.request.urlopen(url, timeout=5) as res:
                        weather_text.value = f"{state['city']}: {res.read().decode('utf-8')}"
                except:
                    weather_text.value = "Weather Offline"
                last_weather_update = time.time()

            # 4. FORCE UPDATE
            page.update()
            time.sleep(1)

    # Start the thread
    t = threading.Thread(target=update_loop, daemon=True)
    t.start()
    
    # Final nudge to start the visual loop
    page.update()

if __name__ == "__main__":
    ft.app(target=main)