# Whatsapp Sender
This is a project that sends batch messages through WhatsApp

## Installation
Create a virtual enviroment ans install libraries
```bash
python -m venv ./venv
source venv/Scripts/activate
python -m pip install --upgrade pip
python install -r requirements.txt
```

## Usage
Once the libraries are installed, run the python script to launch the sender
```bash
python bot_wsp_interface.py
```

## Browser drivers
The drivers are found at [google dev](https://googlechromelabs.github.io/chrome-for-testing/) and [edge dev](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH) for Google Chrome and Microsoft Edge.


## Executable
To create an executable, run the following commands
```bash
pip install pyinstaller
pyinstaller --onefile –-windowed bot_wsp_interface.py
```