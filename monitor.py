import flet as ft
import asyncio
import random
import subprocess
import datetime
import urllib.request
import json
import time
import os
import vlc
import threading
import re
import shutil

async def main(page: ft.Page):
    # ### --- WINDOW CONFIGURATION ---
    page.title = "Jarvis System Hub"
    page.window.width = 450 
    page.window.height = 800 
    page.window.resizable = False 
    page.bgcolor = "#E0E0E0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER 
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state = {
        "running": True, 
        "city": "Locating...", 
        "temp_val": "40.0", 
        "voice_active": False,
        "weather_now": "6°C"
    }

    # ### --- VOICE ENGINE ---
    def jarvis_report_logic(report_text, voice_gender):
        state["voice_active"] = True
        clean_text = report_text.replace("'", "")
        voice_index = 1 if "Female" in voice_gender else 0
        segments = clean_text.split(". ")
        for segment in segments:
            if not state["voice_active"]: break
            cmd = (
                f'PowerShell -Command "Add-Type –AssemblyName System.Speech; '
                f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
                f'$voices = $speak.GetInstalledVoices(); '
                f'$speak.SelectVoice($voices[{voice_index}].VoiceInfo.Name); '
                f'$speak.Speak(\'{segment}\')"'
            )
            subprocess.run(cmd, shell=True)
            for _ in range(5):
                if not state["voice_active"]: break
                time.sleep(0.1)
        state["voice_active"] = False

    def start_voice_thread(text, gender):
        threading.Thread(target=jarvis_report_logic, args=(text, gender), daemon=True).start()

    # ### --- BOOT SEQUENCE LOGIC ---
    def play_boot_sound():
        paths = ["jarvis.wav", r"C:\progrsming_project\github\jarvis.wav"]
        target_path = None
        for p in paths:
            if os.path.exists(p):
                target_path = p
                break
        if target_path:
            try:
                instance = vlc.Instance()
                player = instance.media_player_new()
                media = instance.media_new(target_path)
                player.set_media(media)
                player.play()
            except Exception:
                pass

    # ### --- WELCOME UI (BOOT SCREEN) ---
    loading_text = ft.Text("INITIALIZING SYSTEM CORES...", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_800)
    progress_bar = ft.ProgressBar(width=300, color=ft.Colors.CYAN_700, bgcolor=ft.Colors.WHITE24, value=0)
    version_text = ft.Text("JARVIS VERSION 2.0", size=12, color=ft.Colors.GREY_500)
    
    page.add(
        ft.Icon(ft.Icons.SHIELD_MOON_ROUNDED, size=60, color=ft.Colors.CYAN_800), 
        loading_text, 
        progress_bar,
        version_text
    )
    page.update()
    
    play_boot_sound()
    for i in range(1, 101):
        progress_bar.value = i / 100
        page.update()
        await asyncio.sleep(0.17)

    page.clean()
    page.vertical_alignment = ft.MainAxisAlignment.START 
    page.horizontal_alignment = ft.CrossAxisAlignment.START

    # ### --- MAIN DASHBOARD ELEMENTS ---
    clock_val = ft.Text(value="00:00:00 PM", size=26, weight=ft.FontWeight.BOLD)
    cpu_val = ft.Text(value="40.0°C", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    weather_display = ft.Text(value="SYNCING WEATHER...", size=16, weight=ft.FontWeight.W_500)
    status_msg = ft.Text(value="SYSTEM ONLINE", color=ft.Colors.GREY_600, size=11)

    identity_dd = ft.Dropdown(
        label="Identity", width=200, value="Male (Sir)", 
        options=[ft.dropdown.Option("Male (Sir)"), ft.dropdown.Option("Female (Ma'am)")]
    )
    
    voice_dd = ft.Dropdown(
        label="Voice", width=200, value="Male Engine", 
        options=[ft.dropdown.Option("Male Engine"), ft.dropdown.Option("Female Engine")]
    )

    # ### --- WEATHER SYSTEM (AUTO-LOCATION) ---
    async def update_weather():
        try:
            loc_url = "http://ip-api.com/json/"
            with urllib.request.urlopen(loc_url) as response:
                loc_data = json.loads(response.read().decode())
                state["city"] = loc_data.get("city", "Unknown")
            
            url = f"https://wttr.in/{state['city']}?format=%t&m"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as res:
                temp_raw = res.read().decode('utf-8').strip()
                temp_num = int(re.sub(r'[^0-9-]', '', temp_raw))
                state["weather_now"] = f"{temp_num}°C"
                weather_display.value = f"{state['city'].upper()}: {state['weather_now']}"
        except:
            weather_display.value = "WEATHER: OFFLINE"
        page.update()

    # ### --- SYSTEM ACTIONS ---
    async def surprise_me(e):
        if state["voice_active"]: return
        selected_title = "Ma'am" if "Female" in identity_dd.value else "Sir"
        selected_voice = voice_dd.value
        now = datetime.datetime.now()
        report = (f"Good morning {selected_title}. The time is {now.strftime('%I:%M %p')}. "
                  f"The CPU temperature is {state['temp_val']} degrees. "
                  f"In {state['city']}, the temperature is {state['weather_now']}.")
        status_msg.value = f"JARVIS ({selected_voice.upper()}): REPORTING..."
        page.update()
        start_voice_thread(report, selected_voice)

    def stop_voice(e):
        state["voice_active"] = False
        subprocess.run("taskkill /IM powershell.exe /F", shell=True)
        status_msg.value = "VOICE TERMINATED"
        page.update()

    def clean_temp_files(e):
        temp_path = os.path.join(os.environ['LOCALAPPDATA'], 'Temp')
        status_msg.value = "PURGING TEMPORARY FILES..."
        page.update()
        files_deleted = 0
        errors = 0
        if os.path.exists(temp_path):
            for filename in os.listdir(temp_path):
                file_path = os.path.join(temp_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    files_deleted += 1
                except Exception:
                    errors += 1
            status_msg.value = f"CLEANUP: {files_deleted} REMOVED, {errors} IN USE"
        else:
            status_msg.value = "ERROR: PATH NOT FOUND"
        page.update()

    # ### --- LAYOUT ASSEMBLY ---
    page.add(
        ft.Text("USER CONFIG:", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
        ft.Row([identity_dd, voice_dd], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.ACCESS_TIME_FILLED), title=ft.Text("TIME"), subtitle=clock_val), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
        ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.DASHBOARD_ROUNDED), title=ft.Text("CPU"), subtitle=cpu_val), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
        ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.WB_CLOUDY_ROUNDED), title=ft.Text("WEATHER"), subtitle=weather_display), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.ElevatedButton("SURPRISE ME (REPORT)", on_click=surprise_me, icon=ft.Icons.AUTO_AWESOME, width=410, height=50, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.CYAN_800)),
        ft.OutlinedButton("STOP VOICE", on_click=stop_voice, icon=ft.Icons.VOLUME_OFF, width=410, height=40, style=ft.ButtonStyle(color=ft.Colors.RED_700)),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        ft.ElevatedButton("CLEAR TEMPORARY FILES", icon=ft.Icons.DELETE_SWEEP_OUTLINED, on_click=clean_temp_files, width=410, height=50, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_GREY_900)),
        status_msg
    )

    await update_weather()

    # ### --- MAIN REFRESH LOOP ---
    while state["running"]:
        clock_val.value = datetime.datetime.now().strftime("%I:%M:%S %p")
        temp = round(40.0 + random.uniform(-0.5, 2.5), 1)
        state["temp_val"] = str(temp)
        cpu_val.value = f"{temp}°C"
        page.update()
        await asyncio.sleep(1)

if __name__ == "__main__":
    ft.app(target=main)