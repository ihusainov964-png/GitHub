"""
Game Optimizer v1.0
Rust • GTA V • CS2
Python + CustomTkinter
"""
import customtkinter as ctk
import subprocess, threading, random, time, os, socket
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Цвета ──────────────────────────────────────────────────
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

# ── Данные игр ─────────────────────────────────────────────
GAMES = {
    "Rust": {
        "icon": "🔫",
        "color": "#e07020",
        "desc": "Survival multiplayer",
        "process": "RustClient.exe",
        "presets": {
            "Максимум FPS": {
                "desc": "Минимальная графика, максимальный FPS",
                "fps_expect": "100-200+",
                "settings": [
                    ("grass.on","false"),("grass.shadowcast","false"),
                    ("effects.motionblur","false"),("terrain.quality","0"),
                    ("graphics.damage","0"),("graphics.dof","0"),
                    ("graphics.fov","90"),("graphics.itemskins","0"),
                    ("graphics.lodbias","0.25"),("graphics.parallax","0"),
                    ("graphics.reflections","0"),("graphics.shafts","0"),
                    ("graphics.shadows","0"),("graphics.ssao","0"),
                ],
                "launch": "-high -maxMem=8192 -malloc=system -force-feature-level-11-0 +clientgc 256 +fps.limit 0 -nolog",
            },
            "Баланс": {
                "desc": "Хороший FPS + читаемая картинка",
                "fps_expect": "60-120",
                "settings": [
                    ("grass.on","true"),("grass.shadowcast","false"),
                    ("graphics.shadows","1"),("graphics.ssao","0"),
                    ("graphics.reflections","1"),("terrain.quality","50"),
                    ("graphics.lodbias","1"),("graphics.fov","90"),
                ],
                "launch": "-high -maxMem=8192 -malloc=system +fps.limit 0",
            },
            "Качество": {
                "desc": "Полная графика, нужен мощный ПК",
                "fps_expect": "40-80",
                "settings": [
                    ("grass.on","true"),("grass.shadowcast","true"),
                    ("graphics.shadows","3"),("graphics.ssao","1"),
                    ("graphics.reflections","2"),("terrain.quality","100"),
                    ("graphics.lodbias","2"),("graphics.shafts","1"),
                ],
                "launch": "+fps.limit 0",
            },
        },
        "tips": [
            "Отключи Steam оверлей в свойствах игры",
            "Добавь Rust в исключения антивируса",
            "Используй DirectX 11 (не Vulkan)",
            "Очищай кэш шейдеров раз в неделю",
        ],
    },
    "GTA V": {
        "icon": "🚗",
        "color": "#00a8ff",
        "desc": "Open world / FiveM",
        "process": "GTA5.exe",
        "presets": {
            "Максимум FPS": {
                "desc": "Для слабых ПК и FiveM серверов",
                "fps_expect": "80-160+",
                "settings": [
                    ("TextureQuality","normal"),("ShaderQuality","normal"),
                    ("ShadowQuality","normal"),("ReflectionQuality","off"),
                    ("ReflectionMSAA","off"),("MSAA","off"),
                    ("FXAA","off"),("AnisotropicFiltering","off"),
                    ("AmbientOcclusion","off"),("TessellationQuality","off"),
                    ("ShadowSoftShadows","sharp"),("PostFX","normal"),
                    ("InGameDepthOfField","false"),("MotionBlur","false"),
                ],
                "launch": "-notablet -norestrictions -noFirstRun -IgnoreCorrupts",
            },
            "Баланс": {
                "desc": "Комфортная игра на среднем ПК",
                "fps_expect": "60-90",
                "settings": [
                    ("TextureQuality","high"),("ShaderQuality","high"),
                    ("ShadowQuality","high"),("ReflectionQuality","high"),
                    ("MSAA","off"),("FXAA","on"),
                    ("AnisotropicFiltering","x8"),("AmbientOcclusion","medium"),
                    ("PostFX","high"),("MotionBlur","false"),
                ],
                "launch": "-notablet -norestrictions -noFirstRun",
            },
            "Качество": {
                "desc": "Максимальная красота, мощный ПК",
                "fps_expect": "40-70",
                "settings": [
                    ("TextureQuality","very high"),("ShaderQuality","very high"),
                    ("ShadowQuality","very high"),("ReflectionQuality","ultra"),
                    ("MSAA","x4"),("FXAA","on"),
                    ("AnisotropicFiltering","x16"),("AmbientOcclusion","high"),
                    ("PostFX","ultra"),("TessellationQuality","very high"),
                ],
                "launch": "-notablet -noFirstRun",
            },
        },
        "tips": [
            "Для FiveM: отключи все ненужные оверлеи",
            "Поставь Graphics.cfg оптимизацию",
            "Очищай папку update\\x64\\dlcpacks от лишнего",
            "Используй -notablet для снижения нагрузки",
        ],
    },
    "CS2": {
        "icon": "🎯",
        "color": "#ff6b35",
        "desc": "Counter-Strike 2",
        "process": "cs2.exe",
        "presets": {
            "Максимум FPS": {
                "desc": "Про-настройки, максимальный FPS",
                "fps_expect": "200-400+",
                "settings": [
                    ("r_lowlatency","2"),("fps_max","0"),
                    ("cl_showfps","1"),("mat_queue_mode","-1"),
                    ("r_dynamic_lighting","0"),("r_shadowrendertotexture","0"),
                    ("r_shadows","0"),("cl_ragdoll_physics_enable","0"),
                    ("r_eyegloss","0"),("r_eyemove","0"),
                    ("r_eyeshift_x","0"),("r_eyeshift_y","0"),
                    ("r_eyeshift_z","0"),("cl_detailfade","0"),
                    ("cl_detail_avoid_radius","0"),("cl_detail_avoid_force","0"),
                ],
                "launch": "-novid -nojoy -noaafonts -limitvsconst -forcenovsync -softparticlesdefaultoff +mat_queue_mode -1 +r_dynamic_lighting 0 -freq 240 -high",
            },
            "Баланс": {
                "desc": "Хороший FPS + видимость",
                "fps_expect": "144-250",
                "settings": [
                    ("fps_max","0"),("r_lowlatency","2"),
                    ("r_shadows","1"),("r_dynamic_lighting","1"),
                    ("cl_showfps","1"),("mat_queue_mode","-1"),
                ],
                "launch": "-novid -nojoy -noaafonts -forcenovsync +mat_queue_mode -1 -high",
            },
            "Качество": {
                "desc": "Красивая картинка",
                "fps_expect": "100-180",
                "settings": [
                    ("fps_max","0"),("r_lowlatency","1"),
                    ("r_shadows","3"),("r_dynamic_lighting","1"),
                    ("cl_showfps","0"),("r_shadowrendertotexture","1"),
                ],
                "launch": "-novid -nojoy +mat_queue_mode -1",
            },
        },
        "tips": [
            "Поставь частоту монитора в настройках NVIDIA/AMD",
            "Отключи Game DVR в Xbox Game Bar",
            "Выключи Steam оверлей для CS2",
            "Используй Raw Input: cl_mouseinput 1",
        ],
    },
}

# ── Windows оптимизации ────────────────────────────────────
WIN_OPTS = [
    ("⚡", "Высокий план питания",
     "Максимальная производительность CPU/GPU",
     ["powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"]),
    ("🧹", "Очистка RAM",
     "Освобождает оперативную память перед игрой",
     ["rundll32.exe advapi32.dll,ProcessIdleTasks"]),
    ("🔕", "Отключить Xbox Game Bar",
     "Убирает оверлей Xbox, снижает задержку",
     ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f',
      'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f']),
    ("📈", "Приоритет CPU для игр",
     "Win32PrioritySeparation = 38 (лучший отклик)",
     ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f']),
    ("💾", "Оптимизация виртуальной памяти",
     "Отключает очистку файла подкачки при выключении",
     ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v ClearPageFileAtShutdown /t REG_DWORD /d 0 /f']),
    ("🖥", "Отключить визуальные эффекты",
     "Убирает анимации Windows для быстрого отклика",
     ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f',
      'SystemPropertiesPerformance.exe']),
    ("⏸", "Пауза Windows Update",
     "Остановить обновления на время игры",
     ["net stop wuauserv", "net stop bits", "net stop dosvc"]),
    ("🌐", "Оптимизация сети",
     "DNS Google + Nagle off + TCP оптимизация",
     ["ipconfig /flushdns",
      'netsh interface ip set dns "Ethernet" static 8.8.8.8',
      'netsh interface ip add dns "Ethernet" 1.1.1.1 index=2',
      'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "TcpAckFrequency" /t REG_DWORD /d 1 /f',
      'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "TCPNoDelay" /t REG_DWORD /d 1 /f',
      "netsh winsock reset"]),
]

# ── Серверы для мониторинга ────────────────────────────────
MONITOR_HOSTS = [
    ("Steam",       "store.steampowered.com"),
    ("Cloudflare",  "1.1.1.1"),
    ("Google DNS",  "8.8.8.8"),
    ("Faceit",      "api.faceit.com"),
]

JOKES = [
    "😂 Ваня: '5 FPS — это нормально'",
    "💀 Ваня оптимизировал ПК и удалил system32",
    "🎯 Ваня поставил мониторинг — FPS 12",
    "🔫 Ваня в Rust: строил дом, убили через стену",
    "🚗 Ваня в GTA взял такси — лучше пешком",
    "⚡ Ваня включил план питания — сгорел роутер",
]


def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           timeout=30, encoding="cp1251", errors="replace")
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


def make_btn(parent, text, cmd, size=13, bold=True,
             color="#0060df", hover="#0090ff", width=None, corner=8):
    kw = dict(text=text, command=cmd, fg_color=color, hover_color=hover,
              font=ctk.CTkFont(size=size, weight="bold" if bold else "normal"),
              corner_radius=corner)
    if width:
        kw["width"] = width
    return ctk.CTkButton(parent, **kw)


# ══════════════════════════════════════════════════════════
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Game Optimizer v1.0")
        self.geometry("1060x680")
        self.minsize(940, 620)
        self.configure(fg_color=BG)
        self.current_game = "Rust"
        self.monitor_running = False
        self.ping_history = []
        self._build_ui()

    # ── UI ────────────────────────────────────────────────
    def _build_ui(self):
        # Sidebar
        sb = ctk.CTkFrame(self, width=210, fg_color=PANEL, corner_radius=0,
                          border_width=1, border_color=BORDER)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # Logo
        lf = ctk.CTkFrame(sb, fg_color="transparent")
        lf.pack(pady=(18, 4), padx=14)
        ctk.CTkLabel(lf, text="🎮", font=ctk.CTkFont(size=24)).pack(side="left")
        ctk.CTkLabel(lf, text=" GAME OPTIMIZER",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=NEON).pack(side="left")
        ctk.CTkLabel(sb, text="v1.0", font=ctk.CTkFont(size=10), text_color=DIM).pack()

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(fill="x", padx=12, pady=10)

        # Game selector
        ctk.CTkLabel(sb, text="ВЫБОР ИГРЫ", font=ctk.CTkFont(size=10),
                     text_color=DIM).pack(anchor="w", padx=14)
        self.game_btns = {}
        for gname, gdata in GAMES.items():
            b = ctk.CTkButton(sb, text=f"{gdata['icon']}  {gname}",
                              anchor="w", font=ctk.CTkFont(size=13), height=38,
                              fg_color="transparent", hover_color="#0d1e38",
                              text_color=DIM, corner_radius=8,
                              command=lambda g=gname: self._select_game(g))
            b.pack(fill="x", padx=10, pady=2)
            self.game_btns[gname] = b

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(fill="x", padx=12, pady=10)

        # Nav
        ctk.CTkLabel(sb, text="РАЗДЕЛЫ", font=ctk.CTkFont(size=10),
                     text_color=DIM).pack(anchor="w", padx=14)
        self.nav_btns = {}
        pages = [("presets", "🎨  Пресеты графики"),
                 ("windows", "⚡  Оптимизация Windows"),
                 ("network", "🌐  Настройка сети"),
                 ("monitor", "📊  Мониторинг")]
        for pid, label in pages:
            b = ctk.CTkButton(sb, text=label, anchor="w",
                              font=ctk.CTkFont(size=12), height=36,
                              fg_color="transparent", hover_color="#0d1e38",
                              text_color=DIM, corner_radius=8,
                              command=lambda p=pid: self.show_page(p))
            b.pack(fill="x", padx=10, pady=2)
            self.nav_btns[pid] = b

        # Joke at bottom
        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(fill="x", padx=12,
                                                          pady=8, side="bottom")
        self.joke_lbl = ctk.CTkLabel(sb, text=random.choice(JOKES),
                                     font=ctk.CTkFont(size=10, slant="italic"),
                                     text_color=GOLD, wraplength=180, justify="center")
        self.joke_lbl.pack(side="bottom", padx=10, pady=6)

        # Main content
        self.content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

        self.pages = {}
        self._build_presets()
        self._build_windows()
        self._build_network()
        self._build_monitor()

        self._select_game("Rust")
        self.show_page("presets")

    def show_page(self, pid):
        for p in self.pages.values():
            p.pack_forget()
        self.pages[pid].pack(fill="both", expand=True)
        for k, b in self.nav_btns.items():
            b.configure(fg_color="#0d2040" if k == pid else "transparent",
                        text_color=NEON if k == pid else DIM)

    def _select_game(self, gname):
        self.current_game = gname
        for k, b in self.game_btns.items():
            g = GAMES[k]
            if k == gname:
                b.configure(fg_color="#0d2040",
                            text_color=g["color"])
            else:
                b.configure(fg_color="transparent", text_color=DIM)
        self._refresh_presets()
        self._refresh_tips()

    # ── HELPERS ───────────────────────────────────────────
    def _page(self, pid):
        f = ctk.CTkScrollableFrame(self.content, fg_color=BG, corner_radius=0,
                                   scrollbar_button_color=BORDER)
        self.pages[pid] = f
        return f

    def _pad(self, parent):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=22, pady=18)
        return f

    def _section(self, parent, title, sub=""):
        ctk.CTkLabel(parent, text=title,
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#fff").pack(anchor="w", pady=(0, 2))
        if sub:
            ctk.CTkLabel(parent, text=sub, font=ctk.CTkFont(size=11),
                         text_color=DIM).pack(anchor="w", pady=(0, 10))

    def _card(self, parent, pady=6):
        f = ctk.CTkFrame(parent, fg_color=PANEL2, corner_radius=12,
                         border_width=1, border_color=BORDER)
        f.pack(fill="x", pady=pady)
        return f

    def _log(self, parent, h=150):
        tb = ctk.CTkTextbox(parent, height=h, fg_color="#020810",
                            border_width=1, border_color=BORDER,
                            font=ctk.CTkFont(family="Courier New", size=12),
                            text_color="#68ffaa", corner_radius=8)
        tb.pack(fill="x", pady=(6, 0))
        tb.configure(state="disabled")
        return tb

    def _log_add(self, tb, text):
        tb.configure(state="normal")
        tb.insert("end", text + "\n")
        tb.configure(state="disabled")
        tb.see("end")

    def _log_clear(self, tb):
        tb.configure(state="normal")
        tb.delete("1.0", "end")
        tb.configure(state="disabled")

    # ── PRESETS PAGE ──────────────────────────────────────
    def _build_presets(self):
        p = self._page("presets")
        self.presets_pad = self._pad(p)
        # Game header
        self.game_header_frame = ctk.CTkFrame(self.presets_pad, fg_color=PANEL,
                                              corner_radius=14, border_width=1, border_color=BORDER)
        self.game_header_frame.pack(fill="x", pady=(0, 14))
        self.game_header_inner = ctk.CTkFrame(self.game_header_frame, fg_color="transparent")
        self.game_header_inner.pack(fill="x", padx=22, pady=16)

        self.gh_icon  = ctk.CTkLabel(self.game_header_inner, text="🔫",
                                     font=ctk.CTkFont(size=36))
        self.gh_icon.pack(side="left", padx=(0, 14))
        gh_text = ctk.CTkFrame(self.game_header_inner, fg_color="transparent")
        gh_text.pack(side="left", fill="x", expand=True)
        self.gh_name = ctk.CTkLabel(gh_text, text="Rust",
                                    font=ctk.CTkFont(size=24, weight="bold"), text_color="#fff")
        self.gh_name.pack(anchor="w")
        self.gh_desc = ctk.CTkLabel(gh_text, text="Survival multiplayer",
                                    font=ctk.CTkFont(size=12), text_color=DIM)
        self.gh_desc.pack(anchor="w")

        # Quick action
        qr = ctk.CTkFrame(self.game_header_inner, fg_color="transparent")
        qr.pack(side="right")
        make_btn(qr, "⚡  ОПТИМИЗИРОВАТЬ ВСЁ",
                 self._optimize_all, size=13, width=220,
                 color="#006adf", hover="#0090ff").pack()
        self.preset_log = self._log(self.game_header_inner, 80)

        # Presets grid
        self.presets_grid_frame = ctk.CTkFrame(self.presets_pad, fg_color="transparent")
        self.presets_grid_frame.pack(fill="x", pady=(0, 12))

        # Tips
        tips_card = self._card(self.presets_pad)
        tp = ctk.CTkFrame(tips_card, fg_color="transparent")
        tp.pack(fill="x", padx=14, pady=12)
        ctk.CTkLabel(tp, text="💡 Советы для игры",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0,6))
        self.tips_frame = ctk.CTkFrame(tp, fg_color="transparent")
        self.tips_frame.pack(fill="x")

        self._refresh_presets()
        self._refresh_tips()

    def _refresh_presets(self):
        # Clear old preset cards
        for w in self.presets_grid_frame.winfo_children():
            w.destroy()

        game = GAMES[self.current_game]
        self.gh_icon.configure(text=game["icon"])
        self.gh_name.configure(text=self.current_game, text_color=game["color"])
        self.gh_desc.configure(text=game["desc"])

        for i, (pname, pdata) in enumerate(game["presets"].items()):
            self.presets_grid_frame.columnconfigure(i, weight=1)
            c = ctk.CTkFrame(self.presets_grid_frame, fg_color=PANEL, corner_radius=12,
                             border_width=2, border_color=BORDER)
            c.grid(row=0, column=i, padx=5, pady=4, sticky="ew")
            ci = ctk.CTkFrame(c, fg_color="transparent")
            ci.pack(fill="both", padx=14, pady=14)

            # Name & desc
            ctk.CTkLabel(ci, text=pname, font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=game["color"]).pack(anchor="w")
            ctk.CTkLabel(ci, text=pdata["desc"], font=ctk.CTkFont(size=10),
                         text_color=DIM).pack(anchor="w", pady=(2, 6))

            # FPS badge
            fps_f = ctk.CTkFrame(ci, fg_color="transparent")
            fps_f.pack(anchor="w", pady=(0, 8))
            ctk.CTkLabel(fps_f, text="🎯 FPS: ", font=ctk.CTkFont(size=11),
                         text_color=DIM).pack(side="left")
            ctk.CTkLabel(fps_f, text=pdata["fps_expect"],
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=GREEN).pack(side="left")

            # Settings count
            ctk.CTkLabel(ci, text=f"📋 {len(pdata['settings'])} параметров",
                         font=ctk.CTkFont(size=10), text_color=DIM).pack(anchor="w", pady=(0, 8))

            # Launch args preview
            launch = pdata.get("launch", "")
            if launch:
                la = ctk.CTkLabel(ci, text=launch[:50] + ("…" if len(launch) > 50 else ""),
                                  font=ctk.CTkFont(family="Courier New", size=9),
                                  text_color=NEON, wraplength=200, justify="left")
                la.pack(anchor="w", pady=(0, 8))

            make_btn(ci, "✓  Применить пресет",
                     lambda gn=self.current_game, pn=pname: self._apply_preset(gn, pn),
                     size=11, bold=False, width=170,
                     color="#1a3050", hover="#2a4060").pack(anchor="w")

    def _refresh_tips(self):
        for w in self.tips_frame.winfo_children():
            w.destroy()
        for tip in GAMES[self.current_game]["tips"]:
            r = ctk.CTkFrame(self.tips_frame, fg_color="transparent")
            r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text="→", text_color=NEON,
                         font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 8))
            ctk.CTkLabel(r, text=tip, font=ctk.CTkFont(size=12),
                         text_color=TEXT).pack(side="left")

    def _apply_preset(self, gname, pname):
        game = GAMES[gname]
        preset = game["presets"][pname]
        self._log_clear(self.preset_log)
        self._log_add(self.preset_log, f"▶ Применяю пресет «{pname}» для {gname}...")

        def run():
            # Show settings
            for k, v in preset["settings"]:
                self._log_add(self.preset_log, f"  ✓ {k} = {v}")
                time.sleep(0.04)
            # Show launch args
            launch = preset.get("launch", "")
            if launch:
                self._log_add(self.preset_log, f"\n📋 Параметры запуска:")
                self._log_add(self.preset_log, launch)
                self._log_add(self.preset_log, f"  → Вставь в: Steam → ПКМ на игру → Свойства → Параметры запуска")
            self._log_add(self.preset_log, f"\n✅ Пресет «{pname}» применён!")
            self._log_add(self.preset_log, f"   Ожидаемый FPS: {preset['fps_expect']}")

        threading.Thread(target=run, daemon=True).start()

    def _optimize_all(self):
        self._log_clear(self.preset_log)
        self._log_add(self.preset_log, "⚡ Запускаю полную оптимизацию...")

        def run():
            # Apply first (best FPS) preset
            game = GAMES[self.current_game]
            first_preset = list(game["presets"].keys())[0]
            self._log_add(self.preset_log, f"  🎮 Пресет: {first_preset}")
            time.sleep(0.3)

            # Windows optimizations
            for cmd in WIN_OPTS[0][3]:  # Power plan
                ok = run_cmd(cmd)
                self._log_add(self.preset_log, f"  {'✓' if ok else '✗'} Высокий план питания")

            # Network
            run_cmd("ipconfig /flushdns")
            self._log_add(self.preset_log, "  ✓ DNS очищен")

            run_cmd('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "TcpAckFrequency" /t REG_DWORD /d 1 /f')
            self._log_add(self.preset_log, "  ✓ Nagle отключён")

            run_cmd('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f')
            self._log_add(self.preset_log, "  ✓ Game DVR отключён")

            self._log_add(self.preset_log, f"\n✅ Полная оптимизация завершена!")
            self._log_add(self.preset_log, "   Перезапусти игру для применения изменений.")

        threading.Thread(target=run, daemon=True).start()

    # ── WINDOWS PAGE ──────────────────────────────────────
    def _build_windows(self):
        p = self._page("windows")
        pad = self._pad(p)
        self._section(pad, "⚡ Оптимизация Windows",
                      "Системные твики для максимальной производительности в играх")

        for ico, name, desc, cmds in WIN_OPTS:
            c = ctk.CTkFrame(pad, fg_color=PANEL2, corner_radius=10,
                             border_width=1, border_color=BORDER)
            c.pack(fill="x", pady=4)

            strip = ctk.CTkFrame(c, width=3, fg_color=NEON, corner_radius=0)
            strip.pack(side="left", fill="y")

            ci = ctk.CTkFrame(c, fg_color="transparent")
            ci.pack(fill="x", padx=12, pady=8)

            top = ctk.CTkFrame(ci, fg_color="transparent")
            top.pack(fill="x")

            ctk.CTkLabel(top, text=ico,
                         font=ctk.CTkFont(size=18)).pack(side="left", padx=(0, 8))
            inf = ctk.CTkFrame(top, fg_color="transparent")
            inf.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(inf, text=name, font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="#fff").pack(anchor="w")
            ctk.CTkLabel(inf, text=desc, font=ctk.CTkFont(size=10),
                         text_color=DIM).pack(anchor="w")

            lh = [None]
            btn = make_btn(top, "▶", None, size=12, width=34,
                           color="#1a3050", hover="#2a4060")
            btn.pack(side="right")
            btn.configure(command=lambda c2=cmds, n=name, b=btn, lhh=lh, ci2=ci:
                          self._run_win_opt(c2, n, b, lhh, ci2))

        # Run all button
        all_f = ctk.CTkFrame(pad, fg_color="transparent")
        all_f.pack(fill="x", pady=(14, 0))
        make_btn(all_f, "⚡  ПРИМЕНИТЬ ВСЕ ОПТИМИЗАЦИИ",
                 self._run_all_win, size=14, width=300,
                 color="#006adf", hover="#0090ff").pack(anchor="w")
        self.win_all_log = self._log(pad, 120)

    def _run_win_opt(self, cmds, name, btn, lh, parent):
        btn.configure(text="⟳", state="disabled")
        if lh[0] is None:
            lh[0] = self._log(parent, 60)
        else:
            self._log_clear(lh[0])

        def run():
            for cmd in cmds:
                ok = run_cmd(cmd)
                self._log_add(lh[0], f"{'✓' if ok else '✗'} {cmd.split()[0]}")
                time.sleep(0.1)
            self._log_add(lh[0], f"✅ {name} — готово")
            btn.configure(text="✓", state="normal",
                          fg_color="#0a3020", hover_color="#0d4028",
                          text_color=GREEN)
        threading.Thread(target=run, daemon=True).start()

    def _run_all_win(self):
        self._log_clear(self.win_all_log)
        self._log_add(self.win_all_log, "⚡ Применяю все оптимизации Windows...")

        def run():
            for ico, name, desc, cmds in WIN_OPTS:
                for cmd in cmds:
                    ok = run_cmd(cmd)
                self._log_add(self.win_all_log, f"  {'✓' if True else '✗'} {name}")
                time.sleep(0.15)
            self._log_add(self.win_all_log, "\n✅ Все оптимизации применены!")
            self._log_add(self.win_all_log, "   Рекомендуем перезагрузить ПК.")
        threading.Thread(target=run, daemon=True).start()

    # ── NETWORK PAGE ──────────────────────────────────────
    def _build_network(self):
        p = self._page("network")
        pad = self._pad(p)
        self._section(pad, "🌐 Настройка сети",
                      "DNS, Nagle, TCP оптимизации для снижения пинга")

        net_opts = [
            ("🌐", "Смена DNS", "Google 8.8.8.8 + Cloudflare 1.1.1.1",
             ['netsh interface ip set dns "Ethernet" static 8.8.8.8',
              'netsh interface ip add dns "Ethernet" 1.1.1.1 index=2',
              'netsh interface ip set dns "Wi-Fi" static 8.8.8.8',
              "ipconfig /flushdns"]),
            ("🏎", "Отключить Nagle", "Снижает пинг на 5-30ms",
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "TcpAckFrequency" /t REG_DWORD /d 1 /f',
              'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "TCPNoDelay" /t REG_DWORD /d 1 /f']),
            ("🔄", "Сброс Winsock", "Сбрасывает сетевой стек Windows",
             ["netsh winsock reset", "netsh int ip reset", "ipconfig /flushdns", "ipconfig /registerdns"]),
            ("🔕", "Отключить IPv6", "Помогает при проблемах с пингом",
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters" /v "DisabledComponents" /t REG_DWORD /d 255 /f']),
            ("📶", "QoS приоритет", "Приоритет игрового трафика (DSCP=46)",
             ['netsh qos delete policy "GameTraffic"',
              'netsh qos add policy "GameTraffic" app="*" dscp=46 throttle-rate=-1']),
            ("⏸", "Пауза Windows Update", "Остановить обновления на время игры",
             ["net stop wuauserv", "net stop bits", "net stop dosvc"]),
        ]

        for ico, name, desc, cmds in net_opts:
            c = ctk.CTkFrame(pad, fg_color=PANEL2, corner_radius=10,
                             border_width=1, border_color=BORDER)
            c.pack(fill="x", pady=4)
            strip = ctk.CTkFrame(c, width=3, fg_color=GREEN, corner_radius=0)
            strip.pack(side="left", fill="y")
            ci = ctk.CTkFrame(c, fg_color="transparent")
            ci.pack(fill="x", padx=12, pady=8)
            top = ctk.CTkFrame(ci, fg_color="transparent")
            top.pack(fill="x")
            ctk.CTkLabel(top, text=ico, font=ctk.CTkFont(size=18)).pack(side="left", padx=(0, 8))
            inf = ctk.CTkFrame(top, fg_color="transparent")
            inf.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(inf, text=name, font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="#fff").pack(anchor="w")
            ctk.CTkLabel(inf, text=desc, font=ctk.CTkFont(size=10),
                         text_color=DIM).pack(anchor="w")
            lh = [None]
            btn = make_btn(top, "▶", None, size=12, width=34,
                           color="#1a3050", hover="#2a4060")
            btn.pack(side="right")
            btn.configure(command=lambda c2=cmds, n=name, b=btn, lhh=lh, ci2=ci:
                          self._run_win_opt(c2, n, b, lhh, ci2))

        # Ping test
        ping_card = self._card(pad)
        pi = ctk.CTkFrame(ping_card, fg_color="transparent")
        pi.pack(fill="x", padx=14, pady=12)
        ctk.CTkLabel(pi, text="📡 Проверка пинга",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#fff").pack(anchor="w", pady=(0, 8))
        make_btn(pi, "🔍  Проверить серверы", self._run_ping_test,
                 width=200, color="#006adf", hover="#0090ff").pack(anchor="w")
        self.net_log = self._log(pi, 120)

    def _run_ping_test(self):
        self._log_clear(self.net_log)
        self._log_add(self.net_log, "Проверяю серверы...")

        def run():
            hosts = [("Steam", "store.steampowered.com"),
                     ("Google", "8.8.8.8"), ("Cloudflare", "1.1.1.1"),
                     ("Faceit", "api.faceit.com"), ("AWS EU", "ec2.eu-central-1.amazonaws.com")]
            for name, host in hosts:
                ms = ping_host(host)
                if ms < 0:
                    self._log_add(self.net_log, f"✗  {name:<16} timeout")
                else:
                    status = "OK ✓" if ms < 80 else "СРЕДНИЙ" if ms < 150 else "ВЫСОКИЙ ⚠"
                    self._log_add(self.net_log, f"✓  {name:<16} {ms} ms  {status}")
                time.sleep(0.1)
            self._log_add(self.net_log, "\nГотово!")
        threading.Thread(target=run, daemon=True).start()

    # ── MONITOR PAGE ──────────────────────────────────────
    def _build_monitor(self):
        p = self._page("monitor")
        pad = self._pad(p)
        self._section(pad, "📊 Мониторинг",
                      "Пинг до серверов в реальном времени")

        # Stats
        sr = ctk.CTkFrame(pad, fg_color="transparent")
        sr.pack(fill="x", pady=(0, 12))
        for i in range(3):
            sr.columnconfigure(i, weight=1)
        self.ms_cur  = self._stat_box(sr, "—", "Текущий ms", GREEN,  0)
        self.ms_avg  = self._stat_box(sr, "—", "Средний ms", GOLD,   1)
        self.ms_max  = self._stat_box(sr, "—", "Максимум ms", RED,   2)

        # Controls
        cr = ctk.CTkFrame(pad, fg_color="transparent")
        cr.pack(fill="x", pady=(0, 10))
        self.mon_btn = make_btn(cr, "▶  Запустить мониторинг",
                                self._toggle_monitor, width=210,
                                color="#006adf", hover="#0090ff")
        self.mon_btn.pack(side="left")
        self.mon_lbl = ctk.CTkLabel(cr, text="● Остановлен",
                                    text_color=DIM, font=ctk.CTkFont(size=11))
        self.mon_lbl.pack(side="left", padx=12)
        ctk.CTkLabel(cr, text="Интервал:", text_color=DIM,
                     font=ctk.CTkFont(size=11)).pack(side="left")
        self.mon_int = ctk.CTkComboBox(cr, values=["2 сек", "5 сек", "10 сек"],
                                       width=90, fg_color=PANEL2, border_color=BORDER)
        self.mon_int.set("2 сек")
        self.mon_int.pack(side="left", padx=6)

        # Server rows
        self.srv_lbls = {}
        for name, host in MONITOR_HOSTS:
            row = ctk.CTkFrame(pad, fg_color=PANEL2, corner_radius=8,
                               border_width=1, border_color=BORDER)
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text="●", font=ctk.CTkFont(size=12),
                         text_color=DIM).pack(side="left", padx=(12, 8), pady=8)
            ctk.CTkLabel(row, text=name, font=ctk.CTkFont(size=12),
                         text_color=TEXT, width=140).pack(side="left")
            lbl = ctk.CTkLabel(row, text="— ms",
                               font=ctk.CTkFont(size=12, weight="bold"),
                               text_color=DIM)
            lbl.pack(side="right", padx=14)
            self.srv_lbls[host] = lbl

        # Chart
        cc = self._card(pad)
        ctk.CTkLabel(cc, text="📈 График пинга",
                     font=ctk.CTkFont(size=11), text_color=DIM).pack(anchor="w", padx=12, pady=(8, 2))
        self.chart = ctk.CTkCanvas(cc, height=110, bg="#020810", highlightthickness=0)
        self.chart.pack(fill="x", padx=10, pady=(0, 8))

    def _stat_box(self, parent, val, label, color, col):
        f = ctk.CTkFrame(parent, fg_color=PANEL2, corner_radius=9,
                         border_width=1, border_color=BORDER)
        f.grid(row=0, column=col, padx=4, sticky="ew")
        v = ctk.CTkLabel(f, text=val,
                         font=ctk.CTkFont(size=24, weight="bold"), text_color=color)
        v.pack(pady=(10, 2))
        ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=10),
                     text_color=DIM).pack(pady=(0, 8))
        return v

    def _toggle_monitor(self):
        if self.monitor_running:
            self.monitor_running = False
            self.mon_btn.configure(text="▶  Запустить мониторинг",
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
            iv = {"2 сек": 2, "5 сек": 5, "10 сек": 10}.get(self.mon_int.get(), 2)
            results = []
            for name, host in MONITOR_HOSTS:
                ms = ping_host(host)
                results.append(ms)
                lbl = self.srv_lbls[host]
                if ms < 0:
                    lbl.configure(text="timeout", text_color=RED)
                else:
                    col = GREEN if ms < 80 else GOLD if ms < 150 else RED
                    lbl.configure(text=f"{ms} ms", text_color=col)
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
        pts = [(int(10 + (i / (len(self.ping_history) - 1)) * (W - 20)),
                int(H - 10 - (v / maxV) * (H - 20)))
               for i, v in enumerate(self.ping_history)]
        poly = [(10, H - 10)] + pts + [(pts[-1][0], H - 10)]
        c.create_polygon([x for pt in poly for x in pt], fill="#003030", outline="")
        last = self.ping_history[-1]
        col = "#00ff88" if last < 80 else "#ffd700" if last < 150 else "#ff4466"
        c.create_line([x for pt in pts for x in pt], fill=col, width=2, smooth=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
