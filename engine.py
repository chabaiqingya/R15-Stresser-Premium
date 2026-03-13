import os
import subprocess
import threading
import time
import re


class R15Engine:
    BENCHMARK_CONFIG = {
        "R15": {
            "args": ["-cb_cpux"],
            "score_regex": r"CB Score\s*[:：]\s*([\d\.]+)"
        },
        "R23": {
            "args": ["g_CinebenchCpuXTest=true", "g_CinebenchMinimumTestDuration=1"],
            "score_regex": r"Multi Core\s*[:：]\s*([\d\.]+)"
        }
    }

    def __init__(self, log_callback):
        self.log_callback = log_callback
        self.is_running = False
        self.current_process = None
        self.stop_requested = False

    # 移除了 show_window 参数
    def run_cycle(self, exe_path, loop_count, software_type="R15"):
        self.is_running = True
        self.stop_requested = False

        config = self.BENCHMARK_CONFIG.get(software_type, self.BENCHMARK_CONFIG["R15"])
        r15_dir = os.path.abspath(os.path.dirname(exe_path))
        abs_exe = os.path.abspath(exe_path)

        self.log_callback(f"📂 模式: {software_type} | 目录: {r15_dir}", "info")

        for i in range(1, loop_count + 1):
            if self.stop_requested:
                break

            self.log_callback(f"🚀 启动第 {i}/{loop_count} 圈测试...", "info")

            try:
                # 组合参数
                cmd = [abs_exe] + config["args"]

                # 强制不显示测试黑框窗口
                creationinfo = subprocess.CREATE_NO_WINDOW

                self.current_process = subprocess.Popen(
                    cmd,
                    cwd=r15_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=creationinfo
                )

                score = "Unknown"
                for line in iter(self.current_process.stdout.readline, ''):
                    if self.stop_requested:
                        break

                    # 使用配置的正则匹配分数
                    match = re.search(config["score_regex"], line, re.IGNORECASE)
                    if match:
                        score = match.group(1)
                        self.log_callback(f"✨ 第 {i} 圈完成！分数: {score} pts", "success")

                self.current_process.wait()
                status = self.current_process.returncode

                if status != 0 and not self.stop_requested:
                    self.log_callback(f"❌ 第 {i} 圈异常退出 (Code: {status})", "error")
                    if status == 3221225477:
                        self.log_callback("💡 提示: 检测到访问冲突，可能由于电压不稳或内存溢出。", "hint")

            except Exception as e:
                self.log_callback(f"‼️ 引擎运行报错: {str(e)}", "error")
                break

        self.is_running = False
        self.log_callback("🏁 所有测试流程已结束。", "info")

    def stop(self):
        self.stop_requested = True
        if self.current_process:
            self.current_process.terminate()
            self.log_callback("⚠️ 用户已手动终止测试。", "warning")