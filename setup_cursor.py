#!/usr/bin/env python3

import json
import os
import sys
from pathlib import Path

def setup_cursor_mcp():
    """Setup MCP server configuration for Cursor"""
    
    print("=== Web Content Analyzer MCP Setup for Cursor ===\n")
    
    # Get current directory
    current_dir = os.path.abspath(os.path.dirname(__file__))
    main_py_path = os.path.join(current_dir, "main.py")
    venv_python_path = os.path.join(current_dir, "venv", "bin", "python3")
    
    # Check if main.py exists
    if not os.path.exists(main_py_path):
        print("❌ Error: main.py not found in current directory")
        print(f"   Expected path: {main_py_path}")
        return False
    
    # Check if virtual environment exists
    if not os.path.exists(venv_python_path):
        print("❌ Error: Virtual environment not found")
        print(f"   Expected path: {venv_python_path}")
        print("   Please run: python3 -m venv venv && source venv/bin/activate && pip install mcp")
        return False
    
    # Cursor MCP config path
    cursor_config_dir = Path.home() / ".cursor"
    cursor_config_file = cursor_config_dir / "mcp.json"
    
    # Create .cursor directory if it doesn't exist
    cursor_config_dir.mkdir(exist_ok=True)
    
    # MCP server configuration - use virtual environment Python
    mcp_config = {
        "mcpServers": {
            "web-content-analyzer": {
                "command": venv_python_path,
                "args": [main_py_path],
                "description": "A web content analyzer that can fetch and analyze content from URLs using FastMCP"
            }
        }
    }
    
    # Check if config file already exists
    if cursor_config_file.exists():
        try:
            with open(cursor_config_file, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
            
            # Merge configurations
            if "mcpServers" not in existing_config:
                existing_config["mcpServers"] = {}
            
            existing_config["mcpServers"]["web-content-analyzer"] = mcp_config["mcpServers"]["web-content-analyzer"]
            mcp_config = existing_config
            
            print("✓ Found existing Cursor MCP configuration, merging...")
            
        except json.JSONDecodeError:
            print("⚠️  Warning: Existing config file is invalid JSON, creating new one...")
        except Exception as e:
            print(f"⚠️  Warning: Could not read existing config: {e}")
    
    # Write configuration
    try:
        with open(cursor_config_file, 'w', encoding='utf-8') as f:
            json.dump(mcp_config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ MCP configuration written to: {cursor_config_file}")
        print(f"✅ Server path: {main_py_path}")
        print(f"✅ Python path: {venv_python_path}")
        
        print("\n📋 Next steps:")
        print("1. Open Cursor")
        print("2. Go to Settings → MCP")
        print("3. You should see 'web-content-analyzer' server listed")
        print("4. Make sure it shows a green status indicator")
        print("5. Start chatting and ask to analyze a URL!")
        
        print("\n💡 Example usage:")
        print('   "请分析这个网址的内容：https://example.com"')
        print('   "帮我看看这个文件里有什么：https://raw.githubusercontent.com/user/repo/main/README.md"')
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing configuration: {e}")
        return False

def setup_claude_desktop():
    """Setup MCP server configuration for Claude Desktop"""
    
    print("\n=== Web Content Analyzer MCP Setup for Claude Desktop ===\n")
    
    # Get current directory
    current_dir = os.path.abspath(os.path.dirname(__file__))
    main_py_path = os.path.join(current_dir, "main.py")
    venv_python_path = os.path.join(current_dir, "venv", "bin", "python3")
    
    # Claude Desktop config paths (different for different OS)
    if sys.platform == "darwin":  # macOS
        claude_config_file = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "win32":  # Windows
        claude_config_file = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    else:  # Linux
        claude_config_file = Path.home() / ".config" / "claude" / "claude_desktop_config.json"
    
    # Create directory if it doesn't exist
    claude_config_file.parent.mkdir(parents=True, exist_ok=True)
    
    # MCP server configuration for Claude Desktop - use virtual environment Python
    claude_config = {
        "mcpServers": {
            "web-content-analyzer": {
                "command": venv_python_path,
                "args": [main_py_path],
                "description": "A web content analyzer that can fetch and analyze content from URLs using FastMCP"
            }
        }
    }
    
    # Check if config file already exists
    if claude_config_file.exists():
        try:
            with open(claude_config_file, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
            
            # Merge configurations
            if "mcpServers" not in existing_config:
                existing_config["mcpServers"] = {}
            
            existing_config["mcpServers"]["web-content-analyzer"] = claude_config["mcpServers"]["web-content-analyzer"]
            claude_config = existing_config
            
            print("✓ Found existing Claude Desktop MCP configuration, merging...")
            
        except json.JSONDecodeError:
            print("⚠️  Warning: Existing config file is invalid JSON, creating new one...")
        except Exception as e:
            print(f"⚠️  Warning: Could not read existing config: {e}")
    
    # Write configuration
    try:
        with open(claude_config_file, 'w', encoding='utf-8') as f:
            json.dump(claude_config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Claude Desktop MCP configuration written to: {claude_config_file}")
        print(f"✅ Server path: {main_py_path}")
        print(f"✅ Python path: {venv_python_path}")
        
        print("\n📋 Next steps:")
        print("1. Restart Claude Desktop completely")
        print("2. Look for a tool icon in the chat interface")
        print("3. Start chatting and ask to analyze a URL!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing Claude Desktop configuration: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Web Content Analyzer MCP Server...\n")
    
    # Test if MCP library is available
    try:
        import sys
        sys.path.append('.')
        # Try to import the FastMCP version
        from main import MCP_AVAILABLE
        if MCP_AVAILABLE:
            print("✅ MCP library is available")
        else:
            print("❌ MCP library not found. Please install with: pip install mcp")
            return
    except Exception as e:
        print(f"❌ Error importing main module: {e}")
        return
    
    # Setup for both applications
    cursor_success = setup_cursor_mcp()
    claude_success = setup_claude_desktop()
    
    if cursor_success or claude_success:
        print("\n🎉 Setup complete! Your MCP server is ready to use.")
        print("\n🔧 If you encounter issues:")
        print("   - Make sure Python 3.7+ is installed")
        print("   - Make sure MCP library is installed: pip install mcp")
        print("   - Check that the file paths are correct")
        print("   - Restart Cursor/Claude Desktop after configuration")
        print("   - Test the server manually first")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 