#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加CORS头部，允许跨域请求
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # 如果请求根路径，重定向到index.html
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

def start_server(port=8000):
    """启动本地HTTP服务器"""
    # 确保在正确的目录中
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # 检查必要文件是否存在
    required_files = [
        'index.html',
        '1-初中-顺序.json',
        '2-高中-顺序.json', 
        '3-CET4-顺序.json',
        '4-CET6-顺序.json',
        '6-托福-顺序.json',
        '7-SAT-顺序.json'
    ]
    
    missing_files = [f for f in required_files if not Path(f).exists()]
    if missing_files:
        print(f"❌ 缺少以下文件: {', '.join(missing_files)}")
        return
    
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 词汇学习系统已启动!")
            print(f"📍 服务器地址: http://localhost:{port}")
            print(f"📂 服务目录: {os.getcwd()}")
            print(f"\n🌐 正在自动打开浏览器...")
            print(f"💡 按 Ctrl+C 停止服务器")
            print("=" * 50)
            
            # 自动打开浏览器
            webbrowser.open(f'http://localhost:{port}')
            
            # 启动服务器
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 服务器已停止")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ 端口 {port} 已被占用，尝试使用端口 {port + 1}")
            start_server(port + 1)
        else:
            print(f"❌ 启动服务器失败: {e}")

if __name__ == "__main__":
    print("🎓 智能词汇学习系统 - 本地服务器")
    print("=" * 50)
    start_server()