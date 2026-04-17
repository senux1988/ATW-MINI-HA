# ATW MINI Home Assistant Integracia

![ATW MINI icon](assets/atw-mini-icon.svg)

Vlastna integracia pre Home Assistant pre tepelne cerpadlo ATW MINI / NeoRe Mini s lokalnou HTTP/XML/HTML komunikaciou.

Anglicka verzia je v [README.md](README.md).

## Aktualny Stav

Integracia sa uz vie lokalne pripojit na zariadenie a citat viacero endpointov.

Aktualna verzia pluginu:
- `0.4.0`

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
- teplota TUV
- teplota senzora E
- teplota senzora F
- teplota senzora G
- vonkajsia teplota
- aktualny vykon v percentach
- operation state zo `status.xml`
  - `hidden_off`
  - `heating_mode`
  - `cooling_mode`
  - `off`
  - `defrost`
  - `fault`
- heating delivery state zo `status.xml`
  - `hidden_off`
  - `heating_via_hp`
  - `heating_via_hp_plus_bivalent_stage_1`
  - `heating_via_hp_plus_bivalent_stage_1_2`
  - `summer_mode_dhw_only`
- DHW heating state zo `status.xml`
  - `hidden_off`
  - `dhw_heating_via_hp`
  - `dhw_heating_via_electric_heater`
- operation mode z `control.xml`
  - `heating`
  - `cooling`
- season mode z `control.xml`
  - `summer`
  - `winter`
- zapnute / vypnute tepelne cerpadlo
- binary stav rozmrazovania
- aktivny casovy utlm
- aktivne HDO / blokovanie vstupom ON2

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

- [README.md](README.md) - anglicka verzia
- [CHANGELOG.md](CHANGELOG.md) - historia verzii
- [docs/hacs-navrh.md](docs/hacs-navrh.md) - architektonicky navrh
- [docs/github-project-plan.md](docs/github-project-plan.md) - navrh GitHub projektu
- [tests/fixtures](tests/fixtures) - anonymizovane parser fixtures

## Verzovanie

Verzia, ktoru Home Assistant zobrazuje pri custom integracii, sa cita z [manifest.json](custom_components/atw_mini/manifest.json).

Pravidla verzovania:
- patch: opravy a male kompatibilitne zmeny
- minor: nove read-only entity, nove zdroje, backward-compatible vylepsenia
- major: breaking zmeny v nazvoch entit, konfiguracii alebo spravani

Pre kazdy verejny release:
- upravit `custom_components/atw_mini/manifest.json`
- upravit [CHANGELOG.md](CHANGELOG.md)
- vytvorit Git tag
- publikovat GitHub release

## Poznamky

- realna IP a prihlasovacie udaje sa nesmu commitovat
- lokalne raw zachyty maju ostat mimo Git
- `tep4` je teraz mapovany ako teplota TUV
- `tep5`, `tep6` a `tep7` su zatial vystavene ako senzory E/F/G, kym nebudu potvrdene presnejsie nazvy
- `status.xml st1` az `st5` su teraz mapovane podla podkladov od vyrobcu
- asset ikony je ulozeny v `assets/atw-mini-icon.svg`
- ikonka v Home Assistant UI nie je ta ista ako obrazok v README a na nahradenie default placeholdera zvycajne treba Home Assistant branding assety
