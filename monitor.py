import flet as ft
import asyncio
import random
import subprocess
import datetime
import urllib.request
import time

async def main(page: ft.Page):
    page.title = "Jarvis System Hub"
    page.window.width = 420
    page.window.height = 760 # Increased for more buttons
    page.window.resizable = False 
    page.bgcolor = "#E0E0E0" 
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 25

    # Changed default to "Sir" so it sounds better immediately
    state = {"running": True, "city": "Stockholm", "temp_val": "40.0", "title": "Sir"}

    # --- THE DYNAMIC VOICE LOGIC ---
    def jarvis_report(report_text):
        clean_text = report_text.replace("'", "")
        # Using a specific name for the process so we can kill it later
        cmd = f'PowerShell -Command "Add-Type –AssemblyName System.Speech; ' \
              f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; ' \
              f'$speak.Speak(\'{clean_text}\')"'
        # Start as a subprocess
        subprocess.Popen(cmd, shell=True)

    def stop_voice(e):
        # Professional "Kill Switch" to stop PowerShell speech
        subprocess.run("taskkill /IM powershell.exe /F", shell=True)
        status_msg.value = "VOICE PROTOCOL TERMINATED"
        status_msg.color = ft.Colors.RED_700
        page.update()

    # --- UI ELEMENTS ---
    clock_val = ft.Text(value="12:00:00 PM", size=26, weight=ft.FontWeight.BOLD)
    cpu_val = ft.Text(value="40.0°C", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    weather_display = ft.Text(value="STOCKHOLM: --", size=16, weight=ft.FontWeight.W_500)
    status_msg = ft.Text(value="SYSTEM ONLINE", color=ft.Colors.GREY_600, size=11)

    gender_dd = ft.Dropdown(
        label="Select Identity",
        width=200,
        options=[
            ft.dropdown.Option("Male (Sir)"),
            ft.dropdown.Option("Female (Ma'am)"),
        ],
    )

    def update_identity(e):
        state["title"] = "Sir" if gender_dd.value == "Male (Sir)" else "Ma'am"
        status_msg.value = f"Identity updated to {state['title']}"
        page.update()

    gender_dd.on_change = update_identity

    async def surprise_me(e):
        now = datetime.datetime.now()
        current_time_voice = now.strftime("%I:%M %p")
        report = f"Good morning {state['title']}. The time is {current_time_voice}. The CPU temperature is {state['temp_val']} degrees Celsius."
        status_msg.value = f"JARVIS: REPORTING TO {state['title'].upper()}..."
        page.update()
        jarvis_report(report)
        await asyncio.sleep(4)
        status_msg.value = "SYSTEM MONITORING ACTIVE"
        page.update()

    # --- LAYOUT ---
    page.add(
        ft.Row([ft.Text("USER CONFIG:", size=11, weight=ft.FontWeight.BOLD), gender_dd], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.ACCESS_TIME_FILLED), title=ft.Text("TIME"), subtitle=clock_val), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
        ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.DASHBOARD_ROUNDED), title=ft.Text("CPU"), subtitle=cpu_val), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
        ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.WB_CLOUDY_ROUNDED), title=ft.Text("WEATHER"), subtitle=weather_display), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        
        # Report Button
        ft.ElevatedButton("SURPRISE ME (REPORT)", on_click=surprise_me, icon=ft.Icons.AUTO_AWESOME, width=400, height=50, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.CYAN_800)),
        
        # STOP VOICE BUTTON
        ft.OutlinedButton("STOP VOICE", on_click=stop_voice, icon=ft.Icons.VOLUME_OFF, width=400, height=40, style=ft.ButtonStyle(color=ft.Colors.RED_700)),
        
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        ft.ElevatedButton("CLEAR TEMPORARY FILES", on_click=lambda e: print("Cleaning..."), width=400, height=50, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_GREY_900)),
        status_msg
    )

    while state["running"]:
        clock_val.value = datetime.datetime.now().strftime("%I:%M:%S %p")
        temp = round(40.0 + random.uniform(-0.5, 2.5), 1)
        state["temp_val"] = str(temp)
        cpu_val.value = f"{temp}°C"
        page.update()
        await asyncio.sleep(1)

if __name__ == "__main__":
    ft.app(target=main)