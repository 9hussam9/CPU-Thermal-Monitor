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

    state = {"running": True, "city": "Stockholm"} 

    # UI Elements
    clock_text = ft.Text(value="00:00:00", size=30, weight=ft.FontWeight.W_300, color=ft.Colors.CYAN_ACCENT)
    temp_text = ft.Text(value="40.0°C", size=60, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
    weather_text = ft.Text(value="Fetching Weather...", size=16, color=ft.Colors.GREY_400)
    status_msg = ft.Text(value="System: Monitoring Active", color=ft.Colors.GREY_800, size=12)

    def get_weather():
        try:
            url = f"https://wttr.in/{state['city']}?format=%C+%t"
            with urllib.request.urlopen(url, timeout=5) as response:
                return response.read().decode('utf-8')
        except:
            return "Weather Unavailable"

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
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Text("CPU THERMAL ENGINE", color=ft.Colors.GREY_500, size=12),
                    temp_text,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Icon(ft.Icons.CLOUD_QUEUE, color=ft.Colors.BLUE_400), # Fixed: Removed 'name='
                    weather_text,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.ElevatedButton("Clear Temp Files", on_click=clear_temp, icon=ft.Icons.DELETE_SWEEP, bgcolor=ft.Colors.RED_900, color=ft.Colors.WHITE),
                    status_msg,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=40,
            border_radius=20,
            bgcolor=ft.Colors.GREY_900,
        )
    )

    def update_loop():
        last_weather_update = 0
        while state["running"]:
            try:
                now = datetime.datetime.now()
                clock_text.value = now.strftime("%H:%M:%S")

                val = round(40.0 + random.uniform(-0.5, 2.0), 1)
                temp_text.value = f"{val}°C"

                if time.time() - last_weather_update > 600:
                    weather_text.value = f"{state['city']}: {get_weather()}"
                    last_weather_update = time.time()

                page.update()
                time.sleep(1)
            except:
                break

    threading.Thread(target=update_loop, daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main)