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


# ══════════════════════════════════════════════════════════
# ДАННЫЕ ИГРЫ: CS2
# ══════════════════════════════════════════════════════════

CS2_STEAM_ID = "730"
CS2_CFG_PATH = r"%USERPROFILE%\AppData\Local\cs2\cfg\autoexec.cfg"

CS2_PRESETS = {
    "Макс FPS": {
        "desc":   "Про-настройки для максимального FPS",
        "fps":    "200-400+",
        "launch": "-novid -nojoy -noaafonts -limitvsconst -forcenovsync +mat_queue_mode -1 +r_dynamic_lighting 0 -freq 240 -high",
        "settings": [
            ("r_lowlatency",              "2"),
            ("fps_max",                   "0"),
            ("mat_queue_mode",            "-1"),
            ("r_dynamic_lighting",        "0"),
            ("r_shadows",                 "0"),
            ("cl_ragdoll_physics_enable", "0"),
            ("r_motionblur",              "0"),
            ("cl_showfps",                "1"),
            ("rate",                      "786432"),
            ("cl_interp",                 "0"),
            ("cl_interp_ratio",           "1"),
            ("m_rawinput",                "1"),
            ("cl_draw_only_deathnotices", "1"),
            ("snd_menumusic_volume",      "0"),
        ],
    },
    "Баланс": {
        "desc":   "Хороший FPS и хорошая видимость врагов",
        "fps":    "144-250",
        "launch": "-novid -nojoy -forcenovsync +mat_queue_mode -1 -high",
        "settings": [
            ("fps_max",        "0"),
            ("r_lowlatency",   "2"),
            ("r_shadows",      "1"),
            ("r_dynamic_lighting", "1"),
            ("cl_showfps",     "1"),
            ("r_motionblur",   "0"),
            ("rate",           "786432"),
            ("m_rawinput",     "1"),
        ],
    },
    "Качество": {
        "desc":   "Красивая картинка для мощного ПК",
        "fps":    "100-180",
        "launch": "-novid +mat_queue_mode -1",
        "settings": [
            ("fps_max",            "0"),
            ("r_shadows",          "3"),
            ("r_dynamic_lighting", "1"),
            ("r_motionblur",       "0"),
            ("m_rawinput",         "1"),
        ],
    },
}

# Полный autoexec.cfg с подробными комментариями
CS2_AUTOEXEC_CONTENT = """\
// ═══════════════════════════════════════════════════════
// CS2 autoexec.cfg — Game Optimizer v5.0
// Вставь в: %USERPROFILE%\\AppData\\Local\\cs2\\cfg\\
// Добавь в параметры запуска: +exec autoexec
// ═══════════════════════════════════════════════════════

// ── FPS и производительность ──────────────────────────
fps_max 0                          // Без ограничения FPS
r_lowlatency 2                     // Минимальная задержка рендера
mat_queue_mode -1                  // Многопоточный рендер
r_dynamic_lighting 0               // Откл. динамическое освещение
r_shadows 0                        // Откл. тени (включи если хочешь видеть)

// ── Сетевые настройки ─────────────────────────────────
rate 786432                        // Максимальный rate (нет ограничений в CS2)
cl_interp 0                        // Минимальная интерполяция
cl_interp_ratio 1                  // Соотношение интерполяции
cl_updaterate 128                  // Обновлений от сервера в секунду
cl_cmdrate 128                     // Команд в секунду

// ── Графика ───────────────────────────────────────────
r_motionblur 0                     // Откл. motion blur (убирает FPS зря)
cl_ragdoll_physics_enable 0        // Откл. физику трупов (жрёт CPU)
cl_detailfade 0                    // Откл. детали окружения (трава)
cl_detail_avoid_radius 0           // Убрать разлетание мусора
cl_detail_avoid_force 0            // Убрать разлетание мусора

// ── Звук ──────────────────────────────────────────────
snd_menumusic_volume 0             // Тишина в главном меню
snd_deathcamera_volume 0.4         // Звук камеры смерти

// ── Мышь ──────────────────────────────────────────────
m_rawinput 1                       // Прямой ввод без обработки Windows
sensitivity 2.0                    // Чувствительность (настрой под себя)
zoom_sensitivity_ratio_mouse 0.818 // Чувствительность при прицеливании

// ── HUD и интерфейс ───────────────────────────────────
cl_showfps 1                       // Показать FPS в углу
cl_draw_only_deathnotices 1        // Только важная информация в HUD
hud_scaling 0.85                   // Уменьшить размер HUD
net_graphproportionalfont 0        // Маленький net_graph

// ── Прицел ────────────────────────────────────────────
cl_crosshairsize 2                 // Размер прицела
cl_crosshairgap -2                 // Зазор прицела
cl_crosshairthickness 1            // Толщина прицела
cl_crosshaircolor 1                // 1=зелёный 2=жёлтый 4=синий 5=кастомный
cl_crosshairdot 0                  // Убрать центральную точку
cl_crosshair_drawoutline 0         // Контур прицела

// ── ViewModel (положение оружия) ──────────────────────
viewmodel_presetpos 3              // Положение оружия (3 = далеко, меньше мусора)
viewmodel_fov 68                   // Угол обзора оружия

// ── Bind-ы ────────────────────────────────────────────
// bind "F5" "screenshot"          // Скриншот по F5
// bind "mwheelup" "+jump"         // Прыжок на колёсико вверх
// bind "mwheeldown" "+jump"       // Прыжок на колёсико вниз
"""

CS2_KILL_CFG = (
    "r_motionblur 0\n"
    "cl_ragdoll_physics_enable 0\n"
    "cl_detailfade 0\n"
    "snd_menumusic_volume 0\n"
    "cl_draw_only_deathnotices 1\n"
    "fps_max 0\n"
    "r_lowlatency 2\n"
    "cl_interp 0\n"
    "cl_interp_ratio 1\n"
    "rate 786432\n"
    "m_rawinput 1\n"
    "r_dynamic_lighting 0\n"
    "r_shadows 0\n"
)

CS2_PARASITES = [
    ("🎓", "Обучение / Tutorial",
     "Убирает предложение зайти в обучалку при каждом запуске.",
     ["reg add \"HKCU\\Software\\Valve\\Counter-Strike Global Offensive\" /v TutorialDone /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Valve\\Counter-Strike Global Offensive\" /v TutorialDone /t REG_DWORD /d 0 /f"]),

    ("🎬", "Интро видео Valve",
     "Логотип Valve при каждом запуске — 3-5 секунд зря.",
     ["reg add \"HKCU\\Software\\Valve\\Counter-Strike Global Offensive\" /v NoVideoIntro /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Valve\\Counter-Strike Global Offensive\" /v NoVideoIntro /t REG_DWORD /d 0 /f"]),

    ("🌀", "Motion Blur (r_motionblur 0)",
     "Размытие при движении снижает FPS и мешает целиться.",
     ["echo r_motionblur 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo r_motionblur 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),

    ("💀", "Ragdoll физика трупов",
     "Физика трупов жрёт CPU — никакой пользы в игре.",
     ["echo cl_ragdoll_physics_enable 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo cl_ragdoll_physics_enable 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),

    ("🌿", "Детали окружения (трава/листья)",
     "Декоративные детали вокруг — ненужная нагрузка на GPU.",
     ["echo cl_detailfade 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo cl_detailfade 400 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),

    ("🎵", "Музыка в главном меню",
     "Звуковой движок работает даже в меню — зря расходует ресурсы.",
     ["echo snd_menumusic_volume 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo snd_menumusic_volume 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),

    ("💬", "Kill feed анимации",
     "cl_draw_only_deathnotices 1 — только важное на экране.",
     ["echo cl_draw_only_deathnotices 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo cl_draw_only_deathnotices 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),

    ("🔫", "Анимация осмотра оружия",
     "viewmodel_presetpos 3 — оружие дальше, лучше видимость карты.",
     ["echo viewmodel_presetpos 3 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo viewmodel_presetpos 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),

    ("👁", "Lens Flare / Блики линзы",
     "Декоративный эффект бликов — GPU работает зря.",
     ["echo r_eyegloss 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\"",
      "echo r_eyemove 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo r_eyegloss 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),

    ("🌊", "Динамическое освещение",
     "r_dynamic_lighting 0 — источники света не обновляются динамически.",
     ["echo r_dynamic_lighting 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo r_dynamic_lighting 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),

    ("🌑", "Тени (r_shadows 0)",
     "Отключение теней даёт +20-40 FPS. Враги всё равно видны.",
     ["echo r_shadows 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo r_shadows 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),

    ("📶", "Сетевой граф (net_graph)",
     "Показывает пинг и потери пакетов в реальном времени.",
     ["echo net_graphproportionalfont 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\"",
      "echo cl_showfps 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo cl_showfps 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),
]

CS2_TIPS = [
    ("🖥", "Частота монитора",
     "NVIDIA: Панель управления → Разрешение дисплея → выбери 144/240Hz. AMD: Software → Display."),
    ("🖱", "Raw Input мышь",
     "m_rawinput 1 — прямой ввод без обработки Windows. Убирает акселерацию мыши."),
    ("📡", "Rate команды",
     "rate 786432; cl_interp 0; cl_interp_ratio 1 — добавь в autoexec.cfg."),
    ("🌡", "Температура CPU",
     "CS2 очень нагружает процессор. Больше 90°C = нужна чистка кулера и замена термопасты."),
    ("🎮", "Game DVR отключить",
     "Win+G → Настройки → Выключи запись и трансляцию. Даёт +5-10 FPS."),
    ("⚙", "autoexec.cfg путь",
     "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\ — создай файл и добавь +exec autoexec в параметры запуска."),
    ("🎯", "Practice конфиг",
     "sv_cheats 1; sv_infinite_ammo 1; bot_stop 1; mp_roundtime 60 — для тренировки аима."),
    ("🔊", "Звук врагов",
     "snd_headphone_pan_exponent 2 — лучше слышно откуда стреляют. Добавь в autoexec."),
    ("📊", "FPS счётчик",
     "cl_showfps 1 в autoexec или параметр запуска -dev показывает подробную статистику."),
]

# ══════════════════════════════════════════════════════════
# ДАННЫЕ ИГРЫ: FORTNITE
# ══════════════════════════════════════════════════════════

FN_EPIC_ID   = "Fortnite"
FN_INI_PATH  = r"%LOCALAPPDATA%\FortniteGame\Saved\Config\WindowsClient\GameUserSettings.ini"

FN_PRESETS = {
    "Макс FPS": {
        "desc":   "Минимум графики, максимум FPS",
        "fps":    "144-300+",
        "launch": "-NOTEXTURESTREAMING -USEALLAVAILABLECORES -nomansky -novsync -dx12",
        "settings": [
            ("sg.ResolutionQuality",  "75"),
            ("sg.ViewDistanceQuality","1"),
            ("sg.ShadowQuality",      "0"),
            ("sg.PostProcessQuality", "0"),
            ("sg.TextureQuality",     "0"),
            ("sg.EffectsQuality",     "0"),
            ("sg.FoliageQuality",     "0"),
            ("bUseVSync",             "False"),
            ("FrameRateLimit",        "0"),
            ("bShowFPS",              "True"),
        ],
    },
    "Баланс": {
        "desc":   "Хороший FPS и красивая картинка",
        "fps":    "90-144",
        "launch": "-USEALLAVAILABLECORES -nomansky -novsync",
        "settings": [
            ("sg.ResolutionQuality",  "100"),
            ("sg.ViewDistanceQuality","2"),
            ("sg.ShadowQuality",      "2"),
            ("sg.PostProcessQuality", "2"),
            ("sg.TextureQuality",     "2"),
            ("bUseVSync",             "False"),
            ("FrameRateLimit",        "144"),
        ],
    },
    "Качество": {
        "desc":   "Красивая картинка для мощного ПК",
        "fps":    "60-90",
        "launch": "-USEALLAVAILABLECORES -novsync",
        "settings": [
            ("sg.ResolutionQuality",  "100"),
            ("sg.ViewDistanceQuality","4"),
            ("sg.ShadowQuality",      "4"),
            ("sg.PostProcessQuality", "4"),
            ("sg.TextureQuality",     "4"),
            ("bUseVSync",             "False"),
            ("FrameRateLimit",        "0"),
        ],
    },
}

# INI файл для максимального FPS — записывается напрямую
FN_KILL_INI = (
    "[ScalabilityGroups]\n"
    "sg.ResolutionQuality=75\n"
    "sg.ViewDistanceQuality=1\n"
    "sg.ShadowQuality=0\n"
    "sg.PostProcessQuality=0\n"
    "sg.TextureQuality=0\n"
    "sg.EffectsQuality=0\n"
    "sg.FoliageQuality=0\n"
    "\n"
    "[/Script/FortniteGame.FortGameUserSettings]\n"
    "bUseVSync=False\n"
    "FrameRateLimit=0.000000\n"
    "bShowFPS=True\n"
    "ResolutionSizeX=1920\n"
    "ResolutionSizeY=1080\n"
    "LastUserConfirmedResolutionSizeX=1920\n"
    "LastUserConfirmedResolutionSizeY=1080\n"
    "WindowPosX=-1\n"
    "WindowPosY=-1\n"
    "FullscreenMode=1\n"
    "LastConfirmedFullscreenMode=1\n"
    "PreferredFullscreenMode=1\n"
    "Version=5\n"
    "AudioQualityLevel=0\n"
    "LastConfirmedAudioQualityLevel=0\n"
    "FrameRateLimitWhenBackgrounded=30.000000\n"
    "MinDesiredFrameRate=60.000000\n"
)

FN_PARASITES = [
    ("🎓", "Обучение / Tutorial",
     "Убирает обучалку при входе в Battle Royale.",
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v TutorialCompleted /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v TutorialCompleted /t REG_DWORD /d 0 /f"]),

    ("🎬", "Интро видео Epic Games",
     "Логотипы Epic и Unreal при каждом запуске — убираем.",
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v SkipIntro /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v SkipIntro /t REG_DWORD /d 0 /f"]),

    ("🌀", "Motion Blur",
     "Размытие при движении — снижает FPS и мешает целиться.",
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v MotionBlur /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v MotionBlur /t REG_DWORD /d 1 /f"]),

    ("🌿", "Foliage / Листва и трава",
     "Трава и кусты — лишняя нагрузка, не влияет на геймплей.",
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v FoliageQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v FoliageQuality /t REG_DWORD /d 4 /f"]),

    ("🌊", "Глубина резкости DOF",
     "Размытие фона — GPU расходуется зря.",
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v DepthOfField /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v DepthOfField /t REG_DWORD /d 1 /f"]),

    ("🎵", "Музыка в лобби",
     "Фоновая музыка нагружает CPU и аудиодрайвер.",
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v LobbyMusicVolume /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v LobbyMusicVolume /t REG_DWORD /d 100 /f"]),

    ("📡", "Replays / Повторы матчей",
     "Постоянно пишет replay файлы на диск — грузит I/O.",
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v bShouldRecord /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v bShouldRecord /t REG_DWORD /d 1 /f"]),

    ("💥", "Nanite / Lumen материалы",
     "Nanite и Lumen — очень тяжёлые современные эффекты рендеринга.",
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v MaterialQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v MaterialQuality /t REG_DWORD /d 4 /f"]),

    ("🌟", "Ambient Occlusion / SSAO",
     "Тени в углах — красиво, но тяжело для GPU.",
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v AmbientOcclusion /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v AmbientOcclusion /t REG_DWORD /d 1 /f"]),

    ("☁️", "Volumetric облака",
     "Объёмные облака — очень тяжёлый эффект на слабых ПК.",
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v VolumetricClouds /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v VolumetricClouds /t REG_DWORD /d 1 /f"]),

    ("🎆", "Particle Effects / Взрывы",
     "Сложные эффекты частиц при взрывах и выстрелах.",
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v EffectsQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v EffectsQuality /t REG_DWORD /d 4 /f"]),

    ("🔆", "Post Processing эффекты",
     "Bloom, хроматическая аберрация, виньетка — лишнее.",
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v PostProcessQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v PostProcessQuality /t REG_DWORD /d 4 /f"]),
]

FN_TIPS = [
    ("📁", "Путь к настройкам",
     "%LOCALAPPDATA%\\FortniteGame\\Saved\\Config\\WindowsClient\\ — тут лежит GameUserSettings.ini."),
    ("⚡", "Параметры запуска Epic",
     "Epic Launcher → три точки у Fortnite → Параметры → Дополнительные аргументы командной строки."),
    ("🛡", "Исключения Windows Defender",
     "Defender → Защита → Исключения → папка Fortnite. Ускоряет загрузку шейдеров."),
    ("🎮", "DirectX 12 vs DX11",
     "На RTX картах DX12 быстрее. На GTX и AMD — попробуй оба варианта и выбери лучший."),
    ("🔄", "Очистка кэша шейдеров",
     "%LOCALAPPDATA%\\FortniteGame\\Saved\\Cache — удаляй при фризах. Кэш пересоздастся сам."),
    ("⚙", "Performance Mode",
     "В настройках Fortnite есть 'Performance Mode (Alpha)' — упрощённый рендер, +30-50% FPS."),
    ("🎯", "Настройки для конструирования",
     "Для конструктора важна отзывчивость: FrameRateLimit=0 и максимальная чувствительность прицела."),
    ("🖥", "Разрешение 75%",
     "sg.ResolutionQuality=75 даёт +20-30% FPS при минимальной потере визуального качества."),
    ("🔧", "Fortnite и EAC",
     "Fortnite тоже использует Easy Anti-Cheat. Запуск только через Epic Games Launcher!"),
]

# ══════════════════════════════════════════════════════════
# ДАННЫЕ ИГРЫ: ARK
# ══════════════════════════════════════════════════════════

# ARK Survival Evolved = Steam ID 346110
# ARK Survival Ascended = Steam ID 2399830
ARK_STEAM_ID  = "346110"
ARK_ASA_STEAM_ID = "2399830"  # Ascended версия

ARK_PRESETS = {
    "Макс FPS": {
        "desc":   "Минимум графики, максимум FPS",
        "fps":    "60-120+",
        "launch": "-USEALLAVAILABLECORES -sm4 -d3d10 -nomansky -lowmemory -novsync",
        "settings": [
            ("sg.ResolutionQuality", "75"),
            ("sg.ShadowQuality",     "0"),
            ("sg.TextureQuality",    "0"),
            ("sg.EffectsQuality",    "0"),
            ("sg.FoliageQuality",    "0"),
            ("bUseVSync",            "False"),
            ("FrameRateLimit",       "0"),
        ],
    },
    "Баланс": {
        "desc":   "Хороший FPS и читаемая картинка",
        "fps":    "40-80",
        "launch": "-USEALLAVAILABLECORES -nomansky -novsync",
        "settings": [
            ("sg.ResolutionQuality", "100"),
            ("sg.ShadowQuality",     "2"),
            ("sg.TextureQuality",    "2"),
            ("sg.EffectsQuality",    "2"),
            ("sg.FoliageQuality",    "2"),
            ("bUseVSync",            "False"),
        ],
    },
    "Качество": {
        "desc":   "Красивая картинка, нужен мощный ПК",
        "fps":    "25-50",
        "launch": "-USEALLAVAILABLECORES",
        "settings": [
            ("sg.ResolutionQuality", "100"),
            ("sg.ShadowQuality",     "4"),
            ("sg.TextureQuality",    "4"),
            ("sg.EffectsQuality",    "4"),
            ("sg.FoliageQuality",    "4"),
            ("bUseVSync",            "False"),
        ],
    },
}

ARK_PARASITES = [
    ("🎓", "Обучение / подсказки Tutorial",
     "Постоянные подсказки для новичка при каждом входе.",
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v TutorialDone /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v TutorialDone /t REG_DWORD /d 0 /f"]),

    ("🎬", "Интро видео Studio Wildcard",
     "Логотипы разработчиков при каждом запуске.",
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v SkipIntro /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v SkipIntro /t REG_DWORD /d 0 /f"]),

    ("🌿", "Foliage / Листва и деревья",
     "Деревья и кусты — ГЛАВНЫЙ убийца FPS в ARK. Ставь на минимум!",
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v FoliageQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v FoliageQuality /t REG_DWORD /d 100 /f"]),

    ("🦕", "Анимации динозавров NPC",
     "Сложные анимации всех динозавров нагружают CPU.",
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v NPCQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v NPCQuality /t REG_DWORD /d 2 /f"]),

    ("🌊", "Глубина резкости DOF",
     "Размытие фона — GPU работает зря.",
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v DepthOfField /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v DepthOfField /t REG_DWORD /d 1 /f"]),

    ("🌀", "Motion Blur",
     "Размытие при движении — обязательно отключить.",
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v MotionBlur /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v MotionBlur /t REG_DWORD /d 1 /f"]),

    ("☁️", "Volumetric Clouds",
     "Объёмные облака — очень тяжёлый эффект для GPU.",
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v VolumetricClouds /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v VolumetricClouds /t REG_DWORD /d 1 /f"]),

    ("💧", "Water Quality / Вода",
     "Отражения и качество воды — красиво но дорого.",
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v WaterQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v WaterQuality /t REG_DWORD /d 2 /f"]),

    ("🌅", "Sky / Небо",
     "Качество атмосферы и неба.",
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v SkyQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v SkyQuality /t REG_DWORD /d 2 /f"]),

    ("💥", "Particle Effects",
     "Эффекты частиц при атаках и взрывах.",
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v ParticleQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v ParticleQuality /t REG_DWORD /d 2 /f"]),

    ("🌑", "Shadows / Тени",
     "Тени в ARK очень тяжёлые — ставь на минимум.",
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v ShadowQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v ShadowQuality /t REG_DWORD /d 2 /f"]),

    ("🌡", "Ground Clutter / Мусор на земле",
     "Камни, листья, мусор на земле — мелочь, но грузит.",
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v GroundClutter /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v GroundClutter /t REG_DWORD /d 1 /f"]),
]

ARK_TIPS = [
    ("💾", "RAM — самое главное в ARK",
     "ARK требует минимум 16GB RAM. Закрой всё перед игрой — браузер, Discord и т.д."),
    ("⚡", "Параметры запуска",
     "-USEALLAVAILABLECORES -sm4 -d3d10 -nomansky -lowmemory -novsync"),
    ("🌿", "Листва = главный враг FPS",
     "Листва в ARK — ставь на абсолютный минимум. Разница огромная — от 20 до 80 FPS."),
    ("🧹", "Кэш шейдеров ARK",
     "Папка: ARK\\ShooterGame\\Saved\\Cache — удаляй при фризах. Первый вход будет дольше."),
    ("🦕", "Дистанция прорисовки динозавров",
     "В настройках сервера снижай View Distance для динозавров — главный CPU-убийца в трибах."),
    ("🖥", "Разрешение 900p",
     "1600×900 вместо 1920×1080 — даёт +25-35% FPS почти без потери качества."),
    ("🔧", "Ini файлы ARK",
     "Documents\\My Games\\ARK\\Saved\\Config\\WindowsNoEditor\\ — GameUserSettings.ini."),
    ("🏠", "Стены базы и FPS",
     "Много стен и структур в видимой зоне убивает FPS. Строй эффективно, не нагромождай."),
    ("📊", "ARK Performance Mode",
     "В настройках графики ARK есть Low Quality Mode — включи для максимального FPS."),
]

# ══════════════════════════════════════════════════════════
# ОБЩИЕ ДАННЫЕ — одинаковые для всех игр
# ══════════════════════════════════════════════════════════

# Оверлеи — жрут FPS у всех игр
OVERLAYS = [
    ("🎮", "Xbox Game Bar / Game DVR",
     "Сжирает 5-15% CPU, записывает видео, вызывает фризы.",
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f",
      "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR\" /v AllowGameDVR /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 1 /f"]),

    ("📸", "NVIDIA ShadowPlay / GeForce Overlay",
     "Записывает видео в фоне постоянно — нагружает GPU на 5-10%.",
     ["reg add \"HKCU\\Software\\NVIDIA Corporation\\NVCapture\" /v CaptureEnabled /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\NVIDIA Corporation\\NVCapture\" /v CaptureEnabled /t REG_DWORD /d 1 /f"]),

    ("💬", "Discord оверлей в игре",
     "Накладывает оверлей на игру — +3-8ms задержки на каждый кадр.",
     ["reg add \"HKCU\\Software\\Discord\" /v Overlay /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Discord\" /v Overlay /t REG_DWORD /d 1 /f"]),

    ("🎵", "Steam оверлей (Shift+Tab)",
     "Shift+Tab лагает в игре, оверлей постоянно занимает RAM.",
     ["reg add \"HKCU\\Software\\Valve\\Steam\" /v SteamOverlayEnabled /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Valve\\Steam\" /v SteamOverlayEnabled /t REG_DWORD /d 1 /f"]),

    ("📹", "AMD ReLive / Radeon Overlay",
     "Аналог ShadowPlay для AMD видеокарт — пишет видео в фоне.",
     ["reg add \"HKCU\\Software\\AMD\\CN\" /v DVREnabled /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\AMD\\CN\" /v DVREnabled /t REG_DWORD /d 1 /f"]),
]

# Фоновые процессы Windows
BG_PROCS = [
    ("🔄", "Windows Update (автообновления)",
     "Качает обновления прямо во время игры — занимает сеть и диск.",
     ["net stop wuauserv", "net stop bits", "net stop dosvc"],
     ["net start wuauserv"]),

    ("🔍", "Windows Search / Indexer",
     "Индексирует файлы на диске — грузит HDD/SSD во время игры.",
     ["net stop wsearch", "sc config wsearch start=disabled"],
     ["net start wsearch", "sc config wsearch start=auto"]),

    ("📊", "SysMain / Superfetch",
     "Предзагружает программы в RAM — мешает играм занять всю память.",
     ["net stop sysmain", "sc config sysmain start=disabled"],
     ["net start sysmain", "sc config sysmain start=auto"]),

    ("☁️", "OneDrive синхронизация",
     "Синхронизирует файлы — грузит диск и интернет во время игры.",
     ["taskkill /f /im OneDrive.exe", "sc config OneSyncSvc start=disabled"],
     ["sc config OneSyncSvc start=auto"]),

    ("🔒", "Windows Defender (реальное время)",
     "Сканирует файлы игры в реальном времени — нагружает CPU.",
     ["sc config WdNisSvc start=disabled"],
     ["sc config WdNisSvc start=auto"]),

    ("🖨", "Print Spooler (если нет принтера)",
     "Фоновый сервис принтера — зачем он если принтера нет?",
     ["net stop spooler", "sc config spooler start=disabled"],
     ["net start spooler", "sc config spooler start=auto"]),
]

# ══════════════════════════════════════════════════════════
# ОПТИМИЗАЦИИ WINDOWS
# ══════════════════════════════════════════════════════════
WIN_OPTS = [
    ("⚡", "Высокий план электропитания",
     "Максимальная производительность CPU — не ограничивает частоты процессора.",
     ["powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"],
     ["powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e"]),

    ("📈", "Приоритет игровых процессов Win32=38",
     "Windows даёт играм больший приоритет над фоновыми задачами.",
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v Win32PrioritySeparation /t REG_DWORD /d 2 /f"]),

    ("🎮", "Hardware Accelerated GPU Scheduling",
     "HAGS снижает задержку GPU. Нужна Windows 10 2004+ и NVIDIA 10xx+ или AMD Vega+.",
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v HwSchMode /t REG_DWORD /d 2 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v HwSchMode /t REG_DWORD /d 1 /f"]),

    ("🖥", "Отключить визуальные эффекты Windows",
     "Анимации, тени в проводнике, плавные шрифты — тратят CPU зря.",
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects\" /v VisualFXSetting /t REG_DWORD /d 2 /f"],
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects\" /v VisualFXSetting /t REG_DWORD /d 0 /f"]),

    ("🔕", "Отключить Xbox Game Bar / DVR",
     "Один из главных воров производительности. -5-15% CPU в играх.",
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f",
      "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR\" /v AllowGameDVR /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 1 /f"]),

    ("🔍", "Отключить Windows Search",
     "Перестаёт индексировать файлы во время игры — меньше нагрузка на диск.",
     ["net stop wsearch", "sc config wsearch start=disabled"],
     ["net start wsearch", "sc config wsearch start=auto"]),

    ("📊", "Отключить SysMain / Superfetch",
     "Освобождает RAM для игры — не пытается предзагружать программы.",
     ["net stop sysmain", "sc config sysmain start=disabled"],
     ["net start sysmain", "sc config sysmain start=auto"]),

    ("🧹", "Очистить RAM перед игрой",
     "ProcessIdleTasks — принудительно освобождает кэш оперативной памяти.",
     ["rundll32.exe advapi32.dll,ProcessIdleTasks"],
     []),

    ("⏸", "Пауза Windows Update",
     "Остановить скачивание обновлений на время игровой сессии.",
     ["net stop wuauserv", "net stop bits", "net stop dosvc"],
     ["net start wuauserv"]),

    ("💾", "Отключить очистку PageFile при выключении",
     "Windows не будет очищать файл подкачки при выключении — быстрее.",
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v ClearPageFileAtShutdown /t REG_DWORD /d 0 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v ClearPageFileAtShutdown /t REG_DWORD /d 1 /f"]),

    ("🚀", "Отключить Nagle в Windows сети",
     "TcpAckFrequency — базовая сетевая оптимизация для игр.",
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpAckFrequency /t REG_DWORD /d 1 /f",
      "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TCPNoDelay /t REG_DWORD /d 1 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpAckFrequency /t REG_DWORD /d 2 /f"]),

    ("🖱", "Отключить мышиный акселератор",
     "Убирает аппаратное ускорение курсора — важно для игр с мышью.",
     ["reg add \"HKCU\\Control Panel\\Mouse\" /v MouseSpeed /t REG_SZ /d 0 /f",
      "reg add \"HKCU\\Control Panel\\Mouse\" /v MouseThreshold1 /t REG_SZ /d 0 /f",
      "reg add \"HKCU\\Control Panel\\Mouse\" /v MouseThreshold2 /t REG_SZ /d 0 /f"],
     ["reg add \"HKCU\\Control Panel\\Mouse\" /v MouseSpeed /t REG_SZ /d 1 /f"]),
]

# ══════════════════════════════════════════════════════════
# СЕТЕВЫЕ ОПТИМИЗАЦИИ
# ══════════════════════════════════════════════════════════
NET_OPTS = [
    ("🌐", "DNS Google + Cloudflare 8.8.8.8 + 1.1.1.1",
     "Быстрый публичный DNS — меньше задержка при подключении к серверам.",
     ["netsh interface ip set dns \"Ethernet\" static 8.8.8.8",
      "netsh interface ip add dns \"Ethernet\" 1.1.1.1 index=2",
      "netsh interface ip set dns \"Wi-Fi\" static 8.8.8.8",
      "netsh interface ip add dns \"Wi-Fi\" 1.1.1.1 index=2",
      "ipconfig /flushdns"],
     ["netsh interface ip set dns \"Ethernet\" dhcp",
      "netsh interface ip set dns \"Wi-Fi\" dhcp",
      "ipconfig /flushdns"]),

    ("🏎", "Отключить алгоритм Nagle (TcpAckFrequency=1)",
     "Снижает задержку отправки пакетов — -5-30ms пинга в онлайн играх.",
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpAckFrequency /t REG_DWORD /d 1 /f",
      "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TCPNoDelay /t REG_DWORD /d 1 /f",
      "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpDelAckTicks /t REG_DWORD /d 0 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpAckFrequency /t REG_DWORD /d 2 /f"]),

    ("📶", "QoS DSCP=46 приоритет игрового трафика",
     "Windows даёт игровым пакетам высокий приоритет в сети.",
     ["netsh qos delete policy \"GO_Game\"",
      "netsh qos add policy \"GO_Game\" app=\"*\" dscp=46 throttle-rate=-1"],
     ["netsh qos delete policy \"GO_Game\""]),

    ("🔕", "Отключить IPv6 (убрать конфликты)",
     "Убирает конфликты IPv4/IPv6 которые бывают в российских/СНГ сетях.",
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters\" /v DisabledComponents /t REG_DWORD /d 255 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters\" /v DisabledComponents /t REG_DWORD /d 0 /f"]),

    ("🔄", "Полный сброс Winsock + IP стека",
     "Полный сброс сетевого стека Windows — помогает при странных проблемах.",
     ["netsh winsock reset", "netsh int ip reset",
      "ipconfig /flushdns", "ipconfig /registerdns"],
     []),

    ("🚀", "TCP AutoTuning Highlyrestricted",
     "Стабилизирует TCP соединение — меньше пиков пинга.",
     ["netsh interface tcp set global autotuninglevel=highlyrestricted"],
     ["netsh interface tcp set global autotuninglevel=normal"]),

    ("🌊", "Очистить кэш DNS",
     "Сбросить DNS кэш — помогает при проблемах с подключением.",
     ["ipconfig /flushdns"],
     []),

    ("📡", "Оптимизация буфера TCP",
     "Увеличивает размер окна TCP для лучшей пропускной способности.",
     ["netsh interface tcp set global chimney=enabled",
      "netsh interface tcp set global rss=enabled"],
     ["netsh interface tcp set global chimney=disabled"]),

    ("🔧", "Отключить Network Throttling",
     "Windows ограничивает сеть для мультимедиа — отключаем для игр.",
     ["reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v NetworkThrottlingIndex /t REG_DWORD /d 4294967295 /f"],
     ["reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v NetworkThrottlingIndex /t REG_DWORD /d 10 /f"]),

    ("⚙", "Системный профиль для игр",
     "SystemResponsiveness=0 — Windows уступает всё процессорное время игре.",
     ["reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v SystemResponsiveness /t REG_DWORD /d 0 /f",
      "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games\" /v \"GPU Priority\" /t REG_DWORD /d 8 /f",
      "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games\" /v Priority /t REG_DWORD /d 6 /f"],
     ["reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v SystemResponsiveness /t REG_DWORD /d 20 /f"]),
]

# ══════════════════════════════════════════════════════════
# ГЛАВНЫЙ СЛОВАРЬ ИГР
# ══════════════════════════════════════════════════════════
GAMES = {
    "Rust": {
        "icon":     "🔫",
        "color":    "#e07020",
        "desc":     "Survival multiplayer — EAC защита",
        "steam":    "252490",
        "epic":     None,
        "presets":  RUST_PRESETS,
        "parasites":RUST_PARASITES,
        "tips":     RUST_TIPS,
        "cfg":      RUST_CFG_PATH,
        "kill_cfg": RUST_KILL_CFG,
        "kill_ini": None,
        "cfg_append": True,
        "eac":      True,   # Easy Anti-Cheat — запуск только через Steam!
    },
    "GTA V": {
        "icon":     "🚗",
        "color":    "#00a8ff",
        "desc":     "Open world / FiveM RP серверы",
        "steam":    "271590",
        "epic":     None,
        "presets":  GTAV_PRESETS,
        "parasites":GTAV_PARASITES,
        "tips":     GTAV_TIPS,
        "cfg":      None,
        "kill_cfg": None,
        "kill_ini": None,
        "cfg_append": True,
        "eac":      False,
    },
    "CS2": {
        "icon":     "🎯",
        "color":    "#ff6b35",
        "desc":     "Counter-Strike 2",
        "steam":    "730",
        "epic":     None,
        "presets":  CS2_PRESETS,
        "parasites":CS2_PARASITES,
        "tips":     CS2_TIPS,
        "cfg":      CS2_CFG_PATH,
        "kill_cfg": CS2_KILL_CFG,
        "kill_ini": None,
        "cfg_append": True,
        "eac":      False,
    },
    "Fortnite": {
        "icon":     "🌀",
        "color":    "#00d4ff",
        "desc":     "Battle Royale — Epic Games",
        "steam":    None,
        "epic":     "Fortnite",
        "presets":  FN_PRESETS,
        "parasites":FN_PARASITES,
        "tips":     FN_TIPS,
        "cfg":      FN_INI_PATH,
        "kill_cfg": None,
        "kill_ini": FN_KILL_INI,
        "cfg_append": False,
        "eac":      False,
    },
    "ARK": {
        "icon":     "🦕",
        "color":    "#76b041",
        "desc":     "Survival Evolved / Ascended",
        "steam":    "346110",
        "epic":     None,
        "presets":  ARK_PRESETS,
        "parasites":ARK_PARASITES,
        "tips":     ARK_TIPS,
        "cfg":      None,
        "kill_cfg": None,
        "kill_ini": None,
        "cfg_append": True,
        "eac":      False,
    },
}

# ══════════════════════════════════════════════════════════
# ГОРЯЧИЕ КЛАВИШИ — справочник
# ══════════════════════════════════════════════════════════
HOTKEYS_HELP = {
    "Ctrl+1": "Открыть Rust",
    "Ctrl+2": "Открыть GTA V",
    "Ctrl+3": "Открыть CS2",
    "Ctrl+4": "Открыть Fortnite",
    "Ctrl+5": "Открыть ARK",
    "Ctrl+P": "Профиль ПК",
    "Ctrl+W": "Windows оптимизации",
    "Ctrl+N": "Настройка сети",
    "Ctrl+M": "Мониторинг пинга",
    "F5":     "Обновить профиль ПК",
    "F1":     "Показать горячие клавиши",
}

# ══════════════════════════════════════════════════════════
# FIVEM СПЕЦИАЛЬНЫЕ ТВИКИ
# ══════════════════════════════════════════════════════════
FIVEM_OPTS = [
    ("🧹", "Очистить кэш FiveM",
     "Удаляет кэш шейдеров и текстур — помогает при фризах и вылетах.",
     ["rmdir /s /q \"%LOCALAPPDATA%\\FiveM\\FiveM.app\\cache\""],
     []),

    ("🔕", "Отключить оверлей FiveM",
     "Убирает оверлей сервера — иногда вызывает лаги.",
     ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v DrawOverlay /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v DrawOverlay /t REG_DWORD /d 1 /f"]),

    ("⚡", "StreamMemory 756MB",
     "Увеличить память для стриминга текстур — меньше подгрузок.",
     ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v StreamingMemory /t REG_DWORD /d 756 /f"],
     ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v StreamingMemory /t REG_DWORD /d 512 /f"]),

    ("🌐", "Автовыбор региона",
     "Отключить автовыбор региона FiveM.",
     ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v LastServer /t REG_SZ /d \"\" /f"],
     []),

    ("📁", "Очистить кэш GTA V для FiveM",
     "Очищает устаревший кэш файлов GTA V.",
     ["del /f /q \"%LOCALAPPDATA%\\Rockstar Games\\GTA V\\cache\\*\""],
     []),

    ("🎮", "Откл. NUI (Chromium встроенный)",
     "NUI браузер в FiveM жрёт RAM — отключи если не нужен.",
     ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v NUIEnabled /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v NUIEnabled /t REG_DWORD /d 1 /f"]),
]

FIVEM_TIPS = [
    ("💡", "Параметры запуска FiveM",
     "+set fpslimit 0 +set sv_enforceGameBuild 2189 — добавь в настройках FiveM."),
    ("🎮", "Оверлеи перед FiveM",
     "Обязательно отключи: Discord overlay, Steam overlay, NVIDIA/AMD overlay."),
    ("🔧", "Папка кэша FiveM",
     "%LOCALAPPDATA%\\FiveM\\FiveM.app\\cache — удаляй при лагах и зависаниях."),
    ("📡", "Выбор сервера",
     "Играй на серверах с ping < 60ms для FiveM RP — важно для синхронизации."),
    ("💾", "RAM для FiveM",
     "FiveM + GTA V вместе требуют 12-16GB RAM. Закрой всё лишнее."),
    ("🚀", "Параметр lowmemory",
     "Если мало RAM — добавь в параметры запуска GTA V: -memrestrict 536870912"),
]

# ══════════════════════════════════════════════════════════
# СОВЕТЫ ПО ЖЕЛЕЗУ — общие для всех игр
# ══════════════════════════════════════════════════════════
HARDWARE_TIPS = [
    ("🌡", "Чистка от пыли",
     "Раз в 6 месяцев чисти ПК от пыли и меняй термопасту. +10-20°C разницы."),
    ("💨", "Охлаждение",
     "Температура CPU не должна превышать 85°C под нагрузкой. GPU — 85°C."),
    ("💾", "SSD vs HDD",
     "SSD ускоряет загрузку игр в 3-5 раз. Если возможно — установи игры на SSD."),
    ("🖥", "Монитор 144Hz+",
     "Монитор 144Hz даёт огромное преимущество в динамичных играх — движения плавнее."),
    ("🖱", "Мышь для игр",
     "Игровая мышь с DPI 800-1600 и polling rate 1000Hz — оптимальные настройки."),
    ("🔌", "Блок питания",
     "Слабый БП может вызывать нестабильную работу при пиковой нагрузке."),
    ("📶", "Провод vs WiFi",
     "Кабель Ethernet всегда лучше WiFi для онлайн игр — меньше пинг и потери пакетов."),
    ("🎧", "Гарнитура",
     "Стереогарнитура даёт лучшее позиционирование звука чем обычные наушники."),
]

# ══════════════════════════════════════════════════════════
# ИЗВЕСТНЫЕ ПРОБЛЕМЫ И РЕШЕНИЯ
# ══════════════════════════════════════════════════════════
KNOWN_ISSUES = {
    "Rust": [
        {
            "problem": "EAC блокирует вход в игру",
            "cause":   "Прямой запуск RustClient.exe, изменения в реестре Facepunch",
            "fix":     "Запускай ТОЛЬКО через Steam. Запусти FixRustEAC.bat для очистки реестра.",
            "danger":  True,
        },
        {
            "problem": "Постоянные фризы каждые несколько секунд",
            "cause":   "Нехватка RAM или загрузка скинов предметов",
            "fix":     "graphics.itemskins 0 в client.cfg + закрой фоновые программы.",
            "danger":  False,
        },
        {
            "problem": "Низкий FPS несмотря на настройки",
            "cause":   "Трава и тени — главные убийцы FPS в Rust",
            "fix":     "grass.on false + graphics.shadows 0 в F1 консоли.",
            "danger":  False,
        },
        {
            "problem": "Игра вылетает при входе на сервер",
            "cause":   "Переполненный кэш шейдеров",
            "fix":     "Удали папку: %LocalAppData%\\Temp\\Rust",
            "danger":  False,
        },
    ],
    "GTA V": [
        {
            "problem": "FiveM вылетает при загрузке",
            "cause":   "Устаревший кэш FiveM или конфликт оверлеев",
            "fix":     "Удали кэш FiveM и отключи все оверлеи (Discord, Steam, NVIDIA).",
            "danger":  False,
        },
        {
            "problem": "Низкий FPS в онлайн",
            "cause":   "Много NPC и Extended Distance",
            "fix":     "Снизь плотность NPC до 0 и Extended Distance до 0 в реестре.",
            "danger":  False,
        },
        {
            "problem": "Зависание при запуске",
            "cause":   "Rockstar Launcher или антивирус блокирует",
            "fix":     "Добавь папку GTA V в исключения Defender, перезапусти Launcher.",
            "danger":  False,
        },
    ],
    "CS2": [
        {
            "problem": "Заикание / stuttering при движении",
            "cause":   "Shader compilation или NVIDIA Reflex",
            "fix":     "Добавь +r_dynamic_lighting 0 +mat_queue_mode -1 в параметры запуска.",
            "danger":  False,
        },
        {
            "problem": "Высокий пинг несмотря на хороший интернет",
            "cause":   "Алгоритм Nagle или DNS",
            "fix":     "Отключи Nagle (TcpAckFrequency=1) и смени DNS на Google 8.8.8.8.",
            "danger":  False,
        },
        {
            "problem": "FPS падает до 20-30 каждые несколько минут",
            "cause":   "Windows Update или антивирус сканирует в фоне",
            "fix":     "Остановить wuauserv + добавить CS2 в исключения Defender.",
            "danger":  False,
        },
    ],
    "Fortnite": [
        {
            "problem": "Черный экран при запуске",
            "cause":   "DirectX 12 не поддерживается или конфликт драйвера",
            "fix":     "Убери -dx12 из параметров запуска, попробуй -dx11.",
            "danger":  False,
        },
        {
            "problem": "Фризы при строительстве",
            "cause":   "Нехватка VRAM или CPU bottleneck",
            "fix":     "Снизь качество текстур до Low, отключи Shadows.",
            "danger":  False,
        },
        {
            "problem": "Долгая загрузка шейдеров",
            "cause":   "Первый запуск или обновление игры",
            "fix":     "Добавь папку Fortnite в исключения Windows Defender.",
            "danger":  False,
        },
    ],
    "ARK": [
        {
            "problem": "Постоянные вылеты на рабочий стол",
            "cause":   "Нехватка RAM или переполненный кэш",
            "fix":     "Добавь -lowmemory в параметры, удали папку Saved\\Cache.",
            "danger":  False,
        },
        {
            "problem": "5-10 FPS рядом с базой трайба",
            "cause":   "Много структур и динозавров в зоне видимости",
            "fix":     "Снизь Foliage до 0, View Distance до минимума, Shadow до 0.",
            "danger":  False,
        },
        {
            "problem": "Зависание при телепортации",
            "cause":   "Подгрузка шейдеров новой зоны",
            "fix":     "Подожди — это нормально при первом посещении локации.",
            "danger":  False,
        },
    ],
}

# ══════════════════════════════════════════════════════════
# КОНФИГИ ДЛЯ БЫСТРОГО ПРИМЕНЕНИЯ
# ══════════════════════════════════════════════════════════

# Полный список Windows-оптимизаций для кнопки "Применить всё"
WIN_ALL_STEPS = [
    ("⚡ Высокий план питания",
     "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"),
    ("🔕 Откл. Game DVR / Xbox Bar",
     "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f"),
    ("🔕 Откл. Game DVR политика",
     "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR\" /v AllowGameDVR /t REG_DWORD /d 0 /f"),
    ("📈 Приоритет CPU Win32=38",
     "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f"),
    ("🎮 HAGS GPU Scheduling",
     "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v HwSchMode /t REG_DWORD /d 2 /f"),
    ("🖥 Откл. визуальные эффекты",
     "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects\" /v VisualFXSetting /t REG_DWORD /d 2 /f"),
    ("🔍 Стоп Windows Search",
     "net stop wsearch"),
    ("📊 Стоп SysMain",
     "net stop sysmain"),
    ("⏸ Стоп Windows Update",
     "net stop wuauserv"),
    ("🔧 Откл. Network Throttling",
     "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v NetworkThrottlingIndex /t REG_DWORD /d 4294967295 /f"),
    ("🎮 System Profile Games GPU",
     "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games\" /v \"GPU Priority\" /t REG_DWORD /d 8 /f"),
    ("🎮 System Profile Games Priority",
     "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games\" /v Priority /t REG_DWORD /d 6 /f"),
    ("🌐 DNS Google Ethernet",
     "netsh interface ip set dns \"Ethernet\" static 8.8.8.8"),
    ("🌐 DNS Cloudflare Ethernet",
     "netsh interface ip add dns \"Ethernet\" 1.1.1.1 index=2"),
    ("🌐 DNS Google WiFi",
     "netsh interface ip set dns \"Wi-Fi\" static 8.8.8.8"),
    ("🌐 DNS Cloudflare WiFi",
     "netsh interface ip add dns \"Wi-Fi\" 1.1.1.1 index=2"),
    ("🏎 Откл. Nagle TcpAckFrequency",
     "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpAckFrequency /t REG_DWORD /d 1 /f"),
    ("🏎 Откл. Nagle TCPNoDelay",
     "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TCPNoDelay /t REG_DWORD /d 1 /f"),
    ("🔄 Flush DNS",
     "ipconfig /flushdns"),
    ("🧹 Очистка RAM",
     "rundll32.exe advapi32.dll,ProcessIdleTasks"),
]

# Список серверов для проверки пинга
PING_SERVERS = [
    ("Steam",        "store.steampowered.com"),
    ("Cloudflare",   "1.1.1.1"),
    ("Google DNS",   "8.8.8.8"),
    ("Faceit",       "api.faceit.com"),
    ("AWS EU",       "ec2.eu-central-1.amazonaws.com"),
    ("AWS US",       "ec2.us-east-1.amazonaws.com"),
    ("Yandex",       "yandex.ru"),
    ("Mail.ru",      "mail.ru"),
]


# ══════════════════════════════════════════════════════════
# ГЛАВНЫЙ КЛАСС ПРИЛОЖЕНИЯ
# ══════════════════════════════════════════════════════════

class App(ctk.CTk):
    """
    Game Optimizer v5.0 — главное окно приложения.
    Структура:
        - Боковая панель (sidebar): кнопки игр + навигация
        - Область контента: страницы для каждой игры и раздела
    """

    def __init__(self):
        super().__init__()
        self.title("Game Optimizer v5.0")
        self.configure(fg_color=T("bg"))

        # Состояние мониторинга пинга
        self.monitor_running = False
        self.ping_history    = []

        # Фоновые потоки
        self._live_running = True

        # Ссылки на логи (хранятся здесь чтобы не терять при перестройке)
        self._kill_log_widget = [None]   # лог кнопки "убить паразиты"
        self.win_log          = None     # лог Windows оптимизаций
        self.net_log          = None     # лог сетевых оптимизаций

        # Ссылки на виджеты профиля
        self.info_labels = {}
        self.stat_boxes  = {}
        self.prog_bars   = {}
        self.ping_g      = None
        self.ping_s      = None

        # Ссылки на виджеты мониторинга
        self.ms_cur    = None
        self.ms_avg    = None
        self.ms_max    = None
        self.srv_lbls  = {}
        self.chart     = None
        self.mon_btn   = None
        self.mon_lbl   = None
        self.mon_int   = None

        # Строим интерфейс
        self._build_ui()
        self._bind_hotkeys()

        # Размер окна — после build_ui чтобы не вызывать рекурсию
        self.geometry("1130x730")
        self.minsize(990, 650)

    # ══════════════════════════════════════════════════════
    # ГОРЯЧИЕ КЛАВИШИ
    # ══════════════════════════════════════════════════════

    def _bind_hotkeys(self):
        """Назначить горячие клавиши"""
        game_names = list(GAMES.keys())
        for i, gname in enumerate(game_names):
            self.bind(
                f"<Control-Key-{i + 1}>",
                lambda e, g=gname: self.show_game(g)
            )
        self.bind("<Control-p>", lambda e: self.show_page("profile"))
        self.bind("<Control-P>", lambda e: self.show_page("profile"))
        self.bind("<Control-w>", lambda e: self.show_page("windows"))
        self.bind("<Control-W>", lambda e: self.show_page("windows"))
        self.bind("<Control-n>", lambda e: self.show_page("network"))
        self.bind("<Control-N>", lambda e: self.show_page("network"))
        self.bind("<Control-m>", lambda e: self.show_page("monitor"))
        self.bind("<Control-M>", lambda e: self.show_page("monitor"))
        self.bind("<F5>",        lambda e: self._refresh_profile())
        self.bind("<F1>",        lambda e: self._show_hotkeys_help())

    def _show_hotkeys_help(self):
        """Показать окно с горячими клавишами"""
        win = ctk.CTkToplevel(self)
        win.title("Горячие клавиши")
        win.geometry("340x320")
        win.configure(fg_color=T("bg"))
        win.lift()
        win.focus_force()
        ctk.CTkLabel(
            win, text="⌨️ Горячие клавиши",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T("accent")
        ).pack(pady=(16, 10))
        for key, desc in HOTKEYS_HELP.items():
            row = ctk.CTkFrame(win, fg_color=T("panel2"), corner_radius=6)
            row.pack(fill="x", padx=16, pady=2)
            ri = ctk.CTkFrame(row, fg_color="transparent")
            ri.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(
                ri, text=key, width=70,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=T("accent")
            ).pack(side="left")
            ctk.CTkLabel(
                ri, text=desc,
                font=ctk.CTkFont(size=10),
                text_color=T("text")
            ).pack(side="left", padx=8)
        make_btn(win, "✕  Закрыть", win.destroy,
                 size=11, corner=8).pack(pady=12)

    # ══════════════════════════════════════════════════════
    # ПОСТРОЕНИЕ ОСНОВНОГО ИНТЕРФЕЙСА
    # ══════════════════════════════════════════════════════

    def _build_ui(self):
        """Строит боковую панель и область контента"""

        # ── Боковая панель ───────────────────────────────
        sb = ctk.CTkFrame(
            self, width=196,
            fg_color=T("panel"), corner_radius=0,
            border_width=1, border_color=T("border")
        )
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # Логотип
        lf = ctk.CTkFrame(sb, fg_color="transparent")
        lf.pack(pady=(14, 2), padx=10)
        ctk.CTkLabel(
            lf, text="🎮",
            font=ctk.CTkFont(size=22)
        ).pack(side="left")
        ctk.CTkLabel(
            lf, text=" GAME OPT",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=T("accent")
        ).pack(side="left")

        ctk.CTkLabel(
            sb, text="v5.0  •  F1 = клавиши",
            font=ctk.CTkFont(size=8),
            text_color=T("dim")
        ).pack()

        ctk.CTkFrame(sb, height=1, fg_color=T("border")).pack(
            fill="x", padx=10, pady=6)

        # Раздел "ИГРЫ"
        ctk.CTkLabel(
            sb, text="ИГРЫ",
            font=ctk.CTkFont(size=9),
            text_color=T("dim")
        ).pack(anchor="w", padx=12)

        self.game_btns = {}
        for i, (gname, g) in enumerate(GAMES.items()):
            # Кнопка игры
            b = ctk.CTkButton(
                sb,
                text=f"{g['icon']}  {gname}",
                anchor="w",
                font=ctk.CTkFont(size=12),
                height=32,
                fg_color="transparent",
                hover_color=T("panel2"),
                text_color=T("dim"),
                corner_radius=8,
                command=lambda gn=gname: self.show_game(gn)
            )
            b.pack(fill="x", padx=7, pady=1)
            self.game_btns[gname] = b

            # Подсказка с горячей клавишей
            ctk.CTkLabel(
                sb,
                text=f"  Ctrl+{i + 1}",
                font=ctk.CTkFont(size=7),
                text_color=T("dim")
            ).pack(anchor="w", padx=16)

        ctk.CTkFrame(sb, height=1, fg_color=T("border")).pack(
            fill="x", padx=10, pady=6)

        # Раздел "ОБЩЕЕ"
        ctk.CTkLabel(
            sb, text="ОБЩЕЕ",
            font=ctk.CTkFont(size=9),
            text_color=T("dim")
        ).pack(anchor="w", padx=12)

        self.nav_btns = {}
        nav_items = [
            ("profile", "💻  Профиль ПК",    "Ctrl+P"),
            ("windows", "⚡  Windows",        "Ctrl+W"),
            ("network", "🌐  Сеть",           "Ctrl+N"),
            ("monitor", "📊  Мониторинг",     "Ctrl+M"),
        ]
        for pid, lbl, hotkey in nav_items:
            f = ctk.CTkFrame(sb, fg_color="transparent")
            f.pack(fill="x")
            b = ctk.CTkButton(
                f, text=lbl, anchor="w",
                font=ctk.CTkFont(size=11), height=30,
                fg_color="transparent",
                hover_color=T("panel2"),
                text_color=T("dim"), corner_radius=8,
                command=lambda p=pid: self.show_page(p)
            )
            b.pack(fill="x", padx=7)
            ctk.CTkLabel(
                f, text=f"  {hotkey}",
                font=ctk.CTkFont(size=7),
                text_color=T("dim")
            ).pack(anchor="w", padx=16)
            self.nav_btns[pid] = b

        # Разделитель
        ctk.CTkFrame(sb, height=1, fg_color=T("border")).pack(
            fill="x", padx=10, pady=6)

        # Кнопка смены темы
        make_btn(
            sb, "🎨  Тема оформления",
            self._open_theme_window,
            size=10, bold=False, corner=8
        ).pack(fill="x", padx=7, pady=2)

        # Кнопка горячих клавиш
        make_btn(
            sb, "⌨️  Горячие клавиши (F1)",
            self._show_hotkeys_help,
            size=10, bold=False,
            color=T("panel2"), hover=T("panel"), corner=8
        ).pack(fill="x", padx=7, pady=2)

        # Шутка внизу
        ctk.CTkFrame(sb, height=1, fg_color=T("border")).pack(
            fill="x", padx=10, pady=4, side="bottom")
        self.joke_lbl = ctk.CTkLabel(
            sb, text=random.choice(JOKES),
            font=ctk.CTkFont(size=8, slant="italic"),
            text_color=T("gold"),
            wraplength=174, justify="center"
        )
        self.joke_lbl.pack(side="bottom", padx=7, pady=5)

        # ── Область контента ─────────────────────────────
        self.content = ctk.CTkFrame(self, fg_color=T("bg"), corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

        # Строим все страницы
        self.pages = {}
        for gname in GAMES:
            self._build_game_page(gname)
        self._build_profile_page()
        self._build_windows_page()
        self._build_network_page()
        self._build_monitor_page()

        # Открываем первую страницу
        self.show_game("Rust")

    # ══════════════════════════════════════════════════════
    # СМЕНА ТЕМЫ
    # ══════════════════════════════════════════════════════

    def _open_theme_window(self):
        """Окно выбора темы оформления"""
        win = ctk.CTkToplevel(self)
        win.title("Выбор темы")
        win.geometry("320x300")
        win.configure(fg_color=T("bg"))
        win.lift()
        win.focus_force()

        ctk.CTkLabel(
            win, text="🎨 Выбери тему оформления",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=T("accent")
        ).pack(pady=(16, 12))

        for theme_name, th in THEMES.items():
            is_current = (theme_name == _CURRENT_THEME)
            btn = ctk.CTkButton(
                win,
                text=("✓  " if is_current else "    ") + theme_name,
                font=ctk.CTkFont(size=12),
                fg_color=th["panel2"],
                hover_color=th["panel"],
                text_color=th["accent"],
                border_width=2 if is_current else 1,
                border_color=th["accent"] if is_current else th["border"],
                corner_radius=10,
                command=lambda tn=theme_name: self._apply_theme(tn, win)
            )
            btn.pack(fill="x", padx=20, pady=4)

    def _apply_theme(self, theme_name, win):
        """Применить выбранную тему"""
        set_theme(theme_name)
        win.destroy()
        messagebox.showinfo(
            "Тема изменена",
            f"Тема «{theme_name}» выбрана!\n\n"
            "Перезапусти программу для полного применения темы."
        )

    # ══════════════════════════════════════════════════════
    # ПЕРЕКЛЮЧЕНИЕ СТРАНИЦ
    # ══════════════════════════════════════════════════════

    def show_game(self, gname):
        """Показать страницу игры"""
        for p in self.pages.values():
            p.pack_forget()
        self.pages[gname].pack(fill="both", expand=True)

        # Обновляем кнопки боковой панели
        for k, b in self.game_btns.items():
            if k == gname:
                b.configure(
                    fg_color=T("panel2"),
                    text_color=GAMES[k]["color"]
                )
            else:
                b.configure(
                    fg_color="transparent",
                    text_color=T("dim")
                )
        for b in self.nav_btns.values():
            b.configure(fg_color="transparent", text_color=T("dim"))

    def show_page(self, pid):
        """Показать страницу раздела (профиль/windows/сеть/монитор)"""
        for p in self.pages.values():
            p.pack_forget()
        self.pages[pid].pack(fill="both", expand=True)

        for b in self.game_btns.values():
            b.configure(fg_color="transparent", text_color=T("dim"))
        for k, b in self.nav_btns.items():
            if k == pid:
                b.configure(fg_color=T("panel2"), text_color=T("accent"))
            else:
                b.configure(fg_color="transparent", text_color=T("dim"))

    # ══════════════════════════════════════════════════════
    # СКРОЛЛ — вспомогательные методы
    # ══════════════════════════════════════════════════════

    def _scrollable(self, parent):
        """
        Создать скроллируемую область с колёсиком мыши.
        Использует tkinter.Canvas — без CTkScrollableFrame (вызывает рекурсию).
        Скролл работает только когда мышь над этой областью.
        """
        canvas = tkinter.Canvas(parent, bg=T("bg"), highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(
            parent, command=canvas.yview,
            button_color=T("accent"),
            button_hover_color=T("accent2")
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = ctk.CTkFrame(canvas, fg_color="transparent")
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        # Подстраиваем ширину под размер канваса
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(win_id, width=e.width)
        )
        # Обновляем scrollregion при изменении содержимого
        inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Колёсико работает только когда мышь над этой областью
        def _enter(e):
            canvas.bind_all(
                "<MouseWheel>",
                lambda ev: canvas.yview_scroll(int(-1 * (ev.delta / 120)), "units")
            )
        def _leave(e):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", _enter)
        canvas.bind("<Leave>", _leave)
        inner.bind("<Enter>",  _enter)
        inner.bind("<Leave>",  _leave)

        return inner

    def _make_page(self, pid):
        """Создать страницу раздела со скроллом"""
        outer = ctk.CTkFrame(self.content, fg_color=T("bg"), corner_radius=0)
        self.pages[pid] = outer
        inner = self._scrollable(outer)
        pad = ctk.CTkFrame(inner, fg_color="transparent")
        pad.pack(fill="both", expand=True, padx=20, pady=14)
        return pad

    # ══════════════════════════════════════════════════════
    # ВИДЖЕТ-ХЕЛПЕРЫ
    # ══════════════════════════════════════════════════════

    def _make_log(self, parent, height=105):
        """Создать текстовый лог-бокс"""
        tb = ctk.CTkTextbox(
            parent, height=height,
            fg_color=T("panel"),
            border_width=1, border_color=T("border"),
            font=ctk.CTkFont(family="Courier New", size=11),
            text_color=T("green"),
            corner_radius=10
        )
        tb.pack(fill="x", pady=(3, 0))
        tb.configure(state="disabled")
        return tb

    def _log_write(self, tb, text):
        """Написать строку в лог"""
        if tb is None:
            return
        tb.configure(state="normal")
        tb.insert("end", text + "\n")
        tb.configure(state="disabled")
        tb.see("end")

    def _log_clear(self, tb):
        """Очистить лог"""
        if tb is None:
            return
        tb.configure(state="normal")
        tb.delete("1.0", "end")
        tb.configure(state="disabled")

    def _section_label(self, parent, text):
        """Заголовок секции — тёмная полоска с текстом"""
        f = ctk.CTkFrame(
            parent, fg_color=T("panel2"),
            corner_radius=6, height=26
        )
        f.pack(fill="x", pady=(5, 2))
        f.pack_propagate(False)
        ctk.CTkLabel(
            f, text=text,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=T("accent")
        ).pack(anchor="w", padx=10, pady=4)

    def _divider(self, parent):
        """Горизонтальный разделитель"""
        ctk.CTkFrame(parent, height=1, fg_color=T("border")).pack(
            fill="x", pady=6)

    def _safe_set(self, lbl, text):
        """Безопасно установить текст метки (не падает если виджет удалён)"""
        try:
            lbl.configure(text=text)
        except Exception:
            pass

    def _compact_toggle(self, parent, ico, name, desc, on_cmds, off_cmds):
        """
        Компактный переключатель в одну строку:
        [полоска] [иконка] [название + описание] [switch]
        """
        row = ctk.CTkFrame(
            parent, fg_color=T("panel2"),
            corner_radius=8, border_width=1,
            border_color=T("border")
        )
        row.pack(fill="x", pady=1)

        # Акцентная полоска слева
        ctk.CTkFrame(
            row, width=3, fg_color=T("accent"), corner_radius=0
        ).pack(side="left", fill="y")

        # Иконка
        ctk.CTkLabel(
            row, text=ico,
            font=ctk.CTkFont(size=13), width=24
        ).pack(side="left", padx=(5, 2))

        # Текст: название + описание
        text_f = ctk.CTkFrame(row, fg_color="transparent")
        text_f.pack(side="left", fill="x", expand=True, pady=4)
        ctk.CTkLabel(
            text_f, text=name,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w")
        ctk.CTkLabel(
            text_f, text=desc,
            font=ctk.CTkFont(size=9),
            text_color=T("dim")
        ).pack(anchor="w")

        # Переключатель
        var = ctk.BooleanVar(value=False)
        def _on_toggle(v=var, on=on_cmds, off=off_cmds):
            cmds = on if v.get() else off
            threading.Thread(
                target=lambda c=cmds: [run_cmd(x) for x in c],
                daemon=True
            ).start()

        ctk.CTkSwitch(
            row, text="",
            variable=var, command=_on_toggle,
            progress_color=T("accent"),
            button_color=T("text"),
            width=38
        ).pack(side="right", padx=7)

    # ══════════════════════════════════════════════════════
    # СТРАНИЦА ИГРЫ — главный строитель
    # ══════════════════════════════════════════════════════

    def _build_game_page(self, gname):
        """Построить страницу для конкретной игры"""
        g = GAMES[gname]
        outer = ctk.CTkFrame(self.content, fg_color=T("bg"), corner_radius=0)
        self.pages[gname] = outer

        # ── Шапка ────────────────────────────────────────
        hbar = ctk.CTkFrame(
            outer, fg_color=T("panel"),
            corner_radius=0, border_width=1,
            border_color=T("border"), height=58
        )
        hbar.pack(fill="x")
        hbar.pack_propagate(False)

        hi = ctk.CTkFrame(hbar, fg_color="transparent")
        hi.pack(fill="both", padx=14, pady=8)

        # Иконка игры
        ctk.CTkLabel(
            hi, text=g["icon"],
            font=ctk.CTkFont(size=26)
        ).pack(side="left", padx=(0, 10))

        # Название и описание
        title_f = ctk.CTkFrame(hi, fg_color="transparent")
        title_f.pack(side="left", fill="y", expand=True)
        ctk.CTkLabel(
            title_f, text=gname,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=g["color"]
        ).pack(anchor="w")

        # Описание + EAC предупреждение
        desc_text = g["desc"]
        if g.get("eac"):
            desc_text += " • ⚠ EAC: только через Steam!"
        ctk.CTkLabel(
            title_f, text=desc_text,
            font=ctk.CTkFont(size=9),
            text_color=T("dim") if not g.get("eac") else T("gold")
        ).pack(anchor="w")

        # Кнопки в шапке
        btn_f = ctk.CTkFrame(hi, fg_color="transparent")
        btn_f.pack(side="right")

        make_btn(
            btn_f, "▶  ЗАПУСТИТЬ",
            lambda gn=gname: self._launch_game(gn),
            color=T("accent"), hover=T("accent2"),
            size=11, width=128
        ).pack(side="left", padx=3)

        make_btn(
            btn_f, "⚡  ВСЁ",
            lambda gn=gname: self._full_optimize(gn),
            color=T("panel2"), hover=T("panel"),
            size=11, width=85
        ).pack(side="left", padx=3)

        # ── Панель вкладок ────────────────────────────────
        tab_bar = ctk.CTkFrame(
            outer, fg_color=T("panel2"),
            corner_radius=0, height=34
        )
        tab_bar.pack(fill="x")
        tab_bar.pack_propagate(False)

        tab_content = ctk.CTkFrame(outer, fg_color=T("bg"), corner_radius=0)
        tab_content.pack(fill="both", expand=True)

        tab_frames = {}
        tab_btns   = {}

        # Список вкладок зависит от игры
        tab_names = ["🎨 Графика", "🚫 Паразиты", "🌐 Сеть", "💡 Советы"]
        if gname == "CS2":
            tab_names.append("⚙️ Конфиг")
        elif gname == "GTA V":
            tab_names.append("🟣 FiveM")
        elif gname in ("Rust", "ARK", "Fortnite"):
            tab_names.append("🔩 Launch")

        def _show_tab(name, frames=tab_frames, btns=tab_btns):
            for f in frames.values():
                f.pack_forget()
            frames[name].pack(fill="both", expand=True)
            for n, b in btns.items():
                if n == name:
                    b.configure(
                        fg_color=T("panel"),
                        text_color=T("accent")
                    )
                else:
                    b.configure(
                        fg_color="transparent",
                        text_color=T("dim")
                    )

        # Создаём кнопки и фреймы для каждой вкладки
        for tname in tab_names:
            tb_btn = ctk.CTkButton(
                tab_bar, text=tname, anchor="w",
                font=ctk.CTkFont(size=10), height=32,
                fg_color="transparent",
                hover_color=T("panel"),
                text_color=T("dim"),
                corner_radius=0, width=112,
                command=lambda t=tname: _show_tab(t)
            )
            tb_btn.pack(side="left", padx=1)
            tab_btns[tname] = tb_btn

            # Скроллируемый фрейм вкладки
            frame = ctk.CTkFrame(tab_content, fg_color=T("bg"), corner_radius=0)
            tab_frames[tname] = frame
            sc_inner = self._scrollable(frame)
            inner = ctk.CTkFrame(sc_inner, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=18, pady=11)

            # Строим содержимое вкладки
            if "Графика"  in tname: self._build_tab_graphics(inner, gname, g)
            elif "Паразиты" in tname: self._build_tab_parasites(inner, gname, g)
            elif "Сеть"   in tname: self._build_tab_net_game(inner, gname)
            elif "Советы" in tname: self._build_tab_tips(inner, g)
            elif "Конфиг" in tname: self._build_tab_cs2cfg(inner)
            elif "FiveM"  in tname: self._build_tab_fivem(inner)
            elif "Launch" in tname: self._build_tab_launch(inner, gname, g)

        # Открываем первую вкладку
        _show_tab(tab_names[0])

    # ══════════════════════════════════════════════════════
    # ВКЛАДКА: ГРАФИКА
    # ══════════════════════════════════════════════════════

    def _build_tab_graphics(self, pad, gname, g):
        """Вкладка с пресетами графики"""
        ctk.CTkLabel(
            pad, text="🎨 Пресеты графики",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w", pady=(0, 3))
        ctk.CTkLabel(
            pad,
            text="Выбери пресет → получишь список настроек и параметры запуска для Steam",
            font=ctk.CTkFont(size=10),
            text_color=T("dim")
        ).pack(anchor="w", pady=(0, 8))

        log_ref = [None]

        # Карточки пресетов в сетке
        grid = ctk.CTkFrame(pad, fg_color="transparent")
        grid.pack(fill="x", pady=(0, 6))

        for i, (pname, pdata) in enumerate(g["presets"].items()):
            grid.columnconfigure(i, weight=1)

            card = ctk.CTkFrame(
                grid, fg_color=T("panel"),
                corner_radius=12,
                border_width=2, border_color=T("border")
            )
            card.grid(row=0, column=i, padx=4, sticky="ew")

            ci = ctk.CTkFrame(card, fg_color="transparent")
            ci.pack(fill="both", padx=11, pady=10)

            # Название пресета
            ctk.CTkLabel(
                ci, text=pname,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=g["color"]
            ).pack(anchor="w")

            # Описание
            ctk.CTkLabel(
                ci, text=pdata["desc"],
                font=ctk.CTkFont(size=9),
                text_color=T("dim")
            ).pack(anchor="w", pady=(1, 4))

            # FPS ожидаемый
            fps_row = ctk.CTkFrame(ci, fg_color="transparent")
            fps_row.pack(anchor="w", pady=(0, 4))
            ctk.CTkLabel(
                fps_row, text="FPS: ",
                font=ctk.CTkFont(size=9),
                text_color=T("dim")
            ).pack(side="left")
            ctk.CTkLabel(
                fps_row, text=pdata["fps"],
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color=T("green")
            ).pack(side="left")

            # Кол-во настроек
            ctk.CTkLabel(
                ci, text=f"{len(pdata['settings'])} настроек",
                font=ctk.CTkFont(size=9),
                text_color=T("dim")
            ).pack(anchor="w", pady=(0, 6))

            # Кнопка применить
            make_btn(
                ci, "✓  Применить",
                lambda p=pdata, n=pname, lr=log_ref: self._apply_preset(p, n, lr),
                size=10, bold=False, width=130
            ).pack(anchor="w")

        log_ref[0] = self._make_log(pad, 90)

    def _apply_preset(self, pdata, pname, log_ref):
        """Применить пресет — показать настройки в логе"""
        if not log_ref[0]:
            return
        self._log_clear(log_ref[0])
        self._log_write(log_ref[0], f"▶ Применяю пресет «{pname}»...")

        def run():
            for k, v in pdata["settings"]:
                self._log_write(log_ref[0], f"  {k} = {v}")
                time.sleep(0.02)
            launch = pdata.get("launch", "")
            if launch:
                self._log_write(log_ref[0], "")
                self._log_write(log_ref[0], "Steam → ПКМ игра → Свойства → Параметры запуска:")
                self._log_write(log_ref[0], f"  {launch}")
                self._log_write(log_ref[0], "  Скопируй строку выше и вставь!")
            self._log_write(log_ref[0], "")
            self._log_write(log_ref[0], f"✅ Готово! Ожидаемый FPS: {pdata['fps']}")

        threading.Thread(target=run, daemon=True).start()

    # ══════════════════════════════════════════════════════
    # ВКЛАДКА: ПАРАЗИТЫ
    # ══════════════════════════════════════════════════════

    def _build_tab_parasites(self, pad, gname, g):
        """Вкладка с паразитными функциями игры"""
        ctk.CTkLabel(
            pad, text="🚫 Паразитные функции",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w", pady=(0, 3))

        # Предупреждение для игр с EAC
        if g.get("eac"):
            warn_f = ctk.CTkFrame(
                pad, fg_color=T("panel2"),
                corner_radius=10,
                border_width=2, border_color=T("gold")
            )
            warn_f.pack(fill="x", pady=(0, 8))
            wf = ctk.CTkFrame(warn_f, fg_color="transparent")
            wf.pack(fill="x", padx=12, pady=8)
            ctk.CTkLabel(
                wf, text="⚠  RUST + EAC: используем ТОЛЬКО client.cfg команды!",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=T("gold")
            ).pack(anchor="w")
            ctk.CTkLabel(
                wf,
                text="Это стандартные консольные команды игры — абсолютно безопасно для EAC.\n"
                     "НЕ редактируем реестр HKCU\\Software\\Facepunch\\Rust — EAC это проверяет!",
                font=ctk.CTkFont(size=9),
                text_color=T("text"),
                justify="left"
            ).pack(anchor="w")

        ctk.CTkLabel(
            pad,
            text="Тогл вправо = выключить.  Кнопка ☠️ = убить всё одним кликом.",
            font=ctk.CTkFont(size=9),
            text_color=T("dim")
        ).pack(anchor="w", pady=(0, 6))

        # Паразиты игры
        self._section_label(pad, f"🎮 Внутри {gname} — ненужные функции")
        for ico, name, desc, on_c, off_c in g["parasites"]:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c)

        self._divider(pad)

        # Оверлеи
        self._section_label(pad, "🖥 Оверлеи — жрут FPS и память")
        for ico, name, desc, on_c, off_c in OVERLAYS:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c)

        self._divider(pad)

        # Фоновые процессы
        self._section_label(pad, "⚙️ Фоновые процессы Windows")
        for ico, name, desc, on_c, off_c in BG_PROCS:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c)

        self._divider(pad)

        # Главная кнопка — убить всё
        kill_btn = ctk.CTkButton(
            pad,
            text=f"☠️  УБИТЬ ВСЕ ПАРАЗИТЫ {gname.upper()}",
            command=lambda gn=gname: self._kill_all_parasites(gn),
            fg_color=T("accent"),
            hover_color=T("accent2"),
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=12, height=40
        )
        kill_btn.pack(fill="x", pady=(0, 4))

        make_btn(
            pad, "🚫  ОТКЛ. ВСЕ СИСТЕМНЫЕ ПАРАЗИТЫ",
            self._kill_system_parasites,
            color=T("panel2"), hover=T("panel"),
            size=11
        ).pack(fill="x")

        # Лог результатов
        self._kill_log_widget[0] = self._make_log(pad, 70)

    def _kill_all_parasites(self, gname):
        """Убить всех паразитов для конкретной игры"""
        g   = GAMES[gname]
        log = self._kill_log_widget[0]

        def run():
            if log:
                self._log_write(log, f"☠️ Убиваю паразиты {gname}...")
            count = 0

            # Паразиты игры через реестр
            for item in g["parasites"]:
                ico, name, desc, on_c, off_c = item
                for cmd in on_c:
                    run_cmd(cmd)
                    count += 1

            # Оверлеи
            for ico, name, desc, on_c, off_c in OVERLAYS:
                for cmd in on_c:
                    run_cmd(cmd)
                    count += 1

            # Запись в файл конфигурации игры
            cfg_path = g.get("cfg")
            kill_cfg = g.get("kill_cfg")
            kill_ini = g.get("kill_ini")

            if cfg_path and kill_cfg:
                path = expand(cfg_path)
                try:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    mode = "a" if g.get("cfg_append", True) else "w"
                    with open(path, mode, encoding="utf-8") as f:
                        f.write("\n" + kill_cfg + "\n")
                    if log:
                        self._log_write(log, f"  ✓ Записано: {os.path.basename(path)}")
                except Exception as e:
                    if log:
                        self._log_write(log, f"  ✗ Ошибка файла: {e}")

            if cfg_path and kill_ini:
                path = expand(cfg_path)
                try:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(kill_ini)
                    if log:
                        self._log_write(log, f"  ✓ INI записан: {os.path.basename(path)}")
                except Exception as e:
                    if log:
                        self._log_write(log, f"  ✗ Ошибка INI: {e}")

            if log:
                self._log_write(log, f"  ✓ Выполнено {count} операций")
                self._log_write(log, f"✅ {gname} — паразиты убиты!")

        threading.Thread(target=run, daemon=True).start()

    def _kill_system_parasites(self):
        """Отключить системные паразиты Windows"""
        cmds = [
            "net stop wuauserv",
            "net stop wsearch",
            "net stop sysmain",
            "taskkill /f /im OneDrive.exe",
            "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" "
            "/v AppCaptureEnabled /t REG_DWORD /d 0 /f",
            "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR\" "
            "/v AllowGameDVR /t REG_DWORD /d 0 /f",
        ]
        threading.Thread(
            target=lambda: [run_cmd(c) for c in cmds],
            daemon=True
        ).start()

    # ══════════════════════════════════════════════════════
    # ВКЛАДКА: СЕТЬ (внутри игры)
    # ══════════════════════════════════════════════════════

    def _build_tab_net_game(self, pad, gname):
        """Вкладка сетевых оптимизаций внутри игры"""
        ctk.CTkLabel(
            pad, text="🌐 Настройка сети",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w", pady=(0, 3))
        ctk.CTkLabel(
            pad, text=f"Оптимизация пинга специально для {gname}",
            font=ctk.CTkFont(size=10),
            text_color=T("dim")
        ).pack(anchor="w", pady=(0, 8))

        for ico, name, desc, on_c, off_c in NET_OPTS:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c)

        self._divider(pad)
        make_btn(
            pad, "📡  Проверить пинг",
            lambda p=pad: self._quick_ping_check(p),
            width=185
        ).pack(anchor="w")

    def _quick_ping_check(self, pad):
        """Быстрая проверка пинга до основных серверов"""
        log = self._make_log(pad, 70)

        def run():
            for name, host in [
                ("Google",     "8.8.8.8"),
                ("Steam",      "store.steampowered.com"),
                ("Cloudflare", "1.1.1.1"),
            ]:
                ms = ping_host(host)
                if ms > 0:
                    self._log_write(log, f"✓  {name:<12} {ms} ms")
                else:
                    self._log_write(log, f"✗  {name:<12} timeout")
                time.sleep(0.1)
            self._log_write(log, "✅ Готово!")

        threading.Thread(target=run, daemon=True).start()

    # ══════════════════════════════════════════════════════
    # ВКЛАДКА: СОВЕТЫ
    # ══════════════════════════════════════════════════════

    def _build_tab_tips(self, pad, g):
        """Вкладка с советами по оптимизации игры"""
        ctk.CTkLabel(
            pad, text="💡 Советы и хитрости",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w", pady=(0, 8))

        for ico, title, text in g["tips"]:
            card = ctk.CTkFrame(
                pad, fg_color=T("panel2"),
                corner_radius=10,
                border_width=1, border_color=T("border")
            )
            card.pack(fill="x", pady=2)
            ci = ctk.CTkFrame(card, fg_color="transparent")
            ci.pack(fill="x", padx=12, pady=7)
            ctk.CTkLabel(
                ci, text=f"{ico}  {title}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=T("accent")
            ).pack(anchor="w")
            ctk.CTkLabel(
                ci, text=text,
                font=ctk.CTkFont(size=10),
                text_color=T("text"),
                wraplength=680, justify="left"
            ).pack(anchor="w", pady=(2, 0))

    # ══════════════════════════════════════════════════════
    # ВКЛАДКА: CS2 КОНФИГ
    # ══════════════════════════════════════════════════════

    def _build_tab_cs2cfg(self, pad):
        """Вкладка с autoexec.cfg для CS2"""
        ctk.CTkLabel(
            pad, text="⚙️ autoexec.cfg для CS2",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w", pady=(0, 3))
        ctk.CTkLabel(
            pad,
            text="Кнопка «Сохранить в CS2» записывает прямо в папку игры.\n"
                 "Добавь в параметры запуска CS2: +exec autoexec",
            font=ctk.CTkFont(size=10),
            text_color=T("dim")
        ).pack(anchor="w", pady=(0, 8))

        # Текстовый редактор конфига
        tb = ctk.CTkTextbox(
            pad, height=300,
            fg_color=T("panel"),
            border_width=1, border_color=T("border"),
            font=ctk.CTkFont(family="Courier New", size=10),
            text_color=T("green"),
            corner_radius=10
        )
        tb.pack(fill="x", pady=(0, 8))
        tb.insert("end", CS2_AUTOEXEC_CONTENT)

        # Кнопки сохранения
        btn_row = ctk.CTkFrame(pad, fg_color="transparent")
        btn_row.pack(anchor="w")

        def save_to_cs2():
            path = expand(CS2_CFG_PATH)
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(tb.get("1.0", "end"))
                messagebox.showinfo(
                    "Сохранено!",
                    f"Файл записан:\n{path}\n\n"
                    "Добавь в параметры запуска CS2:\n"
                    "+exec autoexec"
                )
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        def save_to_downloads():
            path = os.path.join(os.path.expanduser("~"), "Downloads", "autoexec.cfg")
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(tb.get("1.0", "end"))
                messagebox.showinfo("Сохранено!", f"Файл сохранён:\n{path}")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        make_btn(
            btn_row, "💾  Сохранить в CS2",
            save_to_cs2, width=195
        ).pack(side="left", padx=(0, 6))
        make_btn(
            btn_row, "📁  В Downloads",
            save_to_downloads,
            color=T("panel2"), hover=T("panel"), width=155
        ).pack(side="left")

    # ══════════════════════════════════════════════════════
    # ВКЛАДКА: FIVEM
    # ══════════════════════════════════════════════════════

    def _build_tab_fivem(self, pad):
        """Вкладка FiveM оптимизации для GTA V"""
        ctk.CTkLabel(
            pad, text="🟣 FiveM оптимизация",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w", pady=(0, 3))
        ctk.CTkLabel(
            pad, text="Специальные твики для FiveM RP серверов",
            font=ctk.CTkFont(size=10),
            text_color=T("dim")
        ).pack(anchor="w", pady=(0, 8))

        for ico, name, desc, on_c, off_c in FIVEM_OPTS:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c)

        self._divider(pad)

        # Советы FiveM
        ctk.CTkLabel(
            pad, text="💡 Советы FiveM",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=T("accent")
        ).pack(anchor="w", pady=(0, 4))

        for ico, title, text in FIVEM_TIPS:
            card = ctk.CTkFrame(
                pad, fg_color=T("panel2"),
                corner_radius=8,
                border_width=1, border_color=T("border")
            )
            card.pack(fill="x", pady=2)
            ci = ctk.CTkFrame(card, fg_color="transparent")
            ci.pack(fill="x", padx=12, pady=6)
            ctk.CTkLabel(
                ci, text=f"{ico}  {title}",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=T("accent")
            ).pack(anchor="w")
            ctk.CTkLabel(
                ci, text=text,
                font=ctk.CTkFont(size=9),
                text_color=T("text"),
                wraplength=640
            ).pack(anchor="w")

    # ══════════════════════════════════════════════════════
    # ВКЛАДКА: LAUNCH ARGS
    # ══════════════════════════════════════════════════════

    def _build_tab_launch(self, pad, gname, g):
        """Вкладка с параметрами запуска Steam"""
        ctk.CTkLabel(
            pad, text="🔩 Параметры запуска Steam",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w", pady=(0, 3))
        ctk.CTkLabel(
            pad,
            text="Steam → ПКМ на игре → Свойства → Параметры запуска.\n"
                 "Выбери нужный пресет и скопируй строку.",
            font=ctk.CTkFont(size=10),
            text_color=T("dim")
        ).pack(anchor="w", pady=(0, 8))

        for pname, pdata in g["presets"].items():
            card = ctk.CTkFrame(
                pad, fg_color=T("panel2"),
                corner_radius=10,
                border_width=1, border_color=T("border")
            )
            card.pack(fill="x", pady=3)
            ci = ctk.CTkFrame(card, fg_color="transparent")
            ci.pack(fill="x", padx=12, pady=8)

            # Заголовок
            hr = ctk.CTkFrame(ci, fg_color="transparent")
            hr.pack(fill="x", pady=(0, 4))
            ctk.CTkLabel(
                hr, text=pname,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=T("text")
            ).pack(side="left")
            ctk.CTkLabel(
                hr, text=f"FPS: {pdata['fps']}",
                font=ctk.CTkFont(size=9),
                text_color=T("green")
            ).pack(side="right")

            # Поле с параметрами (редактируемое)
            tb = ctk.CTkTextbox(
                ci, height=36,
                fg_color=T("panel"),
                border_width=1, border_color=T("border"),
                font=ctk.CTkFont(family="Courier New", size=10),
                text_color=T("neon"), corner_radius=6
            )
            tb.pack(fill="x")
            tb.insert("end", pdata.get("launch", ""))

    # ══════════════════════════════════════════════════════
    # ЗАПУСК ИГРЫ
    # ══════════════════════════════════════════════════════

    def _launch_game(self, gname):
        """
        Запустить игру.
        ТОЛЬКО через Steam или Epic — никогда прямым exe!
        Прямой запуск exe блокируется EAC (Rust и другие).
        """
        g = GAMES[gname]

        if g.get("steam"):
            launch_via_steam(g["steam"])
            return

        if g.get("epic"):
            launch_via_epic(g["epic"])
            return

        messagebox.showinfo(
            "Запуск игры",
            f"Запусти {gname} вручную через Steam или Epic Games Launcher.\n\n"
            "Прямой запуск .exe не используется — "
            "это может заблокировать вход в игру через EAC."
        )

    # ══════════════════════════════════════════════════════
    # ПОЛНАЯ ОПТИМИЗАЦИЯ (кнопка ⚡ ВСЁ)
    # ══════════════════════════════════════════════════════

    def _full_optimize(self, gname):
        """Окно полной оптимизации — Windows + сеть + паразиты"""
        win = ctk.CTkToplevel(self)
        win.title(f"⚡ Полная оптимизация {gname}")
        win.geometry("540x420")
        win.configure(fg_color=T("bg"))
        win.lift()

        ctk.CTkLabel(
            win, text=f"⚡ Полная оптимизация {gname}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T("accent")
        ).pack(pady=(12, 5), padx=14, anchor="w")

        ctk.CTkLabel(
            win,
            text="Применяет: Windows твики + сеть + убивает все паразиты игры",
            font=ctk.CTkFont(size=10),
            text_color=T("dim")
        ).pack(padx=14, anchor="w", pady=(0, 8))

        log = ctk.CTkTextbox(
            win, height=300,
            fg_color=T("panel"),
            border_width=1, border_color=T("border"),
            font=ctk.CTkFont(family="Courier New", size=11),
            text_color=T("green"), corner_radius=10
        )
        log.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        log.configure(state="disabled")

        def w(text):
            log.configure(state="normal")
            log.insert("end", text + "\n")
            log.configure(state="disabled")
            log.see("end")

        def run():
            w(f"⚡ Начинаю полную оптимизацию для {gname}...")
            w("")

            # Windows оптимизации
            w("── Windows ─────────────────────────────────────")
            for name, cmd in WIN_ALL_STEPS:
                ok = run_cmd(cmd)
                w(f"  {'✓' if ok else '✗'} {name}")
                time.sleep(0.08)

            w("")
            w("── Паразиты игры ────────────────────────────────")
            self._kill_all_parasites(gname)
            time.sleep(0.8)

            w("")
            w("════════════════════════════════════════════════")
            w(f"✅ Готово! Запускай {gname}!")

        threading.Thread(target=run, daemon=True).start()


    # ══════════════════════════════════════════════════════
    # СТРАНИЦА: ПРОФИЛЬ ПК
    # ══════════════════════════════════════════════════════

    def _build_profile_page(self):
        """
        Страница профиля ПК.
        Показывает характеристики системы и живую нагрузку.
        Использует wmic и typeperf — работает без сторонних библиотек.
        """
        pad = self._make_page("profile")

        # Заголовок
        ctk.CTkLabel(
            pad, text="💻 Профиль ПК",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w", pady=(0, 3))
        ctk.CTkLabel(
            pad,
            text="Характеристики системы и нагрузка в реальном времени  •  F5 = обновить",
            font=ctk.CTkFont(size=10),
            text_color=T("dim")
        ).pack(anchor="w", pady=(0, 10))

        # ── Карточки характеристик ───────────────────────
        info_card = ctk.CTkFrame(
            pad, fg_color=T("panel"),
            corner_radius=12,
            border_width=1, border_color=T("border")
        )
        info_card.pack(fill="x", pady=(0, 10))

        ic_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        ic_inner.pack(fill="x", padx=14, pady=12)

        ctk.CTkLabel(
            ic_inner, text="🖥 Характеристики системы",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=T("accent")
        ).pack(anchor="w", pady=(0, 8))

        # Сетка 2 колонки
        info_grid = ctk.CTkFrame(ic_inner, fg_color="transparent")
        info_grid.pack(fill="x")
        info_grid.columnconfigure(0, weight=1)
        info_grid.columnconfigure(1, weight=1)

        fields = ["OS", "CPU", "RAM", "Диск C:", "GPU", "IP адрес"]
        for i, field in enumerate(fields):
            f = ctk.CTkFrame(
                info_grid, fg_color=T("panel2"),
                corner_radius=8,
                border_width=1, border_color=T("border")
            )
            f.grid(row=i // 2, column=i % 2, padx=3, pady=2, sticky="ew")
            fi = ctk.CTkFrame(f, fg_color="transparent")
            fi.pack(fill="x", padx=10, pady=6)

            ctk.CTkLabel(
                fi, text=field,
                font=ctk.CTkFont(size=9),
                text_color=T("dim")
            ).pack(anchor="w")

            lbl = ctk.CTkLabel(
                fi, text="Загружаю...",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=T("text")
            )
            lbl.pack(anchor="w")
            self.info_labels[field] = lbl

        # ── Живые показатели ─────────────────────────────
        self._divider(pad)
        ctk.CTkLabel(
            pad, text="📊 Нагрузка прямо сейчас",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w", pady=(0, 6))

        # 4 карточки: CPU / RAM / Disk / Temp
        stats_row = ctk.CTkFrame(pad, fg_color="transparent")
        stats_row.pack(fill="x", pady=(0, 8))
        for i in range(4):
            stats_row.columnconfigure(i, weight=1)

        stat_configs = [
            ("cpu",  "CPU %",    T("green")),
            ("ram",  "RAM %",    T("neon")),
            ("disk", "Диск %",   T("gold")),
            ("temp", "Темп °C",  T("accent")),
        ]
        for i, (key, label, color) in enumerate(stat_configs):
            f = ctk.CTkFrame(
                stats_row, fg_color=T("panel2"),
                corner_radius=10,
                border_width=1, border_color=T("border")
            )
            f.grid(row=0, column=i, padx=3, sticky="ew")
            v = ctk.CTkLabel(
                f, text="—",
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color=color
            )
            v.pack(pady=(9, 2))
            ctk.CTkLabel(
                f, text=label,
                font=ctk.CTkFont(size=9),
                text_color=T("dim")
            ).pack(pady=(0, 8))
            self.stat_boxes[key] = v

        # ── Прогресс бары ────────────────────────────────
        bars_card = ctk.CTkFrame(
            pad, fg_color=T("panel"),
            corner_radius=10,
            border_width=1, border_color=T("border")
        )
        bars_card.pack(fill="x", pady=(0, 8))
        bars_inner = ctk.CTkFrame(bars_card, fg_color="transparent")
        bars_inner.pack(fill="x", padx=12, pady=8)

        bar_configs = [
            ("cpu",  "CPU",   T("green")),
            ("ram",  "RAM",   T("neon")),
            ("disk", "ДИСК",  T("gold")),
        ]
        for key, label, color in bar_configs:
            row = ctk.CTkFrame(bars_inner, fg_color="transparent")
            row.pack(fill="x", pady=3)

            ctk.CTkLabel(
                row, text=label,
                font=ctk.CTkFont(size=9),
                text_color=T("dim"), width=38
            ).pack(side="left")

            bar = ctk.CTkProgressBar(
                row, height=12,
                progress_color=color,
                fg_color=T("panel2"),
                corner_radius=5
            )
            bar.set(0)
            bar.pack(side="left", fill="x", expand=True, padx=6)

            pct = ctk.CTkLabel(
                row, text="0%",
                font=ctk.CTkFont(size=9),
                text_color=color, width=32
            )
            pct.pack(side="left")
            self.prog_bars[key] = (bar, pct)

        # ── Пинг ─────────────────────────────────────────
        self._divider(pad)
        ctk.CTkLabel(
            pad, text="🌐 Пинг до серверов",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w", pady=(0, 6))

        ping_row = ctk.CTkFrame(pad, fg_color="transparent")
        ping_row.pack(fill="x", pady=(0, 8))
        ping_row.columnconfigure(0, weight=1)
        ping_row.columnconfigure(1, weight=1)

        self.ping_g = self._ping_stat_box(ping_row, "Google DNS  8.8.8.8",     0)
        self.ping_s = self._ping_stat_box(ping_row, "Steam серверы",            1)

        # ── Кнопки ───────────────────────────────────────
        btn_row = ctk.CTkFrame(pad, fg_color="transparent")
        btn_row.pack(anchor="w")

        make_btn(
            btn_row, "🔄  Обновить (F5)",
            self._refresh_profile, width=160
        ).pack(side="left", padx=(0, 6))

        make_btn(
            btn_row, "😂  Новая шутка",
            lambda: self.joke_lbl.configure(text=random.choice(JOKES)),
            color=T("panel2"), hover=T("panel"), width=140
        ).pack(side="left", padx=(0, 6))

        make_btn(
            btn_row, "⌨️  Горячие клавиши",
            self._show_hotkeys_help,
            color=T("panel2"), hover=T("panel"), width=155
        ).pack(side="left")

        # Запускаем фоновые потоки
        threading.Thread(target=self._load_profile_data, daemon=True).start()
        threading.Thread(target=self._live_stats_loop,   daemon=True).start()

    def _ping_stat_box(self, parent, label, col):
        """Виджет для отображения пинга"""
        f = ctk.CTkFrame(
            parent, fg_color=T("panel2"),
            corner_radius=8,
            border_width=1, border_color=T("border")
        )
        f.grid(row=0, column=col, padx=3, sticky="ew")
        fi = ctk.CTkFrame(f, fg_color="transparent")
        fi.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(
            fi, text=label,
            font=ctk.CTkFont(size=9),
            text_color=T("dim")
        ).pack(anchor="w")

        v = ctk.CTkLabel(
            fi, text="—",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=T("neon")
        )
        v.pack(anchor="w")
        return v

    # ── Загрузка статических данных системы ──────────────

    def _load_profile_data(self):
        """
        Загружает информацию о системе через wmic.
        Работает без psutil — только стандартные инструменты Windows.
        """
        # OS
        self._safe_set(
            self.info_labels["OS"],
            platform.system() + " " + platform.release()
        )

        # CPU — через wmic
        cpu = run_cmd_out("wmic cpu get Name /value").replace("Name=", "").strip()
        # Убираем дубликаты (wmic иногда возвращает двойную строку)
        cpu_lines = [l for l in cpu.splitlines() if l.strip()]
        cpu = cpu_lines[0] if cpu_lines else "—"
        if len(cpu) > 44:
            cpu = cpu[:44] + "..."
        self._safe_set(self.info_labels["CPU"], cpu or "—")

        # RAM — общий объём
        try:
            raw = run_cmd_out(
                "wmic computersystem get TotalPhysicalMemory /value"
            ).replace("TotalPhysicalMemory=", "").strip()
            # Берём только первую строку с числом
            for line in raw.splitlines():
                if line.strip().isdigit():
                    rb = int(line.strip())
                    self._safe_set(
                        self.info_labels["RAM"],
                        str(round(rb / 1024 ** 3, 1)) + " GB"
                    )
                    break
        except Exception:
            self._safe_set(self.info_labels["RAM"], "—")

        # Диск C: — свободно / всего
        try:
            raw = run_cmd_out(
                'wmic logicaldisk where DeviceID="C:" get FreeSpace,Size /value'
            )
            d = {}
            for line in raw.splitlines():
                if "=" in line:
                    parts = line.split("=", 1)
                    if len(parts) == 2 and parts[1].strip().isdigit():
                        d[parts[0].strip()] = int(parts[1].strip())
            free  = d.get("FreeSpace", 0) // 1024 ** 3
            total = d.get("Size", 0)      // 1024 ** 3
            self._safe_set(
                self.info_labels["Диск C:"],
                f"{free} GB свободно / {total} GB"
            )
        except Exception:
            self._safe_set(self.info_labels["Диск C:"], "—")

        # GPU — через wmic
        gpu = run_cmd_out(
            "wmic path win32_videocontroller get Name /value"
        ).replace("Name=", "").strip()
        gpu_lines = [l for l in gpu.splitlines() if l.strip()]
        gpu = gpu_lines[0] if gpu_lines else "—"
        if len(gpu) > 44:
            gpu = gpu[:44] + "..."
        self._safe_set(self.info_labels["GPU"], gpu or "—")

        # IP адрес — через сокет
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
        except Exception:
            ip = "—"
        self._safe_set(self.info_labels["IP адрес"], ip)

        # Пинг до Google и Steam
        ms_g = ping_host("8.8.8.8")
        ms_s = ping_host("store.steampowered.com")

        if self.ping_g:
            self._safe_set(
                self.ping_g,
                (str(ms_g) + " ms") if ms_g > 0 else "timeout"
            )
        if self.ping_s:
            self._safe_set(
                self.ping_s,
                (str(ms_s) + " ms") if ms_s > 0 else "timeout"
            )

    def _refresh_profile(self):
        """Сбросить и перезагрузить данные профиля"""
        for lbl in self.info_labels.values():
            self._safe_set(lbl, "Обновляю...")
        threading.Thread(target=self._load_profile_data, daemon=True).start()

    # ── Живой мониторинг нагрузки ─────────────────────────

    def _live_stats_loop(self):
        """Основной цикл обновления живых показателей (каждые 2 сек)"""
        while self._live_running:
            self._update_live_stats()
            time.sleep(2)

    def _update_live_stats(self):
        """
        Обновляет CPU / RAM / Disk / Temp.
        Все данные через wmic и typeperf — без psutil.
        """
        # ── CPU % через typeperf ──────────────────────────
        try:
            r = subprocess.run(
                'typeperf "\\Processor(_Total)\\% Processor Time" -sc 1',
                shell=True, capture_output=True, text=True,
                timeout=5, encoding="cp1251", errors="replace"
            )
            # typeperf возвращает строку вида: "timestamp","value"
            lines = [
                l for l in r.stdout.splitlines()
                if "," in l
                and "%" not in l
                and "Time" not in l
                and l.strip()
            ]
            if lines:
                raw_val = lines[0].split(",")[1].replace('"', '').strip()
                val = int(float(raw_val))
                color = T("green") if val < 50 else T("gold") if val < 80 else T("accent")
                self._safe_set(self.stat_boxes["cpu"], f"{val}%")
                self.stat_boxes["cpu"].configure(text_color=color)
                self.prog_bars["cpu"][0].set(val / 100)
                self.prog_bars["cpu"][1].configure(text=f"{val}%")
        except Exception:
            pass

        # ── RAM % через wmic ──────────────────────────────
        try:
            raw = run_cmd_out(
                "wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /value"
            )
            d = {}
            for line in raw.splitlines():
                if "=" in line:
                    parts = line.split("=", 1)
                    if len(parts) == 2 and parts[1].strip().isdigit():
                        d[parts[0].strip()] = int(parts[1].strip())
            free_kb  = d.get("FreePhysicalMemory",      0)
            total_kb = d.get("TotalVisibleMemorySize", 1)
            val = int((1 - free_kb / total_kb) * 100)
            color = T("green") if val < 60 else T("gold") if val < 80 else T("accent")
            self._safe_set(self.stat_boxes["ram"], f"{val}%")
            self.stat_boxes["ram"].configure(text_color=color)
            self.prog_bars["ram"][0].set(val / 100)
            self.prog_bars["ram"][1].configure(text=f"{val}%")
        except Exception:
            pass

        # ── Disk C: % через wmic ──────────────────────────
        try:
            raw = run_cmd_out(
                'wmic logicaldisk where DeviceID="C:" get FreeSpace,Size /value'
            )
            d3 = {}
            for line in raw.splitlines():
                if "=" in line:
                    parts = line.split("=", 1)
                    if len(parts) == 2 and parts[1].strip().isdigit():
                        d3[parts[0].strip()] = int(parts[1].strip())
            free_b  = d3.get("FreeSpace", 0)
            total_b = d3.get("Size",      1)
            val = int((1 - free_b / total_b) * 100)
            self._safe_set(self.stat_boxes["disk"], f"{val}%")
            self.prog_bars["disk"][0].set(val / 100)
            self.prog_bars["disk"][1].configure(text=f"{val}%")
        except Exception:
            pass

        # ── Температура CPU через WMI ─────────────────────
        try:
            raw = run_cmd_out(
                "wmic /namespace:\\\\root\\wmi "
                "PATH MSAcpi_ThermalZoneTemperature "
                "get CurrentTemperature /value"
            )
            temps = []
            for line in raw.splitlines():
                if "CurrentTemperature=" in line:
                    try:
                        # Температура хранится в Kelvin * 10
                        kelvin_x10 = int(line.split("=")[1].strip())
                        celsius = (kelvin_x10 - 2732) / 10.0
                        if 0 < celsius < 120:   # фильтруем мусорные значения
                            temps.append(celsius)
                    except Exception:
                        pass
            if temps:
                val = int(sum(temps) / len(temps))
                color = T("green") if val < 60 else T("gold") if val < 80 else T("accent")
                self._safe_set(self.stat_boxes["temp"], f"{val}°")
                self.stat_boxes["temp"].configure(text_color=color)
            else:
                # WMI не поддерживает температуру на этой системе
                self._safe_set(self.stat_boxes["temp"], "N/A")
        except Exception:
            self._safe_set(self.stat_boxes["temp"], "N/A")

    # ══════════════════════════════════════════════════════
    # СТРАНИЦА: WINDOWS ОПТИМИЗАЦИИ
    # ══════════════════════════════════════════════════════

    def _build_windows_page(self):
        """
        Страница системных оптимизаций Windows.
        Тогл вправо = включить оптимизацию, влево = вернуть как было.
        """
        pad = self._make_page("windows")

        ctk.CTkLabel(
            pad, text="⚡ Оптимизация Windows",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w", pady=(0, 3))
        ctk.CTkLabel(
            pad,
            text="Системные твики для максимального FPS в любой игре.  "
                 "Тогл вправо = включить, влево = вернуть как было.",
            font=ctk.CTkFont(size=10),
            text_color=T("dim")
        ).pack(anchor="w", pady=(0, 8))

        # Все оптимизации Windows
        for ico, name, desc, on_c, off_c in WIN_OPTS:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c)

        self._divider(pad)

        # Кнопка применить всё
        apply_btn = ctk.CTkButton(
            pad,
            text="⚡  ПРИМЕНИТЬ ВСЕ ОПТИМИЗАЦИИ WINDOWS",
            command=self._run_all_windows,
            fg_color=T("accent"),
            hover_color=T("accent2"),
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=12, height=40
        )
        apply_btn.pack(fill="x", pady=(0, 4))

        make_btn(
            pad, "🔄  Сбросить всё (вернуть как было)",
            self._reset_windows,
            color=T("panel2"), hover=T("panel"),
            size=11
        ).pack(fill="x")

        self.win_log = self._make_log(pad, 110)

    def _run_all_windows(self):
        """Применить все Windows оптимизации одним нажатием"""
        self._log_clear(self.win_log)
        self._log_write(self.win_log, "⚡ Применяю все оптимизации Windows...")

        def run():
            for name, cmd in WIN_ALL_STEPS:
                ok = run_cmd(cmd)
                self._log_write(
                    self.win_log,
                    f"  {'✓' if ok else '✗'} {name}"
                )
                time.sleep(0.07)
            self._log_write(self.win_log, "")
            self._log_write(self.win_log, "✅ Готово! Рекомендуем перезагрузить ПК.")

        threading.Thread(target=run, daemon=True).start()

    def _reset_windows(self):
        """Вернуть Windows настройки к стандартным"""
        self._log_clear(self.win_log)
        self._log_write(self.win_log, "🔄 Сбрасываю настройки...")

        reset_steps = [
            ("⚡ Балансированный план питания",
             "powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e"),
            ("📈 Стандартный приоритет Win32",
             'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" '
             "/v Win32PrioritySeparation /t REG_DWORD /d 2 /f"),
            ("🔍 Запустить Windows Search",
             "net start wsearch"),
            ("📊 Запустить SysMain",
             "net start sysmain"),
            ("⏸ Запустить Windows Update",
             "net start wuauserv"),
        ]

        def run():
            for name, cmd in reset_steps:
                ok = run_cmd(cmd)
                self._log_write(
                    self.win_log,
                    f"  {'✓' if ok else '✗'} {name}"
                )
                time.sleep(0.1)
            self._log_write(self.win_log, "")
            self._log_write(self.win_log, "✅ Настройки сброшены.")

        threading.Thread(target=run, daemon=True).start()

    # ══════════════════════════════════════════════════════
    # СТРАНИЦА: НАСТРОЙКА СЕТИ
    # ══════════════════════════════════════════════════════

    def _build_network_page(self):
        """
        Страница сетевых оптимизаций.
        DNS, Nagle, QoS, IPv6, Winsock сброс и другие твики.
        """
        pad = self._make_page("network")

        ctk.CTkLabel(
            pad, text="🌐 Настройка сети",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w", pady=(0, 3))
        ctk.CTkLabel(
            pad,
            text="Оптимизация пинга и стабильности соединения для всех онлайн игр",
            font=ctk.CTkFont(size=10),
            text_color=T("dim")
        ).pack(anchor="w", pady=(0, 8))

        # Все сетевые оптимизации
        for ico, name, desc, on_c, off_c in NET_OPTS:
            self._compact_toggle(pad, ico, name, desc, on_c, off_c)

        self._divider(pad)

        # Кнопки внизу
        btn_row = ctk.CTkFrame(pad, fg_color="transparent")
        btn_row.pack(anchor="w", pady=(0, 4))

        make_btn(
            btn_row, "📡  Проверить пинг",
            self._run_global_ping, width=200
        ).pack(side="left", padx=(0, 6))

        make_btn(
            btn_row, "🔄  Сброс Winsock + DNS",
            self._reset_network,
            color=T("panel2"), hover=T("panel"), width=200
        ).pack(side="left")

        self.net_log = self._make_log(pad, 120)

    def _run_global_ping(self):
        """Проверить пинг до всех серверов из списка"""
        self._log_clear(self.net_log)

        def run():
            self._log_write(self.net_log, "📡 Проверяю серверы...")
            for name, host in PING_SERVERS:
                ms = ping_host(host)
                if ms > 0:
                    status = "OK ✓" if ms < 80 else ("СРЕДНИЙ" if ms < 150 else "ВЫСОКИЙ ⚠")
                    self._log_write(
                        self.net_log,
                        f"  {name:<16} {str(ms) + ' ms':>8}   {status}"
                    )
                else:
                    self._log_write(
                        self.net_log,
                        f"  {name:<16} {'timeout':>8}   ✗"
                    )
                time.sleep(0.1)
            self._log_write(self.net_log, "")
            self._log_write(self.net_log, "✅ Готово!")

        threading.Thread(target=run, daemon=True).start()

    def _reset_network(self):
        """Полный сброс сетевого стека"""
        self._log_clear(self.net_log)
        self._log_write(self.net_log, "🔄 Сбрасываю сетевой стек...")

        cmds = [
            ("Сброс Winsock",         "netsh winsock reset"),
            ("Сброс IP стека",        "netsh int ip reset"),
            ("Очистка DNS кэша",      "ipconfig /flushdns"),
            ("Регистрация DNS",       "ipconfig /registerdns"),
        ]

        def run():
            for name, cmd in cmds:
                ok = run_cmd(cmd)
                self._log_write(
                    self.net_log,
                    f"  {'✓' if ok else '✗'} {name}"
                )
                time.sleep(0.2)
            self._log_write(self.net_log, "")
            self._log_write(
                self.net_log,
                "✅ Готово! Перезагрузи ПК для полного применения."
            )

        threading.Thread(target=run, daemon=True).start()

    # ══════════════════════════════════════════════════════
    # СТРАНИЦА: МОНИТОРИНГ ПИНГА
    # ══════════════════════════════════════════════════════

    def _build_monitor_page(self):
        """
        Страница живого мониторинга пинга.
        График в реальном времени, статистика, серверы.
        """
        pad = self._make_page("monitor")

        ctk.CTkLabel(
            pad, text="📊 Мониторинг пинга",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=T("text")
        ).pack(anchor="w", pady=(0, 3))
        ctk.CTkLabel(
            pad,
            text="Живой замер задержки до игровых серверов в реальном времени",
            font=ctk.CTkFont(size=10),
            text_color=T("dim")
        ).pack(anchor="w", pady=(0, 8))

        # ── Статистика: текущий / средний / максимум ─────
        stats_row = ctk.CTkFrame(pad, fg_color="transparent")
        stats_row.pack(fill="x", pady=(0, 8))
        for i in range(3):
            stats_row.columnconfigure(i, weight=1)

        self.ms_cur = self._monitor_stat_box(stats_row, "Текущий ms",  T("green"),   0)
        self.ms_avg = self._monitor_stat_box(stats_row, "Средний ms",  T("gold"),    1)
        self.ms_max = self._monitor_stat_box(stats_row, "Максимум ms", T("accent"),  2)

        # ── Управление ───────────────────────────────────
        ctrl = ctk.CTkFrame(pad, fg_color="transparent")
        ctrl.pack(fill="x", pady=(0, 8))

        self.mon_btn = make_btn(
            ctrl, "▶  Запустить мониторинг",
            self._toggle_monitor, width=200
        )
        self.mon_btn.pack(side="left")

        self.mon_lbl = ctk.CTkLabel(
            ctrl, text="● Остановлен",
            text_color=T("dim"),
            font=ctk.CTkFont(size=10)
        )
        self.mon_lbl.pack(side="left", padx=10)

        ctk.CTkLabel(
            ctrl, text="Интервал:",
            text_color=T("dim"),
            font=ctk.CTkFont(size=10)
        ).pack(side="left")

        self.mon_int = ctk.CTkComboBox(
            ctrl,
            values=["2 сек", "5 сек", "10 сек"],
            width=85,
            fg_color=T("panel2"),
            border_color=T("border")
        )
        self.mon_int.set("2 сек")
        self.mon_int.pack(side="left", padx=6)

        # ── Серверы ──────────────────────────────────────
        servers_to_monitor = [
            ("Steam",      "store.steampowered.com"),
            ("Cloudflare", "1.1.1.1"),
            ("Google DNS", "8.8.8.8"),
            ("Faceit",     "api.faceit.com"),
        ]
        for srv_name, srv_host in servers_to_monitor:
            row = ctk.CTkFrame(
                pad, fg_color=T("panel2"),
                corner_radius=8,
                border_width=1, border_color=T("border")
            )
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(
                row, text="●",
                font=ctk.CTkFont(size=11),
                text_color=T("dim")
            ).pack(side="left", padx=(10, 6), pady=8)

            ctk.CTkLabel(
                row, text=srv_name,
                font=ctk.CTkFont(size=11),
                text_color=T("text"), width=122
            ).pack(side="left")

            lbl = ctk.CTkLabel(
                row, text="— ms",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=T("dim")
            )
            lbl.pack(side="right", padx=14)
            self.srv_lbls[srv_host] = lbl

        # ── График ───────────────────────────────────────
        chart_card = ctk.CTkFrame(
            pad, fg_color=T("panel2"),
            corner_radius=12,
            border_width=1, border_color=T("border")
        )
        chart_card.pack(fill="x", pady=6)

        chart_header = ctk.CTkFrame(chart_card, fg_color="transparent")
        chart_header.pack(fill="x", padx=12, pady=(8, 2))
        ctk.CTkLabel(
            chart_header, text="📈 График пинга (последние 30 замеров)",
            font=ctk.CTkFont(size=10),
            text_color=T("dim")
        ).pack(side="left")
        ctk.CTkLabel(
            chart_header, text="─ ─  100ms",
            font=ctk.CTkFont(size=9),
            text_color=T("border")
        ).pack(side="right")

        # Используем tkinter.Canvas — НЕ CTkCanvas (он не существует в customtkinter)
        self.chart = tkinter.Canvas(
            chart_card, height=100,
            bg=T("panel"), highlightthickness=0
        )
        self.chart.pack(fill="x", padx=8, pady=(0, 8))

    def _monitor_stat_box(self, parent, label, color, col):
        """Карточка статистики мониторинга"""
        f = ctk.CTkFrame(
            parent, fg_color=T("panel2"),
            corner_radius=10,
            border_width=1, border_color=T("border")
        )
        f.grid(row=0, column=col, padx=3, sticky="ew")
        v = ctk.CTkLabel(
            f, text="—",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=color
        )
        v.pack(pady=(9, 2))
        ctk.CTkLabel(
            f, text=label,
            font=ctk.CTkFont(size=9),
            text_color=T("dim")
        ).pack(pady=(0, 8))
        return v

    # ── Управление мониторингом ───────────────────────────

    def _toggle_monitor(self):
        """Запустить или остановить мониторинг пинга"""
        if self.monitor_running:
            self.monitor_running = False
            self.mon_btn.configure(
                text="▶  Запустить мониторинг",
                fg_color=T("accent"),
                hover_color=T("accent2")
            )
            self.mon_lbl.configure(text="● Остановлен", text_color=T("dim"))
        else:
            self.monitor_running = True
            self.mon_btn.configure(
                text="⏹  Остановить",
                fg_color=T("panel2"),
                hover_color=T("panel")
            )
            self.mon_lbl.configure(text="● Активен", text_color=T("green"))
            threading.Thread(target=self._monitor_loop, daemon=True).start()

    def _monitor_loop(self):
        """Основной цикл мониторинга пинга"""
        while self.monitor_running:
            # Интервал опроса
            interval_map = {"2 сек": 2, "5 сек": 5, "10 сек": 10}
            iv = interval_map.get(self.mon_int.get(), 2)

            servers = [
                ("Steam",      "store.steampowered.com"),
                ("Cloudflare", "1.1.1.1"),
                ("Google DNS", "8.8.8.8"),
                ("Faceit",     "api.faceit.com"),
            ]

            results = []
            for _, host in servers:
                ms = ping_host(host)
                results.append(ms)

                lbl = self.srv_lbls.get(host)
                if lbl:
                    if ms < 0:
                        lbl.configure(text="timeout", text_color=T("accent"))
                    else:
                        color = T("green") if ms < 80 else T("gold") if ms < 150 else T("accent")
                        lbl.configure(text=f"{ms} ms", text_color=color)

            # Обновляем статистику
            valid = [r for r in results if r >= 0]
            if valid:
                avg = sum(valid) // len(valid)
                self.ping_history.append(avg)
                if len(self.ping_history) > 30:
                    self.ping_history.pop(0)

                # Цвет текущего пинга
                cur_color = (
                    T("green") if avg < 80
                    else T("gold")  if avg < 150
                    else T("accent")
                )
                if self.ms_cur:
                    self.ms_cur.configure(text=str(avg), text_color=cur_color)
                if self.ms_avg:
                    avg_all = sum(self.ping_history) // len(self.ping_history)
                    self.ms_avg.configure(text=str(avg_all))
                if self.ms_max:
                    self.ms_max.configure(text=str(max(self.ping_history)))

                # Обновляем график
                self._draw_ping_chart()

            time.sleep(iv)

    def _draw_ping_chart(self):
        """
        Рисует график пинга на tkinter.Canvas.
        Зелёный = < 80ms, Жёлтый = < 150ms, Красный = > 150ms.
        Пунктирная линия = 100ms.
        """
        c = self.chart
        c.delete("all")

        if len(self.ping_history) < 2:
            return

        W = c.winfo_width() or 520
        H = 100
        max_val = max(max(self.ping_history), 200)
        padding = 10

        # Вычисляем координаты точек
        points = []
        for i, val in enumerate(self.ping_history):
            x = int(
                padding + (i / (len(self.ping_history) - 1)) * (W - padding * 2)
            )
            y = int(H - padding - (val / max_val) * (H - padding * 2))
            points.append((x, y))

        # Заливка под графиком
        last_val = self.ping_history[-1]
        r_col, g_col, b_col = (
            (0, 255, 136)  if last_val < 80
            else (255, 204, 68) if last_val < 150
            else (255, 34, 68)
        )
        # Делаем полупрозрачный цвет заливки (тёмный)
        fill_color = "#{:02x}{:02x}{:02x}".format(
            r_col // 8, g_col // 8, b_col // 8
        )

        poly_pts = [(padding, H - padding)] + points + [(points[-1][0], H - padding)]
        c.create_polygon(
            [coord for pt in poly_pts for coord in pt],
            fill=fill_color, outline=""
        )

        # Пунктирная линия 100ms
        ref_y = int(H - padding - (100 / max_val) * (H - padding * 2))
        if 0 < ref_y < H:
            c.create_line(
                padding, ref_y, W - padding, ref_y,
                fill=T("border"), dash=(4, 4)
            )
            c.create_text(
                W - padding - 2, ref_y - 8,
                text="100ms", fill=T("dim"),
                font=("Courier", 8), anchor="e"
            )

        # Основная линия графика
        line_color = "#{:02x}{:02x}{:02x}".format(r_col, g_col, b_col)
        c.create_line(
            [coord for pt in points for coord in pt],
            fill=line_color, width=2, smooth=True
        )

        # Точка последнего значения
        if points:
            lx, ly = points[-1]
            c.create_oval(lx - 3, ly - 3, lx + 3, ly + 3,
                          fill=line_color, outline="")

    # ══════════════════════════════════════════════════════
    # УТИЛИТЫ ПРИЛОЖЕНИЯ
    # ══════════════════════════════════════════════════════

    def on_closing(self):
        """Корректное закрытие приложения"""
        self._live_running    = False
        self.monitor_running  = False
        self.destroy()


# ══════════════════════════════════════════════════════════
# ТОЧКА ВХОДА
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


# ══════════════════════════════════════════════════════════
# СКРИПТ СБОРКИ — сохрани как build.py и запусти
# ══════════════════════════════════════════════════════════
"""
КАК СОБРАТЬ ОДИН ФАЙЛ ИЗ 4 ЧАСТЕЙ:

Вариант А — Windows CMD:
    copy /b GameOptimizer_part1.py+GameOptimizer_part2.py+GameOptimizer_part3.py+GameOptimizer_part4.py GameOptimizer.py

Вариант Б — Python build.py:
    # Сохрани этот код в build.py рядом с файлами частей:
    parts = [
        'GameOptimizer_part1.py',
        'GameOptimizer_part2.py',
        'GameOptimizer_part3.py',
        'GameOptimizer_part4.py',
    ]
    with open('GameOptimizer.py', 'w', encoding='utf-8') as out:
        for part in parts:
            with open(part, encoding='utf-8') as f:
                content = f.read()
                # Убираем docstring из 2-4 частей
                out.write(content)
                out.write('\\n')
    print('Готово! GameOptimizer.py собран.')

Вариант В — GitHub Actions (build.yml):
    - name: Assemble parts
      run: |
        Get-Content part1.py,part2.py,part3.py,part4.py | Set-Content GameOptimizer.py
      shell: pwsh

    - name: Build exe
      run: |
        pip install pyinstaller customtkinter
        pyinstaller --onefile --windowed --name GameOptimizer GameOptimizer.py
"""
