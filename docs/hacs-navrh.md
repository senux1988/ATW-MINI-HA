# Navrh HACS integracie pre ATW MINI / NeoRe Mini

## 1. Ciel

Vytvorit custom integraciu pre Home Assistant, ktoru bude mozne instalovat cez HACS a ktora bude:

- lokalne citat stav tepelneho cerpadla z `status.xml`
- podporovat viac zariadeni cez UI konfiguraciu
- rozumne mapovat XML polia na Home Assistant entity
- byt pripravena na neskorsie doplnenie zapisovych funkcii, ak sa podari identifikovat API pre ovladanie

Tento navrh je zalozeny na lokalnych zachytoch komunikacie zariadenia a na anonymizovanej XML fixture v [tests/fixtures/status.xml](../tests/fixtures/status.xml).

## 2. Zname vstupy

Zo zariadenia dnes vieme:

- IP zariadenia: lokalna IP adresa nastavena cez config flow
- endpoint: `/status.xml`
- metoda: `GET`
- autentifikacia: HTTP Basic Auth
- default login:
  - username: lokalne konfigurovatelny
  - password: lokalne konfigurovatelne
- XML encoding: `windows-1250`
- zariadenie: `ATW MINI`
- verzia: `UTI-IQCP v2.1`

Poznamka:

- Do GitHub repozitara nesmu ist realne prihlasovacie udaje ani lokalna IP.
- Adresar `inputs/` ma zostat lokalny a nebude commitovany.
- V integracii musi byt IP, username a password nastavitelne cez config entry.

## 3. Co budeme citat

Aktualne potvrdene polia zo `status.xml`:

| XML tag | Priklad | Navrhovany typ entity v HA | Navrhovany nazov | Poznamka |
|---|---:|---|---|---|
| `rtcc` | `Pi 20:15:23 10.04.2026` | `sensor` | Device time | Casova znacka zariadenia, diagnosticky sensor |
| `tep2` | `20.4?C` | `sensor` | Indoor temperature | Vnutorna teplota v dome |
| `tep3` | `39.2?C` | `sensor` | Water target temperature | Teplota, na ktoru tepelne cerpadlo hreje vodu |
| `tep4` | `0.0?C` | `sensor` | Temperature 4 | Neznamy vstup |
| `tep8` | `3.2?C` | `sensor` | Outdoor temperature | Vonkajsi teplotny senzor |
| `pwr` | `73 %` | `sensor` | Power level | Aktualny vykon tepelneho cerpadla v percentach, nie elektricky prikon |
| `st1` | `1` | `binary_sensor` | Status 1 | Stavovy bit, treba domapovat |
| `st2` | `1` | `binary_sensor` | Status 2 | Stavovy bit, treba domapovat |
| `st3` | `0` | `binary_sensor` | Status 3 | Stavovy bit, treba domapovat |
| `st4` | `0` | `binary_sensor` | Status 4 | Stavovy bit, treba domapovat |
| `st5` | `0` | `binary_sensor` | Status 5 | Stavovy bit, treba domapovat |

## 4. Navrh mapovania do Home Assistant

### 4.1 Prvy release

V prvom release odporucam citat:

- 1 senzor vnutornej teploty: `tep2`
- 1 senzor cielovej teploty vody: `tep3`
- 1 senzor neznamej teploty: `tep4`
- 1 senzor vonkajsej teploty: `tep8`
- 1 percentualny senzor vykonu: `pwr`
- 5 binarnych senzorov: `st1` az `st5`
- 1 diagnosticky senzor: `rtcc`

Tym ziskame funkcnu integraciu s korektne pomenovanymi hlavnymi hodnotami a opatrnym pristupom tam, kde vyznam este nepozname.

### 4.2 Nazvoslovie entit

Pri potvrdenych poliach odporucam pouzit vecne nazvy entit:

- `sensor.atw_mini_indoor_temperature`
- `sensor.atw_mini_water_target_temperature`
- `sensor.atw_mini_temperature_4`
- `sensor.atw_mini_outdoor_temperature`
- `sensor.atw_mini_power_level`
- `binary_sensor.atw_mini_status_1`
- `binary_sensor.atw_mini_status_2`
- `binary_sensor.atw_mini_status_3`
- `binary_sensor.atw_mini_status_4`
- `binary_sensor.atw_mini_status_5`
- `sensor.atw_mini_device_time`

Pre `tep4` a `st1..st5` zatial odporucam ponechat neutralne pomenovanie, kym nepotvrdime ich presny vyznam.

### 4.3 Atributy

Kazda entita moze mat spolocne extra atributy:

- `device_model: ATW MINI`
- `device_version: UTI-IQCP v2.1`
- `endpoint: /status.xml`
- `source_encoding: windows-1250`
- `raw_tag: tep2` a podobne
- `last_update_success`

## 5. Technicky navrh integracie

## 5.1 Typ integracie

Odporucam standardnu Home Assistant custom integraciu:

- domena: `atw_mini`
- instalacia: HACS Custom Repository
- platformy:
  - `sensor`
  - `binary_sensor`

Na zaciatok neodporucam robit:

- `climate`, pretoze nemame potvrdene zapisove API ani setpointy
- `water_heater`, z rovnakeho dovodu
- `switch`, pokial nepozname bezpecny write endpoint

## 5.2 Vnutorna architektura

Navrh modulov:

```text
custom_components/atw_mini/
  __init__.py
  manifest.json
  const.py
  config_flow.py
  coordinator.py
  entity.py
  sensor.py
  binary_sensor.py
  api.py
  diagnostics.py
  translations/en.json
```

Zodpovednosti:

- `api.py`
  - HTTP komunikacia cez `aiohttp`
  - Basic Auth
  - stiahnutie `status.xml`
  - dekodovanie `windows-1250`
  - parsovanie XML
  - cistenie hodnot ako `20.4?C` alebo `73 %`

- `coordinator.py`
  - `DataUpdateCoordinator`
  - centralne obnovovanie dat, napr. kazdych 30 sekund
  - jednotne spracovanie chyb a dostupnosti

- `sensor.py`
  - teploty, percento vykonu, cas zariadenia

- `binary_sensor.py`
  - stavove bity `st1..st5`

- `config_flow.py`
  - host/IP
  - username
  - password
  - scan interval volitelne
  - test spojenia pocas konfiguracie

- `diagnostics.py`
  - anonymizovany export stavu pre debug

## 5.3 Update interval

Odporucany start:

- default `scan_interval`: 30 sekund

Dovody:

- XML je male
- lokalne citanie po LAN je lacne
- hodnoty tepelneho cerpadla sa nemenia po sekundach tak casto, aby bolo nutne citat agresivnejsie

## 5.4 Robustnost parsera

Parser musi zvladnut:

- odpoved bez niektorych tagov
- teplotne hodnoty s netypickym znakom `?C`
- medzery okolo hodnot
- percenta v tvare `73 %`
- docasnu nedostupnost zariadenia
- nevalidne XML alebo chybne kodovanie

Normalizacia hodnot:

- `20.4?C` -> `20.4`
- `73 %` -> `73`
- `1` / `0` -> `True` / `False` pre `binary_sensor`

## 6. Polozky, ktore este treba potvrdit

Pred implementaciou druhej fazy bude dobre zistit:

- co presne znamena `tep4`
- co presne znamenaju bity `st1` az `st5`
- ci existuju dalsie XML endpointy
- ci existuje write API pre zmenu rezimu, teploty alebo zapnutia
- ci zariadenie pouziva stale tie iste tagy vo vsetkych stavoch

Odporucany prakticky postup mapovania:

- logovat XML pri roznych realnych stavoch zariadenia
- porovnat zmeny pri kureni, ohreve TUV, standby a odmrazovani
- k stavom si zapisat, co ukazuje fyzicky panel

## 7. GitHub a HACS priprava

Aby bol projekt rovno publikovatelny, odporucam tuto strukturu repozitara:

```text
.
+-- README.md
+-- LICENSE
+-- .gitignore
+-- hacs.json
+-- custom_components/
|   +-- atw_mini/
|       +-- __init__.py
|       +-- manifest.json
|       +-- const.py
|       +-- config_flow.py
|       +-- coordinator.py
|       +-- entity.py
|       +-- sensor.py
|       +-- binary_sensor.py
|       +-- api.py
|       +-- diagnostics.py
|       +-- translations/
|           +-- en.json
+-- tests/
    +-- test_api.py
    +-- test_sensor.py
    +-- fixtures/
        +-- status.xml
```

### 7.1 `hacs.json`

Minimalne:

- `name`
- `render_readme`
- `homeassistant`
- `country` volitelne

### 7.2 `manifest.json`

Minimalne:

- `domain`
- `name`
- `version`
- `documentation`
- `issue_tracker`
- `config_flow: true`
- `requirements: []`
- `codeowners`
- `iot_class: local_polling`

Detailne GitHub projektove mapovanie je v [docs/github-project-plan.md](github-project-plan.md).

## 8. Navrh implementacnych faz

### Faza 1

- pripravit repozitar
- vytvorit custom integraciu s `sensor` a `binary_sensor`
- nacitat `status.xml`
- pridat config flow
- otestovat na jednom realnom zariadeni

### Faza 2

- pomenovat entity podla realneho vyznamu
- doplnit `device_info`
- pridat diagnostiku a kvalitne logovanie
- pridat unit testy s fixture XML

### Faza 3

- ak najdeme write API, pridat `switch`, `select`, `number` alebo `climate`
- mozno pridat servis na rucny refresh alebo diagnosticky dump

## 9. Odporucanie k bezpecnosti

- nikdy necommitovat realnu IP, username ani password
- do testov dat anonymizovanu XML fixture
- do README dat konfiguraciu len s placeholdermi
- ak bude v logu raw XML, citlive udaje maskovat

## 10. Co by som spravil dalej

Najrozumnejsi dalsi krok je:

1. vytvorit skeleton HACS integracie
2. implementovat `api.py` a parser `status.xml`
3. vystavit potvrdene entity
4. pripravit fixture test s aktualnym XML

Ak budeme chciet, v dalsom kroku uz viem z tohto navrhu rovno vygenerovat aj kostru integracie `custom_components/atw_mini/` pripravenou na commit do GitHub repozitara.
