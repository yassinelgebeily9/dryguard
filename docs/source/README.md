# 📡 RFID Reader FX7500

This repository contains the code, setup instructions, and tools for interacting with the Zebra FX7500 RFID Reader. It also includes scripts to enable systematic RFID performance measurements under various environmental conditions, and data processing scripts using Bayesian Machine Learning Algorithms.

## 📋 Table of Contents

- [📡 RFID Reader FX7500](#-rfid-reader-fx7500)
  - [📋 Table of Contents](#-table-of-contents)
  - [🛠️ Regular Set Up](#️-regular-set-up)
  - [🌐 Networkless Set Up](#-networkless-set-up)
  - [📜 License](#-license)
  - [📂 Project Structure](#-project-structure)
  - [🚀 Getting Started](#-getting-started)
  - [📄 Main Script](#-main-script)
  - [📊 Plots](#-plots)
  - [🔧 CLI Parameters](#-cli-parameters)
    - [Available Parameters](#available-parameters)
    - [Example Usage](#example-usage)
  - [📜 Scripts](#-scripts)
    - [MQTT Setup Script](#mqtt-setup-script)
    - [Live USB Setup Script](#live-usb-setup-script)
  - [📚 Modules](#-modules)
    - [Reader Module](#reader-module)
    - [Gaussian Mixture Models](#gaussian-mixture-models)
    - [Fitting Module](#fitting-module)
    - [Accuracy Module](#accuracy-module)
    - [Parser Module](#parser-module)

## 🛠️ Regular Set Up

For the regular setup of the Zebra FX7500 RFID Reader, please refer to the [Regular Set Up Guide](./docs/01_Regular_Set_Up.md).

## 🌐 Networkless Set Up

For the networkless setup of the Zebra FX7500 RFID Reader, please refer to the [Networkless Set Up Guide](./docs/02_Networkless_Set_Up.md).

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## 📂 Project Structure

```
RFID-Reader-FX7500/
├── arduino_serial/
│   ├── __init__.py 
│   └── main.py
├── assets/
│   └── old/
│       └── HOWTO.md
├── data/
│   └── 00-Examples/
│   └── 01-Preliminary-Measurements/
│   └── 02-Final-Measurements/
├── docs/
│   ├── 01_Regular_Set_Up.md
│   └── 02_Networkless_Set_Up.md
├── scripts/
│   ├── mqtt_set_up.sh
│   ├── live_usb_set_up.sh
├── src/
│   ├── __init__.py 
│   ├── accuracy.py
│   ├── data_management.py
│   ├── fitting.py
│   ├── gaussian_mixture_models_3D.py
│   ├── gaussian_mixture_models.py
│   ├── plotting.py
│   ├── reader.py
│   └── sensors.ino
├── main_tui.css
├── tui.py
├── requirements.txt
├── LICENSE
└── README.md
```

## 🚀 Getting Started

To get started with the Zebra FX7500 RFID Reader, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Wireless-Information-Networking/RFID-Reader-FX7500.git
   cd RFID-Reader-FX7500
   ```

2. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the MQTT broker:**

   ```bash
   bash scripts/mqtt_set_up.sh
   ```

4. **Run the main script:**

   ```bash
   python main.py
   ```

## 📄 Main Script

The main script is located at [tui.py](./tui.py). It initializes the application, sets up the MQTT broker, and starts the RFID reader control interface.

## 📊 Plots

The plots are generated using the data from the RFID reader. The plotting scripts are located in the `src` directory:

- [src/gaussian_mixture_models.py](./src/gaussian_mixture_models.py): Handles 2D Gaussian Mixture Models.
- [src/gaussian_mixture_models_3D.py](./src/gaussian_mixture_models_3D.py): Handles 3D Gaussian Mixture Models.
- [src/plotting.py](./src/plotting.py): Other plotting and helper functions for data visualization.

## 🔧 CLI Parameters

You can pass parameters through the CLI to customize the behavior of the RFID reader. If a parameter is not provided, the default value defined in the "CONSTANTS" section of `main.py` will be used.

### Available Parameters

| Flag        | Long Option   | Description                                                   | Type   | Default Value |
|-------------|---------------|---------------------------------------------------------------|--------|---------------|
| `-t`        | `--Tag`       | The coded value of the tag of the RFID reader.                | `int`  | `0`           |
| `-f`        | `--Frequency` | The frequency of the RFID reader, in MHz.                     | `float`| `865.7`       |
| `-d`        | `--Distance`  | The distance between the RFID reader and the RFID tag, in meters. | `float`| `0.3`         |
| `-o`        | `--Obstacle`  | The coded value of the obstacle between the RFID reader and the RFID tag. | `int`  | `0`           |
| `-s`        | `--Duration`  | The duration of the reading process, in seconds.              | `float`| `5.0`         |
| `-p`        | `--Power`     | The transmission power of the RFID reader, in dBm             | `float`| `10.0`        |

### Example Usage

To run the script with custom parameters:

```bash
python main.py -t 1 -f 866.0 -d 0.5 -o 2 -s 10
```

In this example:

- The tag is set to `1`.
- The frequency is set to `866.0` MHz.
- The distance is set to `0.5` meters.
- The obstacle is set to `2` (Metal).
- The duration is set to `10` seconds.

If any parameter is not provided, the default value will be used. For example, running:

```bash
python main.py -t 1 -f 866.0
```

will use:

- The tag `1`.
- The frequency `866.0` MHz.
- The default distance `0.3` meters.
- The default obstacle `0` (None).
- The default duration `5.0` seconds.

## 📜 Scripts

### MQTT Setup Script

The [scripts/mqtt_set_up.sh](./scripts/mqtt_set_up.sh) script installs and configures the Mosquitto MQTT broker.

### Live USB Setup Script

The [scripts/live_usb_set_up.sh](./scripts/live_usb_set_up.sh) script sets up a live USB environment for running the RFID reader application without network access.

## 📚 Modules

### Reader Module

The [src/reader.py](./src/reader.py) module handles communication with the RFID reader and processes incoming data.

### Gaussian Mixture Models

- [src/gaussian_mixture_models.py](./src/gaussian_mixture_models.py): Implements 2D Gaussian Mixture Models for clustering RFID data.
- [src/gaussian_mixture_models_3D.py](./src/gaussian_mixture_models_3D.py): Extends Gaussian Mixture Models to 3D for advanced clustering.

### Fitting Module

The [src/fitting.py](./src/fitting.py) module uses machine learning techniques to fit experimental RSSI values to the Friis equation.

### Accuracy Module

The [src/accuracy.py](./src/accuracy.py) module evaluates the accuracy of RFID measurements using ROC curves and other metrics.

### Parser Module

The [src/parser.py](./src/parser.py) module parses CLI arguments and configures the application based on user input.
