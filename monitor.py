import flet as ft
import asyncio
import random
import subprocess
import datetime
import urllib.request
import time

async def main(page: ft.Page):
    page.title = "Jarvis System Hub"
    page.window.width = 450 # Made slightly wider for better spacing
    page.window.height = 800 
    page.window.resizable = False 
    page.bgcolor = "#E0E0E0" 
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    state = {"running": True, "city": "Stockholm", "temp_val": "40.0"}

    # --- VOICE LOGIC ---
    def jarvis_report(report_text, voice_gender):
        clean_text = report_text.replace("'", "")
        voice_index = 0 if voice_gender == "Male" else 1
        cmd = f'PowerShell -Command "Add-Type –AssemblyName System.Speech; ' \
              f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; ' \
              f'$voices = $speak.GetInstalledVoices(); ' \
              f'$speak.SelectVoice($voices[{voice_index}].VoiceInfo.Name); ' \
              f'$speak.Speak(\'{clean_text}\')"'
        subprocess.Popen(cmd, shell=True)

    def stop_voice(e):
        subprocess.run("taskkill /IM powershell.exe /F", shell=True)
        status_msg.value = "VOICE TERMINATED"
        page.update()

    # --- UI ELEMENTS ---
    clock_val = ft.Text(value="12:00:00 PM", size=26, weight=ft.FontWeight.BOLD)
    cpu_val = ft.Text(value="40.0°C", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    weather_display = ft.Text(value="STOCKHOLM: FETCHING...", size=16, weight=ft.FontWeight.W_500)
    status_msg = ft.Text(value="SYSTEM ONLINE", color=ft.Colors.GREY_600, size=11)

    # Side-by-Side Dropdowns with slightly more width (200)
    identity_dd = ft.Dropdown(
        label="Identity", 
        width=200, 
        value="Male (Sir)", 
        options=[ft.dropdown.Option("Male (Sir)"), ft.dropdown.Option("Female (Ma'am)")] 
    )
    
    voice_dd = ft.Dropdown(
        label="Voice", 
        width=200, 
        value="Male Engine", 
        options=[ft.dropdown.Option("Male Engine"), ft.dropdown.Option("Female Engine")] 
    )

    # --- WEATHER FUNCTION ---
    async def update_weather():
        try:
            url = f"https://wttr.in/{state['city']}?format=%C+%t"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as res:
                weather_data = res.read().decode('utf-8')
                weather_display.value = f"{state['city'].upper()}: {weather_data}"
        except:
            weather_display.value = f"{state['city'].upper()}: OFFLINE"
        page.update()

    async def surprise_me(e):
        selected_title = "Ma'am" if "Female" in identity_dd.value else "Sir"
        selected_voice = "Female" if "Female" in voice_dd.value else "Male"
        now = datetime.datetime.now()
        report = f"Good morning {selected_title}. The time is {now.strftime('%I:%M %p')}. The CPU temperature is {state['temp_val']} degrees."
        status_msg.value = f"JARVIS ({selected_voice.upper()}): REPORTING..."
        page.update()
        jarvis_report(report, selected_voice)
        await asyncio.sleep(4)
        status_msg.value = "SYSTEM MONITORING ACTIVE"
        page.update()

    # --- LAYOUT (Side-by-Side restored) ---
    page.add(
        ft.Text("SYSTEM CONFIGURATION", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
        ft.Row([
            identity_dd,
            voice_dd,
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        
        ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.ACCESS_TIME_FILLED), title=ft.Text("TIME"), subtitle=clock_val), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
        ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.DASHBOARD_ROUNDED), title=ft.Text("CPU"), subtitle=cpu_val), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
        ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.WB_CLOUDY_ROUNDED), title=ft.Text("WEATHER"), subtitle=weather_display), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
        
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        
        ft.ElevatedButton("SURPRISE ME (REPORT)", on_click=surprise_me, icon=ft.Icons.AUTO_AWESOME, width=410, height=50, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.CYAN_800)),
        ft.OutlinedButton("STOP VOICE", on_click=stop_voice, icon=ft.Icons.VOLUME_OFF, width=410, height=40, style=ft.ButtonStyle(color=ft.Colors.RED_700)),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        ft.ElevatedButton("CLEAR TEMPORARY FILES", on_click=lambda e: print("Cleaning..."), width=410, height=50, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_GREY_900)),
        
        status_msg
    )

    await update_weather()

    while state["running"]:
        clock_val.value = datetime.datetime.now().strftime("%I:%M:%S %p")
        temp = round(40.0 + random.uniform(-0.5, 2.5), 1)
        state["temp_val"] = str(temp)
        cpu_val.value = f"{temp}°C"
        page.update()
        await asyncio.sleep(1)

if __name__ == "__main__":
    ft.app(target=main)