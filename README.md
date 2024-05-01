# Spot

Semestrální práce z předmětu KIV/ZPP.

## Instalace

Naklonovat repozitář:

```sh
git clone https://github.com/Lorem-Ipsum-Spot/spot
```

Instalace závislostí (do virtuálního protředí):

```sh
pip install -r requirements.txt
```

### VOSK model

Instalace modelu na rozpoznání řeči (přejmenovat na "model" a dát do rootu projektu):
[VOSK Models - Czech](https://alphacephei.com/vosk/models/vosk-model-small-cs-0.4-rhasspy.zip)

Např. na Linuxu:

```sh
curl "https://alphacephei.com/vosk/models/vosk-model-small-cs-0.4-rhasspy.zip" -o model.zip
unzip model.zip
mv -iv vosk-model-small-cs-0.4-rhasspy model
```

### PyAudio

Na Debianových systémech (Ubuntu, RaspbianOS) nebo na jiném Unixu občas
instalace selže, protože neexistuje `"pyaudio.h"`. Potom je potřeba
nainstalovat `PyAudio` ze systémového správce balíčků.

```sh
sudo apt install python3-pyaudio
```

Poté `PyAudio` dočasně vymazat z `requirements.txt` a znovu spustit
`pip install` jako předtím.

## Spuštění

```txt
python -m spot [-h] [-v] [-t TIMEOUT] [-c CREDENTIALS] hostname

positional arguments:
  hostname              Hostname or address of robot, e.g. "192.168.80.3"

options:
  -h, --help            show help message and exit
  -v, --verbose         Print debug-level messages
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout in seconds
  -c CREDENTIALS, --credentials CREDENTIALS
                        Credentials file
```

Credentials file má formát:

```txt
name
password
```

## Struktura

### [cli](spot/cli/README.md)

Hlavní spustitelný modul, zpracovává argumenty příkazu a spouští všechny ostatní moduly.

### [curses](spot/curses/README.md)

Terminal user interface (TUI) library for EStop client.

### [audio](spot/audio/README.md)

Using Google speech API for audio recognition.
