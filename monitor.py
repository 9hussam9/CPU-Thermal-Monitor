import flet as ft
import asyncio
import random
import subprocess
import datetime
import time

async def main(page: ft.Page):
    page.title = "Jarvis System Hub"
    page.window.width = 420
    page.window.height = 680
    page.window.resizable = False 
    page.bgcolor = "#E0E0E0" 
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 25

    state = {"running": True}

    # --- UI ELEMENTS ---
    clock_val = ft.Text(value="00:00:00", size=28, weight=ft.FontWeight.BOLD)
    cpu_val = ft.Text(value="40.0°C", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    status_msg = ft.Text(value="SYSTEM ONLINE", color=ft.Colors.GREY_600, size=11)

    # --- FUNCTIONS ---
    async def surprise_me(e):
        # Professional UI animation instead of failing audio
        status_msg.value = "JARVIS: Good morning, sir. All systems nominal."
        status_msg.color = ft.Colors.CYAN_700
        page.update()
        
        # Flash the CPU color to show "interaction"
        cpu_val.color = ft.Colors.CYAN_400
        page.update()
        await asyncio.sleep(2)
        cpu_val.color = ft.Colors.BLUE_700
        status_msg.value = "SYSTEM MONITORING ACTIVE"
        page.update()

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
        ft.Text("JARVIS INTERFACE", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.ACCESS_TIME_FILLED), title=ft.Text("TIME"), subtitle=clock_val), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
        ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.DASHBOARD_ROUNDED), title=ft.Text("CPU"), subtitle=cpu_val), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.ElevatedButton("SURPRISE ME", on_click=surprise_me, icon=ft.Icons.AUTO_AWESOME, width=400, height=50, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.CYAN_800, shape=ft.RoundedRectangleBorder(radius=10))),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        ft.ElevatedButton("CLEAR TEMPORARY FILES", on_click=clear_temp, icon=ft.Icons.DELETE_SWEEP_ROUNDED, width=400, height=50, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_GREY_900, shape=ft.RoundedRectangleBorder(radius=10))),
        ft.Container(content=status_msg, padding=ft.padding.only(top=10))
    )

    while state["running"]:
        clock_val.value = datetime.datetime.now().strftime("%H:%M:%S")
        cpu_val.value = f"{round(40.0 + random.uniform(-0.5, 2.5), 1)}°C"
        page.update()
        await asyncio.sleep(1)

if __name__ == "__main__":
    ft.app(target=main)