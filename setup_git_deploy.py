#!/usr/bin/env python3
"""
Git仓库部署配置助手
自动配置Git仓库部署，包括Cursor MCP设置
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path

class GitDeploySetup:
    def __init__(self):
        self.system = platform.system().lower()
        self.project_dir = Path(__file__).parent
        self.home_dir = Path.home()
        
    def check_git_repo(self):
        """检查是否在Git仓库中"""
        try:
            result = subprocess.run(['git', 'status'], 
                                  capture_output=True, text=True, cwd=self.project_dir)
            if result.returncode == 0:
                print("✅ 检测到Git仓库")
                return True
            else:
                print("❌ 当前目录不是Git仓库")
                return False
        except FileNotFoundError:
            print("❌ 未找到Git，请先安装Git")
            return False
    
    def get_git_remote_url(self):
        """获取Git远程仓库URL"""
        try:
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  capture_output=True, text=True, cwd=self.project_dir)
            if result.returncode == 0:
                url = result.stdout.strip()
                print(f"📍 Git仓库地址: {url}")
                return url
            else:
                print("⚠️ 未找到远程仓库地址")
                return None
        except:
            return None
    
    def setup_cursor_mcp(self):
        """配置Cursor MCP设置"""
        print("🔧 配置Cursor MCP设置...")
        
        # 确定Cursor配置目录
        if self.system == "windows":
            cursor_config_dir = self.home_dir / "AppData" / "Roaming" / "Cursor" / "User"
        elif self.system == "darwin":  # macOS
            cursor_config_dir = self.home_dir / "Library" / "Application Support" / "Cursor" / "User"
        else:  # Linux
            cursor_config_dir = self.home_dir / ".config" / "Cursor" / "User"
        
        # 创建配置目录
        cursor_config_dir.mkdir(parents=True, exist_ok=True)
        
        # MCP配置文件路径
        mcp_config_file = cursor_config_dir / "mcp_settings.json"
        
        # 获取当前项目路径
        main_py_path = str(self.project_dir / "main.py")
        
        # MCP配置内容
        mcp_config = {
            "mcpServers": {
                "performance-analyzer": {
                    "command": "python",
                    "args": [main_py_path],
                    "env": {},
                    "description": "移动应用性能监控数据分析"
                }
            }
        }
        
        # 如果配置文件已存在，合并配置
        if mcp_config_file.exists():
            try:
                with open(mcp_config_file, 'r', encoding='utf-8') as f:
                    existing_config = json.load(f)
                
                if "mcpServers" not in existing_config:
                    existing_config["mcpServers"] = {}
                
                existing_config["mcpServers"]["performance-analyzer"] = mcp_config["mcpServers"]["performance-analyzer"]
                mcp_config = existing_config
                
                print("✅ 合并现有MCP配置")
            except:
                print("⚠️ 现有配置文件格式错误，将创建新配置")
        
        # 写入配置文件
        with open(mcp_config_file, 'w', encoding='utf-8') as f:
            json.dump(mcp_config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Cursor MCP配置已保存到: {mcp_config_file}")
        return mcp_config_file
    
    def create_deployment_scripts(self):
        """创建部署相关脚本"""
        print("📝 创建部署脚本...")
        
        # 更新脚本
        update_script_content = """#!/bin/bash
# 更新MCP服务器脚本

echo "🔄 更新MCP性能分析服务器..."

# 检查Git仓库
if [ ! -d ".git" ]; then
    echo "❌ 当前目录不是Git仓库"
    exit 1
fi

# 拉取最新代码
echo "📥 拉取最新代码..."
git pull origin main

# 检查是否有更新
if [ $? -eq 0 ]; then
    echo "✅ 代码更新成功"
else
    echo "❌ 代码更新失败"
    exit 1
fi

# 更新依赖
if [ -f "requirements.txt" ]; then
    echo "📦 更新Python依赖..."
    pip install --upgrade -r requirements.txt
fi

echo "🎉 更新完成！"
echo "💡 重启MCP服务器以应用更新"
"""
        
        update_script_file = self.project_dir / "update.sh"
        with open(update_script_file, 'w', encoding='utf-8') as f:
            f.write(update_script_content)
        
        if self.system != "windows":
            os.chmod(update_script_file, 0o755)
        
        # Windows批处理文件
        if self.system == "windows":
            update_bat_content = """@echo off
REM 更新MCP服务器脚本

echo 🔄 更新MCP性能分析服务器...

REM 检查Git仓库
if not exist ".git" (
    echo ❌ 当前目录不是Git仓库
    pause
    exit /b 1
)

REM 拉取最新代码
echo 📥 拉取最新代码...
git pull origin main

if errorlevel 1 (
    echo ❌ 代码更新失败
    pause
    exit /b 1
)

echo ✅ 代码更新成功

REM 更新依赖
if exist "requirements.txt" (
    echo 📦 更新Python依赖...
    pip install --upgrade -r requirements.txt
)

echo 🎉 更新完成！
echo 💡 重启MCP服务器以应用更新
pause
"""
            update_bat_file = self.project_dir / "update.bat"
            with open(update_bat_file, 'w', encoding='utf-8') as f:
                f.write(update_bat_content)
        
        print("✅ 部署脚本创建完成")
    
    def create_quick_start_guide(self):
        """创建快速开始指南"""
        git_url = self.get_git_remote_url()
        
        if not git_url:
            git_url = "https://github.com/your-username/mcp_demo.git"
        
        quick_start_content = f"""# 🚀 快速开始指南

## 一键部署到新电脑

### 方法1: 自动部署脚本
```bash
# Linux/macOS
curl -sSL {git_url.replace('.git', '')}/raw/main/git_deploy.sh | bash

# Windows PowerShell
iwr -useb {git_url.replace('.git', '')}/raw/main/git_deploy.sh | iex
```

### 方法2: 手动部署
```bash
# 1. 克隆仓库
git clone {git_url}
cd {self.project_dir.name}

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置MCP
python setup_git_deploy.py

# 4. 启动服务器
python main.py --network
```

## 更新现有部署

```bash
# 使用更新脚本
./update.sh          # Linux/macOS
update.bat           # Windows

# 或手动更新
git pull origin main
pip install --upgrade -r requirements.txt
```

## Cursor配置

MCP配置已自动添加到Cursor，重启Cursor即可使用。

配置文件位置:
- Windows: `%APPDATA%\\Cursor\\User\\mcp_settings.json`
- macOS: `~/Library/Application Support/Cursor/User/mcp_settings.json`
- Linux: `~/.config/Cursor/User/mcp_settings.json`

## 网络访问配置

### 服务器端
```bash
python main.py --network
# 记录显示的IP地址
```

### 客户端Cursor配置
```json
{{
  "mcpServers": {{
    "performance-analyzer": {{
      "command": "python",
      "args": ["-c", "import urllib.request; exec(urllib.request.urlopen('http://服务器IP:8000/mcp').read())"],
      "env": {{}}
    }}
  }}
}}
```

## 故障排除

1. **Git克隆失败**: 检查网络连接和仓库权限
2. **依赖安装失败**: 升级pip或使用国内镜像
3. **MCP连接失败**: 重启Cursor，检查配置文件
4. **端口被占用**: 使用 `--port` 参数指定其他端口

## 技术支持

- 仓库地址: {git_url}
- 问题反馈: 在GitHub仓库创建Issue
- 文档: 查看项目README.md
"""
        
        quick_start_file = self.project_dir / "QUICK_START.md"
        with open(quick_start_file, 'w', encoding='utf-8') as f:
            f.write(quick_start_content)
        
        print(f"✅ 快速开始指南已创建: {quick_start_file}")
    
    def run_setup(self):
        """运行完整设置流程"""
        print("🚀 Git仓库部署配置助手")
        print("=" * 40)
        
        # 检查Git仓库
        if not self.check_git_repo():
            print("\n💡 建议:")
            print("1. 初始化Git仓库: git init")
            print("2. 添加远程仓库: git remote add origin <repo-url>")
            print("3. 提交代码: git add . && git commit -m 'Initial commit'")
            print("4. 推送代码: git push -u origin main")
            return False
        
        try:
            # 配置Cursor MCP
            mcp_config_file = self.setup_cursor_mcp()
            
            # 创建部署脚本
            self.create_deployment_scripts()
            
            # 创建快速开始指南
            self.create_quick_start_guide()
            
            print("\n🎉 Git仓库部署配置完成！")
            print("=" * 40)
            print(f"📁 项目目录: {self.project_dir}")
            print(f"⚙️ MCP配置: {mcp_config_file}")
            print("📖 快速指南: QUICK_START.md")
            
            print("\n🔄 下一步:")
            print("1. 重启Cursor以加载MCP配置")
            print("2. 运行 'python main.py --network' 启动服务器")
            print("3. 在其他电脑上使用 'git clone' 部署")
            
            # 获取Git仓库信息
            git_url = self.get_git_remote_url()
            if git_url:
                print(f"\n🌐 分享给其他人的部署命令:")
                print(f"git clone {git_url} && cd {self.project_dir.name} && pip install -r requirements.txt && python setup_git_deploy.py")
            
            return True
            
        except Exception as e:
            print(f"❌ 配置失败: {e}")
            return False

def main():
    setup = GitDeploySetup()
    success = setup.run_setup()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 