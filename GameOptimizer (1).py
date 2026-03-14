"""Game Optimizer v2.0 — Rust / GTA V / CS2"""
import customtkinter as ctk
import tkinter
import subprocess, threading, random, time, os, socket, sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG="#05080f"; PANEL="#090f1d"; PANEL2="#0c1628"; BORDER="#1a3050"
TEXT="#b8cfea"; DIM="#3a5a7a"; NEON="#00f0ff"; GREEN="#00ff88"
GOLD="#ffd700"; RED="#ff4466"; PURPLE="#b060ff"; ORANGE="#ff9f40"

JOKES=[
    "😂 Ваня: '5 FPS — это нормально'",
    "💀 Ваня оптимизировал и удалил system32",
    "🎯 Ваня поставил мониторинг — FPS 12",
    "🔫 Ваня в Rust строил дом — убили через стену",
    "🚗 Ваня в GTA взял такси — лучше пешком",
    "⚡ Ваня включил план питания — сгорел роутер",
]

def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True,
                           text=True, timeout=30, encoding="cp1251", errors="replace")
        return r.returncode == 0
    except:
        return False

def ping_host(host, timeout=2):
    try:
        t0 = time.time()
        s = socket.create_connection((host, 80), timeout=timeout)
        s.close()
        return int((time.time() - t0) * 1000)
    except:
        return -1

def mkbtn(parent, text, cmd, size=13, bold=True,
          color="#0060df", hover="#0090ff", width=None, corner=8):
    kw = dict(text=text, command=cmd,
              fg_color=color, hover_color=hover,
              font=ctk.CTkFont(size=size, weight="bold" if bold else "normal"),
              corner_radius=corner)
    if width:
        kw["width"] = width
    return ctk.CTkButton(parent, **kw)

def sec_lbl(parent, text):
    ctk.CTkLabel(parent, text=text,
                 font=ctk.CTkFont(size=12, weight="bold"),
                 text_color=DIM).pack(anchor="w", pady=(0, 5))

def divider(parent):
    ctk.CTkFrame(parent, height=1, fg_color=BORDER).pack(fill="x", pady=10)

# ── Game data ─────────────────────────────────────────────
GAMES = {
    "Rust": {
        "icon": "🔫", "color": "#e07020", "desc": "Survival multiplayer",
        "presets": {
            "Максимум FPS": {
                "desc": "Минимум графики", "fps_expect": "100-200+",
                "launch": "-high -maxMem=8192 -malloc=system +fps.limit 0 -nolog",
                "settings": [("grass.on","false"),("terrain.quality","0"),
                             ("graphics.shadows","0"),("graphics.ssao","0"),
                             ("graphics.damage","0"),("graphics.itemskins","0"),
                             ("graphics.lodbias","0.25"),("graphics.dof","false")]},
            "Баланс": {
                "desc": "FPS + читаемость", "fps_expect": "60-120",
                "launch": "-high -maxMem=8192 +fps.limit 0",
                "settings": [("grass.on","true"),("terrain.quality","50"),
                             ("graphics.shadows","1"),("graphics.ssao","0"),
                             ("graphics.lodbias","1")]},
            "Качество": {
                "desc": "Полная графика", "fps_expect": "40-80",
                "launch": "+fps.limit 0",
                "settings": [("grass.on","true"),("terrain.quality","100"),
                             ("graphics.shadows","3"),("graphics.ssao","1"),
                             ("graphics.lodbias","2")]},
        },
        "in_game": [
            ("🎓","Обучалка / подсказки","Постоянные подсказки новичка",RED,
             [r'reg add "HKCU\Software\Facepunch\Rust" /v tutorial_complete /t REG_DWORD /d 1 /f'],
             [r'reg add "HKCU\Software\Facepunch\Rust" /v tutorial_complete /t REG_DWORD /d 0 /f']),
            ("🎬","Вступительное видео","Логотип при каждом запуске",ORANGE,
             [r'reg add "HKCU\Software\Facepunch\Rust" /v skip_intro /t REG_DWORD /d 1 /f'],
             [r'reg add "HKCU\Software\Facepunch\Rust" /v skip_intro /t REG_DWORD /d 0 /f']),
            ("🌿","Трава (grass.on false)","Убирает траву — +20-40 FPS",GREEN,
             ['echo grass.on false >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
             ['echo grass.on true >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
            ("💨","Motion Blur","Размытие при движении — снижает FPS",NEON,
             ['echo effects.motionblur false >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
             ['echo effects.motionblur true >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
            ("🔊","VOIP / Голосовой чат","Постоянно слушает микрофон",PURPLE,
             ['echo voice.use false >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
             ['echo voice.use true >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
            ("📦","Скины предметов","Загрузка скинов жрёт RAM",GOLD,
             ['echo graphics.itemskins 0 >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
             ['echo graphics.itemskins 1 >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
            ("🎆","Эффекты взрывов","Партиклы взрывов — лишняя нагрузка",RED,
             ['echo graphics.damage 0 >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
             ['echo graphics.damage 1 >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
            ("🌅","God Rays / Лучи света","Volumetric lighting — дорогой эффект",ORANGE,
             ['echo graphics.shafts 0 >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
             ['echo graphics.shafts 1 >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
        ],
        "tips": [
            {"icon":"💡","title":"Отключи Steam оверлей","text":"Steam → ПКМ на Rust → Свойства → Снять галочку 'Включить Steam Overlay'"},
            {"icon":"🛡","title":"Добавь в исключения антивируса","text":"Windows Defender → Защита → Исключения → Папка с Rust"},
            {"icon":"🎮","title":"Используй DirectX 11","text":"В параметрах запуска добавь -force-feature-level-11-0"},
            {"icon":"🧹","title":"Очищай кэш шейдеров","text":"Папка Rust → AppData\\Local\\Temp\\Rust — удаляй раз в неделю"},
            {"icon":"📡","title":"Выбирай сервер близко","text":"Выбирай сервер с наименьшим пингом вручную"},
        ],
    },
    "GTA V": {
        "icon": "🚗", "color": "#00a8ff", "desc": "Open world / FiveM",
        "presets": {
            "Максимум FPS": {
                "desc": "Для слабых ПК и FiveM", "fps_expect": "80-160+",
                "launch": "-notablet -norestrictions -noFirstRun -IgnoreCorrupts",
                "settings": [("TextureQuality","normal"),("ShaderQuality","normal"),
                             ("ShadowQuality","normal"),("ReflectionQuality","off"),
                             ("MSAA","off"),("FXAA","off"),("AmbientOcclusion","off"),
                             ("MotionBlur","false"),("InGameDepthOfField","false")]},
            "Баланс": {
                "desc": "Комфортная игра", "fps_expect": "60-100",
                "launch": "-notablet -noFirstRun",
                "settings": [("TextureQuality","high"),("ShaderQuality","high"),
                             ("ShadowQuality","high"),("MSAA","off"),("FXAA","on"),
                             ("AmbientOcclusion","medium"),("MotionBlur","false")]},
            "Качество": {
                "desc": "Максимальная красота", "fps_expect": "40-70",
                "launch": "-notablet",
                "settings": [("TextureQuality","very high"),("ShaderQuality","very high"),
                             ("ShadowQuality","very high"),("MSAA","x4"),("FXAA","on"),
                             ("AmbientOcclusion","high"),("TessellationQuality","very high")]},
        },
        "in_game": [
            ("🎓","Обучающие подсказки","Всплывают каждый раз — бесполезно",RED,
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v TutorialDone /t REG_DWORD /d 1 /f'],
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v TutorialDone /t REG_DWORD /d 0 /f']),
            ("🎬","Вступительные ролики","Логотип + ролик при каждом запуске",ORANGE,
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v InstallComplete /t REG_DWORD /d 1 /f'],
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v InstallComplete /t REG_DWORD /d 0 /f']),
            ("🌀","Motion Blur","Размытие при движении — -10-15 FPS",RED,
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v MotionBlur /t REG_DWORD /d 0 /f'],
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v MotionBlur /t REG_DWORD /d 1 /f']),
            ("🌊","Глубина резкости DOF","Размытие фона — зря расходует GPU",NEON,
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v InGameDepthOfField /t REG_DWORD /d 0 /f'],
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v InGameDepthOfField /t REG_DWORD /d 1 /f']),
            ("🎬","Replay / Rockstar Editor","Постоянно пишет буфер в фоне",GOLD,
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ReplayBuffer /t REG_DWORD /d 0 /f'],
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ReplayBuffer /t REG_DWORD /d 1 /f']),
            ("🐾","Tessellation","Детализация поверхностей — очень дорого",PURPLE,
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v Tessellation /t REG_DWORD /d 0 /f'],
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v Tessellation /t REG_DWORD /d 1 /f']),
            ("🌆","Extended Distance Scaling","Далёкие объекты — огромная нагрузка",RED,
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ExtendedDistanceScaling /t REG_DWORD /d 0 /f'],
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ExtendedDistanceScaling /t REG_DWORD /d 1 /f']),
            ("🚶","Плотность NPC / трафика","Много NPC грузят CPU",ORANGE,
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v PedDensity /t REG_DWORD /d 0 /f'],
             [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v PedDensity /t REG_DWORD /d 100 /f']),
        ],
        "tips": [
            {"icon":"🟣","title":"FiveM: отключи все оверлеи","text":"Discord, Steam, NVIDIA — все оверлеи отключи перед FiveM"},
            {"icon":"⚡","title":"Параметр -notablet","text":"Обязательный параметр — убирает ненужный ввод планшета"},
            {"icon":"🌐","title":"GTA Online: NAT Type Open","text":"Пробрось порты 6672 UDP и 61455-61458 UDP для стабильного онлайна"},
            {"icon":"🔧","title":"Rockstar Launcher","text":"Выключи Rockstar Launcher из автозагрузки — жрёт RAM"},
            {"icon":"🗑","title":"Очисти кэш","text":"update\\x64\\dlcpacks — удали ненужные DLC моды"},
        ],
    },
    "CS2": {
        "icon": "🎯", "color": "#ff6b35", "desc": "Counter-Strike 2",
        "presets": {
            "Максимум FPS": {
                "desc": "Про-настройки", "fps_expect": "200-400+",
                "launch": "-novid -nojoy -noaafonts -limitvsconst -forcenovsync +mat_queue_mode -1 +r_dynamic_lighting 0 -freq 240 -high",
                "settings": [("r_lowlatency","2"),("fps_max","0"),
                             ("mat_queue_mode","-1"),("r_dynamic_lighting","0"),
                             ("r_shadows","0"),("cl_ragdoll_physics_enable","0"),
                             ("r_motionblur","0"),("cl_showfps","1")]},
            "Баланс": {
                "desc": "FPS + видимость", "fps_expect": "144-250",
                "launch": "-novid -nojoy -forcenovsync +mat_queue_mode -1 -high",
                "settings": [("fps_max","0"),("r_lowlatency","2"),
                             ("r_shadows","1"),("r_dynamic_lighting","1"),
                             ("cl_showfps","1"),("r_motionblur","0")]},
            "Качество": {
                "desc": "Красивая картинка", "fps_expect": "100-180",
                "launch": "-novid +mat_queue_mode -1",
                "settings": [("fps_max","0"),("r_shadows","3"),
                             ("r_dynamic_lighting","1"),("r_motionblur","0")]},
        },
        "in_game": [
            ("🎓","Обучение / Tutorial","Убирает предложение зайти в обучалку",RED,
             [r'reg add "HKCU\Software\Valve\Counter-Strike Global Offensive" /v TutorialDone /t REG_DWORD /d 1 /f'],
             [r'reg add "HKCU\Software\Valve\Counter-Strike Global Offensive" /v TutorialDone /t REG_DWORD /d 0 /f']),
            ("🎬","Интро видео Valve","Логотип Valve при каждом запуске",ORANGE,
             [r'reg add "HKCU\Software\Valve\Counter-Strike Global Offensive" /v NoVideoIntro /t REG_DWORD /d 1 /f'],
             [r'reg add "HKCU\Software\Valve\Counter-Strike Global Offensive" /v NoVideoIntro /t REG_DWORD /d 0 /f']),
            ("🌀","Motion Blur","Размытие — снижает FPS без пользы",RED,
             ['echo r_motionblur 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
             ['echo r_motionblur 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
            ("💀","Ragdoll физика трупов","Трупы с физикой жрут CPU",NEON,
             ['echo cl_ragdoll_physics_enable 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
             ['echo cl_ragdoll_physics_enable 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
            ("🌿","Детали окружения (трава)","Декоративные детали — ненужная нагрузка",GREEN,
             ['echo cl_detailfade 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
             ['echo cl_detailfade 400 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
            ("🎵","Музыка в главном меню","Звуковой движок в меню зря работает",PURPLE,
             ['echo snd_menumusic_volume 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
             ['echo snd_menumusic_volume 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
            ("💬","Kill feed анимации","cl_draw_only_deathnotices — только важное",GOLD,
             ['echo cl_draw_only_deathnotices 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
             ['echo cl_draw_only_deathnotices 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
            ("🔫","Анимация осмотра оружия","viewmodel далеко — меньше мусора на экране",ORANGE,
             ['echo viewmodel_presetpos 3 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
             ['echo viewmodel_presetpos 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
        ],
        "tips": [
            {"icon":"🖥","title":"Частота монитора","text":"NVIDIA → Панель управления → Разрешение дисплея → Выбери 144/240Hz"},
            {"icon":"🖱","title":"Raw Input мышь","text":"Настройки CS2: m_rawinput 1 — прямой ввод без обработки Windows"},
            {"icon":"📡","title":"Rate команды","text":"rate 786432; cl_interp 0; cl_interp_ratio 1 — в autoexec.cfg"},
            {"icon":"🎮","title":"Откл. Game DVR","text":"Win+G → Настройки → Выключи запись и трансляцию"},
            {"icon":"🌡","title":"Температура CPU","text":"CS2 нагружает CPU — следи за температурой, больше 90°C = чистка кулера"},
        ],
    },
}

# ══════════════════════════════════════════════════════════
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

    # ── Build sidebar + content ───────────────────────────
    def _build_ui(self):
        # Sidebar
        sb = ctk.CTkFrame(self, width=200, fg_color=PANEL, corner_radius=0,
                          border_width=1, border_color=BORDER)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        lf = ctk.CTkFrame(sb, fg_color="transparent")
        lf.pack(pady=(16, 4), padx=12)
        ctk.CTkLabel(lf, text="🎮", font=ctk.CTkFont(size=22)).pack(side="left")
        ctk.CTkLabel(lf, text=" GAME OPTIMIZER",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=NEON).pack(side="left")
        ctk.CTkLabel(sb, text="v2.0", font=ctk.CTkFont(size=10),
                     text_color=DIM).pack()

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(fill="x", padx=10, pady=8)
        ctk.CTkLabel(sb, text="ИГРЫ", font=ctk.CTkFont(size=10),
                     text_color=DIM).pack(anchor="w", padx=12)

        self.game_btns = {}
        for gname in GAMES:
            b = ctk.CTkButton(sb, text=f"{GAMES[gname]['icon']}  {gname}",
                              anchor="w", font=ctk.CTkFont(size=13), height=38,
                              fg_color="transparent", hover_color="#0d1e38",
                              text_color=DIM, corner_radius=8,
                              command=lambda g=gname: self.show_game(g))
            b.pack(fill="x", padx=8, pady=2)
            self.game_btns[gname] = b

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(fill="x", padx=10, pady=8)
        ctk.CTkLabel(sb, text="ОБЩЕЕ", font=ctk.CTkFont(size=10),
                     text_color=DIM).pack(anchor="w", padx=12)

        self.nav_btns = {}
        for pid, label in [("windows", "⚡  Windows"),
                           ("network", "🌐  Сеть"),
                           ("monitor", "📊  Мониторинг")]:
            b = ctk.CTkButton(sb, text=label, anchor="w",
                              font=ctk.CTkFont(size=12), height=34,
                              fg_color="transparent", hover_color="#0d1e38",
                              text_color=DIM, corner_radius=8,
                              command=lambda p=pid: self.show_page(p))
            b.pack(fill="x", padx=8, pady=2)
            self.nav_btns[pid] = b

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(
            fill="x", padx=10, pady=8, side="bottom")
        self.joke_lbl = ctk.CTkLabel(
            sb, text=random.choice(JOKES),
            font=ctk.CTkFont(size=10, slant="italic"),
            text_color=GOLD, wraplength=178, justify="center")
        self.joke_lbl.pack(side="bottom", padx=8, pady=6)

        # Content
        self.content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

        self.pages = {}
        for gname in GAMES:
            self._build_game_page(gname)
        self._build_windows()
        self._build_network()
        self._build_monitor()

        self.show_game("Rust")

    # ── Page switching ────────────────────────────────────
    def show_game(self, gname):
        for p in self.pages.values():
            p.pack_forget()
        self.pages[gname].pack(fill="both", expand=True)
        for k, b in self.game_btns.items():
            b.configure(fg_color="#0d2040" if k == gname else "transparent",
                        text_color=GAMES[k]["color"] if k == gname else DIM)
        for b in self.nav_btns.values():
            b.configure(fg_color="transparent", text_color=DIM)

    def show_page(self, pid):
        for p in self.pages.values():
            p.pack_forget()
        self.pages[pid].pack(fill="both", expand=True)
        for b in self.game_btns.values():
            b.configure(fg_color="transparent", text_color=DIM)
        for k, b in self.nav_btns.items():
            b.configure(fg_color="#0d2040" if k == pid else "transparent",
                        text_color=NEON if k == pid else DIM)

    # ── Widget helpers ────────────────────────────────────
    def _scr(self, pid):
        f = ctk.CTkScrollableFrame(self.content, fg_color=BG,
                                   corner_radius=0, scrollbar_button_color=BORDER)
        self.pages[pid] = f
        return f

    def _log(self, parent, h=120):
        tb = ctk.CTkTextbox(parent, height=h, fg_color="#020810",
                            border_width=1, border_color=BORDER,
                            font=ctk.CTkFont(family="Courier New", size=11),
                            text_color="#68ffaa", corner_radius=8)
        tb.pack(fill="x", pady=(4, 0))
        tb.configure(state="disabled")
        return tb

    def _w(self, tb, t):
        tb.configure(state="normal")
        tb.insert("end", t + "\n")
        tb.configure(state="disabled")
        tb.see("end")

    def _clr(self, tb):
        tb.configure(state="normal")
        tb.delete("1.0", "end")
        tb.configure(state="disabled")

    def _toggle_row(self, parent, label, desc, on_cmd, off_cmd, accent=NEON):
        row = ctk.CTkFrame(parent, fg_color=PANEL2, corner_radius=9,
                           border_width=1, border_color=BORDER)
        row.pack(fill="x", pady=3)
        strip = ctk.CTkFrame(row, width=3, fg_color=accent, corner_radius=0)
        strip.pack(side="left", fill="y")
        ri = ctk.CTkFrame(row, fg_color="transparent")
        ri.pack(fill="x", padx=12, pady=8, side="left", expand=True)
        ctk.CTkLabel(ri, text=label,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#fff").pack(anchor="w")
        ctk.CTkLabel(ri, text=desc, font=ctk.CTkFont(size=10),
                     text_color=DIM).pack(anchor="w")
        var = ctk.BooleanVar(value=False)
        def _toggle(v=var, on=on_cmd, off=off_cmd):
            cmds = on if v.get() else off
            threading.Thread(target=lambda: [run_cmd(c) for c in cmds],
                             daemon=True).start()
        ctk.CTkSwitch(row, text="", variable=var, command=_toggle,
                      progress_color=accent, button_color="#ffffff",
                      width=46).pack(side="right", padx=12)

    # ── Game page ─────────────────────────────────────────
    def _build_game_page(self, gname):
        g = GAMES[gname]
        outer = ctk.CTkFrame(self.content, fg_color=BG, corner_radius=0)
        self.pages[gname] = outer

        # Header bar
        hbar = ctk.CTkFrame(outer, fg_color=PANEL, corner_radius=0,
                            border_width=1, border_color=BORDER, height=64)
        hbar.pack(fill="x")
        hbar.pack_propagate(False)
        hi = ctk.CTkFrame(hbar, fg_color="transparent")
        hi.pack(fill="both", padx=20, pady=10)
        ctk.CTkLabel(hi, text=g["icon"], font=ctk.CTkFont(size=28)).pack(side="left", padx=(0, 12))
        ht = ctk.CTkFrame(hi, fg_color="transparent")
        ht.pack(side="left", fill="y", expand=True)
        ctk.CTkLabel(ht, text=gname,
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=g["color"]).pack(anchor="w")
        ctk.CTkLabel(ht, text=g["desc"],
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(anchor="w")
        mkbtn(hi, "⚡  ОПТИМИЗИРОВАТЬ ВСЁ",
              lambda gn=gname: self._full_optimize(gn),
              size=12, width=200, color=g["color"], hover="#ffffff").pack(side="right")

        # Tab bar
        tab_bar = ctk.CTkFrame(outer, fg_color=PANEL2, corner_radius=0, height=40)
        tab_bar.pack(fill="x")
        tab_bar.pack_propagate(False)

        tab_content = ctk.CTkFrame(outer, fg_color=BG, corner_radius=0)
        tab_content.pack(fill="both", expand=True)

        tabs = {}
        tab_btns = {}
        tab_names = ["🎨 Графика", "🚫 Паразиты", "🌐 Сеть", "💡 Советы"]
        if gname == "CS2":
            tab_names.append("⚙️ Конфиг")
        if gname == "GTA V":
            tab_names.append("🟣 FiveM")
        if gname == "Rust":
            tab_names.append("🔩 Launch")

        def show_tab(tname, btns=tab_btns, all_tabs=tabs, gc=g["color"]):
            for t in all_tabs.values():
                t.pack_forget()
            all_tabs[tname].pack(fill="both", expand=True)
            for k2, b2 in btns.items():
                b2.configure(fg_color="#0d2040" if k2 == tname else "transparent",
                             text_color=gc if k2 == tname else DIM)

        for tname in tab_names:
            b = ctk.CTkButton(tab_bar, text=tname, anchor="w",
                              font=ctk.CTkFont(size=11), height=38,
                              fg_color="transparent", hover_color="#0d1e38",
                              text_color=DIM, corner_radius=0, width=120,
                              command=lambda t=tname: show_tab(t))
            b.pack(side="left", padx=2)
            tab_btns[tname] = b

        for tname in tab_names:
            scr = ctk.CTkScrollableFrame(tab_content, fg_color=BG,
                                         corner_radius=0, scrollbar_button_color=BORDER)
            tabs[tname] = scr
            pad = ctk.CTkFrame(scr, fg_color="transparent")
            pad.pack(fill="both", expand=True, padx=20, pady=14)
            if "Графика" in tname:
                self._tab_graphics(pad, gname, g)
            elif "Паразиты" in tname:
                self._tab_parasites(pad, gname, g)
            elif "Сеть" in tname:
                self._tab_network_game(pad, gname, g)
            elif "Советы" in tname:
                self._tab_tips(pad, g)
            elif "Конфиг" in tname:
                self._tab_cs2_config(pad)
            elif "FiveM" in tname:
                self._tab_fivem(pad)
            elif "Launch" in tname:
                self._tab_rust_launch(pad)

        show_tab(tab_names[0])

    # ── Tab: Graphics ────────────────────────────────────
    def _tab_graphics(self, pad, gname, g):
        ctk.CTkLabel(pad, text="🎨 Пресеты графики",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text="Выбери пресет — получишь параметры запуска для Steam",
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(anchor="w", pady=(0, 12))

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
                         font=ctk.CTkFont(size=10), text_color=DIM).pack(anchor="w", pady=(2, 6))
            fr = ctk.CTkFrame(ci, fg_color="transparent")
            fr.pack(anchor="w", pady=(0, 4))
            ctk.CTkLabel(fr, text="🎯 FPS: ",
                         font=ctk.CTkFont(size=10), text_color=DIM).pack(side="left")
            ctk.CTkLabel(fr, text=pdata["fps_expect"],
                         font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=GREEN).pack(side="left")
            ctk.CTkLabel(ci, text=f"📋 {len(pdata['settings'])} параметров",
                         font=ctk.CTkFont(size=10), text_color=DIM).pack(anchor="w", pady=(0, 8))
            mkbtn(ci, "✓  Применить",
                  lambda p=pdata, n=pname, lr=log_ref: self._apply_preset(p, n, lr),
                  size=11, bold=False, width=150,
                  color="#1a3050", hover="#2a4060").pack(anchor="w")

        log_ref[0] = self._log(pad, 100)

    def _apply_preset(self, pdata, pname, log_ref):
        if log_ref[0] is None:
            return
        self._clr(log_ref[0])
        self._w(log_ref[0], f"▶ Применяю «{pname}»...")
        def run():
            for k, v in pdata["settings"]:
                self._w(log_ref[0], f"  ✓ {k} = {v}")
                time.sleep(0.03)
            launch = pdata.get("launch", "")
            if launch:
                self._w(log_ref[0], "\n📋 Параметры запуска Steam:")
                self._w(log_ref[0], f"  {launch}")
                self._w(log_ref[0], "  → Steam → ПКМ на игре → Свойства → Параметры запуска")
            self._w(log_ref[0], f"\n✅ Готово! Ожид. FPS: {pdata['fps_expect']}")
        threading.Thread(target=run, daemon=True).start()

    # ── Tab: Parasites ───────────────────────────────────
    def _tab_parasites(self, pad, gname, g):
        ctk.CTkLabel(pad, text="🚫 Паразитные функции",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad,
                     text="Отключи ненужные функции внутри игры, оверлеи и фоновые процессы",
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(anchor="w", pady=(0, 12))

        # ── Внутри игры
        sec_lbl(pad, f"🎮 Внутри {gname} — ненужные функции")
        for ico, name, desc, accent, on_c, off_c in g["in_game"]:
            self._toggle_row(pad, f"{ico}  {name}", desc, on_c, off_c, accent=accent)

        # ── Оверлеи
        divider(pad)
        sec_lbl(pad, "🖥 Оверлеи — жрут FPS и память")
        overlays = [
            ("🎮", "Xbox Game Bar / Game DVR", "Сжирает 5-15% CPU, вызывает фризы", RED,
             ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f',
              'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f'],
             ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 1 /f']),
            ("📸", "NVIDIA ShadowPlay", "Записывает видео в фоне, нагружает GPU", ORANGE,
             ['reg add "HKCU\\Software\\NVIDIA Corporation\\NVCapture" /v CaptureEnabled /t REG_DWORD /d 0 /f'],
             ['reg add "HKCU\\Software\\NVIDIA Corporation\\NVCapture" /v CaptureEnabled /t REG_DWORD /d 1 /f']),
            ("💬", "Discord оверлей", "+3-8ms задержки на кадр", PURPLE,
             ['reg add "HKCU\\Software\\Discord" /v Overlay /t REG_DWORD /d 0 /f'],
             ['reg add "HKCU\\Software\\Discord" /v Overlay /t REG_DWORD /d 1 /f']),
            ("🎵", "Steam оверлей", "Shift+Tab лагает, грузит память", NEON,
             ['reg add "HKCU\\Software\\Valve\\Steam" /v SteamOverlayEnabled /t REG_DWORD /d 0 /f'],
             ['reg add "HKCU\\Software\\Valve\\Steam" /v SteamOverlayEnabled /t REG_DWORD /d 1 /f']),
        ]
        for ico, name, desc, accent, on_c, off_c in overlays:
            self._toggle_row(pad, f"{ico}  {name}", desc, on_c, off_c, accent=accent)

        # ── Фоновые процессы
        divider(pad)
        sec_lbl(pad, "⚙️ Фоновые процессы Windows")
        win_p = [
            ("🔄", "Windows Update", "Качает обновления во время игры", RED,
             ["net stop wuauserv", "net stop bits", "net stop dosvc"],
             ["net start wuauserv"]),
            ("🔍", "Windows Search", "Индексирует файлы, грузит диск", ORANGE,
             ["net stop wsearch", "sc config wsearch start=disabled"],
             ["net start wsearch", "sc config wsearch start=auto"]),
            ("📊", "SysMain / Superfetch", "Предзагрузка программ мешает играм", GOLD,
             ["net stop sysmain", "sc config sysmain start=disabled"],
             ["net start sysmain", "sc config sysmain start=auto"]),
            ("☁️", "OneDrive синхронизация", "Грузит диск и сеть во время игры", NEON,
             ["taskkill /f /im OneDrive.exe", "sc config OneSyncSvc start=disabled"],
             ["sc config OneSyncSvc start=auto"]),
        ]
        for ico, name, desc, accent, on_c, off_c in win_p:
            self._toggle_row(pad, f"{ico}  {name}", desc, on_c, off_c, accent=accent)

        divider(pad)
        mkbtn(pad, "🚫  ОТКЛЮЧИТЬ ВСЕ ПАРАЗИТЫ",
              self._disable_all_parasites, size=13, width=260,
              color="#6b0000", hover="#8b0000").pack(anchor="w")

    def _disable_all_parasites(self):
        cmds = [
            'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f',
            "net stop wuauserv", "net stop wsearch", "net stop sysmain",
            "taskkill /f /im OneDrive.exe",
        ]
        threading.Thread(target=lambda: [run_cmd(c) for c in cmds], daemon=True).start()

    # ── Tab: Network (per game) ───────────────────────────
    def _tab_network_game(self, pad, gname, g):
        ctk.CTkLabel(pad, text="🌐 Настройка сети",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text=f"Оптимизация пинга для {gname}",
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(anchor="w", pady=(0, 12))

        net = [
            ("🌐", "DNS Google + Cloudflare", "8.8.8.8 + 1.1.1.1 — быстрый DNS", GREEN,
             ['netsh interface ip set dns "Ethernet" static 8.8.8.8',
              'netsh interface ip add dns "Ethernet" 1.1.1.1 index=2', "ipconfig /flushdns"],
             ['netsh interface ip set dns "Ethernet" dhcp', "ipconfig /flushdns"]),
            ("🏎", "Откл. Nagle", "TcpAckFrequency=1, -5-30ms пинга", NEON,
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TcpAckFrequency /t REG_DWORD /d 1 /f',
              'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TCPNoDelay /t REG_DWORD /d 1 /f'],
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TcpAckFrequency /t REG_DWORD /d 2 /f']),
            ("🔕", "Откл. IPv6", "Убирает конфликты IPv4/IPv6", ORANGE,
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters" /v DisabledComponents /t REG_DWORD /d 255 /f'],
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters" /v DisabledComponents /t REG_DWORD /d 0 /f']),
            ("🔄", "Сброс Winsock", "Полный сброс сетевого стека", RED,
             ["netsh winsock reset", "netsh int ip reset", "ipconfig /flushdns"], []),
        ]
        for ico, name, desc, accent, on_c, off_c in net:
            self._toggle_row(pad, f"{ico}  {name}", desc, on_c, off_c, accent=accent)

        divider(pad)
        mkbtn(pad, "📡  Проверить пинг",
              lambda: self._quick_ping(pad), width=180,
              color="#006adf", hover="#0090ff").pack(anchor="w")

    def _quick_ping(self, pad):
        log = self._log(pad, 80)
        def run():
            for name, host in [("Steam", "store.steampowered.com"),
                                ("Cloudflare", "1.1.1.1"), ("Google", "8.8.8.8")]:
                ms = ping_host(host)
                self._w(log, f"{'✓' if ms > 0 else '✗'}  {name:<14} {ms if ms > 0 else 'timeout'} {'ms' if ms > 0 else ''}")
                time.sleep(0.1)
            self._w(log, "✅ Готово!")
        threading.Thread(target=run, daemon=True).start()

    # ── Tab: Tips ─────────────────────────────────────────
    def _tab_tips(self, pad, g):
        ctk.CTkLabel(pad, text="💡 Советы",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 12))
        for tip in g["tips"]:
            c = ctk.CTkFrame(pad, fg_color=PANEL2, corner_radius=9,
                             border_width=1, border_color=BORDER)
            c.pack(fill="x", pady=3)
            ci = ctk.CTkFrame(c, fg_color="transparent")
            ci.pack(fill="x", padx=14, pady=10)
            ctk.CTkLabel(ci, text=f"{tip['icon']}  {tip['title']}",
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="#fff").pack(anchor="w")
            ctk.CTkLabel(ci, text=tip["text"],
                         font=ctk.CTkFont(size=11), text_color=TEXT,
                         wraplength=700, justify="left").pack(anchor="w", pady=(2, 0))

    # ── Tab: CS2 config ───────────────────────────────────
    def _tab_cs2_config(self, pad):
        ctk.CTkLabel(pad, text="⚙️ autoexec.cfg",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text="Готовый конфиг для максимального FPS",
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(anchor="w", pady=(0, 10))
        cfg = ("fps_max 0\nr_lowlatency 2\ncl_showfps 1\nmat_queue_mode -1\n"
               "r_dynamic_lighting 0\nr_shadowrendertotexture 0\nr_shadows 0\n"
               "cl_ragdoll_physics_enable 0\nr_motionblur 0\ncl_interp 0\n"
               "cl_interp_ratio 1\nrate 786432\ncl_updaterate 128\ncl_cmdrate 128\n"
               "m_rawinput 1\nsensitivity 2.0\nsnd_menumusic_volume 0")
        tb = ctk.CTkTextbox(pad, height=260, fg_color="#020810",
                            border_width=1, border_color=BORDER,
                            font=ctk.CTkFont(family="Courier New", size=12),
                            text_color="#68ffaa", corner_radius=8)
        tb.pack(fill="x", pady=(0, 10))
        tb.insert("end", cfg)
        mkbtn(pad, "💾  Сохранить в Downloads",
              lambda: self._save_cfg(tb.get("1.0", "end"), "autoexec.cfg"),
              width=230, color="#006adf", hover="#0090ff").pack(anchor="w")

    def _save_cfg(self, content, filename):
        path = os.path.join(os.path.expanduser("~"), "Downloads", filename)
        try:
            with open(path, "w") as f:
                f.write(content)
        except:
            pass

    # ── Tab: FiveM ────────────────────────────────────────
    def _tab_fivem(self, pad):
        ctk.CTkLabel(pad, text="🟣 FiveM оптимизация",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text="Специальные твики для FiveM серверов",
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(anchor="w", pady=(0, 12))
        opts = [
            ("🧹", "Очистить кэш FiveM", "Удаляет кэш шейдеров и текстур", NEON,
             [r'rmdir /s /q "%LOCALAPPDATA%\FiveM\FiveM.app\cache"'], []),
            ("🔕", "Откл. оверлей FiveM", "Убирает оверлей сервера", ORANGE,
             ['reg add "HKCU\\Software\\CitizenFX\\FiveM" /v DrawOverlay /t REG_DWORD /d 0 /f'],
             ['reg add "HKCU\\Software\\CitizenFX\\FiveM" /v DrawOverlay /t REG_DWORD /d 1 /f']),
            ("⚡", "StreamMemory 756MB", "Увеличить память стриминга текстур", GREEN,
             ['reg add "HKCU\\Software\\CitizenFX\\FiveM" /v StreamingMemory /t REG_DWORD /d 756 /f'],
             ['reg add "HKCU\\Software\\CitizenFX\\FiveM" /v StreamingMemory /t REG_DWORD /d 512 /f']),
        ]
        for ico, name, desc, accent, on_c, off_c in opts:
            self._toggle_row(pad, f"{ico}  {name}", desc, on_c, off_c, accent=accent)
        divider(pad)
        ctk.CTkLabel(pad, text="💡 Добавь +set fpslimit 0 в параметры запуска FiveM",
                     font=ctk.CTkFont(size=11, slant="italic"), text_color=GOLD).pack(anchor="w")

    # ── Tab: Rust launch ──────────────────────────────────
    def _tab_rust_launch(self, pad):
        ctk.CTkLabel(pad, text="🔩 Launch Arguments",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text="Вставь в Steam → ПКМ на Rust → Свойства → Параметры запуска",
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(anchor="w", pady=(0, 10))
        for pname, args in [
            ("⚡ Максимум FPS",
             "-high -maxMem=8192 -malloc=system -force-feature-level-11-0 +clientgc 256 +fps.limit 0 -nolog"),
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
            tb = ctk.CTkTextbox(ci, height=40, fg_color="#020810",
                                border_width=1, border_color=BORDER,
                                font=ctk.CTkFont(family="Courier New", size=11),
                                text_color=NEON, corner_radius=6)
            tb.pack(fill="x", pady=(4, 0))
            tb.insert("end", args)

    # ── Full optimize ─────────────────────────────────────
    def _full_optimize(self, gname):
        win = ctk.CTkToplevel(self)
        win.title(f"Оптимизация {gname}")
        win.geometry("500x380")
        win.configure(fg_color=BG)
        ctk.CTkLabel(win, text=f"⚡ Полная оптимизация {gname}",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#fff").pack(pady=(16, 8), padx=16, anchor="w")
        log = self._log(win, 260)
        log.pack_forget()
        log.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        def run():
            steps = [
                ("⚡ Высокий план питания",
                 "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"),
                ("🔕 Откл. Game DVR",
                 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f'),
                ("🌐 DNS Google",
                 'netsh interface ip set dns "Ethernet" static 8.8.8.8'),
                ("🏎 Откл. Nagle",
                 'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TcpAckFrequency /t REG_DWORD /d 1 /f'),
                ("🔄 Flush DNS", "ipconfig /flushdns"),
                ("⏸ Стоп Win Update", "net stop wuauserv"),
                ("🔍 Стоп Indexer", "net stop wsearch"),
                ("🧹 Очистка RAM", "rundll32.exe advapi32.dll,ProcessIdleTasks"),
            ]
            for name, cmd in steps:
                ok = run_cmd(cmd)
                self._w(log, f"  {'✓' if ok else '✗'} {name}")
                time.sleep(0.15)
            self._w(log, f"\n✅ Готово! Запускай {gname}!")
        threading.Thread(target=run, daemon=True).start()

    # ── Windows page ──────────────────────────────────────
    def _build_windows(self):
        p = self._scr("windows")
        pad = ctk.CTkFrame(p, fg_color="transparent")
        pad.pack(fill="both", expand=True, padx=22, pady=16)
        ctk.CTkLabel(pad, text="⚡ Оптимизация Windows",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text="Системные твики для максимального FPS",
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(anchor="w", pady=(0, 12))
        opts = [
            ("⚡","Высокий план питания","Максимальная производительность CPU",NEON,
             ["powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"],
             ["powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e"]),
            ("📈","Приоритет CPU (Win32=38)","Лучший отклик в играх",GREEN,
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f'],
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 2 /f']),
            ("🎮","HAGS (GPU Scheduling)","Меньше задержка GPU",PURPLE,
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v HwSchMode /t REG_DWORD /d 2 /f'],
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v HwSchMode /t REG_DWORD /d 1 /f']),
            ("🖥","Откл. визуальные эффекты","Анимации Windows — ненужный расход",ORANGE,
             ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f'],
             ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 0 /f']),
            ("🔕","Откл. Xbox Game Bar","-5-15% CPU в играх",RED,
             ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f'],
             ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 1 /f']),
            ("🔍","Откл. Windows Search","Не индексирует во время игры",GOLD,
             ["net stop wsearch","sc config wsearch start=disabled"],
             ["net start wsearch","sc config wsearch start=auto"]),
            ("📊","Откл. SysMain","Освобождает RAM и диск",ORANGE,
             ["net stop sysmain","sc config sysmain start=disabled"],
             ["net start sysmain","sc config sysmain start=auto"]),
            ("🧹","Очистка RAM","Освобождает память перед игрой",GREEN,
             ["rundll32.exe advapi32.dll,ProcessIdleTasks"],[]),
            ("⏸","Пауза Windows Update","Обновления не мешают игре",RED,
             ["net stop wuauserv","net stop bits","net stop dosvc"],
             ["net start wuauserv"]),
        ]
        for ico, name, desc, accent, on_c, off_c in opts:
            self._toggle_row(pad, f"{ico}  {name}", desc, on_c, off_c, accent=accent)
        divider(pad)
        mkbtn(pad, "⚡  ПРИМЕНИТЬ ВСЕ",
              self._run_all_windows, size=14, width=260,
              color="#006adf", hover="#0090ff").pack(anchor="w")
        self.win_log = self._log(pad, 100)

    def _run_all_windows(self):
        self._clr(self.win_log)
        self._w(self.win_log, "⚡ Применяю все оптимизации...")
        cmds = [
            ("⚡ План питания", "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"),
            ("🔕 Game DVR", 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f'),
            ("📈 Приоритет CPU", 'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f'),
            ("🎮 HAGS", 'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v HwSchMode /t REG_DWORD /d 2 /f'),
            ("🔍 Search", "net stop wsearch"),
            ("📊 SysMain", "net stop sysmain"),
            ("⏸ Update", "net stop wuauserv"),
            ("🧹 RAM", "rundll32.exe advapi32.dll,ProcessIdleTasks"),
        ]
        def run():
            for name, cmd in cmds:
                ok = run_cmd(cmd)
                self._w(self.win_log, f"  {'✓' if ok else '✗'} {name}")
                time.sleep(0.1)
            self._w(self.win_log, "\n✅ Готово! Перезагрузи ПК для полного эффекта.")
        threading.Thread(target=run, daemon=True).start()

    # ── Network page ──────────────────────────────────────
    def _build_network(self):
        p = self._scr("network")
        pad = ctk.CTkFrame(p, fg_color="transparent")
        pad.pack(fill="both", expand=True, padx=22, pady=16)
        ctk.CTkLabel(pad, text="🌐 Настройка сети",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text="Оптимизация пинга для всех игр",
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(anchor="w", pady=(0, 12))
        opts = [
            ("🌐","DNS Google + Cloudflare","8.8.8.8 + 1.1.1.1",GREEN,
             ['netsh interface ip set dns "Ethernet" static 8.8.8.8',
              'netsh interface ip add dns "Ethernet" 1.1.1.1 index=2',"ipconfig /flushdns"],
             ['netsh interface ip set dns "Ethernet" dhcp',"ipconfig /flushdns"]),
            ("🏎","Откл. Nagle","-5-30ms пинга",NEON,
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TcpAckFrequency /t REG_DWORD /d 1 /f',
              'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TCPNoDelay /t REG_DWORD /d 1 /f'],
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TcpAckFrequency /t REG_DWORD /d 2 /f']),
            ("📶","QoS DSCP=46","Приоритет игрового трафика",PURPLE,
             ['netsh qos delete policy "GO_Game"',
              'netsh qos add policy "GO_Game" app="*" dscp=46 throttle-rate=-1'],
             ['netsh qos delete policy "GO_Game"']),
            ("🔕","Откл. IPv6","Убирает конфликты",ORANGE,
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters" /v DisabledComponents /t REG_DWORD /d 255 /f'],
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters" /v DisabledComponents /t REG_DWORD /d 0 /f']),
            ("🔄","Сброс Winsock","Полный сброс сети",RED,
             ["netsh winsock reset","netsh int ip reset","ipconfig /flushdns"],[]),
        ]
        for ico, name, desc, accent, on_c, off_c in opts:
            self._toggle_row(pad, f"{ico}  {name}", desc, on_c, off_c, accent=accent)
        divider(pad)
        mkbtn(pad, "📡  Проверить пинг",
              self._run_global_ping, width=180,
              color="#006adf", hover="#0090ff").pack(anchor="w")
        self.net_log = self._log(pad, 110)

    def _run_global_ping(self):
        self._clr(self.net_log)
        def run():
            for name, host in [("Steam","store.steampowered.com"),
                                ("Cloudflare","1.1.1.1"),("Google","8.8.8.8"),
                                ("Faceit","api.faceit.com"),("AWS EU","ec2.eu-central-1.amazonaws.com")]:
                ms = ping_host(host)
                s = "OK ✓" if 0 < ms < 80 else "СРЕДНИЙ" if 0 < ms < 150 else "ВЫСОКИЙ ⚠" if ms > 0 else "timeout ✗"
                self._w(self.net_log, f"  {name:<16} {str(ms)+' ms' if ms>0 else 'timeout':>10}  {s}")
                time.sleep(0.1)
            self._w(self.net_log, "✅ Готово!")
        threading.Thread(target=run, daemon=True).start()

    # ── Monitor page ──────────────────────────────────────
    def _build_monitor(self):
        p = self._scr("monitor")
        pad = ctk.CTkFrame(p, fg_color="transparent")
        pad.pack(fill="both", expand=True, padx=22, pady=16)
        ctk.CTkLabel(pad, text="📊 Мониторинг пинга",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(pad, text="Живой график задержки",
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(anchor="w", pady=(0, 10))

        # Stats row
        sr = ctk.CTkFrame(pad, fg_color="transparent")
        sr.pack(fill="x", pady=(0, 10))
        for i in range(3):
            sr.columnconfigure(i, weight=1)
        def stat(col, label, color):
            f = ctk.CTkFrame(sr, fg_color=PANEL2, corner_radius=9,
                             border_width=1, border_color=BORDER)
            f.grid(row=0, column=col, padx=4, sticky="ew")
            v = ctk.CTkLabel(f, text="—",
                             font=ctk.CTkFont(size=24, weight="bold"), text_color=color)
            v.pack(pady=(10, 2))
            ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=10),
                         text_color=DIM).pack(pady=(0, 8))
            return v
        self.ms_cur = stat(0, "Текущий ms", GREEN)
        self.ms_avg = stat(1, "Средний ms", GOLD)
        self.ms_max = stat(2, "Максимум ms", RED)

        # Controls
        cr = ctk.CTkFrame(pad, fg_color="transparent")
        cr.pack(fill="x", pady=(0, 10))
        self.mon_btn = mkbtn(cr, "▶  Запустить", self._toggle_mon,
                             width=200, color="#006adf", hover="#0090ff")
        self.mon_btn.pack(side="left")
        self.mon_lbl = ctk.CTkLabel(cr, text="● Остановлен",
                                    text_color=DIM, font=ctk.CTkFont(size=11))
        self.mon_lbl.pack(side="left", padx=12)
        ctk.CTkLabel(cr, text="Интервал:", text_color=DIM,
                     font=ctk.CTkFont(size=11)).pack(side="left")
        self.mon_int = ctk.CTkComboBox(cr, values=["2 сек","5 сек","10 сек"],
                                       width=88, fg_color=PANEL2, border_color=BORDER)
        self.mon_int.set("2 сек")
        self.mon_int.pack(side="left", padx=6)

        # Server rows
        self.srv_lbls = {}
        for name, host in [("Steam","store.steampowered.com"),
                            ("Cloudflare","1.1.1.1"),
                            ("Google DNS","8.8.8.8"),
                            ("Faceit","api.faceit.com")]:
            row = ctk.CTkFrame(pad, fg_color=PANEL2, corner_radius=8,
                               border_width=1, border_color=BORDER)
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text="●", font=ctk.CTkFont(size=12),
                         text_color=DIM).pack(side="left", padx=(12,8), pady=8)
            ctk.CTkLabel(row, text=name, font=ctk.CTkFont(size=12),
                         text_color=TEXT, width=130).pack(side="left")
            lbl = ctk.CTkLabel(row, text="— ms",
                               font=ctk.CTkFont(size=12, weight="bold"), text_color=DIM)
            lbl.pack(side="right", padx=14)
            self.srv_lbls[host] = lbl

        # Chart
        cc = ctk.CTkFrame(pad, fg_color=PANEL2, corner_radius=12,
                          border_width=1, border_color=BORDER)
        cc.pack(fill="x", pady=6)
        ctk.CTkLabel(cc, text="📈 График пинга",
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(anchor="w", padx=12, pady=(8,2))
        self.chart = tkinter.Canvas(cc, height=110, bg="#020810", highlightthickness=0)
        self.chart.pack(fill="x", padx=10, pady=(0,8))

    def _toggle_mon(self):
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
            threading.Thread(target=self._mon_loop, daemon=True).start()

    def _mon_loop(self):
        while self.monitor_running:
            iv = {"2 сек":2,"5 сек":5,"10 сек":10}.get(self.mon_int.get(), 2)
            results = []
            for name, host in [("Steam","store.steampowered.com"),
                                ("Cloudflare","1.1.1.1"),
                                ("Google DNS","8.8.8.8"),
                                ("Faceit","api.faceit.com")]:
                ms = ping_host(host)
                results.append(ms)
                lbl = self.srv_lbls[host]
                if ms < 0:
                    lbl.configure(text="timeout", text_color=RED)
                else:
                    c = GREEN if ms < 80 else GOLD if ms < 150 else RED
                    lbl.configure(text=f"{ms} ms", text_color=c)
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
        pts = [(int(10 + (i/(len(self.ping_history)-1))*(W-20)),
                int(H-10-(v/maxV)*(H-20)))
               for i, v in enumerate(self.ping_history)]
        poly = [(10, H-10)] + pts + [(pts[-1][0], H-10)]
        c.create_polygon([x for pt in poly for x in pt], fill="#003030", outline="")
        last = self.ping_history[-1]
        col = "#00ff88" if last < 80 else "#ffd700" if last < 150 else "#ff4466"
        c.create_line([x for pt in pts for x in pt], fill=col, width=2, smooth=True)

if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(10000)
    app = App()
    app.mainloop()
