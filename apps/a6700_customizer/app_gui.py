"""Sony α6700 极简定制工具 (Ver 2.00) - Desktop GUI.

Dedicated interface focusing exclusively on:
1. Full FTP Support (including Playback Gallery Custom Key Action 0x0817 fix)
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
from apps.a6700_customizer.targets import (
    ALL_FTP_TARGETS,
    INTERLEAVED_PRESERVED_BYTES,
    LOGICAL_CHANGED_BYTES,
    LOGICAL_TARGET_COUNT,
    PHYSICAL_SPANS_COUNT,
    PHYSICAL_WRITE_FOOTPRINT_BYTES,
    TARGET_ENGLISH,
    build_target_spans,
)

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
        self.unresolved_journal = self.backend.get_unresolved_journal()
        self.reconciliation_result = None

        self._init_styles()
        self._build_layout()
        self._render_recovery_journal()
        self.show_page("reconcile" if self.unresolved_journal else "notice")

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
            ("reconcile", "⚠️ 7. 会话恢复与对账"),
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
            badge_frame, text="🛡️ R4 固件段级分段事务\n前置全量快照 · 逐字节回读校验",
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
        self._build_reconcile_page()

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
            "restore": "6. 有条件出厂还原",
            "reconcile": "7. 会话恢复与只读对账",
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
            "本工具针对两项相机原生功能：\n"
            "  1. FTP 菜单与动作：网络配置、相册回放「选择传输」菜单树（81 处权限）及自定义键 Action 0x0817。\n"
            "     菜单与动作绑定已经静态分析和真机菜单回读验证；端到端网络长效传输仍属持续验证。\n"
            "  2. 原生英文菜单：开放 English 选项，使用相机原生英文资源，不改写中文字库。\n\n"
            "【R4 固件程序修改安全准则】\n"
            "● 仅支持 Sony ILCE-6700 (α6700) 国行版、固件 Ver. 2.00 的精确目标。\n"
            "● 修改范围仅涉及 /usr/lib/appFw.so 中已审查的权限位与语言断言，不包含内核、bootloader、传感器标定或射频配置。\n"
            "● 写入前保存完整分段快照并执行零变化探针；超时或断连立即锁定 NEEDS_REVIEW，禁止盲目重试。\n"
            "● 有条件出厂还原依赖 USB 服务模式正常通信；硬件损坏或固件不可访问时，软件层恢复无法保证。"
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
        if self.busy:
            return
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
        if self.busy:
            return
        res = self.backend.check_driver()
        if res.get("ok"):
            messagebox.showinfo(
                "驱动已就绪",
                "当前 WinUSB 驱动已经处于就绪状态（已成功关联 WinUSB 服务）！\n\n"
                "无需重复安装，您可以直接点击「下一步：相机准备」或进入「4. 检测与备份」。"
            )
            return

        self._set_busy(True)
        self.progress_bar.start(10)
        self.log("正在请求管理员权限安装 WinUSB 驱动…")
        def worker():
            try:
                self.backend.install_driver(progress=self.log)
                self.log("驱动安装完成，正在更新状态…")
                self.after(1000, self._do_driver_scan)
            except Exception as exc:
                self.log(f"驱动安装异常: {exc}")
                self.after(0, lambda exc=exc: messagebox.showerror("安装驱动错误", str(exc)))
            finally:
                self.after(0, self._finish_task)

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
                self.after(0, lambda exc=exc: messagebox.showerror("检测失败", str(exc)))
            finally:
                self.after(0, self._finish_task)

        threading.Thread(target=worker, daemon=True).start()

    def _render_inspection_success(self, res: dict, backup_path: Path):
        en_str = "已解锁 (Patched)" if res["english_status"] == "PATCHED" else "原始锁定 (Stock)"
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
            f"● 完整 FTP 传输状态: {ftp_str}\n"
            f"● 自动快照保存位置: {backup_path.name}"
        )
        self.inspect_info_lbl.configure(text=msg)
        self.set_status("相机检测通过", "#4ade80")

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

        card_ftp = ttk.Frame(page, style="Card.TFrame", padding=14)
        card_ftp.pack(fill="x", pady=(0, 10))

        self.var_ftp = tk.BooleanVar(value=True)
        chk_ftp = ttk.Checkbutton(
            card_ftp, text="FTP 网络菜单 + 相册选择传输菜单 + 回放自定义键动作",
            variable=self.var_ftp
        )
        chk_ftp.pack(anchor="w", pady=(0, 6))

        ftp_desc = (
            "开启 Network 菜单 0x05a5..0x05b0、Playback「选择传输」菜单树（81 处权限），"
            "并解锁 Action 0x0817 (FTP_TRANSFER) 自定义键绑定。\n"
            "证据边界：固件静态分析与真机菜单回读已验证；端到端实际网络长效传输稳定性仍在持续验证。"
        )
        ttk.Label(
            card_ftp, text=ftp_desc, style="CardMuted.TLabel", justify="left", wraplength=650
        ).pack(anchor="w")

        self.ftp_upgrade_banner = tk.Label(
            card_ftp,
            text="💡 检测到基础网络 FTP 已开启。本次仅补齐相册菜单、按键动作与所选语言断言；\n工具不主动修改 Backup NVRAM 中的 FTP 服务器或 Wi-Fi 配置。",
            font=(FONT_FAMILY, 9), bg="#042f2e", fg="#2dd4bf",
            padx=10, pady=8, justify="left", bd=1, relief="solid"
        )

        card_en = ttk.Frame(page, style="Card.TFrame", padding=14)
        card_en.pack(fill="x", pady=(0, 10))

        self.var_en = tk.BooleanVar(value=True)
        chk_en = ttk.Checkbutton(
            card_en, text="原生英文语言菜单解锁 (True Native English Language)",
            variable=self.var_en
        )
        chk_en.pack(anchor="w", pady=(0, 6))

        en_desc = (
            "通过 english_predicate (0x023080f8) 开放 English 选项；选择后由相机原生机制"
            "持久化为 Bank 0 英文资源，不改写中文字库。逻辑修改为 4 字节。"
        )
        ttk.Label(card_en, text=en_desc, style="CardMuted.TLabel", justify="left", wraplength=650).pack(anchor="w")

        metrics_card = ttk.Frame(page, style="Card.TFrame", padding=14)
        metrics_card.pack(fill="x", pady=(0, 6))
        ttk.Label(
            metrics_card, text="📊 写入范围与足迹披露 (Truth in Labeling)", style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 6))
        metrics_text = (
            f"逻辑修改目标：{LOGICAL_CHANGED_BYTES} 字节（{LOGICAL_TARGET_COUNT} 处固件权限与语言断言）\n"
            f"物理写入跨度：{PHYSICAL_SPANS_COUNT} 个固件段，共 {PHYSICAL_WRITE_FOOTPRINT_BYTES:,} 字节 "
            f"(~{PHYSICAL_WRITE_FOOTPRINT_BYTES / 1024:.1f} KiB，两项全选时的计划上限)\n"
            f"安全说明：顺序分段事务写入（各段独立，单段 <= 128 KiB）；段内其余 "
            f"{INTERLEAVED_PRESERVED_BYTES:,} 字节来自只读预读并原样保留，写入前后均执行全段逐字节比对。"
        )
        ttk.Label(
            metrics_card, text=metrics_text, style="CardMuted.TLabel", justify="left", wraplength=650
        ).pack(anchor="w")

        self.apply_btn = ttk.Button(
            page, text="⚡ 写入所选功能至相机", style="Success.TButton",
            command=self._start_apply_task
        )
        self.apply_btn.pack(anchor="e", pady=6)

    def _start_apply_task(self):
        if self.busy:
            return
        en = self.var_en.get()
        ftp = self.var_ftp.get()
        if not en and not ftp:
            messagebox.showwarning("提示", "请至少勾选一项功能！")
            return
        if self.backend.get_unresolved_journal():
            self._reload_recovery_journal()
            self.show_page("reconcile")
            messagebox.showwarning("安全锁定", "存在未闭环写入会话，请先完成只读对账。")
            return

        selected_targets = ([TARGET_ENGLISH] if en else []) + (ALL_FTP_TARGETS if ftp else [])
        selected_spans = build_target_spans(selected_targets)
        logical_bytes = sum(len(t.patched) for t in selected_targets if t.preimage != t.patched)
        physical_bytes = sum(span.length for span in selected_spans)
        confirm = messagebox.askyesno(
            "确认 R4 固件分段写入",
            f"目标文件：/usr/lib/appFw.so\n"
            f"逻辑修改：{logical_bytes} 字节 / {len(selected_targets)} 处目标\n"
            f"计划物理足迹：{len(selected_spans)} 段 / {physical_bytes:,} 字节（已是目标值的段会跳过）\n\n"
            f"● 英文菜单解锁：{'是' if en else '否'}\n"
            f"● FTP 菜单与动作：{'是' if ftp else '否'}\n\n"
            "写入前保存完整分段快照并执行零变化探针；每段写入后执行全段逐字节回读。\n"
            "超时、断连或不匹配将立即锁定 NEEDS_REVIEW，不会自动重试或自动回退。\n"
            "是否明确批准本次写入？"
        )
        if not confirm:
            return

        self._set_busy(True)
        self.progress_bar.start(10)
        self.log("正在执行顺序分段事务写入（各段独立写入与校验）…")

        def worker():
            try:
                self.backend.apply_features(en, ftp, progress=self.log)
                self.log("所选目标状态确认完成；实际写入段已通过回读校验。")
                self.after(0, lambda: messagebox.showinfo(
                    "目标状态确认完成",
                    "所选功能字段均已达到目标状态；实际写入段已通过全段回读校验，未修改段已跳过。\n\n"
                    "【验收步骤】\n"
                    "1. 安全断开 USB 连接并关闭相机电源\n"
                    "2. 等待约 30 秒至 1 分钟后重新开机\n"
                    "3. 在相机菜单中验证 FTP 菜单、动作绑定与英文选项\n\n"
                    "菜单验证不等同于端到端网络长效传输验证。"
                ))
            except Exception as exc:
                self.log(f"写入中断: {exc}")
                self.after(0, self._handle_operation_error, "写入异常", str(exc))
            finally:
                self.after(0, self._finish_task)

        threading.Thread(target=worker, daemon=True).start()

    # --- Page 6: Restore ---
    def _build_restore_page(self):
        page = ttk.Frame(self.pages_container)
        self.pages["restore"] = page

        card = ttk.Frame(page, style="Card.TFrame", padding=20)
        card.pack(fill="both", expand=True, pady=10)

        title = ttk.Label(card, text="有条件出厂还原", style="CardTitle.TLabel")
        title.pack(anchor="w", pady=(0, 6))

        desc = ttk.Label(
            card, text=(
                "将本工具管理的 FTP、按键与英文语言字段恢复为 Ver. 2.00 原厂预置值，"
                "并按 7 个独立固件段执行全段回读校验。\n"
                "恢复依赖 USB 服务模式保持正常通信；硬件损坏或固件不可访问时，无法保证软件层恢复。"
            ),
            style="CardMuted.TLabel", justify="left", wraplength=650
        )
        desc.pack(anchor="w", pady=(0, 20))

        self.restore_btn = ttk.Button(
            card, text="🔄 还原管理字段为原厂预置值", style="Danger.TButton",
            command=self._start_restore_task
        )
        self.restore_btn.pack(anchor="w")

    def _start_restore_task(self):
        if self.busy:
            return
        if self.backend.get_unresolved_journal():
            self._reload_recovery_journal()
            self.show_page("reconcile")
            messagebox.showwarning("安全锁定", "存在未闭环写入会话，请先完成只读对账。")
            return
        confirm = messagebox.askyesno(
            "确认 R4 原厂字段还原",
            "此操作将按 7 个独立固件段，把 FTP、按键支持、英文语言门禁恢复为官方 Ver. 2.00 预置值。\n"
            "每段写入前保存完整快照，写入后执行全段逐字节回读；异常时立即锁定，不自动重试。\n\n"
            "是否明确批准本次还原写入？"
        )
        if not confirm:
            return

        self._set_busy(True)
        self.progress_bar.start(10)
        self.log("正在执行原厂字段顺序分段还原事务…")

        def worker():
            try:
                self.backend.restore_factory(progress=self.log)
                self.log("原厂目标状态确认完成；实际恢复段已通过回读校验。")
                self.after(0, lambda: messagebox.showinfo(
                    "原厂目标状态确认完成",
                    "本工具管理的字段均已达到原厂预置状态；实际恢复段已通过全段回读校验，未修改段已跳过。\n\n"
                    "请安全断开数据线并重启相机。此结果不代表硬件故障场景下的恢复保证。"
                ))
            except Exception as exc:
                self.log(f"还原中断: {exc}")
                self.after(0, self._handle_operation_error, "还原异常", str(exc))
            finally:
                self.after(0, self._finish_task)

        threading.Thread(target=worker, daemon=True).start()

    # --- Page 7: Interrupted session reconciliation ---
    def _build_reconcile_page(self):
        page = ttk.Frame(self.pages_container)
        self.pages["reconcile"] = page

        card = ttk.Frame(page, style="Card.TFrame", padding=16)
        card.pack(fill="both", expand=True, pady=6)

        self.recovery_warning_lbl = tk.Label(
            card, text="", font=(FONT_FAMILY, 10, "bold"), bg="#451a03", fg="#fbbf24",
            padx=12, pady=10, justify="left", wraplength=650
        )
        self.recovery_warning_lbl.pack(fill="x", pady=(0, 10))

        self.recovery_session_lbl = ttk.Label(
            card, text="", style="CardMuted.TLabel", justify="left", wraplength=650
        )
        self.recovery_session_lbl.pack(anchor="w", pady=(0, 10))

        ttk.Label(
            card,
            text="先连接相机并执行只读对账。扫描完成前禁止回退或续写；任何写操作都需再次明确确认。",
            style="CardMuted.TLabel", justify="left", wraplength=650
        ).pack(anchor="w", pady=(0, 10))

        self.recovery_findings_frame = ttk.Frame(card, style="Card.TFrame")
        self.recovery_findings_frame.pack(fill="both", expand=True, pady=(0, 10))

        btn_row = ttk.Frame(card, style="Card.TFrame")
        btn_row.pack(fill="x")
        self.reconcile_scan_btn = ttk.Button(
            btn_row, text="🔍 开始只读对账扫描", style="Primary.TButton",
            command=self._start_reconcile_task
        )
        self.reconcile_scan_btn.pack(side="left", padx=(0, 8))
        self.rollback_session_btn = ttk.Button(
            btn_row, text="🔄 回退全部修改段", style="Danger.TButton",
            state="disabled", command=self._start_rollback_task
        )
        self.rollback_session_btn.pack(side="left", padx=(0, 8))
        self.resume_session_btn = ttk.Button(
            btn_row, text="▶️ 续写未完成段", style="Success.TButton",
            state="disabled", command=self._start_resume_task
        )
        self.resume_session_btn.pack(side="left")

    def _clear_recovery_findings(self):
        for child in self.recovery_findings_frame.winfo_children():
            child.destroy()

    def _render_recovery_journal(self):
        self._clear_recovery_findings()
        if not self.unresolved_journal:
            self.reconciliation_result = None
            self.recovery_warning_lbl.configure(
                text="✅ 当前没有未闭环的写入会话。", bg="#052e16", fg="#4ade80"
            )
            self.recovery_session_lbl.configure(
                text="正常功能写入或原厂字段还原完成后，会话才会闭环。若发生断连，请重新打开本页面。"
            )
        else:
            try:
                meta = self.unresolved_journal.read_meta()
            except (OSError, ValueError, TypeError) as exc:
                meta = {
                    "session_id": self.unresolved_journal.session_dir.name,
                    "status": "METADATA_ERROR",
                    "created_at": f"日志元数据无法读取: {exc}",
                }
            self.recovery_warning_lbl.configure(
                text=(
                    "⚠️ 检测到上次写入会话未正常闭环或被中断 "
                    f"(状态: {meta.get('status', 'UNKNOWN')})"
                ),
                bg="#451a03", fg="#fbbf24"
            )
            self.recovery_session_lbl.configure(
                text=(
                    f"session_id: {meta.get('session_id', 'UNKNOWN')}\n"
                    f"created_at: {meta.get('created_at', 'UNKNOWN')}  |  mode: {meta.get('mode', 'UNKNOWN')}  |  "
                    f"spans: {meta.get('span_count', 'UNKNOWN')}\n"
                    "原始分段快照保存在本机会话目录；请勿删除或手工修改 journal/bin 文件。"
                )
            )
        self._update_recovery_buttons()

    def _reload_recovery_journal(self):
        self.unresolved_journal = self.backend.get_unresolved_journal()
        self.reconciliation_result = None
        self._render_recovery_journal()

    def _update_recovery_buttons(self):
        if not hasattr(self, "reconcile_scan_btn"):
            return
        has_journal = self.unresolved_journal is not None
        self.reconcile_scan_btn.configure(
            state="normal" if has_journal and not self.busy else "disabled"
        )
        result = self.reconciliation_result
        can_rollback = bool(result and result.get("can_rollback"))
        can_resume = bool(result and result.get("can_resume"))
        self.rollback_session_btn.configure(
            state="normal" if has_journal and can_rollback and not self.busy else "disabled"
        )
        self.resume_session_btn.configure(
            state="normal" if has_journal and can_resume and not self.busy else "disabled"
        )

    def _start_reconcile_task(self):
        if self.busy or not self.unresolved_journal:
            return
        journal = self.unresolved_journal
        self._set_busy(True)
        self.progress_bar.start(10)
        self.log("开始只读对账；此步骤不发送固件写入命令…")

        def worker():
            try:
                result = self.backend.reconcile_device(journal=journal, progress=self.log)
                self.after(0, self._render_reconciliation, result)
            except Exception as exc:
                self.log(f"只读对账失败: {exc}")
                self.after(0, self._handle_operation_error, "只读对账失败", str(exc))
            finally:
                self.after(0, self._finish_task)

        threading.Thread(target=worker, daemon=True).start()

    def _render_reconciliation(self, result):
        self.reconciliation_result = result
        self._clear_recovery_findings()
        colors = {
            "UNTOUCHED_STOCK": "#4ade80",
            "FULLY_PATCHED": "#60a5fa",
            "CORRUPTED_OR_PARTIAL": "#f87171",
        }
        for finding in result.get("findings", []):
            classification = finding.get("classification", "UNKNOWN")
            row = tk.Label(
                self.recovery_findings_frame,
                text=(
                    f"段 {finding.get('span_index')}: 0x{finding.get('offset', 0):08x}  |  "
                    f"{finding.get('length', 0):,} B  |  {classification}  |  {finding.get('status_text', '')}"
                ),
                font=(FONT_FAMILY, 9), bg=BG_CARD, fg=colors.get(classification, "#f87171"),
                justify="left", anchor="w"
            )
            row.pack(fill="x", pady=2)
        self.recovery_warning_lbl.configure(
            text=(
                f"对账完成：写前状态 {result.get('untouched_stock', 0)} 段，"
                f"目标状态 {result.get('fully_patched', 0)} 段，"
                f"异常/部分 {result.get('corrupted_or_partial', 0)} 段。"
            ),
            bg="#172554" if result.get("corrupted_or_partial", 0) == 0 else "#450a0a",
            fg="#93c5fd" if result.get("corrupted_or_partial", 0) == 0 else "#fca5a5"
        )
        self.set_status("只读对账完成", "#60a5fa")
        self._update_recovery_buttons()

    def _start_rollback_task(self):
        if self.busy or not self.unresolved_journal or not self.reconciliation_result:
            return
        if not self.reconciliation_result.get("can_rollback"):
            return
        count = self.reconciliation_result.get("total_spans", 0)
        confirm = messagebox.askyesno(
            "确认回退中断会话",
            f"将依据刚才的只读对账，把 {count} 个会话段中的已修改/异常段恢复至写前原始 .bin 快照。\n"
            "未改动段跳过；每段写入后执行全段逐字节回读。若对账后数据变化，将在写入前停止。\n"
            "此操作仍依赖 USB 服务模式正常通信，不是无条件恢复保证。\n\n"
            "是否明确批准本次回退写入？"
        )
        if not confirm:
            return
        journal = self.unresolved_journal
        reconciliation = self.reconciliation_result
        self._set_busy(True)
        self.progress_bar.start(10)

        def worker():
            try:
                self.backend.rollback_interrupted_session(
                    journal=journal, reconciliation=reconciliation, progress=self.log
                )
                self.after(0, self._finish_recovery, "回退")
            except Exception as exc:
                self.log(f"会话回退中断: {exc}")
                self.after(0, self._handle_operation_error, "会话回退异常", str(exc))
            finally:
                self.after(0, self._finish_task)

        threading.Thread(target=worker, daemon=True).start()

    def _start_resume_task(self):
        if self.busy or not self.unresolved_journal or not self.reconciliation_result:
            return
        if not self.reconciliation_result.get("can_resume"):
            messagebox.showwarning("禁止续写", "存在异常或部分写入段，请先重新对账并选择回退。")
            return
        confirm = messagebox.askyesno(
            "确认续写中断会话",
            "将依据刚才的只读对账，仅续写仍处于写前状态的段；已达到目标状态的段跳过。\n"
            "若任何段在对账后变化，将在写入前停止；每段写入后执行全段逐字节回读。\n"
            "超时或断连会立即锁定 NEEDS_REVIEW，不自动重试。\n\n"
            "是否明确批准本次续写？"
        )
        if not confirm:
            return
        journal = self.unresolved_journal
        reconciliation = self.reconciliation_result
        self._set_busy(True)
        self.progress_bar.start(10)

        def worker():
            try:
                self.backend.resume_interrupted_session(
                    journal=journal, reconciliation=reconciliation, progress=self.log
                )
                self.after(0, self._finish_recovery, "续写")
            except Exception as exc:
                self.log(f"会话续写中断: {exc}")
                self.after(0, self._handle_operation_error, "会话续写异常", str(exc))
            finally:
                self.after(0, self._finish_task)

        threading.Thread(target=worker, daemon=True).start()

    def _finish_recovery(self, operation):
        self._reload_recovery_journal()
        self.set_status("恢复会话已闭环", "#4ade80")
        messagebox.showinfo(
            f"{operation}完成",
            f"中断会话的{operation}操作已完成，相关段均通过全段逐字节回读校验，会话已闭环。\n"
            "请安全断开 USB 并重启相机后验证菜单状态。"
        )

    def _handle_operation_error(self, title, message):
        self._reload_recovery_journal()
        if self.unresolved_journal:
            self.show_page("reconcile")
            self.set_status("会话需要只读对账", "#f87171")
        messagebox.showerror(title, message)

    def _set_busy(self, busy: bool):
        self.busy = busy
        state = "disabled" if busy else "normal"
        self.driver_scan_btn.configure(state=state)
        self.driver_install_btn.configure(state=state)
        self.inspect_btn.configure(state=state)
        self.apply_btn.configure(state=state)
        self.restore_btn.configure(state=state)
        self._update_recovery_buttons()

    def _finish_task(self):
        self.progress_bar.stop()
        self._set_busy(False)


def main():
    app = SonyCustomizerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
