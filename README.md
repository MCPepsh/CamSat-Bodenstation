# CamSat-Bodenstation
## COM-Ports
Ich habe so programmiert, dass der Arduino auf COM4 liegt, sollte das nicht passen, muss das in [Datenziehen.bat](Visualisierung/Datenziehen.bat#L2) und in [steuerung.py](Teleskop-Steuerung/steuerung.py#L55) geändert werden. Sollten dafür zwei verschiedene Arduinos verwendet werden, muss der jeweilige COM-Port angegeben werden.

## Visualisierung 
Für die Visualisierung einfach [Alles.bat](Visualisierung/Alles.bat) ausführen.
Es kann sehr gut sein, dass dafür aber vorher noch [node.js](https://nodejs.org/en/) und einige Node-Packages installiert werden müssen.

## Steuerung
Für die Steuerung müssen in der [settings.json](Teleskop-Steuerung/settings.json) Position, Blickrichtung und Höhe über N. N. des Teleskops eingetragen werden.

Außerdem muss das Python-Package [pyserial](https://pypi.org/project/pyserial/) mit ```pip install pyserial``` installiert werden.

Um die Steuerung dann zu starten, muss lediglich die Datei [steuerung.py](Teleskop-Steuerung/steuerung.py) (Python 3.7.3) ausgeführt werden.
