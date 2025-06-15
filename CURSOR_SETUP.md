# 在Cursor中使用Web Content Analyzer MCP服务器

## ✅ 配置已完成

MCP服务器已经自动配置完成！配置文件位于：
- **Cursor**: `~/.cursor/mcp.json`
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`

## 🚀 在Cursor中使用步骤

### 1. 打开Cursor设置
1. 打开Cursor
2. 按 `Cmd + ,` (macOS) 或 `Ctrl + ,` (Windows/Linux) 打开设置
3. 在左侧菜单中找到 **"MCP"** 选项

### 2. 验证MCP服务器状态
在MCP设置页面中，你应该看到：
- 服务器名称：`web-content-analyzer`
- 状态：绿色圆点 ✅（表示正常运行）
- 描述：A web content analyzer that can fetch and analyze content from URLs using FastMCP

如果状态是红色，请检查：
- Python路径是否正确
- 虚拟环境是否存在
- MCP库是否已安装

### 3. 开始使用
在Cursor的聊天界面中，你可以使用自然语言请求分析网址：

#### 示例对话：

**你**: "请分析这个网址的内容：https://www.baidu.com"

**Cursor**: 会自动调用MCP工具，获取网页内容并提供详细分析，包括：
- 内容类型和大小
- 字数、字符数、行数统计
- 发现的URL链接数量
- 发现的邮箱地址
- 最常出现的关键词
- 内容预览

**你**: "帮我看看这个GitHub文件里有什么：https://raw.githubusercontent.com/python/cpython/main/README.rst"

**Cursor**: 会分析GitHub上的README文件内容

### 4. 更多使用示例

```
"分析这个API文档：https://api.example.com/docs"
"这个网站有什么内容：https://news.ycombinator.com"
"帮我看看这个配置文件：https://raw.githubusercontent.com/user/repo/main/config.json"
"分析这个博客文章：https://blog.example.com/post/123"
```

## 🔧 故障排除

### 如果MCP服务器显示红色状态：

1. **检查虚拟环境**：
   ```bash
   cd /Users/staff/project/mcp_projects/mcp_demo
   source venv/bin/activate
   python3 -c "import mcp; print('MCP库已安装')"
   ```

2. **手动测试服务器**：
   ```bash
   source venv/bin/activate
   python3 main.py
   # 然后输入: {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}
   ```

3. **重新配置**：
   ```bash
   source venv/bin/activate
   python3 setup_cursor.py
   ```

4. **重启Cursor**：完全关闭并重新打开Cursor

### 如果工具调用失败：

- 检查网络连接
- 确认目标URL可以访问
- 查看Cursor的错误信息

## 📝 技术细节

- **服务器类型**: FastMCP (官方推荐)
- **通信方式**: stdio (标准输入输出)
- **支持的内容**: 文本文件、HTML页面、API响应等
- **分析功能**: 文本统计、链接提取、关键词分析

## 🎉 享受使用！

现在你可以在Cursor中直接分析任何网址的内容，无需手动复制粘贴或切换应用程序。MCP服务器会自动处理网络请求和内容分析，让你的工作流程更加高效！ 