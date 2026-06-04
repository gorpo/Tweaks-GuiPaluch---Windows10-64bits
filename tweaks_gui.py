import ctypes
import datetime as dt
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import tkinter as tk
import webbrowser
import zipfile
from ctypes import wintypes
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

import customtkinter as ctk
from PIL import Image


APP_TITLE = "Tweaks GuiPaluch"
BG = "#171717"
SIDEBAR = "#171717"
PANEL = "#212121"
PANEL_2 = "#2a2a2a"
TEXT = "#f3f3f3"
MUTED = "#a3a3a3"
ACCENT = "#ffffff"
ACCENT_2 = "#d4d4d4"
BUTTON = "#2f2f2f"
BUTTON_ACTIVE = "#3a3a3a"
TITLEBAR = "#171717"
SURFACE = "#212121"
SURFACE_2 = "#2f2f2f"
BORDER = "#3a3a3a"
HOVER = "#383838"
LOG_BG = "#0f0f0f"
DESKTOP = Path.home() / "Desktop"
DEFAULT_BACKUP_DIR = Path(r"D:\TweaksGuiPaluchBackups")
CONFIG_DIR = Path(os.environ.get("APPDATA", DESKTOP)) / "TweaksGuiPaluch"
CONFIG_FILE = CONFIG_DIR / "settings.json"
MINECRAFT_DIR = Path(os.environ.get("APPDATA", "")) / ".minecraft"
USER_START_MENU = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
COMMON_START_MENU = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
USER_STARTUP = USER_START_MENU / "Startup"
COMMON_STARTUP = COMMON_START_MENU / "Startup"
SEND_TO = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "SendTo"
QUICK_LAUNCH = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Internet Explorer" / "Quick Launch"
HOSTS_FILE = Path(r"C:\Windows\System32\drivers\etc\hosts")
SAVED_GAMES = Path.home() / "Saved Games"
MY_GAMES = Path.home() / "Documents" / "My Games"
STEAM_USERDATA = Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Steam" / "userdata"
STEAM_COMMON = Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Steam" / "steamapps" / "common"
EPIC_PROGRAMDATA = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Epic"
ROCKSTAR_DOCUMENTS = Path.home() / "Documents" / "Rockstar Games"
BATTLE_NET_PROGRAMDATA = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Battle.net"
DIRECTX_SHADER_CACHE = Path(os.environ.get("LOCALAPPDATA", "")) / "D3DSCache"
AMD_SHADER_CACHE = Path(os.environ.get("LOCALAPPDATA", "")) / "AMD" / "DxCache"
AMD_GL_CACHE = Path(os.environ.get("LOCALAPPDATA", "")) / "AMD" / "GLCache"
WINDOWS_CRASH_DUMPS = Path(os.environ.get("LOCALAPPDATA", "")) / "CrashDumps"
REDRAGON_DIR = Path(r"C:\Program Files (x86)\Redragon  M602P-KS  Gaming Mouse")
REDRAGON_EXE = REDRAGON_DIR / "DeviceDriver.exe"
REDRAGON_CONFIG = REDRAGON_DIR / "config.xml"
REDRAGON_LAYOUT = REDRAGON_DIR / "layouts" / "MOUSE_DM204.xml"
REDRAGON_PRESET_DIR = CONFIG_DIR / "redragon-light-presets"
REDRAGON_LIGHT_MODES = [
    {"name": "Fixo", "english": "Steady", "mode": 5, "lang": 902, "attribute": 49},
    {"name": "Respiracao", "english": "Breathing", "mode": 6, "lang": 903, "attribute": 67},
    {"name": "Fluxo", "english": "Flowing light", "mode": 1, "lang": 901, "attribute": 7},
    {"name": "Neon", "english": "Neon", "mode": 2, "lang": 905, "attribute": 3},
    {"name": "Corrida", "english": "Horse Racing", "mode": 3, "lang": 908, "attribute": 71},
    {"name": "Respiracao misturada", "english": "Mixed color breathing", "mode": 4, "lang": 913, "attribute": 71},
    {"name": "Luz desligada", "english": "Light Off", "mode": 7, "lang": 521, "attribute": 0},
    {"name": "Musica", "english": "Music", "mode": 11, "lang": 911, "attribute": 512, "experimental": True},
    {"name": "Ambilight", "english": "Ambilight", "mode": 12, "lang": 912, "attribute": 1024, "experimental": True},
]
REDRAGON_LIGHT_PRESETS = [
    ("Fixo branco", "Fixo", "#FFFFFF", 5, 1),
    ("Fixo vermelho", "Fixo", "#FF0000", 5, 1),
    ("Fixo verde", "Fixo", "#00FF00", 5, 1),
    ("Fixo azul", "Fixo", "#006CFF", 5, 1),
    ("Fixo ciano", "Fixo", "#00E5FF", 5, 1),
    ("Fixo roxo", "Fixo", "#8B5CF6", 5, 1),
    ("Fixo rosa", "Fixo", "#FF4FD8", 5, 1),
    ("Fixo amarelo", "Fixo", "#FFD000", 5, 1),
    ("Respirar azul", "Respiracao", "#006CFF", 4, 2),
    ("Respirar vermelho", "Respiracao", "#FF0000", 4, 2),
    ("Respirar roxo", "Respiracao", "#8B5CF6", 4, 2),
    ("Fluxo RGB", "Fluxo", "RGB", 5, 2),
    ("Neon RGB", "Neon", "RGB", 5, 2),
    ("Corrida RGB", "Corrida", "RGB", 5, 2),
    ("Respiracao misturada RGB", "Respiracao misturada", "RGB", 5, 2),
    ("Apagar luz", "Luz desligada", "OFF", 0, 0),
    ("Musica experimental", "Musica", "RGB", 5, 2),
    ("Ambilight experimental", "Ambilight", "RGB", 5, 2),
]
MINECRAFT_BACKUP_ITEMS = [
    "saves",
    "mods",
    "resourcepacks",
    "shaderpacks",
    "config",
    "defaultconfigs",
    "journeymap",
    "versions",
    "launcher_profiles.json",
    "TlauncherProfiles.json",
    "options.txt",
    "servers.dat",
]

DOWNLOAD_LINKS = {
    "AMD RX 580 drivers oficiais": "https://www.amd.com/en/support/download/drivers.html",
    "AMD RX580 primeiro estavel - 23.11.1 Polaris/Vega": "https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-23-11-1.html",
    "AMD RX580 estavel para Forza6 - 23.10.01.14": "https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-MS-AGILITY-SDK-2023-6-711.html",
    "AMD 23.10.01.14 notas oficiais": "https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-MS-AGILITY-SDK-2023-6-711.html",
    "Display Driver Uninstaller (DDU)": "https://www.wagnardsoft.com/display-driver-uninstaller-DDU-",
    "Temurin Java 8": "https://adoptium.net/temurin/releases/?version=8",
    "Temurin Java 17": "https://adoptium.net/temurin/releases/?version=17",
    "Temurin Java 21": "https://adoptium.net/temurin/releases/?version=21",
    "Temurin Java 25": "https://adoptium.net/temurin/releases/?version=25",
    "Minecraft Launcher": "https://www.minecraft.net/download",
    "Prism Launcher": "https://prismlauncher.org/download/",
    "Forge": "https://files.minecraftforge.net/net/minecraftforge/forge/",
    "NeoForge": "https://neoforged.net/",
    "Fabric": "https://fabricmc.net/use/installer/",
    "Modrinth App": "https://modrinth.com/app",
    "CurseForge App": "https://www.curseforge.com/download/app",
    "Git for Windows": "https://git-scm.com/download/win",
    "Visual Studio Code": "https://code.visualstudio.com/Download",
    "7-Zip": "https://www.7-zip.org/download.html",
}


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def relaunch_as_admin():
    if getattr(sys, "frozen", False):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
        return

    script = Path(__file__).resolve()
    params = f'"{script}"'
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)


def resource_path(name):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / name
    return Path(__file__).with_name(name)


def run_command(command, shell=False, timeout=None):
    try:
        completed = subprocess.run(
            command,
            shell=shell,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        output = completed.stdout.strip()
        error = completed.stderr.strip()
        parts = []
        if output:
            parts.append(output)
        if error:
            parts.append(error)
        parts.append(f"Codigo de saida: {completed.returncode}")
        return "\n".join(parts)
    except subprocess.TimeoutExpired:
        return "O comando demorou demais e foi interrompido."
    except Exception as exc:
        return f"Erro: {exc}"


def run_powershell(command, timeout=None):
    return run_command(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
        timeout=timeout,
    )


def open_target(target):
    try:
        os.startfile(target)
        return f"Aberto: {target}"
    except Exception as exc:
        return f"Erro ao abrir {target}: {exc}"


def remove_contents(path):
    base = Path(path)
    if not base.exists():
        return f"Pasta nao encontrada: {base}"

    removed = 0
    failed = 0
    for item in base.iterdir():
        try:
            if item.is_dir():
                shutil.rmtree(item, ignore_errors=False)
            else:
                item.unlink()
            removed += 1
        except Exception:
            failed += 1

    return (
        f"Limpeza concluida em: {base}\n"
        f"Itens removidos: {removed}\n"
        f"Itens ignorados/em uso: {failed}"
    )


def quick_temp_prefetch_cleanup():
    targets = [
        ("C:\\Windows\\Temp", r"C:\Windows\Temp"),
        ("%TEMP%", tempfile.gettempdir()),
        ("C:\\Windows\\Prefetch", r"C:\Windows\Prefetch"),
    ]

    results = []
    for label, path in targets:
        results.append(f"--- {label} ---\n{remove_contents(path)}")
    return "\n\n".join(results)


def clear_extra_caches():
    targets = [
        ("DirectX Shader Cache", DIRECTX_SHADER_CACHE),
        ("AMD DxCache", AMD_SHADER_CACHE),
        ("AMD GLCache", AMD_GL_CACHE),
        ("Crash Dumps do usuario", WINDOWS_CRASH_DUMPS),
    ]

    results = []
    for label, path in targets:
        results.append(f"--- {label} ---\n{remove_contents(path)}")
    return "\n\n".join(results)


def clear_browser_cache_paths():
    paths = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data" / "Default" / "Cache",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Edge" / "User Data" / "Default" / "Cache",
    ]

    firefox_profiles = Path(os.environ.get("APPDATA", "")) / "Mozilla" / "Firefox" / "Profiles"
    if firefox_profiles.exists():
        paths.extend(profile / "cache2" for profile in firefox_profiles.iterdir() if profile.is_dir())

    results = []
    for path in paths:
        results.append(remove_contents(path))

    return "\n\n".join(results) if results else "Nenhum cache de navegador encontrado."


def zip_existing_items(zip_name, base, items):
    backup_dir = ensure_backup_dir()
    zip_path = backup_dir / f"{zip_name}-{timestamp()}.zip"
    base = Path(base)
    included = 0
    missing = []

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for item in items:
            source = base / item
            if not source.exists():
                missing.append(str(source))
                continue
            if source.is_dir():
                for file in source.rglob("*"):
                    if file.is_file():
                        archive.write(file, file.relative_to(base))
                        included += 1
            else:
                archive.write(source, source.relative_to(base))
                included += 1

    details = [f"Backup criado:\n{zip_path}", f"Arquivos incluidos: {included}"]
    if missing:
        details.append("Itens nao encontrados:")
        details.extend(missing)
    return "\n".join(details)


def backup_folder_contents(label, folder):
    folder = Path(folder)
    if not folder.exists():
        return f"Pasta nao encontrada: {folder}"

    backup_dir = ensure_backup_dir()
    zip_path = backup_dir / f"{label}-{timestamp()}.zip"
    included = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for file in folder.rglob("*"):
            if file.is_file():
                archive.write(file, file.relative_to(folder.parent))
                included += 1
    return f"Backup criado:\n{zip_path}\nArquivos incluidos: {included}"


def backup_start_menu_shortcuts():
    backup_dir = ensure_backup_dir()
    zip_path = backup_dir / f"start-menu-shortcuts-{timestamp()}.zip"
    included = 0
    roots = [("usuario", USER_START_MENU), ("todos-usuarios", COMMON_START_MENU)]

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for label, root in roots:
            if not root.exists():
                continue
            for file in root.rglob("*"):
                if file.is_file():
                    archive.write(file, Path(label) / file.relative_to(root))
                    included += 1
    return f"Backup do Menu Iniciar criado:\n{zip_path}\nArquivos incluidos: {included}"


def backup_post_format_bundle():
    backup_dir = ensure_backup_dir()
    report = [export_pc_profile()]
    report.append(backup_start_menu_shortcuts())
    report.append(backup_folder_contents("desktop-backup", DESKTOP))
    if MINECRAFT_DIR.exists():
        report.append(backup_minecraft_modding_only())

    checklist = backup_dir / f"checklist-pos-formatacao-{timestamp()}.txt"
    checklist.write_text(
        "\n\n".join([
            "Checklist pos-formatacao Tweaks GuiPaluch",
            "1. Instalar driver AMD RX580 primeiro estavel ou Forza6, conforme necessidade.",
            "2. Instalar Java 8/17/21 para Minecraft e modding.",
            "3. Restaurar atalhos do Menu Iniciar se necessario.",
            "4. Restaurar backups de Minecraft/mods/saves.",
            "5. Conferir apps de inicializacao, privacidade, plano de energia e tela.",
            "6. Criar ponto de restauracao depois que tudo estiver ajustado.",
        ]),
        encoding="utf-8",
    )
    report.append(f"Checklist criado:\n{checklist}")
    return "\n\n".join(report)


def minecraft_clean_logs_and_cache():
    targets = [
        ("logs", MINECRAFT_DIR / "logs"),
        ("crash-reports", MINECRAFT_DIR / "crash-reports"),
        (".mixin.out", MINECRAFT_DIR / ".mixin.out"),
        ("cache", MINECRAFT_DIR / "cache"),
    ]
    results = []
    for label, path in targets:
        results.append(f"--- {label} ---\n{remove_contents(path)}")
    return "\n\n".join(results)


def minecraft_latest_crash_report():
    reports = MINECRAFT_DIR / "crash-reports"
    if not reports.exists():
        return "Pasta crash-reports nao encontrada."

    files = sorted([p for p in reports.glob("*.txt") if p.is_file()], key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return "Nenhum crash report encontrado."

    latest = files[0]
    try:
        os.startfile(str(latest))
    except Exception:
        pass
    return f"Crash report mais recente:\n{latest}"


def list_minecraft_mods():
    mods_dir = MINECRAFT_DIR / "mods"
    if not mods_dir.exists():
        return "Pasta mods nao encontrada."

    mods = sorted([p.name for p in mods_dir.glob("*.jar")])
    output = ensure_backup_dir() / f"minecraft-mods-{timestamp()}.txt"
    output.write_text("\n".join(mods), encoding="utf-8")
    return f"Mods encontrados: {len(mods)}\nLista salva em:\n{output}"


def java_versions_report():
    return "\n\n".join([
        "=== where java ===",
        run_command("where java", shell=True),
        "=== java -version ===",
        run_command("java -version", shell=True),
        "=== Program Files Java/Temurin ===",
        run_powershell("Get-ChildItem 'C:\\Program Files','C:\\Program Files (x86)' -Directory -ErrorAction SilentlyContinue | Where-Object {$_.Name -match 'Java|Eclipse|Temurin|Adoptium'} | Select-Object FullName | Format-Table -AutoSize"),
    ])


def miracast_diagnostics():
    return "\n\n".join([
        "=== Miracast / Wi-Fi driver ===",
        run_command(["netsh", "wlan", "show", "drivers"]),
        "=== Adaptadores de rede ===",
        run_powershell("Get-NetAdapter | Select-Object Name,InterfaceDescription,Status,LinkSpeed,MacAddress | Format-Table -AutoSize"),
        "=== Configuracao de rede ===",
        run_command(["ipconfig"]),
    ])


def network_diagnostics():
    gateway = run_powershell("(Get-NetRoute -DestinationPrefix '0.0.0.0/0' | Sort-Object RouteMetric | Select-Object -First 1 -ExpandProperty NextHop)", timeout=30).splitlines()
    gateway = gateway[0].strip() if gateway else ""
    parts = [run_command(["ipconfig"])]
    if gateway and "Codigo de saida" not in gateway:
        parts.append(f"=== Ping gateway {gateway} ===\n{run_command(['ping', '-n', '4', gateway], timeout=30)}")
    parts.append("=== Ping Google DNS ===\n" + run_command(["ping", "-n", "4", "8.8.8.8"], timeout=30))
    parts.append("=== Ping google.com ===\n" + run_command(["ping", "-n", "4", "google.com"], timeout=30))
    return "\n\n".join(parts)


def bluetooth_diagnostics():
    return "\n\n".join([
        "=== Servicos Bluetooth ===",
        run_powershell("Get-Service bthserv,BluetoothUserService* -ErrorAction SilentlyContinue | Select-Object Name,DisplayName,Status,StartType | Format-Table -AutoSize"),
        "=== Dispositivos Bluetooth ===",
        run_powershell("Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue | Select-Object Status,FriendlyName,InstanceId | Format-Table -AutoSize"),
        "=== Dispositivos de audio ===",
        run_powershell("Get-PnpDevice -Class Media -ErrorAction SilentlyContinue | Select-Object Status,FriendlyName,InstanceId | Format-Table -AutoSize"),
    ])


def restart_bluetooth_services():
    command = (
        "Get-Service bthserv,BluetoothUserService* -ErrorAction SilentlyContinue | "
        "Restart-Service -Force -ErrorAction SilentlyContinue; "
        "Get-Service bthserv,BluetoothUserService* -ErrorAction SilentlyContinue | "
        "Select-Object Name,DisplayName,Status | Format-Table -AutoSize"
    )
    return run_powershell(command, timeout=120)


def restart_audio_services():
    command = (
        "Restart-Service Audiosrv,AudioEndpointBuilder -Force -ErrorAction SilentlyContinue; "
        "Get-Service Audiosrv,AudioEndpointBuilder | Select-Object Name,DisplayName,Status | Format-Table -AutoSize"
    )
    return run_powershell(command, timeout=120)


def timestamp():
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def load_settings():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_settings(settings):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8")


def get_backup_dir():
    settings = load_settings()
    configured = settings.get("backup_dir")
    return Path(configured) if configured else DEFAULT_BACKUP_DIR


def set_backup_dir(path):
    settings = load_settings()
    settings["backup_dir"] = str(Path(path))
    save_settings(settings)


def ensure_backup_dir():
    backup_dir = get_backup_dir()
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir


def ps_text(command, timeout=120):
    return run_powershell(command, timeout=timeout)


def collect_pc_profile():
    profile = {
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "computer": socket.gethostname(),
        "user": os.getlogin(),
        "windows": ps_text("Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber,OSArchitecture,InstallDate | ConvertTo-Json"),
        "computer_system": ps_text("Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer,Model,TotalPhysicalMemory,UserName | ConvertTo-Json"),
        "cpu": ps_text("Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed | ConvertTo-Json"),
        "gpu": ps_text("Get-CimInstance Win32_VideoController | Select-Object Name,AdapterCompatibility,DriverVersion,DriverDate,AdapterRAM | ConvertTo-Json"),
        "disks": ps_text("Get-CimInstance Win32_LogicalDisk | Select-Object DeviceID,VolumeName,Size,FreeSpace,DriveType | ConvertTo-Json"),
        "network": run_command(["ipconfig"]),
        "java": run_command("where java & java -version", shell=True),
        "power_plan": run_command(["powercfg", "/getactivescheme"]),
        "downloads": DOWNLOAD_LINKS,
    }
    return profile


def export_pc_profile():
    backup_dir = ensure_backup_dir()
    profile = collect_pc_profile()
    json_path = backup_dir / f"pc-profile-{timestamp()}.json"
    txt_path = backup_dir / f"pc-profile-{timestamp()}.txt"

    json_path.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = []
    for key, value in profile.items():
        lines.append(f"=== {key} ===")
        lines.append(str(value))
        lines.append("")
    txt_path.write_text("\n".join(lines), encoding="utf-8")

    return f"Perfil exportado:\n{json_path}\n{txt_path}"


def minecraft_summary():
    lines = [f"Pasta Minecraft: {MINECRAFT_DIR}"]
    if not MINECRAFT_DIR.exists():
        return "Pasta .minecraft nao encontrada."

    for item in MINECRAFT_BACKUP_ITEMS:
        path = MINECRAFT_DIR / item
        if path.exists():
            if path.is_dir():
                count = sum(1 for _ in path.rglob("*"))
                lines.append(f"{item}: pasta encontrada ({count} itens)")
            else:
                lines.append(f"{item}: arquivo encontrado ({path.stat().st_size} bytes)")
        else:
            lines.append(f"{item}: nao encontrado")
    return "\n".join(lines)


def backup_minecraft():
    if not MINECRAFT_DIR.exists():
        return "Pasta .minecraft nao encontrada."

    backup_dir = ensure_backup_dir()
    zip_path = backup_dir / f"minecraft-backup-{timestamp()}.zip"
    included = 0

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for item in MINECRAFT_BACKUP_ITEMS:
            source = MINECRAFT_DIR / item
            if not source.exists():
                continue
            if source.is_dir():
                for file in source.rglob("*"):
                    if file.is_file():
                        archive.write(file, file.relative_to(MINECRAFT_DIR))
                        included += 1
            else:
                archive.write(source, source.relative_to(MINECRAFT_DIR))
                included += 1

    return f"Backup criado:\n{zip_path}\nArquivos incluidos: {included}"


def backup_minecraft_modding_only():
    if not MINECRAFT_DIR.exists():
        return "Pasta .minecraft nao encontrada."

    backup_dir = ensure_backup_dir()
    zip_path = backup_dir / f"minecraft-modding-{timestamp()}.zip"
    items = ["mods", "resourcepacks", "shaderpacks", "config", "defaultconfigs", "options.txt"]
    included = 0

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for item in items:
            source = MINECRAFT_DIR / item
            if not source.exists():
                continue
            if source.is_dir():
                for file in source.rglob("*"):
                    if file.is_file():
                        archive.write(file, file.relative_to(MINECRAFT_DIR))
                        included += 1
            else:
                archive.write(source, source.relative_to(MINECRAFT_DIR))
                included += 1

    return f"Backup de mods/config criado:\n{zip_path}\nArquivos incluidos: {included}"


def open_download_link(name):
    url = DOWNLOAD_LINKS[name]
    webbrowser.open(url)
    return f"Abrindo link:\n{name}\n{url}"


def open_parent_select_file(path):
    target = Path(path)
    if target.exists():
        os.startfile(str(target.parent))
        return f"Aberto: {target.parent}\nArquivo: {target.name}"
    return f"Arquivo nao encontrado: {target}"


def load_local_icon(path, size=(18, 18)):
    try:
        path = Path(path)
        if path.exists():
            return ctk.CTkImage(Image.open(path), size=size)
    except Exception:
        return None
    return None


def redragon_light_report():
    if not REDRAGON_LAYOUT.exists():
        return f"Layout nao encontrado:\n{REDRAGON_LAYOUT}"
    try:
        text = REDRAGON_LAYOUT.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return f"Erro lendo layout: {exc}"

    official_modes = []
    experimental_modes = []
    for mode in REDRAGON_LIGHT_MODES:
        marker = "experimental" if mode.get("experimental") else "oficial"
        item = (
            f"- {mode['name']} ({mode['english']}) | modo {mode['mode']} | "
            f"idioma {mode['lang']} | atributo {mode['attribute']} | {marker}"
        )
        if mode.get("experimental"):
            experimental_modes.append(item)
        else:
            official_modes.append(item)

    lines = [
        "Redragon M602P-KS / Griffin Pro",
        f"Software: {REDRAGON_EXE}",
        "",
        "Modos mapeados no Tweaks:",
        *official_modes,
        "",
        "Modos encontrados no idioma/layout, mas comentados no layout:",
        *experimental_modes,
        "",
        "Resumo extraido do layout:",
    ]
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned.startswith("<light") or cleaned.startswith("<info"):
            lines.append(cleaned)
    lines.append("")
    lines.append("Obs: isso mostra modos/limites da interface. Aplicar cor direto no mouse ainda depende do protocolo HID do software.")
    return "\n".join(lines)


def redragon_mode_by_name(mode_name):
    for mode in REDRAGON_LIGHT_MODES:
        if mode["name"] == mode_name:
            return mode
    return None


def create_redragon_light_preset(preset_name, mode_name, color, brightness, speed):
    mode = redragon_mode_by_name(mode_name)
    if not mode:
        return f"Modo nao encontrado: {mode_name}"

    REDRAGON_PRESET_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(ch if ch.isalnum() else "-" for ch in preset_name.lower()).strip("-")
    preset_file = REDRAGON_PRESET_DIR / f"{safe_name}.json"
    preset = {
        "mouse": "Redragon Griffin Pro M602P-KS",
        "preset": preset_name,
        "mode": mode,
        "color": color,
        "brightness_0_to_5": brightness,
        "speed_0_to_2": speed,
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "status": "recipe-only",
        "note": (
            "Este preset documenta o modo para aplicar no software Redragon. "
            "O envio direto ao mouse ainda depende de descobrir o arquivo/protocolo HID usado pelo DeviceDriver.exe."
        ),
    }
    preset_file.write_text(json.dumps(preset, indent=2, ensure_ascii=False), encoding="utf-8")

    experimental = "\nAviso: este modo e experimental no layout do mouse." if mode.get("experimental") else ""
    return (
        f"Preset salvo, mas ainda NAO aplicado no mouse:\n{preset_file}\n\n"
        f"Modo: {preset_name}\n"
        f"Tipo: {mode['name']} ({mode['english']})\n"
        f"Codigo interno: modo {mode['mode']}, atributo {mode['attribute']}\n"
        f"Cor: {color}\n"
        f"Brilho: {brightness}/5\n"
        f"Velocidade: {speed}/2"
        f"{experimental}\n\n"
        "Removi a abertura automatica do software Redragon. "
        "Para aplicar direto no mouse ainda precisamos descobrir o arquivo de perfil ou o protocolo HID usado pelo driver."
    )


def open_redragon_preset_folder():
    REDRAGON_PRESET_DIR.mkdir(parents=True, exist_ok=True)
    return open_target(str(REDRAGON_PRESET_DIR))


def backup_redragon_files():
    if not REDRAGON_DIR.exists():
        return f"Pasta Redragon nao encontrada:\n{REDRAGON_DIR}"
    return zip_existing_items(
        "redragon-m602pks",
        REDRAGON_DIR,
        ["config.xml", "layouts", "language"],
    )


def restart_redragon_software():
    command = (
        "taskkill /f /im DeviceDriver.exe >nul 2>&1 & "
        f"start \"\" \"{REDRAGON_EXE}\""
    )
    return run_command(command, shell=True, timeout=120)


class PhysicalMonitor(ctypes.Structure):
    _fields_ = [
        ("handle", wintypes.HANDLE),
        ("description", wintypes.WCHAR * 128),
    ]


def iter_physical_monitors():
    user32 = ctypes.windll.user32
    dxva2 = ctypes.windll.dxva2
    monitors = []

    monitor_enum_proc = ctypes.WINFUNCTYPE(
        wintypes.BOOL,
        wintypes.HMONITOR,
        wintypes.HDC,
        ctypes.POINTER(wintypes.RECT),
        wintypes.LPARAM,
    )

    def callback(hmonitor, hdc, rect, data):
        count = wintypes.DWORD()
        if not dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(hmonitor, ctypes.byref(count)):
            return True
        if count.value == 0:
            return True

        array_type = PhysicalMonitor * count.value
        physicals = array_type()
        if dxva2.GetPhysicalMonitorsFromHMONITOR(hmonitor, count, physicals):
            for monitor in physicals:
                monitors.append((monitor.handle, monitor.description))
        return True

    user32.EnumDisplayMonitors(None, None, monitor_enum_proc(callback), 0)
    return monitors


def monitor_brightness_report():
    dxva2 = ctypes.windll.dxva2
    monitors = iter_physical_monitors()
    if not monitors:
        return "Nenhum monitor fisico encontrado via DDC/CI."

    lines = []
    handles = []
    for handle, description in monitors:
        handles.append(handle)
        minimum = wintypes.DWORD()
        current = wintypes.DWORD()
        maximum = wintypes.DWORD()
        ok = dxva2.GetMonitorBrightness(handle, ctypes.byref(minimum), ctypes.byref(current), ctypes.byref(maximum))
        if ok:
            percent = round(((current.value - minimum.value) / max(1, maximum.value - minimum.value)) * 100)
            lines.append(f"{description}: brilho {percent}% (valor {current.value}, faixa {minimum.value}-{maximum.value})")
        else:
            lines.append(f"{description}: sem controle de brilho via DDC/CI.")

    if handles:
        array_type = wintypes.HANDLE * len(handles)
        dxva2.DestroyPhysicalMonitors(len(handles), array_type(*handles))
    return "\n".join(lines)


def set_monitor_brightness(percent):
    dxva2 = ctypes.windll.dxva2
    percent = max(0, min(100, int(percent)))
    monitors = iter_physical_monitors()
    if not monitors:
        return "Nenhum monitor fisico encontrado via DDC/CI."

    lines = []
    handles = []
    for handle, description in monitors:
        handles.append(handle)
        minimum = wintypes.DWORD()
        current = wintypes.DWORD()
        maximum = wintypes.DWORD()
        if not dxva2.GetMonitorBrightness(handle, ctypes.byref(minimum), ctypes.byref(current), ctypes.byref(maximum)):
            lines.append(f"{description}: sem controle de brilho via DDC/CI.")
            continue

        value = int(minimum.value + ((maximum.value - minimum.value) * percent / 100))
        if dxva2.SetMonitorBrightness(handle, value):
            lines.append(f"{description}: brilho ajustado para {percent}%")
        else:
            lines.append(f"{description}: falhou ao ajustar brilho.")

    if handles:
        array_type = wintypes.HANDLE * len(handles)
        dxva2.DestroyPhysicalMonitors(len(handles), array_type(*handles))
    return "\n".join(lines)


VCP_CONTROLS = {
    0x10: "Luz de fundo / Luminancia",
    0x12: "Contraste",
    0x14: "Preset de cor selecionado",
    0x16: "Ganho vermelho",
    0x18: "Ganho verde",
    0x1A: "Ganho azul",
    0x52: "Preset de cor ativo",
    0x54: "Temperatura de cor",
    0x60: "Fonte de entrada",
    0x62: "Volume",
    0x6C: "Nivel preto vermelho",
    0x6E: "Nivel preto verde",
    0x70: "Nivel preto azul",
    0x87: "Nitidez",
    0x8A: "Saturacao",
    0x8D: "Mute audio",
    0x90: "Matiz",
    0x92: "Nivel de preto",
    0xD6: "Modo energia",
}


def vcp_report():
    dxva2 = ctypes.windll.dxva2
    monitors = iter_physical_monitors()
    if not monitors:
        return "Nenhum monitor fisico encontrado via DDC/CI."

    lines = []
    handles = []
    for handle, description in monitors:
        handles.append(handle)
        lines.append(f"=== {description} ===")
        for code, name in VCP_CONTROLS.items():
            code_type = wintypes.DWORD()
            current = wintypes.DWORD()
            maximum = wintypes.DWORD()
            ok = dxva2.GetVCPFeatureAndVCPFeatureReply(
                handle,
                ctypes.c_ubyte(code),
                ctypes.byref(code_type),
                ctypes.byref(current),
                ctypes.byref(maximum),
            )
            if ok:
                lines.append(f"{name} (0x{code:02X}): atual {current.value}, max {maximum.value}")
            else:
                lines.append(f"{name} (0x{code:02X}): nao suportado/sem resposta")

    if handles:
        array_type = wintypes.HANDLE * len(handles)
        dxva2.DestroyPhysicalMonitors(len(handles), array_type(*handles))
    return "\n".join(lines)


def set_vcp_percent(code, percent):
    dxva2 = ctypes.windll.dxva2
    percent = max(0, min(100, int(percent)))
    monitors = iter_physical_monitors()
    if not monitors:
        return "Nenhum monitor fisico encontrado via DDC/CI."

    lines = []
    handles = []
    for handle, description in monitors:
        handles.append(handle)
        code_type = wintypes.DWORD()
        current = wintypes.DWORD()
        maximum = wintypes.DWORD()
        ok = dxva2.GetVCPFeatureAndVCPFeatureReply(
            handle,
            ctypes.c_ubyte(code),
            ctypes.byref(code_type),
            ctypes.byref(current),
            ctypes.byref(maximum),
        )
        if not ok or maximum.value == 0:
            lines.append(f"{description}: controle 0x{code:02X} sem suporte/resposta.")
            continue

        value = int(maximum.value * percent / 100)
        if dxva2.SetVCPFeature(handle, ctypes.c_ubyte(code), wintypes.DWORD(value)):
            lines.append(f"{description}: {VCP_CONTROLS.get(code, hex(code))} ajustado para {percent}% (valor {value})")
        else:
            lines.append(f"{description}: falhou ao ajustar controle 0x{code:02X}.")

    if handles:
        array_type = wintypes.HANDLE * len(handles)
        dxva2.DestroyPhysicalMonitors(len(handles), array_type(*handles))
    return "\n".join(lines)


def set_vcp_value(code, value):
    dxva2 = ctypes.windll.dxva2
    monitors = iter_physical_monitors()
    if not monitors:
        return "Nenhum monitor fisico encontrado via DDC/CI."

    lines = []
    handles = []
    for handle, description in monitors:
        handles.append(handle)
        if dxva2.SetVCPFeature(handle, ctypes.c_ubyte(code), wintypes.DWORD(int(value))):
            lines.append(f"{description}: {VCP_CONTROLS.get(code, hex(code))} definido como valor {value}")
        else:
            lines.append(f"{description}: falhou ao definir controle 0x{code:02X} como {value}.")

    if handles:
        array_type = wintypes.HANDLE * len(handles)
        dxva2.DestroyPhysicalMonitors(len(handles), array_type(*handles))
    return "\n".join(lines)


def set_rgb_gain(percent):
    parts = []
    for code in (0x16, 0x18, 0x1A):
        parts.append(set_vcp_percent(code, percent))
    return "\n\n".join(parts)


def confirm(title, text):
    return messagebox.askyesno(title, text)


class TweaksApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1180x760")
        self.minsize(780, 540)
        self.configure(bg=BG)
        self.overrideredirect(True)
        self._drag_start = None
        self._normal_geometry = None
        self._is_maximized = False
        self._set_icon()
        self._apply_theme()

        self.status_var = tk.StringVar()
        self.status_var.set("Pronto. Administrador: " + ("sim" if is_admin() else "nao"))

        self._build_ui()

    def _set_icon(self):
        icon_path = resource_path("tweaks_guipaluch.ico")
        if icon_path.exists():
            try:
                self.iconbitmap(str(icon_path))
            except tk.TclError:
                pass

    def _apply_theme(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.option_add("*Font", ("Segoe UI", 10))
        self.style.configure(".", background=BG, foreground=TEXT, fieldbackground=PANEL)
        self.style.configure("TFrame", background=BG)
        self.style.configure("Panel.TFrame", background=PANEL)
        self.style.configure("Sidebar.TFrame", background=SIDEBAR)
        self.style.configure("TLabel", background=BG, foreground=TEXT)
        self.style.configure("Muted.TLabel", background=BG, foreground=MUTED)
        self.style.configure("Title.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 19, "bold"))
        self.style.configure("SidebarTitle.TLabel", background=SIDEBAR, foreground=ACCENT_2, font=("Segoe UI", 11, "bold"))
        self.style.configure("SidebarMuted.TLabel", background=SIDEBAR, foreground=MUTED, font=("Segoe UI", 9))
        self.style.configure("Section.TLabel", background=PANEL, foreground=ACCENT, font=("Segoe UI", 12, "bold"))
        self.style.configure(
            "TButton",
            background=BUTTON,
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BUTTON,
            darkcolor=BUTTON,
            focusthickness=1,
            focuscolor=ACCENT,
            padding=(13, 10),
        )
        self.style.map(
            "TButton",
            background=[("active", BUTTON_ACTIVE), ("pressed", SURFACE_2)],
            foreground=[("disabled", MUTED), ("active", "#ffffff")],
        )
        self.style.configure(
            "TNotebook",
            background=BG,
            borderwidth=0,
            tabmargins=(0, 0, 0, 0),
        )
        self.style.configure(
            "TNotebook.Tab",
            background=PANEL_2,
            foreground=TEXT,
            padding=(14, 9),
            borderwidth=0,
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", SURFACE_2), ("active", HOVER)],
            foreground=[("selected", "#ffffff"), ("active", "#ffffff")],
        )
        self.style.configure("Vertical.TScrollbar", background=PANEL_2, troughcolor=BG, arrowcolor=TEXT)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.titlebar = ctk.CTkFrame(self, height=38, fg_color=TITLEBAR, corner_radius=0)
        self.titlebar.grid(row=0, column=0, sticky="ew")
        self.titlebar.grid_columnconfigure(1, weight=1)
        self.titlebar.bind("<Button-1>", self._start_drag)
        self.titlebar.bind("<B1-Motion>", self._drag_window)

        title = ctk.CTkLabel(
            self.titlebar,
            text="  " + APP_TITLE,
            font=("Segoe UI", 12, "bold"),
            text_color=TEXT,
        )
        title.grid(row=0, column=0, sticky="w", padx=(10, 0))
        title.bind("<Button-1>", self._start_drag)
        title.bind("<B1-Motion>", self._drag_window)

        admin_text = "Administrador" if is_admin() else "Sem admin"
        ctk.CTkLabel(
            self.titlebar,
            text=admin_text,
            font=("Segoe UI", 10),
            text_color=MUTED,
        ).grid(row=0, column=1, sticky="e", padx=(0, 12))

        for col, (text, command, hover) in enumerate([
            ("-", self._minimize_window, "#2a2a2a"),
            ("□", self._toggle_maximize, "#2a2a2a"),
            ("×", self.destroy, "#7f1d1d"),
        ], start=2):
            ctk.CTkButton(
                self.titlebar,
                text=text,
                width=40,
                height=28,
                corner_radius=8,
                fg_color="transparent",
                hover_color=hover,
                text_color=TEXT,
                font=("Segoe UI", 14),
                command=command,
            ).grid(row=0, column=col, padx=(0, 4), pady=4)

        shell = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        shell.grid(row=1, column=0, sticky="nsew", padx=12, pady=(10, 10))
        shell.grid_columnconfigure(1, weight=1)
        shell.grid_rowconfigure(0, weight=1)

        sidebar = ctk.CTkFrame(shell, width=220, fg_color=SURFACE, corner_radius=18)
        sidebar.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            sidebar,
            text="Tweaks",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT,
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(18, 0))
        ctk.CTkLabel(
            sidebar,
            text="GuiPaluch",
            font=("Segoe UI", 11),
            text_color=MUTED,
        ).grid(row=1, column=0, sticky="w", padx=18, pady=(0, 14))

        self.nav_frame = ctk.CTkScrollableFrame(sidebar, fg_color="transparent", corner_radius=0)
        self.nav_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

        right = ctk.CTkFrame(shell, fg_color=BG, corner_radius=0)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(0, weight=1)

        self.pages = {}
        self.nav_buttons = {}
        self.nav_images = []
        self.current_page = None
        self.content_area = ctk.CTkFrame(right, fg_color=PANEL, corner_radius=18)
        self.content_area.grid(row=0, column=0, sticky="nsew")
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        self.log = ctk.CTkTextbox(
            right,
            height=126,
            corner_radius=18,
            fg_color=LOG_BG,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT,
            font=("Cascadia Mono", 10),
        )
        self.log.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        self.log.insert("end", "Logs aparecerao aqui.\n")

        status = ctk.CTkLabel(
            self,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            text_color=MUTED,
            anchor="w",
        )
        status.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 8))

        self._add_sections()
        if self.pages:
            first_page = next(iter(self.pages))
            self._show_page(first_page)

    def _start_drag(self, event):
        self._drag_start = (event.x_root, event.y_root, self.winfo_x(), self.winfo_y())

    def _drag_window(self, event):
        if not self._drag_start or self._is_maximized:
            return
        start_x, start_y, win_x, win_y = self._drag_start
        self.geometry(f"+{win_x + event.x_root - start_x}+{win_y + event.y_root - start_y}")

    def _minimize_window(self):
        self.overrideredirect(False)
        self.iconify()
        self.after(150, lambda: self.overrideredirect(True))

    def _toggle_maximize(self):
        if self._is_maximized:
            if self._normal_geometry:
                self.geometry(self._normal_geometry)
            self._is_maximized = False
            return

        self._normal_geometry = self.geometry()
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight() - 40
        self.geometry(f"{width}x{height}+0+0")
        self._is_maximized = True

    def _add_sections(self):
        cleanup = self._tab("Limpeza")
        self._section(cleanup, "Arquivos temporarios e caches", [
            ("Limpeza rapida: Temp + %TEMP% + Prefetch", lambda: self.run_task(quick_temp_prefetch_cleanup)),
            ("Limpar shader/cache AMD + DirectX", self.confirm_clear_extra_caches),
            ("Limpar C:\\Windows\\Temp", lambda: self.run_task(remove_contents, r"C:\Windows\Temp")),
            ("Limpar %TEMP%", lambda: self.run_task(remove_contents, tempfile.gettempdir())),
            ("Limpar Prefetch", lambda: self.run_task(remove_contents, r"C:\Windows\Prefetch")),
            ("Esvaziar lixeira", self.empty_recycle_bin),
            ("Limpeza de disco", self.cleanmgr),
            ("Limpar cache Windows Update", self.clear_windows_update_cache),
            ("Limpar miniaturas", self.clear_thumbnails),
            ("Limpar cache Microsoft Store", self.clear_store_cache),
            ("Limpar caches dos navegadores", self.clear_browser_caches),
        ])

        security = self._tab("Seguranca")
        self._section(security, "Defender", [
            ("Desativar antivirus", self.disable_defender),
            ("Ativar antivirus", self.enable_defender),
            ("Abrir Windows Defender", lambda: self.run_task(open_target, "windowsdefender:")),
            ("Status do Defender", self.defender_status),
            ("Scan rapido com Defender", self.defender_quick_scan),
            ("Scan completo com Defender", self.defender_full_scan),
        ])

        network = self._tab("Rede")
        self._section(network, "Conexao", [
            ("Limpar cache DNS", lambda: self.run_task(run_command, ["ipconfig", "/flushdns"])),
            ("Espelhar em TV/dispositivo sem fio", self.open_wireless_display),
            ("Configuracoes de projecao", lambda: self.run_task(open_target, "ms-settings:project")),
            ("Adicionar dispositivo Bluetooth/tela", lambda: self.run_task(open_target, "ms-settings:bluetooth")),
            ("Configuracoes de tela", lambda: self.run_task(open_target, "ms-settings:display")),
            ("Abrir Win+P / projetar", lambda: self.run_task(open_target, "DisplaySwitch.exe")),
            ("Diagnostico Miracast/Wi-Fi", lambda: self.run_task(miracast_diagnostics)),
            ("Diagnostico de internet", lambda: self.run_task(network_diagnostics)),
            ("Resetar rede", self.reset_network),
        ])

        display = self._tab("Tela")
        self._section(display, "Monitor DDC/CI", [
            ("Relatorio DDC/CI completo", lambda: self.run_task(vcp_report)),
            ("Luz atual / luminancia", lambda: self.run_task(monitor_brightness_report)),
        ])
        self._section(display, "Luz de fundo / luminancia", [
            ("Luz de fundo 20%", lambda: self.run_task(set_vcp_percent, 0x10, 20)),
            ("Luz de fundo 40%", lambda: self.run_task(set_vcp_percent, 0x10, 40)),
            ("Luz de fundo 60%", lambda: self.run_task(set_vcp_percent, 0x10, 60)),
            ("Luz de fundo 80%", lambda: self.run_task(set_vcp_percent, 0x10, 80)),
            ("Luz de fundo 100%", lambda: self.run_task(set_vcp_percent, 0x10, 100)),
        ])
        self._section(display, "Contraste / nitidez / cor", [
            ("Contraste 40%", lambda: self.run_task(set_vcp_percent, 0x12, 40)),
            ("Contraste 50%", lambda: self.run_task(set_vcp_percent, 0x12, 50)),
            ("Contraste 60%", lambda: self.run_task(set_vcp_percent, 0x12, 60)),
            ("Contraste 80%", lambda: self.run_task(set_vcp_percent, 0x12, 80)),
            ("Contraste 100%", lambda: self.run_task(set_vcp_percent, 0x12, 100)),
            ("Nitidez 25%", lambda: self.run_task(set_vcp_percent, 0x87, 25)),
            ("Nitidez 50%", lambda: self.run_task(set_vcp_percent, 0x87, 50)),
            ("Nitidez 75%", lambda: self.run_task(set_vcp_percent, 0x87, 75)),
            ("Saturacao 25%", lambda: self.run_task(set_vcp_percent, 0x8A, 25)),
            ("Saturacao 50%", lambda: self.run_task(set_vcp_percent, 0x8A, 50)),
            ("Saturacao 75%", lambda: self.run_task(set_vcp_percent, 0x8A, 75)),
            ("Matiz 25%", lambda: self.run_task(set_vcp_percent, 0x90, 25)),
            ("Matiz 50%", lambda: self.run_task(set_vcp_percent, 0x90, 50)),
            ("Matiz 75%", lambda: self.run_task(set_vcp_percent, 0x90, 75)),
            ("Nivel de preto 25%", lambda: self.run_task(set_vcp_percent, 0x92, 25)),
            ("Nivel de preto 50%", lambda: self.run_task(set_vcp_percent, 0x92, 50)),
            ("Nivel de preto 75%", lambda: self.run_task(set_vcp_percent, 0x92, 75)),
        ])
        self._section(display, "Ganhos RGB / temperatura", [
            ("RGB ganho 40%", lambda: self.run_task(set_rgb_gain, 40)),
            ("RGB ganho 50%", lambda: self.run_task(set_rgb_gain, 50)),
            ("RGB ganho 60%", lambda: self.run_task(set_rgb_gain, 60)),
            ("RGB ganho 80%", lambda: self.run_task(set_rgb_gain, 80)),
            ("Vermelho 50%", lambda: self.run_task(set_vcp_percent, 0x16, 50)),
            ("Verde 50%", lambda: self.run_task(set_vcp_percent, 0x18, 50)),
            ("Azul 50%", lambda: self.run_task(set_vcp_percent, 0x1A, 50)),
            ("Preset cor 6500K", lambda: self.run_task(set_vcp_value, 0x14, 5)),
            ("Preset cor 9300K", lambda: self.run_task(set_vcp_value, 0x14, 8)),
            ("Preset cor usuario", lambda: self.run_task(set_vcp_value, 0x14, 11)),
        ])
        self._section(display, "Nivel preto RGB", [
            ("Preto vermelho 40%", lambda: self.run_task(set_vcp_percent, 0x6C, 40)),
            ("Preto vermelho 50%", lambda: self.run_task(set_vcp_percent, 0x6C, 50)),
            ("Preto vermelho 60%", lambda: self.run_task(set_vcp_percent, 0x6C, 60)),
            ("Preto verde 40%", lambda: self.run_task(set_vcp_percent, 0x6E, 40)),
            ("Preto verde 50%", lambda: self.run_task(set_vcp_percent, 0x6E, 50)),
            ("Preto verde 60%", lambda: self.run_task(set_vcp_percent, 0x6E, 60)),
            ("Preto azul 40%", lambda: self.run_task(set_vcp_percent, 0x70, 40)),
            ("Preto azul 50%", lambda: self.run_task(set_vcp_percent, 0x70, 50)),
            ("Preto azul 60%", lambda: self.run_task(set_vcp_percent, 0x70, 60)),
        ])
        self._section(display, "Audio do monitor / energia", [
            ("Volume monitor 0%", lambda: self.run_task(set_vcp_percent, 0x62, 0)),
            ("Volume monitor 25%", lambda: self.run_task(set_vcp_percent, 0x62, 25)),
            ("Volume monitor 50%", lambda: self.run_task(set_vcp_percent, 0x62, 50)),
            ("Volume monitor 100%", lambda: self.run_task(set_vcp_percent, 0x62, 100)),
            ("Mute audio monitor", lambda: self.run_task(set_vcp_value, 0x8D, 1)),
            ("Desmutar audio monitor", lambda: self.run_task(set_vcp_value, 0x8D, 2)),
        ])
        self._section(display, "Windows / HDR / Projecao", [
            ("Configuracoes de tela", lambda: self.run_task(open_target, "ms-settings:display")),
            ("HDR do Windows", lambda: self.run_task(open_target, "ms-settings:display-advancedgraphics")),
            ("Luz noturna", lambda: self.run_task(open_target, "ms-settings:nightlight")),
            ("Abrir Win+P / projetar", lambda: self.run_task(open_target, "DisplaySwitch.exe")),
        ])

        bluetooth = self._tab("Bluetooth")
        self._section(bluetooth, "Conexao e audio Bluetooth", [
            ("Abrir Bluetooth", lambda: self.run_task(open_target, "ms-settings:bluetooth")),
            ("Adicionar dispositivo", lambda: self.run_task(open_target, "ms-settings:bluetooth")),
            ("Dispositivos conectados", lambda: self.run_task(open_target, "ms-settings:connecteddevices")),
            ("Config de som", lambda: self.run_task(open_target, "ms-settings:sound")),
            ("Painel de sons classico", lambda: self.run_task(open_target, "mmsys.cpl")),
            ("Diagnostico Bluetooth", lambda: self.run_task(bluetooth_diagnostics)),
            ("Reset Bluetooth", self.confirm_restart_bluetooth),
            ("Reset audio Windows", self.confirm_restart_audio),
            ("Gerenciador de Dispositivos", lambda: self.run_task(open_target, "devmgmt.msc")),
            ("Servicos do Windows", lambda: self.run_task(open_target, "services.msc")),
        ])

        redragon = self._tab("Redragon")
        self._section(redragon, "Mouse Griffin Pro M602P-KS", [
            ("Abrir software Redragon", lambda: self.run_task(open_target, str(REDRAGON_EXE))),
            ("Reiniciar software Redragon", lambda: self.run_task(restart_redragon_software)),
            ("Abrir pasta do software", lambda: self.run_task(open_target, str(REDRAGON_DIR))),
            ("Abrir config.xml", lambda: self.run_task(open_target, str(REDRAGON_CONFIG))),
            ("Abrir layout MOUSE_DM204", lambda: self.run_task(open_target, str(REDRAGON_LAYOUT))),
            ("Relatorio de luz/modos", lambda: self.run_task(redragon_light_report)),
            ("Backup configs Redragon", lambda: self.run_task(backup_redragon_files)),
            ("Site Redragon", lambda: self.run_task(open_target, "https://www.redragon.com.br/")),
        ])
        self._section(redragon, "Modos de luz oficiais", [
            ("Fixo / Steady", lambda: self.run_task(create_redragon_light_preset, "Fixo branco", "Fixo", "#FFFFFF", 5, 1)),
            ("Respiracao / Breathing", lambda: self.run_task(create_redragon_light_preset, "Respirar azul", "Respiracao", "#006CFF", 4, 2)),
            ("Fluxo / Flowing light", lambda: self.run_task(create_redragon_light_preset, "Fluxo RGB", "Fluxo", "RGB", 5, 2)),
            ("Neon", lambda: self.run_task(create_redragon_light_preset, "Neon RGB", "Neon", "RGB", 5, 2)),
            ("Corrida / Horse Racing", lambda: self.run_task(create_redragon_light_preset, "Corrida RGB", "Corrida", "RGB", 5, 2)),
            ("Respiracao misturada", lambda: self.run_task(create_redragon_light_preset, "Respiracao misturada RGB", "Respiracao misturada", "RGB", 5, 2)),
            ("Desligar luz", lambda: self.run_task(create_redragon_light_preset, "Apagar luz", "Luz desligada", "OFF", 0, 0)),
        ])
        self._section(redragon, "Cores prontas", [
            ("Branco fixo", lambda: self.run_task(create_redragon_light_preset, "Fixo branco", "Fixo", "#FFFFFF", 5, 1)),
            ("Vermelho fixo", lambda: self.run_task(create_redragon_light_preset, "Fixo vermelho", "Fixo", "#FF0000", 5, 1)),
            ("Verde fixo", lambda: self.run_task(create_redragon_light_preset, "Fixo verde", "Fixo", "#00FF00", 5, 1)),
            ("Azul fixo", lambda: self.run_task(create_redragon_light_preset, "Fixo azul", "Fixo", "#006CFF", 5, 1)),
            ("Ciano fixo", lambda: self.run_task(create_redragon_light_preset, "Fixo ciano", "Fixo", "#00E5FF", 5, 1)),
            ("Roxo fixo", lambda: self.run_task(create_redragon_light_preset, "Fixo roxo", "Fixo", "#8B5CF6", 5, 1)),
            ("Rosa fixo", lambda: self.run_task(create_redragon_light_preset, "Fixo rosa", "Fixo", "#FF4FD8", 5, 1)),
            ("Amarelo fixo", lambda: self.run_task(create_redragon_light_preset, "Fixo amarelo", "Fixo", "#FFD000", 5, 1)),
        ])
        self._section(redragon, "Modos experimentais do layout", [
            ("Musica / Music", lambda: self.run_task(create_redragon_light_preset, "Musica experimental", "Musica", "RGB", 5, 2)),
            ("Ambilight", lambda: self.run_task(create_redragon_light_preset, "Ambilight experimental", "Ambilight", "RGB", 5, 2)),
            ("Abrir pasta de presets", lambda: self.run_task(open_redragon_preset_folder)),
            ("Relatorio completo", lambda: self.run_task(redragon_light_report)),
        ])

        folders = self._tab("Pastas")
        self._section(folders, "Menu Iniciar e atalhos", [
            ("Menu Iniciar do usuario", lambda: self.run_task(open_target, str(USER_START_MENU))),
            ("Menu Iniciar todos usuarios", lambda: self.run_task(open_target, str(COMMON_START_MENU))),
            ("Atualizar Menu Iniciar", self.restart_explorer),
            ("Inicializar com Windows usuario", lambda: self.run_task(open_target, str(USER_STARTUP))),
            ("Inicializar com Windows todos", lambda: self.run_task(open_target, str(COMMON_STARTUP))),
            ("Enviar para", lambda: self.run_task(open_target, str(SEND_TO))),
            ("Quick Launch", lambda: self.run_task(open_target, str(QUICK_LAUNCH))),
        ])
        self._section(folders, "Pastas do usuario", [
            ("Desktop", lambda: self.run_task(open_target, str(DESKTOP))),
            ("Downloads", lambda: self.run_task(open_target, str(Path.home() / "Downloads"))),
            ("Documentos", lambda: self.run_task(open_target, str(Path.home() / "Documents"))),
            ("AppData Roaming", lambda: self.run_task(open_target, os.environ.get("APPDATA", ""))),
            ("AppData Local", lambda: self.run_task(open_target, os.environ.get("LOCALAPPDATA", ""))),
            ("Temp do usuario", lambda: self.run_task(open_target, tempfile.gettempdir())),
        ])
        self._section(folders, "Pastas do sistema", [
            ("Raiz do disco C:", lambda: self.run_task(open_target, r"C:\\")),
            ("ProgramData", lambda: self.run_task(open_target, os.environ.get("PROGRAMDATA", r"C:\ProgramData"))),
            ("Program Files", lambda: self.run_task(open_target, os.environ.get("ProgramFiles", r"C:\Program Files"))),
            ("Program Files x86", lambda: self.run_task(open_target, os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"))),
            ("Windows", lambda: self.run_task(open_target, os.environ.get("WINDIR", r"C:\Windows"))),
            ("System32", lambda: self.run_task(open_target, r"C:\Windows\System32")),
            ("Drivers etc / hosts", lambda: self.run_task(open_parent_select_file, HOSTS_FILE)),
            ("Windows Temp", lambda: self.run_task(open_target, r"C:\Windows\Temp")),
            ("Prefetch", lambda: self.run_task(open_target, r"C:\Windows\Prefetch")),
        ])
        self._section(folders, "Jogos e saves", [
            ("Saved Games", lambda: self.run_task(open_target, str(SAVED_GAMES))),
            ("Documents\\My Games", lambda: self.run_task(open_target, str(MY_GAMES))),
            ("Steam userdata", lambda: self.run_task(open_target, str(STEAM_USERDATA))),
            ("Steam games/common", lambda: self.run_task(open_target, str(STEAM_COMMON))),
            ("Epic ProgramData", lambda: self.run_task(open_target, str(EPIC_PROGRAMDATA))),
            ("Rockstar Documents", lambda: self.run_task(open_target, str(ROCKSTAR_DOCUMENTS))),
            ("Battle.net ProgramData", lambda: self.run_task(open_target, str(BATTLE_NET_PROGRAMDATA))),
        ])

        repair = self._tab("Reparo")
        self._section(repair, "Windows e disco", [
            ("Verificar arquivos do Windows (SFC)", self.sfc_scan),
            ("Reparar imagem do Windows (DISM)", self.dism_restore),
            ("Verificar disco", self.check_disk),
            ("Otimizar unidades", lambda: self.run_task(open_target, "dfrgui")),
            ("Gerenciamento de Disco", lambda: self.run_task(open_target, "diskmgmt.msc")),
            ("Visualizador de Eventos", lambda: self.run_task(open_target, "eventvwr.msc")),
            ("Ultimos erros criticos", lambda: self.run_task(self.recent_critical_events)),
        ])

        system = self._tab("Sistema")
        self._section(system, "Ferramentas do sistema", [
            ("Abrir Gerenciador de Tarefas", lambda: self.run_task(open_target, "taskmgr")),
            ("Gerenciador de Dispositivos", lambda: self.run_task(open_target, "devmgmt.msc")),
            ("Servicos", lambda: self.run_task(open_target, "services.msc")),
            ("Agendador de Tarefas", lambda: self.run_task(open_target, "taskschd.msc")),
            ("MSConfig", lambda: self.run_task(open_target, "msconfig")),
            ("Apps que iniciam com Windows", lambda: self.run_task(open_target, "ms-settings:startupapps")),
            ("Apps instalados", lambda: self.run_task(open_target, "ms-settings:appsfeatures")),
            ("Criar ponto de restauracao", self.create_restore_point),
            ("Abrir restauracao do sistema", lambda: self.run_task(open_target, "rstrui")),
            ("Informacoes do PC", self.pc_info),
            ("Listar programas instalados", self.list_installed_programs),
            ("Listar processos pesados", self.list_heavy_processes),
            ("Reiniciar Explorer", self.restart_explorer),
            ("Plano Alto Desempenho", self.high_performance_plan),
            ("Plano Equilibrado", self.balanced_plan),
            ("Opcoes de energia avancadas", lambda: self.run_task(run_command, "control.exe powercfg.cpl,,3", True, 120)),
            ("Desativar hibernacao", self.disable_hibernation),
            ("Desempenho visual", lambda: self.run_task(open_target, "SystemPropertiesPerformance.exe")),
            ("Config Xbox Game Bar", lambda: self.run_task(open_target, "ms-settings:gaming-gamebar")),
            ("Capturas/Game DVR", lambda: self.run_task(open_target, "ms-settings:gaming-gamedvr")),
            ("Desativar apps em segundo plano", lambda: self.run_task(open_target, "ms-settings:privacy-backgroundapps")),
            ("Abrir privacidade", lambda: self.run_task(open_target, "ms-settings:privacy")),
        ])

        pc = self._tab("Meu PC")
        self._section(pc, "Diagnostico e perfil desta maquina", [
            ("Resumo do PC", self.pc_info),
            ("Status da GPU/driver", self.gpu_status),
            ("Exportar perfil pos-formatacao", lambda: self.run_task(export_pc_profile)),
            ("Mostrar pasta de backup atual", self.show_backup_folder),
            ("Mudar pasta de backup", self.choose_backup_folder),
            ("Voltar backup para D:", self.reset_backup_folder),
            ("Abrir pasta de backups", self.open_backup_folder),
            ("Listar drivers instalados", self.list_installed_drivers),
            ("Listar servicos ativos", self.list_running_services),
            ("Backup Menu Iniciar", lambda: self.run_task(backup_start_menu_shortcuts)),
            ("Backup Area de Trabalho", lambda: self.run_task(backup_folder_contents, "desktop-backup", DESKTOP)),
        ])

        games = self._tab("Jogos")
        self._section(games, "Backups e pastas de saves", [
            ("Backup Saved Games", lambda: self.run_task(backup_folder_contents, "saved-games-backup", SAVED_GAMES)),
            ("Backup Documents\\My Games", lambda: self.run_task(backup_folder_contents, "my-games-backup", MY_GAMES)),
            ("Backup Steam userdata", lambda: self.run_task(backup_folder_contents, "steam-userdata-backup", STEAM_USERDATA)),
            ("Backup Rockstar Documents", lambda: self.run_task(backup_folder_contents, "rockstar-games-backup", ROCKSTAR_DOCUMENTS)),
            ("Abrir Saved Games", lambda: self.run_task(open_target, str(SAVED_GAMES))),
            ("Abrir Steam userdata", lambda: self.run_task(open_target, str(STEAM_USERDATA))),
            ("Abrir Rockstar", lambda: self.run_task(open_target, str(ROCKSTAR_DOCUMENTS))),
            ("Abrir Battle.net", lambda: self.run_task(open_target, str(BATTLE_NET_PROGRAMDATA))),
        ])
        self._section(games, "Presets de jogo", [
            ("Antes de jogar", self.preset_before_gaming),
            ("Depois de jogar", self.preset_after_gaming),
            ("Preparar Forza6", self.preset_forza6),
        ])

        downloads = self._tab("Downloads")
        self._section(downloads, "Drivers e ferramentas essenciais", [
            ("AMD RX 580 drivers oficiais", lambda: self.run_task(open_download_link, "AMD RX 580 drivers oficiais")),
            ("AMD primeiro estavel 23.11.1", lambda: self.run_task(open_download_link, "AMD RX580 primeiro estavel - 23.11.1 Polaris/Vega")),
            ("AMD estavel Forza6 23.10.01.14", lambda: self.run_task(open_download_link, "AMD RX580 estavel para Forza6 - 23.10.01.14")),
            ("Notas AMD 23.10.01.14", lambda: self.run_task(open_download_link, "AMD 23.10.01.14 notas oficiais")),
            ("DDU", lambda: self.run_task(open_download_link, "Display Driver Uninstaller (DDU)")),
            ("Git for Windows", lambda: self.run_task(open_download_link, "Git for Windows")),
            ("Visual Studio Code", lambda: self.run_task(open_download_link, "Visual Studio Code")),
            ("7-Zip", lambda: self.run_task(open_download_link, "7-Zip")),
        ])
        self._section(downloads, "Minecraft e Java", [
            ("Java 8", lambda: self.run_task(open_download_link, "Temurin Java 8")),
            ("Java 17", lambda: self.run_task(open_download_link, "Temurin Java 17")),
            ("Java 21", lambda: self.run_task(open_download_link, "Temurin Java 21")),
            ("Java 25", lambda: self.run_task(open_download_link, "Temurin Java 25")),
            ("Minecraft Launcher", lambda: self.run_task(open_download_link, "Minecraft Launcher")),
            ("Prism Launcher", lambda: self.run_task(open_download_link, "Prism Launcher")),
            ("Forge", lambda: self.run_task(open_download_link, "Forge")),
            ("NeoForge", lambda: self.run_task(open_download_link, "NeoForge")),
            ("Fabric", lambda: self.run_task(open_download_link, "Fabric")),
            ("Modrinth App", lambda: self.run_task(open_download_link, "Modrinth App")),
            ("CurseForge App", lambda: self.run_task(open_download_link, "CurseForge App")),
        ])

        minecraft = self._tab("Minecraft")
        self._section(minecraft, "Backups e modding", [
            ("Resumo da .minecraft", lambda: self.run_task(minecraft_summary)),
            ("Backup completo .minecraft", self.confirm_backup_minecraft),
            ("Backup mods/configs", lambda: self.run_task(backup_minecraft_modding_only)),
            ("Backup mundos/saves", lambda: self.run_task(backup_folder_contents, "minecraft-worlds", MINECRAFT_DIR / "saves")),
            ("Listar mods atuais", lambda: self.run_task(list_minecraft_mods)),
            ("Limpar logs/crash/cache", self.confirm_minecraft_clean_logs),
            ("Abrir ultimo crash report", lambda: self.run_task(minecraft_latest_crash_report)),
            ("Ver Java instalado", lambda: self.run_task(java_versions_report)),
            ("Abrir .minecraft", lambda: self.run_task(open_target, str(MINECRAFT_DIR))),
            ("Abrir mods", lambda: self.run_task(open_target, str(MINECRAFT_DIR / "mods"))),
            ("Abrir resourcepacks", lambda: self.run_task(open_target, str(MINECRAFT_DIR / "resourcepacks"))),
            ("Abrir shaderpacks", lambda: self.run_task(open_target, str(MINECRAFT_DIR / "shaderpacks"))),
            ("Abrir saves", lambda: self.run_task(open_target, str(MINECRAFT_DIR / "saves"))),
            ("Restaurar backup .zip", self.restore_minecraft_backup),
            ("Abrir logs", lambda: self.run_task(open_target, str(MINECRAFT_DIR / "logs"))),
        ])

        post = self._tab("Pos-formatacao")
        self._section(post, "Checklist automatico", [
            ("Exportar tudo que der para lembrar", lambda: self.run_task(export_pc_profile)),
            ("Pacote pos-formatacao completo", self.confirm_post_format_bundle),
            ("Backup atalhos Menu Iniciar", lambda: self.run_task(backup_start_menu_shortcuts)),
            ("Backup Area de Trabalho", lambda: self.run_task(backup_folder_contents, "desktop-backup", DESKTOP)),
            ("Criar backup Minecraft agora", self.confirm_backup_minecraft),
            ("Abrir downloads essenciais", self.open_essential_downloads),
            ("Criar ponto de restauracao", self.create_restore_point),
            ("Plano Alto Desempenho", self.high_performance_plan),
            ("Abrir apps de inicializacao", lambda: self.run_task(open_target, "ms-settings:startupapps")),
            ("Abrir privacidade", lambda: self.run_task(open_target, "ms-settings:privacy")),
            ("Abrir programas instalados", lambda: self.run_task(open_target, "ms-settings:appsfeatures")),
        ])

        presets = self._tab("Presets")
        self._section(presets, "Rotinas prontas", [
            ("Manutencao rapida", self.preset_quick_maintenance),
            ("Antes de jogar", self.preset_before_gaming),
            ("Depois de jogar", self.preset_after_gaming),
            ("Minecraft modding", self.preset_minecraft_modding),
            ("Pos-formatacao completo", self.confirm_post_format_bundle),
        ])

    def _tab(self, title):
        outer = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color=PANEL,
            corner_radius=18,
            scrollbar_button_color=SURFACE_2,
            scrollbar_button_hover_color=HOVER,
        )
        self.pages[title] = outer

        icons = {
            "Limpeza": "⌁",
            "Seguranca": "◈",
            "Rede": "⌘",
            "Tela": "◐",
            "Bluetooth": "⌁",
            "Redragon": "▰",
            "Pastas": "▣",
            "Reparo": "◇",
            "Sistema": "⚙",
            "Meu PC": "▰",
            "Jogos": "▶",
            "Downloads": "↓",
            "Minecraft": "■",
            "Pos-formatacao": "✓",
            "Presets": "✦",
        }
        icon_files = {
            "Limpeza": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_brightness_up.png",
            "Seguranca": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_config.png",
            "Rede": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_pc.png",
            "Tela": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_brightness_up.png",
            "Bluetooth": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_bluetooth.png",
            "Redragon": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_mouse.png",
            "Pastas": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_file.png",
            "Reparo": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_config.png",
            "Sistema": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_pc.png",
            "Meu PC": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_pc.png",
            "Jogos": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_playpause.png",
            "Downloads": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_file.png",
            "Minecraft": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_customlayout.png",
            "Pos-formatacao": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_cal.png",
            "Presets": REDRAGON_DIR / "skins" / "theme1" / "icon" / "icon_lightmode.png",
        }
        nav_text = f"{icons.get(title, '•')}  {title}"
        image = None
        if image:
            self.nav_images.append(image)
            nav_text = title
        button = ctk.CTkButton(
            self.nav_frame,
            text=nav_text,
            image=image,
            compound="left",
            anchor="w",
            height=38,
            corner_radius=12,
            fg_color="transparent",
            hover_color=SURFACE_2,
            text_color=TEXT,
            font=("Segoe UI", 12),
            command=lambda page=title: self._show_page(page),
        )
        button.pack(fill="x", padx=2, pady=4)
        self.nav_buttons[title] = button
        return outer

    def _show_page(self, title):
        if title not in self.pages:
            return
        if self.current_page:
            self.pages[self.current_page].grid_remove()
            self.nav_buttons[self.current_page].configure(fg_color="transparent", text_color=TEXT)
        self.pages[title].grid(row=0, column=0, sticky="nsew", padx=14, pady=14)
        self.current_page = title
        self.nav_buttons[title].configure(fg_color=SURFACE_2, text_color="#ffffff")

    def _section(self, parent, title, buttons):
        section = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=18)
        section.pack(fill="x", padx=4, pady=(4, 14))
        section.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(
            section,
            text=title,
            anchor="w",
            font=("Segoe UI", 13, "bold"),
            text_color=TEXT,
        )
        label.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))

        grid = ctk.CTkFrame(section, fg_color="transparent")
        grid.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))

        button_widgets = []
        for index, (text, command) in enumerate(buttons):
            button = ctk.CTkButton(
                grid,
                text=text,
                command=command,
                height=42,
                corner_radius=14,
                fg_color=SURFACE_2,
                hover_color=HOVER,
                border_width=1,
                border_color=BORDER,
                text_color=TEXT,
                font=("Segoe UI", 11),
            )
            button_widgets.append(button)

        def layout(event=None):
            width = grid.winfo_width()
            if width < 620:
                columns = 1
            elif width < 940:
                columns = 2
            else:
                columns = 3

            for child in button_widgets:
                child.grid_forget()
            for col in range(3):
                grid.columnconfigure(col, weight=0)
            for col in range(columns):
                grid.columnconfigure(col, weight=1, uniform="actions")
            for index, button in enumerate(button_widgets):
                row = index // columns
                col = index % columns
                button.grid(row=row, column=col, sticky="ew", padx=6, pady=6)

        grid.bind("<Configure>", layout)
        self.after(50, layout)

    def append_log(self, title, text):
        self.log.insert("end", f"\n=== {title} ===\n{text}\n")
        self.log.see("end")
        self.status_var.set(title + " concluido.")

    def run_task(self, func, *args):
        title = getattr(func, "__name__", "Acao")
        if args:
            title = str(args[0]) if isinstance(args[0], str) else title
        self.status_var.set("Executando...")

        def worker():
            try:
                result = func(*args)
            except Exception as exc:
                result = f"Erro: {exc}"
            self.after(0, lambda: self.append_log(title, result))

        threading.Thread(target=worker, daemon=True).start()

    def enable_defender(self):
        command = (
            "Set-MpPreference -DisableRealtimeMonitoring $false; "
            "Set-MpPreference -DisableBehaviorMonitoring $false; "
            "Set-MpPreference -DisableBlockAtFirstSeen $false; "
            "Set-MpPreference -DisableIOAVProtection $false; "
            "Start-Service -Name WinDefend -ErrorAction SilentlyContinue"
        )
        self.run_task(run_powershell, command)

    def disable_defender(self):
        if confirm("Desativar antivirus", "Tem certeza que deseja desativar a protecao em tempo real do Defender?"):
            self.run_task(run_powershell, "Set-MpPreference -DisableRealtimeMonitoring $true")

    def defender_status(self):
        command = (
            "Get-MpComputerStatus | Select-Object "
            "AMServiceEnabled,AntivirusEnabled,RealTimeProtectionEnabled,BehaviorMonitorEnabled,"
            "AntispywareEnabled,FullScanAge,QuickScanAge | Format-List"
        )
        self.run_task(run_powershell, command)

    def defender_quick_scan(self):
        self.run_task(run_powershell, "Start-MpScan -ScanType QuickScan", 7200)

    def defender_full_scan(self):
        if confirm("Scan completo", "Scan completo pode demorar bastante. Deseja iniciar?"):
            self.run_task(run_powershell, "Start-MpScan -ScanType FullScan", 21600)

    def empty_recycle_bin(self):
        self.run_task(run_powershell, "Clear-RecycleBin -Force -ErrorAction SilentlyContinue")

    def cleanmgr(self):
        self.run_task(open_target, "cleanmgr")

    def clear_windows_update_cache(self):
        if not confirm("Windows Update", "Parar servicos e limpar o cache do Windows Update?"):
            return
        command = (
            "Stop-Service wuauserv,bits -Force -ErrorAction SilentlyContinue; "
            "Remove-Item -Path $env:windir\\SoftwareDistribution\\Download\\* -Recurse -Force -ErrorAction SilentlyContinue; "
            "Start-Service bits -ErrorAction SilentlyContinue; "
            "Start-Service wuauserv -ErrorAction SilentlyContinue"
        )
        self.run_task(run_powershell, command)

    def clear_thumbnails(self):
        command = (
            "Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue; "
            "Remove-Item -Path $env:LOCALAPPDATA\\Microsoft\\Windows\\Explorer\\thumbcache_*.db -Force -ErrorAction SilentlyContinue; "
            "Start-Process explorer.exe"
        )
        self.run_task(run_powershell, command)

    def clear_store_cache(self):
        self.run_task(open_target, "wsreset")

    def clear_browser_caches(self):
        if not confirm("Caches dos navegadores", "Feche Chrome, Edge e Firefox antes. Deseja tentar limpar os caches?"):
            return
        self.run_task(clear_browser_cache_paths)

    def confirm_clear_extra_caches(self):
        if confirm("Limpar caches extras", "Limpar shader cache AMD/DirectX e crash dumps do usuario?"):
            self.run_task(clear_extra_caches)

    def open_wireless_display(self):
        command = "Start-Process explorer.exe 'ms-settings-connectabledevices:devicediscovery'"
        self.run_task(run_powershell, command)

    def reset_network(self):
        if confirm("Resetar rede", "Isso pode exigir reiniciar o PC depois. Deseja continuar?"):
            self.run_task(run_command, "netsh winsock reset & netsh int ip reset", True, 300)

    def confirm_restart_bluetooth(self):
        if confirm("Reset Bluetooth", "Reiniciar servicos Bluetooth? Seus dispositivos podem desconectar e reconectar."):
            self.run_task(restart_bluetooth_services)

    def confirm_restart_audio(self):
        if confirm("Reset audio", "Reiniciar servicos de audio do Windows? O som pode cortar por alguns segundos."):
            self.run_task(restart_audio_services)

    def sfc_scan(self):
        self.run_task(run_command, ["sfc", "/scannow"], False, 7200)

    def dism_restore(self):
        self.run_task(run_command, ["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"], False, 7200)

    def check_disk(self):
        self.run_task(run_command, ["chkdsk", "C:"], False, 3600)

    def create_restore_point(self):
        command = (
            "Checkpoint-Computer -Description 'Tweaks Restore Point' "
            "-RestorePointType 'MODIFY_SETTINGS'"
        )
        self.run_task(run_powershell, command)

    def recent_critical_events(self):
        command = (
            "Get-WinEvent -FilterHashtable @{LogName='System'; Level=1,2; StartTime=(Get-Date).AddDays(-7)} "
            "-MaxEvents 30 | Select-Object TimeCreated,ProviderName,Id,LevelDisplayName,Message | "
            "Format-List"
        )
        return run_powershell(command, timeout=120)

    def disable_hibernation(self):
        if confirm("Desativar hibernacao", "Desativar hibernacao libera espaco, mas remove inicializacao rapida. Continuar?"):
            self.run_task(run_command, ["powercfg", "-h", "off"], False, 120)

    def pc_info(self):
        info = []
        info.append(f"Computador: {socket.gethostname()}")
        info.append(f"Usuario: {os.getlogin()}")
        info.append(f"Windows: {platform.platform()}")
        info.append(run_powershell("Get-CimInstance Win32_Processor | Select-Object Name | Format-List"))
        info.append(run_powershell("Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory | Format-List"))
        info.append(run_command(["ipconfig"]))
        self.append_log("Informacoes do PC", "\n".join(info))

    def gpu_status(self):
        command = (
            "Get-CimInstance Win32_VideoController | "
            "Select-Object Name,AdapterCompatibility,DriverVersion,DriverDate,AdapterRAM | Format-List"
        )
        self.run_task(run_powershell, command)

    def open_backup_folder(self):
        try:
            backup_dir = ensure_backup_dir()
        except Exception as exc:
            self.append_log("Abrir pasta de backups", f"Erro: {exc}")
            return
        self.run_task(open_target, str(backup_dir))

    def show_backup_folder(self):
        self.append_log("Pasta de backup atual", str(get_backup_dir()))

    def choose_backup_folder(self):
        selected = filedialog.askdirectory(
            title="Escolha a pasta para backups",
            initialdir=str(get_backup_dir() if get_backup_dir().exists() else DESKTOP),
        )
        if not selected:
            return
        set_backup_dir(selected)
        self.append_log("Pasta de backup alterada", f"Nova pasta:\n{get_backup_dir()}")

    def reset_backup_folder(self):
        set_backup_dir(DEFAULT_BACKUP_DIR)
        self.append_log("Pasta de backup alterada", f"Padrao restaurado:\n{get_backup_dir()}")

    def list_installed_drivers(self):
        backup_dir = ensure_backup_dir()
        output = backup_dir / f"drivers-instalados-{timestamp()}.txt"
        command = (
            f"New-Item -ItemType Directory -Force -Path '{backup_dir}' | Out-Null; "
            "Get-CimInstance Win32_PnPSignedDriver | "
            "Select-Object DeviceName,Manufacturer,DriverVersion,DriverDate,InfName | "
            "Sort-Object DeviceName | Format-Table -AutoSize | Out-String | "
            f"Set-Content -Path '{output}' -Encoding UTF8; "
            f"Write-Output 'Arquivo criado: {output}'"
        )
        self.run_task(run_powershell, command)

    def list_running_services(self):
        command = (
            "Get-Service | Where-Object Status -eq 'Running' | "
            "Select-Object Name,DisplayName,Status | Sort-Object DisplayName | Format-Table -AutoSize"
        )
        self.run_task(run_powershell, command)

    def confirm_post_format_bundle(self):
        if confirm("Pacote pos-formatacao", f"Criar pacote de backups e checklist em {get_backup_dir()}?"):
            self.run_task(backup_post_format_bundle)

    def confirm_backup_minecraft(self):
        if confirm("Backup Minecraft", f"Criar backup em {get_backup_dir()}?"):
            self.run_task(backup_minecraft)

    def confirm_minecraft_clean_logs(self):
        if confirm("Limpar Minecraft", "Limpar logs, crash-reports, cache e .mixin.out da .minecraft?"):
            self.run_task(minecraft_clean_logs_and_cache)

    def restore_minecraft_backup(self):
        backup_dir = get_backup_dir()
        file_path = filedialog.askopenfilename(
            title="Escolha um backup .zip do Minecraft",
            initialdir=str(backup_dir if backup_dir.exists() else DESKTOP),
            filetypes=[("Arquivos ZIP", "*.zip"), ("Todos os arquivos", "*.*")],
        )
        if not file_path:
            return
        if not confirm("Restaurar backup", "Isso vai extrair arquivos por cima da sua .minecraft atual. Continuar?"):
            return

        def restore():
            if not MINECRAFT_DIR.exists():
                MINECRAFT_DIR.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(file_path, "r") as archive:
                archive.extractall(MINECRAFT_DIR)
            return f"Backup restaurado em:\n{MINECRAFT_DIR}\nOrigem:\n{file_path}"

        self.run_task(restore)

    def open_essential_downloads(self):
        essentials = [
            "AMD RX 580 drivers oficiais",
            "AMD RX580 primeiro estavel - 23.11.1 Polaris/Vega",
            "AMD RX580 estavel para Forza6 - 23.10.01.14",
            "AMD 23.10.01.14 notas oficiais",
            "Display Driver Uninstaller (DDU)",
            "Temurin Java 8",
            "Temurin Java 17",
            "Temurin Java 21",
            "Git for Windows",
            "Visual Studio Code",
            "7-Zip",
            "Prism Launcher",
            "Forge",
            "NeoForge",
            "Fabric",
        ]
        for name in essentials:
            webbrowser.open(DOWNLOAD_LINKS[name])
        self.append_log("Downloads essenciais", "Links essenciais abertos no navegador.")

    def preset_quick_maintenance(self):
        if not confirm("Manutencao rapida", "Executar limpeza rapida, cache extra e flush DNS?"):
            return

        def task():
            return "\n\n".join([
                "=== Limpeza rapida ===",
                quick_temp_prefetch_cleanup(),
                "=== Caches extras ===",
                clear_extra_caches(),
                "=== DNS ===",
                run_command(["ipconfig", "/flushdns"]),
            ])

        self.run_task(task)

    def preset_before_gaming(self):
        if not confirm("Antes de jogar", "Ativar alto desempenho, limpar temporarios/shader cache e flush DNS?"):
            return

        def task():
            return "\n\n".join([
                "=== Plano alto desempenho ===",
                run_command(
                    "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61 >nul 2>&1 & "
                    "powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61",
                    True,
                    120,
                ),
                "=== Limpeza rapida ===",
                quick_temp_prefetch_cleanup(),
                "=== Shader/cache ===",
                clear_extra_caches(),
                "=== DNS ===",
                run_command(["ipconfig", "/flushdns"]),
            ])

        self.run_task(task)

    def preset_after_gaming(self):
        if not confirm("Depois de jogar", "Voltar plano equilibrado e limpar temporarios?"):
            return

        def task():
            return "\n\n".join([
                "=== Plano equilibrado ===",
                run_command(["powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"], False, 120),
                "=== Limpeza rapida ===",
                quick_temp_prefetch_cleanup(),
            ])

        self.run_task(task)

    def preset_forza6(self):
        for name in [
            "AMD RX580 estavel para Forza6 - 23.10.01.14",
            "Display Driver Uninstaller (DDU)",
        ]:
            webbrowser.open(DOWNLOAD_LINKS[name])
        self.run_task(open_target, "ms-settings:display")

    def preset_minecraft_modding(self):
        if not confirm("Minecraft modding", "Backup mods/configs, listar mods, abrir .minecraft e ver Java?"):
            return

        def task():
            try:
                os.startfile(str(MINECRAFT_DIR))
            except Exception:
                pass
            return "\n\n".join([
                "=== Backup mods/configs ===",
                backup_minecraft_modding_only(),
                "=== Lista de mods ===",
                list_minecraft_mods(),
                "=== Java ===",
                java_versions_report(),
            ])

        self.run_task(task)

    def list_installed_programs(self):
        desktop = Path.home() / "Desktop" / "programas_instalados.txt"
        command = (
            "$apps = Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*,"
            "HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*,"
            "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* "
            "-ErrorAction SilentlyContinue | Where-Object DisplayName | "
            "Select-Object DisplayName,DisplayVersion,Publisher,InstallDate | Sort-Object DisplayName; "
            f"$apps | Format-Table -AutoSize | Out-String | Set-Content -Path '{desktop}' -Encoding UTF8; "
            f"Write-Output 'Arquivo criado: {desktop}'"
        )
        self.run_task(run_powershell, command)

    def list_heavy_processes(self):
        command = (
            "Get-Process | Sort-Object WS -Descending | "
            "Select-Object -First 20 ProcessName,Id,CPU,@{Name='RAM_MB';Expression={[math]::Round($_.WS/1MB,1)}} | "
            "Format-Table -AutoSize"
        )
        self.run_task(run_powershell, command)

    def restart_explorer(self):
        command = (
            "taskkill /f /im StartMenuExperienceHost.exe >nul 2>&1 & "
            "taskkill /f /im ShellExperienceHost.exe >nul 2>&1 & "
            "taskkill /f /im explorer.exe >nul 2>&1 & "
            "timeout /t 2 /nobreak >nul & "
            "start explorer.exe"
        )
        self.run_task(run_command, command, True, 120)

    def high_performance_plan(self):
        command = (
            "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61 >nul 2>&1 & "
            "powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61"
        )
        self.run_task(run_command, command, True, 120)

    def balanced_plan(self):
        self.run_task(run_command, ["powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"], False, 120)


if __name__ == "__main__":
    if not is_admin():
        relaunch_as_admin()
        sys.exit()

    app = TweaksApp()
    app.mainloop()
