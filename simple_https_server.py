#!/usr/bin/env python3

import http.server
import ssl
import socketserver
import os

# Configuration
PORT = 8443
CERT_FILE = 'cert.pem'
KEY_FILE = 'key.pem'

class SimpleHTTPSServer:
    def __init__(self, port=PORT):
        self.port = port
        
    def create_ssl_certificates(self):
        """Create self-signed SSL certificates if they don't exist"""
        if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
            print("Creating self-signed SSL certificates...")
            import subprocess
            
            # Create self-signed certificate valid for localhost
            cmd = [
                'openssl', 'req', '-x509', '-newkey', 'rsa:4096', '-keyout', KEY_FILE,
                '-out', CERT_FILE, '-days', '365', '-nodes', '-subj',
                '/C=US/ST=State/L=City/O=Organization/CN=localhost'
            ]
            
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"✅ SSL certificates created: {CERT_FILE}, {KEY_FILE}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to create SSL certificates: {e}")
                print("Please install OpenSSL or create certificates manually")
                return False
        else:
            print("✅ SSL certificates already exist")
        return True
        
    def start_server(self):
        """Start the HTTPS server"""
        if not self.create_ssl_certificates():
            return
            
        try:
            # Create HTTP server
            Handler = http.server.SimpleHTTPRequestHandler
            
            with socketserver.TCPServer(("", self.port), Handler) as httpd:
                # Wrap with SSL
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                context.load_cert_chain(CERT_FILE, KEY_FILE)
                httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
                
                print("=" * 60)
                print("Simple HTTPS Server for DocuSign Button")
                print("=" * 60)
                print(f"🌐 Server URL: https://localhost:{self.port}")
                print(f"📁 Serving files from: {os.getcwd()}")
                print(f"🔒 SSL certificates: {CERT_FILE}, {KEY_FILE}")
                print("\nPress Ctrl+C to stop the server")
                print("=" * 60)
                
                # Start serving
                httpd.serve_forever()
                
        except KeyboardInterrupt:
            print("\n\nServer stopped.")
        except Exception as e:
            print(f"❌ Server error: {e}")

if __name__ == "__main__":
    server = SimpleHTTPSServer()
    server.start_server()