"""
Game Optimizer v5.0 — ЧАСТЬ 1 из 4
Импорты, утилиты, темы оформления, данные Rust и GTA V
"""
import sys, os, time, socket, random, threading, subprocess, tkinter, platform
import customtkinter as ctk
from tkinter import filedialog, messagebox

sys.setrecursionlimit(5000)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ══════════════════════════════════════════════════════════
# ТЕМЫ ОФОРМЛЕНИЯ — выбирается в настройках
# ══════════════════════════════════════════════════════════
THEMES = {
    "Красная": {
        "accent":  "#ff2244", "accent2": "#cc1133",
        "bg":      "#0a0408", "panel":   "#150a10",
        "panel2":  "#1e0f18", "border":  "#3a1428",
        "neon":    "#ff4466", "green":   "#44ff88",
        "gold":    "#ffcc44", "purple":  "#cc44ff",
        "orange":  "#ff8844", "dim":     "#664455",
        "text":    "#ffccdd", "red":     "#ff2244",
    },
    "Синяя": {
        "accent":  "#00f0ff", "accent2": "#0090ff",
        "bg":      "#05080f", "panel":   "#090f1d",
        "panel2":  "#0c1628", "border":  "#1a3050",
        "neon":    "#00f0ff", "green":   "#00ff88",
        "gold":    "#ffd700", "purple":  "#b060ff",
        "orange":  "#ff9f40", "dim":     "#3a5a7a",
        "text":    "#b8cfea", "red":     "#ff4466",
    },
    "Зелёная": {
        "accent":  "#00ff44", "accent2": "#00cc33",
        "bg":      "#030a04", "panel":   "#071008",
        "panel2":  "#0a1a0c", "border":  "#1a4020",
        "neon":    "#00ff44", "green":   "#00ff88",
        "gold":    "#ccff44", "purple":  "#44ffcc",
        "orange":  "#88ff44", "dim":     "#2a5a30",
        "text":    "#aaffbb", "red":     "#ff4466",
    },
    "Фиолетовая": {
        "accent":  "#cc44ff", "accent2": "#8822cc",
        "bg":      "#080410", "panel":   "#0f0820",
        "panel2":  "#160c2e", "border":  "#2a1450",
        "neon":    "#cc44ff", "green":   "#44ffcc",
        "gold":    "#ffcc44", "purple":  "#cc44ff",
        "orange":  "#ff6644", "dim":     "#4a2a70",
        "text":    "#ddbbff", "red":     "#ff4466",
    },
}

# Текущая тема — меняется через кнопку в приложении
_CURRENT_THEME = "Красная"
_T = THEMES[_CURRENT_THEME]

def T(key):
    """Получить цвет текущей темы"""
    return _T.get(key, "#ffffff")

def set_theme(name):
    global _CURRENT_THEME, _T
    if name in THEMES:
        _CURRENT_THEME = name
        _T = THEMES[name]

# ══════════════════════════════════════════════════════════
# ШУТКИ ПРО ВАНЮ
# ══════════════════════════════════════════════════════════
JOKES = [
    "😂 Ваня: '5 FPS — это нормально, не вижу разницы'",
    "💀 Ваня оптимизировал ПК — удалил system32",
    "🎯 Ваня поставил мониторинг — увидел FPS 12",
    "🔫 Ваня строил дом в Rust — убили через стену",
    "🚗 Ваня в GTA взял такси — лучше пешком",
    "⚡ Ваня включил высокий план питания — сгорел роутер",
    "🦕 Ваня пошёл в ARK — съел динозавр",
    "🌀 Ваня в Fortnite — убил профи-строитель",
    "📊 Ваня смотрел мониторинг — умер от температуры",
    "🏆 Ваня купил ПК за 200к — Rust выдаёт 8 FPS",
    "🎮 Ваня отключил все паразиты — случайно удалил игру",
    "😤 Ваня применил пресет Макс FPS — стало 3 FPS",
]

# ══════════════════════════════════════════════════════════
# УТИЛИТЫ
# ══════════════════════════════════════════════════════════

def run_cmd(cmd):
    """Выполнить команду, вернуть True если успешно"""
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, timeout=30,
            encoding="cp1251", errors="replace"
        )
        return r.returncode == 0
    except Exception:
        return False

def run_cmd_out(cmd):
    """Выполнить команду, вернуть вывод"""
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, timeout=15,
            encoding="cp1251", errors="replace"
        )
        return r.stdout.strip()
    except Exception:
        return ""

def expand(path):
    """Раскрыть переменные окружения в пути"""
    return os.path.expandvars(os.path.expanduser(path))

def ping_host(host, timeout=2):
    """Пинг через TCP соединение"""
    try:
        t0 = time.time()
        s = socket.create_connection((host, 80), timeout=timeout)
        s.close()
        return int((time.time() - t0) * 1000)
    except Exception:
        return -1

def launch_via_steam(steam_id):
    """
    Запустить игру ЧЕРЕЗ Steam.
    ВАЖНО: Только этот способ работает с EAC (Rust и др.)
    Прямой запуск exe — EAC блокирует и не даёт войти!
    """
    try:
        subprocess.Popen(
            ["cmd", "/c", "start", "", f"steam://rungameid/{steam_id}"],
            shell=False
        )
    except Exception as e:
        messagebox.showerror("Ошибка запуска Steam", str(e))

def launch_via_epic(app_name):
    """Запустить игру через Epic Games Launcher"""
    try:
        url = f"com.epicgames.launcher://apps/{app_name}?action=launch&silent=true"
        subprocess.Popen(["cmd", "/c", "start", "", url], shell=False)
    except Exception as e:
        messagebox.showerror("Ошибка запуска Epic", str(e))

def make_btn(parent, text, cmd,
             color=None, hover=None,
             size=12, bold=True,
             width=None, corner=8):
    """Создать кнопку — без конфликтов kwargs"""
    c = color if color else T("accent")
    h = hover if hover else T("accent2")
    kw = dict(
        text=text, command=cmd,
        fg_color=c, hover_color=h,
        font=ctk.CTkFont(size=size, weight="bold" if bold else "normal"),
        corner_radius=corner,
    )
    if width:
        kw["width"] = width
    return ctk.CTkButton(parent, **kw)

# ══════════════════════════════════════════════════════════
# ДАННЫЕ ИГРЫ: RUST
#
# БЕЗОПАСНОСТЬ EAC:
# - Запуск ТОЛЬКО через Steam (steam://rungameid/252490)
# - Паразиты — ТОЛЬКО через client.cfg (консольные команды)
# - НЕ пишем в HKCU\Software\Facepunch\Rust — EAC проверяет!
# ══════════════════════════════════════════════════════════

RUST_STEAM_ID = "252490"
RUST_CFG_PATH = r"%APPDATA%\Rust\cfg\client.cfg"

RUST_PRESETS = {
    "Макс FPS": {
        "desc":   "Минимум всего, максимум FPS",
        "fps":    "100-200+",
        "launch": "-high -maxMem=8192 -malloc=system -force-feature-level-11-0 +fps.limit 0 -nolog",
        "settings": [
            ("grass.on",             "false"),
            ("terrain.quality",      "0"),
            ("graphics.shadows",     "0"),
            ("graphics.ssao",        "0"),
            ("graphics.damage",      "0"),
            ("graphics.itemskins",   "0"),
            ("graphics.lodbias",     "0.25"),
            ("graphics.dof",         "false"),
            ("graphics.shafts",      "0"),
            ("graphics.reflections", "0"),
            ("graphics.parallax",    "0"),
        ],
    },
    "Баланс": {
        "desc":   "Хороший FPS и читаемая картинка",
        "fps":    "60-120",
        "launch": "-high -maxMem=8192 +fps.limit 0",
        "settings": [
            ("grass.on",         "true"),
            ("terrain.quality",  "50"),
            ("graphics.shadows", "1"),
            ("graphics.ssao",    "0"),
            ("graphics.lodbias", "1"),
        ],
    },
    "Качество": {
        "desc":   "Полная графика, нужен мощный ПК",
        "fps":    "40-80",
        "launch": "+fps.limit 0",
        "settings": [
            ("grass.on",         "true"),
            ("terrain.quality",  "100"),
            ("graphics.shadows", "3"),
            ("graphics.ssao",    "1"),
            ("graphics.lodbias", "2"),
        ],
    },
}

# Паразиты Rust — ТОЛЬКО client.cfg команды, без реестра!
RUST_PARASITES = [
    ("🌿", "Трава (grass.on false)",
     "Убирает траву → +20-40 FPS. Безопасно для EAC.",
     ["echo grass.on false >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo grass.on true  >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),

    ("💨", "Motion Blur",
     "Размытие при движении снижает FPS.",
     ["echo effects.motionblur false >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo effects.motionblur true  >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),

    ("🪞", "Отражения (reflections 0)",
     "Отражения на воде — дорогой эффект.",
     ["echo graphics.reflections 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.reflections 2 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),

    ("🌅", "God Rays (shafts 0)",
     "Volumetric лучи света — тяжёлый эффект.",
     ["echo graphics.shafts 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.shafts 1 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),

    ("🌊", "Глубина резкости (dof false)",
     "Размытие фона — GPU зря тратится.",
     ["echo graphics.dof false >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.dof true  >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),

    ("🎆", "Эффекты взрывов (damage 0)",
     "Партиклы взрывов — лишняя нагрузка.",
     ["echo graphics.damage 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.damage 1 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),

    ("📦", "Скины предметов (itemskins 0)",
     "Загрузка скинов жрёт RAM и VRAM.",
     ["echo graphics.itemskins 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.itemskins 1 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),

    ("🔵", "SSAO (ssao 0)",
     "Ambient occlusion — тени в углах, дорого.",
     ["echo graphics.ssao 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.ssao 1 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),

    ("🔊", "VOIP (voice.use false)",
     "Голосовой чат постоянно слушает микрофон.",
     ["echo voice.use false >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo voice.use true  >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),

    ("🌱", "LOD Bias (lodbias 0.25)",
     "Дистанция детализации объектов.",
     ["echo graphics.lodbias 0.25 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.lodbias 2    >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),

    ("🌫", "Terrain Quality (0)",
     "Качество рельефа — огромная нагрузка.",
     ["echo terrain.quality 0   >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo terrain.quality 100 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),

    ("☀️", "Parallax (parallax 0)",
     "Параллакс-эффект на поверхностях.",
     ["echo graphics.parallax 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.parallax 1 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
]

# Команды записываемые в client.cfg при "убить всё"
RUST_KILL_CFG = (
    "// Game Optimizer v5.0 — Maximum Performance\n"
    "grass.on false\n"
    "grass.shadowcast false\n"
    "effects.motionblur false\n"
    "graphics.damage 0\n"
    "graphics.dof false\n"
    "graphics.shafts 0\n"
    "graphics.shadows 0\n"
    "graphics.ssao 0\n"
    "graphics.lodbias 0.25\n"
    "graphics.itemskins 0\n"
    "graphics.reflections 0\n"
    "graphics.parallax 0\n"
    "voice.use false\n"
    "fps.limit 0\n"
    "terrain.quality 0\n"
)

RUST_TIPS = [
    ("💡", "Steam оверлей",
     "Steam → ПКМ на Rust → Свойства → убери 'Включить Steam Overlay'. +5-10 FPS на слабых ПК."),
    ("🛡", "Исключения антивируса",
     "Windows Defender → Защита → Исключения → папка с Rust. EAC и игра грузятся быстрее."),
    ("🎮", "DirectX 11",
     "Параметры запуска: -force-feature-level-11-0. Стабильнее DX12 на большинстве видеокарт."),
    ("🧹", "Кэш шейдеров",
     "Удали: %LocalAppData%\\Temp\\Rust — первый запуск медленнее, потом FPS стабильнее."),
    ("⚙", "F1 консоль в игре",
     "В Rust нажми F1 и вставь команды из пресета напрямую. Работают без перезапуска."),
    ("📡", "Выбор сервера",
     "Играй на серверах с пингом < 80ms. В Rust нет официальных регионов — выбирай вручную."),
    ("⚠", "EAC безопасность",
     "Запуск ТОЛЬКО через Steam! Прямой запуск exe — EAC блокирует вход в игру."),
    ("🔧", "client.cfg",
     "Путь: %AppData%\\Rust\\cfg\\client.cfg — стандартные консольные настройки. Редактировать безопасно."),
    ("🖥", "Разрешение",
     "Попробуй 1600×900 — в Rust это даёт +15-25% FPS почти без потери качества."),
]

# ══════════════════════════════════════════════════════════
# ДАННЫЕ ИГРЫ: GTA V
# ══════════════════════════════════════════════════════════

GTAV_STEAM_ID = "271590"

GTAV_PRESETS = {
    "Макс FPS": {
        "desc":   "Для слабых ПК и FiveM серверов",
        "fps":    "80-160+",
        "launch": "-notablet -norestrictions -noFirstRun -IgnoreCorrupts",
        "settings": [
            ("TextureQuality",       "normal"),
            ("ShaderQuality",        "normal"),
            ("ShadowQuality",        "normal"),
            ("ReflectionQuality",    "off"),
            ("ReflectionMSAA",       "off"),
            ("MSAA",                 "off"),
            ("FXAA",                 "off"),
            ("AmbientOcclusion",     "off"),
            ("TessellationQuality",  "off"),
            ("ShadowSoftShadows",    "sharp"),
            ("PostFX",               "normal"),
            ("InGameDepthOfField",   "false"),
            ("MotionBlur",           "false"),
        ],
    },
    "Баланс": {
        "desc":   "Комфортная игра на среднем ПК",
        "fps":    "60-100",
        "launch": "-notablet -noFirstRun",
        "settings": [
            ("TextureQuality",    "high"),
            ("ShaderQuality",     "high"),
            ("ShadowQuality",     "high"),
            ("MSAA",              "off"),
            ("FXAA",              "on"),
            ("AmbientOcclusion",  "medium"),
            ("PostFX",            "high"),
            ("MotionBlur",        "false"),
        ],
    },
    "Качество": {
        "desc":   "Максимальная красота, мощный ПК",
        "fps":    "40-70",
        "launch": "-notablet",
        "settings": [
            ("TextureQuality",       "very high"),
            ("ShaderQuality",        "very high"),
            ("ShadowQuality",        "very high"),
            ("MSAA",                 "x4"),
            ("FXAA",                 "on"),
            ("AmbientOcclusion",     "high"),
            ("TessellationQuality",  "very high"),
            ("PostFX",               "ultra"),
        ],
    },
}

GTAV_PARASITES = [
    ("🎓", "Обучающие подсказки",
     "Всплывают каждый раз при входе в игру.",
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v TutorialDone /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v TutorialDone /t REG_DWORD /d 0 /f"]),

    ("🎬", "Вступительные ролики",
     "Логотип Rockstar + ролик при каждом запуске.",
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v InstallComplete /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v InstallComplete /t REG_DWORD /d 0 /f"]),

    ("🌀", "Motion Blur",
     "Размытие при движении — -10-15 FPS без пользы.",
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v MotionBlur /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v MotionBlur /t REG_DWORD /d 1 /f"]),

    ("🌊", "Глубина резкости DOF",
     "Размытие фона — GPU расходуется зря.",
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v InGameDepthOfField /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v InGameDepthOfField /t REG_DWORD /d 1 /f"]),

    ("🎥", "Replay / Rockstar Editor",
     "Постоянно пишет буфер повтора на диск в фоне.",
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ReplayBuffer /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ReplayBuffer /t REG_DWORD /d 1 /f"]),

    ("🐾", "Tessellation поверхностей",
     "Детализация травы и земли — очень дорого.",
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v Tessellation /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v Tessellation /t REG_DWORD /d 1 /f"]),

    ("🌆", "Extended Distance Scaling",
     "Далёкие объекты высокого качества — огромная нагрузка.",
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ExtendedDistanceScaling /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ExtendedDistanceScaling /t REG_DWORD /d 1 /f"]),

    ("🚶", "Плотность NPC и трафика",
     "Много NPC и машин сильно нагружают CPU.",
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v PedDensity /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v PedDensity /t REG_DWORD /d 100 /f"]),

    ("🌧", "Particle Effects / Дождь",
     "Дождь, снег, дым — дорогие частицы.",
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ParticleQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ParticleQuality /t REG_DWORD /d 2 /f"]),

    ("🔆", "PostFX эффекты",
     "Bloom, хроматическая аберрация — лишняя нагрузка.",
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v PostFX /t REG_SZ /d \"normal\" /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v PostFX /t REG_SZ /d \"high\" /f"]),
]

GTAV_TIPS = [
    ("🟣", "FiveM — отключи все оверлеи",
     "Перед FiveM отключи Discord, Steam, NVIDIA ShadowPlay. FiveM сам по себе тяжёлый."),
    ("⚡", "Параметр -notablet",
     "Обязательный параметр запуска — убирает ненужный ввод планшета. Экономит ресурсы."),
    ("🌐", "NAT Type Open",
     "Для стабильного GTA Online пробрось порты: 6672 UDP, 61455-61458 UDP."),
    ("🔧", "Rockstar Launcher автозагрузка",
     "Win+R → msconfig → Автозагрузка → снять галочку Rockstar Launcher."),
    ("🗑", "Кэш FiveM",
     "%LOCALAPPDATA%\\FiveM\\FiveM.app\\cache — удаляй при лагах и вылетах."),
    ("📁", "Graphics config",
     "Documents\\Rockstar Games\\GTA V\\settings.xml — можно редактировать вручную."),
    ("💾", "VRAM индикатор",
     "В настройках GTA V есть индикатор VRAM. Следи чтобы не превышало 90%."),
    ("🖥", "Расширенный масштаб",
     "Extended Distance Scaling = главный убийца FPS в GTA V. Ставь на 0."),
]
