#!/usr/bin/env python3

import urllib.request
import urllib.error
import csv
import io
import os
from typing import Dict, Any, List

# 这个版本需要安装: pip install mcp
try:
    from mcp.server.fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("Warning: MCP library not installed. Run 'pip install mcp' to use FastMCP version.")

# CSV列含义说明
COLUMN_MEANINGS = {
    "Time": "监控时间戳",
    "Total Pss": "总内存使用量(KB) - 应用实际占用的物理内存",
    "Heap Size(J)": "Java堆大小(KB) - Java虚拟机分配的堆内存",
    "Heap Alloc(J)": "Java堆已分配(KB) - Java堆中已使用的内存",
    "Heap Free(J)": "Java堆空闲(KB) - Java堆中可用的内存",
    "Heap Size(N)": "Native堆大小(KB) - 原生代码分配的堆内存",
    "Heap Alloc(N)": "Native堆已分配(KB) - Native堆中已使用的内存",
    "Heap Free(N)": "Native堆空闲(KB) - Native堆中可用的内存",
    "FD": "文件描述符数量 - 打开的文件句柄数",
    "Views": "视图数量 - UI视图对象的总数",
    "ViewRootImpl": "根视图数量 - 顶级视图容器数量",
    "AppContexts": "应用上下文数量 - Application Context实例数",
    "Activities": "Activity数量 - 当前存活的Activity实例数",
    "WebViews": "WebView数量 - WebView组件实例数",
    "Thread": "线程数量(旧字段) - 应用创建的线程总数",
    "Threads": "线程数量 - 应用创建的线程总数",
    "HandlerThread": "Handler线程数量 - 专门处理消息的后台线程数",
    "Bitmap": "图片Bitmap数量 - 内存中的图片对象数量",
    "VmPeak": "虚拟内存峰值(KB) - 进程使用的最大虚拟内存",
    "VmSize": "虚拟内存大小(KB) - 进程当前虚拟内存大小",
    "VmHWM": "物理内存峰值(KB) - 进程使用的最大物理内存",
    "VmRSS": "物理内存大小(KB) - 进程当前占用的物理内存"
}

def load_analysis_rules() -> str:
    """加载分析规则"""
    rules_path = ".cursor/rules/quality-rules.mdc"
    if os.path.exists(rules_path):
        try:
            with open(rules_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            return f"无法读取规则文件: {e}"
    return "未找到分析规则文件"

def fetch_csv_data(url: str) -> Dict[str, Any]:
    """获取CSV数据并解析为结构化格式"""
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read()
            content_type = response.info().get_content_type()
            
            # 解码为文本
            try:
                if content_type and ('text' in content_type or 'csv' in content_type):
                    text_content = content.decode('utf-8')
                    
                    # 解析CSV
                    csv_file = io.StringIO(text_content)
                    reader = csv.DictReader(csv_file)
                    
                    data_rows = []
                    for row in reader:
                        data_rows.append(row)
                    
                    if not data_rows:
                        return {"error": "没有找到数据行"}
                    
                    # 获取列信息
                    columns = list(data_rows[0].keys())
                    
                    # 添加列含义说明
                    column_info = {}
                    for col in columns:
                        column_info[col] = {
                            "meaning": COLUMN_MEANINGS.get(col, "未知列含义"),
                            "sample_values": [row.get(col, "") for row in data_rows[:3]]  # 前3个样本值
                        }
                    
                    # 加载分析规则
                    analysis_rules = load_analysis_rules()
                    
                    return {
                        "url": url,
                        "content_type": content_type,
                        "data_info": {
                            "total_records": len(data_rows),
                            "columns_count": len(columns),
                            "time_range": {
                                "start": data_rows[0].get("Time", "未知"),
                                "end": data_rows[-1].get("Time", "未知")
                            }
                        },
                        "column_meanings": column_info,
                        "raw_data": data_rows,
                        "analysis_rules": analysis_rules,
                        "output_requirement": "⚠️ 重要：请严格按照analysis_rules中的规则进行分析，只返回触发严重警告的问题，不要返回其他详细信息、建议措施或完整报告。如果没有严重警告，只返回'未发现严重问题'。"
                    }
                else:
                    return {
                        "url": url,
                        "error": "不是CSV格式的数据",
                        "content_type": content_type
                    }
            except UnicodeDecodeError:
                return {
                    "url": url,
                    "error": "内容编码不支持",
                    "content_type": content_type
                }
                
    except urllib.error.URLError as e:
        return {
            "url": url,
            "error": f"获取URL失败: {str(e)}"
        }

if MCP_AVAILABLE:
    # 创建FastMCP服务器实例
    mcp = FastMCP("Performance Data Fetcher")

    @mcp.tool()
    def fetch_performance_data(url: str) -> Dict[str, Any]:
        """
        获取性能监控CSV数据，提供列含义说明，供AI分析使用
        
        Args:
            url: CSV数据的URL地址
            
        Returns:
            包含数据、列含义说明和分析规则的结构化信息。AI必须严格按照规则只返回严重警告信息，不返回其他内容。
        """
        return fetch_csv_data(url)

def main():
    """Main entry point for the MCP server"""
    if MCP_AVAILABLE:
        print(f"🚀 启动MCP数据获取服务器...")
        print(f"📊 功能：获取CSV数据 + 列含义说明")
        print(f"🤖 分析规则：只返回严重警告信息")
        
        # 运行FastMCP服务器 - 使用stdio模式
        mcp.run()
    else:
        print("FastMCP not available. Please install with: pip install mcp")

if __name__ == "__main__":
    main() 