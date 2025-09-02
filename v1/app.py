import os
import sys
from application import app
import uvicorn
from asgiref.wsgi import WsgiToAsgi

app.config["TAHRIRCHI_API_TOKEN"] = os.environ.get("TAHRIRCHI_API_TOKEN")
app.config["TAHRIRCHI_API_BASE"] = "https://websocket.tahrirchi.uz/translate-v2"
app.config["APP_PATH"] = "./application"

# getting token from arguments
for arg in sys.argv:
    if arg.startswith("TAHRIRCHI_API_TOKEN="):
        app.config["TAHRIRCHI_API_TOKEN"] = arg[20:]

if not app.config["TAHRIRCHI_API_TOKEN"]:
    print("No Tahrirchi (translator) API token was provided")
    exit(1)

asgi = WsgiToAsgi(app)

if __name__ == "__main__":
    uvicorn.run(asgi)