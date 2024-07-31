from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        chat_id = data['message']['chat']['id']
        text = data['message']['text']

        if text.startswith('/paste'):
            links = text.split()[1:]
            url = f"https://{self.headers['Host']}/webapp?link1={links[0]}&link2={links[1]}"
            response = {
                "method": "sendMessage",
                "chat_id": chat_id,
                "text": f"Click to open the webapp: {url}",
                "reply_markup": {"inline_keyboard": [[{"text": "Open Webapp", "web_app": {"url": url}}]]}
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Invalid command".encode('utf-8'))
