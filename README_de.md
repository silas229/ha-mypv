# MyPV Home Assistant Addon

Ein  Addon, das die MyPV-App in Home Assistant integriert.

## Unterstützte Geräte

- MyPV ELWA 2
- Steuere gerne die HTML-Seite für ein anderes Modell bei

## Features

- Web-Interface für MyPV Heizstab
- Konfigurierbare Geräte-IP
- Home Assistant Ingress-Integration
- Seitenleisten-Integration
- Einfache Installation und Konfiguration

## Installation

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsilas229%2Fha-mypv)

1. Füge dieses [Repository](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsilas229%2Fha-mypv) zu deinen Home Assistant Addon-Repositories hinzu (oder klicke auf den oberen Button)
2. Installiere das "MyPV" Addon
3. Konfiguriere die IP-Adresse deines Heizstabs
4. Starte das Addon

## Konfiguration

- `device_ip`: IP-Adresse des MyPV Heizstabs (Standard: 192.168.1.100)
- `device_port`: Port des MyPV Heizstabs (Standard: 80)
- `log_level`: Log-Level für das Addon (info, debug, etc.)

## Verwendung

Nach der Installation und Konfiguration erscheint das Interface automatisch in der Home Assistant Seitenleiste. Das Addon verwendet Home Assistant Ingress für sichere und nahtlose Integration.

### Zugriff über Ingress

Das Interface ist über Home Assistant Ingress verfügbar und erscheint als Panel in der Seitenleiste mit dem Namen "MyPV Heizstab".

### API-Endpoints

Das Addon stellt diese MyPV-spezifischen Endpoints zur Verfügung:

- `/mypv_dev.jsn` - Geräteinformationen
- `/data.jsn` - Aktuelle Sensordaten
- `/chart.jsn` - Chart/historische Daten
- `/setup.jsn` - Setup-Konfiguration
- `/api/wifidata.jsn` - WiFi-Status-Daten

## Entwicklung

Das Addon verwendet Python Flask als Proxy-Server und stellt die originale HTML-Datei als statisches Asset zur Verfügung. Der Proxy-Adapter intercepted alle API-Aufrufe und leitet sie über den Flask-Server weiter.
