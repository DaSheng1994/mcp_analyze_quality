# 🚀 MCP性能分析服务器

> 移动应用性能监控数据智能分析工具，支持内存泄漏检测、资源监控告警

## 🎯 **如何接入使用**

### 📋 **方式一：直接使用（推荐）**

#### 1. **获取项目**
```bash
git clone https://github.com/your-username/mcp_analyze_quality.git
cd mcp_analyze_quality
```

#### 2. **安装依赖**
```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 3. **配置Cursor MCP**
在Cursor中配置MCP服务器：

**macOS/Linux:**
编辑 `~/.cursor/mcp.json`：
```json
{
  "mcpServers": {
    "performance-analyzer": {
      "command": "/path/to/your/project/.venv/bin/python",
      "args": ["/path/to/your/project/main.py"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

**Windows:**
编辑 `%USERPROFILE%\.cursor\mcp.json`：
   ```json
   {
     "mcpServers": {
       "performance-analyzer": {
      "command": "C:\\path\\to\\your\\project\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\your\\project\\main.py"],
      "cwd": "C:\\path\\to\\your\\project"
       }
     }
   }
   ```

#### 4. **重启Cursor**
完全退出并重新启动Cursor应用

#### 5. **开始使用**
在Cursor对话中输入：
```
分析这个性能数据：http://localhost:8000/meminfo.csv
```

---

### 🌐 **方式二：网络部署（多人使用）**

#### 1. **服务器端部署**
```bash
# 在服务器上部署
git clone https://github.com/your-username/mcp_analyze_quality.git
cd mcp_analyze_quality
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 启动网络服务
python main.py &
python3 -m http.server 8000 &  # 提供数据文件访问
```

#### 2. **客户端配置**
其他人只需在Cursor中配置：
```json
{
  "mcpServers": {
    "performance-analyzer": {
      "command": "python",
      "args": ["-c", "import urllib.request; import subprocess; subprocess.run(['python', '-c', urllib.request.urlopen('http://YOUR_SERVER_IP:8000/main.py').read().decode()])"],
      "env": {}
    }
  }
}
```

---

### 📦 **方式三：Docker部署（企业级）**

#### 1. **创建Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

#### 2. **构建和运行**
```bash
docker build -t mcp-analyze-quality .
docker run -d -p 8000:8000 mcp-analyze-quality
```

#### 3. **客户端配置**
```json
{
  "mcpServers": {
    "performance-analyzer": {
      "command": "docker",
      "args": ["exec", "mcp-container", "python", "/app/main.py"],
      "env": {}
    }
  }
}
```

---

## 🔧 **配置选项**

### **环境变量**
```bash
export MCP_HOST=0.0.0.0      # 监听地址
export MCP_PORT=8000         # 监听端口
export MCP_DEBUG=true        # 调试模式
```

### **命令行参数**
```bash
python main.py --help        # 查看所有选项
python main.py --port 8080   # 自定义端口
python main.py --host 0.0.0.0  # 允许外部访问
```

---

## 📊 **功能特性**

### 🔍 **智能分析**
- **内存泄漏检测**: 自动识别内存持续增长模式
- **资源监控**: 线程、文件描述符、视图数量监控  
- **性能告警**: 多级告警系统（严重/警告/信息）
- **趋势分析**: 33项性能指标深度分析

### 🚨 **告警系统**
- **内存泄漏**: 增长率>100% + 连续5周期 = 🔴 严重告警
- **Java堆**: 增长>80MB = 🔴 严重告警
- **Native堆**: 增长>500MB且无回落 = 🔴 严重告警
- **文件描述符**: 增长>100个 = 🔴 严重告警
- **视图数量**: 增长>700个 = 🔴 严重告警

---

## 💡 **使用示例**

### **分析CSV性能数据**
```
# 在Cursor中直接使用MCP工具
分析这个性能数据：http://your-server:8000/meminfo.csv

# 或分析本地文件
分析这个文件的性能数据：/path/to/meminfo.csv
```

### **示例输出**
```json
{
  "系统健康状态": "🔴 严重",
  "严重告警": [
    "🚨 严重内存泄漏风险：内存持续大幅增长，建议立即检查",
    "🚨 Java堆内存增长严重超标：增长114.5MB，建议检查内存泄漏"
  ],
  "关键指标": {
    "内存使用": {
      "初始值": "698,126 KB",
      "最终值": "1,095,184 KB", 
      "峰值": "1,429,966 KB",
      "变化": "+56.9%"
    }
  },
  "内存泄漏分析": {
    "总体增长率": "108.6%",
    "连续增长周期": 5,
    "风险等级": "🔴 极高"
  }
}
```

---

## 🛠️ **系统要求**

- **Python**: 3.8+ 
- **内存**: 最少512MB
- **磁盘**: 最少100MB
- **网络**: 可选（用于远程访问）

---

## 🚨 **故障排除**

### **常见问题**

**1. MCP工具不可用**
```bash
# 检查Cursor配置
cat ~/.cursor/mcp.json

# 检查Python路径
which python
which python3

# 重启Cursor
```

**2. 依赖安装失败**
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

**3. 端口被占用**
```bash
# 查看端口占用
lsof -i :8000  # macOS/Linux
netstat -an | findstr 8000  # Windows

# 使用其他端口
python main.py --port 8001
```

**4. 权限问题**
```bash
# 给脚本执行权限
chmod +x main.py

# 检查文件权限
ls -la main.py
```

---

## 🔄 **更新维护**

### **更新代码**
```bash
cd mcp_analyze_quality
git pull origin main
pip install --upgrade -r requirements.txt
```

### **检查服务状态**
```bash
# 查看进程
ps aux | grep main.py

# 查看日志
tail -f mcp.log
```

---

## 📞 **技术支持**

### **获取帮助**
- 📧 **邮件**: your-email@example.com
- 🐛 **问题反馈**: [GitHub Issues](https://github.com/your-username/mcp_analyze_quality/issues)
- 📖 **文档**: [项目Wiki](https://github.com/your-username/mcp_analyze_quality/wiki)

### **贡献代码**
```bash
# Fork项目
git clone https://github.com/your-username/mcp_analyze_quality.git
cd mcp_analyze_quality

# 创建分支
git checkout -b feature/your-feature

# 提交更改
git commit -m "Add your feature"
git push origin feature/your-feature

# 创建Pull Request
```

---

## 📄 **许可证**

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 🎉 **快速开始**

```bash
# 一键启动（推荐）
curl -sSL https://raw.githubusercontent.com/your-username/mcp_analyze_quality/main/install.sh | bash

# 或手动安装
git clone https://github.com/your-username/mcp_analyze_quality.git
cd mcp_analyze_quality && pip install -r requirements.txt
python main.py
```

**🚀 现在就开始使用MCP性能分析工具吧！**
