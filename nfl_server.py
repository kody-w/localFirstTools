import http.server
import socketserver
import urllib.request
import json
import sys

PORT = 8000

class NFLProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the main HTML file
        if self.path == '/' or self.path == '/nfl-live-stats.html':
            self.path = '/nfl-live-stats.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
            
        # Proxy API requests
        if self.path.startswith('/api/'):
            target_url = ""
            
            if self.path == '/api/scoreboard':
                target_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
            elif self.path == '/api/stats':
                target_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/statistics"
            elif self.path == '/api/news':
                target_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/news"
            
            if target_url:
                try:
                    with urllib.request.urlopen(target_url) as response:
                        data = response.read()
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(data)
                except Exception as e:
                    self.send_error(500, str(e))
                return

        # Default behavior for other files (css, js, etc)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

print(f"Starting NFL Stats Server at http://localhost:{PORT}")
print("Press Ctrl+C to stop")

with socketserver.TCPServer(("", PORT), NFLProxyHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
