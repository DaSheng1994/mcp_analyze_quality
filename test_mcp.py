#!/usr/bin/env python3

import json
from main import WebContentAnalyzer

def test_mcp_server():
    """Test the MCP server with various requests"""
    server = WebContentAnalyzer()
    
    print("=== Testing MCP Web Content Analyzer ===\n")
    
    # Test 1: Initialize
    print("1. Testing initialization...")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    response = server.handle_request(init_request)
    print(f"✓ Server initialized: {response['result']['serverInfo']['name']}")
    
    # Test 2: List tools
    print("\n2. Testing tools list...")
    tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    }
    response = server.handle_request(tools_request)
    tools = response['result']['tools']
    print(f"✓ Available tools: {len(tools)}")
    for tool in tools:
        print(f"   - {tool['name']}: {tool['description']}")
    
    # Test 3: Analyze a URL
    print("\n3. Testing URL analysis...")
    test_urls = [
        "https://httpbin.org/robots.txt",
        "https://raw.githubusercontent.com/python/cpython/main/README.rst"
    ]
    
    for url in test_urls:
        print(f"\nAnalyzing: {url}")
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "fetch_and_analyze_url",
                "arguments": {
                    "url": url
                }
            }
        }
        
        try:
            response = server.handle_request(call_request)
            if 'result' in response:
                result_text = response['result']['content'][0]['text']
                result_data = json.loads(result_text)
                
                print(f"✓ Content type: {result_data.get('content_type', 'Unknown')}")
                if result_data.get('is_text'):
                    analysis = result_data['analysis']
                    print(f"✓ Word count: {analysis['word_count']}")
                    print(f"✓ Character count: {analysis['character_count']}")
                    print(f"✓ URLs found: {analysis['urls_found']}")
                    print(f"✓ Emails found: {analysis['emails_found']}")
                    if analysis['top_words']:
                        print(f"✓ Top words: {', '.join([f'{word}({count})' for word, count in analysis['top_words'][:3]])}")
                else:
                    print(f"✓ File size: {result_data.get('size_bytes', 0)} bytes")
            else:
                print(f"✗ Error: {response.get('error', {}).get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
    
    print("\n=== MCP Server Test Complete ===")

if __name__ == "__main__":
    test_mcp_server() 