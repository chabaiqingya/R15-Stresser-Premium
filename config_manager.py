import json
import os

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        # 默认配置数据
        self.config_data = {
            "R15": "",
            "R23": ""
        }

    def load(self):
        """读取本地配置文件并返回"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    saved_paths = json.load(f)
                    if isinstance(saved_paths, dict):
                        self.config_data.update(saved_paths)
            except Exception as e:
                print(f"读取配置文件失败: {e}")
        return self.config_data

    def save(self, data):
        """保存配置到本地文件"""
        try:
            # 更新内存中的数据并写入文件
            self.config_data.update(data)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

    def get_path(self, version):
        """快捷获取某个版本的路径"""
        return self.config_data.get(version, "")