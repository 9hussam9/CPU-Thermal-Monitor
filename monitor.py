import flet as ft
import asyncio
import random
import subprocess
import datetime
import urllib.request
import time

async def main(page: ft.Page):
    page.title = "System Monitor"
    page.window_width = 400
    page.window_height = 600
    page.bgcolor = "#F0F0F0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.START

    state = {"running": True, "city": "Stockholm", "max_temp": 40.0} 

    # --- UI ELEMENTS ---
    clock_val = ft.Text(value="00:00:00", size=24, weight=ft.FontWeight.BOLD)
    cpu_val = ft.Text(value="40.0°C", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    
    # We define this here so the loop can find it easily
    weather_display = ft.Text(value="STOCKHOLM: --", size=18)
    
    status_msg = ft.Text(value="System Active", color=ft.Colors.GREY_600, size=12)

    def clear_temp(e):
        status_msg.value = "Cleaning..."
        page.update()
        clean_cmd = r'powershell -Command "Remove-Item -Path $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue"'
        subprocess.run(clean_cmd, shell=True)
        status_msg.value = "Temp Files Cleared"
        page.update()

    # --- LAYOUT (BOXES) ---
    page.add(
        ft.Text("SYSTEM DASHBOARD", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
        
        # Clock Card
        ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.ACCESS_TIME),
                    title=ft.Text("CLOCK"),
                    subtitle=clock_val,
                ),
                padding=10,
            )
        ),
        
        # CPU Card
        ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.COMPUTER),
                    title=ft.Text("CPU TEMP"),
                    subtitle=cpu_val,
                ),
                padding=10,
            )
        ),
        
        # Weather Card
        ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.CLOUD),
                    title=ft.Text("WEATHER"),
                    subtitle=weather_display,
                ),
                padding=10,
            )
        ),

        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.ElevatedButton("CLEAR TEMP FILES", on_click=clear_temp, icon=ft.Icons.DELETE_OUTLINE),
        status_msg
    )

    # --- ASYNC LOOP ---
    last_weather_update = 0
    while state["running"]:
        clock_val.value = datetime.datetime.now().strftime("%H:%M:%S")
        
        val = round(40.0 + random.uniform(-0.5, 2.5), 1)
        cpu_val.value = f"{val}°C"

        # Fetch weather if 10 mins have passed
        if time.time() - last_weather_update > 600:
            try:
                url = f"https://wttr.in/{state['city']}?format=%C+%t"
                with urllib.request.urlopen(url, timeout=5) as res:
                    weather_display.value = f"{state['city'].upper()}: {res.read().decode('utf-8')}"
            except:
                weather_display.value = "Weather Offline"
            last_weather_update = time.time()

        page.update()
        await asyncio.sleep(1)

if __name__ == "__main__":
    ft.app(target=main)