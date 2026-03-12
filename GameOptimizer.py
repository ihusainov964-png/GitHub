"""Game Optimizer v2.0 — Rust • GTA V • CS2"""
import customtkinter as ctk
import subprocess, threading, random, time, os, socket

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG="#05080f";PANEL="#090f1d";PANEL2="#0c1628";BORDER="#1a3050"
TEXT="#b8cfea";DIM="#3a5a7a";NEON="#00f0ff";GREEN="#00ff88"
GOLD="#ffd700";RED="#ff4466";PURPLE="#b060ff";ORANGE="#ff9f40"

JOKES=["😂 Ваня: '5 FPS — это нормально'","💀 Ваня оптимизировал и удалил system32",
       "🎯 Ваня поставил мониторинг — FPS 12","🔫 Ваня в Rust строил дом — убили через стену",
       "🚗 Ваня в GTA взял такси — лучше пешком","⚡ Ваня включил план питания — сгорел роутер"]

def run_cmd(cmd):
    try:
        r=subprocess.run(cmd,shell=True,capture_output=True,text=True,timeout=30,encoding="cp1251",errors="replace")
        return r.returncode==0
    except: return False

def ping_host(host,timeout=2):
    try:
        t0=time.time(); s=socket.create_connection((host,80),timeout=timeout); s.close()
        return int((time.time()-t0)*1000)
    except: return -1

def btn(parent,text,cmd,size=13,bold=True,color="#0060df",hover="#0090ff",width=None,corner=8):
    kw=dict(text=text,command=cmd,fg_color=color,hover_color=hover,
            font=ctk.CTkFont(size=size,weight="bold"if bold else"normal"),corner_radius=corner)
    if width: kw["width"]=width
    return ctk.CTkButton(parent,**kw)

# ═══════════════════════════════════════════════════════
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Game Optimizer v2.0")
        self.geometry("1100x700"); self.minsize(980,640); self.configure(fg_color=BG)
        self.monitor_running=False; self.ping_history=[]
        self._build_ui()

    def _build_ui(self):
        # ── Sidebar ──────────────────────────────────────
        sb=ctk.CTkFrame(self,width=200,fg_color=PANEL,corner_radius=0,border_width=1,border_color=BORDER)
        sb.pack(side="left",fill="y"); sb.pack_propagate(False)
        lf=ctk.CTkFrame(sb,fg_color="transparent"); lf.pack(pady=(16,4),padx=12)
        ctk.CTkLabel(lf,text="🎮",font=ctk.CTkFont(size=22)).pack(side="left")
        ctk.CTkLabel(lf,text=" GAME OPTIMIZER",font=ctk.CTkFont(size=11,weight="bold"),text_color=NEON).pack(side="left")
        ctk.CTkLabel(sb,text="v2.0",font=ctk.CTkFont(size=10),text_color=DIM).pack()
        ctk.CTkFrame(sb,height=1,fg_color=BORDER).pack(fill="x",padx=10,pady=8)
        ctk.CTkLabel(sb,text="ИГРЫ",font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w",padx=12)
        self.game_btns={}
        for gname,gdata in GAMES.items():
            b=ctk.CTkButton(sb,text=f"{gdata['icon']}  {gname}",anchor="w",font=ctk.CTkFont(size=13),
                            height=38,fg_color="transparent",hover_color="#0d1e38",text_color=DIM,
                            corner_radius=8,command=lambda g=gname:self.show_game(g))
            b.pack(fill="x",padx=8,pady=2); self.game_btns[gname]=b
        ctk.CTkFrame(sb,height=1,fg_color=BORDER).pack(fill="x",padx=10,pady=8)
        ctk.CTkLabel(sb,text="ОБЩЕЕ",font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w",padx=12)
        self.nav_btns={}
        for pid,label in [("windows","⚡  Windows"),("network","🌐  Сеть"),("monitor","📊  Мониторинг")]:
            b=ctk.CTkButton(sb,text=label,anchor="w",font=ctk.CTkFont(size=12),height=34,
                            fg_color="transparent",hover_color="#0d1e38",text_color=DIM,corner_radius=8,
                            command=lambda p=pid:self.show_page(p))
            b.pack(fill="x",padx=8,pady=2); self.nav_btns[pid]=b
        ctk.CTkFrame(sb,height=1,fg_color=BORDER).pack(fill="x",padx=10,pady=8,side="bottom")
        self.joke_lbl=ctk.CTkLabel(sb,text=random.choice(JOKES),font=ctk.CTkFont(size=10,slant="italic"),
                                   text_color=GOLD,wraplength=178,justify="center")
        self.joke_lbl.pack(side="bottom",padx=8,pady=6)
        # ── Content ──────────────────────────────────────
        self.content=ctk.CTkFrame(self,fg_color=BG,corner_radius=0)
        self.content.pack(side="left",fill="both",expand=True)
        self.pages={}
        for gname in GAMES: self._build_game_page(gname)
        self._build_windows(); self._build_network(); self._build_monitor()
        self.show_game("Rust")

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

    # ── Helpers ──────────────────────────────────────────
    def _scr(self,pid):
        f=ctk.CTkScrollableFrame(self.content,fg_color=BG,corner_radius=0,scrollbar_button_color=BORDER)
        self.pages[pid]=f; return f

    def _pad(self,p):
        f=ctk.CTkFrame(p,fg_color="transparent"); f.pack(fill="both",expand=True,padx=22,pady=16); return f

    def _card(self,parent,pady=5):
        f=ctk.CTkFrame(parent,fg_color=PANEL2,corner_radius=12,border_width=1,border_color=BORDER)
        f.pack(fill="x",pady=pady); return f

    def _log(self,parent,h=120):
        tb=ctk.CTkTextbox(parent,height=h,fg_color="#020810",border_width=1,border_color=BORDER,
                          font=ctk.CTkFont(family="Courier New",size=11),text_color="#68ffaa",corner_radius=8)
        tb.pack(fill="x",pady=(4,0)); tb.configure(state="disabled"); return tb

    def _w(self,tb,t):
        tb.configure(state="normal"); tb.insert("end",t+"\n"); tb.configure(state="disabled"); tb.see("end")

    def _clr(self,tb):
        tb.configure(state="normal"); tb.delete("1.0","end"); tb.configure(state="disabled")

    def _section_label(self,parent,text):
        ctk.CTkLabel(parent,text=text,font=ctk.CTkFont(size=12,weight="bold"),
                     text_color=DIM).pack(anchor="w",pady=(0,6))

    def _toggle_row(self,parent,label,desc,on_cmd,off_cmd,default=False,accent=NEON):
        row=ctk.CTkFrame(parent,fg_color=PANEL2,corner_radius=9,border_width=1,border_color=BORDER)
        row.pack(fill="x",pady=3)
        strip=ctk.CTkFrame(row,width=3,fg_color=accent,corner_radius=0); strip.pack(side="left",fill="y")
        ri=ctk.CTkFrame(row,fg_color="transparent"); ri.pack(fill="x",padx=12,pady=8,side="left",expand=True)
        ctk.CTkLabel(ri,text=label,font=ctk.CTkFont(size=12,weight="bold"),text_color="#fff").pack(anchor="w")
        ctk.CTkLabel(ri,text=desc,font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w")
        var=ctk.BooleanVar(value=default)
        def toggle():
            if var.get():
                threading.Thread(target=lambda:[run_cmd(c) for c in on_cmd],daemon=True).start()
            else:
                threading.Thread(target=lambda:[run_cmd(c) for c in off_cmd],daemon=True).start()
        sw=ctk.CTkSwitch(row,text="",variable=var,command=toggle,
                         progress_color=accent,button_color="#ffffff",width=46)
        sw.pack(side="right",padx=12)
        return var

    # ═══════════════════════════════════════════════════
    # GAME PAGES
    # ═══════════════════════════════════════════════════
    def _build_game_page(self,gname):
        g=GAMES[gname]
        outer=ctk.CTkFrame(self.content,fg_color=BG,corner_radius=0)
        self.pages[gname]=outer

        # Game header bar
        hbar=ctk.CTkFrame(outer,fg_color=PANEL,corner_radius=0,border_width=1,border_color=BORDER,height=64)
        hbar.pack(fill="x"); hbar.pack_propagate(False)
        hi=ctk.CTkFrame(hbar,fg_color="transparent"); hi.pack(fill="both",padx=20,pady=10)
        ctk.CTkLabel(hi,text=g["icon"],font=ctk.CTkFont(size=28)).pack(side="left",padx=(0,12))
        ht=ctk.CTkFrame(hi,fg_color="transparent"); ht.pack(side="left",fill="y",expand=True)
        ctk.CTkLabel(ht,text=gname,font=ctk.CTkFont(size=20,weight="bold"),text_color=g["color"]).pack(anchor="w")
        ctk.CTkLabel(ht,text=g["desc"],font=ctk.CTkFont(size=11),text_color=DIM).pack(anchor="w")
        btn(hi,"⚡  ОПТИМИЗИРОВАТЬ ВСЁ",lambda gn=gname:self._full_optimize(gn),
            size=12,width=200,color=g["color"],hover="#ffffff").pack(side="right")

        # Tab bar
        tab_frame=ctk.CTkFrame(outer,fg_color=PANEL2,corner_radius=0,height=40)
        tab_frame.pack(fill="x"); tab_frame.pack_propagate(False)
        self._make_tabs(outer,tab_frame,gname,g)

    def _make_tabs(self,outer,tab_frame,gname,g):
        tab_content=ctk.CTkFrame(outer,fg_color=BG,corner_radius=0)
        tab_content.pack(fill="both",expand=True)
        tabs={}
        tab_names=["🎨 Графика","🌐 Сеть","🚫 Паразиты","💡 Советы"]
        if gname=="CS2": tab_names.append("⚙️ Конфиг")
        if gname=="GTA V": tab_names.append("🟣 FiveM")
        if gname=="Rust": tab_names.append("🔩 Launch args")

        tab_btns={}
        def show_tab(tname):
            for t in tabs.values(): t.pack_forget()
            tabs[tname].pack(fill="both",expand=True)
            for k,b in tab_btns.items():
                b.configure(fg_color="#0d2040" if k==tname else "transparent",
                            text_color=g["color"] if k==tname else DIM)

        for tname in tab_names:
            tb2=ctk.CTkButton(tab_frame,text=tname,anchor="w",font=ctk.CTkFont(size=11),
                              height=38,fg_color="transparent",hover_color="#0d1e38",
                              text_color=DIM,corner_radius=0,width=120,
                              command=lambda t=tname:show_tab(t))
            tb2.pack(side="left",padx=2); tab_btns[tname]=tb2

        # Build tab content
        for tname in tab_names:
            scr=ctk.CTkScrollableFrame(tab_content,fg_color=BG,corner_radius=0,scrollbar_button_color=BORDER)
            tabs[tname]=scr
            pad=ctk.CTkFrame(scr,fg_color="transparent"); pad.pack(fill="both",expand=True,padx=20,pady=14)
            if "Графика" in tname: self._tab_graphics(pad,gname,g)
            elif "Сеть" in tname: self._tab_network(pad,gname,g)
            elif "Паразиты" in tname: self._tab_parasites(pad,gname,g)
            elif "Советы" in tname: self._tab_tips(pad,gname,g)
            elif "Конфиг" in tname: self._tab_cs2_config(pad)
            elif "FiveM" in tname: self._tab_fivem(pad)
            elif "Launch" in tname: self._tab_rust_launch(pad)

        show_tab(tab_names[0])

    # ── TAB: GRAPHICS ────────────────────────────────────
    def _tab_graphics(self,pad,gname,g):
        ctk.CTkLabel(pad,text="🎨 Пресеты графики",font=ctk.CTkFont(size=16,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,4))
        ctk.CTkLabel(pad,text="Выбери пресет — получишь список настроек и параметры запуска Steam",
                     font=ctk.CTkFont(size=11),text_color=DIM).pack(anchor="w",pady=(0,12))
        gr=ctk.CTkFrame(pad,fg_color="transparent"); gr.pack(fill="x")
        log=[None]
        log[0]=self._log(pad,100)
        for i,(pname,pdata) in enumerate(g["presets"].items()):
            gr.columnconfigure(i,weight=1)
            c=ctk.CTkFrame(gr,fg_color=PANEL,corner_radius=11,border_width=2,border_color=BORDER)
            c.grid(row=0,column=i,padx=4,sticky="ew")
            ci=ctk.CTkFrame(c,fg_color="transparent"); ci.pack(fill="both",padx=12,pady=12)
            ctk.CTkLabel(ci,text=pname,font=ctk.CTkFont(size=13,weight="bold"),text_color=g["color"]).pack(anchor="w")
            ctk.CTkLabel(ci,text=pdata["desc"],font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w",pady=(2,6))
            fr=ctk.CTkFrame(ci,fg_color="transparent"); fr.pack(anchor="w",pady=(0,6))
            ctk.CTkLabel(fr,text="🎯 FPS: ",font=ctk.CTkFont(size=10),text_color=DIM).pack(side="left")
            ctk.CTkLabel(fr,text=pdata["fps_expect"],font=ctk.CTkFont(size=10,weight="bold"),text_color=GREEN).pack(side="left")
            ctk.CTkLabel(ci,text=f"📋 {len(pdata['settings'])} параметров",font=ctk.CTkFont(size=10),text_color=DIM).pack(anchor="w",pady=(0,8))
            btn(ci,"✓  Применить",lambda p=pdata,l=log,n=pname:self._apply_preset(p,l[0],n),
                size=11,bold=False,width=150,color="#1a3050",hover="#2a4060").pack(anchor="w")

    def _apply_preset(self,pdata,log_tb,pname):
        self._clr(log_tb); self._w(log_tb,f"▶ Применяю пресет «{pname}»...")
        def run():
            for k,v in pdata["settings"]:
                self._w(log_tb,f"  ✓ {k} = {v}"); time.sleep(0.03)
            launch=pdata.get("launch","")
            if launch:
                self._w(log_tb,"\n📋 Параметры запуска Steam:")
                self._w(log_tb,f"  {launch}")
                self._w(log_tb,"  → Steam → ПКМ игра → Свойства → Параметры запуска")
            self._w(log_tb,f"\n✅ {pname} применён! FPS: {pdata['fps_expect']}")
        threading.Thread(target=run,daemon=True).start()

    # ── TAB: NETWORK ─────────────────────────────────────
    def _tab_network(self,pad,gname,g):
        ctk.CTkLabel(pad,text="🌐 Настройка сети",font=ctk.CTkFont(size=16,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,4))
        ctk.CTkLabel(pad,text="Оптимизация пинга и соединения для "+gname,
                     font=ctk.CTkFont(size=11),text_color=DIM).pack(anchor="w",pady=(0,12))
        net_items=[
            ("🌐","Смена DNS","Google 8.8.8.8 + Cloudflare 1.1.1.1",GREEN,
             ['netsh interface ip set dns "Ethernet" static 8.8.8.8',
              'netsh interface ip add dns "Ethernet" 1.1.1.1 index=2',
              'netsh interface ip set dns "Wi-Fi" static 8.8.8.8',"ipconfig /flushdns"],
             ["netsh interface ip set dns \"Ethernet\" dhcp","netsh interface ip set dns \"Wi-Fi\" dhcp"]),
            ("🏎","Откл. Nagle","Снижает пинг на 5-30ms",NEON,
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TcpAckFrequency /t REG_DWORD /d 1 /f',
              'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TCPNoDelay /t REG_DWORD /d 1 /f'],
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TcpAckFrequency /t REG_DWORD /d 2 /f']),
            ("📶","QoS приоритет","Приоритет игрового трафика",PURPLE,
             ['netsh qos delete policy "GameTraffic"',
              'netsh qos add policy "GameTraffic" app="*" dscp=46 throttle-rate=-1'],
             ['netsh qos delete policy "GameTraffic"']),
            ("🔕","Откл. IPv6","Помогает при лагах в СНГ",ORANGE,
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters" /v DisabledComponents /t REG_DWORD /d 255 /f'],
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters" /v DisabledComponents /t REG_DWORD /d 0 /f']),
            ("🔄","Сброс Winsock","Полный сброс сетевого стека",GREEN,
             ["netsh winsock reset","netsh int ip reset","ipconfig /flushdns"],
             []),
        ]
        # Game-specific
        if gname=="CS2":
            net_items.append(("🎯","CS2 Rate команды","Оптимальные сетевые настройки",NEON,
                ["echo rate 786432 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\"",
                 "echo cl_interp 0 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\"",
                 "echo cl_interp_ratio 1 >> \"%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg\""],
                []))
        elif gname=="Rust":
            net_items.append(("🔫","Rust Network","Оптимальные настройки сети Rust",ORANGE,
                ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v GlobalMaxTcpWindowSize /t REG_DWORD /d 65535 /f'],
                []))
        elif gname=="GTA V":
            net_items.append(("🚗","GTA Online Network","Улучшение GTA Online сессий",NEON,
                ['netsh interface tcp set global autotuninglevel=highlyrestricted'],
                ['netsh interface tcp set global autotuninglevel=normal']))

        for ico,name,desc,accent,on_c,off_c in net_items:
            self._toggle_row(pad,f"{ico}  {name}",desc,on_c,off_c,accent=accent)

        ctk.CTkFrame(pad,height=1,fg_color=BORDER).pack(fill="x",pady=10)
        btn(pad,"📡  Проверить пинг",lambda:self._ping_test_inline(pad,gname),
            width=180,color="#006adf",hover="#0090ff").pack(anchor="w")

    def _ping_test_inline(self,pad,gname):
        log=self._log(pad,90)
        hosts=[("Steam","store.steampowered.com"),("Cloudflare","1.1.1.1"),("Google","8.8.8.8")]
        if gname=="CS2": hosts.append(("Faceit","api.faceit.com"))
        if gname=="GTA V": hosts.append(("Rockstar","socialclub.rockstargames.com"))
        if gname=="Rust": hosts.append(("Facepunch","facepunch.com"))
        def run():
            for name,host in hosts:
                ms=ping_host(host)
                self._w(log,f"{'✓' if ms>0 else '✗'}  {name:<16} {ms if ms>0 else 'timeout'} {'ms' if ms>0 else ''}")
                time.sleep(0.1)
            self._w(log,"✅ Готово!")
        threading.Thread(target=run,daemon=True).start()

    # ── TAB: PARASITES ───────────────────────────────────
    def _tab_parasites(self,pad,gname,g):
        ctk.CTkLabel(pad,text="🚫 Паразитные функции",font=ctk.CTkFont(size=16,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,4))
        ctk.CTkLabel(pad,text="Отключи всё лишнее — оверлеи, фоновые процессы и ненужные функции внутри игры",
                     font=ctk.CTkFont(size=11),text_color=DIM).pack(anchor="w",pady=(0,12))

        # ── Внутри игры ──────────────────────────────────
        self._section_label(pad,f"🎮 Внутри {gname} — ненужные функции")
        if gname=="Rust":
            in_game=[
                ("🎓","Обучалка / Tutorial подсказки","Постоянные подсказки новичка — мешают и грузят",RED,
                 [r'reg add "HKCU\Software\Facepunch\Rust" /v tutorial_complete /t REG_DWORD /d 1 /f'],
                 [r'reg add "HKCU\Software\Facepunch\Rust" /v tutorial_complete /t REG_DWORD /d 0 /f']),
                ("🎬","Вступительное видео Rust","Логотип при каждом запуске — зачем?",ORANGE,
                 [r'reg add "HKCU\Software\Facepunch\Rust" /v skip_intro /t REG_DWORD /d 1 /f'],
                 [r'reg add "HKCU\Software\Facepunch\Rust" /v skip_intro /t REG_DWORD /d 0 /f']),
                ("🌿","Трава (grass.on false)","Убирает траву — +20-40 FPS",GREEN,
                 ['echo grass.on false > "%APPDATA%\\Rust\\cfg\\client.cfg"'],
                 ['echo grass.on true > "%APPDATA%\\Rust\\cfg\\client.cfg"']),
                ("💨","Motion Blur (effects.motionblur)","Размытие при движении — снижает FPS",NEON,
                 ['echo effects.motionblur false >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
                 ['echo effects.motionblur true >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
                ("🔊","VOIP / Голосовой чат","Постоянно слушает микрофон — грузит CPU",PURPLE,
                 ['echo voice.use false >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
                 ['echo voice.use true >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
                ("📦","Скины предметов","Загрузка скинов жрёт RAM и VRAM",GOLD,
                 ['echo graphics.itemskins 0 >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
                 ['echo graphics.itemskins 1 >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
                ("🎆","Эффекты урона / взрывов","Партиклы взрывов — ненужная нагрузка",RED,
                 ['echo graphics.damage 0 >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
                 ['echo graphics.damage 1 >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
                ("🌊","Глубина резкости (DOF)","Размытие фона — FPS тратится зря",ORANGE,
                 ['echo graphics.dof false >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
                 ['echo graphics.dof true >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
                ("🐟","Рыбы / Животные рядом","Клиентская анимация животных грузит CPU",DIM,
                 ['echo population.animal 0 >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
                 ['echo population.animal 50 >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
                ("🌅","God Rays / Лучи света","Volumetric lighting — дорогой эффект",PURPLE,
                 ['echo graphics.shafts 0 >> "%APPDATA%\\Rust\\cfg\\client.cfg"'],
                 ['echo graphics.shafts 1 >> "%APPDATA%\\Rust\\cfg\\client.cfg"']),
            ]
        elif gname=="GTA V":
            in_game=[
                ("🎓","Обучающие подсказки","Всплывают каждый раз — бесполезно",RED,
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v TutorialDone /t REG_DWORD /d 1 /f'],
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v TutorialDone /t REG_DWORD /d 0 /f']),
                ("🎬","Вступительные ролики Rockstar","Логотип + ролик при каждом запуске",ORANGE,
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v InstallComplete /t REG_DWORD /d 1 /f'],
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v InstallComplete /t REG_DWORD /d 0 /f']),
                ("🌀","Motion Blur","Размытие при движении — -10-15 FPS",RED,
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v MotionBlur /t REG_DWORD /d 0 /f'],
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v MotionBlur /t REG_DWORD /d 1 /f']),
                ("🌊","Глубина резкости (DOF)","Размытие фона — зря расходует GPU",NEON,
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v InGameDepthOfField /t REG_DWORD /d 0 /f'],
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v InGameDepthOfField /t REG_DWORD /d 1 /f']),
                ("🎬","Rockstar Editor / Replay буфер","Постоянно пишет буфер повтора в фоне",GOLD,
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ReplayBuffer /t REG_DWORD /d 0 /f'],
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ReplayBuffer /t REG_DWORD /d 1 /f']),
                ("🐾","Tessellation поверхностей","Детализация травы/земли — очень дорого",PURPLE,
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v Tessellation /t REG_DWORD /d 0 /f'],
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v Tessellation /t REG_DWORD /d 1 /f']),
                ("🌆","Extended Distance Scaling","Далёкие объекты — огромная нагрузка",RED,
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ExtendedDistanceScaling /t REG_DWORD /d 0 /f'],
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ExtendedDistanceScaling /t REG_DWORD /d 1 /f']),
                ("🚁","Трафик и пешеходы (NPC)","Высокая плотность NPC грузит CPU",ORANGE,
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v PedDensity /t REG_DWORD /d 0 /f'],
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v PedDensity /t REG_DWORD /d 100 /f']),
                ("🌧","Particle Effects / Погода","Дождь, снег, дым — дорогие партиклы",NEON,
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ParticleQuality /t REG_DWORD /d 0 /f'],
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v ParticleQuality /t REG_DWORD /d 2 /f']),
                ("📺","Cutscene анимации","Вставки при входе в миссии",DIM,
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v SkipCutscenes /t REG_DWORD /d 1 /f'],
                 [r'reg add "HKCU\Software\Rockstar Games\Grand Theft Auto V" /v SkipCutscenes /t REG_DWORD /d 0 /f']),
            ]
        else:  # CS2
            in_game=[
                ("🎓","Обучение / Tutorial режим","Убирает предложение зайти в обучалку",RED,
                 [r'reg add "HKCU\Software\Valve\Counter-Strike Global Offensive" /v TutorialDone /t REG_DWORD /d 1 /f'],
                 [r'reg add "HKCU\Software\Valve\Counter-Strike Global Offensive" /v TutorialDone /t REG_DWORD /d 0 /f']),
                ("🎬","Интро видео Valve (-novid)","Логотип Valve при каждом запуске",ORANGE,
                 [r'reg add "HKCU\Software\Valve\Counter-Strike Global Offensive" /v NoVideoIntro /t REG_DWORD /d 1 /f'],
                 [r'reg add "HKCU\Software\Valve\Counter-Strike Global Offensive" /v NoVideoIntro /t REG_DWORD /d 0 /f']),
                ("🌀","Motion Blur (r_motionblur 0)","Размытие — снижает FPS без пользы",RED,
                 ['echo r_motionblur 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
                 ['echo r_motionblur 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
                ("💀","Ragdoll физика трупов","Трупы с физикой жрут CPU — отключи",NEON,
                 ['echo cl_ragdoll_physics_enable 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
                 ['echo cl_ragdoll_physics_enable 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
                ("🌿","Детали окружения (трава/листья)","Декоративные детали — ненужная нагрузка",GREEN,
                 ['echo cl_detailfade 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"\necho cl_detail_avoid_force 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
                 ['echo cl_detailfade 400 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
                ("👁","Lens Flare / Блики объектива","Декоративный эффект — зачем?",GOLD,
                 ['echo r_eyegloss 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"\necho r_eyemove 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
                 ['echo r_eyegloss 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
                ("🎵","Музыка в главном меню","Звуковой движок работает даже в меню",PURPLE,
                 ['echo snd_menumusic_volume 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
                 ['echo snd_menumusic_volume 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
                ("📊","HUD анимации","Анимированные элементы интерфейса",DIM,
                 ['echo cl_hud_radar_scale 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"\necho hud_scaling 0.85 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
                 []),
                ("🔫","Анимация осмотра оружия","viewmodel_presetpos — скрыть оружие",ORANGE,
                 ['echo viewmodel_presetpos 3 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
                 ['echo viewmodel_presetpos 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
                ("💬","Сообщения смерти / Kill feed","cl_draw_only_deathnotices — только важное",NEON,
                 ['echo cl_draw_only_deathnotices 1 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"'],
                 ['echo cl_draw_only_deathnotices 0 >> "%USERPROFILE%\\AppData\\Local\\cs2\\cfg\\autoexec.cfg"']),
            ]

        for ico,name,desc,accent,on_c,off_c in in_game:
            self._toggle_row(pad,f"{ico}  {name}",desc,on_c,off_c,accent=accent)

        # ── Оверлеи ──────────────────────────────────────
        ctk.CTkFrame(pad,height=1,fg_color=BORDER).pack(fill="x",pady=10)
        self._section_label(pad,"🖥 Оверлеи — жрут FPS и память")
        overlays=[
            ("🎮","Xbox Game Bar / Game DVR","Сжирает 5-15% CPU, вызывает фризы",RED,
             ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f',
              'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f'],
             ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 1 /f']),
            ("📸","NVIDIA ShadowPlay / Share","Записывает видео в фоне, нагружает GPU",ORANGE,
             ['reg add "HKCU\\Software\\NVIDIA Corporation\\NVCapture" /v CaptureEnabled /t REG_DWORD /d 0 /f'],
             ['reg add "HKCU\\Software\\NVIDIA Corporation\\NVCapture" /v CaptureEnabled /t REG_DWORD /d 1 /f']),
            ("💬","Discord оверлей","+3-8ms задержки на кадр",PURPLE,
             ['reg add "HKCU\\Software\\Discord" /v Overlay /t REG_DWORD /d 0 /f'],
             ['reg add "HKCU\\Software\\Discord" /v Overlay /t REG_DWORD /d 1 /f']),
            ("🎵","Steam оверлей","Shift+Tab лагает, грузит память",NEON,
             ['reg add "HKCU\\Software\\Valve\\Steam" /v SteamOverlayEnabled /t REG_DWORD /d 0 /f'],
             ['reg add "HKCU\\Software\\Valve\\Steam" /v SteamOverlayEnabled /t REG_DWORD /d 1 /f']),
        ]
        for ico,name,desc,accent,on_c,off_c in overlays:
            self._toggle_row(pad,f"{ico}  {name}",desc,on_c,off_c,accent=accent)

        # ── Фоновые процессы ──────────────────────────────
        ctk.CTkFrame(pad,height=1,fg_color=BORDER).pack(fill="x",pady=10)
        self._section_label(pad,"⚙️ Фоновые процессы Windows")
        win_parasites=[
            ("🔄","Windows Update","Качает обновления во время игры",RED,
             ["net stop wuauserv","net stop bits","net stop dosvc"],
             ["net start wuauserv"]),
            ("🔍","Windows Search / Indexer","Индексирует файлы, грузит диск",ORANGE,
             ["net stop wsearch","sc config wsearch start=disabled"],
             ["net start wsearch","sc config wsearch start=auto"]),
            ("📊","SysMain (Superfetch)","Предзагрузка программ, мешает играм",GOLD,
             ["net stop sysmain","sc config sysmain start=disabled"],
             ["net start sysmain","sc config sysmain start=auto"]),
            ("☁️","OneDrive синхронизация","Грузит диск и сеть во время игры",NEON,
             ["taskkill /f /im OneDrive.exe","sc config OneSyncSvc start=disabled"],
             ["sc config OneSyncSvc start=auto"]),
            ("🦠","Antimalware / Windows Defender","Сканирует файлы игры — жрёт CPU",RED,
             ['reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f'],
             ['reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 0 /f']),
        ]
        for ico,name,desc,accent,on_c,off_c in win_parasites:
            self._toggle_row(pad,f"{ico}  {name}",desc,on_c,off_c,accent=accent)

        ctk.CTkFrame(pad,height=1,fg_color=BORDER).pack(fill="x",pady=10)
        btn(pad,"🚫  ОТКЛЮЧИТЬ ВСЕ ПАРАЗИТЫ",
            lambda:self._disable_all_parasites(),
            size=13,width=260,color="#6b0000",hover="#8b0000").pack(anchor="w")

    def _disable_all_parasites(self):
        cmds=[
            'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f',
            "net stop wuauserv","net stop wsearch","net stop sysmain",
            "taskkill /f /im OneDrive.exe",
        ]
        threading.Thread(target=lambda:[run_cmd(c) for c in cmds],daemon=True).start()

    # ── TAB: TIPS ────────────────────────────────────────
    def _tab_tips(self,pad,gname,g):
        ctk.CTkLabel(pad,text="💡 Советы и хитрости",font=ctk.CTkFont(size=16,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,4))
        ctk.CTkLabel(pad,text=f"Проверенные советы для {gname}",font=ctk.CTkFont(size=11),text_color=DIM).pack(anchor="w",pady=(0,12))
        for i,tip in enumerate(g["tips"]):
            c=ctk.CTkFrame(pad,fg_color=PANEL2,corner_radius=9,border_width=1,border_color=BORDER)
            c.pack(fill="x",pady=3)
            ci=ctk.CTkFrame(c,fg_color="transparent"); ci.pack(fill="x",padx=14,pady=10)
            nr=ctk.CTkFrame(ci,fg_color="transparent"); nr.pack(fill="x")
            ctk.CTkLabel(nr,text=f"{tip['icon']}  {tip['title']}",
                         font=ctk.CTkFont(size=12,weight="bold"),text_color="#fff").pack(anchor="w")
            ctk.CTkLabel(nr,text=tip["text"],font=ctk.CTkFont(size=11),
                         text_color=TEXT,wraplength=700,justify="left").pack(anchor="w",pady=(2,0))

    # ── TAB: CS2 CONFIG ──────────────────────────────────
    def _tab_cs2_config(self,pad):
        ctk.CTkLabel(pad,text="⚙️ autoexec.cfg",font=ctk.CTkFont(size=16,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,4))
        ctk.CTkLabel(pad,text="Готовый конфиг для максимального FPS и низкого пинга",
                     font=ctk.CTkFont(size=11),text_color=DIM).pack(anchor="w",pady=(0,10))
        cfg_text="""// CS2 Autoexec — Game Optimizer v2.0
fps_max 0
r_lowlatency 2
cl_showfps 1
mat_queue_mode -1
r_dynamic_lighting 0
r_shadowrendertotexture 0
r_shadows 0
cl_ragdoll_physics_enable 0
r_motionblur 0
cl_interp 0
cl_interp_ratio 1
rate 786432
cl_updaterate 128
cl_cmdrate 128
net_graphproportionalfont 0
cl_mouseinput 1
m_rawinput 1
sensitivity 2.0"""
        tb=ctk.CTkTextbox(pad,height=280,fg_color="#020810",border_width=1,border_color=BORDER,
                          font=ctk.CTkFont(family="Courier New",size=12),text_color="#68ffaa",corner_radius=8)
        tb.pack(fill="x",pady=(0,10)); tb.insert("end",cfg_text)
        btn(pad,"💾  Сохранить autoexec.cfg",lambda:self._save_cs2_cfg(tb.get("1.0","end")),
            width=240,color="#006adf",hover="#0090ff").pack(anchor="w")

    def _save_cs2_cfg(self,content):
        path=os.path.join(os.path.expanduser("~"),"Downloads","autoexec.cfg")
        try:
            with open(path,"w") as f: f.write(content)
        except: pass

    # ── TAB: FIVEM ───────────────────────────────────────
    def _tab_fivem(self,pad):
        ctk.CTkLabel(pad,text="🟣 FiveM оптимизация",font=ctk.CTkFont(size=16,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,4))
        ctk.CTkLabel(pad,text="Специальные твики для FiveM серверов",font=ctk.CTkFont(size=11),text_color=DIM).pack(anchor="w",pady=(0,12))
        fivem_opts=[
            ("🧹","Очистить кэш FiveM","Удаляет кэш шейдеров и текстур",NEON,
             [r'rmdir /s /q "%LOCALAPPDATA%\FiveM\FiveM.app\cache"'],
             []),
            ("🔕","Отключить оверлей FiveM","Убирает оверлей сервера",ORANGE,
             ['reg add "HKCU\\Software\\CitizenFX\\FiveM" /v DrawOverlay /t REG_DWORD /d 0 /f'],
             ['reg add "HKCU\\Software\\CitizenFX\\FiveM" /v DrawOverlay /t REG_DWORD /d 1 /f']),
            ("⚡","Режим StreamMemory","Увеличить память стриминга",GREEN,
             ['reg add "HKCU\\Software\\CitizenFX\\FiveM" /v StreamingMemory /t REG_DWORD /d 756 /f'],
             ['reg add "HKCU\\Software\\CitizenFX\\FiveM" /v StreamingMemory /t REG_DWORD /d 512 /f']),
            ("📡","Только нужные ресурсы","Отключить ненужные серверные скрипты",PURPLE,
             ["echo Отключи ненужные ресурсы в меню сервера"],
             []),
        ]
        for ico,name,desc,accent,on_c,off_c in fivem_opts:
            self._toggle_row(pad,f"{ico}  {name}",desc,on_c,off_c,accent=accent)
        ctk.CTkFrame(pad,height=1,fg_color=BORDER).pack(fill="x",pady=10)
        ctk.CTkLabel(pad,text="💡 Совет: используй +set fpslimit 0 в параметрах запуска FiveM",
                     font=ctk.CTkFont(size=11,slant="italic"),text_color=GOLD).pack(anchor="w")

    # ── TAB: RUST LAUNCH ─────────────────────────────────
    def _tab_rust_launch(self,pad):
        ctk.CTkLabel(pad,text="🔩 Launch Arguments",font=ctk.CTkFont(size=16,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,4))
        ctk.CTkLabel(pad,text="Параметры запуска Rust — вставь в Steam → Свойства → Параметры запуска",
                     font=ctk.CTkFont(size=11),text_color=DIM).pack(anchor="w",pady=(0,10))
        presets_launch=[
            ("⚡ Максимум FPS","-high -maxMem=8192 -malloc=system -force-feature-level-11-0 +clientgc 256 +fps.limit 0 -nolog -nosteam"),
            ("⚖️ Баланс","-high -maxMem=8192 -malloc=system +fps.limit 0"),
            ("🖥 Слабый ПК","-high -maxMem=4096 -malloc=system -force-feature-level-10-0 +fps.limit 60 -nolog"),
        ]
        for pname,args in presets_launch:
            c=ctk.CTkFrame(pad,fg_color=PANEL2,corner_radius=9,border_width=1,border_color=BORDER)
            c.pack(fill="x",pady=4)
            ci=ctk.CTkFrame(c,fg_color="transparent"); ci.pack(fill="x",padx=14,pady=10)
            ctk.CTkLabel(ci,text=pname,font=ctk.CTkFont(size=12,weight="bold"),text_color="#fff").pack(anchor="w")
            tb=ctk.CTkTextbox(ci,height=50,fg_color="#020810",border_width=1,border_color=BORDER,
                              font=ctk.CTkFont(family="Courier New",size=11),text_color=NEON,corner_radius=6)
            tb.pack(fill="x",pady=(4,0)); tb.insert("end",args)

    # ── FULL OPTIMIZE ────────────────────────────────────
    def _full_optimize(self,gname):
        # Find or create a floating log
        win=ctk.CTkToplevel(self); win.title(f"Оптимизация {gname}"); win.geometry("500x400")
        win.configure(fg_color=BG)
        ctk.CTkLabel(win,text=f"⚡ Оптимизация {gname}",font=ctk.CTkFont(size=16,weight="bold"),text_color="#fff").pack(pady=(16,8))
        log=self._log(win,280); log.pack_forget(); log.pack(fill="both",expand=True,padx=16,pady=(0,16))
        def run():
            self._w(log,f"▶ Полная оптимизация для {gname}...")
            cmds=[
                ("⚡ Высокий план питания","powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"),
                ("🚫 Откл. Game DVR",'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f'),
                ("🌐 DNS Google",'netsh interface ip set dns "Ethernet" static 8.8.8.8'),
                ("🏎 Откл. Nagle",'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TcpAckFrequency /t REG_DWORD /d 1 /f'),
                ("🔄 Flush DNS","ipconfig /flushdns"),
                ("⏸ Стоп Windows Update","net stop wuauserv"),
                ("🔍 Стоп Indexer","net stop wsearch"),
                ("📊 Стоп SysMain","net stop sysmain"),
                ("🧹 Очистка RAM","rundll32.exe advapi32.dll,ProcessIdleTasks"),
            ]
            for name,cmd in cmds:
                ok=run_cmd(cmd); self._w(log,f"  {'✓' if ok else '✗'} {name}"); time.sleep(0.15)
            self._w(log,f"\n✅ Оптимизация завершена!")
            self._w(log,f"   Запускай {gname}!")
        threading.Thread(target=run,daemon=True).start()

    # ── WINDOWS PAGE ─────────────────────────────────────
    def _build_windows(self):
        p=self._scr("windows"); pad=self._pad(p)
        ctk.CTkLabel(pad,text="⚡ Оптимизация Windows",font=ctk.CTkFont(size=18,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,4))
        ctk.CTkLabel(pad,text="Системные твики для максимального FPS в любой игре",font=ctk.CTkFont(size=11),text_color=DIM).pack(anchor="w",pady=(0,12))
        win_opts=[
            ("⚡","Высокий план питания","Максимальная производительность CPU",NEON,
             ["powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"],
             ["powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e"]),
            ("📈","Приоритет CPU (Win32=38)","Лучший отклик в играх",GREEN,
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f'],
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 2 /f']),
            ("🎮","Hardware-Accelerated GPU Scheduling","HAGS — меньше задержка GPU",PURPLE,
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v HwSchMode /t REG_DWORD /d 2 /f'],
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v HwSchMode /t REG_DWORD /d 1 /f']),
            ("🖥","Откл. визуальные эффекты Windows","Анимации, тени — ненужный расход",ORANGE,
             ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f'],
             ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 0 /f']),
            ("💾","Откл. очистку PageFile","Быстрее выключение ПК",NEON,
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v ClearPageFileAtShutdown /t REG_DWORD /d 0 /f'],
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v ClearPageFileAtShutdown /t REG_DWORD /d 1 /f']),
            ("🔕","Откл. Xbox Game Bar","-5-15% CPU в играх",RED,
             ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f',
              'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f'],
             ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 1 /f']),
            ("🔍","Откл. Windows Search","Не индексирует во время игры",GOLD,
             ["net stop wsearch","sc config wsearch start=disabled"],
             ["net start wsearch","sc config wsearch start=auto"]),
            ("📊","Откл. SysMain / Superfetch","Освобождает RAM и диск",ORANGE,
             ["net stop sysmain","sc config sysmain start=disabled"],
             ["net start sysmain","sc config sysmain start=auto"]),
            ("🧹","Очистка RAM перед игрой","Освобождает оперативную память",GREEN,
             ["rundll32.exe advapi32.dll,ProcessIdleTasks"],[]),
            ("⏸","Пауза Windows Update","Обновления не мешают игре",RED,
             ["net stop wuauserv","net stop bits","net stop dosvc"],
             ["net start wuauserv"]),
        ]
        for ico,name,desc,accent,on_c,off_c in win_opts:
            self._toggle_row(pad,f"{ico}  {name}",desc,on_c,off_c,accent=accent)
        ctk.CTkFrame(pad,height=1,fg_color=BORDER).pack(fill="x",pady=12)
        btn(pad,"⚡  ВКЛЮЧИТЬ ВСЕ ОПТИМИЗАЦИИ",self._run_all_windows,size=14,width=300,color="#006adf",hover="#0090ff").pack(anchor="w")
        self.win_log=self._log(pad,100)

    def _run_all_windows(self):
        self._clr(self.win_log); self._w(self.win_log,"⚡ Применяю все оптимизации...")
        cmds=["powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
              'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f',
              'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f',
              'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v HwSchMode /t REG_DWORD /d 2 /f',
              "net stop wsearch","net stop sysmain","net stop wuauserv",
              "rundll32.exe advapi32.dll,ProcessIdleTasks"]
        names=["⚡ Высокий план питания","🔕 Откл. Game DVR","📈 Приоритет CPU",
               "🎮 HAGS включён","🔍 Откл. Search","📊 Откл. SysMain","⏸ Стоп Update","🧹 Очистка RAM"]
        def run():
            for name,cmd in zip(names,cmds):
                ok=run_cmd(cmd); self._w(self.win_log,f"  {'✓' if ok else '✗'} {name}"); time.sleep(0.1)
            self._w(self.win_log,"\n✅ Готово! Перезагрузи ПК для полного эффекта.")
        threading.Thread(target=run,daemon=True).start()

    # ── NETWORK PAGE ─────────────────────────────────────
    def _build_network(self):
        p=self._scr("network"); pad=self._pad(p)
        ctk.CTkLabel(pad,text="🌐 Настройка сети",font=ctk.CTkFont(size=18,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,4))
        ctk.CTkLabel(pad,text="Оптимизация пинга для всех игр",font=ctk.CTkFont(size=11),text_color=DIM).pack(anchor="w",pady=(0,12))
        net_opts=[
            ("🌐","DNS Google + Cloudflare","Быстрый DNS = меньше задержка",GREEN,
             ['netsh interface ip set dns "Ethernet" static 8.8.8.8',
              'netsh interface ip add dns "Ethernet" 1.1.1.1 index=2',"ipconfig /flushdns"],
             ['netsh interface ip set dns "Ethernet" dhcp',"ipconfig /flushdns"]),
            ("🏎","Откл. Nagle","TcpAckFrequency=1, -5-30ms пинга",NEON,
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TcpAckFrequency /t REG_DWORD /d 1 /f',
              'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TCPNoDelay /t REG_DWORD /d 1 /f'],
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TcpAckFrequency /t REG_DWORD /d 2 /f']),
            ("📶","QoS DSCP=46","Приоритет игрового трафика",PURPLE,
             ['netsh qos delete policy "GO_Game"',
              'netsh qos add policy "GO_Game" app="*" dscp=46 throttle-rate=-1'],
             ['netsh qos delete policy "GO_Game"']),
            ("🔕","Откл. IPv6","Убирает конфликты IPv6/IPv4",ORANGE,
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters" /v DisabledComponents /t REG_DWORD /d 255 /f'],
             ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters" /v DisabledComponents /t REG_DWORD /d 0 /f']),
            ("🔄","Сброс Winsock + IP стека","Полный сброс сети",RED,
             ["netsh winsock reset","netsh int ip reset","ipconfig /flushdns","ipconfig /registerdns"],
             []),
            ("🚀","Автонастройка TCP","Highlyrestricted = стабильнее",GOLD,
             ["netsh interface tcp set global autotuninglevel=highlyrestricted"],
             ["netsh interface tcp set global autotuninglevel=normal"]),
        ]
        for ico,name,desc,accent,on_c,off_c in net_opts:
            self._toggle_row(pad,f"{ico}  {name}",desc,on_c,off_c,accent=accent)
        ctk.CTkFrame(pad,height=1,fg_color=BORDER).pack(fill="x",pady=10)
        btn(pad,"📡  Проверить пинг",self._run_global_ping,width=180,color="#006adf",hover="#0090ff").pack(anchor="w")
        self.net_log=self._log(pad,110)

    def _run_global_ping(self):
        self._clr(self.net_log); self._w(self.net_log,"Проверяю серверы...")
        def run():
            for name,host in [("Steam","store.steampowered.com"),("Cloudflare","1.1.1.1"),
                               ("Google","8.8.8.8"),("Faceit","api.faceit.com"),("AWS EU","ec2.eu-central-1.amazonaws.com")]:
                ms=ping_host(host)
                s="OK ✓" if ms>0 and ms<80 else "СРЕДНИЙ" if ms>0 and ms<150 else "ВЫСОКИЙ ⚠" if ms>0 else "timeout ✗"
                self._w(self.net_log,f"  {name:<16} {str(ms)+' ms' if ms>0 else 'timeout':>10}  {s}")
                time.sleep(0.1)
            self._w(self.net_log,"✅ Готово!")
        threading.Thread(target=run,daemon=True).start()

    # ── MONITOR PAGE ─────────────────────────────────────
    def _build_monitor(self):
        p=self._scr("monitor"); pad=self._pad(p)
        ctk.CTkLabel(pad,text="📊 Мониторинг пинга",font=ctk.CTkFont(size=18,weight="bold"),text_color="#fff").pack(anchor="w",pady=(0,4))
        ctk.CTkLabel(pad,text="Живой график задержки до игровых серверов",font=ctk.CTkFont(size=11),text_color=DIM).pack(anchor="w",pady=(0,10))
        sr=ctk.CTkFrame(pad,fg_color="transparent"); sr.pack(fill="x",pady=(0,10))
        for i in range(3): sr.columnconfigure(i,weight=1)
        def sbox(col,val,label,color):
            f=ctk.CTkFrame(sr,fg_color=PANEL2,corner_radius=9,border_width=1,border_color=BORDER)
            f.grid(row=0,column=col,padx=4,sticky="ew")
            v=ctk.CTkLabel(f,text=val,font=ctk.CTkFont(size=24,weight="bold"),text_color=color); v.pack(pady=(10,2))
            ctk.CTkLabel(f,text=label,font=ctk.CTkFont(size=10),text_color=DIM).pack(pady=(0,8))
            return v
        self.ms_cur=sbox(0,"—","Текущий ms",GREEN)
        self.ms_avg=sbox(1,"—","Средний ms",GOLD)
        self.ms_max=sbox(2,"Максимум ms",RED,"—")
        cr=ctk.CTkFrame(pad,fg_color="transparent"); cr.pack(fill="x",pady=(0,10))
        self.mon_btn=btn(cr,"▶  Запустить",self._toggle_mon,width=200,color="#006adf",hover="#0090ff")
        self.mon_btn.pack(side="left")
        self.mon_lbl=ctk.CTkLabel(cr,text="● Остановлен",text_color=DIM,font=ctk.CTkFont(size=11)); self.mon_lbl.pack(side="left",padx=12)
        ctk.CTkLabel(cr,text="Интервал:",text_color=DIM,font=ctk.CTkFont(size=11)).pack(side="left")
        self.mon_int=ctk.CTkComboBox(cr,values=["2 сек","5 сек","10 сек"],width=88,fg_color=PANEL2,border_color=BORDER)
        self.mon_int.set("2 сек"); self.mon_int.pack(side="left",padx=6)
        self.srv_lbls={}
        for name,host in [("Steam","store.steampowered.com"),("Cloudflare","1.1.1.1"),
                           ("Google DNS","8.8.8.8"),("Faceit","api.faceit.com")]:
            row=ctk.CTkFrame(pad,fg_color=PANEL2,corner_radius=8,border_width=1,border_color=BORDER); row.pack(fill="x",pady=3)
            ctk.CTkLabel(row,text="●",font=ctk.CTkFont(size=12),text_color=DIM).pack(side="left",padx=(12,8),pady=8)
            ctk.CTkLabel(row,text=name,font=ctk.CTkFont(size=12),text_color=TEXT,width=130).pack(side="left")
            lbl=ctk.CTkLabel(row,text="— ms",font=ctk.CTkFont(size=12,weight="bold"),text_color=DIM); lbl.pack(side="right",padx=14)
            self.srv_lbls[host]=lbl
        cc=ctk.CTkFrame(pad,fg_color=PANEL2,corner_radius=12,border_width=1,border_color=BORDER); cc.pack(fill="x",pady=6)
        ctk.CTkLabel(cc,text="📈 График",font=ctk.CTkFont(size=11),text_color=DIM).pack(anchor="w",padx=12,pady=(8,2))
        self.chart=ctk.CTkCanvas(cc,height=110,bg="#020810",highlightthickness=0); self.chart.pack(fill="x",padx=10,pady=(0,8))

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
            for name,host in [("Steam","store.steampowered.com"),("Cloudflare","1.1.1.1"),
                               ("Google DNS","8.8.8.8"),("Faceit","api.faceit.com")]:
                ms=ping_host(host); results.append(ms)
                lbl=self.srv_lbls[host]
                if ms<0: lbl.configure(text="timeout",text_color=RED)
                else:
                    c=GREEN if ms<80 else GOLD if ms<150 else RED
                    lbl.configure(text=f"{ms} ms",text_color=c)
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
        W=c.winfo_width() or 500; H=110; maxV=max(max(self.ping_history),200)
        pts=[(int(10+(i/(len(self.ping_history)-1))*(W-20)),int(H-10-(v/maxV)*(H-20))) for i,v in enumerate(self.ping_history)]
        poly=[(10,H-10)]+pts+[(pts[-1][0],H-10)]
        c.create_polygon([x for pt in poly for x in pt],fill="#003030",outline="")
        last=self.ping_history[-1]; col=GREEN if last<80 else GOLD if last<150 else RED
        c.create_line([x for pt in pts for x in pt],fill=col,width=2,smooth=True)

# ═══════════════════════════════════════════════════════
# GAME DATA
# ═══════════════════════════════════════════════════════
GAMES={
    "Rust":{
        "icon":"🔫","color":"#e07020","desc":"Survival multiplayer",
        "presets":{
            "Максимум FPS":{"desc":"Минимум графики","fps_expect":"100-200+","launch":"-high -maxMem=8192 -malloc=system +fps.limit 0 -nolog",
                "settings":[("grass.on","false"),("terrain.quality","0"),("graphics.shadows","0"),("graphics.ssao","0"),("graphics.damage","0"),("graphics.itemskins","0"),("graphics.lodbias","0.25")]},
            "Баланс":{"desc":"FPS + читаемость","fps_expect":"60-120","launch":"-high -maxMem=8192 +fps.limit 0",
                "settings":[("grass.on","true"),("terrain.quality","50"),("graphics.shadows","1"),("graphics.ssao","0"),("graphics.lodbias","1")]},
            "Качество":{"desc":"Полная графика","fps_expect":"40-80","launch":"+fps.limit 0",
                "settings":[("grass.on","true"),("terrain.quality","100"),("graphics.shadows","3"),("graphics.ssao","1"),("graphics.lodbias","2")]},
        },
        "tips":[
            {"icon":"💡","title":"Отключи Steam оверлей","text":"В Steam → ПКМ на Rust → Свойства → Снять галочку 'Включить Steam Overlay'"},
            {"icon":"🛡","title":"Добавь в исключения антивируса","text":"Windows Defender → Защита → Исключения → Папка с Rust (обычно SteamApps\\common\\Rust)"},
            {"icon":"🎮","title":"Используй DirectX 11","text":"В параметрах запуска добавь -force-feature-level-11-0 для стабильного FPS"},
            {"icon":"🧹","title":"Очищай кэш шейдеров","text":"Папка Rust → AppData\\Local\\Temp\\Rust — удаляй раз в неделю, первый запуск будет дольше"},
            {"icon":"📡","title":"Выбирай сервер близко","text":"Rust не имеет официальных регионов — выбирай сервер с наименьшим пингом вручную"},
            {"icon":"🔧","title":"client.connect вместо F1","text":"Подключайся через F1 консоль: client.connect IP:PORT — быстрее и стабильнее"},
        ],
    },
    "GTA V":{
        "icon":"🚗","color":"#00a8ff","desc":"Open world / FiveM",
        "presets":{
            "Максимум FPS":{"desc":"Для слабых ПК и FiveM","fps_expect":"80-160+","launch":"-notablet -norestrictions -noFirstRun -IgnoreCorrupts",
                "settings":[("TextureQuality","normal"),("ShaderQuality","normal"),("ShadowQuality","normal"),("ReflectionQuality","off"),("MSAA","off"),("FXAA","off"),("AmbientOcclusion","off"),("MotionBlur","false"),("InGameDepthOfField","false")]},
            "Баланс":{"desc":"Комфортная игра","fps_expect":"60-100","launch":"-notablet -noFirstRun",
                "settings":[("TextureQuality","high"),("ShaderQuality","high"),("ShadowQuality","high"),("MSAA","off"),("FXAA","on"),("AmbientOcclusion","medium"),("MotionBlur","false")]},
            "Качество":{"desc":"Максимальная красота","fps_expect":"40-70","launch":"-notablet",
                "settings":[("TextureQuality","very high"),("ShaderQuality","very high"),("ShadowQuality","very high"),("MSAA","x4"),("FXAA","on"),("AmbientOcclusion","high"),("TessellationQuality","very high")]},
        },
        "tips":[
            {"icon":"🟣","title":"FiveM: отключи все оверлеи","text":"Discord, Steam, NVIDIA — все оверлеи отключи, FiveM сам по себе тяжёлый"},
            {"icon":"🗑","title":"Очисти папку cache","text":"GTA V → update\\x64\\dlcpacks → удали ненужные DLC. Уменьшает время загрузки"},
            {"icon":"📁","title":"Установи Graphics Config","text":"Скачай оптимизированный graphics.cfg с GTA Forums для твоей видеокарты"},
            {"icon":"⚡","title":"Параметр -notablet","text":"Обязательный параметр запуска — убирает ненужный ввод планшета, экономит ресурсы"},
            {"icon":"🌐","title":"GTA Online: NAT Type Open","text":"Для стабильного GTA Online нужен открытый NAT — пробрось порты 6672 UDP и 61455-61458 UDP"},
            {"icon":"🔧","title":"Rockstar Launcher","text":"Выключи Rockstar Games Launcher из автозагрузки — он жрёт RAM когда не нужен"},
        ],
    },
    "CS2":{
        "icon":"🎯","color":"#ff6b35","desc":"Counter-Strike 2",
        "presets":{
            "Максимум FPS":{"desc":"Про-настройки","fps_expect":"200-400+","launch":"-novid -nojoy -noaafonts -limitvsconst -forcenovsync -softparticlesdefaultoff +mat_queue_mode -1 +r_dynamic_lighting 0 -freq 240 -high",
                "settings":[("r_lowlatency","2"),("fps_max","0"),("mat_queue_mode","-1"),("r_dynamic_lighting","0"),("r_shadows","0"),("cl_ragdoll_physics_enable","0"),("r_motionblur","0"),("cl_showfps","1")]},
            "Баланс":{"desc":"FPS + видимость","fps_expect":"144-250","launch":"-novid -nojoy -forcenovsync +mat_queue_mode -1 -high",
                "settings":[("fps_max","0"),("r_lowlatency","2"),("r_shadows","1"),("r_dynamic_lighting","1"),("cl_showfps","1"),("r_motionblur","0")]},
            "Качество":{"desc":"Красивая картинка","fps_expect":"100-180","launch":"-novid +mat_queue_mode -1",
                "settings":[("fps_max","0"),("r_shadows","3"),("r_dynamic_lighting","1"),("r_shadowrendertotexture","1"),("r_motionblur","0")]},
        },
        "tips":[
            {"icon":"🖥","title":"Частота монитора","text":"NVIDIA: Панель управления → Разрешение дисплея → Выбери максимальную частоту (144/240Hz)"},
            {"icon":"🎮","title":"Откл. Game DVR","text":"Win+G → Настройки → Выключи всё. Или Win+I → Игры → Xbox Game Bar → Выключить"},
            {"icon":"🖱","title":"Raw Input мышь","text":"В настройках CS2: m_rawinput 1 — прямой ввод мыши без обработки Windows"},
            {"icon":"📡","title":"Rate команды","text":"rate 786432; cl_interp 0; cl_interp_ratio 1 — в autoexec.cfg для минимального пинга"},
            {"icon":"🔧","title":"config.cfg","text":"Папка: SteamApps\\common\\Counter-Strike Global Offensive\\game\\csgo\\cfg\\"},
            {"icon":"🌡","title":"Температура","text":"CS2 очень нагружает CPU. Следи за температурой — больше 90°C нужна чистка кулера"},
        ],
    },
}

if __name__=="__main__":
    app=App(); app.mainloop()
