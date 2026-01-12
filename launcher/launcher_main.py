import requests
import subprocess
import os
import sys
import json

APP_EXE = "app.exe"
VERSION_URL = "https://raw.githubusercontent.com/hgkrautsalat/pdf_to_excel_kpi/main/version.json"
LOCAL_VERSION = "1.0.0"

def check_for_update()-> None:
    try:
        r: requests.Response = requests.get(VERSION_URL, timeout=5)
        data:requests.Any = r.json()

        if data["version"] != LOCAL_VERSION:
            download_update(data["exe_url"])
    except Exception as e:
        print()
        print("Kein Internet / Fehler → normal starten")
        print()
        print('Exception:','\n', e)
        print()
        print()

def download_update(url):
    r = requests.get(url)
    with open(APP_EXE, "wb") as f:
        f.write(r.content)

def start_app():
    subprocess.Popen(
        [sys.executable, os.path.join("converter", "main.py")],
        cwd=os.getcwd()
    )

if __name__ == "__main__":
    check_for_update()
    start_app()

# # launcher/launcher_main.py
# import requests
# import subprocess
# import os
# import json

# VERSION_URL = "https://raw.githubusercontent.com/DEIN_USER/DEIN_REPO/main/version.json"
# APP_EXE = "app.exe"

# def start_app():
#     subprocess.Popen([APP_EXE], cwd=os.getcwd())

# def main():
#     r = requests.get(VERSION_URL)
#     data = r.json()

#     if not os.path.exists(APP_EXE):
#         print("App fehlt – Download...")
#         download(data["download_url"])

#     start_app()

# def download(url):
#     r = requests.get(url)
#     with open(APP_EXE, "wb") as f:
#         f.write(r.content)

# if __name__ == "__main__":
#     main()
