#!/usr/bin/env python3

import urllib.request
import urllib.error
import re
import csv
import io
from typing import Dict, Any, List
from datetime import datetime

# 这个版本需要安装: pip install mcp
try:
    from mcp.server.fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("Warning: MCP library not installed. Run 'pip install mcp' to use FastMCP version.")

# 告警阈值配置
ALERT_THRESHOLDS = {
    "memory_leak": {
        "growth_rate_critical": 100,  # 内存增长率超过100%为严重
        "growth_rate_warning": 50,    # 内存增长率超过50%为警告
        "continuous_growth_periods": 5,  # 连续增长周期数
        "peak_to_avg_ratio": 1.5,    # 峰值与平均值比例
    },
    "thread_management": {
        "max_threads_critical": 400,  # 线程数超过400为严重
        "max_threads_warning": 350,   # 线程数超过350为警告
        "thread_variance_critical": 100,  # 线程波动超过100为严重
        "thread_variance_warning": 50,    # 线程波动超过50为警告
    },
    "heap_usage": {
        "heap_growth_critical": 200,  # 堆增长率超过200%为严重
        "heap_growth_warning": 100,   # 堆增长率超过100%为警告
        "heap_utilization_critical": 0.9,  # 堆利用率超过90%为严重
    },
    "system_resources": {
        "fd_critical": 800,           # 文件描述符超过800为严重
        "fd_warning": 600,            # 文件描述符超过600为警告
        "views_growth_critical": 200, # 视图增长率超过200%为严重
    }
}

def analyze_memory_leak_risk(data_rows: List[Dict], stats: Dict) -> Dict[str, Any]:
    """分析内存泄漏风险"""
    alerts = {
        "risk_level": "低",
        "alerts": [],
        "detailed_analysis": {}
    }
    
    if "Total Pss" not in stats:
        return alerts
    
    pss_stat = stats["Total Pss"]
    growth_rate = ((pss_stat['最大值'] - pss_stat['最小值']) / pss_stat['最小值']) * 100
    
    # 分析连续增长趋势
    pss_values = []
    for row in data_rows:
        try:
            pss_values.append(float(row["Total Pss"].replace(',', '')))
        except:
            continue
    
    # 检测连续增长段
    continuous_growth_count = 0
    max_continuous_growth = 0
    
    for i in range(1, len(pss_values)):
        if pss_values[i] > pss_values[i-1]:
            continuous_growth_count += 1
            max_continuous_growth = max(max_continuous_growth, continuous_growth_count)
        else:
            continuous_growth_count = 0
    
    # 计算峰值与平均值比例
    peak_to_avg_ratio = pss_stat['最大值'] / pss_stat['平均值']
    
    # 分析最近趋势（最后20%的数据）
    recent_data_size = max(5, len(pss_values) // 5)
    recent_values = pss_values[-recent_data_size:]
    recent_growth = ((recent_values[-1] - recent_values[0]) / recent_values[0]) * 100 if len(recent_values) > 1 else 0
    
    alerts["detailed_analysis"] = {
        "总体增长率": f"{growth_rate:.1f}%",
        "最大连续增长周期": max_continuous_growth,
        "峰值平均比": f"{peak_to_avg_ratio:.2f}",
        "近期增长率": f"{recent_growth:.1f}%",
        "数据点数": len(pss_values)
    }
    
    # 严重告警条件
    if (growth_rate > ALERT_THRESHOLDS["memory_leak"]["growth_rate_critical"] and 
        max_continuous_growth >= ALERT_THRESHOLDS["memory_leak"]["continuous_growth_periods"]):
        alerts["risk_level"] = "严重"
        alerts["alerts"].append("🚨 严重内存泄漏风险：内存持续大幅增长，建议立即检查")
        
    elif (growth_rate > ALERT_THRESHOLDS["memory_leak"]["growth_rate_critical"] or
          (recent_growth > 30 and max_continuous_growth >= 3)):
        alerts["risk_level"] = "高"
        alerts["alerts"].append("⚠️ 高内存泄漏风险：检测到明显的内存增长趋势")
        
    elif growth_rate > ALERT_THRESHOLDS["memory_leak"]["growth_rate_warning"]:
        alerts["risk_level"] = "中"
        alerts["alerts"].append("⚠️ 中等内存泄漏风险：内存使用量增长较快")
    
    # 额外检查
    if peak_to_avg_ratio > ALERT_THRESHOLDS["memory_leak"]["peak_to_avg_ratio"]:
        alerts["alerts"].append(f"📊 内存峰值异常：峰值是平均值的{peak_to_avg_ratio:.1f}倍")
    
    if recent_growth > 20:
        alerts["alerts"].append(f"📈 近期内存增长加速：最近增长{recent_growth:.1f}%")
    
    return alerts

def analyze_performance_alerts(data_rows: List[Dict], stats: Dict) -> Dict[str, Any]:
    """综合性能告警分析"""
    all_alerts = {
        "priority_alerts": [],
        "warning_alerts": [],
        "info_alerts": [],
        "overall_health": "良好"
    }
    
    # 内存泄漏分析
    memory_analysis = analyze_memory_leak_risk(data_rows, stats)
    if memory_analysis["risk_level"] in ["严重", "高"]:
        all_alerts["priority_alerts"].extend(memory_analysis["alerts"])
        all_alerts["overall_health"] = "严重" if memory_analysis["risk_level"] == "严重" else "警告"
    elif memory_analysis["risk_level"] == "中":
        all_alerts["warning_alerts"].extend(memory_analysis["alerts"])
        if all_alerts["overall_health"] == "良好":
            all_alerts["overall_health"] = "注意"
    
    # 线程管理告警
    if "Threads" in stats:
        thread_stat = stats["Threads"]
        max_threads = thread_stat['最大值']
        thread_variance = thread_stat['最大值'] - thread_stat['最小值']
        
        if max_threads > ALERT_THRESHOLDS["thread_management"]["max_threads_critical"]:
            all_alerts["priority_alerts"].append(f"🚨 线程数严重超标：峰值{max_threads}，建议立即优化")
            all_alerts["overall_health"] = "严重"
        elif max_threads > ALERT_THRESHOLDS["thread_management"]["max_threads_warning"]:
            all_alerts["warning_alerts"].append(f"⚠️ 线程数偏高：峰值{max_threads}，建议优化")
            if all_alerts["overall_health"] == "良好":
                all_alerts["overall_health"] = "注意"
        
        if thread_variance > ALERT_THRESHOLDS["thread_management"]["thread_variance_critical"]:
            all_alerts["priority_alerts"].append(f"🚨 线程波动严重：变化范围{thread_variance}，线程管理不稳定")
        elif thread_variance > ALERT_THRESHOLDS["thread_management"]["thread_variance_warning"]:
            all_alerts["warning_alerts"].append(f"⚠️ 线程波动较大：变化范围{thread_variance}")
    
    # 堆内存告警
    heap_fields = ["Heap Size(J)", "Heap Size(N)"]
    for field in heap_fields:
        if field in stats:
            heap_stat = stats[field]
            heap_growth = ((heap_stat['最大值'] - heap_stat['最小值']) / heap_stat['最小值']) * 100
            
            if heap_growth > ALERT_THRESHOLDS["heap_usage"]["heap_growth_critical"]:
                all_alerts["priority_alerts"].append(f"🚨 {field}严重增长：增长{heap_growth:.1f}%")
            elif heap_growth > ALERT_THRESHOLDS["heap_usage"]["heap_growth_warning"]:
                all_alerts["warning_alerts"].append(f"⚠️ {field}增长较快：增长{heap_growth:.1f}%")
    
    # 系统资源告警
    if "FD" in stats:
        fd_stat = stats["FD"]
        if fd_stat['最大值'] > ALERT_THRESHOLDS["system_resources"]["fd_critical"]:
            all_alerts["priority_alerts"].append(f"🚨 文件描述符严重超标：峰值{fd_stat['最大值']}，可能导致系统不稳定")
        elif fd_stat['最大值'] > ALERT_THRESHOLDS["system_resources"]["fd_warning"]:
            all_alerts["warning_alerts"].append(f"⚠️ 文件描述符偏高：峰值{fd_stat['最大值']}，建议检查文件句柄管理")
    
    if "Views" in stats:
        views_stat = stats["Views"]
        views_growth = ((views_stat['最大值'] - views_stat['最小值']) / views_stat['最小值']) * 100
        if views_growth > ALERT_THRESHOLDS["system_resources"]["views_growth_critical"]:
            all_alerts["priority_alerts"].append(f"🚨 视图数量异常增长：增长{views_growth:.1f}%，可能存在视图泄漏")
    
    # WebView特殊检查
    if "WebViews" in stats and stats["WebViews"]['最大值'] > 0:
        webview_count = stats["WebViews"]['最大值']
        if webview_count > 5:
            all_alerts["warning_alerts"].append(f"⚠️ WebView数量较多：{webview_count}个，注意内存管理")
        else:
            all_alerts["info_alerts"].append(f"ℹ️ 检测到WebView使用：{webview_count}个，建议优化内存管理")
    
    # 添加内存分析详情到info
    if memory_analysis["detailed_analysis"]:
        all_alerts["memory_analysis"] = memory_analysis["detailed_analysis"]
    
    return all_alerts

def parse_performance_data(csv_content: str) -> Dict[str, Any]:
    """解析性能监控CSV数据"""
    try:
        # 使用StringIO来处理CSV内容
        csv_file = io.StringIO(csv_content)
        reader = csv.DictReader(csv_file)
        
        data_rows = []
        for row in reader:
            data_rows.append(row)
        
        if not data_rows:
            return {"error": "没有找到数据行"}
        
        # 获取列名
        columns = list(data_rows[0].keys())
        
        # 分析数据
        analysis = {
            "总记录数": len(data_rows),
            "列数": len(columns),
            "列名": columns,
            "时间范围": {
                "开始时间": data_rows[0].get("Time", "未知"),
                "结束时间": data_rows[-1].get("Time", "未知")
            }
        }
        
        # 分析数值型字段的统计信息
        numeric_stats = {}
        numeric_fields = [
            "Total Pss", "Heap Size(J)", "Heap Alloc(J)", "Heap Free(J)",
            "Heap Size(N)", "Heap Alloc(N)", "Heap Free(N)", "FD", "Views",
            "ViewRootImpl", "AppContexts", "Activities", "WebViews", "Thread",
            "HandlerThread", "Bitmap", "VmPeak", "VmSize", "VmHWM", "VmRSS", "Threads"
        ]
        
        for field in numeric_fields:
            if field in columns:
                values = []
                for row in data_rows:
                    try:
                        value = float(row[field].replace(',', ''))
                        values.append(value)
                    except (ValueError, AttributeError):
                        continue
                
                if values:
                    numeric_stats[field] = {
                        "最小值": min(values),
                        "最大值": max(values),
                        "平均值": round(sum(values) / len(values), 2),
                        "变化趋势": "上升" if values[-1] > values[0] else "下降" if values[-1] < values[0] else "稳定"
                    }
        
        analysis["数值统计"] = numeric_stats
        
        # 内存使用分析
        memory_analysis = {}
        if "Total Pss" in columns:
            pss_values = []
            for row in data_rows:
                try:
                    pss_values.append(float(row["Total Pss"].replace(',', '')))
                except:
                    continue
            
            if pss_values:
                memory_analysis["内存使用"] = {
                    "初始值": f"{pss_values[0]:,.0f} KB",
                    "最终值": f"{pss_values[-1]:,.0f} KB",
                    "峰值": f"{max(pss_values):,.0f} KB",
                    "变化": f"{((pss_values[-1] - pss_values[0]) / pss_values[0] * 100):+.1f}%"
                }
        
        # 线程分析
        if "Threads" in columns:
            thread_values = []
            for row in data_rows:
                try:
                    thread_values.append(int(row["Threads"]))
                except:
                    continue
            
            if thread_values:
                memory_analysis["线程数"] = {
                    "初始值": thread_values[0],
                    "最终值": thread_values[-1],
                    "峰值": max(thread_values),
                    "变化": thread_values[-1] - thread_values[0]
                }
        
        if memory_analysis:
            analysis["关键指标分析"] = memory_analysis
        
        # 智能告警分析
        alert_analysis = analyze_performance_alerts(data_rows, numeric_stats)
        analysis["告警分析"] = alert_analysis
        
        # 传统性能建议（保持向后兼容）
        suggestions = []
        if "Total Pss" in numeric_stats:
            pss_trend = numeric_stats["Total Pss"]["变化趋势"]
            if pss_trend == "上升":
                suggestions.append("内存使用呈上升趋势，建议检查内存泄漏")
        
        if "Threads" in numeric_stats:
            max_threads = numeric_stats["Threads"]["最大值"]
            if max_threads > 300:
                suggestions.append(f"线程数较高({max_threads})，建议优化线程管理")
        
        if "WebViews" in numeric_stats:
            max_webviews = numeric_stats["WebViews"]["最大值"]
            if max_webviews > 0:
                suggestions.append(f"检测到WebView使用({max_webviews})，注意WebView内存管理")
        
        if suggestions:
            analysis["性能建议"] = suggestions
        
        return analysis
        
    except Exception as e:
        return {"error": f"解析CSV数据时出错: {str(e)}"}

def analyze_text_content(content: str, url: str, content_type: str) -> Dict[str, Any]:
    """分析文本内容，专门处理性能监控数据"""
    
    # 检查是否是CSV格式的性能数据
    if "Time,Total Pss,Heap Size" in content or content.strip().startswith("Time,"):
        # 这是性能监控CSV数据
        csv_analysis = parse_performance_data(content)
        
        return {
            "url": url,
            "content_type": content_type,
            "data_type": "performance_monitoring_csv",
            "is_text": True,
            "analysis": csv_analysis,
            "content_preview": content[:500] + "..." if len(content) > 500 else content
        }
    
    # 如果不是性能数据，进行通用文本分析
    word_count = len(content.split())
    char_count = len(content)
    line_count = len(content.split('\n'))
    
    # Extract URLs if any
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls_found = re.findall(url_pattern, content)
    
    # Extract email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails_found = re.findall(email_pattern, content)
    
    # Simple keyword extraction (most common words)
    words = re.findall(r'\b\w+\b', content.lower())
    word_freq = {}
    for word in words:
        if len(word) > 3:  # Only count words longer than 3 characters
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Get top 10 most common words
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        "url": url,
        "content_type": content_type,
        "data_type": "general_text",
        "is_text": True,
        "analysis": {
            "word_count": word_count,
            "character_count": char_count,
            "line_count": line_count,
            "urls_found": len(urls_found),
            "emails_found": len(emails_found),
            "top_words": top_words,
            "sample_urls": urls_found[:5] if urls_found else [],
            "sample_emails": emails_found[:5] if emails_found else []
        },
        "content_preview": content[:500] + "..." if len(content) > 500 else content
    }

if MCP_AVAILABLE:
    # 创建FastMCP服务器实例
    mcp = FastMCP("Performance Data Analyzer")

    @mcp.tool()
    def fetch_and_analyze_url(url: str) -> Dict[str, Any]:
        """Fetch content from a URL and analyze it, with special handling for performance monitoring CSV data"""
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read()
                content_type = response.info().get_content_type()
                
                # Try to decode as text
                try:
                    if content_type and ('text' in content_type or 'csv' in content_type):
                        text_content = content.decode('utf-8')
                        return analyze_text_content(text_content, url, content_type)
                    else:
                        return {
                            "url": url,
                            "content_type": content_type,
                            "size_bytes": len(content),
                            "analysis": "Binary content - cannot analyze text",
                            "is_text": False
                        }
                except UnicodeDecodeError:
                    return {
                        "url": url,
                        "content_type": content_type,
                        "size_bytes": len(content),
                        "analysis": "Content encoding not supported",
                        "is_text": False
                    }
                    
        except urllib.error.URLError as e:
            return {
                "url": url,
                "error": str(e),
                "analysis": "Failed to fetch URL"
            }

    if __name__ == "__main__":
        # 运行FastMCP服务器
        mcp.run()
else:
    print("FastMCP not available. Please install with: pip install mcp")
    print("Or use the manual implementation in main.py") 