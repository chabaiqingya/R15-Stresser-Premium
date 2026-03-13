import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from engine import R15Engine
from config_manager import ConfigManager
from task_manager import TaskManager
from ui_components import SidebarFrame, LogFrame  # 引入美化后的 UI 组件

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class R15StresserApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("R15 Stresser Premium")
        self.geometry("900x650")

        # 1. 初始化后台逻辑组件
        self.config_manager = ConfigManager()
        self.benchmark_paths = self.config_manager.load()
        self.engine = R15Engine(self.add_log_relay)
        self.task_manager = TaskManager(self.engine, self.add_log_relay, self.reset_ui_relay)

        # 2. 组装 UI 界面
        self.setup_layout()

        # === 新增：监听窗口关闭事件 ===
        # 这一行告诉程序：当用户点击右上角的 [X] 时，去执行 self.on_closing 方法
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """处理窗口关闭时的逻辑"""
        if self.engine.is_running:
            # 如果压测引擎正在运行，弹出二次确认
            if messagebox.askokcancel("退出", "压测正在进行中，确定要停止并退出吗？"):
                self.engine.stop()  # 停止子线程中的 Popen 进程
                self.destroy()  # 销毁主窗口并完全退出程序
        else:
            # 如果没有在测试，直接关闭
            self.destroy()

    def setup_layout(self):
        """初始化布局和组件"""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 实例化侧边栏
        self.sidebar = SidebarFrame(
            self,
            select_path_cb=self.handle_select_path,
            toggle_test_cb=self.handle_toggle_test,
            version_change_cb=self.handle_version_change
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # 实例化主展示区
        self.main_view = LogFrame(self)
        self.main_view.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # 初始路径检查提示
        if any(self.benchmark_paths.values()):
            self.main_view.add_log("📂 已成功加载历史路径配置", "info")

    # --- 界面交互逻辑 ---

    def handle_version_change(self, choice):
        self.sidebar.path_btn.configure(text=f"选择 {choice} 路径")
        self.main_view.banner.configure(text=f"{choice} 模式就绪")
        self.main_view.add_log(f"🔄 切换测试模式为: {choice}", "info")

    def handle_select_path(self):
        choice = self.sidebar.version_option.get()
        path = filedialog.askopenfilename(title=f"选择 {choice}.exe", filetypes=[("EXE", "*.exe")])
        if path:
            self.benchmark_paths[choice] = path
            self.config_manager.save(self.benchmark_paths)
            self.main_view.add_log(f"📍 已记住 {choice} 路径: {os.path.basename(path)}", "info")

    def handle_toggle_test(self):
        if self.engine.is_running:
            self.task_manager.stop_task()
        else:
            soft_type = self.sidebar.version_option.get()
            exe_path = self.benchmark_paths.get(soft_type, "")
            loop_input = self.sidebar.loop_entry.get()

            # 调用任务管理器进行输入校验
            success, result = self.task_manager.validate_inputs(exe_path, loop_input)
            if not success:
                messagebox.showwarning("提示", result)
                return

            # 更新 UI 进入运行态
            self.sidebar.run_btn.configure(text="停止压测", fg_color="#dc3545", hover_color="#c82333")
            self.sidebar.status_indicator.configure(text="● 正在压测", text_color="#dc3545")
            self.main_view.banner.configure(text=f"正在运行 {soft_type} 测试...")
            self.main_view.log_box.configure(state="normal")
            self.main_view.log_box.delete("1.0", "end")
            self.main_view.log_box.configure(state="disabled")

            # 启动多线程压测任务
            self.task_manager.start_task(exe_path, result, soft_type)

    # --- 跨线程回调中转 ---

    def add_log_relay(self, msg, level="info"):
        """将引擎的日志传递给 UI 组件显示"""
        self.main_view.add_log(msg, level)

    def reset_ui_relay(self):
        """压测结束后，通知 UI 恢复到初始状态"""
        self.after(0, self._actual_reset)

    def _actual_reset(self):
        choice = self.sidebar.version_option.get()
        self.sidebar.run_btn.configure(text="开始压测", fg_color="#28a745", hover_color="#218838")
        self.sidebar.status_indicator.configure(text="● 准备就绪", text_color="gray")
        self.main_view.banner.configure(text=f"{choice} 模式已就绪")


if __name__ == "__main__":
    app = R15StresserApp()
    app.mainloop()