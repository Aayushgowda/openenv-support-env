from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Request received")

        try:
            output = subprocess.getoutput("python -m scripts.baseline")
        except Exception as e:
            output = str(e)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(output.encode())


if __name__ == "__main__":
    print("Starting server on 0.0.0.0:7860")

    server = HTTPServer(("0.0.0.0", 7860), Handler)

    print("Server is LIVE")

    server.serve_forever()
