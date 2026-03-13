import unittest
from task_manager import TaskManager
from config_manager import ConfigManager
import os

class ProjectTest(unittest.TestCase):
    def test_input_validation(self):
        """验证输入拦截逻辑"""
        tm = TaskManager(None, print, None)
        # 测试非法字符串
        ok, res = tm.validate_inputs("path.exe", "error_num")
        self.assertFalse(ok)
        # 测试负数
        ok, res = tm.validate_inputs("path.exe", "-1")
        self.assertFalse(ok)
        # 测试正常正整数
        ok, res = tm.validate_inputs("path.exe", "10")
        self.assertTrue(ok)
        self.assertEqual(res, 10)

    def test_config_memory(self):
        """验证路径记忆逻辑"""
        cm = ConfigManager("test_cfg.json")
        test_data = {"R15": "C:/test.exe"}
        cm.save(test_data)
        loaded = cm.load()
        self.assertEqual(loaded["R15"], "C:/test.exe")
        os.remove("test_cfg.json")

if __name__ == "__main__":
    unittest.main()