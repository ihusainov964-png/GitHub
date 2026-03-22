"""
Game Optimizer v5.0 — ЧАСТЬ 3 из 4
Класс приложения App: построение UI, боковая панель,
страницы игр, все вкладки (Графика, Паразиты, Сеть, Советы, Конфиги)
Горячие клавиши, смена темы, скролл колёсиком.

ИНСТРУКЦИЯ ПО СБОРКЕ:
    Объедини все 4 части в один файл в таком порядке:
    part1.py + part2.py + part3.py + part4.py → GameOptimizer.py
    Команда: copy /b part1.py+part2.py+part3.py+part4.py GameOptimizer.py
"""

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
