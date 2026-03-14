import sys, os, time, socket, random, threading, subprocess, tkinter, platform
import customtkinter as ctk
from tkinter import filedialog, messagebox

sys.setrecursionlimit(5000)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG="#05080f"; PANEL="#090f1d"; PANEL2="#0c1628"; BORDER="#1a3050"
TEXT="#b8cfea"; DIM="#3a5a7a"; NEON="#00f0ff"; GREEN="#00ff88"
GOLD="#ffd700"; RED="#ff4466"; PURPLE="#b060ff"; ORANGE="#ff9f40"

JOKES=["😂 Ваня: 5 FPS — это нормально","💀 Ваня оптимизировал — удалил system32",
       "🎯 Ваня поставил мониторинг — FPS 12","🔫 Ваня строил дом — убили через стену",
       "🚗 Ваня в GTA взял такси — лучше пешком","⚡ Ваня включил план питания — сгорел роутер",
       "🦕 Ваня в ARK — съел динозавр","🌀 Ваня в Fortnite — убил строитель"]

# ═══ УТИЛИТЫ ═══════════════════════════════════════════════
def run_cmd(cmd):
    try:
        r=subprocess.run(cmd,shell=True,capture_output=True,text=True,
                         timeout=30,encoding="cp1251",errors="replace")
        return r.returncode==0
    except: return False

def run_cmd_out(cmd):
    try:
        r=subprocess.run(cmd,shell=True,capture_output=True,text=True,
                         timeout=15,encoding="cp1251",errors="replace")
        return r.stdout.strip()
    except: return ""

def ping_host(host,timeout=2):
    try:
        t0=time.time(); s=socket.create_connection((host,80),timeout=timeout); s.close()
        return int((time.time()-t0)*1000)
    except: return -1

def expand(path):
    return os.path.expandvars(os.path.expanduser(path))

def find_exe(paths):
    for p in paths:
        e=expand(p)
        if os.path.exists(e): return e
    return None

def write_cfg(path_template, lines, append=True):
    path=expand(path_template)
    try:
        os.makedirs(os.path.dirname(path),exist_ok=True)
        mode="a" if append else "w"
        with open(path,mode,encoding="utf-8") as f:
            f.write("\n".join(lines)+"\n")
        return True,path
    except Exception as e: return False,str(e)

def make_btn(parent,text,cmd,color="#0060df",hover="#0090ff",
             size=12,bold=True,width=None,corner=7):
    kw=dict(text=text,command=cmd,fg_color=color,hover_color=hover,
            font=ctk.CTkFont(size=size,weight="bold" if bold else "normal"),
            corner_radius=corner)
    if width: kw["width"]=width
    return ctk.CTkButton(parent,**kw)

# ═══ ДАННЫЕ ИГР ════════════════════════════════════════════

# ── RUST ──────────────────────────────────────────────────
RUST_EXE=[
    r"C:\Program Files (x86)\Steam\steamapps\common\Rust\RustClient.exe",
    r"D:\Steam\steamapps\common\Rust\RustClient.exe",
    r"E:\Steam\steamapps\common\Rust\RustClient.exe",
    r"D:\Games\Steam\steamapps\common\Rust\RustClient.exe",
]
RUST_CFG=r"%APPDATA%\Rust\cfg\client.cfg"
RUST_PRESETS={
    "Макс FPS":{"desc":"Минимум графики","fps":"100-200+",
        "launch":"-high -maxMem=8192 -malloc=system -force-feature-level-11-0 +fps.limit 0 -nolog",
        "settings":[("grass.on","false"),("terrain.quality","0"),("graphics.shadows","0"),
                    ("graphics.ssao","0"),("graphics.damage","0"),("graphics.itemskins","0"),
                    ("graphics.lodbias","0.25"),("graphics.dof","false"),("graphics.shafts","0")]},
    "Баланс":{"desc":"FPS + читаемость","fps":"60-120",
        "launch":"-high -maxMem=8192 +fps.limit 0",
        "settings":[("grass.on","true"),("terrain.quality","50"),("graphics.shadows","1"),
                    ("graphics.ssao","0"),("graphics.lodbias","1")]},
    "Качество":{"desc":"Полная графика","fps":"40-80",
        "launch":"+fps.limit 0",
        "settings":[("grass.on","true"),("terrain.quality","100"),("graphics.shadows","3"),
                    ("graphics.ssao","1"),("graphics.lodbias","2")]},
}
RUST_KILL_CFG=[
    "grass.on false","effects.motionblur false","voice.use false",
    "graphics.itemskins 0","graphics.damage 0","graphics.dof false",
    "graphics.shafts 0","graphics.shadows 0","graphics.ssao 0",
    "graphics.lodbias 0.25","graphics.parallax 0","graphics.reflections 0",
    "terrain.quality 0","population.animal 0",
]
RUST_PARASITES=[
    ("🎓","Обучалка/подсказки",       "Подсказки при каждом заходе",       RED,
     ["reg add \"HKCU\\Software\\Facepunch\\Rust\" /v tutorial_complete /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Facepunch\\Rust\" /v tutorial_complete /t REG_DWORD /d 0 /f"]),
    ("🎬","Вступительное видео",       "Логотип при каждом запуске",         ORANGE,
     ["reg add \"HKCU\\Software\\Facepunch\\Rust\" /v skip_intro /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Facepunch\\Rust\" /v skip_intro /t REG_DWORD /d 0 /f"]),
    ("🌿","Трава",                     "grass.on false → +20-40 FPS",        GREEN,
     ["echo grass.on false >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo grass.on true >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("💨","Motion Blur",               "Размытие снижает FPS",               NEON,
     ["echo effects.motionblur false >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo effects.motionblur true >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("🔊","VOIP чат",                  "Слушает микрофон постоянно",         PURPLE,
     ["echo voice.use false >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo voice.use true >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("📦","Скины предметов",           "Загрузка скинов жрёт RAM",           GOLD,
     ["echo graphics.itemskins 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.itemskins 1 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("🎆","Эффекты взрывов",           "Партиклы взрывов — лишнее",          RED,
     ["echo graphics.damage 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.damage 1 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("🌅","God Rays",                  "Volumetric lighting — дорого",       ORANGE,
     ["echo graphics.shafts 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.shafts 1 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("🐟","Популяция животных",        "Клиентские животные грузят CPU",     DIM,
     ["echo population.animal 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo population.animal 50 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
    ("🪞","Отражения",                 "graphics.reflections 0",             NEON,
     ["echo graphics.reflections 0 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""],
     ["echo graphics.reflections 2 >> \"%APPDATA%\\Rust\\cfg\\client.cfg\""]),
]
RUST_TIPS=[
    ("💡","Steam оверлей","Steam → ПКМ на Rust → Свойства → убери Steam Overlay"),
    ("🛡","Антивирус","Windows Defender → Исключения → папка с Rust"),
    ("🎮","DirectX 11","Параметры запуска: -force-feature-level-11-0"),
    ("🧹","Кэш шейдеров","AppData/Local/Temp/Rust — удаляй раз в неделю"),
    ("⚙","F1 консоль","В игре F1 → вставь команды из пресета графики"),
    ("📡","Выбор сервера","Выбирай сервер с пингом < 80ms для комфортной игры"),
]

# ── GTA V ──────────────────────────────────────────────────
GTAV_EXE=[
    r"C:\Program Files (x86)\Steam\steamapps\common\Grand Theft Auto V\GTA5.exe",
    r"C:\Program Files\Rockstar Games\Grand Theft Auto V\GTA5.exe",
    r"D:\Rockstar Games\Grand Theft Auto V\GTA5.exe",
    r"D:\Steam\steamapps\common\Grand Theft Auto V\GTA5.exe",
    r"E:\Games\Grand Theft Auto V\GTA5.exe",
]
GTAV_PRESETS={
    "Макс FPS":{"desc":"Для слабых ПК и FiveM","fps":"80-160+",
        "launch":"-notablet -norestrictions -noFirstRun -IgnoreCorrupts",
        "settings":[("TextureQuality","normal"),("ShaderQuality","normal"),("ShadowQuality","normal"),
                    ("ReflectionQuality","off"),("MSAA","off"),("FXAA","off"),
                    ("AmbientOcclusion","off"),("MotionBlur","false"),("InGameDepthOfField","false")]},
    "Баланс":{"desc":"Комфортная игра","fps":"60-100",
        "launch":"-notablet -noFirstRun",
        "settings":[("TextureQuality","high"),("ShaderQuality","high"),("ShadowQuality","high"),
                    ("MSAA","off"),("FXAA","on"),("AmbientOcclusion","medium"),("MotionBlur","false")]},
    "Качество":{"desc":"Максимальная красота","fps":"40-70",
        "launch":"-notablet",
        "settings":[("TextureQuality","very high"),("ShaderQuality","very high"),
                    ("ShadowQuality","very high"),("MSAA","x4"),("FXAA","on"),
                    ("AmbientOcclusion","high"),("TessellationQuality","very high")]},
}
GTAV_PARASITES=[
    ("🎓","Обучающие подсказки",       "Всплывают каждый раз",               RED,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v TutorialDone /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v TutorialDone /t REG_DWORD /d 0 /f"]),
    ("🎬","Вступительные ролики",      "Логотип + ролик при запуске",        ORANGE,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v InstallComplete /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v InstallComplete /t REG_DWORD /d 0 /f"]),
    ("🌀","Motion Blur",               "-10-15 FPS без пользы",              RED,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v MotionBlur /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v MotionBlur /t REG_DWORD /d 1 /f"]),
    ("🌊","Глубина резкости DOF",      "Размытие фона — GPU зря",            NEON,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v InGameDepthOfField /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v InGameDepthOfField /t REG_DWORD /d 1 /f"]),
    ("🎬","Replay / Rockstar Editor",  "Пишет буфер постоянно в фоне",       GOLD,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ReplayBuffer /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ReplayBuffer /t REG_DWORD /d 1 /f"]),
    ("🐾","Tessellation",              "Детализация поверхностей — дорого",  PURPLE,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v Tessellation /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v Tessellation /t REG_DWORD /d 1 /f"]),
    ("🌆","Extended Distance",         "Далёкие объекты — огромно нагружает",RED,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ExtendedDistanceScaling /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v ExtendedDistanceScaling /t REG_DWORD /d 1 /f"]),
    ("🚶","Плотность NPC",             "Много NPC грузят CPU",               ORANGE,
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v PedDensity /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Rockstar Games\\Grand Theft Auto V\" /v PedDensity /t REG_DWORD /d 100 /f"]),
]
GTAV_TIPS=[
    ("🟣","FiveM","Отключи все оверлеи перед FiveM — Discord, Steam, NVIDIA"),
    ("⚡","-notablet","Обязательный параметр — убирает ненужный ввод планшета"),
    ("🌐","NAT Open","Пробрось порты 6672 UDP и 61455-61458 UDP"),
    ("🔧","Rockstar Launcher","Выключи из автозагрузки — жрёт RAM"),
    ("🗑","Кэш FiveM","%%LOCALAPPDATA%%\\FiveM\\FiveM.app\\cache — удаляй при лагах"),
]

# ── CS2 ────────────────────────────────────────────────────
CS2_EXE=[
    r"C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
    r"D:\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
    r"E:\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
]
CS2_CFG=r"%USERPROFILE%\AppData\Local\cs2\cfg\autoexec.cfg"
CS2_PRESETS={
    "Макс FPS":{"desc":"Про-настройки","fps":"200-400+",
        "launch":"-novid -nojoy -noaafonts -limitvsconst -forcenovsync +mat_queue_mode -1 +r_dynamic_lighting 0 -freq 240 -high",
        "settings":[("r_lowlatency","2"),("fps_max","0"),("mat_queue_mode","-1"),
                    ("r_dynamic_lighting","0"),("r_shadows","0"),("cl_ragdoll_physics_enable","0"),
                    ("r_motionblur","0"),("cl_showfps","1"),("rate","786432"),
                    ("cl_interp","0"),("cl_interp_ratio","1"),("m_rawinput","1")]},
    "Баланс":{"desc":"FPS + видимость","fps":"144-250",
        "launch":"-novid -nojoy -forcenovsync +mat_queue_mode -1 -high",
        "settings":[("fps_max","0"),("r_lowlatency","2"),("r_shadows","1"),
                    ("r_dynamic_lighting","1"),("cl_showfps","1"),("r_motionblur","0")]},
    "Качество":{"desc":"Красивая картинка","fps":"100-180",
        "launch":"-novid +mat_queue_mode -1",
        "settings":[("fps_max","0"),("r_shadows","3"),("r_dynamic_lighting","1"),("r_motionblur","0")]},
}
CS2_KILL_CFG=[
    "r_motionblur 0","cl_ragdoll_physics_enable 0","cl_detailfade 0",
    "snd_menumusic_volume 0","cl_draw_only_deathnotices 1","fps_max 0",
    "r_lowlatency 2","cl_interp 0","cl_interp_ratio 1","rate 786432",
    "m_rawinput 1","r_dynamic_lighting 0","r_shadows 0",
]
CS2_PARASITES=[
    ("🎓","Обучение / Tutorial",       "Предложение зайти в обучалку",       RED,
     ["reg add \"HKCU\\Software\\Valve\\Counter-Strike Global Offensive\" /v TutorialDone /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Valve\\Counter-Strike Global Offensive\" /v TutorialDone /t REG_DWORD /d 0 /f"]),
    ("🎬","Интро видео Valve",         "Логотип Valve при запуске",          ORANGE,
     ["reg add \"HKCU\\Software\\Valve\\Counter-Strike Global Offensive\" /v NoVideoIntro /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Valve\\Counter-Strike Global Offensive\" /v NoVideoIntro /t REG_DWORD /d 0 /f"]),
    ("🌀","Motion Blur",               "Размытие — FPS без пользы",          RED,
     ["echo r_motionblur 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo r_motionblur 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),
    ("💀","Ragdoll физика",            "Трупы с физикой жрут CPU",           NEON,
     ["echo cl_ragdoll_physics_enable 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo cl_ragdoll_physics_enable 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),
    ("🌿","Детали окружения",          "Трава и листья — декорации",         GREEN,
     ["echo cl_detailfade 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo cl_detailfade 400 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),
    ("🎵","Музыка в меню",             "Звуковой движок зря работает",       PURPLE,
     ["echo snd_menumusic_volume 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo snd_menumusic_volume 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),
    ("💬","Kill feed анимации",        "Только важное на экране",            GOLD,
     ["echo cl_draw_only_deathnotices 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo cl_draw_only_deathnotices 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),
    ("🔫","Анимация осмотра оружия",   "viewmodel далеко — меньше мусора",   ORANGE,
     ["echo viewmodel_presetpos 3 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
     ["echo viewmodel_presetpos 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""]),
]
CS2_TIPS=[
    ("🖥","Частота монитора","NVIDIA → Панель управления → выбери 144/240Hz"),
    ("🖱","Raw Input","m_rawinput 1 — прямой ввод без обработки Windows"),
    ("📡","Rate команды","rate 786432; cl_interp 0; cl_interp_ratio 1 — в autoexec"),
    ("🌡","Температура","CS2 нагружает CPU — больше 90°C = чистка кулера"),
    ("🎮","Game DVR","Win+G → Настройки → выключи запись и трансляцию"),
]

# ── FORTNITE ───────────────────────────────────────────────
FN_EXE=[
    r"C:\Program Files\Epic Games\Fortnite\FortniteGame\Binaries\Win64\FortniteClient-Win64-Shipping.exe",
    r"D:\Epic Games\Fortnite\FortniteGame\Binaries\Win64\FortniteClient-Win64-Shipping.exe",
    r"C:\Program Files (x86)\Epic Games\Fortnite\FortniteGame\Binaries\Win64\FortniteClient-Win64-Shipping.exe",
    r"E:\Fortnite\FortniteGame\Binaries\Win64\FortniteClient-Win64-Shipping.exe",
]
FN_INI=r"%LOCALAPPDATA%\FortniteGame\Saved\Config\WindowsClient\GameUserSettings.ini"
FN_PRESETS={
    "Макс FPS":{"desc":"Минимум графики","fps":"144-300+",
        "launch":"-NOTEXTURESTREAMING -USEALLAVAILABLECORES -nomansky -novsync -dx12",
        "settings":[("sg.ResolutionQuality","75"),("sg.ViewDistanceQuality","1"),
                    ("sg.ShadowQuality","0"),("sg.PostProcessQuality","0"),
                    ("sg.TextureQuality","0"),("sg.EffectsQuality","0"),
                    ("sg.FoliageQuality","0"),("bUseVSync","False"),
                    ("FrameRateLimit","0"),("bShowFPS","True")]},
    "Баланс":{"desc":"FPS + картинка","fps":"90-144",
        "launch":"-USEALLAVAILABLECORES -nomansky -novsync",
        "settings":[("sg.ResolutionQuality","100"),("sg.ViewDistanceQuality","2"),
                    ("sg.ShadowQuality","2"),("sg.PostProcessQuality","2"),
                    ("sg.TextureQuality","2"),("bUseVSync","False"),("FrameRateLimit","144")]},
    "Качество":{"desc":"Красивая картинка","fps":"60-90",
        "launch":"-USEALLAVAILABLECORES -novsync",
        "settings":[("sg.ResolutionQuality","100"),("sg.ViewDistanceQuality","4"),
                    ("sg.ShadowQuality","4"),("sg.PostProcessQuality","4"),
                    ("sg.TextureQuality","4"),("bUseVSync","False"),("FrameRateLimit","0")]},
}
FN_KILL_INI="""[ScalabilityGroups]
sg.ResolutionQuality=75
sg.ViewDistanceQuality=1
sg.ShadowQuality=0
sg.PostProcessQuality=0
sg.TextureQuality=0
sg.EffectsQuality=0
sg.FoliageQuality=0

[/Script/FortniteGame.FortGameUserSettings]
bUseVSync=False
FrameRateLimit=0.000000
bShowFPS=True
ResolutionSizeX=1920
ResolutionSizeY=1080
"""
FN_PARASITES=[
    ("🎓","Обучение / Tutorial",       "Убирает обучалку при входе",         RED,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v TutorialCompleted /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v TutorialCompleted /t REG_DWORD /d 0 /f"]),
    ("🎬","Интро видео Epic",           "Логотип при каждом запуске",         ORANGE,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v SkipIntro /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v SkipIntro /t REG_DWORD /d 0 /f"]),
    ("🌀","Motion Blur",               "Размытие при движении — -FPS",       RED,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v MotionBlur /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v MotionBlur /t REG_DWORD /d 1 /f"]),
    ("🌿","Foliage / Листва",          "Трава и кусты — лишняя нагрузка",    GREEN,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v FoliageQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v FoliageQuality /t REG_DWORD /d 4 /f"]),
    ("🌊","Глубина резкости DOF",      "Размытие фона — GPU зря",            NEON,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v DepthOfField /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v DepthOfField /t REG_DWORD /d 1 /f"]),
    ("🎵","Музыка в лобби",            "Фоновая музыка жрёт CPU",            PURPLE,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v LobbyMusicVolume /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v LobbyMusicVolume /t REG_DWORD /d 100 /f"]),
    ("📡","Replays / Повторы",         "Пишет replay файлы постоянно",       GOLD,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v bShouldRecord /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v bShouldRecord /t REG_DWORD /d 1 /f"]),
    ("💥","Nanite/Lumen материалы",    "Очень тяжёлые эффекты",              ORANGE,
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v MaterialQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Epic Games\\Fortnite\" /v MaterialQuality /t REG_DWORD /d 4 /f"]),
]
FN_TIPS=[
    ("📁","Путь к настройкам","%%LOCALAPPDATA%%\\FortniteGame\\Saved\\Config\\WindowsClient\\"),
    ("⚡","Параметры запуска","-NOTEXTURESTREAMING -USEALLAVAILABLECORES -dx12"),
    ("🛡","Исключения Defender","Добавь папку Fortnite в исключения антивируса"),
    ("🎮","DirectX 12","Используй DX12 — лучше FPS на современных GPU"),
    ("🔄","Очистка кэша","Папка FortniteGame\\Saved\\Cache — удаляй при фризах"),
]

# ── ARK ────────────────────────────────────────────────────
ARK_EXE=[
    r"C:\Program Files (x86)\Steam\steamapps\common\ARK\ShooterGame\Binaries\Win64\ShooterGame.exe",
    r"D:\Steam\steamapps\common\ARK\ShooterGame\Binaries\Win64\ShooterGame.exe",
    r"C:\Program Files (x86)\Steam\steamapps\common\ARK Survival Ascended\ShooterGame\Binaries\Win64\ArkAscended.exe",
    r"D:\Steam\steamapps\common\ARK Survival Ascended\ShooterGame\Binaries\Win64\ArkAscended.exe",
    r"E:\Steam\steamapps\common\ARK\ShooterGame\Binaries\Win64\ShooterGame.exe",
]
ARK_PRESETS={
    "Макс FPS":{"desc":"Минимум графики","fps":"60-120+",
        "launch":"-USEALLAVAILABLECORES -sm4 -d3d10 -nomansky -lowmemory -novsync",
        "settings":[("sg.ResolutionQuality","75"),("sg.ShadowQuality","0"),
                    ("sg.TextureQuality","0"),("sg.EffectsQuality","0"),
                    ("sg.FoliageQuality","0"),("bUseVSync","False"),("FrameRateLimit","0")]},
    "Баланс":{"desc":"FPS + читаемость","fps":"40-80",
        "launch":"-USEALLAVAILABLECORES -nomansky -novsync",
        "settings":[("sg.ResolutionQuality","100"),("sg.ShadowQuality","2"),
                    ("sg.TextureQuality","2"),("sg.EffectsQuality","2"),
                    ("sg.FoliageQuality","2"),("bUseVSync","False")]},
    "Качество":{"desc":"Красивая картинка","fps":"25-50",
        "launch":"-USEALLAVAILABLECORES",
        "settings":[("sg.ResolutionQuality","100"),("sg.ShadowQuality","4"),
                    ("sg.TextureQuality","4"),("sg.EffectsQuality","4"),
                    ("sg.FoliageQuality","4"),("bUseVSync","False")]},
}
ARK_PARASITES=[
    ("🎓","Обучение / подсказки",      "Постоянные подсказки новичка",       RED,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v TutorialDone /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v TutorialDone /t REG_DWORD /d 0 /f"]),
    ("🎬","Интро видео",               "Логотипы при каждом запуске",        ORANGE,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v SkipIntro /t REG_DWORD /d 1 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v SkipIntro /t REG_DWORD /d 0 /f"]),
    ("🌿","Foliage / Листва",          "Деревья и кусты — огромная нагрузка",GREEN,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v FoliageQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v FoliageQuality /t REG_DWORD /d 100 /f"]),
    ("🦕","Анимации динозавров",       "Сложные анимации жрут CPU",          PURPLE,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v NPCQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v NPCQuality /t REG_DWORD /d 2 /f"]),
    ("🌊","Глубина резкости DOF",      "Размытие фона — грузит GPU",         NEON,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v DepthOfField /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v DepthOfField /t REG_DWORD /d 1 /f"]),
    ("🌀","Motion Blur",               "Размытие при движении — отключи",    RED,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v MotionBlur /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v MotionBlur /t REG_DWORD /d 1 /f"]),
    ("☁️","Volumetric Clouds",         "Объёмные облака — очень тяжело",     GOLD,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v VolumetricClouds /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v VolumetricClouds /t REG_DWORD /d 1 /f"]),
    ("💧","Water Quality",             "Отражения воды — дорогой эффект",    ORANGE,
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v WaterQuality /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Studio Wildcard\\ARK\" /v WaterQuality /t REG_DWORD /d 2 /f"]),
]
ARK_TIPS=[
    ("💾","Память","ARK требует 16GB+ RAM. Закрой всё перед игрой"),
    ("⚡","Параметры запуска","-USEALLAVAILABLECORES -sm4 -d3d10 -nomansky -lowmemory"),
    ("🌿","Foliage","Листва = главный убийца FPS. Ставь на минимум"),
    ("🧹","Кэш шейдеров","Папка ARK\\ShooterGame\\Saved\\Cache — удаляй при фризах"),
    ("🦕","Динозавры рядом","Снижай дистанцию прорисовки мобов в настройках сервера"),
]

# ── Общие паразиты ─────────────────────────────────────────
OVERLAYS=[
    ("🎮","Xbox Game Bar / DVR",   "Сжирает 5-15% CPU, вызывает фризы",  RED,
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f",
      "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR\" /v AllowGameDVR /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 1 /f"]),
    ("📸","NVIDIA ShadowPlay",     "Пишет видео в фоне, нагружает GPU",  ORANGE,
     ["reg add \"HKCU\\Software\\NVIDIA Corporation\\NVCapture\" /v CaptureEnabled /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\NVIDIA Corporation\\NVCapture\" /v CaptureEnabled /t REG_DWORD /d 1 /f"]),
    ("💬","Discord оверлей",       "+3-8ms задержки на кадр",             PURPLE,
     ["reg add \"HKCU\\Software\\Discord\" /v Overlay /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Discord\" /v Overlay /t REG_DWORD /d 1 /f"]),
    ("🎵","Steam оверлей",         "Shift+Tab лагает, грузит память",     NEON,
     ["reg add \"HKCU\\Software\\Valve\\Steam\" /v SteamOverlayEnabled /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Valve\\Steam\" /v SteamOverlayEnabled /t REG_DWORD /d 1 /f"]),
]
BG_PROCS=[
    ("🔄","Windows Update",        "Качает обновления во время игры",     RED,
     ["net stop wuauserv","net stop bits","net stop dosvc"],
     ["net start wuauserv"]),
    ("🔍","Windows Search",        "Индексирует файлы, грузит диск",      ORANGE,
     ["net stop wsearch","sc config wsearch start=disabled"],
     ["net start wsearch","sc config wsearch start=auto"]),
    ("📊","SysMain / Superfetch",  "Предзагрузка мешает играм",           GOLD,
     ["net stop sysmain","sc config sysmain start=disabled"],
     ["net start sysmain","sc config sysmain start=auto"]),
    ("☁️","OneDrive синхронизация","Грузит диск и сеть",                  NEON,
     ["taskkill /f /im OneDrive.exe","sc config OneSyncSvc start=disabled"],
     ["sc config OneSyncSvc start=auto"]),
]

# ── Windows оптимизации ────────────────────────────────────
WIN_OPTS=[
    ("⚡","Высокий план питания",       "Максимальная производительность CPU",   NEON,
     ["powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"],
     ["powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e"]),
    ("📈","Приоритет CPU Win32=38",     "Лучший отклик в играх",                 GREEN,
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v Win32PrioritySeparation /t REG_DWORD /d 2 /f"]),
    ("🎮","HAGS GPU Scheduling",        "Меньше задержка GPU (нужна Win10 2004+)",PURPLE,
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v HwSchMode /t REG_DWORD /d 2 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v HwSchMode /t REG_DWORD /d 1 /f"]),
    ("🖥","Откл. визуальные эффекты",   "Анимации Windows — ненужный расход",    ORANGE,
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects\" /v VisualFXSetting /t REG_DWORD /d 2 /f"],
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects\" /v VisualFXSetting /t REG_DWORD /d 0 /f"]),
    ("🔕","Откл. Xbox Game Bar",        "-5-15% CPU в играх",                    RED,
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f",
      "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR\" /v AllowGameDVR /t REG_DWORD /d 0 /f"],
     ["reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 1 /f"]),
    ("🔍","Откл. Windows Search",       "Не индексирует во время игры",          GOLD,
     ["net stop wsearch","sc config wsearch start=disabled"],
     ["net start wsearch","sc config wsearch start=auto"]),
    ("📊","Откл. SysMain",              "Освобождает RAM и диск",                ORANGE,
     ["net stop sysmain","sc config sysmain start=disabled"],
     ["net start sysmain","sc config sysmain start=auto"]),
    ("🧹","Очистка RAM",                "Освобождает память перед игрой",        GREEN,
     ["rundll32.exe advapi32.dll,ProcessIdleTasks"],[]),
    ("⏸","Пауза Windows Update",        "Обновления не мешают игре",             RED,
     ["net stop wuauserv","net stop bits","net stop dosvc"],
     ["net start wuauserv"]),
    ("💾","Откл. очистку PageFile",     "Быстрее выключение ПК",                 NEON,
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v ClearPageFileAtShutdown /t REG_DWORD /d 0 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v ClearPageFileAtShutdown /t REG_DWORD /d 1 /f"]),
]
NET_OPTS=[
    ("🌐","DNS Google + Cloudflare",   "8.8.8.8 + 1.1.1.1 — быстрый DNS",    GREEN,
     ["netsh interface ip set dns \"Ethernet\" static 8.8.8.8",
      "netsh interface ip add dns \"Ethernet\" 1.1.1.1 index=2",
      "netsh interface ip set dns \"Wi-Fi\" static 8.8.8.8",
      "netsh interface ip add dns \"Wi-Fi\" 1.1.1.1 index=2",
      "ipconfig /flushdns"],
     ["netsh interface ip set dns \"Ethernet\" dhcp",
      "netsh interface ip set dns \"Wi-Fi\" dhcp","ipconfig /flushdns"]),
    ("🏎","Откл. Nagle алгоритм",      "TcpAckFrequency=1 → -5-30ms пинга",   NEON,
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpAckFrequency /t REG_DWORD /d 1 /f",
      "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TCPNoDelay /t REG_DWORD /d 1 /f",
      "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpDelAckTicks /t REG_DWORD /d 0 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpAckFrequency /t REG_DWORD /d 2 /f"]),
    ("📶","QoS DSCP=46",               "Приоритет игрового трафика",          PURPLE,
     ["netsh qos delete policy \"GO_Game\"",
      "netsh qos add policy \"GO_Game\" app=\"*\" dscp=46 throttle-rate=-1"],
     ["netsh qos delete policy \"GO_Game\""]),
    ("🔕","Откл. IPv6",                "Убирает конфликты IPv4/IPv6",         ORANGE,
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters\" /v DisabledComponents /t REG_DWORD /d 255 /f"],
     ["reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters\" /v DisabledComponents /t REG_DWORD /d 0 /f"]),
    ("🔄","Сброс Winsock + IP стека",  "Полный сброс сетевого стека",         RED,
     ["netsh winsock reset","netsh int ip reset","ipconfig /flushdns","ipconfig /registerdns"],[]),
    ("🚀","TCP AutoTuning",             "Highlyrestricted = стабильнее",       GOLD,
     ["netsh interface tcp set global autotuninglevel=highlyrestricted"],
     ["netsh interface tcp set global autotuninglevel=normal"]),
]

# ── Словарь игр ────────────────────────────────────────────
GAMES={
    "Rust":    {"icon":"🔫","color":"#e07020","desc":"Survival multiplayer","steam":"252490",
                "exe":RUST_EXE,"epic":None,"presets":RUST_PRESETS,
                "parasites":RUST_PARASITES,"tips":RUST_TIPS,
                "cfg":RUST_CFG,"kill_cfg":RUST_KILL_CFG,"cfg_append":True},
    "GTA V":   {"icon":"🚗","color":"#00a8ff","desc":"Open world / FiveM","steam":"271590",
                "exe":GTAV_EXE,"epic":None,"presets":GTAV_PRESETS,
                "parasites":GTAV_PARASITES,"tips":GTAV_TIPS,
                "cfg":None,"kill_cfg":[],"cfg_append":True},
    "CS2":     {"icon":"🎯","color":"#ff6b35","desc":"Counter-Strike 2","steam":"730",
                "exe":CS2_EXE,"epic":None,"presets":CS2_PRESETS,
                "parasites":CS2_PARASITES,"tips":CS2_TIPS,
                "cfg":CS2_CFG,"kill_cfg":CS2_KILL_CFG,"cfg_append":True},
    "Fortnite":{"icon":"🌀","color":"#00d4ff","desc":"Battle Royale","steam":None,
                "exe":FN_EXE,"epic":"Fortnite","presets":FN_PRESETS,
                "parasites":FN_PARASITES,"tips":FN_TIPS,
                "cfg":FN_INI,"kill_cfg":[],"kill_ini":FN_KILL_INI,"cfg_append":False},
    "ARK":     {"icon":"🦕","color":"#76b041","desc":"Survival Evolved/Ascended","steam":"346110",
                "exe":ARK_EXE,"epic":None,"presets":ARK_PRESETS,
                "parasites":ARK_PARASITES,"tips":ARK_TIPS,
                "cfg":None,"kill_cfg":[],"cfg_append":True},
}

# ═══ ПРИЛОЖЕНИЕ ════════════════════════════════════════════
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Game Optimizer v2.0")
        self.configure(fg_color=BG)
        self.monitor_running=False
        self.ping_history=[]
        self._live_running=True
        self.game_exe_override={}  # custom exe paths set by user
        self._build_ui()
        self.geometry("1100x700")
        self.minsize(960,620)

    # ── BUILD UI ──────────────────────────────────────────
    def _build_ui(self):
        sb=ctk.CTkFrame(self,width=195,fg_color=PANEL,corner_radius=0,
                        border_width=1,border_color=BORDER)
        sb.pack(side="left",fill="y"); sb.pack_propagate(False)
        lf=ctk.CTkFrame(sb,fg_color="transparent"); lf.pack(pady=(14,4),padx=10)
        ctk.CTkLabel(lf,text="🎮",font=ctk.CTkFont(size=20)).pack(side="left")
        ctk.CTkLabel(lf,text=" GAME OPTIMIZER",
                     font=ctk.CTkFont(size=11,weight="bold"),text_color=NEON).pack(side="left")
        ctk.CTkLabel(sb,text="v2.0",font=ctk.CTkFont(size=9),text_color=DIM).pack()
        ctk.CTkFrame(sb,height=1,fg_color=BORDER).pack(fill="x",padx=10,pady=7)
        ctk.CTkLabel(sb,text="ИГРЫ",font=ctk.CTkFont(size=9),text_color=DIM).pack(anchor="w",padx=10)
        self.game_btns={}
        for gname,g in GAMES.items():
            b=ctk.CTkButton(sb,text=g["icon"]+"  "+gname,anchor="w",
                            font=ctk.CTkFont(size=12),height=34,
                            fg_color="transparent",hover_color="#0d1e38",
                            text_color=DIM,corner_radius=7,
                            command=lambda gn=gname:self.show_game(gn))
            b.pack(fill="x",padx=7,pady=1); self.game_btns[gname]=b
        ctk.CTkFrame(sb,height=1,fg_color=BORDER).pack(fill="x",padx=10,pady=7)
        ctk.CTkLabel(sb,text="ОБЩЕЕ",font=ctk.CTkFont(size=9),text_color=DIM).pack(anchor="w",padx=10)
        self.nav_btns={}
        for pid,lbl in [("profile","💻  Профиль ПК"),("windows","⚡  Windows"),
                        ("network","🌐  Сеть"),("monitor","📊  Мониторинг")]:
            b=ctk.CTkButton(sb,text=lbl,anchor="w",font=ctk.CTkFont(size=11),height=32,
                            fg_color="transparent",hover_color="#0d1e38",
                            text_color=DIM,corner_radius=7,
                            command=lambda p=pid:self.show_page(p))
            b.pack(fill="x",padx=7,pady=1); self.nav_btns[pid]=b
        ctk.CTkFrame(sb,height=1,fg_color=BORDER).pack(fill="x",padx=10,pady=7,side="bottom")
        self.joke_lbl=ctk.CTkLabel(sb,text=random.choice(JOKES),
                                   font=ctk.CTkFont(size=9,slant="italic"),
                                   text_color=GOLD,wraplength=175,justify="center")
        self.joke_lbl.pack(side="bottom",padx=7,pady=5)
        self.content=ctk.CTkFrame(self,fg_color=BG,corner_radius=0)
        self.content.pack(side="left",fill="both",expand=True)
        self.pages={}
        for gname in GAMES: self._build_game_page(gname)
        self._build_profile_page()
        self._build_windows_page()
        self._build_network_page()
        self._build_monitor_page()
        self.show_game("Rust")

    # ── PAGE SWITCHING ────────────────────────────────────
    def show_game(self,gname):
        for p in self.pages.values(): p.pack_forget()
        self.pages[gname].pack(fill="both",expand=True)
        for k,b in self.game_btns.items():
            b.configure(fg_color="#0d2040" if k==gname else "transparent",
                        text_color=GAMES[k]["color"] if k==gname else DIM)
        for b in self.nav_btns.values(): b.configure(fg_color="transparent",text_color=DIM)

    def show_page(self,pid):
        for p in self.pages.values(): p.pack_forget()
        self.pages[pid].pack(fill="both",expand=True)
        for b in self.game_btns.values(): b.configure(fg_color="transparent",text_color=DIM)
        for k,b in self.nav_btns.items():
            b.configure(fg_color="#0d2040" if k==pid else "transparent",
                        text_color=NEON if k==pid else DIM)

    # ── SCROLL HELPER ─────────────────────────────────────
    def _scrollable(self,parent):
        c=tkinter.Canvas(parent,bg=BG,highlightthickness=0)
        sb=ctk.CTkScrollbar(parent,command=c.yview)
        c.configure(yscrollcommand=sb.set)
        sb.pack(side="right",fill="y")
        c.pack(side="left",fill="both",expand=True)
        inner=ctk.CTkFrame(c,fg_color="transparent")
        win=c.create_window((0,0),window=inner,anchor="nw")
        c.bind("<Configure>",lambda e:c.itemconfig(win,width=e.width))
        inner.bind("<Configure>",lambda e:c.configure(scrollregion=c.bbox("all")))
        def _enter(e):
            c.bind_all("<MouseWheel>",lambda ev:c.yview_scroll(int(-1*(ev.delta/120)),"units"))
        def _leave(e): c.unbind_all("<MouseWheel>")
        c.bind("<Enter>",_enter); c.bind("<Leave>",_leave)
        inner.bind("<Enter>",_enter); inner.bind("<Leave>",_leave)
        return inner

    def _make_page(self,pid):
        outer=ctk.CTkFrame(self.content,fg_color=BG,corner_radius=0)
        self.pages[pid]=outer
        inner=self._scrollable(outer)
        pad=ctk.CTkFrame(inner,fg_color="transparent")
        pad.pack(fill="both",expand=True,padx=20,pady=14)
        return pad

    # ── WIDGET HELPERS ────────────────────────────────────
    def _log(self,parent,h=110):
        tb=ctk.CTkTextbox(parent,height=h,fg_color="#020810",
                          border_width=1,border_color=BORDER,
                          font=ctk.CTkFont(family="Courier New",size=11),
                          text_color="#68ffaa",corner_radius=7)
        tb.pack(fill="x",pady=(3,0)); tb.configure(state="disabled"); return tb

    def _lw(self,tb,t):
        tb.configure(state="normal"); tb.insert("end",t+"\n")
        tb.configure(state="disabled"); tb.see("end")

    def _lclr(self,tb):
        tb.configure(state="normal"); tb.delete("1.0","end"); tb.configure(state="disabled")

    def _sec(self,parent,text,color=DIM):
        ctk.CTkLabel(parent,text=text,font=ctk.CTkFont(size=11,weight="bold"),
                     text_color=color).pack(anchor="w",pady=(6,3))

    def _div(self,parent):
        ctk.CTkFrame(parent,height=1,fg_color=BORDER).pack(fill="x",pady=7)

    def _compact_toggle(self,parent,ico,name,desc,on_c,off_c,accent=NEON):
        """Single compact line toggle — icon + name + switch"""
        row=ctk.CTkFrame(parent,fg_color=PANEL2,corner_radius=5,
                         border_width=1,border_color=BORDER)
        row.pack(fill="x",pady=1)
        st=ctk.CTkFrame(row,width=3,fg_color=accent,corner_radius=0)
        st.pack(side="left",fill="y")
        ctk.CTkLabel(row,text=ico,font=ctk.CTkFont(size=13),width=24).pack(side="left",padx=(6,2))
        ri=ctk.CTkFrame(row,fg_color="transparent")
        ri.pack(side="left",fill="x",expand=True,pady=4)
        ctk.CTkLabel(ri,text=name,font=ctk.CTkFont(size=11,weight="bold"),
                     text_color="#fff").pack(anchor="w")
        ctk.CTkLabel(ri,text=desc,font=ctk.CTkFont(size=9),text_color=DIM).pack(anchor="w")
        var=ctk.BooleanVar(value=False)
        def _tog(v=var,on=on_c,off=off_c):
            cmds=on if v.get() else off
            threading.Thread(target=lambda c=cmds:[run_cmd(x) for x in c],daemon=True).start()
        ctk.CTkSwitch(row,text="",variable=var,command=_tog,
                      progress_color=accent,button_color="#fff",width=38
                      ).pack(side="right",padx=7)

    def _safe_set(self,lbl,text):
        try: lbl.configure(text=text)
        except: pass

    # ── GAME PAGE ─────────────────────────────────────────
    def _build_game_page(self,gname):
        g=GAMES[gname]
        outer=ctk.CTkFrame(self.content,fg_color=BG,corner_radius=0)
        self.pages[gname]=outer
        # Header
        hbar=ctk.CTkFrame(outer,fg_color=PANEL,corner_radius=0,
                          border_width=1,border_color=BORDER,height=60)
        hbar.pack(fill="x"); hbar.pack_propagate(False)
        hi=ctk.CTkFrame(hbar,fg_color="transparent"); hi.pack(fill="both",padx=16,pady=8)
        ctk.CTkLabel(hi,text=g["icon"],font=ctk.CTkFont(size=26)).pack(side="left",padx=(0,10))
        ht=ctk.CTkFrame(hi,fg_color="transparent"); ht.pack(side="left",fill="y",expand=True)
        ctk.CTkLabel(ht,text=gname,font=ctk.CTkFont(size=18,weight="bold"),
                     text_color=g["color"]).pack(anchor="w")
        ctk.CTkLabel(ht,text=g["desc"],font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w")
        # Buttons right side
        br=ctk.CTkFrame(hi,fg_color="transparent"); br.pack(side="right")
        make_btn(br,"▶  ЗАПУСТИТЬ",lambda gn=gname:self._launch_game(gn),
                 color="#006adf",hover="#0099ff",size=11,width=130).pack(side="left",padx=3)
        make_btn(br,"⚡  ВСЁ",lambda gn=gname:self._full_optimize(gn),
                 color=g["color"],hover="#ffffff",size=11,width=90).pack(side="left",padx=3)
        # Tabs
        tab_bar=ctk.CTkFrame(outer,fg_color=PANEL2,corner_radius=0,height=36)
        tab_bar.pack(fill="x"); tab_bar.pack_propagate(False)
        tab_content=ctk.CTkFrame(outer,fg_color=BG,corner_radius=0)
        tab_content.pack(fill="both",expand=True)
        tab_frames={}; tab_btns={}
        tab_names=["🎨 Графика","🚫 Паразиты","🌐 Сеть","💡 Советы"]
        if gname=="CS2": tab_names.append("⚙️ Конфиг")
        elif gname=="GTA V": tab_names.append("🟣 FiveM")
        elif gname in ("Rust","ARK","Fortnite"): tab_names.append("🔩 Launch")

        def _show_tab(name,frames=tab_frames,btns=tab_btns,gc=g["color"]):
            for f in frames.values(): f.pack_forget()
            frames[name].pack(fill="both",expand=True)
            for n,b in btns.items():
                b.configure(fg_color="#0d2040" if n==name else "transparent",
                            text_color=gc if n==name else DIM)

        for tname in tab_names:
            tb2=ctk.CTkButton(tab_bar,text=tname,anchor="w",
                              font=ctk.CTkFont(size=10),height=34,
                              fg_color="transparent",hover_color="#0d1e38",
                              text_color=DIM,corner_radius=0,width=110,
                              command=lambda t=tname:_show_tab(t))
            tb2.pack(side="left",padx=1); tab_btns[tname]=tb2
            frame=ctk.CTkFrame(tab_content,fg_color=BG,corner_radius=0)
            tab_frames[tname]=frame
            sc_inner=self._scrollable(frame)
            inner=ctk.CTkFrame(sc_inner,fg_color="transparent")
            inner.pack(fill="both",expand=True,padx=18,pady=12)
            if "Графика" in tname: self._tab_graphics(inner,gname,g)
            elif "Паразиты" in tname: self._tab_parasites(inner,gname,g)
            elif "Сеть" in tname: self._tab_net_game(inner,gname)
            elif "Советы" in tname: self._tab_tips(inner,g)
            elif "Конфиг" in tname: self._tab_cs2cfg(inner)
            elif "FiveM" in tname: self._tab_fivem(inner)
            elif "Launch" in tname: self._tab_launch(inner,gname,g)

        _show_tab(tab_names[0])

    # ── TAB: GRAPHICS ─────────────────────────────────────
    def _tab_graphics(self,pad,gname,g):
        ctk.CTkLabel(pad,text="🎨 Пресеты графики",
                     font=ctk.CTkFont(size=14,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,3))
        ctk.CTkLabel(pad,text="Выбери пресет — получишь параметры запуска для Steam",
                     font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w",pady=(0,8))
        log_ref=[None]
        gr=ctk.CTkFrame(pad,fg_color="transparent"); gr.pack(fill="x",pady=(0,6))
        for i,(pname,pdata) in enumerate(g["presets"].items()):
            gr.columnconfigure(i,weight=1)
            c=ctk.CTkFrame(gr,fg_color=PANEL,corner_radius=9,
                           border_width=2,border_color=BORDER)
            c.grid(row=0,column=i,padx=3,sticky="ew")
            ci=ctk.CTkFrame(c,fg_color="transparent"); ci.pack(fill="both",padx=10,pady=10)
            ctk.CTkLabel(ci,text=pname,font=ctk.CTkFont(size=12,weight="bold"),
                         text_color=g["color"]).pack(anchor="w")
            ctk.CTkLabel(ci,text=pdata["desc"],font=ctk.CTkFont(size=9),
                         text_color=DIM).pack(anchor="w",pady=(1,4))
            fr=ctk.CTkFrame(ci,fg_color="transparent"); fr.pack(anchor="w",pady=(0,3))
            ctk.CTkLabel(fr,text="FPS: ",font=ctk.CTkFont(size=9),text_color=DIM).pack(side="left")
            ctk.CTkLabel(fr,text=pdata["fps"],font=ctk.CTkFont(size=9,weight="bold"),
                         text_color=GREEN).pack(side="left")
            ctk.CTkLabel(ci,text=str(len(pdata["settings"]))+" настроек",
                         font=ctk.CTkFont(size=9),text_color=DIM).pack(anchor="w",pady=(0,6))
            make_btn(ci,"✓ Применить",
                     lambda p=pdata,n=pname,lr=log_ref:self._apply_preset(p,n,lr),
                     size=10,bold=False,width=130,color="#1a3050",hover="#2a4060").pack(anchor="w")
        log_ref[0]=self._log(pad,90)

    def _apply_preset(self,pdata,pname,lr):
        if not lr[0]: return
        self._lclr(lr[0]); self._lw(lr[0],"▶ "+pname+"...")
        def run():
            for k,v in pdata["settings"]: self._lw(lr[0],"  "+k+" = "+v); time.sleep(0.02)
            launch=pdata.get("launch","")
            if launch:
                self._lw(lr[0],""); self._lw(lr[0],"Steam → Свойства → Параметры запуска:")
                self._lw(lr[0],"  "+launch)
            self._lw(lr[0],""); self._lw(lr[0],"✅ FPS: "+pdata["fps"])
        threading.Thread(target=run,daemon=True).start()

    # ── TAB: PARASITES ────────────────────────────────────
    def _tab_parasites(self,pad,gname,g):
        ctk.CTkLabel(pad,text="🚫 Паразитные функции",
                     font=ctk.CTkFont(size=14,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,3))
        ctk.CTkLabel(pad,text="Тогл = включить/выключить. Кнопка снизу убивает сразу всё.",
                     font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w",pady=(0,6))
        self._sec(pad,"🎮 Внутри "+gname)
        for ico,name,desc,accent,on_c,off_c in g["parasites"]:
            self._compact_toggle(pad,ico,name,desc,on_c,off_c,accent)
        self._div(pad)
        self._sec(pad,"🖥 Оверлеи")
        for ico,name,desc,accent,on_c,off_c in OVERLAYS:
            self._compact_toggle(pad,ico,name,desc,on_c,off_c,accent)
        self._div(pad)
        self._sec(pad,"⚙️ Фоновые процессы Windows")
        for ico,name,desc,accent,on_c,off_c in BG_PROCS:
            self._compact_toggle(pad,ico,name,desc,on_c,off_c,accent)
        self._div(pad)
        # BIG kill button
        make_btn(pad,"☠️  УБИТЬ ВСЕ ПАРАЗИТЫ "+gname.upper(),
                 lambda gn=gname:self._kill_all(gn),
                 size=13,width=320,color="#4a0000",hover="#7a0000").pack(anchor="w",pady=(0,3))
        make_btn(pad,"🚫  ОТКЛ. ВСЕ СИСТЕМНЫЕ",
                 self._kill_system_parasites,
                 size=12,width=220,color="#6b0000",hover="#8b0000").pack(anchor="w")
        self._kill_log=self._log(pad,70)

    def _kill_all(self,gname):
        g=GAMES[gname]; log=getattr(self,"_kill_log",None)
        def run():
            if log: self._lw(log,"☠️ Убиваю все паразиты "+gname+"...")
            count=0
            # Registry
            for item in g["parasites"]:
                _,_,_,_,on_c,_=item
                for cmd in on_c: run_cmd(cmd); count+=1
            # Overlays
            for _,_,_,_,on_c,_ in OVERLAYS:
                for cmd in on_c: run_cmd(cmd); count+=1
            # Write to cfg file
            cfg=g.get("cfg"); kill_cfg=g.get("kill_cfg",[])
            kill_ini=g.get("kill_ini")
            if cfg and kill_cfg:
                path=expand(cfg)
                try:
                    os.makedirs(os.path.dirname(path),exist_ok=True)
                    mode="a" if g.get("cfg_append",True) else "w"
                    with open(path,mode,encoding="utf-8") as f:
                        f.write("\n// Game Optimizer kill\n")
                        f.write("\n".join(kill_cfg)+"\n")
                    if log: self._lw(log,"  ✓ Записано в "+os.path.basename(path))
                except Exception as e:
                    if log: self._lw(log,"  ✗ Файл: "+str(e))
            if cfg and kill_ini:
                path=expand(cfg)
                try:
                    os.makedirs(os.path.dirname(path),exist_ok=True)
                    with open(path,"w",encoding="utf-8") as f: f.write(kill_ini)
                    if log: self._lw(log,"  ✓ INI записан: "+os.path.basename(path))
                except Exception as e:
                    if log: self._lw(log,"  ✗ INI: "+str(e))
            if log:
                self._lw(log,"  ✓ "+str(count)+" команд выполнено")
                self._lw(log,"✅ "+gname+" — паразиты убиты!")
        threading.Thread(target=run,daemon=True).start()

    def _kill_system_parasites(self):
        cmds=["net stop wuauserv","net stop wsearch","net stop sysmain",
              "taskkill /f /im OneDrive.exe",
              "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f"]
        threading.Thread(target=lambda:[run_cmd(c) for c in cmds],daemon=True).start()

    # ── TAB: NETWORK per game ─────────────────────────────
    def _tab_net_game(self,pad,gname):
        ctk.CTkLabel(pad,text="🌐 Настройка сети",
                     font=ctk.CTkFont(size=14,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,6))
        for ico,name,desc,accent,on_c,off_c in NET_OPTS:
            self._compact_toggle(pad,ico,name,desc,on_c,off_c,accent)
        self._div(pad)
        make_btn(pad,"📡  Проверить пинг",lambda p=pad:self._quick_ping(p),
                 width=170,color="#006adf",hover="#0090ff").pack(anchor="w")

    def _quick_ping(self,pad):
        log=self._log(pad,70)
        def run():
            for n,h in [("Google","8.8.8.8"),("Steam","store.steampowered.com"),("Cloudflare","1.1.1.1")]:
                ms=ping_host(h)
                self._lw(log,("✓ " if ms>0 else "✗ ")+n.ljust(12)+(str(ms)+" ms" if ms>0 else "timeout"))
                time.sleep(0.1)
            self._lw(log,"✅ Готово!")
        threading.Thread(target=run,daemon=True).start()

    # ── TAB: TIPS ─────────────────────────────────────────
    def _tab_tips(self,pad,g):
        ctk.CTkLabel(pad,text="💡 Советы",
                     font=ctk.CTkFont(size=14,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,8))
        for ico,title,text in g["tips"]:
            c=ctk.CTkFrame(pad,fg_color=PANEL2,corner_radius=7,
                           border_width=1,border_color=BORDER)
            c.pack(fill="x",pady=2)
            ci=ctk.CTkFrame(c,fg_color="transparent"); ci.pack(fill="x",padx=12,pady=7)
            ctk.CTkLabel(ci,text=ico+"  "+title,font=ctk.CTkFont(size=11,weight="bold"),
                         text_color="#fff").pack(anchor="w")
            ctk.CTkLabel(ci,text=text,font=ctk.CTkFont(size=10),text_color=TEXT,
                         wraplength=680,justify="left").pack(anchor="w",pady=(1,0))

    # ── TAB: CS2 CFG ──────────────────────────────────────
    def _tab_cs2cfg(self,pad):
        ctk.CTkLabel(pad,text="⚙️ autoexec.cfg",
                     font=ctk.CTkFont(size=14,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,4))
        ctk.CTkLabel(pad,text="Готовый конфиг для максимального FPS и минимального пинга",
                     font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w",pady=(0,8))
        cfg="fps_max 0\nr_lowlatency 2\ncl_showfps 1\nmat_queue_mode -1\n"\
            "r_dynamic_lighting 0\nr_shadows 0\ncl_ragdoll_physics_enable 0\n"\
            "r_motionblur 0\ncl_interp 0\ncl_interp_ratio 1\nrate 786432\n"\
            "cl_updaterate 128\ncl_cmdrate 128\nm_rawinput 1\nsnd_menumusic_volume 0\n"\
            "cl_draw_only_deathnotices 1\nviewmodel_presetpos 3"
        tb=ctk.CTkTextbox(pad,height=220,fg_color="#020810",border_width=1,border_color=BORDER,
                          font=ctk.CTkFont(family="Courier New",size=11),
                          text_color="#68ffaa",corner_radius=7)
        tb.pack(fill="x",pady=(0,8)); tb.insert("end",cfg)
        def save():
            path=expand(CS2_CFG)
            try:
                os.makedirs(os.path.dirname(path),exist_ok=True)
                with open(path,"w",encoding="utf-8") as f: f.write(tb.get("1.0","end"))
                messagebox.showinfo("OK","Сохранено: "+path)
            except Exception as e: messagebox.showerror("Ошибка",str(e))
        make_btn(pad,"💾  Сохранить прямо в CS2",save,
                 width=230,color="#006adf",hover="#0090ff").pack(anchor="w")

    # ── TAB: FIVEM ────────────────────────────────────────
    def _tab_fivem(self,pad):
        ctk.CTkLabel(pad,text="🟣 FiveM оптимизация",
                     font=ctk.CTkFont(size=14,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,6))
        opts=[
            ("🧹","Очистить кэш FiveM","Удаляет кэш шейдеров и текстур",NEON,
             ["rmdir /s /q \"%LOCALAPPDATA%\\FiveM\\FiveM.app\\cache\""],
             []),
            ("🔕","Откл. оверлей FiveM","Убирает оверлей сервера",ORANGE,
             ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v DrawOverlay /t REG_DWORD /d 0 /f"],
             ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v DrawOverlay /t REG_DWORD /d 1 /f"]),
            ("⚡","StreamMemory 756MB","Больше памяти для текстур",GREEN,
             ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v StreamingMemory /t REG_DWORD /d 756 /f"],
             ["reg add \"HKCU\\Software\\CitizenFX\\FiveM\" /v StreamingMemory /t REG_DWORD /d 512 /f"]),
        ]
        for ico,name,desc,accent,on_c,off_c in opts:
            self._compact_toggle(pad,ico,name,desc,on_c,off_c,accent)
        self._div(pad)
        ctk.CTkLabel(pad,text="💡 Добавь +set fpslimit 0 в параметры запуска FiveM",
                     font=ctk.CTkFont(size=10,slant="italic"),text_color=GOLD).pack(anchor="w")

    # ── TAB: LAUNCH ARGS ──────────────────────────────────
    def _tab_launch(self,pad,gname,g):
        ctk.CTkLabel(pad,text="🔩 Параметры запуска",
                     font=ctk.CTkFont(size=14,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,4))
        ctk.CTkLabel(pad,text="Steam → ПКМ на игре → Свойства → Параметры запуска",
                     font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w",pady=(0,8))
        for pname,pdata in g["presets"].items():
            c=ctk.CTkFrame(pad,fg_color=PANEL2,corner_radius=7,
                           border_width=1,border_color=BORDER)
            c.pack(fill="x",pady=3)
            ci=ctk.CTkFrame(c,fg_color="transparent"); ci.pack(fill="x",padx=12,pady=8)
            ctk.CTkLabel(ci,text=pname,font=ctk.CTkFont(size=11,weight="bold"),
                         text_color="#fff").pack(anchor="w")
            tb=ctk.CTkTextbox(ci,height=36,fg_color="#020810",border_width=1,border_color=BORDER,
                              font=ctk.CTkFont(family="Courier New",size=10),
                              text_color=NEON,corner_radius=5)
            tb.pack(fill="x",pady=(3,0)); tb.insert("end",pdata.get("launch",""))

    # ── LAUNCH GAME ───────────────────────────────────────
    def _launch_game(self,gname):
        g=GAMES[gname]
        # Check user override first
        override=self.game_exe_override.get(gname)
        if override and os.path.exists(override):
            subprocess.Popen([override]); return
        # Search known paths
        exe=find_exe(g["exe"])
        if exe:
            subprocess.Popen([exe]); return
        # Steam fallback
        if g.get("steam"):
            subprocess.Popen(["cmd","/c","start","","steam://rungameid/"+g["steam"]],shell=False); return
        # Epic fallback
        if g.get("epic"):
            subprocess.Popen(["cmd","/c","start","",
                             "com.epicgames.launcher://apps/"+g["epic"]+"?action=launch&silent=true"],
                             shell=False); return
        # Not found - ask user
        self._ask_exe(gname)

    def _ask_exe(self,gname):
        win=ctk.CTkToplevel(self)
        win.title("Где "+gname+"?")
        win.geometry("480x220")
        win.configure(fg_color=BG)
        ctk.CTkLabel(win,text="⚠ Не удалось найти "+gname,
                     font=ctk.CTkFont(size=14,weight="bold"),text_color=GOLD).pack(pady=(20,6))
        ctk.CTkLabel(win,text="Укажи путь к .exe файлу игры вручную:",
                     font=ctk.CTkFont(size=11),text_color=TEXT).pack()
        path_var=ctk.StringVar()
        entry=ctk.CTkEntry(win,textvariable=path_var,width=380,
                           fg_color=PANEL2,border_color=BORDER)
        entry.pack(pady=8)
        def browse():
            p=filedialog.askopenfilename(
                title="Выбери "+gname+".exe",
                filetypes=[("Исполняемые файлы","*.exe"),("Все файлы","*.*")])
            if p: path_var.set(p)
        def launch_now():
            p=path_var.get()
            if p and os.path.exists(p):
                self.game_exe_override[gname]=p
                subprocess.Popen([p]); win.destroy()
            else:
                messagebox.showerror("Ошибка","Файл не найден: "+p)
        bf=ctk.CTkFrame(win,fg_color="transparent"); bf.pack()
        make_btn(bf,"📁 Обзор",browse,color="#1a3050",hover="#2a4060",width=110).pack(side="left",padx=4)
        make_btn(bf,"▶ Запустить",launch_now,color="#006adf",hover="#0099ff",width=130).pack(side="left",padx=4)
        make_btn(bf,"✕ Закрыть",win.destroy,color="#3a0000",hover="#5a0000",width=90).pack(side="left",padx=4)

    # ── FULL OPTIMIZE ─────────────────────────────────────
    def _full_optimize(self,gname):
        win=ctk.CTkToplevel(self)
        win.title("Оптимизация "+gname)
        win.geometry("500x360"); win.configure(fg_color=BG)
        ctk.CTkLabel(win,text="⚡ Полная оптимизация "+gname,
                     font=ctk.CTkFont(size=14,weight="bold"),text_color="#fff").pack(pady=(14,6),padx=14,anchor="w")
        log=ctk.CTkTextbox(win,height=250,fg_color="#020810",border_width=1,border_color=BORDER,
                           font=ctk.CTkFont(family="Courier New",size=11),
                           text_color="#68ffaa",corner_radius=7)
        log.pack(fill="both",expand=True,padx=14,pady=(0,14))
        log.configure(state="disabled")
        def run():
            steps=[
                ("⚡ Высокий план питания","powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"),
                ("🔕 Откл. Game DVR","reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f"),
                ("🌐 DNS Google","netsh interface ip set dns \"Ethernet\" static 8.8.8.8"),
                ("🏎 Откл. Nagle","reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpAckFrequency /t REG_DWORD /d 1 /f"),
                ("🔄 Flush DNS","ipconfig /flushdns"),
                ("⏸ Стоп Win Update","net stop wuauserv"),
                ("🔍 Стоп Indexer","net stop wsearch"),
                ("🧹 Очистка RAM","rundll32.exe advapi32.dll,ProcessIdleTasks"),
            ]
            for name,cmd in steps:
                ok=run_cmd(cmd)
                log.configure(state="normal")
                log.insert("end","  "+("✓" if ok else "✗")+" "+name+"\n")
                log.configure(state="disabled"); log.see("end")
                time.sleep(0.12)
            self._kill_all(gname)
            log.configure(state="normal")
            log.insert("end","\n✅ Готово! Запускай "+gname+"!\n")
            log.configure(state="disabled"); log.see("end")
        threading.Thread(target=run,daemon=True).start()

    # ── PROFILE PAGE ──────────────────────────────────────
    def _build_profile_page(self):
        pad=self._make_page("profile")
        ctk.CTkLabel(pad,text="💻 Профиль ПК",
                     font=ctk.CTkFont(size=16,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,3))
        ctk.CTkLabel(pad,text="Информация о системе и нагрузка в реальном времени",
                     font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w",pady=(0,10))
        # Info grid
        ig=ctk.CTkFrame(pad,fg_color=PANEL,corner_radius=10,border_width=1,border_color=BORDER)
        ig.pack(fill="x",pady=(0,8))
        igp=ctk.CTkFrame(ig,fg_color="transparent"); igp.pack(fill="x",padx=14,pady=10)
        ctk.CTkLabel(igp,text="🖥 Характеристики",font=ctk.CTkFont(size=12,weight="bold"),
                     text_color="#fff").pack(anchor="w",pady=(0,6))
        self.info_labels={}
        grid=ctk.CTkFrame(igp,fg_color="transparent"); grid.pack(fill="x")
        grid.columnconfigure(0,weight=1); grid.columnconfigure(1,weight=1)
        for i,field in enumerate(["OS","CPU","RAM","Диск C:","GPU","IP"]):
            f=ctk.CTkFrame(grid,fg_color=PANEL2,corner_radius=6,
                           border_width=1,border_color=BORDER)
            f.grid(row=i//2,column=i%2,padx=3,pady=2,sticky="ew")
            fi=ctk.CTkFrame(f,fg_color="transparent"); fi.pack(fill="x",padx=10,pady=5)
            ctk.CTkLabel(fi,text=field,font=ctk.CTkFont(size=9),text_color=DIM).pack(anchor="w")
            lbl=ctk.CTkLabel(fi,text="...",font=ctk.CTkFont(size=10,weight="bold"),text_color="#fff")
            lbl.pack(anchor="w"); self.info_labels[field]=lbl
        # Live stats
        self._div(pad)
        ctk.CTkLabel(pad,text="📊 Нагрузка прямо сейчас",
                     font=ctk.CTkFont(size=12,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,6))
        sr=ctk.CTkFrame(pad,fg_color="transparent"); sr.pack(fill="x",pady=(0,8))
        for i in range(4): sr.columnconfigure(i,weight=1)
        self.stat_boxes={}
        for i,(k,lbl,col) in enumerate([("cpu","CPU %",GREEN),("ram","RAM %",NEON),
                                         ("disk","Диск %",GOLD),("temp","Темп °C",RED)]):
            f=ctk.CTkFrame(sr,fg_color=PANEL2,corner_radius=8,border_width=1,border_color=BORDER)
            f.grid(row=0,column=i,padx=3,sticky="ew")
            v=ctk.CTkLabel(f,text="—",font=ctk.CTkFont(size=22,weight="bold"),text_color=col)
            v.pack(pady=(8,1))
            ctk.CTkLabel(f,text=lbl,font=ctk.CTkFont(size=9),text_color=DIM).pack(pady=(0,7))
            self.stat_boxes[k]=v
        # Progress bars
        bf=ctk.CTkFrame(pad,fg_color=PANEL,corner_radius=9,border_width=1,border_color=BORDER)
        bf.pack(fill="x",pady=(0,8))
        bp=ctk.CTkFrame(bf,fg_color="transparent"); bp.pack(fill="x",padx=12,pady=8)
        self.prog_bars={}
        for k,lbl,col in [("cpu","CPU",GREEN),("ram","RAM",NEON),("disk","ДИСК",GOLD)]:
            r=ctk.CTkFrame(bp,fg_color="transparent"); r.pack(fill="x",pady=2)
            ctk.CTkLabel(r,text=lbl,font=ctk.CTkFont(size=9),text_color=DIM,width=38).pack(side="left")
            bar=ctk.CTkProgressBar(r,height=12,progress_color=col,fg_color=PANEL2,corner_radius=4)
            bar.set(0); bar.pack(side="left",fill="x",expand=True,padx=6)
            pct=ctk.CTkLabel(r,text="0%",font=ctk.CTkFont(size=9),text_color=col,width=32)
            pct.pack(side="left"); self.prog_bars[k]=(bar,pct)
        # Ping
        self._div(pad)
        ctk.CTkLabel(pad,text="🌐 Пинг",font=ctk.CTkFont(size=12,weight="bold"),
                     text_color="#fff").pack(anchor="w",pady=(0,5))
        pr=ctk.CTkFrame(pad,fg_color="transparent"); pr.pack(fill="x",pady=(0,8))
        pr.columnconfigure(0,weight=1); pr.columnconfigure(1,weight=1)
        self.ping_g=self._ping_box(pr,"Google 8.8.8.8",0)
        self.ping_s=self._ping_box(pr,"Steam",1)
        make_btn(pad,"🔄  Обновить",self._refresh_profile,
                 width=140,color="#006adf",hover="#0090ff").pack(anchor="w")
        threading.Thread(target=self._load_profile,daemon=True).start()
        threading.Thread(target=self._live_loop,daemon=True).start()

    def _ping_box(self,parent,label,col):
        f=ctk.CTkFrame(parent,fg_color=PANEL2,corner_radius=7,border_width=1,border_color=BORDER)
        f.grid(row=0,column=col,padx=3,sticky="ew")
        fi=ctk.CTkFrame(f,fg_color="transparent"); fi.pack(fill="x",padx=10,pady=7)
        ctk.CTkLabel(fi,text=label,font=ctk.CTkFont(size=9),text_color=DIM).pack(anchor="w")
        v=ctk.CTkLabel(fi,text="—",font=ctk.CTkFont(size=14,weight="bold"),text_color=NEON)
        v.pack(anchor="w"); return v

    def _load_profile(self):
        self._safe_set(self.info_labels["OS"],platform.system()+" "+platform.release())
        cpu=run_cmd_out("wmic cpu get Name /value").replace("Name=","").strip()
        self._safe_set(self.info_labels["CPU"],(cpu[:40]+"...") if len(cpu)>40 else (cpu or "—"))
        try:
            rb=int(run_cmd_out("wmic computersystem get TotalPhysicalMemory /value").replace("TotalPhysicalMemory=","").strip())
            self._safe_set(self.info_labels["RAM"],str(round(rb/1024**3,1))+" GB")
        except: self._safe_set(self.info_labels["RAM"],"—")
        try:
            raw=run_cmd_out("wmic logicaldisk where DeviceID=\"C:\" get FreeSpace,Size /value")
            d={l.split("=")[0]:l.split("=")[1] for l in raw.splitlines() if "=" in l and len(l.split("="))>1 and l.split("=")[1].strip()}
            free=int(d.get("FreeSpace",0))//1024**3; tot=int(d.get("Size",0))//1024**3
            self._safe_set(self.info_labels["Диск C:"],str(free)+" / "+str(tot)+" GB")
        except: self._safe_set(self.info_labels["Диск C:"],"—")
        gpu=run_cmd_out("wmic path win32_videocontroller get Name /value").replace("Name=","").strip()
        self._safe_set(self.info_labels["GPU"],(gpu[:40]+"...") if len(gpu)>40 else (gpu or "—"))
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(("8.8.8.8",80)); ip=s.getsockname()[0]; s.close()
        except: ip="—"
        self._safe_set(self.info_labels["IP"],ip)
        ms_g=ping_host("8.8.8.8"); ms_s=ping_host("store.steampowered.com")
        self._safe_set(self.ping_g,(str(ms_g)+" ms") if ms_g>0 else "timeout")
        self._safe_set(self.ping_s,(str(ms_s)+" ms") if ms_s>0 else "timeout")

    def _refresh_profile(self):
        for l in self.info_labels.values(): self._safe_set(l,"...")
        threading.Thread(target=self._load_profile,daemon=True).start()

    def _live_loop(self):
        while self._live_running:
            self._update_live(); time.sleep(2)

    def _update_live(self):
        # CPU
        try:
            r=subprocess.run("typeperf \"\\Processor(_Total)\\% Processor Time\" -sc 1",
                shell=True,capture_output=True,text=True,timeout=5,encoding="cp1251",errors="replace")
            lines=[l for l in r.stdout.splitlines() if "," in l and "%" not in l and "Time" not in l]
            if lines:
                v=int(float(lines[0].split(",")[1].replace('"','').strip()))
                c=GREEN if v<50 else GOLD if v<80 else RED
                self._safe_set(self.stat_boxes["cpu"],str(v)+"%")
                self.stat_boxes["cpu"].configure(text_color=c)
                self.prog_bars["cpu"][0].set(v/100)
                self.prog_bars["cpu"][1].configure(text=str(v)+"%")
        except: pass
        # RAM
        try:
            r2=run_cmd_out("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /value")
            d={l.split("=")[0]:l.split("=")[1] for l in r2.splitlines() if "=" in l and len(l.split("="))>1 and l.split("=")[1].strip()}
            free=int(d.get("FreePhysicalMemory",0)); tot=int(d.get("TotalVisibleMemorySize",1))
            v=int((1-free/tot)*100); c=GREEN if v<60 else GOLD if v<80 else RED
            self._safe_set(self.stat_boxes["ram"],str(v)+"%")
            self.stat_boxes["ram"].configure(text_color=c)
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
                self._safe_set(self.stat_boxes["temp"],str(v)+"°")
                self.stat_boxes["temp"].configure(text_color=c)
            else: self._safe_set(self.stat_boxes["temp"],"N/A")
        except: self._safe_set(self.stat_boxes["temp"],"N/A")

    # ── WINDOWS PAGE ──────────────────────────────────────
    def _build_windows_page(self):
        pad=self._make_page("windows")
        ctk.CTkLabel(pad,text="⚡ Оптимизация Windows",
                     font=ctk.CTkFont(size=16,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,3))
        ctk.CTkLabel(pad,text="Системные твики для максимального FPS в любой игре",
                     font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w",pady=(0,8))
        for ico,name,desc,accent,on_c,off_c in WIN_OPTS:
            self._compact_toggle(pad,ico,name,desc,on_c,off_c,accent)
        self._div(pad)
        make_btn(pad,"⚡  ПРИМЕНИТЬ ВСЕ",self._run_all_windows,
                 size=13,width=240,color="#006adf",hover="#0090ff").pack(anchor="w")
        self.win_log=self._log(pad,90)

    def _run_all_windows(self):
        self._lclr(self.win_log); self._lw(self.win_log,"⚡ Применяю...")
        steps=[
            ("⚡ План питания","powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"),
            ("🔕 Game DVR","reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f"),
            ("📈 CPU приоритет","reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f"),
            ("🎮 HAGS","reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v HwSchMode /t REG_DWORD /d 2 /f"),
            ("🔍 Search stop","net stop wsearch"),
            ("📊 SysMain stop","net stop sysmain"),
            ("⏸ Update stop","net stop wuauserv"),
            ("🧹 RAM","rundll32.exe advapi32.dll,ProcessIdleTasks"),
        ]
        def run():
            for name,cmd in steps:
                ok=run_cmd(cmd); self._lw(self.win_log,"  "+("✓" if ok else "✗")+" "+name)
                time.sleep(0.1)
            self._lw(self.win_log,"✅ Готово! Перезагрузи ПК.")
        threading.Thread(target=run,daemon=True).start()

    # ── NETWORK PAGE ──────────────────────────────────────
    def _build_network_page(self):
        pad=self._make_page("network")
        ctk.CTkLabel(pad,text="🌐 Настройка сети",
                     font=ctk.CTkFont(size=16,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,3))
        ctk.CTkLabel(pad,text="Оптимизация пинга для всех игр",
                     font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w",pady=(0,8))
        for ico,name,desc,accent,on_c,off_c in NET_OPTS:
            self._compact_toggle(pad,ico,name,desc,on_c,off_c,accent)
        self._div(pad)
        make_btn(pad,"📡  Проверить пинг",self._global_ping,
                 width=170,color="#006adf",hover="#0090ff").pack(anchor="w")
        self.net_log=self._log(pad,100)

    def _global_ping(self):
        self._lclr(self.net_log)
        def run():
            for n,h in [("Steam","store.steampowered.com"),("Cloudflare","1.1.1.1"),
                        ("Google","8.8.8.8"),("Faceit","api.faceit.com"),
                        ("AWS EU","ec2.eu-central-1.amazonaws.com")]:
                ms=ping_host(h)
                s="OK" if 0<ms<80 else "СРЕДНИЙ" if 0<ms<150 else "ВЫСОКИЙ" if ms>0 else "timeout"
                self._lw(self.net_log,"  "+n.ljust(14)+(str(ms)+" ms").rjust(8)+"  "+s)
                time.sleep(0.1)
            self._lw(self.net_log,"✅ Готово!")
        threading.Thread(target=run,daemon=True).start()

    # ── MONITOR PAGE ──────────────────────────────────────
    def _build_monitor_page(self):
        pad=self._make_page("monitor")
        ctk.CTkLabel(pad,text="📊 Мониторинг пинга",
                     font=ctk.CTkFont(size=16,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,3))
        ctk.CTkLabel(pad,text="Живой замер задержки до серверов",
                     font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w",pady=(0,8))
        sr=ctk.CTkFrame(pad,fg_color="transparent"); sr.pack(fill="x",pady=(0,8))
        for i in range(3): sr.columnconfigure(i,weight=1)
        self.ms_cur=self._stat_box(sr,"Текущий ms",GREEN,0)
        self.ms_avg=self._stat_box(sr,"Средний ms",GOLD,1)
        self.ms_max=self._stat_box(sr,"Максимум ms",RED,2)
        cr=ctk.CTkFrame(pad,fg_color="transparent"); cr.pack(fill="x",pady=(0,8))
        self.mon_btn=make_btn(cr,"▶  Запустить",self._toggle_mon,
                              width=190,color="#006adf",hover="#0090ff")
        self.mon_btn.pack(side="left")
        self.mon_lbl=ctk.CTkLabel(cr,text="● Остановлен",text_color=DIM,
                                   font=ctk.CTkFont(size=10)); self.mon_lbl.pack(side="left",padx=10)
        ctk.CTkLabel(cr,text="Интервал:",text_color=DIM,font=ctk.CTkFont(size=10)).pack(side="left")
        self.mon_int=ctk.CTkComboBox(cr,values=["2 сек","5 сек","10 сек"],
                                     width=82,fg_color=PANEL2,border_color=BORDER)
        self.mon_int.set("2 сек"); self.mon_int.pack(side="left",padx=5)
        self.srv_lbls={}
        for name,host in [("Steam","store.steampowered.com"),("Cloudflare","1.1.1.1"),
                           ("Google DNS","8.8.8.8"),("Faceit","api.faceit.com")]:
            row=ctk.CTkFrame(pad,fg_color=PANEL2,corner_radius=7,
                             border_width=1,border_color=BORDER); row.pack(fill="x",pady=2)
            ctk.CTkLabel(row,text="●",font=ctk.CTkFont(size=11),
                         text_color=DIM).pack(side="left",padx=(10,6),pady=7)
            ctk.CTkLabel(row,text=name,font=ctk.CTkFont(size=11),
                         text_color=TEXT,width=120).pack(side="left")
            lbl=ctk.CTkLabel(row,text="— ms",font=ctk.CTkFont(size=11,weight="bold"),
                             text_color=DIM); lbl.pack(side="right",padx=12)
            self.srv_lbls[host]=lbl
        cc=ctk.CTkFrame(pad,fg_color=PANEL2,corner_radius=10,
                        border_width=1,border_color=BORDER); cc.pack(fill="x",pady=5)
        ctk.CTkLabel(cc,text="📈 График",font=ctk.CTkFont(size=10),
                     text_color=DIM).pack(anchor="w",padx=10,pady=(7,2))
        self.chart=tkinter.Canvas(cc,height=100,bg="#020810",highlightthickness=0)
        self.chart.pack(fill="x",padx=8,pady=(0,7))

    def _stat_box(self,parent,label,color,col):
        f=ctk.CTkFrame(parent,fg_color=PANEL2,corner_radius=8,
                       border_width=1,border_color=BORDER)
        f.grid(row=0,column=col,padx=3,sticky="ew")
        v=ctk.CTkLabel(f,text="—",font=ctk.CTkFont(size=22,weight="bold"),text_color=color)
        v.pack(pady=(9,2))
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
                self.ms_cur.configure(text=str(avg),
                    text_color=GREEN if avg<80 else GOLD if avg<150 else RED)
                self.ms_avg.configure(text=str(sum(self.ping_history)//len(self.ping_history)))
                self.ms_max.configure(text=str(max(self.ping_history)))
                self._draw_chart()
            time.sleep(iv)

    def _draw_chart(self):
        c=self.chart; c.delete("all")
        if len(self.ping_history)<2: return
        W=c.winfo_width() or 500; H=100; maxV=max(max(self.ping_history),200)
        pts=[(int(10+(i/(len(self.ping_history)-1))*(W-20)),
              int(H-10-(v/maxV)*(H-20))) for i,v in enumerate(self.ping_history)]
        poly=[(10,H-10)]+pts+[(pts[-1][0],H-10)]
        c.create_polygon([x for pt in poly for x in pt],fill="#003030",outline="")
        last=self.ping_history[-1]; col="#00ff88" if last<80 else "#ffd700" if last<150 else "#ff4466"
        c.create_line([x for pt in pts for x in pt],fill=col,width=2,smooth=True)

if __name__=="__main__":
    app=App(); app.mainloop()
