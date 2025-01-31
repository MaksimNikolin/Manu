_**date of creation: December, 2024**_

# Manuscripts Scanner

An OCR project, to scan cyrillic and arabic materials, and translate them into Russian / English to preserve history of Uzbek culture and science works

Docker Compose is deploying a Python flask webserver on a Uvicorn (ASGI), and on the deployment server there is a nginx reverse proxy

-----

### Local testing (with Powershell / Mingw64 / WSL / Linux)

1. Create a venv in main folder

    `python3 -m venv .venv`

2. Activate it

    Windows powershell: `.\.venv\Scripts\Activate.ps1`

    Windows bash (e.g. mingw64): `source .venv/Scripts/activate`

    Linux / WSL: `source .venv/bin/activate`

3. Install all requirements

    `pip3 install -r requirements.txt`

4. Running with environment variable

    1. Add environment variable

        Windows powershell: `set TAHRIRCHI_API_TOKEN "TOKEN"`

        Windows bash (e.g. mingw64): `export TAHRIRCHI_API_TOKEN="TOKEN"`

        Linux / WSL: `export TAHRIRCHI_API_TOKEN="TOKEN"`

    2. Run the webserver as a python script or by uvicorn (both automatically start a uvicorn ASGI webserver on http://localhost:8000):
        
        `uvicorn app:asgi` OR `python app.py`

6. Run without environment variable

    1. Run the webserver as a python module (which automatically starts a uvicorn ASGI webserver on http://localhost:8000):
        
        `python3 app.py TAHRIRCHI_API_TOKEN=TOKEN`

