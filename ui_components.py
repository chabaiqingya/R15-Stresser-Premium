import customtkinter as ctk
import time


class SidebarFrame(ctk.CTkFrame):
    """侧边栏组件：负责所有输入和控制按钮"""

    def __init__(self, master, select_path_cb, toggle_test_cb, version_change_cb, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=220, corner_radius=0)

        # 标题/Logo
        self.logo_label = ctk.CTkLabel(self, text="R15 PREMIUM", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.pack(pady=(30, 20))

        # 路径选择按钮
        self.path_btn = ctk.CTkButton(self, text="选择 R15 路径", command=select_path_cb)
        self.path_btn.pack(pady=10, padx=20)

        # 圈数输入
        ctk.CTkLabel(self, text="设定压测圈数:", font=ctk.CTkFont(size=12)).pack(pady=(15, 0))
        self.loop_entry = ctk.CTkEntry(self, placeholder_text="100", justify="center")
        self.loop_entry.insert(0, "100")
        self.loop_entry.pack(pady=5, padx=20)

        # 版本选择
        ctk.CTkLabel(self, text="选择测试版本:", font=ctk.CTkFont(size=12)).pack(pady=(15, 0))
        self.version_option = ctk.CTkComboBox(self, values=["R15", "R23"], command=version_change_cb)
        self.version_option.set("R15")
        self.version_option.pack(pady=5, padx=20)

        # 分隔线
        ctk.CTkLabel(self, text="", height=10).pack()

        # 开始/停止按钮
        self.run_btn = ctk.CTkButton(self, text="开始压测", fg_color="#28a745", hover_color="#218838",
                                     font=ctk.CTkFont(weight="bold"), command=toggle_test_cb)
        self.run_btn.pack(pady=20, padx=20)

        # 底部状态指示灯
        self.status_indicator = ctk.CTkLabel(self, text="● 准备就绪", text_color="gray", font=ctk.CTkFont(size=11))
        self.status_indicator.pack(side="bottom", pady=20)


class LogFrame(ctk.CTkFrame):
    """主日志区域组件：负责状态显示和滚动日志"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(corner_radius=15, fg_color="transparent")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 顶部大横幅
        self.banner = ctk.CTkLabel(self, text="准备就绪", font=ctk.CTkFont(size=28, weight="bold"))
        self.banner.grid(row=0, column=0, sticky="ew", padx=20, pady=(40, 30))

        # 日志文本框
        self.log_box = ctk.CTkTextbox(self, font=("Consolas", 13), border_width=1, border_color="#333")
        self.log_box.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.log_box.configure(state="disabled")

    def add_log(self, msg, level="info"):
        timestamp = time.strftime("%H:%M:%S")
        styles = {
            "info": ("ℹ️", "#888"),
            "success": ("✅", "#28a745"),
            "error": ("❌", "#dc3545"),
            "warning": ("⚠️", "#ffc107"),
            "hint": ("💡", "#17a2b8")
        }
        prefix, color = styles.get(level, ("•", "#ccc"))

        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{timestamp}] {prefix} {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")