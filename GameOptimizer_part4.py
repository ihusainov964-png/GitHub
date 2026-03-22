"""
Game Optimizer v5.0 — ЧАСТЬ 4 из 4
Страницы: Профиль ПК, Windows оптимизации, Настройка сети, Мониторинг пинга.
Живые показатели CPU/RAM/Disk/Temp через wmic.
График пинга. Точка входа if __name__ == "__main__".

════════════════════════════════════════════════════════════
ИНСТРУКЦИЯ ПО СБОРКЕ В ОДИН ФАЙЛ:
════════════════════════════════════════════════════════════

Способ 1 — командная строка Windows:
    copy /b GameOptimizer_part1.py+GameOptimizer_part2.py+GameOptimizer_part3.py+GameOptimizer_part4.py GameOptimizer.py

Способ 2 — PowerShell:
    Get-Content part1.py,part2.py,part3.py,part4.py | Set-Content GameOptimizer.py

Способ 3 — Python скрипт:
    with open('GameOptimizer.py','w',encoding='utf-8') as out:
        for part in ['part1.py','part2.py','part3.py','part4.py']:
            out.write(open(part,encoding='utf-8').read())
            out.write('\\n')

После сборки проверь: python GameOptimizer.py
════════════════════════════════════════════════════════════
"""

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
