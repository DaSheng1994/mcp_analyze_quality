# 🚀 MCP性能分析服务器

> 移动应用性能监控数据智能分析工具，支持内存泄漏检测、资源监控告警

## 📋 **快速开始**

### 1. **获取项目**
```bash
git clone git@github.com:DaSheng1994/mcp_analyze_quality.git
cd mcp_analyze_quality
```

### 2. **安装依赖**
```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS

# 安装依赖
pip install -r requirements.txt
```

### 3. **配置Cursor MCP**
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

### 4. **重启Cursor并使用**
完全退出并重新启动Cursor，然后在对话中输入：
```
分析这个性能数据：http://localhost:8000/meminfo.csv
```

## 🌐 **远程部署**

### **服务器端部署**
```bash
# 在服务器上部署
git clone git@github.com:DaSheng1994/mcp_analyze_quality.git
cd mcp_analyze_quality
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 启动服务（后台运行）
nohup python main.py > mcp.log 2>&1 &
nohup python3 -m http.server 8000 > http.log 2>&1 &
```

### **客户端配置**
团队成员在各自的Cursor中配置：
```json
{
  "mcpServers": {
    "performance-analyzer": {
      "command": "ssh",
      "args": ["your-server", "cd /path/to/mcp_analyze_quality && .venv/bin/python main.py"],
      "env": {}
    }
  }
}
```

### **使用远程服务**
```
分析这个性能数据：http://your-server-ip:8000/meminfo.csv
```

## 📊 **功能特性**

- **内存泄漏检测**: 自动识别内存持续增长模式
- **资源监控**: 线程、文件描述符、视图数量监控  
- **性能告警**: 多级告警系统（严重/警告/信息）
- **趋势分析**: 33项性能指标深度分析

---

**🚀 现在就开始使用MCP性能分析工具吧！**
