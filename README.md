<p align="center">
  <img src="assets/logo.png" width="180" alt="aznumgen logo">
</p>

<h1 align="center">aznumgen</h1>

<p align="center">
  A desktop GUI for generating Azerbaijani license plate images, based on the AZS 599-2015 standard.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/github/license/alimetastic/aznumgen" alt="License">
</p>


## Features

- 14 plate types: standard, passenger transport (blue), transit, honorary consul, diplomatic (D / T), military, plus the square type II, III and IV (motorcycle) layouts
- Type a number or hit **Random** for a valid one (current year on transit plates)
- Input is fitted to the plate's format automatically: wrong characters are skipped, missing ones filled in
- Region name and year shown under the preview
- Dashes on/off for plates that have them
- Exports a transparent PNG at 4 px/mm (a standard 520×110 plate is 2080×440 px)

## Screenshots

![Main window](assets/app.png)

## Examples

| Standard | Passenger transport |
|---|---|
| ![Standard](assets/standard.png) | ![Passenger transport](assets/blue.png) |

| Transit | Diplomatic |
|---|---|
| ![Transit](assets/transit.png) | ![Diplomatic](assets/diplomatic.png) |

| Type II | Type III | Type IV (motorcycle) |
|---|---|---|
| ![Type II](assets/type2.png) | ![Type III](assets/type3.png) | ![Type IV](assets/type4.png) |

## Download

Grab `aznumgen.exe` from the latest release.

Windows SmartScreen may warn about the unsigned .exe, click **More info - Run anyway**.

## Run from source

```bash
git clone https://github.com/alimetastic/aznumgen.git
cd aznumgen
pip install -r requirements.txt
python aznumgen.py
```

## Build the .exe yourself

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name aznumgen --icon assets/logo.ico aznumgen.py
```

The executable will be in `dist/`.

## Fonts

For the most accurate look, put `AZPlate.otf` (77 mm characters) and `AZPlate50.otf` (50 mm characters) next to `aznumgen.py`.
Without them the app falls back to Bahnschrift, then Arial, then DejaVu Sans.

## Disclaimer

The images are for design, education and mockups only. They are not official plates and must not be used on a vehicle.

## License

[MIT](LICENSE)
