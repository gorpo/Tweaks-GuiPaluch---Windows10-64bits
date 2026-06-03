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
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk


APP_TITLE = "Tweaks GuiPaluch"
BG = "#0f172a"
PANEL = "#111827"
PANEL_2 = "#1f2937"
TEXT = "#e5e7eb"
MUTED = "#9ca3af"
ACCENT = "#38bdf8"
BUTTON = "#243244"
BUTTON_ACTIVE = "#334155"
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


def confirm(title, text):
    return messagebox.askyesno(title, text)


class TweaksApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1100x760")
        self.minsize(760, 560)
        self.configure(bg=BG)
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
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.option_add("*Font", ("Segoe UI", 10))
        self.style.configure(".", background=BG, foreground=TEXT, fieldbackground=PANEL)
        self.style.configure("TFrame", background=BG)
        self.style.configure("Panel.TFrame", background=PANEL)
        self.style.configure("TLabel", background=BG, foreground=TEXT)
        self.style.configure("Muted.TLabel", background=BG, foreground=MUTED)
        self.style.configure("Title.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 22, "bold"))
        self.style.configure("Section.TLabel", background=PANEL, foreground=ACCENT, font=("Segoe UI", 12, "bold"))
        self.style.configure(
            "TButton",
            background=BUTTON,
            foreground=TEXT,
            bordercolor="#334155",
            lightcolor=BUTTON,
            darkcolor=BUTTON,
            focusthickness=1,
            focuscolor=ACCENT,
            padding=(12, 9),
        )
        self.style.map(
            "TButton",
            background=[("active", BUTTON_ACTIVE), ("pressed", "#0ea5e9")],
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
            background=[("selected", "#0ea5e9"), ("active", "#334155")],
            foreground=[("selected", "#ffffff"), ("active", "#ffffff")],
        )
        self.style.configure("Vertical.TScrollbar", background=PANEL_2, troughcolor=BG, arrowcolor=TEXT)

    def _build_ui(self):
        header = ttk.Frame(self, padding=(18, 16, 18, 8))
        header.pack(fill="x")

        title = ttk.Label(header, text=APP_TITLE, style="Title.TLabel")
        title.pack(side="left")

        admin_text = "Rodando como administrador" if is_admin() else "Sem administrador"
        admin = ttk.Label(header, text=admin_text, style="Muted.TLabel")
        admin.pack(side="right")

        main = ttk.Frame(self, padding=(18, 8, 18, 8))
        main.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill="both", expand=True)

        self.log = scrolledtext.ScrolledText(
            main,
            wrap="word",
            height=10,
            font=("Consolas", 10),
            bg="#020617",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            borderwidth=0,
        )
        self.log.pack(fill="both", expand=False, pady=(12, 0))
        self.log.insert("end", "Logs aparecerao aqui.\n")

        status = ttk.Label(self, textvariable=self.status_var, padding=(18, 7), style="Muted.TLabel")
        status.pack(fill="x")

        self._add_sections()

    def _add_sections(self):
        cleanup = self._tab("Limpeza")
        self._section(cleanup, "Arquivos temporarios e caches", [
            ("Limpeza rapida: Temp + %TEMP% + Prefetch", lambda: self.run_task(quick_temp_prefetch_cleanup)),
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
            ("Resetar rede", self.reset_network),
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

        repair = self._tab("Reparo")
        self._section(repair, "Windows e disco", [
            ("Verificar arquivos do Windows (SFC)", self.sfc_scan),
            ("Reparar imagem do Windows (DISM)", self.dism_restore),
            ("Verificar disco", self.check_disk),
            ("Otimizar unidades", lambda: self.run_task(open_target, "dfrgui")),
        ])

        system = self._tab("Sistema")
        self._section(system, "Ferramentas do sistema", [
            ("Abrir Gerenciador de Tarefas", lambda: self.run_task(open_target, "taskmgr")),
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
            ("Criar backup Minecraft agora", self.confirm_backup_minecraft),
            ("Abrir downloads essenciais", self.open_essential_downloads),
            ("Criar ponto de restauracao", self.create_restore_point),
            ("Plano Alto Desempenho", self.high_performance_plan),
            ("Abrir apps de inicializacao", lambda: self.run_task(open_target, "ms-settings:startupapps")),
            ("Abrir privacidade", lambda: self.run_task(open_target, "ms-settings:privacy")),
            ("Abrir programas instalados", lambda: self.run_task(open_target, "ms-settings:appsfeatures")),
        ])

    def _tab(self, title):
        outer = ttk.Frame(self.notebook, padding=0, style="Panel.TFrame")
        self.notebook.add(outer, text=title)

        canvas = tk.Canvas(outer, highlightthickness=0, bg=PANEL)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas, padding=14, style="Panel.TFrame")
        window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def resize(event):
            canvas.itemconfigure(window_id, width=event.width)
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", resize)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return inner

    def _section(self, parent, title, buttons):
        label = ttk.Label(parent, text=title, style="Section.TLabel")
        label.pack(fill="x", pady=(6, 10))

        grid = ttk.Frame(parent, style="Panel.TFrame")
        grid.pack(fill="x")

        button_widgets = []
        for index, (text, command) in enumerate(buttons):
            button = ttk.Button(grid, text=text, command=command)
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
                button.grid(row=row, column=col, sticky="ew", padx=5, pady=5)

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

    def open_wireless_display(self):
        command = "Start-Process explorer.exe 'ms-settings-connectabledevices:devicediscovery'"
        self.run_task(run_powershell, command)

    def reset_network(self):
        if confirm("Resetar rede", "Isso pode exigir reiniciar o PC depois. Deseja continuar?"):
            self.run_task(run_command, "netsh winsock reset & netsh int ip reset", True, 300)

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

    def confirm_backup_minecraft(self):
        if confirm("Backup Minecraft", f"Criar backup em {get_backup_dir()}?"):
            self.run_task(backup_minecraft)

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
        self.run_task(run_command, "taskkill /f /im explorer.exe & start explorer.exe", True, 120)

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
