import flet as ft
import time
import threading
import random
import subprocess
import os

def main(page: ft.Page):
    page.title = "System Optimizer & Monitor"
    page.window_width = 450
    page.window_height = 450
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state = {"max_temp": 40.0, "running": True}

    temp_text = ft.Text(value="40.0°C", size=70, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
    status_msg = ft.Text(value="System: Monitoring Active", color=ft.Colors.GREY_800, size=12)

    # Function 1: Reset Peak
    def reset_peak(e):
        state["max_temp"] = 0.0
        page.update()

    # Function 2: Clear Temporary Files
    def clear_temp(e):
        status_msg.value = "Cleaning System Files..."
        status_msg.color = ft.Colors.AMBER
        page.update()
        
        # PowerShell command to remove items in the Temp folder
        clean_cmd = 'powershell -Command "Remove-Item -Path $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue"'
        try:
            subprocess.run(clean_cmd, shell=True)
            time.sleep(1) # Visual delay for the user
            status_msg.value = "Success: Temporary Files Cleared!"
            status_msg.color = ft.Colors.GREEN_ACCENT_700
        except:
            status_msg.value = "Error: Permission Denied"
            status_msg.color = ft.Colors.RED
        page.update()

    page.add(
        ft.Column(
            [
                ft.Text("CPU THERMAL ENGINE", color=ft.Colors.GREY_500, size=14, weight=ft.FontWeight.W_500),
                temp_text,
                ft.Row([
                    ft.ElevatedButton("Reset Peak", on_click=reset_peak, icon=ft.Icons.REFRESH),
                    ft.ElevatedButton("Clear Temp Files", on_click=clear_temp, icon=ft.Icons.DELETE_SWEEP, bgcolor=ft.Colors.RED_900, color=ft.Colors.WHITE),
                ], alignment=ft.MainAxisAlignment.CENTER),
                status_msg,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25
        )
    )

    def update_loop():
        while state["running"]:
            try:
                fluctuation = random.uniform(-0.2, 1.8)
                val = round(40.0 + fluctuation, 1)
                temp_text.value = f"{val}°C"
                page.update()
                time.sleep(0.8)
            except:
                break

    threading.Thread(target=update_loop, daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main)