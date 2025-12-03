import apsw
import re, os
from nicegui import ui, app
from biblemategui import BIBLEMATEGUI_DATA
#from agentmake.plugins.uba.lib.BibleParser import BibleVerseParser
from biblemategui.fx.bible import BibleSelector


def bible_promises_menu(gui=None, **_):

    def promise(event):
        nonlocal gui
        tool, number = event.args
        app.storage.user['tool_query'] = f"{tool}.{number}"
        gui.select_empty_area2_tab()
        gui.load_area_2_content(title='Promises')
    ui.on('promise', promise)

    ui.add_head_html(f"""
    <style>
        /* Main container for the content - LTR flow */
        .content-text {{
            direction: ltr;
            font-family: sans-serif;
            font-size: 1.1rem;
            padding: 0px;
            margin: 0px;
        }}
        /* Verse ref */
        ref {{
            color: {'#f2c522' if app.storage.user['dark_mode'] else 'navy'};
            font-weight: bold;
            cursor: pointer;
        }}
        /* CSS to target all h1 elements */
        h1 {{
            font-size: 2.2rem;
            color: {app.storage.user['primary_color']};
        }}
        /* CSS to target all h2 elements */
        h2 {{
            font-size: 1.8rem;
            color: {app.storage.user['secondary_color']};
        }}
    </style>
    """)

    # --- CONFIGURATION ---
    DB_FILE = os.path.join(BIBLEMATEGUI_DATA, 'books', 'Bible_Promises.book')
    with apsw.Connection(DB_FILE) as connn:
        cursor = connn.cursor()
        cursor.execute("SELECT Chapter, Content FROM Reference")
        fetches = cursor.fetchall()

    # --- UI LAYOUT ---
    with ui.column().classes('w-full max-w-3xl mx-auto p-4 gap-6'):

        # Results Container
        with ui.column().classes('w-full gap-4'):

            for chapter, content in fetches:
                # Create the Expansion with specific icon
                with ui.expansion(chapter, icon='auto_stories', value=False) \
                        .classes('w-full border rounded-lg shadow-sm') \
                        .props('header-class="font-bold text-lg text-primary"'):
                    
                    # convert links, e.g. <ref onclick="bcv(3,19,26)">
                    content = re.sub(r'''(onclick|ondblclick)="(cr|bcv|promise)\((.*?)\)"''', r'''\1="emitEvent('\2', [\3]); return false;"''', content)
                    content = re.sub(r"""(onclick|ondblclick)='(cr|bcv|promise)\((.*?)\)'""", r"""\1='emitEvent("\2", [\3]); return false;'""", content)
                    ui.html(f'<div class="content-text">{content}</div>', sanitize=False).classes('p-4')
