import requests
import json

BASE_URL = "http://172.18.0.2:5000"  # Basierend auf dem Flask-Server-Setup
ADMIN_PASSWORD = "admin"  # Admin-Passwort für autorisierte Aktionen


def generate_license():
    """Testet die Generierung eines Lizenzschlüssels."""
    url = f"{BASE_URL}/generate"
    payload = {"password": ADMIN_PASSWORD}
    response = requests.post(url, json=payload)
    print(f"GENERATE LICENSE: {response.status_code}")
    response_data = response.json()
    print(response_data)
    return response_data.get('key')  # Rückgabe des generierten Lizenzschlüssels


def list_licenses():
    """Testet die Auflistung aller Lizenzschlüssel."""
    url = f"{BASE_URL}/list"
    params = {"password": ADMIN_PASSWORD}
    response = requests.get(url, params=params)
    print(f"LIST LICENSES: {response.status_code}")
    licenses = response.json()
    print(json.dumps(licenses, indent=4))
    return licenses  # Rückgabe der Liste der Lizenzen


def delete_license(key):
    """Testet das Löschen eines Lizenzschlüssels."""
    url = f"{BASE_URL}/delete"
    payload = {"password": ADMIN_PASSWORD, "key": key}
    response = requests.delete(url, json=payload)
    print(f"DELETE LICENSE: {response.status_code}")
    print(response.json())


def link_license(key, username):
    """Testet das Verknüpfen eines Minecraft-Benutzernamens mit einem Lizenzschlüssel."""
    url = f"{BASE_URL}/link"
    payload = {"key": key, "username": username}
    response = requests.post(url, json=payload)
    print(f"LINK LICENSE: {response.status_code}")
    response_data = response.json()
    print(response_data)
    return response_data.get('uuid')  # Rückgabe der UUID aus der Antwort


def verify_license(key, uuid):
    """Testet die Überprüfung eines Lizenzschlüssels mit einer UUID."""
    url = f"{BASE_URL}/verify"
    payload = {"key": key, "uuid": uuid}
    response = requests.post(url, json=payload)
    print(f"VERIFY LICENSE: {response.status_code}")
    response_data = response.json()
    print(response_data)
    return response_data.get('success')  # Rückgabe, ob die Lizenz gültig ist


def automated_tests():
    print("Automatisierter Test startet...")

    # Schritt 1: Lizenz generieren
    print("\n1. Generiere Lizenz...")
    generated_key = generate_license()
    if not generated_key:
        print("Fehler: Ein Lizenzschlüssel konnte nicht generiert werden.")
        return

    # Schritt 2: Lizenzen auflisten
    print("\n2. Lizenzen auflisten...")
    licenses = list_licenses()
    if not any(license_.get('key') == generated_key for license_ in licenses):
        print("Fehler: Der generierte Lizenzschlüssel wurde nicht aufgeführt.")
        return

    # Schritt 3: Lizenz verknüpfen
    print("\n3. Lizenz verknüpfen...")
    username = "TestUser"  # Fester Testbenutzername
    linked_uuid = link_license(generated_key, username)
    if not linked_uuid:
        print("Fehler: Die Lizenz konnte nicht verknüpft werden.")
        return

    # Schritt 4: Lizenzen erneut auflisten
    print("\n4. Lizenzen erneut auflisten, um die Verknüpfung zu überprüfen...")
    licenses = list_licenses()
    if not any(license_.get('key') == generated_key and license_.get('uuid') == linked_uuid for license_ in licenses):
        print("Fehler: Die Verknüpfung der Lizenz wurde nicht korrekt gespeichert.")
        return

    # Schritt 5: Lizenz verifizieren
    print("\n5. Lizenz verifizieren...")
    is_valid = verify_license(generated_key, linked_uuid)
    if not is_valid:
        print("Fehler: Die Lizenz konnte nicht verifiziert werden.")
        return

    # Schritt 6: Lizenz löschen
    print("\n6. Lizenz löschen...")
    delete_license(generated_key)

    # Schritt 7: Lizenzen erneut auflisten, um die Löschung zu überprüfen
    print("\n7. Lizenzen auflisten, um die Löschung zu überprüfen...")
    licenses = list_licenses()
    if any(license_.get('key') == generated_key for license_ in licenses):
        print("Fehler: Die Lizenz wurde nicht gelöscht.")
    else:
        print("Der Test war erfolgreich: Die Lizenz wurde erfolgreich getestet und gelöscht.")


def menu():
    """Menüauswahl für den Nutzer, um verschiedene Funktionen einzeln auszuführen."""
    while True:
        print("\n==== Lizenz-System Menü ====")
        print("1. Generiere Lizenz")
        print("2. Lizenzen auflisten")
        print("3. Lizenz verknüpfen")
        print("4. Lizenz verifizieren")
        print("5. Lizenz löschen")
        print("6. Automatisierte Tests ausführen")
        print("0. Beenden")
        choice = input("Wähle eine Option: ")

        if choice == "1":  # Lizenz generieren
            print("\n1. Generiere Lizenz...")
            generate_license()

        elif choice == "2":  # Lizenzen auflisten
            print("\n2. Lizenzen auflisten...")
            list_licenses()

        elif choice == "3":  # Lizenz verknüpfen
            print("\n3. Lizenz verknüpfen...")
            key = input("Gib den Lizenzschlüssel ein: ")
            username = input("Gib den Minecraft-Benutzernamen ein: ")
            link_license(key, username)

        elif choice == "4":  # Lizenz verifizieren
            print("\n4. Lizenz verifizieren...")
            key = input("Gib den zu überprüfenden Lizenzschlüssel ein: ")
            uuid = input("Gib die zu überprüfende UUID ein: ")
            verify_license(key, uuid)

        elif choice == "5":  # Lizenz löschen
            print("\n5. Lizenz löschen...")
            key = input("Gib den zu löschenden Lizenzschlüssel ein: ")
            delete_license(key)

        elif choice == "6":  # Automatisierte Tests
            print("\n6. Automatisierte Tests ausführen...")
            automated_tests()

        elif choice == "0":  # Beenden
            print("Programm beendet.")
            break

        else:
            print("Ungültige Auswahl, bitte erneut versuchen.")


if __name__ == "__main__":
    menu()
