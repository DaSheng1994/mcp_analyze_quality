#!/usr/bin/env python3

from main import analyze_text_content
import json

def test_meminfo_analysis():
    """测试meminfo.csv文件分析 - 包含智能告警系统"""
    
    print("🔍 性能数据分析报告 - meminfo.csv (智能告警版)")
    print("=" * 70)
    
    # 读取文件
    try:
        with open('meminfo.csv', 'r') as f:
            content = f.read()
        
        # 分析数据
        result = analyze_text_content(content, 'file://meminfo.csv', 'text/csv')
        analysis = result.get('analysis', {})
        
        # 数据概览
        if '总记录数' in analysis:
            print(f"\n📊 数据概览:")
            print(f"   - 总记录数: {analysis['总记录数']}")
            print(f"   - 列数: {analysis['列数']}")
            time_range = analysis.get('时间范围', {})
            print(f"   - 监控时间: {time_range.get('开始时间', '未知')} 到 {time_range.get('结束时间', '未知')}")
            
            # 计算监控时长
            start_time = time_range.get('开始时间', '')
            end_time = time_range.get('结束时间', '')
            if start_time and end_time:
                print(f"   - 监控时长: 约 {analysis['总记录数'] * 5} 分钟 (每5分钟一次采样)")
        
        # 🚨 智能告警分析 - 优先显示
        if '告警分析' in analysis:
            alert_analysis = analysis['告警分析']
            overall_health = alert_analysis.get('overall_health', '良好')
            
            print(f"\n🚨 智能告警分析:")
            print(f"   系统健康状态: {get_health_emoji(overall_health)} {overall_health}")
            
            # 优先告警（严重问题）
            priority_alerts = alert_analysis.get('priority_alerts', [])
            if priority_alerts:
                print(f"\n   🔴 优先告警 (需要立即处理):")
                for i, alert in enumerate(priority_alerts, 1):
                    print(f"     {i}. {alert}")
            
            # 警告告警
            warning_alerts = alert_analysis.get('warning_alerts', [])
            if warning_alerts:
                print(f"\n   🟡 警告告警 (建议关注):")
                for i, alert in enumerate(warning_alerts, 1):
                    print(f"     {i}. {alert}")
            
            # 信息告警
            info_alerts = alert_analysis.get('info_alerts', [])
            if info_alerts:
                print(f"\n   🔵 信息告警 (一般提醒):")
                for i, alert in enumerate(info_alerts, 1):
                    print(f"     {i}. {alert}")
            
            # 内存泄漏详细分析
            if 'memory_analysis' in alert_analysis:
                memory_details = alert_analysis['memory_analysis']
                print(f"\n   🧠 内存泄漏详细分析:")
                print(f"     - 总体增长率: {memory_details.get('总体增长率', '未知')}")
                print(f"     - 最大连续增长周期: {memory_details.get('最大连续增长周期', 0)} 次")
                print(f"     - 峰值/平均值比例: {memory_details.get('峰值平均比', '未知')}")
                print(f"     - 近期增长率: {memory_details.get('近期增长率', '未知')}")
                print(f"     - 分析数据点: {memory_details.get('数据点数', 0)} 个")
            
            if not priority_alerts and not warning_alerts:
                print(f"\n   ✅ 未检测到严重性能问题")
        
        # 关键指标分析
        if '关键指标分析' in analysis:
            print(f"\n📈 关键指标分析:")
            key_metrics = analysis['关键指标分析']
            
            if '内存使用' in key_metrics:
                memory = key_metrics['内存使用']
                print(f"   💾 内存使用 (Total Pss):")
                print(f"     - 初始值: {memory['初始值']}")
                print(f"     - 最终值: {memory['最终值']}")
                print(f"     - 峰值: {memory['峰值']}")
                print(f"     - 变化: {memory['变化']}")
            
            if '线程数' in key_metrics:
                threads = key_metrics['线程数']
                print(f"   🧵 线程数:")
                print(f"     - 初始值: {threads['初始值']}")
                print(f"     - 最终值: {threads['最终值']}")
                print(f"     - 峰值: {threads['峰值']}")
                print(f"     - 变化: {threads['变化']}")
        
        # 详细统计（简化显示）
        if '数值统计' in analysis:
            print(f"\n📊 关键性能指标:")
            stats = analysis['数值统计']
            
            # 重点关注的指标
            key_fields = ['Total Pss', 'Heap Size(J)', 'Heap Size(N)', 'Threads', 'Views', 'FD']
            for field in key_fields:
                if field in stats:
                    stat = stats[field]
                    trend_emoji = get_trend_emoji(stat['变化趋势'])
                    print(f"   {trend_emoji} {field}: {stat['最小值']:,.0f} ~ {stat['最大值']:,.0f} (平均: {stat['平均值']:,.0f})")
        
        # 传统性能建议（如果有）
        if '性能建议' in analysis:
            print(f"\n💡 传统性能建议:")
            for i, suggestion in enumerate(analysis['性能建议'], 1):
                print(f"   {i}. {suggestion}")
        
        # 总结和建议
        print(f"\n📋 分析总结:")
        if '告警分析' in analysis:
            alert_analysis = analysis['告警分析']
            priority_count = len(alert_analysis.get('priority_alerts', []))
            warning_count = len(alert_analysis.get('warning_alerts', []))
            
            if priority_count > 0:
                print(f"   🚨 发现 {priority_count} 个严重问题，建议立即处理")
            if warning_count > 0:
                print(f"   ⚠️ 发现 {warning_count} 个警告问题，建议关注")
            
            if priority_count == 0 and warning_count == 0:
                print(f"   ✅ 系统运行状态良好，未发现严重性能问题")
            
            # 针对性建议
            if priority_count > 0:
                print(f"\n🎯 优先处理建议:")
                print(f"   1. 立即检查内存泄漏问题，重点关注对象生命周期管理")
                print(f"   2. 分析内存增长的根本原因，可能的原因包括：")
                print(f"      - 未释放的大对象或集合")
                print(f"      - 静态引用导致的内存泄漏")
                print(f"      - 监听器或回调未正确注销")
                print(f"      - 图片或资源未及时回收")
                print(f"   3. 使用内存分析工具进行深度诊断")
        
        print(f"\n✅ 分析完成！数据类型: {result.get('data_type', '未知')}")
        
    except FileNotFoundError:
        print("❌ 错误: 找不到meminfo.csv文件")
    except Exception as e:
        print(f"❌ 分析出错: {str(e)}")

def get_health_emoji(health_status):
    """获取健康状态对应的emoji"""
    emoji_map = {
        "良好": "🟢",
        "注意": "🟡", 
        "警告": "🟠",
        "严重": "🔴"
    }
    return emoji_map.get(health_status, "⚪")

def get_trend_emoji(trend):
    """获取趋势对应的emoji"""
    emoji_map = {
        "上升": "📈",
        "下降": "📉",
        "稳定": "➡️"
    }
    return emoji_map.get(trend, "❓")

if __name__ == "__main__":
    test_meminfo_analysis() 