import flet as ft
import asyncio
import random
import subprocess
import datetime
import urllib.request
import json
import time
import os
import threading
import re
import shutil
import sys
import winsound
import ssl

async def main(page: ft.Page):
    # ### --- PAGE CONFIGURATION ---
    page.title = "Jarvis System Hub"
    
    # Window Size Logic
    page.window.width = 450 
    page.window.height = 800 
    
    # Locking the dimensions
    page.window.resizable = False      # Prevents manual stretching
    page.window.maximizable = False    # Disables the maximize button
    page.window.min_width = 450
    page.window.max_width = 450
    page.window.min_height = 800
    page.window.max_height = 800
    
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
        "weather_now": "6°C",
        "user_name": "User" 
    }

    # ### --- VOICE & AUDIO SYSTEM ---
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

    def play_boot_sound():
        paths = [
            "jarvis.wav",
            os.path.join(os.path.dirname(sys.executable), "jarvis.wav"),
            os.path.join(os.path.dirname(__file__), "jarvis.wav")
        ]
        target_path = None
        for p in paths:
            if os.path.exists(p):
                target_path = p
                break
        if target_path:
            try:
                winsound.PlaySound(target_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception:
                pass

    # ### --- 15-SECOND ANIMATION START ---
    loading_text = ft.Text("INITIALIZING SYSTEM CORES...", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_800)
    progress_bar = ft.ProgressBar(width=300, color=ft.Colors.CYAN_700, bgcolor=ft.Colors.WHITE24, value=0)
    version_text = ft.Text("JARVIS VERSION 2.0", size=12, color=ft.Colors.GREY_700)
    
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
        if i == 40: loading_text.value = "ESTABLISHING SECURE CONNECTION..."
        if i == 75: loading_text.value = "SYNCING BIOMETRIC DATA..."
        page.update()
        await asyncio.sleep(0.15) # 15 Seconds Total

    # ### --- NAME INPUT SCREEN ---
    page.clean()
    async def enter_dashboard(e):
        if name_input.value:
            state["user_name"] = name_input.value
            await build_dashboard()

    name_input = ft.TextField(
        label="Enter your name", 
        width=300, 
        border_color=ft.Colors.CYAN_800,
        text_align=ft.TextAlign.CENTER, 
        on_submit=enter_dashboard 
    )

    page.add(
        ft.Icon(ft.Icons.LOCK_PERSON_ROUNDED, size=40, color=ft.Colors.CYAN_800),
        ft.Text("IDENTIFICATION REQUIRED", size=18, weight="bold"),
        name_input,
        ft.ElevatedButton("ACCESS SYSTEM", on_click=enter_dashboard, bgcolor=ft.Colors.CYAN_800, color="white", width=300)
    )
    page.update()

    # ### --- DASHBOARD SYSTEM ---
    async def build_dashboard():
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.START 
        page.horizontal_alignment = ft.CrossAxisAlignment.START

        clock_val = ft.Text(value="00:00:00 PM", size=26, weight=ft.FontWeight.BOLD)
        cpu_val = ft.Text(value="40.0°C", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
        weather_display = ft.Text(value="SYNCING WEATHER...", size=16, weight=ft.FontWeight.W_500)
        status_msg = ft.Text(value=f"SYSTEM READY", color=ft.Colors.GREY_600, size=11)

        voice_dd = ft.Dropdown(
            label="Jarvis Voice Engine", width=410, value="Male Engine", 
            options=[ft.dropdown.Option("Male Engine"), ft.dropdown.Option("Female Engine")]
        )

       # --- UPDATE SYSTEM LOGIC ---
        async def check_for_updates(e):
            import webbrowser
            import json
            
            status_msg.value = "CHECKING GITHUB FOR UPDATES..."
            page.update()

            current_version = "2.0"
            api_url = "https://api.github.com/repos/9hussam9/Jarvis-Hub/releases/latest"

            try:
                context = ssl._create_unverified_context()
                req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
                
                with urllib.request.urlopen(req, timeout=10, context=context) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    latest_version = data.get("tag_name", "").replace("v", "")
                    release_url = data.get("html_url", "")

                if latest_version and latest_version > current_version:
                    def close_dialog(e):
                        update_dialog.open = False
                        page.update()

                    def open_release(e):
                        webbrowser.open(release_url)
                        close_dialog(e)

                    update_dialog = ft.AlertDialog(
                        title=ft.Text("UPDATE AVAILABLE"),
                        content=ft.Text(f"Version {latest_version} is ready. Would you like to download it now?"),
                        actions=[
                            ft.TextButton("OPEN IN BROWSER", on_click=open_release),
                            ft.TextButton("NOT NOW", on_click=close_dialog)
                        ]
                    )
                    page.overlay.append(update_dialog)
                    update_dialog.open = True
                    status_msg.value = f"UPDATE {latest_version} AVAILABLE"
                else:
                    success_snack = ft.SnackBar(
                        content=ft.Text("Latest update is already installed"),
                        bgcolor=ft.Colors.GREEN_700
                    )
                    page.overlay.append(success_snack)
                    success_snack.open = True
                    status_msg.value = "SYSTEM: UP TO DATE"

            except Exception:
                status_msg.value = "UPDATE CHECK FAILED"

            page.update()

        # --- WEATHER & DASHBOARD LOGIC ---
        async def update_weather():
            try:
                context = ssl._create_unverified_context()
                loc_url = "http://ip-api.com/json/"
                with urllib.request.urlopen(loc_url, context=context) as response:
                    loc_data = json.loads(response.read().decode())
                    state["city"] = loc_data.get("city", "Unknown")
                url = f"https://wttr.in/{state['city']}?format=%t&m"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10, context=context) as res:
                    temp_raw = res.read().decode('utf-8').strip()
                    temp_num = int(re.sub(r'[^0-9-]', '', temp_raw))
                    state["weather_now"] = f"{temp_num}°C"
                    weather_display.value = f"{state['city'].upper()}: {state['weather_now']}"
            except: weather_display.value = "WEATHER: OFFLINE"
            page.update()

        async def surprise_me(e):
            if state["voice_active"]: return
            hour = datetime.datetime.now().hour
            if hour < 12: greeting = "Good morning"
            elif 12 <= hour < 18: greeting = "Good afternoon"
            else: greeting = "Good evening"
                
            report = (f"{greeting} {state['user_name']}. The time is {datetime.datetime.now().strftime('%I:%M %p')}. "
                      f"System temperature is {state['temp_val']} degrees. "
                      f"In {state['city']}, it is currently {state['weather_now']}.")
            status_msg.value = "JARVIS: GENERATING REPORT..."
            page.update()
            start_voice_thread(report, voice_dd.value)

        def stop_voice(e):
            state["voice_active"] = False
            subprocess.run("taskkill /IM powershell.exe /F", shell=True)
            status_msg.value = "VOICE TERMINATED"
            page.update()

        def clean_temp_files(e):
            temp_path = os.path.join(os.environ['LOCALAPPDATA'], 'Temp')
            status_msg.value = "PURGING TEMPORARY FILES..."
            page.update()
            files_deleted, errors = 0, 0
            if os.path.exists(temp_path):
                for filename in os.listdir(temp_path):
                    file_path = os.path.join(temp_path, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path): os.unlink(file_path)
                        elif os.path.isdir(file_path): shutil.rmtree(file_path)
                        files_deleted += 1
                    except: errors += 1
                status_msg.value = f"CLEANUP: {files_deleted} REMOVED, {errors} IN USE"
            page.update()

        # UI Layout
        page.add(
            ft.Text(f"LOGGED IN AS: {state['user_name'].upper()}", size=11, weight="bold", color=ft.Colors.CYAN_800),
            voice_dd,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.ACCESS_TIME_FILLED), title=ft.Text("TIME"), subtitle=clock_val), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
            ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.DASHBOARD_ROUNDED), title=ft.Text("CPU"), subtitle=cpu_val), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
            ft.Card(content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.WB_CLOUDY_ROUNDED), title=ft.Text("WEATHER"), subtitle=weather_display), padding=10, bgcolor=ft.Colors.WHITE, border_radius=15)),
            ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
            ft.ElevatedButton("SURPRISE ME (REPORT)", on_click=surprise_me, icon=ft.Icons.AUTO_AWESOME, width=410, height=45, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.CYAN_800)),
            ft.Row([
                ft.OutlinedButton("STOP VOICE", on_click=stop_voice, icon=ft.Icons.VOLUME_OFF, width=200, height=40, style=ft.ButtonStyle(color=ft.Colors.RED_700)),
                ft.OutlinedButton("CHECK UPDATE", on_click=check_for_updates, icon=ft.Icons.UPGRADE, width=200, height=40, style=ft.ButtonStyle(color=ft.Colors.CYAN_800)),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            ft.ElevatedButton("CLEAR TEMPORARY FILES", icon=ft.Icons.DELETE_SWEEP_OUTLINED, on_click=clean_temp_files, width=410, height=45, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_GREY_900)),
            status_msg
        )

        await update_weather()

        while state["running"]:
            clock_val.value = datetime.datetime.now().strftime("%I:%M:%S %p")
            temp = round(40.0 + random.uniform(-0.5, 2.5), 1)
            state["temp_val"], cpu_val.value = str(temp), f"{temp}°C"
            page.update()
            await asyncio.sleep(1)

if __name__ == "__main__":
    ft.app(target=main)