project in progress ..


Manuscripts Scanner
An OCR project, to scan cyrillic and arabic materials, and translate them into Russian / English to preserve history of Uzbek culture and science works
Docker Compose is deploying a Python flask webserver on a Uvicorn (ASGI), and on the deployment server there is a nginx reverse proxy


Local testing (with Powershell / Mingw64 / WSL / Linux)


Create a venv in main folder
python3 -m venv .venv


Activate it
Windows powershell: .\.venv\Scripts\Activate.ps1
Windows bash (e.g. mingw64): source .venv/Scripts/activate
Linux / WSL: source .venv/bin/activate


Install all requirements
pip3 install -r requirements.txt


Running with environment variable


Add environment variable
Windows powershell: set TAHRIRCHI_API_TOKEN "TOKEN"
Windows bash (e.g. mingw64): export TAHRIRCHI_API_TOKEN="TOKEN"
Linux / WSL: export TAHRIRCHI_API_TOKEN="TOKEN"


Run the webserver as a python script or by uvicorn (both automatically start a uvicorn ASGI webserver on http://localhost:8000):
uvicorn app:asgi OR python app.py




Run without environment variable


Run the webserver as a python module (which automatically starts a uvicorn ASGI webserver on http://localhost:8000):
python3 app.py TAHRIRCHI_API_TOKEN=TOKEN
