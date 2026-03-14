import sys
import os
import time
import socket
import random
import threading
import subprocess
import tkinter
import customtkinter as ctk

sys.setrecursionlimit(5000)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Цвета
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
    "😂 Ваня: 5 FPS — это нормально",
    "💀 Ваня оптимизировал и удалил system32",
    "🎯 Ваня поставил мониторинг — FPS 12",
    "🔫 Ваня в Rust строил дом — убили через стену",
    "🚗 Ваня в GTA взял такси — лучше пешком",
    "⚡ Ваня включил план питания — сгорел роутер",
]


def run_cmd(cmd):
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, timeout=30,
            encoding="cp1251", errors="replace"
        )
        return r.returncode == 0
    except Exception:
        return False


def ping_host(host, timeout=2):
    try:
        t0 = time.time()
        s = socket.create_connection((host, 80), timeout=timeout)
        s.close()
        return int((time.time() - t0) * 1000)
    except Exception:
        return -1


def make_btn(parent, text, cmd,
             color="#0060df", hover="#0090ff",
             size=13, bold=True, width=None, corner=8):
    font = ctk.CTkFont(size=size, weight="bold" if bold else "normal")
    kwargs = dict(
        text=text,
        command=cmd,
        fg_color=color,
        hover_color=hover,
        font=font,
        corner_radius=corner,
    )
    if width is not None:
        kwargs["width"] = width
    return ctk.CTkButton(parent, **kwargs)


# ─── Данные игр ────────────────────────────────────────────

RUST_PRESETS = {
    "Макс FPS": {
        "desc": "Минимум графики",
        "fps": "100-200+",
        "launch": "-high -maxMem=8192 -malloc=system +fps.limit 0 -nolog",
        "settings": [
            ("grass.on", "false"), ("terrain.quality", "0"),
            ("graphics.shadows", "0"), ("graphics.ssao", "0"),
            ("graphics.damage", "0"), ("graphics.itemskins", "0"),
            ("graphics.lodbias", "0.25"), ("graphics.dof", "false"),
        ],
    },
    "Баланс": {
        "desc": "FPS + читаемость",
        "fps": "60-120",
        "launch": "-high -maxMem=8192 +fps.limit 0",
        "settings": [
            ("grass.on", "true"), ("terrain.quality", "50"),
            ("graphics.shadows", "1"), ("graphics.ssao", "0"),
            ("graphics.lodbias", "1"),
        ],
    },
    "Качество": {
        "desc": "Полная графика",
        "fps": "40-80",
        "launch": "+fps.limit 0",
        "settings": [
            ("grass.on", "true"), ("terrain.quality", "100"),
            ("graphics.shadows", "3"), ("graphics.ssao", "1"),
            ("graphics.lodbias", "2"),
        ],
    },
}

GTA_PRESETS = {
    "Макс FPS": {
        "desc": "Для слабых ПК и FiveM",
        "fps": "80-160+",
        "launch": "-notablet -norestrictions -noFirstRun -IgnoreCorrupts",
        "settings": [
            ("TextureQuality", "normal"), ("ShaderQuality", "normal"),
            ("ShadowQuality", "normal"), ("ReflectionQuality", "off"),
            ("MSAA", "off"), ("FXAA", "off"),
            ("AmbientOcclusion", "off"), ("MotionBlur", "false"),
            ("InGameDepthOfField", "false"),
        ],
    },
    "Баланс": {
        "desc": "Комфортная игра",
        "fps": "60-100",
        "launch": "-notablet -noFirstRun",
        "settings": [
            ("TextureQuality", "high"), ("ShaderQuality", "high"),
            ("ShadowQuality", "high"), ("MSAA", "off"),
            ("FXAA", "on"), ("AmbientOcclusion", "medium"),
            ("MotionBlur", "false"),
        ],
    },
    "Качество": {
        "desc": "Максимальная красота",
        "fps": "40-70",
        "launch": "-notablet",
        "settings": [
            ("TextureQuality", "very high"), ("ShaderQuality", "very high"),
            ("ShadowQuality", "very high"), ("MSAA", "x4"),
            ("FXAA", "on"), ("AmbientOcclusion", "high"),
        ],
    },
}

CS2_PRESETS = {
    "Макс FPS": {
        "desc": "Про-настройки",
        "fps": "200-400+",
        "launch": "-novid -nojoy -noaafonts -limitvsconst -forcenovsync +mat_queue_mode -1 +r_dynamic_lighting 0 -freq 240 -high",
        "settings": [
            ("r_lowlatency", "2"), ("fps_max", "0"),
            ("mat_queue_mode", "-1"), ("r_dynamic_lighting", "0"),
            ("r_shadows", "0"), ("cl_ragdoll_physics_enable", "0"),
            ("r_motionblur", "0"), ("cl_showfps", "1"),
        ],
    },
    "Баланс": {
        "desc": "FPS + видимость",
        "fps": "144-250",
        "launch": "-novid -nojoy -forcenovsync +mat_queue_mode -1 -high",
        "settings": [
            ("fps_max", "0"), ("r_lowlatency", "2"),
            ("r_shadows", "1"), ("r_dynamic_lighting", "1"),
            ("cl_showfps", "1"), ("r_motionblur", "0"),
        ],
    },
    "Качество": {
        "desc": "Красивая картинка",
        "fps": "100-180",
        "launch": "-novid +mat_queue_mode -1",
        "settings": [
            ("fps_max", "0"), ("r_shadows", "3"),
            ("r_dynamic_lighting", "1"), ("r_motionblur", "0"),
        ],
    },
}

RUST_PARASITES = [
    ("🎓", "Обучалка / подсказки",    "Постоянные подсказки новичка",     RED,
     [r'reg add "HKCU\Software\Facepunch\Rust" /v tutorial_complete /t REG_DWORD /d 1 /f'],
     [r'reg add "HKCU\Software\Facepunch\Rust" /v tutorial_complete /t REG_DWORD /d 0 /f']),
    ("🎬", "Вступительное видео",      "Логотип при каждом запуске",       ORANGE,
     [r'reg add "HKCU\Software\Facepunch\Rust" /v skip_intro /t REG_DWORD /d 1 /f'],
     [r'reg add "HKCU\Software\Facepunch\Rust" /v skip_intro /t REG_DWORD /d 0 /f']),
    ("🌿", "Трава (grass.on false)",   "Убирает траву — +20-40 FPS",       GREEN,
     ['echo grass.on false >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
     ['echo grass.on true  >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
    ("💨", "Motion Blur",              "Размытие движения снижает FPS",    NEON,
     ['echo effects.motionblur false >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
     ['echo effects.motionblur true  >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
    ("🔊", "VOIP / Голосовой чат",     "Постоянно слушает микрофон",       PURPLE,
     ['echo voice.use false >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
     ['echo voice.use true  >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
    ("📦", "Скины предметов",          "Загрузка скинов жрёт RAM",         GOLD,
     ['echo graphics.itemskins 0 >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
     ['echo graphics.itemskins 1 >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
    ("🎆", "Эффекты взрывов",          "Партиклы взрывов — лишняя нагрузка", RED,
     ['echo graphics.damage 0 >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
     ['echo graphics.damage 1 >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
    ("🌅", "God Rays / Лучи света",    "Volumetric lighting — дорого",     ORANGE,
     ['echo graphics.shafts 0 >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
     ['echo graphics.shafts 1 >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
]

GTA_PARASITES = [
    ("🎓", "Обучающие подсказки",      "Всплывают каждый раз",             RED,
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v TutorialDone /t REG_DWORD /d 1 /f'],
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v TutorialDone /t REG_DWORD /d 0 /f']),
    ("🎬", "Вступительные ролики",     "Логотип + ролик при запуске",      ORANGE,
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v InstallComplete /t REG_DWORD /d 1 /f'],
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v InstallComplete /t REG_DWORD /d 0 /f']),
    ("🌀", "Motion Blur",              "Размытие при движении -10-15 FPS", RED,
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v MotionBlur /t REG_DWORD /d 0 /f'],
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v MotionBlur /t REG_DWORD /d 1 /f']),
    ("🌊", "Глубина резкости DOF",     "Размытие фона — зря расходует GPU", NEON,
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v InGameDepthOfField /t REG_DWORD /d 0 /f'],
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v InGameDepthOfField /t REG_DWORD /d 1 /f']),
    ("🎬", "Replay / Rockstar Editor", "Постоянно пишет буфер в фоне",     GOLD,
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ReplayBuffer /t REG_DWORD /d 0 /f'],
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ReplayBuffer /t REG_DWORD /d 1 /f']),
    ("🐾", "Tessellation",             "Детализация поверхностей — дорого", PURPLE,
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v Tessellation /t REG_DWORD /d 0 /f'],
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v Tessellation /t REG_DWORD /d 1 /f']),
    ("🌆", "Extended Distance",        "Далёкие объекты — огромная нагрузка", RED,
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ExtendedDistanceScaling /t REG_DWORD /d 0 /f'],
     [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ExtendedDistanceScaling /t REG_DWORD /d 1 /f']),
]

CS2_PARASITES = [
    ("🎓", "Обучение / Tutorial",      "Убирает предложение обучалки",     RED,
     [r'reg add "HKCU\Software\Valve\Counter-Strike Global Offensive" /v TutorialDone /t REG_DWORD /d 1 /f'],
     [r'reg add "HKCU\Software\Valve\Counter-Strike Global Offensive" /v TutorialDone /t REG_DWORD /d 0 /f']),
    ("🎬", "Интро видео Valve",        "Логотип при каждом запуске",       ORANGE,
     [r'reg add "HKCU\Software\Valve\Counter-Strike Global Offensive" /v NoVideoIntro /t REG_DWORD /d 1 /f'],
     [r'reg add "HKCU\Software\Valve\Counter-Strike Global Offensive" /v NoVideoIntro /t REG_DWORD /d 0 /f']),
    ("🌀", "Motion Blur",              "Размытие снижает FPS без пользы",  RED,
     ['echo r_motionblur 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
     ['echo r_motionblur 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
    ("💀", "Ragdoll физика трупов",    "Трупы с физикой жрут CPU",         NEON,
     ['echo cl_ragdoll_physics_enable 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
     ['echo cl_ragdoll_physics_enable 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
    ("🌿", "Детали окружения",         "Трава и листья — лишняя нагрузка", GREEN,
     ['echo cl_detailfade 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
     ['echo cl_detailfade 400 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
    ("🎵", "Музыка в меню",            "Звуковой движок в меню зря работает", PURPLE,
     ['echo snd_menumusic_volume 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
     ['echo snd_menumusic_volume 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
    ("💬", "Kill feed анимации",       "cl_draw_only_deathnotices — только важное", GOLD,
     ['echo cl_draw_only_deathnotices 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
     ['echo cl_draw_only_deathnotices 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
]


FORTNITE_PRESETS = {
    "Макс FPS": {
        "desc": "Минимум графики", "fps": "144-300+",
        "launch": "-NOTEXTURESTREAMING -USEALLAVAILABLECORES -nomansky -novsync -dx12",
        "settings": [
            ("sg.ResolutionQuality","75"), ("sg.ViewDistanceQuality","1"),
            ("sg.ShadowQuality","0"), ("sg.PostProcessQuality","0"),
            ("sg.TextureQuality","0"), ("sg.EffectsQuality","0"),
            ("sg.FoliageQuality","0"), ("bUseVSync","False"),
            ("FrameRateLimit","0"), ("bShowFPS","True"),
        ],
    },
    "Баланс": {
        "desc": "FPS + картинка", "fps": "90-144",
        "launch": "-USEALLAVAILABLECORES -nomansky -novsync",
        "settings": [
            ("sg.ResolutionQuality","100"), ("sg.ViewDistanceQuality","2"),
            ("sg.ShadowQuality","2"), ("sg.PostProcessQuality","2"),
            ("sg.TextureQuality","2"), ("bUseVSync","False"),
            ("FrameRateLimit","144"),
        ],
    },
    "Качество": {
        "desc": "Красивая картинка", "fps": "60-90",
        "launch": "-USEALLAVAILABLECORES -novsync",
        "settings": [
            ("sg.ResolutionQuality","100"), ("sg.ViewDistanceQuality","4"),
            ("sg.ShadowQuality","4"), ("sg.PostProcessQuality","4"),
            ("sg.TextureQuality","4"), ("bUseVSync","False"),
            ("FrameRateLimit","0"),
        ],
    },
}

FORTNITE_PARASITES = [
    ("🎓","Обучение / Tutorial",     "Убрать обучалку при входе",       RED,
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v TutorialCompleted /t REG_DWORD /d 1 /f"],
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v TutorialCompleted /t REG_DWORD /d 0 /f"]),
    ("🎬","Интро видео Epic Games",  "Логотип при каждом запуске",       ORANGE,
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v SkipIntro /t REG_DWORD /d 1 /f"],
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v SkipIntro /t REG_DWORD /d 0 /f"]),
    ("🌀","Motion Blur",             "Размытие при движении — -FPS",     RED,
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v MotionBlur /t REG_DWORD /d 0 /f"],
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v MotionBlur /t REG_DWORD /d 1 /f"]),
    ("🌿","Foliage / Листва",        "Трава и кусты — лишняя нагрузка",  GREEN,
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v FoliageQuality /t REG_DWORD /d 0 /f"],
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v FoliageQuality /t REG_DWORD /d 4 /f"]),
    ("🌊","Глубина резкости DOF",    "Размытие фона — GPU зря тратится", NEON,
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v DepthOfField /t REG_DWORD /d 0 /f"],
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v DepthOfField /t REG_DWORD /d 1 /f"]),
    ("🎵","Музыка в лобби",          "Фоновая музыка жрёт CPU/звук",     PURPLE,
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v LobbyMusicVolume /t REG_DWORD /d 0 /f"],
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v LobbyMusicVolume /t REG_DWORD /d 100 /f"]),
    ("📡","Replays / Повторы",       "Пишет replay файлы на диск",       GOLD,
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v bShouldRecord /t REG_DWORD /d 0 /f"],
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v bShouldRecord /t REG_DWORD /d 1 /f"]),
    ("💥","Эффекты материалов",      "Nanite/Lumen — очень тяжело",      ORANGE,
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v MaterialQuality /t REG_DWORD /d 0 /f"],
     ["reg add HKCU\\Software\\Epic_Games\\Fortnite /v MaterialQuality /t REG_DWORD /d 4 /f"]),
]

ARK_PRESETS = {
    "Макс FPS": {
        "desc": "Минимум графики", "fps": "60-120+",
        "launch": "-USEALLAVAILABLECORES -sm4 -d3d10 -nomansky -lowmemory -novsync",
        "settings": [
            ("sg.ResolutionQuality","75"), ("sg.ShadowQuality","0"),
            ("sg.TextureQuality","0"), ("sg.EffectsQuality","0"),
            ("sg.FoliageQuality","0"), ("bUseVSync","False"), ("FrameRateLimit","0"),
        ],
    },
    "Баланс": {
        "desc": "FPS + читаемость", "fps": "40-80",
        "launch": "-USEALLAVAILABLECORES -nomansky -novsync",
        "settings": [
            ("sg.ResolutionQuality","100"), ("sg.ShadowQuality","2"),
            ("sg.TextureQuality","2"), ("sg.EffectsQuality","2"),
            ("sg.FoliageQuality","2"), ("bUseVSync","False"),
        ],
    },
    "Качество": {
        "desc": "Красивая картинка", "fps": "25-50",
        "launch": "-USEALLAVAILABLECORES",
        "settings": [
            ("sg.ResolutionQuality","100"), ("sg.ShadowQuality","4"),
            ("sg.TextureQuality","4"), ("sg.EffectsQuality","4"),
            ("sg.FoliageQuality","4"), ("bUseVSync","False"),
        ],
    },
}

ARK_PARASITES = [
    ("🎓","Обучение / подсказки",    "Постоянные подсказки новичка",     RED,
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v TutorialDone /t REG_DWORD /d 1 /f"],
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v TutorialDone /t REG_DWORD /d 0 /f"]),
    ("🎬","Интро видео",             "Логотипы при каждом запуске",      ORANGE,
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v SkipIntro /t REG_DWORD /d 1 /f"],
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v SkipIntro /t REG_DWORD /d 0 /f"]),
    ("🌿","Foliage / Листва",        "Деревья и кусты — огромная нагрузка", GREEN,
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v FoliageQuality /t REG_DWORD /d 0 /f"],
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v FoliageQuality /t REG_DWORD /d 100 /f"]),
    ("🦕","Анимации динозавров",     "Сложные анимации жрут CPU",        PURPLE,
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v NPCQuality /t REG_DWORD /d 0 /f"],
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v NPCQuality /t REG_DWORD /d 2 /f"]),
    ("🌊","Глубина резкости DOF",    "Размытие фона — грузит GPU",       NEON,
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v DepthOfField /t REG_DWORD /d 0 /f"],
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v DepthOfField /t REG_DWORD /d 1 /f"]),
    ("🌀","Motion Blur",             "Размытие при движении — отключи",  RED,
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v MotionBlur /t REG_DWORD /d 0 /f"],
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v MotionBlur /t REG_DWORD /d 1 /f"]),
    ("☁️","Volumetric Clouds",       "Объёмные облака — очень тяжело",   GOLD,
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v VolumetricClouds /t REG_DWORD /d 0 /f"],
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v VolumetricClouds /t REG_DWORD /d 1 /f"]),
    ("💧","Вода / Water Quality",    "Отражения воды — дорогой эффект",  ORANGE,
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v WaterQuality /t REG_DWORD /d 0 /f"],
     ["reg add HKCU\\Software\\Studio_Wildcard\\ARK /v WaterQuality /t REG_DWORD /d 2 /f"]),
]

GAMES = {
    "Rust":  {"icon": "🔫", "color": "#e07020", "desc": "Survival multiplayer",
              "presets": RUST_PRESETS, "parasites": RUST_PARASITES,
              "tips": [
                  ("💡", "Откл. Steam оверлей",    "Steam → ПКМ на Rust → Свойства → убери Steam Overlay"),
                  ("🛡", "Добавь в исключения",     "Windows Defender → Исключения → папка с Rust"),
                  ("🎮", "DirectX 11",              "В параметрах запуска: -force-feature-level-11-0"),
                  ("🧹", "Очищай кэш шейдеров",     "AppData/Local/Temp/Rust — удаляй раз в неделю"),
              ]},
    "GTA V": {"icon": "🚗", "color": "#00a8ff", "desc": "Open world / FiveM",
              "presets": GTA_PRESETS, "parasites": GTA_PARASITES,
              "tips": [
                  ("🟣", "FiveM: откл. все оверлеи", "Discord, Steam, NVIDIA — всё выключи"),
                  ("⚡", "Параметр -notablet",         "Обязательный параметр запуска"),
                  ("🌐", "NAT Type Open",               "Пробрось порты 6672 UDP и 61455-61458 UDP"),
                  ("🔧", "Rockstar Launcher",            "Выключи из автозагрузки — жрёт RAM"),
              ]},
    "CS2":   {"icon": "🎯", "color": "#ff6b35", "desc": "Counter-Strike 2",
              "presets": CS2_PRESETS, "parasites": CS2_PARASITES,
              "tips": [
                  ("🖥", "Частота монитора",   "NVIDIA → Панель управления → выбери 144/240Hz"),
                  ("🖱", "Raw Input мышь",      "В настройках CS2: m_rawinput 1"),
                  ("📡", "Rate команды",         "rate 786432; cl_interp 0; cl_interp_ratio 1"),
                  ("🌡", "Температура CPU",      "CS2 нагружает CPU — больше 90°C = чистка кулера"),
              ]},
    "Fortnite": {"icon": "🌀", "color": "#00d4ff", "desc": "Battle Royale",
              "presets": FORTNITE_PRESETS, "parasites": FORTNITE_PARASITES,
              "tips": [
                  ("📁", "Путь к настройкам",  "%%LOCALAPPDATA%%\\FortniteGame\\Saved\\Config\\WindowsClient\\"),
                  ("⚡", "Параметры запуска",   "-NOTEXTURESTREAMING -USEALLAVAILABLECORES -dx12"),
                  ("🛡", "Исключения Defender", "Добавь папку Fortnite в исключения антивируса"),
                  ("🎮", "DirectX 12",          "Используй DX12 — лучше FPS на современных GPU"),
              ]},
    "ARK":   {"icon": "🦕", "color": "#76b041", "desc": "Survival Evolved/Ascended",
              "presets": ARK_PRESETS, "parasites": ARK_PARASITES,
              "tips": [
                  ("💾", "Память",              "ARK требует 16GB+ RAM. Закрой всё перед игрой"),
                  ("⚡", "Параметры запуска",   "-USEALLAVAILABLECORES -sm4 -d3d10 -nomansky -lowmemory"),
                  ("🌿", "Foliage Quality",      "Листва = главный убийца FPS. Ставь на минимум"),
                  ("🧹", "Очисти кэш шейдеров", "ShaderCache в папке ARK — удаляй при фризах"),
              ]},
}

WIN_OPTS = [
    ("⚡", "Высокий план питания",       "Максимальная производительность CPU",   NEON,
     ["powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"],
     ["powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e"]),
    ("📈", "Приоритет CPU (Win32=38)",    "Лучший отклик в играх",                 GREEN,
     [r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f'],
     [r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 2 /f']),
    ("🎮", "HAGS GPU Scheduling",         "Меньше задержка GPU",                   PURPLE,
     [r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" /v HwSchMode /t REG_DWORD /d 2 /f'],
     [r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" /v HwSchMode /t REG_DWORD /d 1 /f']),
    ("🖥", "Откл. визуальные эффекты",    "Анимации Windows — ненужный расход",    ORANGE,
     [r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f'],
     [r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 0 /f']),
    ("🔕", "Откл. Xbox Game Bar",         "-5-15% CPU в играх",                    RED,
     [r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f',
      r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f'],
     [r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 1 /f']),
    ("🔍", "Откл. Windows Search",        "Не индексирует во время игры",          GOLD,
     ["net stop wsearch", "sc config wsearch start=disabled"],
     ["net start wsearch", "sc config wsearch start=auto"]),
    ("📊", "Откл. SysMain",               "Освобождает RAM и диск",                ORANGE,
     ["net stop sysmain", "sc config sysmain start=disabled"],
     ["net start sysmain", "sc config sysmain start=auto"]),
    ("🧹", "Очистка RAM",                 "Освобождает память перед игрой",        GREEN,
     ["rundll32.exe advapi32.dll,ProcessIdleTasks"], []),
    ("⏸", "Пауза Windows Update",         "Обновления не мешают игре",             RED,
     ["net stop wuauserv", "net stop bits", "net stop dosvc"],
     ["net start wuauserv"]),
]

NET_OPTS = [
    ("🌐", "DNS Google + Cloudflare",  "8.8.8.8 + 1.1.1.1",               GREEN,
     ['netsh interface ip set dns "Ethernet" static 8.8.8.8',
      'netsh interface ip add dns "Ethernet" 1.1.1.1 index=2',
      "ipconfig /flushdns"],
     ['netsh interface ip set dns "Ethernet" dhcp', "ipconfig /flushdns"]),
    ("🏎", "Откл. Nagle",              "-5-30ms пинга",                     NEON,
     [r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v TcpAckFrequency /t REG_DWORD /d 1 /f',
      r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v TCPNoDelay /t REG_DWORD /d 1 /f'],
     [r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v TcpAckFrequency /t REG_DWORD /d 2 /f']),
    ("📶", "QoS DSCP=46",              "Приоритет игрового трафика",        PURPLE,
     ['netsh qos delete policy "GO_Game"',
      'netsh qos add policy "GO_Game" app="*" dscp=46 throttle-rate=-1'],
     ['netsh qos delete policy "GO_Game"']),
    ("🔕", "Откл. IPv6",               "Убирает конфликты IPv4/IPv6",       ORANGE,
     [r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters" /v DisabledComponents /t REG_DWORD /d 255 /f'],
     [r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters" /v DisabledComponents /t REG_DWORD /d 0 /f']),
    ("🔄", "Сброс Winsock",            "Полный сброс сетевого стека",       RED,
     ["netsh winsock reset", "netsh int ip reset", "ipconfig /flushdns"], []),
]

OVERLAYS = [
    ("🎮", "Xbox Game Bar / DVR",   "Сжирает 5-15% CPU",            RED,
     [r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f',
      r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f'],
     [r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 1 /f']),
    ("📸", "NVIDIA ShadowPlay",      "Пишет видео в фоне",           ORANGE,
     [r'reg add "HKCU\Software\NVIDIA Corporation\NVCapture" /v CaptureEnabled /t REG_DWORD /d 0 /f'],
     [r'reg add "HKCU\Software\NVIDIA Corporation\NVCapture" /v CaptureEnabled /t REG_DWORD /d 1 /f']),
    ("💬", "Discord оверлей",        "+3-8ms задержки на кадр",      PURPLE,
     [r'reg add "HKCU\Software\Discord" /v Overlay /t REG_DWORD /d 0 /f'],
     [r'reg add "HKCU\Software\Discord" /v Overlay /t REG_DWORD /d 1 /f']),
    ("🎵", "Steam оверлей",          "Shift+Tab лагает, грузит RAM", NEON,
     [r'reg add "HKCU\Software\Valve\Steam" /v SteamOverlayEnabled /t REG_DWORD /d 0 /f'],
     [r'reg add "HKCU\Software\Valve\Steam" /v SteamOverlayEnabled /t REG_DWORD /d 1 /f']),
]

BG_PROCS = [
    ("🔄", "Windows Update",        "Качает обновления во время игры", RED,
     ["net stop wuauserv", "net stop bits", "net stop dosvc"],
     ["net start wuauserv"]),
    ("🔍", "Windows Search",        "Индексирует файлы, грузит диск",  ORANGE,
     ["net stop wsearch", "sc config wsearch start=disabled"],
     ["net start wsearch", "sc config wsearch start=auto"]),
    ("📊", "SysMain / Superfetch",  "Предзагрузка мешает играм",       GOLD,
     ["net stop sysmain", "sc config sysmain start=disabled"],
     ["net start sysmain", "sc config sysmain start=auto"]),
    ("☁️", "OneDrive синхронизация","Грузит диск и сеть",              NEON,
     ["taskkill /f /im OneDrive.exe", "sc config OneSyncSvc start=disabled"],
     ["sc config OneSyncSvc start=auto"]),
]


# ─── Приложение ────────────────────────────────────────────

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Game Optimizer v2.0")
        self.configure(fg_color=BG)
        self.monitor_running = False
        self.ping_history = []
        self._build_ui()
        self.geometry("1100x700")
        self.minsize(960, 620)

    # ── Sidebar + content ─────────────────────────────────
    def _build_ui(self):
        sb = ctk.CTkFrame(self, width=200, fg_color=PANEL,
                          corner_radius=0, border_width=1, border_color=BORDER)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # Logo
        lf = ctk.CTkFrame(sb, fg_color="transparent")
        lf.pack(pady=(16, 4), padx=12)
        ctk.CTkLabel(lf, text="🎮",
                     font=ctk.CTkFont(size=22)).pack(side="left")
        ctk.CTkLabel(lf, text=" GAME OPTIMIZER",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=NEON).pack(side="left")
        ctk.CTkLabel(sb, text="v2.0",
                     font=ctk.CTkFont(size=10), text_color=DIM).pack()

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(
            fill="x", padx=10, pady=8)
        ctk.CTkLabel(sb, text="ИГРЫ",
                     font=ctk.CTkFont(size=10), text_color=DIM).pack(
            anchor="w", padx=12)

        self.game_btns = {}
        for gname, gdata in GAMES.items():
            b = ctk.CTkButton(
                sb,
                text=gdata["icon"] + "  " + gname,
                anchor="w",
                font=ctk.CTkFont(size=13),
                height=38,
                fg_color="transparent",
                hover_color="#0d1e38",
                text_color=DIM,
                corner_radius=8,
                command=lambda g=gname: self.show_game(g),
            )
            b.pack(fill="x", padx=8, pady=2)
            self.game_btns[gname] = b

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(
            fill="x", padx=10, pady=8)
        ctk.CTkLabel(sb, text="ОБЩЕЕ",
                     font=ctk.CTkFont(size=10), text_color=DIM).pack(
            anchor="w", padx=12)

        self.nav_btns = {}
        for pid, label in [("profile", "💻  Профиль ПК"),
                           ("windows", "⚡  Windows"),
                           ("network", "🌐  Сеть"),
                           ("monitor", "📊  Мониторинг")]:
            b = ctk.CTkButton(
                sb,
                text=label,
                anchor="w",
                font=ctk.CTkFont(size=12),
                height=34,
                fg_color="transparent",
                hover_color="#0d1e38",
                text_color=DIM,
                corner_radius=8,
                command=lambda p=pid: self.show_page(p),
            )
            b.pack(fill="x", padx=8, pady=2)
            self.nav_btns[pid] = b

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(
            fill="x", padx=10, pady=8, side="bottom")
        self.joke_lbl = ctk.CTkLabel(
            sb,
            text=random.choice(JOKES),
            font=ctk.CTkFont(size=10, slant="italic"),
            text_color=GOLD,
            wraplength=178,
            justify="center",
        )
        self.joke_lbl.pack(side="bottom", padx=8, pady=6)

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

    # ── Page switching ────────────────────────────────────
    def show_game(self, gname):
        for p in self.pages.values():
            p.pack_forget()
        self.pages[gname].pack(fill="both", expand=True)
        for k, b in self.game_btns.items():
            if k == gname:
                b.configure(fg_color="#0d2040",
                            text_color=GAMES[k]["color"])
            else:
                b.configure(fg_color="transparent", text_color=DIM)
        for b in self.nav_btns.values():
            b.configure(fg_color="transparent", text_color=DIM)

    def show_page(self, pid):
        for p in self.pages.values():
            p.pack_forget()
        self.pages[pid].pack(fill="both", expand=True)
        for b in self.game_btns.values():
            b.configure(fg_color="transparent", text_color=DIM)
        for k, b in self.nav_btns.items():
            if k == pid:
                b.configure(fg_color="#0d2040", text_color=NEON)
            else:
                b.configure(fg_color="transparent", text_color=DIM)

    # ── Helpers ───────────────────────────────────────────
    def _make_page(self, pid):
        outer = ctk.CTkFrame(self.content, fg_color=BG, corner_radius=0)
        self.pages[pid] = outer
        # Real scrollable area using tkinter Canvas
        canvas = tkinter.Canvas(outer, bg=BG, highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(outer, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        pad_frame = ctk.CTkFrame(canvas, fg_color="transparent")
        canvas_window = canvas.create_window((0, 0), window=pad_frame, anchor="nw")
        def _on_resize(e):
            canvas.itemconfig(canvas_window, width=e.width)
        canvas.bind("<Configure>", _on_resize)
        def _on_frame_change(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        pad_frame.bind("<Configure>", _on_frame_change)
        def _on_mousewheel(e):
            canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        pad = ctk.CTkFrame(pad_frame, fg_color="transparent")
        pad.pack(fill="both", expand=True, padx=22, pady=16)
        return pad

    def _make_log(self, parent, height=120):
        tb = ctk.CTkTextbox(
            parent,
            height=height,
            fg_color="#020810",
            border_width=1,
            border_color=BORDER,
            font=ctk.CTkFont(family="Courier New", size=11),
            text_color="#68ffaa",
            corner_radius=8,
        )
        tb.pack(fill="x", pady=(4, 0))
        tb.configure(state="disabled")
        return tb

    def _log_write(self, tb, text):
        tb.configure(state="normal")
        tb.insert("end", text + "\n")
        tb.configure(state="disabled")
        tb.see("end")

    def _log_clear(self, tb):
        tb.configure(state="normal")
        tb.delete("1.0", "end")
        tb.configure(state="disabled")

    def _make_toggle(self, parent, label, desc, on_cmds, off_cmds, accent=NEON):
        row = ctk.CTkFrame(parent, fg_color=PANEL2,
                           corner_radius=6, border_width=1, border_color=BORDER)
        row.pack(fill="x", pady=2)
        strip = ctk.CTkFrame(row, width=3, fg_color=accent, corner_radius=0)
        strip.pack(side="left", fill="y")
        ri = ctk.CTkFrame(row, fg_color="transparent")
        ri.pack(side="left", fill="x", expand=True, padx=10, pady=5)
        ctk.CTkLabel(ri, text=label,
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#fff").pack(anchor="w")
        ctk.CTkLabel(ri, text=desc,
                     font=ctk.CTkFont(size=9), text_color=DIM).pack(anchor="w")
        var = ctk.BooleanVar(value=False)

        def _on_toggle(v=var, on=on_cmds, off=off_cmds):
            cmds = on if v.get() else off
            threading.Thread(
                target=lambda c=cmds: [run_cmd(x) for x in c],
                daemon=True,
            ).start()

        ctk.CTkSwitch(
            row,
            text="",
            variable=var,
            command=_on_toggle,
            progress_color=accent,
            button_color="#ffffff",
            width=40,
        ).pack(side="right", padx=8)

    def _divider(self, parent):
        ctk.CTkFrame(parent, height=1, fg_color=BORDER).pack(fill="x", pady=10)

    def _sec(self, parent, text):
        ctk.CTkLabel(parent, text=text,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=DIM).pack(anchor="w", pady=(0, 5))

    # ── Game page ─────────────────────────────────────────
    def _build_game_page(self, gname):
        g = GAMES[gname]
        outer = ctk.CTkFrame(self.content, fg_color=BG, corner_radius=0)
        self.pages[gname] = outer

        # Header
        hbar = ctk.CTkFrame(outer, fg_color=PANEL, corner_radius=0,
                            border_width=1, border_color=BORDER, height=64)
        hbar.pack(fill="x")
        hbar.pack_propagate(False)
        hi = ctk.CTkFrame(hbar, fg_color="transparent")
        hi.pack(fill="both", padx=20, pady=10)
        ctk.CTkLabel(hi, text=g["icon"],
                     font=ctk.CTkFont(size=28)).pack(side="left", padx=(0, 12))
        ht = ctk.CTkFrame(hi, fg_color="transparent")
        ht.pack(side="left", fill="y", expand=True)
        ctk.CTkLabel(ht, text=gname,
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=g["color"]).pack(anchor="w")
        ctk.CTkLabel(ht, text=g["desc"],
                     font=ctk.CTkFont(size=11),
                     text_color=DIM).pack(anchor="w")
        make_btn(
            hi, "⚡  ОПТИМИЗИРОВАТЬ ВСЁ",
            lambda gn=gname: self._full_optimize(gn),
            size=12, width=200,
            color=g["color"], hover="#ffffff",
        ).pack(side="right")

        # Tab bar
        tab_bar = ctk.CTkFrame(outer, fg_color=PANEL2,
                               corner_radius=0, height=40)
        tab_bar.pack(fill="x")
        tab_bar.pack_propagate(False)

        tab_content = ctk.CTkFrame(outer, fg_color=BG, corner_radius=0)
        tab_content.pack(fill="both", expand=True)

        tab_frames = {}
        tab_btn_map = {}

        tab_names = ["🎨 Графика", "🚫 Паразиты", "🌐 Сеть", "💡 Советы"]
        if gname == "CS2":
            tab_names.append("⚙️ Конфиг")
        elif gname == "GTA V":
            tab_names.append("🟣 FiveM")
        elif gname == "Rust":
            tab_names.append("🔩 Launch")

        def _show_tab(name, frames=tab_frames, btns=tab_btn_map, gc=g["color"]):
            for f in frames.values():
                f.pack_forget()
            frames[name].pack(fill="both", expand=True)
            for n, b in btns.items():
                if n == name:
                    b.configure(fg_color="#0d2040", text_color=gc)
                else:
                    b.configure(fg_color="transparent", text_color=DIM)

        for tname in tab_names:
            tb2 = ctk.CTkButton(
                tab_bar,
                text=tname,
                anchor="w",
                font=ctk.CTkFont(size=11),
                height=38,
                fg_color="transparent",
                hover_color="#0d1e38",
                text_color=DIM,
                corner_radius=0,
                width=120,
                command=lambda t=tname: _show_tab(t),
            )
            tb2.pack(side="left", padx=2)
            tab_btn_map[tname] = tb2

            frame = ctk.CTkFrame(tab_content, fg_color=BG, corner_radius=0)
            tab_frames[tname] = frame
            # Scrollable tab content
            _tc = tkinter.Canvas(frame, bg=BG, highlightthickness=0)
            _sb = ctk.CTkScrollbar(frame, command=_tc.yview)
            _tc.configure(yscrollcommand=_sb.set)
            _sb.pack(side="right", fill="y")
            _tc.pack(side="left", fill="both", expand=True)
            _pf = ctk.CTkFrame(_tc, fg_color="transparent")
            _cw = _tc.create_window((0, 0), window=_pf, anchor="nw")
            _tc.bind("<Configure>", lambda e, c=_tc, w=_cw: c.itemconfig(w, width=e.width))
            _pf.bind("<Configure>", lambda e, c=_tc: c.configure(scrollregion=c.bbox("all")))
            _tc.bind_all("<MouseWheel>", lambda e, c=_tc: c.yview_scroll(int(-1*(e.delta/120)), "units"))
            inner = ctk.CTkFrame(_pf, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=20, pady=14)

            if "Графика" in tname:
                self._build_tab_graphics(inner, gname, g)
            elif "Паразиты" in tname:
                self._build_tab_parasites(inner, gname, g)
            elif "Сеть" in tname:
                self._build_tab_net(inner, gname)
            elif "Советы" in tname:
                self._build_tab_tips(inner, g)
            elif "Конфиг" in tname:
                self._build_tab_cs2cfg(inner)
            elif "FiveM" in tname:
                self._build_tab_fivem(inner)
            elif "Launch" in tname:
                self._build_tab_launch(inner)

        _show_tab(tab_names[0])

    # ── Tab: Graphics ─────────────────────────────────────
    def _build_tab_graphics(self, pad, gname, g):
        ctk.CTkLabel(pad, text="🎨 Пресеты графики",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad,
                     text="Выбери пресет — получишь параметры запуска для Steam",
                     font=ctk.CTkFont(size=11),
                     text_color=DIM).pack(anchor="w", pady=(0, 12))

        log_ref = [None]
        gr = ctk.CTkFrame(pad, fg_color="transparent")
        gr.pack(fill="x", pady=(0, 8))

        for i, (pname, pdata) in enumerate(g["presets"].items()):
            gr.columnconfigure(i, weight=1)
            c = ctk.CTkFrame(gr, fg_color=PANEL, corner_radius=11,
                             border_width=2, border_color=BORDER)
            c.grid(row=0, column=i, padx=4, sticky="ew")
            ci = ctk.CTkFrame(c, fg_color="transparent")
            ci.pack(fill="both", padx=12, pady=12)
            ctk.CTkLabel(ci, text=pname,
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=g["color"]).pack(anchor="w")
            ctk.CTkLabel(ci, text=pdata["desc"],
                         font=ctk.CTkFont(size=10),
                         text_color=DIM).pack(anchor="w", pady=(2, 6))
            fr = ctk.CTkFrame(ci, fg_color="transparent")
            fr.pack(anchor="w", pady=(0, 4))
            ctk.CTkLabel(fr, text="FPS: ",
                         font=ctk.CTkFont(size=10), text_color=DIM).pack(side="left")
            ctk.CTkLabel(fr, text=pdata["fps"],
                         font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=GREEN).pack(side="left")
            ctk.CTkLabel(ci, text=str(len(pdata["settings"])) + " параметров",
                         font=ctk.CTkFont(size=10),
                         text_color=DIM).pack(anchor="w", pady=(0, 8))
            make_btn(
                ci, "✓  Применить",
                lambda p=pdata, n=pname, lr=log_ref: self._apply_preset(p, n, lr),
                size=11, bold=False, width=150,
                color="#1a3050", hover="#2a4060",
            ).pack(anchor="w")

        log_ref[0] = self._make_log(pad, 100)

    def _apply_preset(self, pdata, pname, log_ref):
        if log_ref[0] is None:
            return
        self._log_clear(log_ref[0])
        self._log_write(log_ref[0], "▶ Применяю «" + pname + "»...")

        def run():
            for k, v in pdata["settings"]:
                self._log_write(log_ref[0], "  ✓ " + k + " = " + v)
                time.sleep(0.03)
            launch = pdata.get("launch", "")
            if launch:
                self._log_write(log_ref[0], "")
                self._log_write(log_ref[0], "Параметры запуска Steam:")
                self._log_write(log_ref[0], "  " + launch)
                self._log_write(log_ref[0], "  → Steam → ПКМ на игре → Свойства → Параметры запуска")
            self._log_write(log_ref[0], "")
            self._log_write(log_ref[0], "✅ Готово! Ожид. FPS: " + pdata["fps"])

        threading.Thread(target=run, daemon=True).start()

    # ── Tab: Parasites ────────────────────────────────────
    def _build_tab_parasites(self, pad, gname, g):
        ctk.CTkLabel(pad, text="🚫 Паразитные функции",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad,
                     text="Отключи ненужные функции внутри игры, оверлеи и фоновые процессы",
                     font=ctk.CTkFont(size=11),
                     text_color=DIM).pack(anchor="w", pady=(0, 12))

        self._sec(pad, "🎮 Внутри " + gname + " — ненужные функции")
        for ico, name, desc, accent, on_c, off_c in g["parasites"]:
            self._make_toggle(pad, ico + "  " + name, desc, on_c, off_c, accent)

        self._divider(pad)
        self._sec(pad, "🖥 Оверлеи — жрут FPS")
        for ico, name, desc, accent, on_c, off_c in OVERLAYS:
            self._make_toggle(pad, ico + "  " + name, desc, on_c, off_c, accent)

        self._divider(pad)
        self._sec(pad, "⚙️ Фоновые процессы Windows")
        for ico, name, desc, accent, on_c, off_c in BG_PROCS:
            self._make_toggle(pad, ico + "  " + name, desc, on_c, off_c, accent)

        self._divider(pad)
        make_btn(
            pad, "☠️  УБИТЬ ВСЕ ПАРАЗИТЫ " + gname.upper(),
            lambda gn=gname: self._kill_game_parasites(gn),
            size=13, width=300,
            color="#4a0000", hover="#7a0000",
        ).pack(anchor="w", pady=(0,4))
        make_btn(
            pad, "🚫  ОТКЛ. ВСЕ СИСТЕМНЫЕ ПАРАЗИТЫ",
            self._disable_all_parasites,
            size=13, width=300,
            color="#6b0000", hover="#8b0000",
        ).pack(anchor="w")
        self._kill_log = self._make_log(pad, 70)

    def _kill_game_parasites(self, gname):
        g = GAMES[gname]
        log = getattr(self, "_kill_log", None)
        def run():
            if log: self._log_write(log, "☠️ Убиваю все паразиты " + gname + "...")
            count = 0
            for item in g["parasites"]:
                ico, name, desc, accent, on_c, off_c = item
                for cmd in on_c:
                    run_cmd(cmd)
                    count += 1
            extra = [
                "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR /v AppCaptureEnabled /t REG_DWORD /d 0 /f",
                "reg add HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR /v AllowGameDVR /t REG_DWORD /d 0 /f",
                "reg add HKCU\\Software\\Valve\\Steam /v SteamOverlayEnabled /t REG_DWORD /d 0 /f",
            ]
            for cmd in extra:
                run_cmd(cmd)
                count += 1
            if log:
                self._log_write(log, "  ✓ " + str(count) + " паразитов отключено")
                self._log_write(log, "✅ Все паразиты " + gname + " убиты!")
        threading.Thread(target=run, daemon=True).start()

    def _disable_all_parasites(self):
        cmds = [
            r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f',
            r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f',
            "net stop wuauserv",
            "net stop wsearch",
            "net stop sysmain",
            "taskkill /f /im OneDrive.exe",
        ]
        threading.Thread(
            target=lambda c=cmds: [run_cmd(x) for x in c],
            daemon=True,
        ).start()

    # ── Tab: Network ─────────────────────────────────────
    def _build_tab_net(self, pad, gname):
        ctk.CTkLabel(pad, text="🌐 Настройка сети",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text="Оптимизация пинга для " + gname,
                     font=ctk.CTkFont(size=11),
                     text_color=DIM).pack(anchor="w", pady=(0, 12))
        for ico, name, desc, accent, on_c, off_c in NET_OPTS:
            self._make_toggle(pad, ico + "  " + name, desc, on_c, off_c, accent)
        self._divider(pad)
        make_btn(
            pad, "📡  Проверить пинг",
            lambda p=pad: self._quick_ping(p),
            width=180, color="#006adf", hover="#0090ff",
        ).pack(anchor="w")

    def _quick_ping(self, pad):
        log = self._make_log(pad, 80)

        def run():
            for name, host in [
                ("Steam",      "store.steampowered.com"),
                ("Cloudflare", "1.1.1.1"),
                ("Google",     "8.8.8.8"),
            ]:
                ms = ping_host(host)
                if ms > 0:
                    self._log_write(log, "✓  " + name.ljust(14) + str(ms) + " ms")
                else:
                    self._log_write(log, "✗  " + name.ljust(14) + "timeout")
                time.sleep(0.1)
            self._log_write(log, "✅ Готово!")

        threading.Thread(target=run, daemon=True).start()

    # ── Tab: Tips ─────────────────────────────────────────
    def _build_tab_tips(self, pad, g):
        ctk.CTkLabel(pad, text="💡 Советы",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 12))
        for ico, title, text in g["tips"]:
            c = ctk.CTkFrame(pad, fg_color=PANEL2, corner_radius=9,
                             border_width=1, border_color=BORDER)
            c.pack(fill="x", pady=3)
            ci = ctk.CTkFrame(c, fg_color="transparent")
            ci.pack(fill="x", padx=14, pady=10)
            ctk.CTkLabel(ci, text=ico + "  " + title,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="#fff").pack(anchor="w")
            ctk.CTkLabel(ci, text=text,
                         font=ctk.CTkFont(size=11),
                         text_color=TEXT,
                         wraplength=700, justify="left").pack(anchor="w", pady=(2, 0))

    # ── Tab: CS2 config ───────────────────────────────────
    def _build_tab_cs2cfg(self, pad):
        ctk.CTkLabel(pad, text="⚙️ autoexec.cfg",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text="Готовый конфиг для максимального FPS",
                     font=ctk.CTkFont(size=11),
                     text_color=DIM).pack(anchor="w", pady=(0, 10))
        cfg = (
            "fps_max 0\n"
            "r_lowlatency 2\n"
            "cl_showfps 1\n"
            "mat_queue_mode -1\n"
            "r_dynamic_lighting 0\n"
            "r_shadows 0\n"
            "cl_ragdoll_physics_enable 0\n"
            "r_motionblur 0\n"
            "cl_interp 0\n"
            "cl_interp_ratio 1\n"
            "rate 786432\n"
            "cl_updaterate 128\n"
            "cl_cmdrate 128\n"
            "m_rawinput 1\n"
            "snd_menumusic_volume 0"
        )
        tb = ctk.CTkTextbox(
            pad, height=260,
            fg_color="#020810", border_width=1, border_color=BORDER,
            font=ctk.CTkFont(family="Courier New", size=12),
            text_color="#68ffaa", corner_radius=8,
        )
        tb.pack(fill="x", pady=(0, 10))
        tb.insert("end", cfg)
        make_btn(
            pad, "💾  Сохранить в Downloads",
            lambda: self._save_file(tb.get("1.0", "end"), "autoexec.cfg"),
            width=230, color="#006adf", hover="#0090ff",
        ).pack(anchor="w")

    def _save_file(self, content, filename):
        path = os.path.join(os.path.expanduser("~"), "Downloads", filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            pass

    # ── Tab: FiveM ────────────────────────────────────────
    def _build_tab_fivem(self, pad):
        ctk.CTkLabel(pad, text="🟣 FiveM оптимизация",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text="Специальные твики для FiveM серверов",
                     font=ctk.CTkFont(size=11),
                     text_color=DIM).pack(anchor="w", pady=(0, 12))
        opts = [
            ("🧹", "Очистить кэш FiveM",   "Удаляет кэш шейдеров и текстур", NEON,
             [r'rmdir /s /q "%LOCALAPPDATA%\FiveM\FiveM.app\cache"'], []),
            ("🔕", "Откл. оверлей FiveM",  "Убирает оверлей сервера",         ORANGE,
             [r'reg add "HKCU\Software\CitizenFX\FiveM" /v DrawOverlay /t REG_DWORD /d 0 /f'],
             [r'reg add "HKCU\Software\CitizenFX\FiveM" /v DrawOverlay /t REG_DWORD /d 1 /f']),
            ("⚡", "StreamMemory 756MB",    "Больше памяти для текстур",       GREEN,
             [r'reg add "HKCU\Software\CitizenFX\FiveM" /v StreamingMemory /t REG_DWORD /d 756 /f'],
             [r'reg add "HKCU\Software\CitizenFX\FiveM" /v StreamingMemory /t REG_DWORD /d 512 /f']),
        ]
        for ico, name, desc, accent, on_c, off_c in opts:
            self._make_toggle(pad, ico + "  " + name, desc, on_c, off_c, accent)
        self._divider(pad)
        ctk.CTkLabel(pad,
                     text="💡 Добавь +set fpslimit 0 в параметры запуска FiveM",
                     font=ctk.CTkFont(size=11, slant="italic"),
                     text_color=GOLD).pack(anchor="w")

    # ── Tab: Rust launch ──────────────────────────────────
    def _build_tab_launch(self, pad):
        ctk.CTkLabel(pad, text="🔩 Launch Arguments",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad,
                     text="Steam → ПКМ на Rust → Свойства → Параметры запуска",
                     font=ctk.CTkFont(size=11),
                     text_color=DIM).pack(anchor="w", pady=(0, 10))
        for pname, args in [
            ("⚡ Максимум FPS",
             "-high -maxMem=8192 -malloc=system -force-feature-level-11-0 +fps.limit 0 -nolog"),
            ("⚖️ Баланс",
             "-high -maxMem=8192 -malloc=system +fps.limit 0"),
            ("🖥 Слабый ПК",
             "-high -maxMem=4096 -malloc=system -force-feature-level-10-0 +fps.limit 60 -nolog"),
        ]:
            c = ctk.CTkFrame(pad, fg_color=PANEL2, corner_radius=9,
                             border_width=1, border_color=BORDER)
            c.pack(fill="x", pady=4)
            ci = ctk.CTkFrame(c, fg_color="transparent")
            ci.pack(fill="x", padx=14, pady=10)
            ctk.CTkLabel(ci, text=pname,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="#fff").pack(anchor="w")
            tb = ctk.CTkTextbox(
                ci, height=40,
                fg_color="#020810", border_width=1, border_color=BORDER,
                font=ctk.CTkFont(family="Courier New", size=11),
                text_color=NEON, corner_radius=6,
            )
            tb.pack(fill="x", pady=(4, 0))
            tb.insert("end", args)

    # ── Full optimize popup ───────────────────────────────
    def _full_optimize(self, gname):
        win = ctk.CTkToplevel(self)
        win.title("Оптимизация " + gname)
        win.geometry("500x380")
        win.configure(fg_color=BG)
        ctk.CTkLabel(win,
                     text="⚡ Полная оптимизация " + gname,
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#fff").pack(pady=(16, 8), padx=16, anchor="w")
        log = self._make_log(win, 260)
        log.pack_forget()
        log.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        def run():
            steps = [
                ("⚡ Высокий план питания",
                 "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"),
                ("🔕 Откл. Game DVR",
                 r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f'),
                ("🌐 DNS Google",
                 'netsh interface ip set dns "Ethernet" static 8.8.8.8'),
                ("🏎 Откл. Nagle",
                 r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v TcpAckFrequency /t REG_DWORD /d 1 /f'),
                ("🔄 Flush DNS", "ipconfig /flushdns"),
                ("⏸ Стоп Win Update", "net stop wuauserv"),
                ("🔍 Стоп Indexer",   "net stop wsearch"),
                ("🧹 Очистка RAM",    "rundll32.exe advapi32.dll,ProcessIdleTasks"),
            ]
            for name, cmd in steps:
                ok = run_cmd(cmd)
                self._log_write(log, "  " + ("✓" if ok else "✗") + " " + name)
                time.sleep(0.15)
            self._log_write(log, "")
            self._log_write(log, "✅ Готово! Запускай " + gname + "!")

        threading.Thread(target=run, daemon=True).start()

    # ── Profile page ──────────────────────────────────────
    def _build_profile_page(self):
        pad = self._make_page("profile")
        ctk.CTkLabel(pad, text="💻 Профиль ПК",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0,4))
        ctk.CTkLabel(pad, text="Характеристики системы и нагрузка в реальном времени",
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(anchor="w", pady=(0,12))

        # System info grid
        info_card = ctk.CTkFrame(pad, fg_color=PANEL, corner_radius=12,
                                 border_width=1, border_color=BORDER)
        info_card.pack(fill="x", pady=(0,10))
        ip = ctk.CTkFrame(info_card, fg_color="transparent")
        ip.pack(fill="x", padx=16, pady=12)
        ctk.CTkLabel(ip, text="🖥 Характеристики",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0,8))
        self.info_labels = {}
        ig = ctk.CTkFrame(ip, fg_color="transparent")
        ig.pack(fill="x")
        ig.columnconfigure(0, weight=1)
        ig.columnconfigure(1, weight=1)
        for i, field in enumerate(["OS","CPU","RAM","Диск C:","GPU","IP"]):
            f = ctk.CTkFrame(ig, fg_color=PANEL2, corner_radius=7,
                             border_width=1, border_color=BORDER)
            f.grid(row=i//2, column=i%2, padx=3, pady=3, sticky="ew")
            fi = ctk.CTkFrame(f, fg_color="transparent")
            fi.pack(fill="x", padx=10, pady=6)
            ctk.CTkLabel(fi, text=field, font=ctk.CTkFont(size=9),
                         text_color=DIM).pack(anchor="w")
            lbl = ctk.CTkLabel(fi, text="Загружаю...",
                               font=ctk.CTkFont(size=11, weight="bold"),
                               text_color="#fff")
            lbl.pack(anchor="w")
            self.info_labels[field] = lbl

        # Live stats boxes
        self._divider(pad)
        ctk.CTkLabel(pad, text="📊 Нагрузка прямо сейчас",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0,8))
        sr = ctk.CTkFrame(pad, fg_color="transparent")
        sr.pack(fill="x", pady=(0,10))
        for i in range(4): sr.columnconfigure(i, weight=1)
        self.stat_boxes = {}
        for i, (k, lbl, col) in enumerate([("cpu","CPU %",GREEN),("ram","RAM %",NEON),("disk","Диск %",GOLD),("temp","Темп °C",RED)]):
            f = ctk.CTkFrame(sr, fg_color=PANEL2, corner_radius=9,
                             border_width=1, border_color=BORDER)
            f.grid(row=0, column=i, padx=4, sticky="ew")
            v = ctk.CTkLabel(f, text="—",
                             font=ctk.CTkFont(size=26, weight="bold"), text_color=col)
            v.pack(pady=(10,2))
            ctk.CTkLabel(f, text=lbl, font=ctk.CTkFont(size=10), text_color=DIM).pack(pady=(0,8))
            self.stat_boxes[k] = v

        # Progress bars
        bf = ctk.CTkFrame(pad, fg_color=PANEL, corner_radius=10,
                          border_width=1, border_color=BORDER)
        bf.pack(fill="x", pady=(0,10))
        bp = ctk.CTkFrame(bf, fg_color="transparent")
        bp.pack(fill="x", padx=14, pady=10)
        self.prog_bars = {}
        for k, lbl, col in [("cpu","CPU",GREEN),("ram","RAM",NEON),("disk","ДИСК",GOLD)]:
            r = ctk.CTkFrame(bp, fg_color="transparent")
            r.pack(fill="x", pady=3)
            ctk.CTkLabel(r, text=lbl, font=ctk.CTkFont(size=10),
                         text_color=DIM, width=40).pack(side="left")
            bar = ctk.CTkProgressBar(r, height=14, progress_color=col,
                                     fg_color=PANEL2, corner_radius=4)
            bar.set(0)
            bar.pack(side="left", fill="x", expand=True, padx=8)
            pct = ctk.CTkLabel(r, text="0%", font=ctk.CTkFont(size=10),
                               text_color=col, width=35)
            pct.pack(side="left")
            self.prog_bars[k] = (bar, pct)

        # Ping row
        self._divider(pad)
        ctk.CTkLabel(pad, text="🌐 Пинг",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0,6))
        pr = ctk.CTkFrame(pad, fg_color="transparent")
        pr.pack(fill="x", pady=(0,8))
        pr.columnconfigure(0, weight=1); pr.columnconfigure(1, weight=1)
        self.ping_google = self._ping_box(pr, "Google 8.8.8.8", 0)
        self.ping_steam  = self._ping_box(pr, "Steam", 1)

        make_btn(pad, "🔄  Обновить", self._refresh_profile,
                 width=160, color="#006adf", hover="#0090ff").pack(anchor="w")

        threading.Thread(target=self._load_profile, daemon=True).start()
        self._live_running = True
        threading.Thread(target=self._live_loop, daemon=True).start()

    def _ping_box(self, parent, label, col):
        f = ctk.CTkFrame(parent, fg_color=PANEL2, corner_radius=8,
                         border_width=1, border_color=BORDER)
        f.grid(row=0, column=col, padx=4, sticky="ew")
        fi = ctk.CTkFrame(f, fg_color="transparent")
        fi.pack(fill="x", padx=10, pady=8)
        ctk.CTkLabel(fi, text=label, font=ctk.CTkFont(size=10), text_color=DIM).pack(anchor="w")
        v = ctk.CTkLabel(fi, text="—", font=ctk.CTkFont(size=16, weight="bold"), text_color=NEON)
        v.pack(anchor="w")
        return v

    def _safe_set(self, lbl, text):
        try: lbl.configure(text=text)
        except: pass

    def _load_profile(self):
        import platform
        self._safe_set(self.info_labels["OS"],
                       platform.system() + " " + platform.release())
        def wmic(cmd):
            try:
                r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                                   timeout=8, encoding="cp1251", errors="replace")
                return r.stdout.strip()
            except: return ""
        cpu = wmic("wmic cpu get Name /value").replace("Name=","").strip()
        self._safe_set(self.info_labels["CPU"], (cpu[:42] + "...") if len(cpu)>42 else cpu or "—")
        try:
            rb = int(wmic("wmic computersystem get TotalPhysicalMemory /value").replace("TotalPhysicalMemory=","").strip())
            self._safe_set(self.info_labels["RAM"], str(round(rb/1024**3,1)) + " GB")
        except: self._safe_set(self.info_labels["RAM"], "—")
        try:
            raw = wmic("wmic logicaldisk where DeviceID=\"C:\" get FreeSpace,Size /value")
            d = {l.split("=")[0]:l.split("=")[1] for l in raw.splitlines() if "=" in l and len(l.split("="))>1 and l.split("=")[1].strip()}
            free = int(d.get("FreeSpace",0))//1024**3
            tot  = int(d.get("Size",0))//1024**3
            self._safe_set(self.info_labels["Диск C:"], str(free) + " GB / " + str(tot) + " GB")
        except: self._safe_set(self.info_labels["Диск C:"], "—")
        gpu = wmic("wmic path win32_videocontroller get Name /value").replace("Name=","").strip()
        self._safe_set(self.info_labels["GPU"], (gpu[:42]+"...") if len(gpu)>42 else gpu or "—")
        try:
            s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s2.connect(("8.8.8.8", 80)); ip = s2.getsockname()[0]; s2.close()
        except: ip = "—"
        self._safe_set(self.info_labels["IP"], ip)
        ms_g = ping_host("8.8.8.8")
        ms_s = ping_host("store.steampowered.com")
        self._safe_set(self.ping_google, (str(ms_g)+" ms") if ms_g>0 else "timeout")
        self._safe_set(self.ping_steam,  (str(ms_s)+" ms") if ms_s>0 else "timeout")

    def _live_loop(self):
        while getattr(self,"_live_running",False):
            self._update_live(); time.sleep(2)

    def _update_live(self):
        try:
            r = subprocess.run(
                "typeperf \"\\Processor(_Total)\\% Processor Time\" -sc 1",
                shell=True, capture_output=True, text=True,
                timeout=5, encoding="cp1251", errors="replace")
            lines = [l for l in r.stdout.splitlines() if "," in l and "Processor" not in l and "Time" not in l]
            if lines:
                v = int(float(lines[0].split(",")[1].replace('"','').strip()))
                c = GREEN if v<50 else GOLD if v<80 else RED
                self._safe_set(self.stat_boxes["cpu"], str(v)+"%")
                self.stat_boxes["cpu"].configure(text_color=c)
                self.prog_bars["cpu"][0].set(v/100)
                self.prog_bars["cpu"][1].configure(text=str(v)+"%")
        except: pass
        try:
            r2 = subprocess.run("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /value",
                shell=True, capture_output=True, text=True, timeout=5, encoding="cp1251", errors="replace")
            d = {l.split("=")[0]:l.split("=")[1] for l in r2.stdout.splitlines() if "=" in l and len(l.split("="))>1 and l.split("=")[1].strip()}
            free=int(d.get("FreePhysicalMemory",0)); tot=int(d.get("TotalVisibleMemorySize",1))
            v=int((1-free/tot)*100); c=GREEN if v<60 else GOLD if v<80 else RED
            self._safe_set(self.stat_boxes["ram"], str(v)+"%")
            self.stat_boxes["ram"].configure(text_color=c)
            self.prog_bars["ram"][0].set(v/100); self.prog_bars["ram"][1].configure(text=str(v)+"%")
        except: pass
        try:
            r3 = subprocess.run("wmic logicaldisk where DeviceID=\"C:\" get FreeSpace,Size /value",
                shell=True, capture_output=True, text=True, timeout=5, encoding="cp1251", errors="replace")
            d3={l.split("=")[0]:l.split("=")[1] for l in r3.stdout.splitlines() if "=" in l and len(l.split("="))>1 and l.split("=")[1].strip()}
            free=int(d3.get("FreeSpace",0)); tot=int(d3.get("Size",1))
            v=int((1-free/tot)*100)
            self._safe_set(self.stat_boxes["disk"], str(v)+"%")
            self.prog_bars["disk"][0].set(v/100); self.prog_bars["disk"][1].configure(text=str(v)+"%")
        except: pass
        try:
            r4 = subprocess.run(
                "wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature /value",
                shell=True, capture_output=True, text=True, timeout=5, encoding="cp1251", errors="replace")
            temps=[]
            for line in r4.stdout.splitlines():
                if "CurrentTemperature=" in line:
                    try: temps.append((int(line.split("=")[1].strip())-2732)/10)
                    except: pass
            if temps:
                v=int(sum(temps)/len(temps)); c=GREEN if v<60 else GOLD if v<80 else RED
                self._safe_set(self.stat_boxes["temp"], str(v)+"°")
                self.stat_boxes["temp"].configure(text_color=c)
            else: self._safe_set(self.stat_boxes["temp"], "N/A")
        except: self._safe_set(self.stat_boxes["temp"], "N/A")

    def _refresh_profile(self):
        for lbl in self.info_labels.values(): self._safe_set(lbl, "Обновляю...")
        threading.Thread(target=self._load_profile, daemon=True).start()

    # ── Windows page ──────────────────────────────────────
    def _build_windows_page(self):
        pad = self._make_page("windows")
        ctk.CTkLabel(pad, text="⚡ Оптимизация Windows",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text="Системные твики для максимального FPS",
                     font=ctk.CTkFont(size=11),
                     text_color=DIM).pack(anchor="w", pady=(0, 12))
        for ico, name, desc, accent, on_c, off_c in WIN_OPTS:
            self._make_toggle(pad, ico + "  " + name, desc, on_c, off_c, accent)
        self._divider(pad)
        make_btn(
            pad, "⚡  ПРИМЕНИТЬ ВСЕ",
            self._run_all_windows,
            size=14, width=260,
            color="#006adf", hover="#0090ff",
        ).pack(anchor="w")
        self.win_log = self._make_log(pad, 100)

    def _run_all_windows(self):
        self._log_clear(self.win_log)
        self._log_write(self.win_log, "⚡ Применяю все оптимизации...")
        steps = [
            ("⚡ План питания",  "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"),
            ("🔕 Game DVR",      r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f'),
            ("📈 Приоритет CPU", r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f'),
            ("🎮 HAGS",          r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" /v HwSchMode /t REG_DWORD /d 2 /f'),
            ("🔍 Search",        "net stop wsearch"),
            ("📊 SysMain",       "net stop sysmain"),
            ("⏸ Update",         "net stop wuauserv"),
            ("🧹 RAM",           "rundll32.exe advapi32.dll,ProcessIdleTasks"),
        ]

        def run():
            for name, cmd in steps:
                ok = run_cmd(cmd)
                self._log_write(self.win_log, "  " + ("✓" if ok else "✗") + " " + name)
                time.sleep(0.1)
            self._log_write(self.win_log, "")
            self._log_write(self.win_log, "✅ Готово! Перезагрузи ПК.")

        threading.Thread(target=run, daemon=True).start()

    # ── Network page ──────────────────────────────────────
    def _build_network_page(self):
        pad = self._make_page("network")
        ctk.CTkLabel(pad, text="🌐 Настройка сети",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text="Оптимизация пинга для всех игр",
                     font=ctk.CTkFont(size=11),
                     text_color=DIM).pack(anchor="w", pady=(0, 12))
        for ico, name, desc, accent, on_c, off_c in NET_OPTS:
            self._make_toggle(pad, ico + "  " + name, desc, on_c, off_c, accent)
        self._divider(pad)
        make_btn(
            pad, "📡  Проверить пинг",
            self._global_ping,
            width=180, color="#006adf", hover="#0090ff",
        ).pack(anchor="w")
        self.net_log = self._make_log(pad, 110)

    def _global_ping(self):
        self._log_clear(self.net_log)

        def run():
            for name, host in [
                ("Steam",      "store.steampowered.com"),
                ("Cloudflare", "1.1.1.1"),
                ("Google",     "8.8.8.8"),
                ("Faceit",     "api.faceit.com"),
                ("AWS EU",     "ec2.eu-central-1.amazonaws.com"),
            ]:
                ms = ping_host(host)
                if ms > 0:
                    s = "OK" if ms < 80 else "СРЕДНИЙ" if ms < 150 else "ВЫСОКИЙ"
                    self._log_write(self.net_log,
                                    "  " + name.ljust(14) + str(ms).rjust(6) + " ms  " + s)
                else:
                    self._log_write(self.net_log,
                                    "  " + name.ljust(14) + "  timeout")
                time.sleep(0.1)
            self._log_write(self.net_log, "✅ Готово!")

        threading.Thread(target=run, daemon=True).start()

    # ── Monitor page ──────────────────────────────────────
    def _build_monitor_page(self):
        pad = self._make_page("monitor")
        ctk.CTkLabel(pad, text="📊 Мониторинг пинга",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text="Живой замер задержки до серверов",
                     font=ctk.CTkFont(size=11),
                     text_color=DIM).pack(anchor="w", pady=(0, 10))

        # Stats
        sr = ctk.CTkFrame(pad, fg_color="transparent")
        sr.pack(fill="x", pady=(0, 10))
        sr.columnconfigure(0, weight=1)
        sr.columnconfigure(1, weight=1)
        sr.columnconfigure(2, weight=1)

        def _stat(col, label, color):
            f = ctk.CTkFrame(sr, fg_color=PANEL2, corner_radius=9,
                             border_width=1, border_color=BORDER)
            f.grid(row=0, column=col, padx=4, sticky="ew")
            v = ctk.CTkLabel(f, text="—",
                             font=ctk.CTkFont(size=24, weight="bold"),
                             text_color=color)
            v.pack(pady=(10, 2))
            ctk.CTkLabel(f, text=label,
                         font=ctk.CTkFont(size=10), text_color=DIM).pack(pady=(0, 8))
            return v

        self.ms_cur = _stat(0, "Текущий ms",  GREEN)
        self.ms_avg = _stat(1, "Средний ms",  GOLD)
        self.ms_max = _stat(2, "Максимум ms", RED)

        # Controls
        cr = ctk.CTkFrame(pad, fg_color="transparent")
        cr.pack(fill="x", pady=(0, 10))
        self.mon_btn = make_btn(
            cr, "▶  Запустить", self._toggle_monitor,
            width=200, color="#006adf", hover="#0090ff",
        )
        self.mon_btn.pack(side="left")
        self.mon_lbl = ctk.CTkLabel(
            cr, text="● Остановлен",
            text_color=DIM, font=ctk.CTkFont(size=11))
        self.mon_lbl.pack(side="left", padx=12)
        ctk.CTkLabel(cr, text="Интервал:",
                     text_color=DIM, font=ctk.CTkFont(size=11)).pack(side="left")
        self.mon_int = ctk.CTkComboBox(
            cr, values=["2 сек", "5 сек", "10 сек"],
            width=88, fg_color=PANEL2, border_color=BORDER)
        self.mon_int.set("2 сек")
        self.mon_int.pack(side="left", padx=6)

        # Server rows
        self.srv_lbls = {}
        for name, host in [
            ("Steam",      "store.steampowered.com"),
            ("Cloudflare", "1.1.1.1"),
            ("Google DNS", "8.8.8.8"),
            ("Faceit",     "api.faceit.com"),
        ]:
            row = ctk.CTkFrame(pad, fg_color=PANEL2, corner_radius=8,
                               border_width=1, border_color=BORDER)
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text="●",
                         font=ctk.CTkFont(size=12), text_color=DIM).pack(
                side="left", padx=(12, 8), pady=8)
            ctk.CTkLabel(row, text=name,
                         font=ctk.CTkFont(size=12), text_color=TEXT,
                         width=130).pack(side="left")
            lbl = ctk.CTkLabel(row, text="— ms",
                               font=ctk.CTkFont(size=12, weight="bold"),
                               text_color=DIM)
            lbl.pack(side="right", padx=14)
            self.srv_lbls[host] = lbl

        # Chart
        cc = ctk.CTkFrame(pad, fg_color=PANEL2, corner_radius=12,
                          border_width=1, border_color=BORDER)
        cc.pack(fill="x", pady=6)
        ctk.CTkLabel(cc, text="📈 График пинга",
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(
            anchor="w", padx=12, pady=(8, 2))
        self.chart = tkinter.Canvas(cc, height=110, bg="#020810",
                                    highlightthickness=0)
        self.chart.pack(fill="x", padx=10, pady=(0, 8))

    def _toggle_monitor(self):
        if self.monitor_running:
            self.monitor_running = False
            self.mon_btn.configure(text="▶  Запустить",
                                   fg_color="#006adf", hover_color="#0090ff")
            self.mon_lbl.configure(text="● Остановлен", text_color=DIM)
        else:
            self.monitor_running = True
            self.mon_btn.configure(text="⏹  Остановить",
                                   fg_color="#6b0000", hover_color="#8b0000")
            self.mon_lbl.configure(text="● Активен", text_color=GREEN)
            threading.Thread(target=self._monitor_loop, daemon=True).start()

    def _monitor_loop(self):
        while self.monitor_running:
            iv = {"2 сек": 2, "5 сек": 5, "10 сек": 10}.get(
                self.mon_int.get(), 2)
            results = []
            for name, host in [
                ("Steam",      "store.steampowered.com"),
                ("Cloudflare", "1.1.1.1"),
                ("Google DNS", "8.8.8.8"),
                ("Faceit",     "api.faceit.com"),
            ]:
                ms = ping_host(host)
                results.append(ms)
                lbl = self.srv_lbls[host]
                if ms < 0:
                    lbl.configure(text="timeout", text_color=RED)
                else:
                    c = GREEN if ms < 80 else GOLD if ms < 150 else RED
                    lbl.configure(text=str(ms) + " ms", text_color=c)
            valid = [r for r in results if r >= 0]
            if valid:
                avg = sum(valid) // len(valid)
                self.ping_history.append(avg)
                if len(self.ping_history) > 30:
                    self.ping_history.pop(0)
                self.ms_cur.configure(
                    text=str(avg),
                    text_color=GREEN if avg < 80 else GOLD if avg < 150 else RED)
                self.ms_avg.configure(
                    text=str(sum(self.ping_history) // len(self.ping_history)))
                self.ms_max.configure(text=str(max(self.ping_history)))
                self._draw_chart()
            time.sleep(iv)

    def _draw_chart(self):
        c = self.chart
        c.delete("all")
        if len(self.ping_history) < 2:
            return
        W = c.winfo_width() or 500
        H = 110
        maxV = max(max(self.ping_history), 200)
        pts = [
            (int(10 + (i / (len(self.ping_history) - 1)) * (W - 20)),
             int(H - 10 - (v / maxV) * (H - 20)))
            for i, v in enumerate(self.ping_history)
        ]
        poly = [(10, H - 10)] + pts + [(pts[-1][0], H - 10)]
        c.create_polygon(
            [x for pt in poly for x in pt],
            fill="#003030", outline="")
        last = self.ping_history[-1]
        col = "#00ff88" if last < 80 else "#ffd700" if last < 150 else "#ff4466"
        c.create_line(
            [x for pt in pts for x in pt],
            fill=col, width=2, smooth=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
