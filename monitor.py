import flet as ft
import asyncio
import random
import subprocess
import datetime
import urllib.request
import time

async def main(page: ft.Page):
    # Lock the window size for a consistent "App" feel
    page.title = "System Monitor"
    page.window.width = 420
    page.window.height = 620
    page.window_resizable = False 
    page.bgcolor = "#E0E0E0" # Slightly darker "Platinum" Grey
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 25
    page.vertical_alignment = ft.MainAxisAlignment.START

    state = {"running": True, "city": "Stockholm"} 

    # --- UI ELEMENTS ---
    clock_val = ft.Text(value="00:00:00", size=28, weight=ft.FontWeight.BOLD)
    cpu_val = ft.Text(value="40.0°C", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    weather_display = ft.Text(value="STOCKHOLM: --", size=16, weight=ft.FontWeight.W_500)
    status_msg = ft.Text(value="System Active", color=ft.Colors.GREY_600, size=11)

    def clear_temp(e):
        status_msg.value = "PURGING TEMPORARY FILES..."
        status_msg.color = ft.Colors.ORANGE_700
        page.update()
        clean_cmd = r'powershell -Command "Remove-Item -Path $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue"'
        subprocess.run(clean_cmd, shell=True)
        status_msg.value = "CLEANUP COMPLETE"
        status_msg.color = ft.Colors.GREEN_700
        page.update()

    # --- LAYOUT ---
    page.add(
        ft.Text("SYSTEM DASHBOARD", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        
        # Clock Card
        ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.ACCESS_TIME_FILLED, color=ft.Colors.BLUE_GREY_700),
                    title=ft.Text("CLOCK", size=12, weight=ft.FontWeight.BOLD),
                    subtitle=clock_val,
                ),
                padding=10, bgcolor=ft.Colors.WHITE, border_radius=15
            ),
            elevation=2
        ),
        
        # CPU Card
        ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.DASHBOARD_ROUNDED, color=ft.Colors.BLUE_GREY_700),
                    title=ft.Text("CPU THERMAL", size=12, weight=ft.FontWeight.BOLD),
                    subtitle=cpu_val,
                ),
                padding=10, bgcolor=ft.Colors.WHITE, border_radius=15
            ),
            elevation=2
        ),
        
        # Weather Card
        ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.WB_CLOUDY_ROUNDED, color=ft.Colors.BLUE_GREY_700),
                    title=ft.Text("WEATHER", size=12, weight=ft.FontWeight.BOLD),
                    subtitle=weather_display,
                ),
                padding=10, bgcolor=ft.Colors.WHITE, border_radius=15
            ),
            elevation=2
        ),

        ft.Divider(height=25, color=ft.Colors.TRANSPARENT),
        
        # BIGGER BUTTON
        ft.ElevatedButton(
            "CLEAR TEMPORARY FILES", 
            on_click=clear_temp, 
            icon=ft.Icons.DELETE_SWEEP_ROUNDED,
            width=400, # Fill the width
            height=50, # Make it taller
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_GREY_900,
                shape=ft.RoundedRectangleBorder(radius=10),
            )
        ),
        ft.Container(content=status_msg, padding=ft.padding.only(top=10))
    )

    # --- ASYNC LOOP ---
    last_weather_update = 0
    while state["running"]:
        clock_val.value = datetime.datetime.now().strftime("%H:%M:%S")
        val = round(40.0 + random.uniform(-0.5, 2.5), 1)
        cpu_val.value = f"{val}°C"

        if time.time() - last_weather_update > 600:
            try:
                url = f"https://wttr.in/{state['city']}?format=%C+%t"
                with urllib.request.urlopen(url, timeout=5) as res:
                    weather_display.value = f"{state['city'].upper()}: {res.read().decode('utf-8')}"
            except:
                weather_display.value = "WEATHER OFFLINE"
            last_weather_update = time.time()

        page.update()
        await asyncio.sleep(1)

if __name__ == "__main__":
    ft.app(target=main)