#!/usr/bin/env python3
from nicegui import ui

from biblemategui import BIBLEMATEGUI_APP_DIR

from biblemategui.pages.home import *

from biblemategui.pages.bibles.original_reader import original_reader
from biblemategui.pages.bibles.original_interlinear import original_interlinear
from biblemategui.pages.bibles.original_parallel import original_parallel
from biblemategui.pages.bibles.original_discourse import original_discourse
from biblemategui.pages.bibles.original_linguistic import original_linguistic

from biblemategui.pages.tools.audio import bibles_audio

import os

# --- Define the Pages ---
# We define our pages first. The create_menu() function will be
# called inside each page function to add the shared navigation.

"""
q - query
t - token
m - menu

b - book
c - chapter
v - verse

bb - default bible
cc - default commentary
ee - default encyclopedia
ll - default lexicon
"""

# Home Page

@ui.page('/')
def page_home(q: str | None = None):
    """
    Home page that accepts an optional 'q' q parameter.
    Example: /?q=hello
    """
    create_menu() # Add the shared menu
    create_home_layout()
    '''with ui.column().classes('w-full items-center'):
        ui.label('Welcome to BibleMate AI!').classes('text-2xl mt-4')
        ui.label('Resize your browser window to see the menu change.')

        # --- Display the q parameter ---
        if q:
            ui.label(f'You passed a parameter:').classes('text-lg mt-4')
            ui.label(f'q = {q}').classes('text-xl font-bold bg-yellow-200 p-4 rounded-lg shadow-md') # <-- USE RENAMED PARAMETER
        else:
            ui.label('Try adding "?q=hello" to the URL!').classes('text-lg mt-4')'''

# Settings

@ui.page('/settings')
def page_Settings(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('BibleMate AI').classes('text-2xl mt-4')
        ui.notify("This feature is currently in progress.")

# Entry_point

def main():
    # --- Run the App ---
    # Make sure to replace the secret!
    ui.run(
        storage_secret='REPLACE_ME_WITH_A_REAL_SECRET', # TODO
        port=8888,
        title='BibleMate AI',
        favicon=os.path.join(BIBLEMATEGUI_APP_DIR, 'eliranwong.jpg')
    )

main()