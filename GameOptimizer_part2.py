"""
Game Optimizer v5.0 — ЧАСТЬ 2 из 4
Данные CS2, Fortnite, ARK + общие паразиты, Windows и сетевые оптимизации
"""

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
