import sys
import requests
import subprocess
import os
import json


LATEST_RELEASE_URL = "https://api.github.com/repos/hgkrautsalat/pdf_to_excel_kpi/releases/latest"
DOWNLOAD_URL = "https://github.com/hgkrautsalat/pdf_to_excel_kpi/releases/download/"

APP_EXE = "app.exe"
LOCAL_VERSION_FILE = "version_local.json"

DIR_PATH:str = os.path.dirname(os.path.realpath(__file__)).split("launcher")[0]


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
    app_path = os.path.join(DIR_PATH, APP_EXE)

    subprocess.Popen(
        [app_path],
        cwd=DIR_PATH
    )
    # subprocess.Popen(
    #     # [sys.executable, os.path.join(APP_EXE, "main.py")],
    #     [sys.executable, APP_EXE],
    #     cwd=os.getcwd()
    # )


def download_app(url:str, version:str) -> None:
    print("⬇️ Lade neues Update herunter...")
    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()

        with open(os.path.join(DIR_PATH, APP_EXE), "wb") as f:
            f.write(response.content)

        save_local_version(version)  # Speichert die Version basierend auf der URL (z.B. "V_1.0.1")

    except Exception as e:
        print("❌ Fehler beim Herunterladen der neuen Version:", "\n",e)


def parse_version(version:str) -> tuple:
    version_list = version.split("_")[-1].split(".")
    version_map = map(int, version_list)
    version_tuple = tuple(version_map)
    return version_tuple


def save_local_version(version:str) -> None:
    local_path = os.path.join(DIR_PATH, LOCAL_VERSION_FILE)
    with open(local_path, "w") as f:
        json.dump({"version": version}, f)


def get_local_version(file_name:str)-> str:
    local_path:str = os.path.join(DIR_PATH, file_name)
    if not os.path.exists(local_path):
        save_local_version("V_0.0.0")
        return "V_0.0.0"

    with open(local_path, "r") as f:
        local_version:str = json.load(f)["version"]
        # print(f"Lokale Version aus Datei geladen: {local_version}")
        return local_version


def get_latest_release_tag(release_info:dict) -> str:
    try:
        tag_name:str = release_info["tag_name"]
        return tag_name
    except Exception as e:
        print("Fehler beim Abrufen der neuesten Release-Tag:", e)
        return "V_0.0.0"


def get_latest_release_info(release_url:str) -> dict:
    try:
        response:requests.Response = requests.get(release_url, timeout=5)
        response.raise_for_status()
        release_info:dict = response.json()
        return release_info
    except Exception as e:
        print("Fehler beim Abrufen der neuesten Release-Informationen:", e)
        return {}


def main():
    latest_release:dict         = get_latest_release_info(LATEST_RELEASE_URL)

    latest_release_tag_name:str    = get_latest_release_tag(latest_release)
    local_release_tag_name:str     = get_local_version(LOCAL_VERSION_FILE)

    latest_release_tag:tuple = parse_version(latest_release_tag_name)
    local_release_tag:tuple  = parse_version(local_release_tag_name)

    download_url:str = DOWNLOAD_URL + latest_release_tag_name + "/" + APP_EXE

    if (latest_release_tag > local_release_tag) or not os.path.exists(os.path.join(DIR_PATH, APP_EXE)):
        print(os.path.join(DIR_PATH, APP_EXE))
        print("🆕 Neues Update verfügbar!")
        download_app(download_url,latest_release_tag_name)
        print("✅ Update erfolgreich installiert")

    start_app()


if __name__ == "__main__":
    main()
