import sys
import requests
import subprocess
import os
import json
import time

# ---- Konfigurationsvariablen ----
# URLs für die GitHub API und den Download der neuesten Version
LATEST_RELEASE_URL = "https://api.github.com/repos/hgkrautsalat/pdf_to_excel_kpi/releases/latest"
DOWNLOAD_URL = "https://github.com/hgkrautsalat/pdf_to_excel_kpi/releases/download/"

# Dateiname der ausführbaren Hauptanwendung und der lokalen Versionsdatei
APP_EXE = "app.exe"
LOCAL_VERSION_FILE = "version_local.json"

# Bestimmt den Pfad zum lokalen AppData-Verzeichnis und den Pfad zum Anwendungsordner
# Anwendungsordner im lokalen AppData-Verzeichnis unter "Programs/KPIConverter"
# Wird über Setup.iss festgelegt
# Verwenden wenn launcher.exe global unter C:\Program Files gespeichert wird
#------------------------------
# BASE_DIR_PATH = os.environ.get("LOCALAPPDATA")
# APP_DIR_PATH = os.path.join(BASE_DIR_PATH, "Programs", "KPIConverter")
#------------------------------
# Verwenden wenn launcher.exe lokal unter C:\Users\<USER>\AppData\Local\Programs gespeichert wird
APP_DIR_PATH = os.path.dirname(os.path.realpath(__file__)).split("launcher")[0]
#------------------------------
# ---- ---------------------- ----


def start_app() -> None:
    """
    Startet die Hauptanwendung in einem separaten Prozess.

    Diese Funktion führt folgende Schritte aus:
    - Gibt eine Startmeldung aus
    - Erstellt einen neuen Subprozess mit subprocess.Popen
    - Führt die app.exe direkt aus
    - Setzt APP_DIR_PATH als Ausführungskontext (cwd) für den Prozess

    Returns:
        None

    Raises:
        FileNotFoundError: Wenn die app.exe Datei nicht im angegebenen Pfad existiert
        PermissionError: Wenn keine Berechtigung zum Ausführen der Datei besteht
    """
    print("Starte Anwendung...")

    # Setzt den Pfad zur ausführbaren Datei der Hauptanwendung auf APP_EXE im APP_DIR_PATH
    app_path = os.path.join(APP_DIR_PATH, APP_EXE)

    subprocess.Popen(
        [app_path],
        cwd=APP_DIR_PATH
    )


def download_app(url:str, version:str) -> bool:
    """
    Lädt die neueste Version der Hauptanwendung und die Versionsdatei von der angegebenen URL
    herunter und speichert sie im Anwendungsordner.

    :param url: URL unter welchem das aktuelle Release abliegt
    :type url: str
    :param version: Versionsnummer der herunterzuladenden Anwendung
    :type version: str
    :return: True, wenn der Download erfolgreich war, sonst False
    :rtype: bool
    """
    print("⬇️ Lade neues Update herunter...")
    try:
        # Sendet eine GET-Anfrage an die angegebene URL,
        # um die neueste Version der Anwendung herunterzuladen
        response: requests.Response = requests.get(url)
        response.raise_for_status()

        # Überprüft, ob der Anwendungsordner existiert, und erstellt ihn gegebenenfalls
        if not os.path.exists(APP_DIR_PATH):
            os.makedirs(APP_DIR_PATH)

        # Speichert die heruntergeladene ausführbare Datei der Hauptanwendung im Anwendungsordner
        with open(os.path.join(APP_DIR_PATH, APP_EXE), "wb") as f:
            f.write(response.content)
        # Speichert die Versionsnummer der heruntergeladenen Anwendung in der
        # lokalen Versionsdatei version_local.json
        save_local_version(version)
        return True

    except Exception as e:
        print("❌ Fehler beim Herunterladen der neuen Version:", "\n",e)
        return False


def parse_version(version:str) -> tuple:
    """
    Verarbeitet die Versionsnummer in der Form "V_X.Y.Z" und gibt sie als Tuple (X, Y, Z) zurück.

    :param version: Versionsnummer im Format "V_X.Y.Z"
    :type version: str
    :return: Tuple mit den einzelnen Versionsnummern (X, Y, Z)
    :rtype: tuple
    """
    # Entfernt den Präfix "V_" und teilt die Versionsnummer in ihre Bestandteile X, Y und Z auf
    version_list = version.split("_")[-1].split(".")
    # Wandelt die einzelnen Bestandteile der Versionsnummer von Strings in Integers um
    version_map = map(int, version_list)
    # Gibt sie als Tuple zurück
    version_tuple = tuple(version_map)
    return version_tuple


def save_local_version(version:str) -> None:
    """
    Speichert die lokale Versionsnummer in einer JSON-Datei.

    :param version: Versionsnummer im Format "V_X.Y.Z"
    :type version: str
    :return: None
    """

    # Bestimmt den Pfad zur lokalen Versionsdatei version_local.json im Anwendungsordner
    local_path:str = os.path.join(APP_DIR_PATH, LOCAL_VERSION_FILE)

    # Speichert die Versionsnummer in der JSON-Datei im Format {"version": "V_X.Y.Z"}
    with open(local_path, "w") as f:
        print(f"Speichere lokale Version {version} in Datei: {local_path}")
        json.dump({"version": version}, f)


def get_local_version(file_name:str)-> str:
    """
    Liest die lokale Versionsnummer aus einer JSON-Datei aus.

    :param file_name: Name der Datei, aus der die Versionsnummer gelesen werden soll
    :type file_name: str
    :return: Versionsnummer im Format "V_X.Y.Z"
    :rtype: str
    """

    # Bestimmt den Pfad zur lokalen Versionsdatei version_local.json im Anwendungsordner
    local_path:str = os.path.join(APP_DIR_PATH, file_name)

    # Überprüft, ob die lokale Versionsdatei existiert
    # und gibt "V_0.0.0" zurück, wenn sie nicht existiert
    if not os.path.exists(local_path):
        return "V_0.0.0"

    # Liest die Versionsnummer aus der JSON-Datei im Format {"version": "V_X.Y.Z"} und gibt sie zurück
    with open(local_path, "r") as f:
        local_version:str = json.load(f)["version"]
        return local_version


def get_latest_release_tag(release_info:dict) -> str:
    """
    Extrahiert den Tag-Namen der neuesten Release-Version aus den Release-Informationen.

    :param release_info: Informationen zur neuesten Release-Version
    :type release_info: dict
    :return: Tag-Name der neuesten Release-Version
    :rtype: str
    """
    try:
        # Extrahiert den Tag-Namen der neuesten Release-Version aus den Release-Informationen
        tag_name:str = release_info["tag_name"]
        return tag_name
    except Exception as e:
        print("Fehler beim Abrufen der neuesten Release-Tag:", e)
        return "V_0.0.0"


def get_latest_release_info(release_url:str) -> dict:
    """
    Ruft die Informationen zur neuesten Release-Version von der angegebenen URL ab.
    Greift auf die GitHub API zu, um die Informationen zur neuesten Release-Version zu erhalten.

    :param release_url: URL zur neuesten Release-Version
    :type release_url: str
    :return: Informationen zur neuesten Release-Version
    :rtype: dict
    """
    try:
        # Sendet eine GET-Anfrage an die angegebene URL, um die Informationen zur
        # neuesten Release-Version abzurufen
        response:requests.Response = requests.get(release_url, timeout=5)
        # Überprüft, ob die Anfrage erfolgreich war
        response.raise_for_status()
        # Gibt die Release-Informationen als Dictionary zurück
        release_info:dict = response.json()
        return release_info
    except Exception as e:
        print("Fehler beim Abrufen der neuesten Release-Informationen:", e)
        return {}


def main():
    # Ruft die Informationen zur neuesten Release-Version von der GitHub API ab
    latest_release:dict             = get_latest_release_info(LATEST_RELEASE_URL)
    # Extrahiert den Tag-Namen der neuesten Release-Version aus den Release-Informationen
    latest_release_tag_name:str     = get_latest_release_tag(latest_release)
    # Liest die lokale Versionsnummer aus der lokalen Versionsdatei version_local.json aus
    local_release_tag_name:str      = get_local_version(LOCAL_VERSION_FILE)

    # Verarbeitet die Versionsnummern der neuesten Release-Version
    # und der lokalen Version in Tuples (X, Y, Z)
    latest_release_tag:tuple        = parse_version(latest_release_tag_name)
    local_release_tag:tuple         = parse_version(local_release_tag_name)

    # Bestimmt die Download-URL für die neueste Release-Version basierend auf dem Tag-Namen
    # der neuesten Release-Version
    download_url:str                = DOWNLOAD_URL + latest_release_tag_name + "/" + APP_EXE

    # Vergleicht die Versionsnummern der neuesten Release-Version und der lokalen Version
    # und prüft, ob eine APP_EXE Datei im Anwendungsordner existiert
    if (latest_release_tag > local_release_tag) or not os.path.exists(os.path.join(APP_DIR_PATH, APP_EXE)):
        print("🆕 Neues Update verfügbar!")
        # Wenn die neueste Release-Version neuer ist als die lokale Version oder
        # die app.exe Datei nicht existiert,
        if download_app(download_url,latest_release_tag_name):
            print("✅ Update erfolgreich installiert")

    # Startet die Hauptanwendung in einem separaten Prozess
    start_app()


if __name__ == "__main__":
    main()
