# 🚀 MCP性能分析服务器

> 移动应用性能监控数据智能分析工具，支持内存泄漏检测、资源监控告警

## ⚡ 快速开始（推荐）

### 一键部署
```bash
# Linux/macOS
curl -sSL https://raw.githubusercontent.com/your-username/mcp_demo/main/git_deploy.sh | bash

# 或手动部署
git clone https://github.com/your-username/mcp_demo.git
cd mcp_demo
pip install -r requirements.txt
python main.py --network
```

### Windows快速启动
```cmd
git clone https://github.com/your-username/mcp_demo.git
cd mcp_demo
pip install -r requirements.txt
start_server.bat
```

## 🌐 多电脑使用

### 方法1: 网络访问（推荐）
1. **服务器端**（任意一台电脑）:
   ```bash
   git clone https://github.com/your-username/mcp_demo.git
   cd mcp_demo
   python main.py --network
   ```

2. **客户端**（其他电脑的Cursor）:
   ```json
   // ~/.cursor/mcp_settings.json
   {
     "mcpServers": {
       "performance-analyzer": {
         "command": "python",
         "args": ["-c", "import urllib.request; exec(urllib.request.urlopen('http://服务器IP:8000/mcp').read())"],
         "env": {}
       }
     }
   }
   ```

### 方法2: 每台电脑独立部署
```bash
# 在每台需要使用的电脑上执行
git clone https://github.com/your-username/mcp_demo.git
cd mcp_demo
pip install -r requirements.txt

# 配置Cursor MCP
# 编辑 ~/.cursor/mcp_settings.json
{
  "mcpServers": {
    "performance-analyzer": {
      "command": "python",
      "args": ["/path/to/mcp_demo/main.py"],
      "env": {}
    }
  }
}
```

## 📊 功能特性

### 🔍 智能分析
- **内存泄漏检测**: 自动识别内存持续增长模式
- **资源监控**: 线程、文件描述符、视图数量监控
- **性能告警**: 多级告警系统（严重/警告/信息）
- **趋势分析**: 33项性能指标深度分析

### 🚨 告警系统
- **内存泄漏**: 增长率>100% + 连续5周期 = 严重告警
- **Java堆**: 增长>80MB = 严重告警
- **Native堆**: 增长>500MB且无回落 = 严重告警
- **文件描述符**: 增长>100个 = 严重告警
- **视图数量**: 增长>700个 = 严重告警

## 🛠️ 安装要求

- Python 3.8+
- Git
- 网络连接（用于安装依赖）

## 📁 项目结构

```
mcp_demo/
├── main.py                 # 主服务器程序
├── requirements.txt        # Python依赖
├── git_deploy.sh          # 一键部署脚本
├── start_server.sh        # Linux/macOS启动脚本
├── start_server.bat       # Windows启动脚本
├── portable_deploy.py     # 便携式部署工具
├── DEPLOYMENT_GUIDE.md    # 详细部署指南
└── README.md              # 本文件
```

## 🔧 配置选项

### 环境变量
```bash
export MCP_HOST=0.0.0.0      # 监听地址
export MCP_PORT=8000         # 监听端口
```

### 命令行参数
```bash
python main.py --network     # 网络模式
python main.py --port 8080   # 自定义端口
```

## 📖 使用示例

### 分析CSV性能数据
```python
# 在Cursor中使用MCP工具
请分析这个性能数据：http://your-server:8000/meminfo.csv
```

### 示例输出
```json
{
  "系统健康状态": "🔴 严重",
  "严重告警": [
    "🚨 严重内存泄漏风险：内存持续大幅增长，建议立即检查",
    "🚨 Java堆内存增长严重超标：增长114.5MB，建议检查内存泄漏"
  ],
  "内存泄漏分析": {
    "总体增长率": "108.6%",
    "连续增长周期": 5,
    "风险等级": "🔴 极高"
  }
}
```

## 🚀 部署方案对比

| 方案 | 适用场景 | 复杂度 | 推荐度 |
|------|----------|--------|--------|
| **Git仓库** | 通用，推荐 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 网络部署 | 临时使用 | ⭐ | ⭐⭐⭐⭐ |
| 云服务器 | 企业级 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Docker | 容器化 | ⭐⭐⭐ | ⭐⭐⭐ |
| 便携式 | 离线环境 | ⭐ | ⭐⭐ |

## 🔄 更新和维护

### 更新代码
```bash
cd mcp_demo
git pull origin main
pip install --upgrade -r requirements.txt
```

### 自动更新脚本
```bash
# 使用内置更新脚本
./update.sh
```

### 服务管理
```bash
# 启动服务
./start.sh

# 停止服务
./stop.sh

# 查看状态
ps aux | grep "python main.py"
```

## 🌍 网络配置

### 防火墙设置
```bash
# Ubuntu/Debian
sudo ufw allow 8000

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload

# Windows
# 在Windows Defender防火墙中允许端口8000
```

### 获取服务器IP
```bash
# Linux/macOS
hostname -I | awk '{print $1}'

# Windows
ipconfig | findstr IPv4
```

## 🚨 故障排除

### 常见问题

**1. Git克隆失败**
```bash
# 使用HTTPS替代SSH
git clone https://github.com/your-username/mcp_demo.git
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
netstat -an | grep 8000
# 使用其他端口
python main.py --network --port 8001
```

**4. MCP连接失败**
- 检查Cursor MCP配置文件路径
- 确认服务器正在运行
- 验证网络连通性

### 调试模式
```bash
# 启用详细日志
python main.py --network --debug

# 查看实时日志
tail -f mcp.log
```

## 📞 技术支持

### 文档资源
- [详细部署指南](./DEPLOYMENT_GUIDE.md)
- [云服务部署](./cloud_deploy.md)
- [部署方案对比](./部署方案总结.md)

### 社区支持
- GitHub Issues: 报告问题和建议
- 讨论区: 技术交流和经验分享

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🎯 为什么选择Git仓库部署？

✅ **标准化**: 业界标准的代码分发方式  
✅ **版本控制**: 自动跟踪更新和回滚  
✅ **跨平台**: 支持所有主流操作系统  
✅ **易维护**: 一条命令完成更新  
✅ **团队协作**: 多人开发和部署友好  
✅ **文档完整**: 包含完整的使用说明  

**开始使用**: `git clone <repo-url> && cd mcp_demo && pip install -r requirements.txt && python main.py --network`
