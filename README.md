# R15 Stresser Premium

[中文说明](#chinese-description) | [English Description](#english-description)

---<img width="599" height="470" alt="screenshot" src="https://github.com/user-attachments/assets/ce9fc05b-a64a-4992-abea-4d10947ec61e" />


<a name="chinese-description"></a>

## 中文说明

R15 Stresser Premium 是一个基于 Python 的自动化测试工具，旨在通过循环运行 Cinebench R15/R23 来验证 CPU 的稳定性。

### 功能特点
- **多版本支持**：支持 Cinebench R15 和 R23。
- **自定义循环**：自由设置测试圈数。
- **路径记忆 (New)**：自动保存并读取不同版本的程序路径，下次启动即点即用。
- **智能拦截**：自动校验输入，防止因非法圈数设定导致的程序异常。
- **安全保护**：新增窗口关闭确认逻辑，防止测试中途误触导致进程残留。

### 快速开始 (需要 Python)
1. **安装依赖库**：
   打开终端或命令行，运行以下命令（本项目仅需两个核心库）：
   ```bash
   pip install customtkinter Pillow
   ```
2. **下载本项目**：
   下载仓库源码并解压。
3. **运行程序**：
   ```bash
   python main_gui.py
   ```
4**使用建议**：

首次运行时，点击侧边栏按钮选择对应的 CINEBENCH.exe。

设定循环圈数后，点击“开始压测”即可。
### 运行 EXE (无需 Python)
如果您不希望安装 Python，可以从 **Releases** 页面下载打包好的 `.exe` 文件直接运行。

---

<a name="english-description"></a>

## English Description

R15 Stresser Premium is a Python-based automation tool designed to verify CPU stability by running Cinebench R15/R23 in continuous loops.

### Key Features
- **Multi-Version Support**: Supports both Cinebench R15 and R23.
- **Path Persistence (New)**：Automatically remembers your executable paths for a seamless experience.
- **Customizable Loops**: Set any number of stress test cycles.
- **Input Validation**: Smart checks for loop counts to ensure reliable execution.
- **Safety Closing**：Confirmation prompts on window close to prevent orphaned benchmark processes.
- **Flexible Modes**: Toggle between silent background testing or visible windows.

### Quick Start (Python Required)
1. **Install Dependencies**:
   Run the following command in your terminal (only two core libraries are required):
   ```bash
   pip install customtkinter Pillow
   ```
2. **Download Project**:
   Clone or download the source code and extract it.
3. **Run the App**:
   ```bash
   python main_gui.py
   ```

### Run as EXE (No Python Required)
If you prefer not to install Python, you can download the pre-compiled `.exe` file from the **Releases** page and run it directly.

---

## 开源协议 / License
本项目采用 [MIT License](LICENSE) 协议。 / This project is licensed under the MIT License.

## 免责声明 / Disclaimer
本工具仅供硬件稳定性测试。作者不对因使用本软件导致的任何硬件损坏承担责任。  
This tool is for stability testing only. The author is not responsible for any hardware damage caused by its use.
=======
# R15-Stresser-Premium
A Python-based automation tool for Cinebench R15/R23 loop testing, designed to catch transient load instabilities.

