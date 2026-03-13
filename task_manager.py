import threading


class TaskManager:
    def __init__(self, engine, log_callback, ui_update_callback):
        self.engine = engine
        self.log_callback = log_callback
        self.ui_update_callback = ui_update_callback  # 用于通知 GUI 刷新状态（如恢复按钮）

    def validate_inputs(self, exe_path, loop_str):
        """验证输入是否合法"""
        if not exe_path:
            return False, "请先选择主程序路径！"

        try:
            loops = int(loop_str)
            if loops <= 0:
                return False, "测试圈数必须是大于 0 的正整数！"
        except ValueError:
            return False, "输入无效，请输入正整数作为测试圈数！"

        return True, loops

    def start_task(self, exe_path, loops, soft_type):
        """在独立线程中启动任务"""
        # 这里的 target 指向内部的执行函数
        thread = threading.Thread(
            target=self._run_task_thread,
            args=(exe_path, loops, soft_type),
            daemon=True
        )
        thread.start()

    def _run_task_thread(self, exe_path, loops, soft_type):
        """线程内部的实际执行逻辑"""
        # 调用引擎开始运行
        self.engine.run_cycle(exe_path, loops, soft_type)
        # 运行结束后，通知 GUI 恢复界面
        if self.ui_update_callback:
            self.ui_update_callback()

    def stop_task(self):
        """停止当前任务"""
        self.engine.stop()