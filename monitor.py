import flet as ft
import asyncio
import random
import subprocess
import datetime
import time

async def main(page: ft.Page):
    page.title = "DASHBOARD PRO"
    page.window_width = 450
    page.window_height = 650
    page.bgcolor = "#0A0A0A"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 40
    # Simplified Alignment
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state = {"running": True, "max_temp": 40.0} 

    # --- UI ELEMENTS ---
    clock_text = ft.Text(value="00:00:00", size=48, weight=ft.FontWeight.W_100, color=ft.Colors.CYAN_400)
    temp_text = ft.Text(value="40.0°C", size=84, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_ACCENT_400)
    peak_text = ft.Text(value="PEAK: 40.0°C", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700)
    status_msg = ft.Text(value="SYSTEM NOMINAL", color=ft.Colors.GREY_800, size=10, weight=ft.FontWeight.BOLD)

    # --- FUNCTIONS ---
    def reset_peak(e):
        state["max_temp"] = 0.0
        peak_text.value = "PEAK: --°C"
        page.update()

    def clear_temp(e):
        status_msg.value = "INITIALIZING PURGE..."
        status_msg.color = ft.Colors.AMBER_400
        page.update()
        clean_cmd = r'powershell -Command "Remove-Item -Path $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue"'
        subprocess.run(clean_cmd, shell=True)
        status_msg.value = "PURGE COMPLETE"
        status_msg.color = ft.Colors.GREEN_ACCENT_400
        page.update()

    # --- LAYOUT ---
    main_card = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.SHIELD_ROUNDED, size=16, color=ft.Colors.CYAN_700), ft.Text("SECURE DASHBOARD", size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_700)], alignment=ft.MainAxisAlignment.CENTER),
                clock_text,
                ft.Divider(height=40, color=ft.Colors.WHITE10),
                temp_text,
                peak_text,
                ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                ft.Row([
                    ft.IconButton(icon=ft.Icons.REPLAY_CIRCLE_FILLED_ROUNDED, icon_color=ft.Colors.CYAN_700, on_click=reset_peak),
                    ft.ElevatedButton("CLEAN SYSTEM", on_click=clear_temp, bgcolor=ft.Colors.RED_900, color=ft.Colors.WHITE),
                ], alignment=ft.MainAxisAlignment.CENTER),
                status_msg,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=30,
        border_radius=30,
        border=ft.border.all(1, ft.Colors.WHITE10),
        # Removed the problematic LinearGradient alignment to ensure it launches
        bgcolor="#151515" 
    )

    page.add(main_card)

    # --- ASYNC LOOP ---
    while state["running"]:
        clock_text.value = datetime.datetime.now().strftime("%H:%M:%S")
        val = round(40.0 + random.uniform(-0.5, 2.8), 1)
        temp_text.value = f"{val}°C"
        
        if val > state["max_temp"]:
            state["max_temp"] = val
            peak_text.value = f"PEAK: {state['max_temp']}°C"

        page.update()
        await asyncio.sleep(1)

if __name__ == "__main__":
    ft.app(target=main)