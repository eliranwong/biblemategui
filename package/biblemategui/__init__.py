from pathlib import Path
import os

BIBLEMATEGUI_APP_DIR = os.path.dirname(os.path.realpath(__file__))
BIBLEMATEGUI_USER_DIR = os.path.join(os.path.expanduser("~"), "biblemate")
BIBLEMATEGUI_DATA = os.path.join(os.path.expanduser("~"), "biblemate", "data")
if not os.path.isdir(BIBLEMATEGUI_USER_DIR):
    Path(BIBLEMATEGUI_USER_DIR).mkdir(parents=True, exist_ok=True)
BIBLEMATEGUI_DATA_CUSTOM = os.path.join(os.path.expanduser("~"), "biblemate", "data_custom")
if not os.path.isdir(BIBLEMATEGUI_DATA_CUSTOM):
    Path(BIBLEMATEGUI_DATA_CUSTOM).mkdir(parents=True, exist_ok=True)
for i in ("audio", "bibles"):
    if not os.path.isdir(os.path.join(BIBLEMATEGUI_DATA, i)):
        Path(os.path.join(BIBLEMATEGUI_DATA, i)).mkdir(parents=True, exist_ok=True)