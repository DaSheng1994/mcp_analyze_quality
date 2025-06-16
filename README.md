# 🚀 MCP性能分析服务器

> 移动应用性能监控数据智能分析工具，专注于严重问题检测

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

- **严重问题检测**: 专注于识别需要立即处理的严重性能问题
- **简洁输出**: 只返回严重警告信息，避免信息过载
- **智能分析**: 基于预定义规则进行精准判断
- **易于集成**: 轻量级MCP服务器，快速部署

## 🚨 **严重警告规则**

当前支持的严重警告检测：
- **物理内存警告**: VmRSS超过1.3GB时触发
- **Views数量警告**: Views增长超过700个时触发

## 📝 **自定义规则**

可以通过修改 `.cursor/rules/quality-rules.mdc` 文件来自定义分析规则。

---

**🚀 现在就开始使用MCP性能分析工具吧！**
