#!/usr/bin/env python3
from nicegui import ui

from biblemateweb import BIBLEMATEWEB_APP_DIR

from biblemateweb.pages.home import *

from biblemateweb.pages.bibles.original_reader import original_reader
from biblemateweb.pages.bibles.original_interlinear import original_interlinear
from biblemateweb.pages.bibles.original_parallel import original_parallel
from biblemateweb.pages.bibles.original_discourse import original_discourse
from biblemateweb.pages.bibles.original_linguistic import original_linguistic

from biblemateweb.pages.tools.audio import bibles_audio

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

# Bible

@ui.page('/bibles/chapter')
def page_bibles_chapter(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Read Bible Chapter(s)').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/compare/chapter')
def page_compare_chapter(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Compare Bible Chapter(s)').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/bibles/verse')
def page_bibles_verse(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Read Bible Verse(s)').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/compare/verse')
def page_compare_verse(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Compare Bible Verse(s)').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/bibles/audio')
def page_bibles_audio(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Bible Audio').classes('text-2xl mt-4')
        bibles_audio()

# Original Bibles

@ui.page('/original/reader')
def page_original_reader(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label("Original Reader's Bible").classes('text-2xl mt-4')
        original_reader(q=q)

@ui.page('/original/interlinear')
def page_original_interlinear(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Original Interlinear Bible').classes('text-2xl mt-4')
        original_interlinear(q=q)

@ui.page('/original/parallel')
def page_original_parallel(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Original Parallel Bible').classes('text-2xl mt-4')
        original_parallel()

@ui.page('/original/discourse')
def page_original_discourse(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Original Discourse Bible').classes('text-2xl mt-4')
        original_discourse()

@ui.page('/original/linguistic')
def page_original_linguistic(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Original Linguistic Bible').classes('text-2xl mt-4')
        original_linguistic(q=q)

# Tools

@ui.page('/tool/indexes')
def page_tool_indexes(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Resource Indexes').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/tool/translations')
def page_tool_translations(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-centermorphology'):
        ui.label('Interlinear, Literal & Dynamic Translations').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/tool/discourse')
def page_tool_discourse(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Discourse Analysis').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/tool/morphology')
def page_tool_morphology(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Morphological Data').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/tool/commentary')
def page_tool_commentary(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Bible Commentaries').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/tool/timelines')
def page_tool_timelines(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Bible Timelines').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/tool/chronology')
def page_tool_chronology(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Bible Chronology').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/tool/xref')
def page_tool_xref(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Bible Cross-references').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/tool/tske')
def page_tool_tske(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('The Treasury of Scripture Knowledge (Enhanced)').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

# Search

@ui.page('/search/bible')
def page_search_bible(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Bible').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/search/parallels')
def page_search_parallels(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Parallels').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/search/promises')
def page_search_promises(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Promises').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/search/topics')
def page_search_topics(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Topics').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/search/names')
def page_search_names(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Names').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/search/characters')
def page_search_characters(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Characters').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/search/locations')
def page_search_locations(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Locations').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/search/dictionary')
def page_search_dictionary(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Dictionary').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/search/encyclopedia')
def page_search_encyclopedia(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Encyclopedia').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/search/lexicon')
def page_search_lexicon(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Lexicon').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

# About

@ui.page('/about')
def page_about(q: str | None = None, m: bool = True):
    if m:
        create_menu() # Add the shared menu
    with ui.column().classes('w-full items-center'):
        ui.label('About Us').classes('text-2xl mt-4')
        ui.label('We are a team that loves Jesus.')

@ui.page('/source')
def page_source(q: str | None = None, m: bool = True):
    if m:
        create_menu() # Add the shared menu
    with ui.column().classes('w-full items-center'):
        ui.label('Source Code').classes('text-2xl mt-4')
        ui.label('https://github.com/eliranwong/biblemateweb')

@ui.page('/contact')
def page_contact(q: str | None = None, m: bool = True):
    if m:
        create_menu() # Add the shared menu
    with ui.column().classes('w-full items-center'):
        ui.label('Contact Page').classes('text-2xl mt-4')
        ui.label('Get in touch with us!')

# AI Features

@ui.page('/ai/commentary')
def page_ai_qna(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('AI Commentary').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/ai/qna')
def page_ai_qna(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Question & Answer').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/ai/chat')
def page_ai_chat(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Chat Mode').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/ai/partner')
def page_ai_partner(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Partner Mode').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

@ui.page('/ai/agent')
def page_ai_agent(q: str | None = None, m: bool = True):
    if m:
        create_menu()
    with ui.column().classes('w-full items-center'):
        ui.label('Agent Mode').classes('text-2xl mt-4')
        ui.label('... WORK IN PROGRESS ...')

def main():
    # --- Run the App ---
    # Make sure to replace the secret!
    ui.run(
        storage_secret='REPLACE_ME_WITH_A_REAL_SECRET',
        port=8888,
        title='BibleMate AI',
        favicon=os.path.join(BIBLEMATEWEB_APP_DIR, 'eliranwong.jpg')
    )

main()