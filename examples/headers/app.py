from MicroPie import Server

class Root(Server):
    def index(self):
        headers = [
            ("Content-Type", "text/html"),
            ("X-Content-Type-Options", "nosniff"),
            ("X-Frame-Options", "DENY"),
            ("X-XSS-Protection", "1; mode=block"),
            ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
            ("Content-Security-Policy", "default-src 'self'")
        ]
        return 200, "hello world", headers

app = Root()
wsgi_app = app.wsgi_app
