import http.server
import socketserver
import os

PORT = 8000
HTML_DIR = "templates"


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # ВСЕ GET-запросы должны возвращать contacts.html
        self.path = "/contacts.html"

        if self.path.endswith(".html"):
            try:
                with open(os.path.join(HTML_DIR, self.path.lstrip('/')), 'r', encoding='utf-8') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, message="File Not Found")
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print("Получены данные POST:", post_data)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('<h2>Данные получены!</h2>'.encode('utf-8'))


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Сервер запущен на http://localhost:{PORT}")
    httpd.serve_forever()
