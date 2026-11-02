"""Sony α6700 极简定制工具 (Ver 2.00) - Desktop GUI.

Dedicated interface focusing exclusively on:
1. Candidate FTP byte patches (playback behavior NOT yet hardware-validated)
2. True Native English Language Menu Unlock
"""
from __future__ import annotations

import os
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from apps.a6700_customizer.app_backend import BackendError, DeviceBackend
from apps.a6700_customizer.targets import ALL_FTP_TARGETS, TARGET_ENGLISH

# Visual Constants (Dark Modern Theme)
BG_MAIN = "#18181b"        # Zinc 900
BG_SIDEBAR = "#121214"     # Darker sidebar
BG_CARD = "#27272a"        # Zinc 800
BG_CARD_HOVER = "#3f3f46"  # Zinc 700
BORDER_COLOR = "#3f3f46"   # Zinc 700 border
TEXT_MAIN = "#f4f4f5"      # Zinc 100
TEXT_MUTED = "#a1a1aa"     # Zinc 400
ACCENT_BLUE = "#2563eb"    # Blue 600
ACCENT_GREEN = "#16a34a"   # Green 600
ACCENT_RED = "#dc2626"     # Red 600
ACCENT_YELLOW = "#ca8a04"  # Yellow 600
FONT_FAMILY = "Segoe UI"


class SonyCustomizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sony α6700 极简定制工具 (Ver 2.00) · FTP & English Unlock")
        self.geometry("960x680")
        self.minsize(880, 620)
        self.configure(bg=BG_MAIN)

        self.backend = DeviceBackend()
        self.busy = False
        self.inspection_result = None

        self._init_styles()
        self._build_layout()
        self.show_page("notice")

    def _init_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Configure common styles
        style.configure(".", background=BG_MAIN, foreground=TEXT_MAIN, font=(FONT_FAMILY, 10))
        style.configure("TFrame", background=BG_MAIN)
        style.configure("Card.TFrame", background=BG_CARD, relief="flat")
        style.configure("Sidebar.TFrame", background=BG_SIDEBAR)

        style.configure("TLabel", background=BG_MAIN, foreground=TEXT_MAIN, font=(FONT_FAMILY, 10))
        style.configure("Card.TLabel", background=BG_CARD, foreground=TEXT_MAIN, font=(FONT_FAMILY, 10))
        style.configure("CardTitle.TLabel", background=BG_CARD, foreground=TEXT_MAIN, font=(FONT_FAMILY, 12, "bold"))
        style.configure("Muted.TLabel", background=BG_MAIN, foreground=TEXT_MUTED, font=(FONT_FAMILY, 9))
        style.configure("CardMuted.TLabel", background=BG_CARD, foreground=TEXT_MUTED, font=(FONT_FAMILY, 9))

        style.configure("Title.TLabel", font=(FONT_FAMILY, 15, "bold"), foreground=TEXT_MAIN)
        style.configure("Header.TLabel", font=(FONT_FAMILY, 13, "bold"), foreground=TEXT_MAIN)

        style.configure("TButton", font=(FONT_FAMILY, 10), padding=(12, 6), background="#3f3f46", foreground=TEXT_MAIN)
        style.map("TButton", background=[("active", "#52525b"), ("disabled", "#27272a")])

        style.configure("Primary.TButton", font=(FONT_FAMILY, 10, "bold"), background=ACCENT_BLUE, foreground="#ffffff")
        style.map("Primary.TButton", background=[("active", "#1d4ed8"), ("disabled", "#1e3a8a")])

        style.configure("Success.TButton", font=(FONT_FAMILY, 10, "bold"), background=ACCENT_GREEN, foreground="#ffffff")
        style.map("Success.TButton", background=[("active", "#15803d"), ("disabled", "#14532d")])

        style.configure("Danger.TButton", font=(FONT_FAMILY, 10), background=ACCENT_RED, foreground="#ffffff")
        style.map("Danger.TButton", background=[("active", "#b91c1c")])

        style.configure("TCheckbutton", background=BG_CARD, foreground=TEXT_MAIN, font=(FONT_FAMILY, 10))
        style.map("TCheckbutton", background=[("active", BG_CARD)])

        style.configure("Horizontal.TProgressbar", background=ACCENT_BLUE, troughcolor="#27272a", bordercolor="#27272a")

    def _build_layout(self):
        # Main split: Sidebar (left) + Content (right)
        self.sidebar = ttk.Frame(self, style="Sidebar.TFrame", width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main_container = ttk.Frame(self, style="TFrame")
        self.main_container.pack(side="right", fill="both", expand=True)

        self._build_sidebar_contents()
        self._build_main_contents()

    def _build_sidebar_contents(self):
        # Brand Header
        brand_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        brand_frame.pack(fill="x", padx=16, pady=(20, 16))

        brand_title = tk.Label(
            brand_frame, text="Sony α6700", font=(FONT_FAMILY, 14, "bold"),
            bg=BG_SIDEBAR, fg="#ffffff"
        )
        brand_title.pack(anchor="w")

        brand_sub = tk.Label(
            brand_frame, text="极简定制 · FTP & English", font=(FONT_FAMILY, 9),
            bg=BG_SIDEBAR, fg=TEXT_MUTED
        )
        brand_sub.pack(anchor="w")

        sep = tk.Frame(self.sidebar, height=1, bg="#27272a")
        sep.pack(fill="x", padx=12, pady=(0, 16))

        # Nav buttons
        self.nav_buttons = {}
        nav_items = [
            ("notice", "📌 1. 操作前须知"),
            ("driver", "🔌 2. 驱动检查"),
            ("prep", "📷 3. 相机准备"),
            ("inspect", "🔍 4. 检测与备份"),
            ("features", "⚡ 5. 功能管理"),
            ("restore", "🔄 6. 出厂还原"),
        ]

        for key, text in nav_items:
            btn = tk.Button(
                self.sidebar, text=text, font=(FONT_FAMILY, 10),
                anchor="w", padx=16, pady=8,
                bg=BG_SIDEBAR, fg=TEXT_MUTED, activebackground=BG_CARD,
                activeforeground="#ffffff", relief="flat", bd=0, cursor="hand2",
                command=lambda k=key: self.show_page(k)
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.nav_buttons[key] = btn

        # Spacer
        tk.Label(self.sidebar, bg=BG_SIDEBAR).pack(fill="both", expand=True)

        # Bottom Safety Badge
        badge_frame = tk.Frame(self.sidebar, bg="#1c1917", padx=10, pady=8)
        badge_frame.pack(fill="x", padx=12, pady=16)

        badge_text = tk.Label(
            badge_frame, text="🛡️ 离线安全保护已就绪\n严守只读预读与原子事务",
            font=(FONT_FAMILY, 8), bg="#1c1917", fg="#a8a29e", justify="left"
        )
        badge_text.pack(anchor="w")

    def _build_main_contents(self):
        # Header / Status bar at top of main container
        self.top_bar = ttk.Frame(self.main_container, padding=(24, 16, 24, 8))
        self.top_bar.pack(fill="x")

        self.page_title_label = ttk.Label(self.top_bar, text="", style="Title.TLabel")
        self.page_title_label.pack(side="left")

        self.status_badge = tk.Label(
            self.top_bar, text="准备就绪", font=(FONT_FAMILY, 9, "bold"),
            bg="#27272a", fg="#a1a1aa", padx=10, pady=3
        )
        self.status_badge.pack(side="right")

        # Content frames stack
        self.pages_container = ttk.Frame(self.main_container, padding=(24, 8, 24, 8))
        self.pages_container.pack(fill="both", expand=True)

        self.pages = {}
        self._build_notice_page()
        self._build_driver_page()
        self._build_prep_page()
        self._build_inspect_page()
        self._build_features_page()
        self._build_restore_page()

        # Bottom Log Viewer / Progress area
        self.bottom_panel = ttk.Frame(self.main_container, padding=(24, 8, 24, 16))
        self.bottom_panel.pack(fill="x", side="bottom")

        self.progress_bar = ttk.Progressbar(self.bottom_panel, mode="indeterminate", style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=(0, 6))

        log_frame = tk.Frame(self.bottom_panel, bg="#09090b", bd=1, relief="solid")
        log_frame.pack(fill="x")

        self.log_text = tk.Text(
            log_frame, height=4, bg="#09090b", fg="#a1a1aa",
            font=("Consolas", 9), relief="flat", padx=8, pady=4,
            wrap="word", state="disabled"
        )
        self.log_text.pack(fill="both", expand=True)

    def log(self, message: str):
        """Append log message thread-safely."""
        self.after(0, self._append_log, message)

    def _append_log(self, message: str):
        self.log_text.configure(state="normal")
        stamp = time.strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{stamp}] {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def set_status(self, text: str, color: str = "#a1a1aa"):
        self.after(0, lambda: self.status_badge.configure(text=text, fg=color))

    def show_page(self, key: str):
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(bg=BG_CARD, fg="#ffffff", font=(FONT_FAMILY, 10, "bold"))
            else:
                btn.configure(bg=BG_SIDEBAR, fg=TEXT_MUTED, font=(FONT_FAMILY, 10))

        for frame in self.pages.values():
            frame.pack_forget()

        if key in self.pages:
            self.pages[key].pack(fill="both", expand=True)

        titles = {
            "notice": "1. 操作前须知与安全声明",
            "driver": "2. Windows USB 驱动检查",
            "prep": "3. 相机连接与模式准备",
            "inspect": "4. 相机只读检测与自动备份",
            "features": "5. 功能管理 (FTP 与英文语言)",
            "restore": "6. 一键出厂无损还原",
        }
        self.page_title_label.configure(text=titles.get(key, ""))

    # --- Page 1: Notice ---
    def _build_notice_page(self):
        page = ttk.Frame(self.pages_container)
        self.pages["notice"] = page

        card = ttk.Frame(page, style="Card.TFrame", padding=20)
        card.pack(fill="both", expand=True, pady=10)

        notice_text = (
            "欢迎使用 Sony ILCE-6700 极简功能定制工具。\n\n"
            "本工具专门为实现两大核心需求而定制开发：\n"
            "  1. 实验性 FTP 解锁候选：网络菜单标记与回放按键 0x0817 候选字段；相册实际传输尚未实机验证\n"
            "  2. 原生英文菜单解锁：通过底层断言门禁原生开放 English 选项，绝不粗暴替换汉字文字包！\n\n"
            "【非协商性安全准则】\n"
            "● 硬件适用范围：仅支持 Sony ILCE-6700 (α6700) 国行版机身，固件版本 2.00。\n"
            "● 极简修改足迹：全部操作仅涉及 /usr/lib/appFw.so 中共 14 个字节。绝不改动内核、bootloader、传感器标定和无线射频。\n"
            "● 注意：字节回读成功仅表示候选目标被写入，不代表 FTP 功能可用；未知字节将拒绝写入，备份不保证能恢复无法启动的相机。"
        )
        lbl = ttk.Label(card, text=notice_text, style="Card.TLabel", justify="left")
        lbl.pack(anchor="w", pady=(0, 20))

        self.notice_var = tk.BooleanVar(value=False)
        chk = ttk.Checkbutton(
            card, text="我已充分阅读并理解上述安全须知，知晓操作规范与备份原则",
            variable=self.notice_var, command=self._toggle_notice_ack
        )
        chk.pack(anchor="w", pady=(0, 20))

        self.notice_next_btn = ttk.Button(
            card, text="下一步：检查驱动 ➔", style="Primary.TButton",
            state="disabled", command=lambda: self.show_page("driver")
        )
        self.notice_next_btn.pack(anchor="e")

    def _toggle_notice_ack(self):
        if self.notice_var.get():
            self.notice_next_btn.configure(state="normal")
        else:
            self.notice_next_btn.configure(state="disabled")

    # --- Page 2: Driver ---
    def _build_driver_page(self):
        page = ttk.Frame(self.pages_container)
        self.pages["driver"] = page

        card = ttk.Frame(page, style="Card.TFrame", padding=20)
        card.pack(fill="both", expand=True, pady=10)

        title = ttk.Label(card, text="WinUSB 驱动状态", style="CardTitle.TLabel")
        title.pack(anchor="w", pady=(0, 10))

        desc = ttk.Label(
            card, text="Sony 相机服务模式与通信依赖 WinUSB 通信驱动。如果当前未绑定，点击下方按钮一键安装。",
            style="CardMuted.TLabel"
        )
        desc.pack(anchor="w", pady=(0, 20))

        self.driver_status_lbl = tk.Label(
            card, text="正在读取驱动状态…", font=(FONT_FAMILY, 11),
            bg=BG_CARD, fg="#e4e4e7", justify="left"
        )
        self.driver_status_lbl.pack(anchor="w", pady=(0, 20))

        btn_row = ttk.Frame(card, style="Card.TFrame")
        btn_row.pack(fill="x", pady=10)

        self.driver_scan_btn = ttk.Button(
            btn_row, text="🔄 重新扫描驱动", command=self._do_driver_scan
        )
        self.driver_scan_btn.pack(side="left", padx=(0, 12))

        self.driver_install_btn = ttk.Button(
            btn_row, text="🛠️ 一键绑定 WinUSB 驱动", style="Primary.TButton",
            command=self._do_driver_install
        )
        self.driver_install_btn.pack(side="left", padx=(0, 12))

        self.driver_next_btn = ttk.Button(
            btn_row, text="下一步：相机准备 ➔", style="Success.TButton",
            command=lambda: self.show_page("prep")
        )
        self.driver_next_btn.pack(side="left")

        self.after(500, self._do_driver_scan)

    def _do_driver_scan(self):
        res = self.backend.check_driver()
        msg = f"状态: {res['message']}\n"
        if res.get("devices"):
            msg += f"检测到设备: {len(res['devices'])} 个接口已关联"
        self.driver_status_lbl.configure(text=msg)
        if res["ok"]:
            self.driver_status_lbl.configure(fg="#4ade80")
            self.set_status("驱动已就绪", "#4ade80")
            if hasattr(self, "driver_next_btn"):
                self.driver_next_btn.configure(state="normal")
        else:
            self.driver_status_lbl.configure(fg="#f87171")

    def _do_driver_install(self):
        res = self.backend.check_driver()
        if res.get("ok"):
            messagebox.showinfo(
                "驱动已就绪",
                "当前 WinUSB 驱动已经处于就绪状态（已成功关联 WinUSB 服务）！\n\n"
                "无需重复安装，您可以直接点击「下一步：相机准备」或进入「4. 检测与备份」。"
            )
            return

        self.log("正在请求管理员权限安装 WinUSB 驱动…")
        def worker():
            try:
                self.backend.install_driver(progress=self.log)
                self.log("驱动安装完成，正在更新状态…")
                self.after(1000, self._do_driver_scan)
            except Exception as exc:
                self.log(f"驱动安装异常: {exc}")
                self.after(0, lambda: messagebox.showerror("安装驱动错误", str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    # --- Page 3: Preparation ---
    def _build_prep_page(self):
        page = ttk.Frame(self.pages_container)
        self.pages["prep"] = page

        card = ttk.Frame(page, style="Card.TFrame", padding=20)
        card.pack(fill="both", expand=True, pady=10)

        title = ttk.Label(card, text="相机物理连接与准备检查", style="CardTitle.TLabel")
        title.pack(anchor="w", pady=(0, 10))

        items = [
            ("prep_1", "1. 相机电池电量保持在 80% 以上，或已连接可靠 USB 供电。"),
            ("prep_2", "2. 相机菜单设置：设置 -> USB -> USB连接模式 设为「海量存储 (MSC)」。"),
            ("prep_3", "3. 菜单设置：设置 -> 电源保存 -> 自动关机温度/时间 设置为长或关闭，防止写入中途休眠。"),
            ("prep_4", "4. 使用高质量 USB-C 数据线直接连接电脑原生接口（严禁经由未经供电的扩展坞）。"),
        ]

        self.prep_vars = {}
        for key, text in items:
            var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(
                card, text=text, variable=var, command=self._check_prep_state
            )
            chk.pack(anchor="w", pady=8)
            self.prep_vars[key] = var

        self.prep_next_btn = ttk.Button(
            card, text="全部确认，进入只读检测 ➔", style="Primary.TButton",
            state="disabled", command=lambda: self.show_page("inspect")
        )
        self.prep_next_btn.pack(anchor="e", pady=(20, 0))

    def _check_prep_state(self):
        if all(v.get() for v in self.prep_vars.values()):
            self.prep_next_btn.configure(state="normal")
        else:
            self.prep_next_btn.configure(state="disabled")

    # --- Page 4: Inspect & Backup ---
    def _build_inspect_page(self):
        page = ttk.Frame(self.pages_container)
        self.pages["inspect"] = page

        card = ttk.Frame(page, style="Card.TFrame", padding=20)
        card.pack(fill="both", expand=True, pady=10)

        title = ttk.Label(card, text="相机只读检测与自动快照", style="CardTitle.TLabel")
        title.pack(anchor="w", pady=(0, 6))

        desc = ttk.Label(
            card, text="在此进行无损只读检查。程序将读取 /usr/lib/appFw.so 并判断功能状态，同时自动留存原始快照。",
            style="CardMuted.TLabel"
        )
        desc.pack(anchor="w", pady=(0, 16))

        self.inspect_info_lbl = tk.Label(
            card, text="尚未检测。请连接相机后点击下方按钮。",
            font=(FONT_FAMILY, 10), bg="#18181b", fg=TEXT_MAIN,
            padx=16, pady=16, justify="left", bd=1, relief="solid"
        )
        self.inspect_info_lbl.pack(fill="x", pady=(0, 20))

        btn_row = ttk.Frame(card, style="Card.TFrame")
        btn_row.pack(fill="x")

        self.inspect_btn = ttk.Button(
            btn_row, text="🔍 开始只读检查与备份", style="Primary.TButton",
            command=self._start_inspect_task
        )
        self.inspect_btn.pack(side="left", padx=(0, 12))

        self.open_backup_btn = ttk.Button(
            btn_row, text="📁 打开备份目录",
            command=self._open_backup_folder
        )
        self.open_backup_btn.pack(side="left")

    def _open_backup_folder(self):
        folder = self.backend.backup_dir
        folder.mkdir(parents=True, exist_ok=True)
        os.startfile(folder)

    def _start_inspect_task(self):
        if self.busy:
            return
        self._set_busy(True)
        self.progress_bar.start(10)
        self.log("开始相机只读检测…")

        def worker():
            try:
                res = self.backend.inspect_device(progress=self.log)
                backup_path = self.backend.perform_backup(res, progress=self.log)
                self.inspection_result = res
                self.after(0, self._render_inspection_success, res, backup_path)
            except Exception as exc:
                self.log(f"检测失败: {exc}")
                self.after(0, lambda: messagebox.showerror("检测失败", str(exc)))
            finally:
                self.after(0, self._finish_task)

        threading.Thread(target=worker, daemon=True).start()

    def _render_inspection_success(self, res: dict, backup_path: Path):
        en_str = {
            "PATCHED": "已写入候选字节 (Patched)",
            "STOCK": "原始锁定 (Stock)",
            "MISMATCH": "字节异常 (Unknown) — 禁止写入",
        }.get(res["english_status"], "未知状态")
        if res.get("ftp_note"):
            ftp_str = res["ftp_note"]
        elif res["ftp_status"] == "PATCHED":
            ftp_str = "完整开放 (Patched)"
        elif res["ftp_status"] == "PARTIAL":
            ftp_str = "部分启用 (Partial)"
        else:
            ftp_str = "原始锁定 (Stock)"

        msg = (
            f"✅ 检测完成！固件版本: ILCE-6700 Ver. 2.00\n"
            f"● /usr/lib/appFw.so 文件大小: {res['appfw_size']:,} 字节 (校验通过)\n"
            f"● 原生英文语言状态: {en_str}\n"
            f"● FTP 候选字节状态（非实机功能验收）: {ftp_str}\n"
            f"● 自动快照保存位置: {backup_path.name}"
        )
        self.inspect_info_lbl.configure(text=msg)
        if res["english_status"] == "MISMATCH" or res["ftp_status"] == "MISMATCH":
            self.set_status("发现未知固件字节 — 请停止写入", "#f59e0b")
            self.apply_btn.configure(state="disabled")
        else:
            self.set_status("候选字节读取完成（需实机验证）", "#4ade80")
            self.apply_btn.configure(state="normal")

        # Update Features page banner for Powerful6700 upgrades
        if hasattr(self, "ftp_upgrade_banner"):
            if res.get("is_powerful6700_upgrade"):
                self.ftp_upgrade_banner.pack(anchor="w", fill="x", pady=(10, 0))
            else:
                self.ftp_upgrade_banner.pack_forget()

        messagebox.showinfo("检测成功", "相机已成功连接，只读校验通过，原始备份已安全存盘！")
        self.show_page("features")

    # --- Page 5: Features Management ---
    def _build_features_page(self):
        page = ttk.Frame(self.pages_container)
        self.pages["features"] = page

        # Card 1: Full FTP
        card_ftp = ttk.Frame(page, style="Card.TFrame", padding=16)
        card_ftp.pack(fill="x", pady=(0, 12))

        self.var_ftp = tk.BooleanVar(value=True)
        chk_ftp = ttk.Checkbutton(
            card_ftp, text="实验性 FTP 候选字段（Network + Playback 0x0817；尚未实机验收）",
            variable=self.var_ftp
        )
        chk_ftp.pack(anchor="w", pady=(0, 6))

        ftp_desc = (
            "包含 Network 菜单 9 个候选标志及回放 Action 0x0817，仍需检查相册界面（Menu 0x02aa）\n"
            "Action 0x0817 (FTP_TRANSFER) 的其它门禁与上传功能尚未确认；切勿视作已修复。"
        )
        ttk.Label(card_ftp, text=ftp_desc, style="CardMuted.TLabel", justify="left").pack(anchor="w")

        self.ftp_upgrade_banner = tk.Label(
            card_ftp,
            text="💡 检测到此前已使用 Powerful6700 开启过网络 FTP 菜单。\n本次勾选只会尝试设置【回放快捷键 0x0817】候选字节，不保证相册菜单或 FTP 上传可用；须核实当前状态。",
            font=(FONT_FAMILY, 9), bg="#042f2e", fg="#2dd4bf",
            padx=10, pady=8, justify="left", bd=1, relief="solid"
        )

        # Card 2: English Unlock
        card_en = ttk.Frame(page, style="Card.TFrame", padding=16)
        card_en.pack(fill="x", pady=(0, 16))

        self.var_en = tk.BooleanVar(value=True)
        chk_en = ttk.Checkbutton(
            card_en, text="原生英文语言菜单解锁 (True Native English Language)",
            variable=self.var_en
        )
        chk_en.pack(anchor="w", pady=(0, 6))

        en_desc = (
            "通过底层 english_predicate (0x023080f8) 门禁断言放开 English 选项。\n"
            "菜单中选中后由相机原生持久化为 Bank 0 英文文字包，绝不粗暴替换汉字文件，仅改写 4 字节。"
        )
        ttk.Label(card_en, text=en_desc, style="CardMuted.TLabel", justify="left").pack(anchor="w")

        # Action Button
        self.apply_btn = ttk.Button(
            page, text="⚡ 写入所选功能至相机", style="Success.TButton",
            command=self._start_apply_task
        )
        self.apply_btn.pack(anchor="e", pady=8)

    def _start_apply_task(self):
        if self.busy:
            return
        en = self.var_en.get()
        ftp = self.var_ftp.get()
        if not en and not ftp:
            messagebox.showwarning("提示", "请至少勾选一项功能！")
            return

        total_bytes = (4 if en else 0) + (10 if ftp else 0)
        confirm = messagebox.askyesno(
            "确认写入",
            f"即将在相机 /usr/lib/appFw.so 中写入共计 {total_bytes} 字节。\n\n"
            f"● 英文菜单解锁: {'是' if en else '否'}\n"
            f"● FTP 候选字节修改: {'是' if ftp else '否'}\n\n"
            "写入前将自动进行零变化探针比对与独立回读校验。\n"
            "是否立即执行写入？"
        )
        if not confirm:
            return

        self._set_busy(True)
        self.progress_bar.start(10)
        self.log("正在执行原子写入事务…")

        def worker():
            try:
                res = self.backend.apply_features(en, ftp, progress=self.log)
                self.log("写入完成！")
                self.after(0, lambda: messagebox.showinfo(
                    "写入成功",
                    "所选功能已成功写入相机并通过回读校验！\n\n"
                    "【验收步骤】\n"
                    "1. 安全断开 USB 连接\n"
                    "2. 拔下相机数据线并关闭相机电源\n"
                    "3. 等待约 30 秒至 1 分钟后重新开机\n"
                    "4. 相机菜单需分别验证英文与 FTP：候选字节写入成功不代表 FTP 已能传图！"
                ))
            except Exception as exc:
                self.log(f"写入失败: {exc}")
                self.after(0, lambda: messagebox.showerror("写入异常", f"操作未能完成: {exc}"))
            finally:
                self.after(0, self._finish_task)

        threading.Thread(target=worker, daemon=True).start()

    # --- Page 6: Restore ---
    def _build_restore_page(self):
        page = ttk.Frame(self.pages_container)
        self.pages["restore"] = page

        card = ttk.Frame(page, style="Card.TFrame", padding=20)
        card.pack(fill="both", expand=True, pady=10)

        title = ttk.Label(card, text="一键无损还原出厂状态", style="CardTitle.TLabel")
        title.pack(anchor="w", pady=(0, 6))

        desc = ttk.Label(
            card, text=(
                "若您希望将相机彻底恢复为未经修改的原厂状态，可在此执行一键还原。\n"
                "程序将把全部修改字段逐字节写回官方原厂预置数据，并进行逐块回读校验。"
            ),
            style="CardMuted.TLabel", justify="left"
        )
        desc.pack(anchor="w", pady=(0, 20))

        self.restore_btn = ttk.Button(
            card, text="🔄 一键出厂无损还原", style="Danger.TButton",
            command=self._start_restore_task
        )
        self.restore_btn.pack(anchor="w")

    def _start_restore_task(self):
        if self.busy:
            return
        confirm = messagebox.askyesno(
            "确认还原出厂",
            "此操作将把所有修改字段（FTP、按键支持、英文语言门禁）恢复为官方出厂预置状态。\n\n"
            "是否确认继续？"
        )
        if not confirm:
            return

        self._set_busy(True)
        self.progress_bar.start(10)
        self.log("正在执行出厂还原事务…")

        def worker():
            try:
                res = self.backend.restore_factory(progress=self.log)
                self.log("还原完成！")
                self.after(0, lambda: messagebox.showinfo(
                    "还原完成",
                    "相机已成功恢复为 100% 出厂原始状态！\n\n"
                    "请安全断开数据线并重启相机。"
                ))
            except Exception as exc:
                self.log(f"还原失败: {exc}")
                self.after(0, lambda: messagebox.showerror("还原异常", str(exc)))
            finally:
                self.after(0, self._finish_task)

        threading.Thread(target=worker, daemon=True).start()

    def _set_busy(self, busy: bool):
        self.busy = busy
        state = "disabled" if busy else "normal"
        self.inspect_btn.configure(state=state)
        self.apply_btn.configure(state=state)
        self.restore_btn.configure(state=state)

    def _finish_task(self):
        self.progress_bar.stop()
        self._set_busy(False)


def main():
    app = SonyCustomizerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
