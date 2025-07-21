# MyPV Heizstab Home Assistant Addon

Ein Home Assistant Addon, das als Proxy für MyPV Heizstab-Geräte fungiert und CORS-Probleme umgeht.

## Features

- Web-Interface für MyPV Heizstab
- CORS-Proxy-Funktionalität
- Konfigurierbare Geräte-IP
- Home Assistant Ingress-Integration
- Seitenleisten-Integration
- Einfache Installation und Konfiguration

## Installation

1. Fügen Sie dieses Repository zu Ihren Home Assistant Addon-Repositories hinzu
2. Installieren Sie das "MyPV Heizstab Interface" Addon
3. Konfigurieren Sie die IP-Adresse Ihres Heizstabs
4. Starten Sie das Addon

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
