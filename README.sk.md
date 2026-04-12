# ATW MINI Home Assistant Integracia

![ATW MINI icon](assets/atw-mini-icon.svg)

Vlastna integracia pre Home Assistant pre tepelne cerpadlo ATW MINI / NeoRe Mini s lokalnou HTTP/XML/HTML komunikaciou.

Anglicka verzia je v [README.md](/Users/peter.glemba/Documents/Projekty/ATW-MINI-HA/README.md).

## Aktualny Stav

Integracia sa uz vie lokalne pripojit na zariadenie a citat viacero endpointov.

Aktualna verzia pluginu:
- `0.3.0`

Aktualny rozsah:
- read-only
- lokalny polling
- konfiguracia cez `config_flow`
- pripravene pre HACS custom repository

## Co Plugin Aktualne Cita

Plugin aktualne cita tieto zdroje:
- `status.xml`
- `control.xml`
- `parameters.htm`
- `about.htm`
- `about.xml`

Komunikacia:
- HTTP Basic Auth
- lokalna IP / hostname zariadenia
- kodovanie odpovedi `windows-1250`

## Co Plugin Aktualne Zobrazuje

### Stav Zariadenia

- vnutorna teplota
- cielova teplota vody
- vonkajsia teplota
- `tep4` ako zatial neznamy teplotny senzor
- aktualny vykon v percentach
- operation state zo `status.xml`
  - `normal_operation`
  - `defrost`
- operation mode z `control.xml`
  - `heating`
  - `cooling`
- season mode z `control.xml`
  - `summer`
  - `winter`
- zapnute / vypnute tepelne cerpadlo
- binary stav rozmrazovania
- dalsie raw status bity `st2` az `st5`

### Informacie O Zariadeni

- verzia firmware
- typ jednotky
- cas zostavenia / build time
- stav SD karty
- cas zariadenia

### Skupiny Parametrov

Integracia uz cita aj parameter senzory z `parameters.htm` v tychto skupinach:
- Heating Curve
- Heating Limits
- Cooling Limits
- DHW
- Advanced / Unknown

Pre parameter-backed senzory integracia interne drzi a vie vystavit:
- parsovanu hodnotu
- zobrazenu hodnotu
- raw parameter hodnotu (`pN`)
- informaciu ci je parameter editovatelny
- raw min / max limity, ak su zname
- grupu / kategoriu parametra

## Co Plugin Este Nerobi

Integracia je stale read-only.

To znamena, ze zatial nevie:
- zapisovat hodnoty spat do tepelneho cerpadla
- menit operating mode
- menit season mode
- menit cielove teploty
- odosielat formular z `parameters.htm`
- vystavovat zapisovatelne `number`, `select`, `switch` alebo `climate` entity

## Odporucany Sposob Instalacie

Odporucany postup:
- pridat repozitar do HACS ako custom repository
- nainstalovat integraciu
- restartovat Home Assistant
- pridat integraciu cez UI
- zadat host/IP, username, password a scan interval

## Obsah Repozitara

- [README.md](/Users/peter.glemba/Documents/Projekty/ATW-MINI-HA/README.md) - anglicka verzia
- [CHANGELOG.md](/Users/peter.glemba/Documents/Projekty/ATW-MINI-HA/CHANGELOG.md) - historia verzii
- [docs/hacs-navrh.md](/Users/peter.glemba/Documents/Projekty/ATW-MINI-HA/docs/hacs-navrh.md) - architektonicky navrh
- [docs/github-project-plan.md](/Users/peter.glemba/Documents/Projekty/ATW-MINI-HA/docs/github-project-plan.md) - navrh GitHub projektu
- [tests/fixtures](/Users/peter.glemba/Documents/Projekty/ATW-MINI-HA/tests/fixtures) - anonymizovane parser fixtures

## Verzovanie

Verzia, ktoru Home Assistant zobrazuje pri custom integracii, sa cita z [manifest.json](/Users/peter.glemba/Documents/Projekty/ATW-MINI-HA/custom_components/atw_mini/manifest.json).

Pravidla verzovania:
- patch: opravy a male kompatibilitne zmeny
- minor: nove read-only entity, nove zdroje, backward-compatible vylepsenia
- major: breaking zmeny v nazvoch entit, konfiguracii alebo spravani

Pre kazdy verejny release:
- upravit `custom_components/atw_mini/manifest.json`
- upravit [CHANGELOG.md](/Users/peter.glemba/Documents/Projekty/ATW-MINI-HA/CHANGELOG.md)
- vytvorit Git tag
- publikovat GitHub release

## Poznamky

- realna IP a prihlasovacie udaje sa nesmu commitovat
- lokalne raw zachyty maju ostat mimo Git
- `tep4` a status bity `st2` az `st5` este potrebuju lepsie semanticke mapovanie
- asset ikony je ulozeny v `assets/atw-mini-icon.svg`
