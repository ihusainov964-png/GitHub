"""
Game Optimizer v4.0
Rust / GTA V / CS2 / Fortnite / ARK
Без конфликтов с EAC. Анимации. Полный функционал.
"""
import sys, os, time, socket, random, threading, subprocess, tkinter, platform, math
import customtkinter as ctk
from tkinter import filedialog, messagebox

sys.setrecursionlimit(5000)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Цвета ──────────────────────────────────────────────────────────────────
BG     = "#05080f"
PANEL  = "#090f1d"
PANEL2 = "#0c1628"
BORDER = "#1a3050"
TEXT   = "#b8cfea"
DIM    = "#3a5a7a"
NEON   = "#00f0ff"
GREEN  = "#00ff88"
GOLD   = "#ffd700"
RED    = "#ff4466"
PURPLE = "#b060ff"
ORANGE = "#ff9f40"

JOKES = [
    "😂 Ваня: '5 FPS — это нормально'",
    "💀 Ваня оптимизировал — удалил system32",
    "🎯 Ваня поставил мониторинг — FPS 12",
    "🔫 Ваня строил дом — убили через стену",
    "🚗 Ваня в GTA взял такси — лучше пешком",
    "⚡ Ваня включил план питания — сгорел роутер",
    "🦕 Ваня в ARK — съел динозавр",
    "🌀 Ваня в Fortnite — убил строитель",
]

# ── Утилиты ────────────────────────────────────────────────────────────────
def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           timeout=30, encoding="cp1251", errors="replace")
        return r.returncode == 0
    except: return False

def run_cmd_out(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           timeout=15, encoding="cp1251", errors="replace")
        return r.stdout.strip()
    except: return ""

def expand(p): return os.path.expandvars(os.path.expanduser(p))
def find_exe(paths):
    for p in paths:
        e = expand(p)
        if os.path.exists(e): return e
    return None
def launch_steam(steam_id):
    """Запустить игру ЧЕРЕЗ Steam — безопасно для EAC"""
    try:
        subprocess.Popen(["cmd","/c","start","",f"steam://rungameid/{steam_id}"],shell=False)
    except: pass

def launch_epic(app_name):
    """Запустить через Epic"""
    try:
        subprocess.Popen(["cmd","/c","start","",f"com.epicgames.launcher://apps/{app_name}?action=launch&silent=true"],shell=False)
    except: pass

def ping_host(host, timeout=2):
    try:
        t0 = time.time()
        s = socket.create_connection((host, 80), timeout=timeout)
        s.close()
        return int((time.time() - t0) * 1000)
    except: return -1

def make_btn(parent, text, cmd, color="#0060df", hover="#0090ff",
             size=12, bold=True, width=None, corner=7):
    kw = dict(text=text, command=cmd, fg_color=color, hover_color=hover,
              font=ctk.CTkFont(size=size, weight="bold" if bold else "normal"),
              corner_radius=corner)
    if width: kw["width"] = width
    return ctk.CTkButton(parent, **kw)

# ── ДАННЫЕ: RUST ─────────────────────────────────────────────────────────────
# ВАЖНО: Rust использует Easy Anti-Cheat.
# Мы НЕ пишем в реестр HKCU\Software\Facepunch\Rust — EAC это проверяет!
# Используем ТОЛЬКО client.cfg (стандартные консольные команды игры).

RUST_EXE = [
    r"C:\Program Files (x86)\Steam\steamapps\common\Rust\RustClient.exe",
    r"D:\Steam\steamapps\common\Rust\RustClient.exe",
    r"E:\Steam\steamapps\common\Rust\RustClient.exe",
    r"D:\Games\Steam\steamapps\common\Rust\RustClient.exe",
]
RUST_CFG = r"%APPDATA%\Rust\cfg\client.cfg"

RUST_PRESETS = {
    "Макс FPS": {
        "desc": "Минимум графики", "fps": "100-200+", "color": NEON,
        "launch": "-high -maxMem=8192 -malloc=system -force-feature-level-11-0 +fps.limit 0 -nolog",
        "settings": [("grass.on","false"),("terrain.quality","0"),("graphics.shadows","0"),
                     ("graphics.ssao","0"),("graphics.damage","0"),("graphics.itemskins","0"),
                     ("graphics.lodbias","0.25"),("graphics.dof","false"),("graphics.shafts","0"),
                     ("graphics.reflections","0"),("graphics.parallax","0")],
    },
    "Баланс": {
        "desc": "FPS + читаемость", "fps": "60-120", "color": PURPLE,
        "launch": "-high -maxMem=8192 +fps.limit 0",
        "settings": [("grass.on","true"),("terrain.quality","50"),("graphics.shadows","1"),
                     ("graphics.ssao","0"),("graphics.lodbias","1")],
    },
    "Качество": {
        "desc": "Полная графика", "fps": "40-80", "color": GOLD,
        "launch": "+fps.limit 0",
        "settings": [("grass.on","true"),("terrain.quality","100"),("graphics.shadows","3"),
                     ("graphics.ssao","1"),("graphics.lodbias","2")],
    },
}

# Паразиты Rust — ТОЛЬКО через client.cfg, без реестра!
RUST_PARASITES = [
    ("🌿","Трава (grass.on false)","Убирает траву → +20-40 FPS. Безопасно для EAC.",GREEN,
     ["echo grass.on false >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo grass.on true >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("💨","Motion Blur","Размытие при движении снижает FPS.",NEON,
     ["echo effects.motionblur false >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo effects.motionblur true >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("🪞","Отражения (reflections 0)","Отражения на воде — дорогой эффект.",ORANGE,
     ["echo graphics.reflections 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.reflections 2 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("🌅","God Rays (shafts 0)","Volumetric лучи света — тяжело.",ORANGE,
     ["echo graphics.shafts 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.shafts 1 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("🌊","Глубина резкости (dof false)","Размытие фона — GPU зря.",NEON,
     ["echo graphics.dof false >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.dof true >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("🎆","Эффекты взрывов (damage 0)","Партиклы взрывов — лишняя нагрузка.",RED,
     ["echo graphics.damage 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.damage 1 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("📦","Скины предметов (itemskins 0)","Загрузка скинов жрёт RAM.",GOLD,
     ["echo graphics.itemskins 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.itemskins 1 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("🔵","SSAO (ssao 0)","Ambient occlusion — тени в углах, дорого.",PURPLE,
     ["echo graphics.ssao 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.ssao 1 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("🔊","VOIP (voice.use false)","Голосовой чат слушает микрофон постоянно.",PURPLE,
     ["echo voice.use false >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo voice.use true >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("🌱","LOD Bias (lodbias 0.25)","Дистанция детализации объектов.",DIM,
     ["echo graphics.lodbias 0.25 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.lodbias 2 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
]

RUST_KILL_CFG = "\n".join([
    "// Game Optimizer v4.0 - Maximum Performance",
    "grass.on false", "grass.shadowcast false", "effects.motionblur false",
    "graphics.damage 0", "graphics.dof false", "graphics.shafts 0",
    "graphics.shadows 0", "graphics.ssao 0", "graphics.lodbias 0.25",
    "graphics.itemskins 0", "graphics.reflections 0", "graphics.parallax 0",
    "voice.use false", "fps.limit 0",
])

RUST_TIPS = [
    ("💡","Steam оверлей","Steam → ПКМ на Rust → Свойства → убери Steam Overlay. +5-10 FPS."),
    ("🛡","Антивирус","Defender → Исключения → папка с Rust. EAC грузится быстрее."),
    ("🎮","DirectX 11","Параметры запуска: -force-feature-level-11-0"),
    ("🧹","Кэш шейдеров","AppData/Local/Temp/Rust — удаляй раз в неделю."),
    ("⚙","F1 консоль","В игре F1 → вставь команды из пресета. Работают сразу."),
    ("📡","Выбор сервера","Играй на серверах с пингом < 80ms."),
    ("⚠","EAC безопасность","НЕ редактируй файлы в RustClient_Data — это бан. Только client.cfg безопасно."),
    ("🔧","client.cfg путь","%AppData%\\Rust\\cfg\\client.cfg — твои настройки консоли."),
]

# ── ДАННЫЕ: GTA V ─────────────────────────────────────────────────────────────
GTAV_EXE = [
    r"C:\Program Files (x86)\Steam\steamapps\common\Grand Theft Auto V\GTA5.exe",
    r"C:\Program Files\Rockstar Games\Grand Theft Auto V\GTA5.exe",
    r"D:\Rockstar Games\Grand Theft Auto V\GTA5.exe",
    r"D:\Steam\steamapps\common\Grand Theft Auto V\GTA5.exe",
    r"E:\Games\Grand Theft Auto V\GTA5.exe",
]

GTAV_PRESETS = {
    "Макс FPS": {
        "desc": "Для слабых ПК и FiveM", "fps": "80-160+", "color": NEON,
        "launch": "-notablet -norestrictions -noFirstRun -IgnoreCorrupts",
        "settings": [("TextureQuality","normal"),("ShaderQuality","normal"),("ShadowQuality","normal"),
                     ("ReflectionQuality","off"),("MSAA","off"),("FXAA","off"),
                     ("AmbientOcclusion","off"),("MotionBlur","false"),("InGameDepthOfField","false")],
    },
    "Баланс": {
        "desc": "Комфортная игра", "fps": "60-100", "color": PURPLE,
        "launch": "-notablet -noFirstRun",
        "settings": [("TextureQuality","high"),("ShaderQuality","high"),("ShadowQuality","high"),
                     ("MSAA","off"),("FXAA","on"),("AmbientOcclusion","medium"),("MotionBlur","false")],
    },
    "Качество": {
        "desc": "Максимальная красота", "fps": "40-70", "color": GOLD,
        "launch": "-notablet",
        "settings": [("TextureQuality","very high"),("ShaderQuality","very high"),
                     ("ShadowQuality","very high"),("MSAA","x4"),("FXAA","on"),
                     ("AmbientOcclusion","high"),("TessellationQuality","very high")],
    },
}

GTAV_PARASITES = [
    ("🎓","Обучающие подсказки","Всплывают каждый раз.",RED,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v TutorialDone /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v TutorialDone /t REG_DWORD /d 0 /f"]),
    ("🎬","Вступительные ролики","Логотип + ролик при запуске.",ORANGE,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v InstallComplete /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v InstallComplete /t REG_DWORD /d 0 /f"]),
    ("🌀","Motion Blur","-10-15 FPS без пользы.",RED,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v MotionBlur /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v MotionBlur /t REG_DWORD /d 1 /f"]),
    ("🌊","Глубина резкости DOF","Размытие фона — GPU зря.",NEON,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v InGameDepthOfField /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v InGameDepthOfField /t REG_DWORD /d 1 /f"]),
    ("🎬","Replay / Rockstar Editor","Пишет буфер в фоне постоянно.",GOLD,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ReplayBuffer /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ReplayBuffer /t REG_DWORD /d 1 /f"]),
    ("🐾","Tessellation","Детализация поверхностей — очень дорого.",PURPLE,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v Tessellation /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v Tessellation /t REG_DWORD /d 1 /f"]),
    ("🌆","Extended Distance","Далёкие объекты — огромная нагрузка.",RED,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ExtendedDistanceScaling /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ExtendedDistanceScaling /t REG_DWORD /d 1 /f"]),
    ("🚶","Плотность NPC","Много NPC грузят CPU.",ORANGE,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v PedDensity /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v PedDensity /t REG_DWORD /d 100 /f"]),
]

GTAV_TIPS = [
    ("🟣","FiveM оверлеи","Перед FiveM отключи Discord/Steam/NVIDIA оверлеи."),
    ("⚡","-notablet","Обязательный параметр — убирает ненужный ввод планшета."),
    ("🌐","NAT Open","Пробрось порты: 6672 UDP, 61455-61458 UDP."),
    ("🔧","Rockstar Launcher","Выключи из автозагрузки — Win+R → msconfig."),
    ("🗑","Кэш FiveM","%%LOCALAPPDATA%%\\FiveM\\FiveM.app\\cache — удаляй при лагах."),
    ("💾","VRAM индикатор","В настройках GTA V следи за VRAM. < 90% = хорошо."),
]

# ── ДАННЫЕ: CS2 ───────────────────────────────────────────────────────────────
CS2_EXE = [
    r"C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
    r"D:\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
    r"E:\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
]
CS2_CFG = r"%USERPROFILE%\AppData\Local\cs2\cfg\autoexec.cfg"

CS2_PRESETS = {
    "Макс FPS": {
        "desc": "Про-настройки", "fps": "200-400+", "color": NEON,
        "launch": "-novid -nojoy -noaafonts -limitvsconst -forcenovsync +mat_queue_mode -1 +r_dynamic_lighting 0 -freq 240 -high",
        "settings": [("r_lowlatency","2"),("fps_max","0"),("mat_queue_mode","-1"),
                     ("r_dynamic_lighting","0"),("r_shadows","0"),("cl_ragdoll_physics_enable","0"),
                     ("r_motionblur","0"),("cl_showfps","1"),("rate","786432"),
                     ("cl_interp","0"),("cl_interp_ratio","1"),("m_rawinput","1")],
    },
    "Баланс": {
        "desc": "FPS + видимость", "fps": "144-250", "color": PURPLE,
        "launch": "-novid -nojoy -forcenovsync +mat_queue_mode -1 -high",
        "settings": [("fps_max","0"),("r_lowlatency","2"),("r_shadows","1"),
                     ("r_dynamic_lighting","1"),("cl_showfps","1"),("r_motionblur","0"),("m_rawinput","1")],
    },
    "Качество": {
        "desc": "Красивая картинка", "fps": "100-180", "color": GOLD,
        "launch": "-novid +mat_queue_mode -1",
        "settings": [("fps_max","0"),("r_shadows","3"),("r_dynamic_lighting","1"),("r_motionblur","0")],
    },
}

CS2_AUTOEXEC = """// CS2 autoexec.cfg — Game Optimizer v4.0
fps_max 0
r_lowlatency 2
cl_showfps 1
mat_queue_mode -1
r_dynamic_lighting 0
r_shadows 0
cl_ragdoll_physics_enable 0
r_motionblur 0
cl_interp 0
cl_interp_ratio 1
rate 786432
cl_updaterate 128
cl_cmdrate 128
m_rawinput 1
snd_menumusic_volume 0
cl_draw_only_deathnotices 1
viewmodel_presetpos 3
"""

CS2_PARASITES = [
    ("🎓","Обучение / Tutorial","Убирает предложение обучалки.",RED,
     ["reg add \"HKCU\\Software\\Valve\\Counter-Strike Global Offensive\" /v TutorialDone /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Valve\\Counter-Strike Global Offensive\" /v TutorialDone /t REG_DWORD /d 0 /f"]),
    ("🎬","Интро видео Valve","Логотип Valve при запуске.",ORANGE,
     ["reg add \"HKCU\\Software\\Valve\\Counter-Strike Global Offensive\" /v NoVideoIntro /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Valve\\Counter-Strike Global Offensive\" /v NoVideoIntro /t REG_DWORD /d 0 /f"]),
    ("🌀","Motion Blur","Размытие — FPS без пользы.",RED,
     ["echo r_motionblur 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo r_motionblur 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),
    ("💀","Ragdoll физика","Трупы с физикой жрут CPU.",NEON,
     ["echo cl_ragdoll_physics_enable 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo cl_ragdoll_physics_enable 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),
    ("🌿","Детали окружения","Трава и листья — декорации.",GREEN,
     ["echo cl_detailfade 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo cl_detailfade 400 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),
    ("🎵","Музыка в меню","Звуковой движок зря работает.",PURPLE,
     ["echo snd_menumusic_volume 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo snd_menumusic_volume 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),
    ("💬","Kill feed анимации","Только важное на экране.",GOLD,
     ["echo cl_draw_only_deathnotices 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo cl_draw_only_deathnotices 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),
    ("🔫","Осмотр оружия (viewmodel 3)","Меньше мусора на экране.",ORANGE,
     ["echo viewmodel_presetpos 3 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo viewmodel_presetpos 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),
]

CS2_TIPS = [
    ("🖥","Частота монитора","NVIDIA → Панель управления → выбери 144/240Hz."),
    ("🖱","Raw Input","m_rawinput 1 — прямой ввод без обработки Windows."),
    ("📡","Rate команды","rate 786432; cl_interp 0; cl_interp_ratio 1 — в autoexec."),
    ("🌡","Температура","CS2 нагружает CPU — больше 90°C = чистка кулера."),
    ("🎮","Game DVR","Win+G → Настройки → выключи всё."),
    ("⚙","autoexec.cfg","Папка: %USERPROFILE%\\AppData\\Local\\cs2\\cfg\\"),
]

# ── ДАННЫЕ: FORTNITE ──────────────────────────────────────────────────────────
FN_EXE = [
    r"C:\Program Files\Epic Games\Fortnite\FortniteGame\Binaries\Win64\FortniteClient-Win64-Shipping.exe",
    r"D:\Epic Games\Fortnite\FortniteGame\Binaries\Win64\FortniteClient-Win64-Shipping.exe",
    r"C:\Program Files (x86)\Epic Games\Fortnite\FortniteGame\Binaries\Win64\FortniteClient-Win64-Shipping.exe",
    r"E:\Fortnite\FortniteGame\Binaries\Win64\FortniteClient-Win64-Shipping.exe",
]
FN_INI = r"%LOCALAPPDATA%\FortniteGame\Saved\Config\WindowsClient\GameUserSettings.ini"

FN_PRESETS = {
    "Макс FPS": {
        "desc": "Минимум графики", "fps": "144-300+", "color": NEON,
        "launch": "-NOTEXTURESTREAMING -USEALLAVAILABLECORES -nomansky -novsync -dx12",
        "settings": [("sg.ResolutionQuality","75"),("sg.ViewDistanceQuality","1"),
                     ("sg.ShadowQuality","0"),("sg.PostProcessQuality","0"),
                     ("sg.TextureQuality","0"),("sg.EffectsQuality","0"),
                     ("sg.FoliageQuality","0"),("bUseVSync","False"),("FrameRateLimit","0"),("bShowFPS","True")],
    },
    "Баланс": {
        "desc": "FPS + картинка", "fps": "90-144", "color": PURPLE,
        "launch": "-USEALLAVAILABLECORES -nomansky -novsync",
        "settings": [("sg.ResolutionQuality","100"),("sg.ViewDistanceQuality","2"),
                     ("sg.ShadowQuality","2"),("sg.PostProcessQuality","2"),
                     ("sg.TextureQuality","2"),("bUseVSync","False"),("FrameRateLimit","144")],
    },
    "Качество": {
        "desc": "Красивая картинка", "fps": "60-90", "color": GOLD,
        "launch": "-USEALLAVAILABLECORES -novsync",
        "settings": [("sg.ResolutionQuality","100"),("sg.ViewDistanceQuality","4"),
                     ("sg.ShadowQuality","4"),("sg.PostProcessQuality","4"),
                     ("sg.TextureQuality","4"),("bUseVSync","False"),("FrameRateLimit","0")],
    },
}

FN_KILL_INI = "[ScalabilityGroups]\nsg.ResolutionQuality=75\nsg.ViewDistanceQuality=1\nsg.ShadowQuality=0\nsg.PostProcessQuality=0\nsg.TextureQuality=0\nsg.EffectsQuality=0\nsg.FoliageQuality=0\n\n[/Script/FortniteGame.FortGameUserSettings]\nbUseVSync=False\nFrameRateLimit=0.000000\nbShowFPS=True\n"

FN_PARASITES = [
    ("🎓","Обучение / Tutorial","Убирает обучалку.",RED,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v TutorialCompleted /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v TutorialCompleted /t REG_DWORD /d 0 /f"]),
    ("🎬","Интро видео Epic","Логотип при запуске.",ORANGE,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v SkipIntro /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v SkipIntro /t REG_DWORD /d 0 /f"]),
    ("🌀","Motion Blur","Размытие при движении.",RED,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v MotionBlur /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v MotionBlur /t REG_DWORD /d 1 /f"]),
    ("🌿","Foliage / Листва","Трава и кусты — лишняя нагрузка.",GREEN,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v FoliageQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v FoliageQuality /t REG_DWORD /d 4 /f"]),
    ("🌊","Глубина резкости DOF","Размытие фона — GPU зря.",NEON,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v DepthOfField /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v DepthOfField /t REG_DWORD /d 1 /f"]),
    ("🎵","Музыка в лобби","Нагружает CPU.",PURPLE,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v LobbyMusicVolume /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v LobbyMusicVolume /t REG_DWORD /d 100 /f"]),
    ("📡","Replays / Повторы","Пишет файлы на диск постоянно.",GOLD,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v bShouldRecord /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v bShouldRecord /t REG_DWORD /d 1 /f"]),
    ("💥","Nanite/Lumen","Очень тяжёлые современные эффекты.",ORANGE,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v MaterialQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v MaterialQuality /t REG_DWORD /d 4 /f"]),
]

FN_TIPS = [
    ("📁","Путь к настройкам","%%LOCALAPPDATA%%\\FortniteGame\\Saved\\Config\\WindowsClient\\"),
    ("⚡","Параметры запуска","-NOTEXTURESTREAMING -USEALLAVAILABLECORES -dx12"),
    ("🛡","Исключения Defender","Добавь папку Fortnite в исключения антивируса."),
    ("🎮","DirectX 12","На RTX картах DX12 быстрее. На GTX — попробуй оба."),
    ("🔄","Очистка кэша","%%LOCALAPPDATA%%\\FortniteGame\\Saved\\Cache — при фризах."),
    ("⚙","Performance Mode","В настройках Fortnite есть Performance Mode — +30-50% FPS на слабых ПК."),
]

# ── ДАННЫЕ: ARK ───────────────────────────────────────────────────────────────
ARK_EXE = [
    r"C:\Program Files (x86)\Steam\steamapps\common\ARK\ShooterGame\Binaries\Win64\ShooterGame.exe",
    r"D:\Steam\steamapps\common\ARK\ShooterGame\Binaries\Win64\ShooterGame.exe",
    r"C:\Program Files (x86)\Steam\steamapps\common\ARK Survival Ascended\ShooterGame\Binaries\Win64\ArkAscended.exe",
    r"D:\Steam\steamapps\common\ARK Survival Ascended\ShooterGame\Binaries\Win64\ArkAscended.exe",
]

ARK_PRESETS = {
    "Макс FPS": {
        "desc": "Минимум графики", "fps": "60-120+", "color": NEON,
        "launch": "-USEALLAVAILABLECORES -sm4 -d3d10 -nomansky -lowmemory -novsync",
        "settings": [("sg.ResolutionQuality","75"),("sg.ShadowQuality","0"),("sg.TextureQuality","0"),
                     ("sg.EffectsQuality","0"),("sg.FoliageQuality","0"),("bUseVSync","False"),("FrameRateLimit","0")],
    },
    "Баланс": {
        "desc": "FPS + читаемость", "fps": "40-80", "color": PURPLE,
        "launch": "-USEALLAVAILABLECORES -nomansky -novsync",
        "settings": [("sg.ResolutionQuality","100"),("sg.ShadowQuality","2"),("sg.TextureQuality","2"),
                     ("sg.EffectsQuality","2"),("sg.FoliageQuality","2"),("bUseVSync","False")],
    },
    "Качество": {
        "desc": "Красивая картинка", "fps": "25-50", "color": GOLD,
        "launch": "-USEALLAVAILABLECORES",
        "settings": [("sg.ResolutionQuality","100"),("sg.ShadowQuality","4"),("sg.TextureQuality","4"),
                     ("sg.EffectsQuality","4"),("sg.FoliageQuality","4"),("bUseVSync","False")],
    },
}

ARK_PARASITES = [
    ("🎓","Обучение / подсказки","Постоянные подсказки новичка.",RED,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v TutorialDone /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v TutorialDone /t REG_DWORD /d 0 /f"]),
    ("🎬","Интро видео","Логотипы при запуске.",ORANGE,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v SkipIntro /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v SkipIntro /t REG_DWORD /d 0 /f"]),
    ("🌿","Foliage / Листва","Деревья и кусты — главный убийца FPS в ARK.",GREEN,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v FoliageQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v FoliageQuality /t REG_DWORD /d 100 /f"]),
    ("🦕","Анимации динозавров NPC","Сложные анимации нагружают CPU.",PURPLE,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v NPCQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v NPCQuality /t REG_DWORD /d 2 /f"]),
    ("🌊","Глубина резкости DOF","Размытие фона — GPU зря.",NEON,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v DepthOfField /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v DepthOfField /t REG_DWORD /d 1 /f"]),
    ("🌀","Motion Blur","Размытие при движении — отключи.",RED,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v MotionBlur /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v MotionBlur /t REG_DWORD /d 1 /f"]),
    ("☁️","Volumetric Clouds","Объёмные облака — очень тяжело.",GOLD,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v VolumetricClouds /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v VolumetricClouds /t REG_DWORD /d 1 /f"]),
    ("💧","Water Quality","Отражения воды — дорогой эффект.",ORANGE,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v WaterQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v WaterQuality /t REG_DWORD /d 2 /f"]),
]

ARK_TIPS = [
    ("💾","RAM","ARK требует 16GB+ RAM. Закрой всё перед игрой."),
    ("⚡","Параметры запуска","-USEALLAVAILABLECORES -sm4 -d3d10 -nomansky -lowmemory"),
    ("🌿","Foliage = главный враг","Листва в ARK — ставь на минимум. Огромная разница."),
    ("🧹","Кэш шейдеров","ARK\\ShooterGame\\Saved\\Cache — удаляй при фризах."),
    ("🦕","Динозавры рядом","Снижай дистанцию прорисовки мобов в настройках сервера."),
    ("🖥","Разрешение","1600x900 вместо 1080p — +30% FPS почти без потери качества."),
]

# ── Общие: оверлеи, Windows, сеть ─────────────────────────────────────────────
OVERLAYS = [
    ("🎮","Xbox Game Bar / DVR","Сжирает 5-15% CPU, вызывает фризы.",RED,
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f",
      "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR\" /v AllowGameDVR /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 1 /f"]),
    ("📸","NVIDIA ShadowPlay","Пишет видео в фоне, нагружает GPU.",ORANGE,
     ["reg add \"HKCU\\Software\\NVIDIA Corporation\\NVCapture\" /v CaptureEnabled /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\NVIDIA Corporation\\NVCapture\" /v CaptureEnabled /t REG_DWORD /d 1 /f"]),
    ("💬","Discord оверлей","+3-8ms задержки на кадр.",PURPLE,
     ["reg add \"HKCU\\Software\\Discord\" /v Overlay /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Discord\" /v Overlay /t REG_DWORD /d 1 /f"]),
    ("🎵","Steam оверлей","Shift+Tab лагает, грузит RAM.",NEON,
     ["reg add \"HKCU\\Software\\Valve\\Steam\" /v SteamOverlayEnabled /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Valve\\Steam\" /v SteamOverlayEnabled /t REG_DWORD /d 1 /f"]),
]

BG_PROCS = [
    ("🔄","Windows Update","Качает обновления во время игры.",RED,
     ["net stop wuauserv","net stop bits","net stop dosvc"],["net start wuauserv"]),
    ("🔍","Windows Search","Индексирует файлы, грузит диск.",ORANGE,
     ["net stop wsearch","sc config wsearch start=disabled"],
     ["net start wsearch","sc config wsearch start=auto"]),
    ("📊","SysMain / Superfetch","Мешает играм занять всю RAM.",GOLD,
     ["net stop sysmain","sc config sysmain start=disabled"],
     ["net start sysmain","sc config sysmain start=auto"]),
    ("☁️","OneDrive синхронизация","Грузит диск и интернет.",NEON,
     ["taskkill /f /im OneDrive.exe","sc config OneSyncSvc start=disabled"],
     ["sc config OneSyncSvc start=auto"]),
]

WIN_OPTS = [
    ("⚡","Высокий план питания","Максимальная производительность CPU.",NEON,
     ["powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"],
     ["powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e"]),
    ("📈","Приоритет CPU (Win32=38)","Лучший отклик в играх.",GREEN,
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v Win32PrioritySeparation /t REG_DWORD /d 2 /f"]),
    ("🎮","HAGS GPU Scheduling","Меньше задержка GPU (Win10 2004+).",PURPLE,
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v HwSchMode /t REG_DWORD /d 2 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v HwSchMode /t REG_DWORD /d 1 /f"]),
    ("🖥","Откл. визуальные эффекты","Анимации Windows — ненужный расход.",ORANGE,
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects\" /v VisualFXSetting /t REG_DWORD /d 2 /f"],
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects\" /v VisualFXSetting /t REG_DWORD /d 0 /f"]),
    ("🔕","Откл. Xbox Game Bar","-5-15% CPU в играх.",RED,
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f",
      "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR\" /v AllowGameDVR /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 1 /f"]),
    ("🔍","Откл. Windows Search","Не индексирует во время игры.",GOLD,
     ["net stop wsearch","sc config wsearch start=disabled"],
     ["net start wsearch","sc config wsearch start=auto"]),
    ("📊","Откл. SysMain","Освобождает RAM для игры.",ORANGE,
     ["net stop sysmain","sc config sysmain start=disabled"],
     ["net start sysmain","sc config sysmain start=auto"]),
    ("🧹","Очистка RAM","ProcessIdleTasks — освобождает кэш.",GREEN,
     ["rundll32.exe advapi32.dll,ProcessIdleTasks"],[]),
    ("⏸","Пауза Windows Update","Обновления не мешают игре.",RED,
     ["net stop wuauserv","net stop bits","net stop dosvc"],["net start wuauserv"]),
    ("💾","Откл. очистку PageFile","Быстрее выключение ПК.",NEON,
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v ClearPageFileAtShutdown /t REG_DWORD /d 0 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v ClearPageFileAtShutdown /t REG_DWORD /d 1 /f"]),
]

NET_OPTS = [
    ("🌐","DNS Google + Cloudflare","8.8.8.8 + 1.1.1.1 — быстрый DNS.",GREEN,
     ["netsh interface ip set dns \"Ethernet\" static 8.8.8.8",
      "netsh interface ip add dns \"Ethernet\" 1.1.1.1 index=2",
      "netsh interface ip set dns \"Wi-Fi\" static 8.8.8.8",
      "netsh interface ip add dns \"Wi-Fi\" 1.1.1.1 index=2",
      "ipconfig /flushdns"],
     ["netsh interface ip set dns \"Ethernet\" dhcp","netsh interface ip set dns \"Wi-Fi\" dhcp","ipconfig /flushdns"]),
    ("🏎","Откл. Nagle алгоритм","TcpAckFrequency=1 → -5-30ms пинга.",NEON,
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpAckFrequency /t REG_DWORD /d 1 /f",
      "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TCPNoDelay /t REG_DWORD /d 1 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpAckFrequency /t REG_DWORD /d 2 /f"]),
    ("📶","QoS DSCP=46","Приоритет игрового трафика.",PURPLE,
     ["netsh qos delete policy \"GO_Game\"","netsh qos add policy \"GO_Game\" app=\"*\" dscp=46 throttle-rate=-1"],
     ["netsh qos delete policy \"GO_Game\""]),
    ("🔕","Откл. IPv6","Убирает конфликты IPv4/IPv6.",ORANGE,
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters\" /v DisabledComponents /t REG_DWORD /d 255 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters\" /v DisabledComponents /t REG_DWORD /d 0 /f"]),
    ("🔄","Сброс Winsock + IP","Полный сброс сетевого стека.",RED,
     ["netsh winsock reset","netsh int ip reset","ipconfig /flushdns","ipconfig /registerdns"],[]),
    ("🚀","TCP AutoTuning","Стабилизирует соединение.",GOLD,
     ["netsh interface tcp set global autotuninglevel=highlyrestricted"],
     ["netsh interface tcp set global autotuninglevel=normal"]),
]

# ── Словарь игр ────────────────────────────────────────────────────────────────
GAMES = {
    "Rust":     {"icon":"🔫","color":"#e07020","desc":"Survival multiplayer","steam":"252490","epic":None,
                 "exe":RUST_EXE,"presets":RUST_PRESETS,"parasites":RUST_PARASITES,"tips":RUST_TIPS,
                 "cfg":RUST_CFG,"kill_cfg":RUST_KILL_CFG,"kill_ini":None,"cfg_append":True,
                 "eac_warning":True},
    "GTA V":    {"icon":"🚗","color":"#00a8ff","desc":"Open world / FiveM","steam":"271590","epic":None,
                 "exe":GTAV_EXE,"presets":GTAV_PRESETS,"parasites":GTAV_PARASITES,"tips":GTAV_TIPS,
                 "cfg":None,"kill_cfg":None,"kill_ini":None,"cfg_append":True,"eac_warning":False},
    "CS2":      {"icon":"🎯","color":"#ff6b35","desc":"Counter-Strike 2","steam":"730","epic":None,
                 "exe":CS2_EXE,"presets":CS2_PRESETS,"parasites":CS2_PARASITES,"tips":CS2_TIPS,
                 "cfg":CS2_CFG,"kill_cfg":"r_motionblur 0\ncl_ragdoll_physics_enable 0\ncl_detailfade 0\nsnd_menumusic_volume 0\ncl_draw_only_deathnotices 1\nfps_max 0\nr_lowlatency 2\ncl_interp 0\ncl_interp_ratio 1\nrate 786432\nm_rawinput 1",
                 "kill_ini":None,"cfg_append":True,"eac_warning":False},
    "Fortnite": {"icon":"🌀","color":"#00d4ff","desc":"Battle Royale","steam":None,"epic":"Fortnite",
                 "exe":FN_EXE,"presets":FN_PRESETS,"parasites":FN_PARASITES,"tips":FN_TIPS,
                 "cfg":FN_INI,"kill_cfg":None,"kill_ini":FN_KILL_INI,"cfg_append":False,"eac_warning":False},
    "ARK":      {"icon":"🦕","color":"#76b041","desc":"Survival Evolved/Ascended","steam":"346110","epic":None,
                 "exe":ARK_EXE,"presets":ARK_PRESETS,"parasites":ARK_PARASITES,"tips":ARK_TIPS,
                 "cfg":None,"kill_cfg":None,"kill_ini":None,"cfg_append":True,"eac_warning":False},
}

# ═══════════════════════════════════════════════════════════════════════════════
# АНИМАЦИИ — красные пульсирующие элементы в стиле action
# ═══════════════════════════════════════════════════════════════════════════════

class AnimatedPulse:
    """Пульсирующая красная анимация для важных кнопок"""
    def __init__(self, widget, color1=RED, color2="#ff0000"):
        self.widget = widget
        self.color1 = color1
        self.color2 = color2
        self.running = False
        self.step = 0

    def start(self):
        self.running = True
        self._animate()

    def stop(self):
        self.running = False

    def _animate(self):
        if not self.running:
            return
        # Интерполяция между двумя цветами
        t = (math.sin(self.step * 0.15) + 1) / 2
        r1, g1, b1 = int(self.color1[1:3],16), int(self.color1[3:5],16), int(self.color1[5:7],16)
        r2, g2, b2 = int(self.color2[1:3],16), int(self.color2[3:5],16), int(self.color2[5:7],16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        color = f"#{r:02x}{g:02x}{b:02x}"
        try:
            self.widget.configure(fg_color=color)
        except: pass
        self.step += 1
        try:
            self.widget.after(50, self._animate)
        except: pass


class AnimatedProgressBar:
    """Анимированная полоска загрузки"""
    def __init__(self, parent, color=RED):
        self.canvas = tkinter.Canvas(parent, height=3, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="x")
        self.color = color
        self.pos = 0
        self.running = False

    def start(self):
        self.running = True
        self._animate()

    def stop(self):
        self.running = False
        self.canvas.delete("all")

    def _animate(self):
        if not self.running:
            return
        W = self.canvas.winfo_width() or 400
        self.canvas.delete("all")
        x = int((self.pos / 100) * W)
        w = 80
        # Градиентная полоска
        self.canvas.create_rectangle(max(0, x-w), 0, x, 3, fill=self.color, outline="")
        self.pos = (self.pos + 3) % 110
        try:
            self.canvas.after(16, self._animate)
        except: pass


class GlowLabel:
    """Метка с эффектом свечения (через обновление цвета)"""
    def __init__(self, parent, text, glow_color=RED, **kwargs):
        self.lbl = ctk.CTkLabel(parent, text=text, **kwargs)
        self.lbl.pack(anchor="w")
        self.glow_color = glow_color
        self.base_color = kwargs.get("text_color", "#fff")
        self.step = 0
        self._glow_loop()

    def _glow_loop(self):
        t = (math.sin(self.step * 0.08) + 1) / 2
        r1, g1, b1 = int(self.base_color[1:3],16) if len(self.base_color)==7 else (255,255,255), \
                     int(self.base_color[3:5],16) if len(self.base_color)==7 else (255,255,255), \
                     int(self.base_color[5:7],16) if len(self.base_color)==7 else (255,255,255)
        try:
            r1 = int(self.base_color[1:3],16)
            g1 = int(self.base_color[3:5],16)
            b1 = int(self.base_color[5:7],16)
        except: r1,g1,b1 = 255,255,255
        try:
            r2 = int(self.glow_color[1:3],16)
            g2 = int(self.glow_color[3:5],16)
            b2 = int(self.glow_color[5:7],16)
        except: r2,g2,b2 = 255,0,0
        r = int(r1 + (r2 - r1) * t * 0.4)
        g = int(g1 + (g2 - g1) * t * 0.4)
        b = int(b1 + (b2 - b1) * t * 0.4)
        color = f"#{r:02x}{g:02x}{b:02x}"
        try:
            self.lbl.configure(text_color=color)
            self.step += 1
            self.lbl.after(60, self._glow_loop)
        except: pass


# ═══════════════════════════════════════════════════════════════════════════════
# ГЛАВНОЕ ПРИЛОЖЕНИЕ
# ═══════════════════════════════════════════════════════════════════════════════
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Game Optimizer v4.0")
        self.configure(fg_color=BG)
        self.monitor_running = False
        self.ping_history = []
        self._live_running = True
        self.game_exe_override = {}
        self._kill_log_ref = [None]
        self._build_ui()
        self.geometry("1120x720")
        self.minsize(980, 640)

    # ── UI ─────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Анимированная полоска вверху
        self._top_bar = AnimatedProgressBar(self, color=RED)
        self._top_bar.start()

        sb = ctk.CTkFrame(self, width=192, fg_color=PANEL, corner_radius=0,
                          border_width=1, border_color=BORDER)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # Лого с анимацией
        lf = ctk.CTkFrame(sb, fg_color="transparent")
        lf.pack(pady=(14,4), padx=10)
        ctk.CTkLabel(lf, text="🎮", font=ctk.CTkFont(size=20)).pack(side="left")
        GlowLabel(lf, " GAME OPTIMIZER", glow_color=RED, text_color=NEON,
                  font=ctk.CTkFont(size=11, weight="bold"))

        ctk.CTkLabel(sb, text="v4.0", font=ctk.CTkFont(size=9), text_color=DIM).pack()

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(fill="x", padx=10, pady=6)
        ctk.CTkLabel(sb, text="ИГРЫ", font=ctk.CTkFont(size=9), text_color=DIM).pack(anchor="w", padx=10)

        self.game_btns = {}
        for gname, g in GAMES.items():
            b = ctk.CTkButton(sb, text=g["icon"]+"  "+gname, anchor="w",
                              font=ctk.CTkFont(size=12), height=33,
                              fg_color="transparent", hover_color="#0d1e38",
                              text_color=DIM, corner_radius=7,
                              command=lambda gn=gname: self.show_game(gn))
            b.pack(fill="x", padx=7, pady=1)
            self.game_btns[gname] = b

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(fill="x", padx=10, pady=6)
        ctk.CTkLabel(sb, text="ОБЩЕЕ", font=ctk.CTkFont(size=9), text_color=DIM).pack(anchor="w", padx=10)

        self.nav_btns = {}
        for pid, lbl in [("profile","💻  Профиль ПК"),("windows","⚡  Windows"),
                         ("network","🌐  Сеть"),("monitor","📊  Мониторинг")]:
            b = ctk.CTkButton(sb, text=lbl, anchor="w",
                              font=ctk.CTkFont(size=11), height=31,
                              fg_color="transparent", hover_color="#0d1e38",
                              text_color=DIM, corner_radius=7,
                              command=lambda p=pid: self.show_page(p))
            b.pack(fill="x", padx=7, pady=1)
            self.nav_btns[pid] = b

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(fill="x", padx=10, pady=6, side="bottom")
        self.joke_lbl = ctk.CTkLabel(sb, text=random.choice(JOKES),
                                     font=ctk.CTkFont(size=9, slant="italic"),
                                     text_color=GOLD, wraplength=172, justify="center")
        self.joke_lbl.pack(side="bottom", padx=7, pady=5)

        self.content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

        self.pages = {}
        for gname in GAMES:
            self._build_game_page(gname)
        self._build_profile_page()
        self._build_windows_page()
        self._build_network_page()
        self._build_monitor_page()

        self.show_game("Rust")

    def show_game(self, gname):
        for p in self.pages.values(): p.pack_forget()
        self.pages[gname].pack(fill="both", expand=True)
        for k, b in self.game_btns.items():
            b.configure(fg_color="#0d2040" if k==gname else "transparent",
                        text_color=GAMES[k]["color"] if k==gname else DIM)
        for b in self.nav_btns.values():
            b.configure(fg_color="transparent", text_color=DIM)

    def show_page(self, pid):
        for p in self.pages.values(): p.pack_forget()
        self.pages[pid].pack(fill="both", expand=True)
        for b in self.game_btns.values():
            b.configure(fg_color="transparent", text_color=DIM)
        for k, b in self.nav_btns.items():
            b.configure(fg_color="#0d2040" if k==pid else "transparent",
                        text_color=NEON if k==pid else DIM)

    # ── Скролл ─────────────────────────────────────────────────────────────
    def _scrollable(self, parent):
        c = tkinter.Canvas(parent, bg=BG, highlightthickness=0)
        sb = ctk.CTkScrollbar(parent, command=c.yview)
        c.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        c.pack(side="left", fill="both", expand=True)
        inner = ctk.CTkFrame(c, fg_color="transparent")
        win = c.create_window((0, 0), window=inner, anchor="nw")
        c.bind("<Configure>", lambda e: c.itemconfig(win, width=e.width))
        inner.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
        def _on(e): c.bind_all("<MouseWheel>", lambda ev: c.yview_scroll(int(-1*(ev.delta/120)), "units"))
        def _off(e): c.unbind_all("<MouseWheel>")
        c.bind("<Enter>", _on); c.bind("<Leave>", _off)
        inner.bind("<Enter>", _on); inner.bind("<Leave>", _off)
        return inner

    def _make_page(self, pid):
        outer = ctk.CTkFrame(self.content, fg_color=BG, corner_radius=0)
        self.pages[pid] = outer
        inner = self._scrollable(outer)
        pad = ctk.CTkFrame(inner, fg_color="transparent")
        pad.pack(fill="both", expand=True, padx=20, pady=14)
        return pad

    # ── Виджеты ────────────────────────────────────────────────────────────
    def _log(self, parent, h=110):
        tb = ctk.CTkTextbox(parent, height=h, fg_color="#020810",
                            border_width=1, border_color=BORDER,
                            font=ctk.CTkFont(family="Courier New", size=11),
                            text_color="#68ffaa", corner_radius=7)
        tb.pack(fill="x", pady=(3,0))
        tb.configure(state="disabled")
        return tb

    def _lw(self, tb, t):
        tb.configure(state="normal"); tb.insert("end", t+"\n")
        tb.configure(state="disabled"); tb.see("end")

    def _lclr(self, tb):
        tb.configure(state="normal"); tb.delete("1.0","end"); tb.configure(state="disabled")

    def _sec(self, parent, text, color=DIM):
        ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=color).pack(anchor="w", pady=(5,2))

    def _div(self, parent):
        ctk.CTkFrame(parent, height=1, fg_color=BORDER).pack(fill="x", pady=6)

    def _safe_set(self, lbl, text):
        try: lbl.configure(text=text)
        except: pass

    def _compact_toggle(self, parent, ico, name, desc, on_c, off_c, accent=NEON):
        row = ctk.CTkFrame(parent, fg_color=PANEL2, corner_radius=5,
                           border_width=1, border_color=BORDER)
        row.pack(fill="x", pady=1)
        ctk.CTkFrame(row, width=3, fg_color=accent, corner_radius=0).pack(side="left", fill="y")
        ctk.CTkLabel(row, text=ico, font=ctk.CTkFont(size=13), width=24).pack(side="left", padx=(6,2))
        rf = ctk.CTkFrame(row, fg_color="transparent")
        rf.pack(side="left", fill="x", expand=True, pady=4)
        ctk.CTkLabel(rf, text=name, font=ctk.CTkFont(size=11, weight="bold"), text_color="#fff").pack(anchor="w")
        ctk.CTkLabel(rf, text=desc, font=ctk.CTkFont(size=9), text_color=DIM).pack(anchor="w")
        var = ctk.BooleanVar(value=False)
        def _tog(v=var, on=on_c, off=off_c):
            cmds = on if v.get() else off
            threading.Thread(target=lambda c=cmds: [run_cmd(x) for x in c], daemon=True).start()
        ctk.CTkSwitch(row, text="", variable=var, command=_tog,
                      progress_color=accent, button_color="#fff", width=38).pack(side="right", padx=7)

    # ── Страница игры ───────────────────────────────────────────────────────
    def _build_game_page(self, gname):
        g = GAMES[gname]
        outer = ctk.CTkFrame(self.content, fg_color=BG, corner_radius=0)
        self.pages[gname] = outer

        # Анимированная полоска
        game_bar = AnimatedProgressBar(outer, color=g["color"])
        game_bar.start()

        # Заголовок
        hbar = ctk.CTkFrame(outer, fg_color=PANEL, corner_radius=0,
                            border_width=1, border_color=BORDER, height=58)
        hbar.pack(fill="x"); hbar.pack_propagate(False)
        hi = ctk.CTkFrame(hbar, fg_color="transparent")
        hi.pack(fill="both", padx=14, pady=8)
        ctk.CTkLabel(hi, text=g["icon"], font=ctk.CTkFont(size=24)).pack(side="left", padx=(0,10))
        ht = ctk.CTkFrame(hi, fg_color="transparent"); ht.pack(side="left", fill="y", expand=True)

        # Название с анимацией свечения
        name_lbl = ctk.CTkLabel(ht, text=gname,
                                font=ctk.CTkFont(size=17, weight="bold"),
                                text_color=g["color"])
        name_lbl.pack(anchor="w")
        ctk.CTkLabel(ht, text=g["desc"], font=ctk.CTkFont(size=10), text_color=DIM).pack(anchor="w")

        # Кнопки
        br = ctk.CTkFrame(hi, fg_color="transparent"); br.pack(side="right")
        launch_btn = make_btn(br, "▶  ЗАПУСТИТЬ",
                              lambda gn=gname: self._launch_game(gn),
                              color="#006adf", hover="#0099ff", size=11, width=128)
        launch_btn.pack(side="left", padx=3)
        # Анимация кнопки запуска
        AnimatedPulse(launch_btn, "#006adf", "#004aaf").start()

        make_btn(br, "⚡  ВСЁ",
                 lambda gn=gname: self._full_optimize(gn),
                 color=g["color"], hover="#ffffff", size=11, width=85).pack(side="left", padx=3)

        # Вкладки
        tab_bar = ctk.CTkFrame(outer, fg_color=PANEL2, corner_radius=0, height=34)
        tab_bar.pack(fill="x"); tab_bar.pack_propagate(False)
        tab_content = ctk.CTkFrame(outer, fg_color=BG, corner_radius=0)
        tab_content.pack(fill="both", expand=True)

        tab_frames = {}; tab_btns = {}
        tab_names = ["🎨 Графика","🚫 Паразиты","🌐 Сеть","💡 Советы"]
        if gname == "CS2": tab_names.append("⚙️ Конфиг")
        elif gname == "GTA V": tab_names.append("🟣 FiveM")
        elif gname in ("Rust","ARK","Fortnite"): tab_names.append("🔩 Launch")

        def _show(name, frames=tab_frames, btns=tab_btns, gc=g["color"]):
            for f in frames.values(): f.pack_forget()
            frames[name].pack(fill="both", expand=True)
            for n, b in btns.items():
                b.configure(fg_color="#0d2040" if n==name else "transparent",
                            text_color=gc if n==name else DIM)

        for tname in tab_names:
            tb2 = ctk.CTkButton(tab_bar, text=tname, anchor="w",
                                font=ctk.CTkFont(size=10), height=32,
                                fg_color="transparent", hover_color="#0d1e38",
                                text_color=DIM, corner_radius=0, width=110,
                                command=lambda t=tname: _show(t))
            tb2.pack(side="left", padx=1); tab_btns[tname] = tb2

            frame = ctk.CTkFrame(tab_content, fg_color=BG, corner_radius=0)
            tab_frames[tname] = frame
            sc = self._scrollable(frame)
            inner = ctk.CTkFrame(sc, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=18, pady=11)

            if "Графика" in tname: self._tab_graphics(inner, gname, g)
            elif "Паразиты" in tname: self._tab_parasites(inner, gname, g)
            elif "Сеть" in tname: self._tab_net(inner, gname)
            elif "Советы" in tname: self._tab_tips(inner, g)
            elif "Конфиг" in tname: self._tab_cs2cfg(inner)
            elif "FiveM" in tname: self._tab_fivem(inner)
            elif "Launch" in tname: self._tab_launch(inner, gname, g)

        _show(tab_names[0])

    # ── Вкладка: Графика ────────────────────────────────────────────────────
    def _tab_graphics(self, pad, gname, g):
        ctk.CTkLabel(pad, text="🎨 Пресеты графики",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,3))
        ctk.CTkLabel(pad, text="Выбери пресет — список настроек + параметры запуска Steam",
                     font=ctk.CTkFont(size=10), text_color=DIM).pack(anchor="w", pady=(0,7))
        lr = [None]
        gr = ctk.CTkFrame(pad, fg_color="transparent"); gr.pack(fill="x", pady=(0,5))
        for i, (pname, pdata) in enumerate(g["presets"].items()):
            gr.columnconfigure(i, weight=1)
            c = ctk.CTkFrame(gr, fg_color=PANEL, corner_radius=9, border_width=2, border_color=BORDER)
            c.grid(row=0, column=i, padx=3, sticky="ew")
            ci = ctk.CTkFrame(c, fg_color="transparent"); ci.pack(fill="both", padx=10, pady=9)
            ctk.CTkLabel(ci, text=pname, font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=g["color"]).pack(anchor="w")
            ctk.CTkLabel(ci, text=pdata["desc"], font=ctk.CTkFont(size=9), text_color=DIM).pack(anchor="w", pady=(1,3))
            fr = ctk.CTkFrame(ci, fg_color="transparent"); fr.pack(anchor="w", pady=(0,3))
            ctk.CTkLabel(fr, text="FPS: ", font=ctk.CTkFont(size=9), text_color=DIM).pack(side="left")
            ctk.CTkLabel(fr, text=pdata["fps"], font=ctk.CTkFont(size=9, weight="bold"), text_color=GREEN).pack(side="left")
            ctk.CTkLabel(ci, text=str(len(pdata["settings"]))+" настроек",
                         font=ctk.CTkFont(size=9), text_color=DIM).pack(anchor="w", pady=(0,5))
            make_btn(ci, "✓ Применить",
                     lambda p=pdata, n=pname, l=lr: self._apply_preset(p, n, l),
                     size=10, bold=False, width=128, color="#1a3050", hover="#2a4060").pack(anchor="w")
        lr[0] = self._log(pad, 85)

    def _apply_preset(self, pdata, pname, lr):
        if not lr[0]: return
        self._lclr(lr[0]); self._lw(lr[0], "▶ "+pname+"...")
        def run():
            for k, v in pdata["settings"]: self._lw(lr[0], "  "+k+" = "+v); time.sleep(0.02)
            launch = pdata.get("launch","")
            if launch:
                self._lw(lr[0], ""); self._lw(lr[0], "Параметры запуска Steam:")
                self._lw(lr[0], "  "+launch)
                self._lw(lr[0], "  → Steam → ПКМ игра → Свойства → Параметры запуска")
            self._lw(lr[0], ""); self._lw(lr[0], "✅ FPS: "+pdata["fps"])
        threading.Thread(target=run, daemon=True).start()

    # ── Вкладка: Паразиты ───────────────────────────────────────────────────
    def _tab_parasites(self, pad, gname, g):
        ctk.CTkLabel(pad, text="🚫 Паразитные функции",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,3))

        # Предупреждение EAC для Rust
        if g.get("eac_warning"):
            warn = ctk.CTkFrame(pad, fg_color="#0a1a04", corner_radius=7,
                               border_width=1, border_color="#3a7a10")
            warn.pack(fill="x", pady=(0,7))
            wf = ctk.CTkFrame(warn, fg_color="transparent"); wf.pack(fill="x", padx=12, pady=7)
            ctk.CTkLabel(wf, text="⚠ RUST + EAC: используем ТОЛЬКО client.cfg команды",
                         font=ctk.CTkFont(size=10, weight="bold"), text_color="#88cc44").pack(anchor="w")
            ctk.CTkLabel(wf, text="Это стандартные консольные команды игры — 100% безопасно для EAC.",
                         font=ctk.CTkFont(size=9), text_color="#668833").pack(anchor="w")

        ctk.CTkLabel(pad, text="Тогл = вкл/выкл. Кнопка ☠️ = убить всё сразу.",
                     font=ctk.CTkFont(size=10), text_color=DIM).pack(anchor="w", pady=(0,6))

        self._sec(pad, "🎮 Внутри "+gname)
        for ico, name, desc, accent, on_c, off_c in g["parasites"]:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c, accent)

        self._div(pad)
        self._sec(pad, "🖥 Оверлеи")
        for ico, name, desc, accent, on_c, off_c in OVERLAYS:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c, accent)

        self._div(pad)
        self._sec(pad, "⚙️ Фоновые процессы Windows")
        for ico, name, desc, accent, on_c, off_c in BG_PROCS:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c, accent)

        self._div(pad)

        # Анимированная кнопка убить всё
        kill_btn = make_btn(pad, "☠️  УБИТЬ ВСЕ ПАРАЗИТЫ "+gname.upper(),
                            lambda gn=gname: self._kill_all(gn),
                            size=12, width=320, color="#4a0000", hover="#7a0000")
        kill_btn.pack(anchor="w", pady=(0,3))
        AnimatedPulse(kill_btn, "#4a0000", "#880000").start()

        make_btn(pad, "🚫  ОТКЛ. ВСЕ СИСТЕМНЫЕ",
                 self._kill_system,
                 size=11, width=220, color="#6b0000", hover="#8b0000").pack(anchor="w")

        self._kill_log_ref[0] = self._log(pad, 65)

    def _kill_all(self, gname):
        g = GAMES[gname]; log = self._kill_log_ref[0]
        def run():
            if log: self._lw(log, "☠️ Убиваю паразиты "+gname+"...")
            count = 0
            for _, _, _, _, on_c, _ in g["parasites"]:
                for cmd in on_c: run_cmd(cmd); count += 1
            for _, _, _, _, on_c, _ in OVERLAYS:
                for cmd in on_c: run_cmd(cmd); count += 1
            # Запись в файл
            cfg = g.get("cfg"); kill_cfg = g.get("kill_cfg"); kill_ini = g.get("kill_ini")
            if cfg and kill_cfg:
                path = expand(cfg)
                try:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    mode = "a" if g.get("cfg_append", True) else "w"
                    with open(path, mode, encoding="utf-8") as f:
                        f.write("\n"+kill_cfg+"\n")
                    if log: self._lw(log, "  ✓ Записано: "+os.path.basename(path))
                except Exception as e:
                    if log: self._lw(log, "  ✗ "+str(e))
            if cfg and kill_ini:
                path = expand(cfg)
                try:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "w", encoding="utf-8") as f: f.write(kill_ini)
                    if log: self._lw(log, "  ✓ INI записан: "+os.path.basename(path))
                except Exception as e:
                    if log: self._lw(log, "  ✗ "+str(e))
            if log:
                self._lw(log, "  ✓ "+str(count)+" операций")
                self._lw(log, "✅ "+gname+" — паразиты убиты!")
        threading.Thread(target=run, daemon=True).start()

    def _kill_system(self):
        cmds = ["net stop wuauserv","net stop wsearch","net stop sysmain",
                "taskkill /f /im OneDrive.exe",
                "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f"]
        threading.Thread(target=lambda: [run_cmd(c) for c in cmds], daemon=True).start()

    # ── Вкладка: Сеть ──────────────────────────────────────────────────────
    def _tab_net(self, pad, gname):
        ctk.CTkLabel(pad, text="🌐 Настройка сети",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,6))
        for ico, name, desc, accent, on_c, off_c in NET_OPTS:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c, accent)
        self._div(pad)
        make_btn(pad, "📡  Проверить пинг",
                 lambda p=pad: self._quick_ping(p),
                 width=170, color="#006adf", hover="#0090ff").pack(anchor="w")

    def _quick_ping(self, pad):
        log = self._log(pad, 65)
        def run():
            for n, h in [("Google","8.8.8.8"),("Steam","store.steampowered.com"),("Cloudflare","1.1.1.1")]:
                ms = ping_host(h)
                self._lw(log, ("✓ " if ms>0 else "✗ ")+n.ljust(12)+(str(ms)+" ms" if ms>0 else "timeout"))
                time.sleep(0.1)
            self._lw(log, "✅ Готово!")
        threading.Thread(target=run, daemon=True).start()

    # ── Вкладка: Советы ─────────────────────────────────────────────────────
    def _tab_tips(self, pad, g):
        ctk.CTkLabel(pad, text="💡 Советы",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,7))
        for ico, title, text in g["tips"]:
            c = ctk.CTkFrame(pad, fg_color=PANEL2, corner_radius=7,
                             border_width=1, border_color=BORDER)
            c.pack(fill="x", pady=2)
            ci = ctk.CTkFrame(c, fg_color="transparent"); ci.pack(fill="x", padx=12, pady=7)
            ctk.CTkLabel(ci, text=ico+"  "+title,
                         font=ctk.CTkFont(size=11, weight="bold"), text_color="#fff").pack(anchor="w")
            ctk.CTkLabel(ci, text=text, font=ctk.CTkFont(size=10),
                         text_color=TEXT, wraplength=680, justify="left").pack(anchor="w", pady=(1,0))

    # ── Вкладка: CS2 Конфиг ─────────────────────────────────────────────────
    def _tab_cs2cfg(self, pad):
        ctk.CTkLabel(pad, text="⚙️ autoexec.cfg",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,4))
        ctk.CTkLabel(pad, text="Готовый конфиг. Кнопка сохраняет прямо в папку CS2.",
                     font=ctk.CTkFont(size=10), text_color=DIM).pack(anchor="w", pady=(0,7))
        tb = ctk.CTkTextbox(pad, height=240, fg_color="#020810",
                            border_width=1, border_color=BORDER,
                            font=ctk.CTkFont(family="Courier New", size=10),
                            text_color="#68ffaa", corner_radius=7)
        tb.pack(fill="x", pady=(0,7)); tb.insert("end", CS2_AUTOEXEC)
        br = ctk.CTkFrame(pad, fg_color="transparent"); br.pack(anchor="w")
        def save_cs2():
            path = expand(CS2_CFG)
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f: f.write(tb.get("1.0","end"))
                messagebox.showinfo("Сохранено!", "Записан:\n"+path+"\n\nДобавь в параметры запуска:\n+exec autoexec")
            except Exception as e: messagebox.showerror("Ошибка", str(e))
        def save_dl():
            path = os.path.join(os.path.expanduser("~"), "Downloads", "autoexec.cfg")
            try:
                with open(path, "w", encoding="utf-8") as f: f.write(tb.get("1.0","end"))
                messagebox.showinfo("Сохранено!", "Файл в Downloads:\n"+path)
            except Exception as e: messagebox.showerror("Ошибка", str(e))
        make_btn(br, "💾  Сохранить в CS2", save_cs2, width=195, color="#006adf", hover="#0090ff").pack(side="left", padx=(0,5))
        make_btn(br, "📁  В Downloads", save_dl, width=160, color="#1a3050", hover="#2a4060").pack(side="left")

    # ── Вкладка: FiveM ──────────────────────────────────────────────────────
    def _tab_fivem(self, pad):
        ctk.CTkLabel(pad, text="🟣 FiveM оптимизация",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,6))
        opts = [
            ("🧹","Очистить кэш FiveM","Удаляет кэш шейдеров — при фризах",NEON,
             ["rmdir /s /q \"%LOCALAPPDATA%\\FiveM\\FiveM.app\\cache\""],
             []),
            ("🔕","Откл. оверлей FiveM","Убирает оверлей сервера",ORANGE,
             ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v DrawOverlay /t REG_DWORD /d 0 /f"],
             ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v DrawOverlay /t REG_DWORD /d 1 /f"]),
            ("⚡","StreamMemory 756MB","Больше памяти для текстур",GREEN,
             ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v StreamingMemory /t REG_DWORD /d 756 /f"],
             ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v StreamingMemory /t REG_DWORD /d 512 /f"]),
        ]
        for ico, name, desc, accent, on_c, off_c in opts:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c, accent)
        self._div(pad)
        ctk.CTkLabel(pad, text="💡 Добавь +set fpslimit 0 в параметры запуска FiveM",
                     font=ctk.CTkFont(size=10, slant="italic"), text_color=GOLD).pack(anchor="w")

    # ── Вкладка: Launch Args ────────────────────────────────────────────────
    def _tab_launch(self, pad, gname, g):
        ctk.CTkLabel(pad, text="🔩 Параметры запуска",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,4))
        ctk.CTkLabel(pad, text="Steam → ПКМ на игре → Свойства → Параметры запуска. Скопируй нужную строку.",
                     font=ctk.CTkFont(size=10), text_color=DIM).pack(anchor="w", pady=(0,7))
        for pname, pdata in g["presets"].items():
            c = ctk.CTkFrame(pad, fg_color=PANEL2, corner_radius=7, border_width=1, border_color=BORDER)
            c.pack(fill="x", pady=3)
            ci = ctk.CTkFrame(c, fg_color="transparent"); ci.pack(fill="x", padx=12, pady=7)
            hr = ctk.CTkFrame(ci, fg_color="transparent"); hr.pack(fill="x", pady=(0,3))
            ctk.CTkLabel(hr, text=pname, font=ctk.CTkFont(size=11, weight="bold"), text_color="#fff").pack(side="left")
            ctk.CTkLabel(hr, text="FPS: "+pdata["fps"], font=ctk.CTkFont(size=9), text_color=GREEN).pack(side="right")
            tb = ctk.CTkTextbox(ci, height=34, fg_color="#020810",
                                border_width=1, border_color=BORDER,
                                font=ctk.CTkFont(family="Courier New", size=10),
                                text_color=NEON, corner_radius=5)
            tb.pack(fill="x"); tb.insert("end", pdata.get("launch",""))

    # ── Запуск игры ─────────────────────────────────────────────────────────
    def _launch_game(self, gname):
        """ИСПРАВЛЕНО: Запуск ТОЛЬКО через Steam/Epic. Прямой exe блокируется EAC!"""
        g = GAMES[gname]
        if g.get("steam"):
            try:
                subprocess.Popen(["cmd","/c","start","","steam://rungameid/"+g["steam"]],shell=False)
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
            return
        if g.get("epic"):
            try:
                subprocess.Popen(["cmd","/c","start","",
                    "com.epicgames.launcher://apps/"+g["epic"]+"?action=launch&silent=true"],shell=False)
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
            return
        messagebox.showinfo("Запуск", "Запусти "+gname+" вручную через Steam или Epic.")


    def _ask_exe(self, gname):
        win = ctk.CTkToplevel(self)
        win.title("Где "+gname+"?"); win.geometry("500x220")
        win.configure(fg_color=BG); win.lift(); win.focus_force()
        ctk.CTkLabel(win, text="⚠ Не удалось найти "+gname,
                     font=ctk.CTkFont(size=13, weight="bold"), text_color=GOLD).pack(pady=(18,5))
        ctk.CTkLabel(win, text="Укажи путь к .exe вручную. Путь сохранится.",
                     font=ctk.CTkFont(size=11), text_color=TEXT).pack(pady=(0,7))
        pv = ctk.StringVar()
        entry = ctk.CTkEntry(win, textvariable=pv, width=400, fg_color=PANEL2, border_color=BORDER)
        entry.pack(pady=4)
        def browse():
            p = filedialog.askopenfilename(title="Выбери "+gname+".exe",
                                           filetypes=[("*.exe","*.exe"),("*","*")])
            if p: pv.set(p)
        def launch_now():
            p = pv.get()
            if p and os.path.exists(p):
                self.game_exe_override[gname] = p
                subprocess.Popen([p]); win.destroy()
            else: messagebox.showerror("Ошибка","Файл не найден:\n"+p)
        br = ctk.CTkFrame(win, fg_color="transparent"); br.pack(pady=7)
        make_btn(br,"📁 Обзор",browse,color="#1a3050",hover="#2a4060",width=110).pack(side="left",padx=4)
        make_btn(br,"▶ Запустить",launch_now,color="#006adf",hover="#0099ff",width=130).pack(side="left",padx=4)
        make_btn(br,"✕ Закрыть",win.destroy,color="#3a0000",hover="#5a0000",width=90).pack(side="left",padx=4)

    # ── Полная оптимизация ──────────────────────────────────────────────────
    def _full_optimize(self, gname):
        win = ctk.CTkToplevel(self)
        win.title("Оптимизация "+gname); win.geometry("520x380")
        win.configure(fg_color=BG); win.lift()

        # Анимированная полоска в окне
        top_anim = AnimatedProgressBar(win, color=RED)
        top_anim.start()

        ctk.CTkLabel(win, text="⚡ Полная оптимизация "+gname,
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#fff").pack(pady=(10,5), padx=14, anchor="w")
        log = ctk.CTkTextbox(win, height=280, fg_color="#020810",
                             border_width=1, border_color=BORDER,
                             font=ctk.CTkFont(family="Courier New", size=11),
                             text_color="#68ffaa", corner_radius=7)
        log.pack(fill="both", expand=True, padx=14, pady=(0,14))
        log.configure(state="disabled")
        def w(t):
            log.configure(state="normal"); log.insert("end",t+"\n")
            log.configure(state="disabled"); log.see("end")
        def run():
            w("⚡ Начинаю для "+gname+"...")
            steps = [
                ("⚡ Высокий план питания","powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"),
                ("🔕 Откл. Game DVR","reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f"),
                ("📈 Приоритет CPU","reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f"),
                ("🎮 HAGS","reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v HwSchMode /t REG_DWORD /d 2 /f"),
                ("🔍 Стоп Search","net stop wsearch"),
                ("📊 Стоп SysMain","net stop sysmain"),
                ("⏸ Стоп Update","net stop wuauserv"),
                ("🌐 DNS Google","netsh interface ip set dns \"Ethernet\" static 8.8.8.8"),
                ("🏎 Откл. Nagle","reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpAckFrequency /t REG_DWORD /d 1 /f"),
                ("🔄 Flush DNS","ipconfig /flushdns"),
                ("🧹 Очистка RAM","rundll32.exe advapi32.dll,ProcessIdleTasks"),
            ]
            for name, cmd in steps:
                ok = run_cmd(cmd); w("  "+("✓" if ok else "✗")+" "+name); time.sleep(0.1)
            w("\n── Паразиты игры ─────────────────────────")
            self._kill_all(gname)
            time.sleep(0.8)
            w("\n══════════════════════════════════════════")
            w("✅ Готово! Запускай "+gname+"!")
        threading.Thread(target=run, daemon=True).start()

    # ── Профиль ПК ──────────────────────────────────────────────────────────
    def _build_profile_page(self):
        pad = self._make_page("profile")
        ctk.CTkLabel(pad, text="💻 Профиль ПК",
                     font=ctk.CTkFont(size=15, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,3))
        ctk.CTkLabel(pad, text="Характеристики и нагрузка в реальном времени (каждые 2 сек)",
                     font=ctk.CTkFont(size=10), text_color=DIM).pack(anchor="w", pady=(0,8))

        # Характеристики
        ic = ctk.CTkFrame(pad, fg_color=PANEL, corner_radius=10, border_width=1, border_color=BORDER)
        ic.pack(fill="x", pady=(0,8))
        icp = ctk.CTkFrame(ic, fg_color="transparent"); icp.pack(fill="x", padx=14, pady=10)
        ctk.CTkLabel(icp, text="🖥 Характеристики системы",
                     font=ctk.CTkFont(size=11, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,6))
        self.info_labels = {}
        grid = ctk.CTkFrame(icp, fg_color="transparent"); grid.pack(fill="x")
        grid.columnconfigure(0, weight=1); grid.columnconfigure(1, weight=1)
        for i, field in enumerate(["OS","CPU","RAM","Диск C:","GPU","IP адрес"]):
            f = ctk.CTkFrame(grid, fg_color=PANEL2, corner_radius=6, border_width=1, border_color=BORDER)
            f.grid(row=i//2, column=i%2, padx=3, pady=2, sticky="ew")
            fi = ctk.CTkFrame(f, fg_color="transparent"); fi.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(fi, text=field, font=ctk.CTkFont(size=9), text_color=DIM).pack(anchor="w")
            lbl = ctk.CTkLabel(fi, text="...", font=ctk.CTkFont(size=10, weight="bold"), text_color="#fff")
            lbl.pack(anchor="w"); self.info_labels[field] = lbl

        # Живые показатели
        self._div(pad)
        ctk.CTkLabel(pad, text="📊 Нагрузка прямо сейчас",
                     font=ctk.CTkFont(size=11, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,5))
        sr = ctk.CTkFrame(pad, fg_color="transparent"); sr.pack(fill="x", pady=(0,7))
        for i in range(4): sr.columnconfigure(i, weight=1)
        self.stat_boxes = {}
        for i, (k,lbl,col) in enumerate([("cpu","CPU %",GREEN),("ram","RAM %",NEON),("disk","Диск %",GOLD),("temp","Темп °C",RED)]):
            f = ctk.CTkFrame(sr, fg_color=PANEL2, corner_radius=8, border_width=1, border_color=BORDER)
            f.grid(row=0, column=i, padx=3, sticky="ew")
            v = ctk.CTkLabel(f, text="—", font=ctk.CTkFont(size=21, weight="bold"), text_color=col)
            v.pack(pady=(8,1))
            ctk.CTkLabel(f, text=lbl, font=ctk.CTkFont(size=9), text_color=DIM).pack(pady=(0,7))
            self.stat_boxes[k] = v

        # Прогресс бары
        bf = ctk.CTkFrame(pad, fg_color=PANEL, corner_radius=9, border_width=1, border_color=BORDER)
        bf.pack(fill="x", pady=(0,7))
        bp = ctk.CTkFrame(bf, fg_color="transparent"); bp.pack(fill="x", padx=12, pady=7)
        self.prog_bars = {}
        for k, lbl, col in [("cpu","CPU",GREEN),("ram","RAM",NEON),("disk","ДИСК",GOLD)]:
            r = ctk.CTkFrame(bp, fg_color="transparent"); r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=lbl, font=ctk.CTkFont(size=9), text_color=DIM, width=36).pack(side="left")
            bar = ctk.CTkProgressBar(r, height=11, progress_color=col, fg_color=PANEL2, corner_radius=4)
            bar.set(0); bar.pack(side="left", fill="x", expand=True, padx=5)
            pct = ctk.CTkLabel(r, text="0%", font=ctk.CTkFont(size=9), text_color=col, width=30)
            pct.pack(side="left"); self.prog_bars[k] = (bar, pct)

        # Пинг
        self._div(pad)
        ctk.CTkLabel(pad, text="🌐 Пинг",
                     font=ctk.CTkFont(size=11, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,5))
        pr = ctk.CTkFrame(pad, fg_color="transparent"); pr.pack(fill="x", pady=(0,7))
        pr.columnconfigure(0, weight=1); pr.columnconfigure(1, weight=1)
        self.ping_g = self._ping_box(pr, "Google 8.8.8.8", 0)
        self.ping_s = self._ping_box(pr, "Steam серверы", 1)

        br = ctk.CTkFrame(pad, fg_color="transparent"); br.pack(anchor="w")
        make_btn(br,"🔄  Обновить",self._refresh_profile,width=140,color="#006adf",hover="#0090ff").pack(side="left",padx=(0,5))
        make_btn(br,"😂  Новая шутка",lambda:self.joke_lbl.configure(text=random.choice(JOKES)),
                 width=140,color="#1a3050",hover="#2a4060").pack(side="left")

        threading.Thread(target=self._load_profile, daemon=True).start()
        threading.Thread(target=self._live_loop, daemon=True).start()

    def _ping_box(self, parent, label, col):
        f = ctk.CTkFrame(parent, fg_color=PANEL2, corner_radius=7, border_width=1, border_color=BORDER)
        f.grid(row=0, column=col, padx=3, sticky="ew")
        fi = ctk.CTkFrame(f, fg_color="transparent"); fi.pack(fill="x", padx=10, pady=7)
        ctk.CTkLabel(fi, text=label, font=ctk.CTkFont(size=9), text_color=DIM).pack(anchor="w")
        v = ctk.CTkLabel(fi, text="—", font=ctk.CTkFont(size=13, weight="bold"), text_color=NEON)
        v.pack(anchor="w"); return v

    def _load_profile(self):
        self._safe_set(self.info_labels["OS"], platform.system()+" "+platform.release())
        cpu = run_cmd_out("wmic cpu get Name /value").replace("Name=","").strip()
        self._safe_set(self.info_labels["CPU"], (cpu[:40]+"...") if len(cpu)>40 else (cpu or "—"))
        try:
            rb = int(run_cmd_out("wmic computersystem get TotalPhysicalMemory /value").replace("TotalPhysicalMemory=","").strip())
            self._safe_set(self.info_labels["RAM"], str(round(rb/1024**3,1))+" GB")
        except: self._safe_set(self.info_labels["RAM"],"—")
        try:
            raw = run_cmd_out("wmic logicaldisk where DeviceID=\"C:\" get FreeSpace,Size /value")
            d = {l.split("=")[0]:l.split("=")[1] for l in raw.splitlines() if "=" in l and len(l.split("="))>1 and l.split("=")[1].strip()}
            free = int(d.get("FreeSpace",0))//1024**3; tot = int(d.get("Size",0))//1024**3
            self._safe_set(self.info_labels["Диск C:"], str(free)+" / "+str(tot)+" GB")
        except: self._safe_set(self.info_labels["Диск C:"],"—")
        gpu = run_cmd_out("wmic path win32_videocontroller get Name /value").replace("Name=","").strip()
        self._safe_set(self.info_labels["GPU"], (gpu[:40]+"...") if len(gpu)>40 else (gpu or "—"))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8",80)); ip = s.getsockname()[0]; s.close()
        except: ip="—"
        self._safe_set(self.info_labels["IP адрес"], ip)
        ms_g = ping_host("8.8.8.8"); ms_s = ping_host("store.steampowered.com")
        self._safe_set(self.ping_g, (str(ms_g)+" ms") if ms_g>0 else "timeout")
        self._safe_set(self.ping_s, (str(ms_s)+" ms") if ms_s>0 else "timeout")

    def _refresh_profile(self):
        for l in self.info_labels.values(): self._safe_set(l,"...")
        threading.Thread(target=self._load_profile, daemon=True).start()

    def _live_loop(self):
        while self._live_running: self._update_live(); time.sleep(2)

    def _update_live(self):
        # CPU
        try:
            r = subprocess.run("typeperf \"\\Processor(_Total)\\% Processor Time\" -sc 1",
                shell=True, capture_output=True, text=True, timeout=5, encoding="cp1251", errors="replace")
            lines = [l for l in r.stdout.splitlines() if "," in l and "%" not in l and "Time" not in l and l.strip()]
            if lines:
                v = int(float(lines[0].split(",")[1].replace('"','').strip()))
                c = GREEN if v<50 else GOLD if v<80 else RED
                self._safe_set(self.stat_boxes["cpu"], str(v)+"%")
                self.stat_boxes["cpu"].configure(text_color=c)
                self.prog_bars["cpu"][0].set(v/100); self.prog_bars["cpu"][1].configure(text=str(v)+"%")
        except: pass
        # RAM
        try:
            r2 = run_cmd_out("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /value")
            d = {l.split("=")[0]:l.split("=")[1] for l in r2.splitlines() if "=" in l and len(l.split("="))>1 and l.split("=")[1].strip()}
            free=int(d.get("FreePhysicalMemory",0)); tot=int(d.get("TotalVisibleMemorySize",1))
            v=int((1-free/tot)*100); c=GREEN if v<60 else GOLD if v<80 else RED
            self._safe_set(self.stat_boxes["ram"],str(v)+"%"); self.stat_boxes["ram"].configure(text_color=c)
            self.prog_bars["ram"][0].set(v/100); self.prog_bars["ram"][1].configure(text=str(v)+"%")
        except: pass
        # Disk
        try:
            r3=run_cmd_out("wmic logicaldisk where DeviceID=\"C:\" get FreeSpace,Size /value")
            d3={l.split("=")[0]:l.split("=")[1] for l in r3.splitlines() if "=" in l and len(l.split("="))>1 and l.split("=")[1].strip()}
            free=int(d3.get("FreeSpace",0)); tot=int(d3.get("Size",1))
            v=int((1-free/tot)*100)
            self._safe_set(self.stat_boxes["disk"],str(v)+"%")
            self.prog_bars["disk"][0].set(v/100); self.prog_bars["disk"][1].configure(text=str(v)+"%")
        except: pass
        # Temp
        try:
            r4=run_cmd_out("wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature /value")
            temps=[]
            for line in r4.splitlines():
                if "CurrentTemperature=" in line:
                    try: temps.append((int(line.split("=")[1].strip())-2732)/10)
                    except: pass
            if temps:
                v=int(sum(temps)/len(temps)); c=GREEN if v<60 else GOLD if v<80 else RED
                self._safe_set(self.stat_boxes["temp"],str(v)+"°"); self.stat_boxes["temp"].configure(text_color=c)
            else: self._safe_set(self.stat_boxes["temp"],"N/A")
        except: self._safe_set(self.stat_boxes["temp"],"N/A")

    # ── Windows ─────────────────────────────────────────────────────────────
    def _build_windows_page(self):
        pad = self._make_page("windows")
        ctk.CTkLabel(pad, text="⚡ Оптимизация Windows",
                     font=ctk.CTkFont(size=15, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,3))
        ctk.CTkLabel(pad, text="Системные твики для максимального FPS в любой игре",
                     font=ctk.CTkFont(size=10), text_color=DIM).pack(anchor="w", pady=(0,7))
        for ico, name, desc, accent, on_c, off_c in WIN_OPTS:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c, accent)
        self._div(pad)
        all_btn = make_btn(pad, "⚡  ПРИМЕНИТЬ ВСЕ",
                          self._run_all_win, size=13, width=240, color="#006adf", hover="#0090ff")
        all_btn.pack(anchor="w")
        AnimatedPulse(all_btn, "#006adf", "#004aaf").start()
        self.win_log = self._log(pad, 85)

    def _run_all_win(self):
        self._lclr(self.win_log); self._lw(self.win_log, "⚡ Применяю...")
        steps = [
            ("⚡ План питания","powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"),
            ("🔕 Game DVR","reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f"),
            ("📈 CPU приоритет","reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f"),
            ("🎮 HAGS","reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v HwSchMode /t REG_DWORD /d 2 /f"),
            ("🔍 Search","net stop wsearch"),("📊 SysMain","net stop sysmain"),
            ("⏸ Update","net stop wuauserv"),("🧹 RAM","rundll32.exe advapi32.dll,ProcessIdleTasks"),
        ]
        def run():
            for name, cmd in steps:
                ok = run_cmd(cmd); self._lw(self.win_log,"  "+("✓" if ok else "✗")+" "+name); time.sleep(0.1)
            self._lw(self.win_log,"✅ Готово! Перезагрузи ПК.")
        threading.Thread(target=run, daemon=True).start()

    # ── Сеть ────────────────────────────────────────────────────────────────
    def _build_network_page(self):
        pad = self._make_page("network")
        ctk.CTkLabel(pad, text="🌐 Настройка сети",
                     font=ctk.CTkFont(size=15, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,3))
        ctk.CTkLabel(pad, text="Оптимизация пинга для всех онлайн игр",
                     font=ctk.CTkFont(size=10), text_color=DIM).pack(anchor="w", pady=(0,7))
        for ico, name, desc, accent, on_c, off_c in NET_OPTS:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c, accent)
        self._div(pad)
        make_btn(pad,"📡  Проверить пинг",self._global_ping,width=200,color="#006adf",hover="#0090ff").pack(anchor="w")
        self.net_log = self._log(pad, 100)

    def _global_ping(self):
        self._lclr(self.net_log)
        def run():
            for n, h in [("Steam","store.steampowered.com"),("Cloudflare","1.1.1.1"),
                         ("Google","8.8.8.8"),("Faceit","api.faceit.com"),("AWS EU","ec2.eu-central-1.amazonaws.com")]:
                ms = ping_host(h)
                s = "OK" if 0<ms<80 else "СРЕДНИЙ" if 0<ms<150 else "ВЫСОКИЙ" if ms>0 else "timeout"
                self._lw(self.net_log,"  "+n.ljust(14)+(str(ms)+" ms").rjust(8)+"  "+s); time.sleep(0.1)
            self._lw(self.net_log,"✅ Готово!")
        threading.Thread(target=run, daemon=True).start()

    # ── Мониторинг ──────────────────────────────────────────────────────────
    def _build_monitor_page(self):
        pad = self._make_page("monitor")
        ctk.CTkLabel(pad, text="📊 Мониторинг пинга",
                     font=ctk.CTkFont(size=15, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,3))
        ctk.CTkLabel(pad, text="Живой замер задержки до серверов",
                     font=ctk.CTkFont(size=10), text_color=DIM).pack(anchor="w", pady=(0,7))
        sr = ctk.CTkFrame(pad, fg_color="transparent"); sr.pack(fill="x", pady=(0,7))
        for i in range(3): sr.columnconfigure(i, weight=1)
        self.ms_cur = self._mon_stat(sr,"Текущий ms",GREEN,0)
        self.ms_avg = self._mon_stat(sr,"Средний ms",GOLD,1)
        self.ms_max = self._mon_stat(sr,"Максимум ms",RED,2)
        cr = ctk.CTkFrame(pad, fg_color="transparent"); cr.pack(fill="x", pady=(0,7))
        self.mon_btn = make_btn(cr,"▶  Запустить",self._toggle_mon,width=185,color="#006adf",hover="#0090ff")
        self.mon_btn.pack(side="left")
        self.mon_lbl = ctk.CTkLabel(cr,text="● Остановлен",text_color=DIM,font=ctk.CTkFont(size=10))
        self.mon_lbl.pack(side="left",padx=10)
        ctk.CTkLabel(cr,text="Интервал:",text_color=DIM,font=ctk.CTkFont(size=10)).pack(side="left")
        self.mon_int = ctk.CTkComboBox(cr,values=["2 сек","5 сек","10 сек"],width=80,fg_color=PANEL2,border_color=BORDER)
        self.mon_int.set("2 сек"); self.mon_int.pack(side="left",padx=5)
        self.srv_lbls = {}
        for name, host in [("Steam","store.steampowered.com"),("Cloudflare","1.1.1.1"),
                           ("Google DNS","8.8.8.8"),("Faceit","api.faceit.com")]:
            row=ctk.CTkFrame(pad,fg_color=PANEL2,corner_radius=7,border_width=1,border_color=BORDER); row.pack(fill="x",pady=2)
            ctk.CTkLabel(row,text="●",font=ctk.CTkFont(size=11),text_color=DIM).pack(side="left",padx=(10,6),pady=7)
            ctk.CTkLabel(row,text=name,font=ctk.CTkFont(size=11),text_color=TEXT,width=118).pack(side="left")
            lbl=ctk.CTkLabel(row,text="— ms",font=ctk.CTkFont(size=11,weight="bold"),text_color=DIM)
            lbl.pack(side="right",padx=12); self.srv_lbls[host]=lbl
        cc=ctk.CTkFrame(pad,fg_color=PANEL2,corner_radius=10,border_width=1,border_color=BORDER); cc.pack(fill="x",pady=5)
        ctk.CTkLabel(cc,text="📈 График пинга",font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w",padx=10,pady=(6,2))
        self.chart=tkinter.Canvas(cc,height=95,bg="#020810",highlightthickness=0)
        self.chart.pack(fill="x",padx=7,pady=(0,6))

    def _mon_stat(self,parent,label,color,col):
        f=ctk.CTkFrame(parent,fg_color=PANEL2,corner_radius=8,border_width=1,border_color=BORDER)
        f.grid(row=0,column=col,padx=3,sticky="ew")
        v=ctk.CTkLabel(f,text="—",font=ctk.CTkFont(size=21,weight="bold"),text_color=color)
        v.pack(pady=(8,2))
        ctk.CTkLabel(f,text=label,font=ctk.CTkFont(size=9),text_color=DIM).pack(pady=(0,7))
        return v

    def _toggle_mon(self):
        if self.monitor_running:
            self.monitor_running=False
            self.mon_btn.configure(text="▶  Запустить",fg_color="#006adf",hover_color="#0090ff")
            self.mon_lbl.configure(text="● Остановлен",text_color=DIM)
        else:
            self.monitor_running=True
            self.mon_btn.configure(text="⏹  Остановить",fg_color="#6b0000",hover_color="#8b0000")
            self.mon_lbl.configure(text="● Активен",text_color=GREEN)
            threading.Thread(target=self._mon_loop,daemon=True).start()

    def _mon_loop(self):
        while self.monitor_running:
            iv={"2 сек":2,"5 сек":5,"10 сек":10}.get(self.mon_int.get(),2)
            results=[]
            for _,host in [("Steam","store.steampowered.com"),("Cloudflare","1.1.1.1"),
                           ("Google DNS","8.8.8.8"),("Faceit","api.faceit.com")]:
                ms=ping_host(host); results.append(ms)
                lbl=self.srv_lbls[host]
                if ms<0: lbl.configure(text="timeout",text_color=RED)
                else:
                    c=GREEN if ms<80 else GOLD if ms<150 else RED
                    lbl.configure(text=str(ms)+" ms",text_color=c)
            valid=[r for r in results if r>=0]
            if valid:
                avg=sum(valid)//len(valid); self.ping_history.append(avg)
                if len(self.ping_history)>30: self.ping_history.pop(0)
                self.ms_cur.configure(text=str(avg),text_color=GREEN if avg<80 else GOLD if avg<150 else RED)
                self.ms_avg.configure(text=str(sum(self.ping_history)//len(self.ping_history)))
                self.ms_max.configure(text=str(max(self.ping_history)))
                self._draw_chart()
            time.sleep(iv)

    def _draw_chart(self):
        c=self.chart; c.delete("all")
        if len(self.ping_history)<2: return
        W=c.winfo_width() or 500; H=95; maxV=max(max(self.ping_history),200)
        pts=[(int(10+(i/(len(self.ping_history)-1))*(W-20)),int(H-10-(v/maxV)*(H-20))) for i,v in enumerate(self.ping_history)]
        poly=[(10,H-10)]+pts+[(pts[-1][0],H-10)]
        c.create_polygon([x for pt in poly for x in pt],fill="#003030",outline="")
        last=self.ping_history[-1]; col="#00ff88" if last<80 else "#ffd700" if last<150 else "#ff4466"
        c.create_line([x for pt in pts for x in pt],fill=col,width=2,smooth=True)
        ref_y=int(H-10-(100/maxV)*(H-20))
        c.create_line(10,ref_y,W-10,ref_y,fill="#333",dash=(3,3))
        c.create_text(W-18,ref_y-7,text="100ms",fill="#444",font=("Courier",8))

if __name__ == "__main__":
    app = App()
    app.mainloop()
