<p align="center">
  <img src="assets/logo.png" width="180" alt="aznumgen logo">
</p>

<h1 align="center">aznumgen</h1>

<p align="center">
  A desktop GUI for generating Azerbaijani license plate images.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/github/license/alimetastic/aznumgen" alt="License">
</p>


## Features



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
