# Spot

Semestrální práce z předmětu KIV/ZPP.

## Instalace

Naklonovat repozitář:

```sh
git clone https://github.com/https://github.com/Lorem-Ipsum-Spot/spot
```

Instalace závislostí (do virtuálního protředí):

```sh
pip install -r requirements.txt
```

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
