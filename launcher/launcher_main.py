# import requests
# import subprocess
# import os
# import sys
# import json

# APP_EXE = "app.exe"
# VERSION_URL = "https://raw.githubusercontent.com/hgkrautsalat/pdf_to_excel_kpi/main/version.json"
# LOCAL_VERSION = "1.0.0"

# def check_for_update()-> None:
#     try:
#         r: requests.Response = requests.get(VERSION_URL, timeout=5)
#         data:requests.Any = r.json()

#         if data["version"] != LOCAL_VERSION:
#             download_update(data["exe_url"])
#     except Exception as e:
#         print()
#         print("Kein Internet / Fehler → normal starten")
#         print()
#         print('Exception:','\n', e)
#         print()
#         print()

# def download_update(url):
#     r = requests.get(url)
#     with open(APP_EXE, "wb") as f:
#         f.write(r.content)

# def start_app():
#     subprocess.Popen(
#         [sys.executable, os.path.join("converter", "main.py")],
#         cwd=os.getcwd()
#     )

# if __name__ == "__main__":
#     check_for_update()
#     start_app()
###################################################################################################################
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


import sys
import requests
import subprocess
import os
import json

VERSION_URL = "https://raw.githubusercontent.com/hgkrautsalat/pdf_to_excel_kpi/main/version.json"

APP_EXE = "converter.exe"
LOCAL_VERSION_FILE = "version.json"


def parse_version(v):
    return tuple(map(int, v.split(".")))


def load_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"

    with open(LOCAL_VERSION_FILE, "r") as f:
        return json.load(f)["version"]


def save_local_version(version):
    with open(LOCAL_VERSION_FILE, "w") as f:
        json.dump({"version": version}, f)


def download_app(url):
    print("⬇️ Lade neues Update herunter...")
    r = requests.get(url)
    r.raise_for_status()

    with open(APP_EXE, "wb") as f:
        f.write(r.content)


def start_app():
    """
    Startet die Hauptanwendung in einem separaten Prozess.

    Diese Funktion führt folgende Schritte aus:
    - Gibt eine Startmeldung mit Raketen-Emoji auf der Konsole aus
    - Erstellt einen neuen Subprozess mit subprocess.Popen
    - Führt die converter.exe direkt aus (nicht mit Python)
    - Setzt das aktuelle Arbeitsverzeichnis (cwd) als Ausführungskontext für den Prozess

    Returns:
        None

    Raises:
        FileNotFoundError: Wenn die converter.exe Datei nicht im angegebenen Pfad existiert
        PermissionError: Wenn keine Berechtigung zum Ausführen der Datei besteht
    """
    print("🚀 Starte Anwendung...")
    subprocess.Popen(
        [APP_EXE],
        cwd=os.getcwd()
    )
    # subprocess.Popen(
    #     # [sys.executable, os.path.join(APP_EXE, "main.py")],
    #     [sys.executable, APP_EXE],
    #     cwd=os.getcwd()
    # )


def main():
    print("🔍 Prüfe auf Updates...")

    remote = requests.get(VERSION_URL).json()
    remote_version = remote["version"]
    download_url = remote["exe_url"]

    local_version = load_local_version()

    print(f"Lokale Version: {local_version}")
    print(f"Remote Version: {remote_version}")

    if parse_version(remote_version) > parse_version(local_version):
        print("🆕 Neues Update verfügbar!")
        download_app(download_url)
        save_local_version(remote_version)
    else:
        print("✅ Keine Updates verfügbar")

    # if not os.path.exists(APP_EXE):
    #     raise RuntimeError("converter.exe fehlt!")

    start_app()


if __name__ == "__main__":
    main()
