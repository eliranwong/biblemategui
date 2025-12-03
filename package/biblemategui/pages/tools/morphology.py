import os, re
from biblemategui import BIBLEMATEGUI_DATA
import apsw
from nicegui import ui, app
from biblemategui.fx.bible import BibleSelector


def word_morphology(gui=None, b=1, c=1, v=1, area=2, **_):

    ui.add_head_html(f"""
    <style>
        /* Hebrew Word Layer */
        wform, heb, bdbheb, bdbarc, hu {{
            font-family: 'SBL Hebrew', 'Ezra SIL', serif;
            font-size: 1.8rem;
            direction: rtl;
            display: inline-block;
            line-height: 1.3em;
            margin-top: 0;
            margin-bottom: -2px;
            cursor: pointer;
        }}
        /* Greek Word Layer (targets <grk> tag) */
        wform, grk, kgrk, gu {{
            font-family: 'SBL Greek', 'Galatia SIL', 'Times New Roman', serif; /* CHANGED */
            font-size: 1.6rem;
            direction: ltr;
            display: inline-block;
            line-height: 1.3em;
            margin-top: 0;
            margin-bottom: -2px;
            cursor: pointer;
        }}
        inter {{
            direction: ltr;
            display: inline-block;
            font-size: 1.1rem;
            color: {'#f2ac7e' if app.storage.user['dark_mode'] else '#D35400'};
        }}
    </style>
    """)

    def add_tooltips(verse_text):
        if "</heb>" in verse_text:
            verse_text = re.sub('(<heb id=")(.*?)"', r'\1\2" data-word="\2" class="tooltip-word"', verse_text)
            verse_text = verse_text.replace("<heb> </heb>", "<heb>&nbsp;</heb>")
        elif "</grk>" in verse_text:
            verse_text = re.sub('(<grk id=")(.*?)"', r'\1\2" data-word="\2" class="tooltip-word"', verse_text)
        return verse_text

    def fetch_morphology(b, c, v):
        results = []
        db = os.path.join(BIBLEMATEGUI_DATA, "morphology.sqlite")
        with apsw.Connection(db) as connn:
            query = "SELECT * FROM morphology WHERE Book=? AND Chapter=? AND Verse=? ORDER BY WordID"
            cursor = connn.cursor()
            cursor.execute(query, (b,c,v))
            results = cursor.fetchall()
        return results

    # --- UI LAYOUT ---
    with ui.column().classes('w-full max-w-3xl mx-auto p-4 gap-6'):

        # Bible Selection menu
        bible_selector = BibleSelector(version_options=["KJV"])
        def additional_items():
            nonlocal gui, bible_selector, area
            def change_morphology(selection):
                if area == 1:
                    app.storage.user['tool_book_text'], app.storage.user['bible_book_number'], app.storage.user['bible_chapter_number'], app.storage.user['bible_verse_number'] = selection
                    gui.load_area_1_content(title="Morphology")
                else:
                    app.storage.user['tool_book_text'], app.storage.user['tool_book_number'], app.storage.user['tool_chapter_number'], app.storage.user['tool_verse_number'] = selection
                    gui.load_area_2_content(title="Morphology", sync=False)
            ui.button('Go', on_click=lambda: change_morphology(bible_selector.get_selection()))
        bible_selector.create_ui("KJV", b, c, v, additional_items=additional_items, show_versions=False)

        def open_lexicon(module, entry):
            app.storage.user['favorite_lexicon'] = module
            app.storage.user['tool_query'] = entry
            gui.select_empty_area2_tab()
            gui.load_area_2_content(title='lexicons')
        
        # Results Container
        with ui.column().classes('w-full gap-4'):
            if results := fetch_morphology(b,c,v):
                for wordID, clauseID, book, chapter, verse, word, lexicalEntry, morphologyCode, morphology, lexeme, transliteration, pronunciation, interlinear, translation, gloss in results:
                    lexicalEntries = lexicalEntry.split(",")[:-1]
                    with ui.card():
                        tag = "heb" if book < 40 else "grk"
                        html = f'''<{tag} id="{'wh' if book < 40 else 'w'}{wordID}">{word}</{tag}>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<ref data-word="{lexicalEntries[-1]}" class="tooltip-word"><{tag}>{lexeme}</{tag}></ref>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<inter>{interlinear}</inter>'''
                        ui.html(add_tooltips(html), sanitize=False).classes('w-full')
                        with ui.row().classes('w-full gap-0'):
                            for index, element in enumerate(morphology.split(",")[:-1]):
                                ui.label(element).classes(
                                    f"text-base px-2 py-0.5 rounded-full"+(" text-secondary" if index == 0 else "")
                                )
                        with ui.row().classes('w-full gap-0'):
                            ui.chip(
                                "Morphology",
                                icon='book',
                                color='secondary',
                                on_click=lambda: open_lexicon("Morphology", lexicalEntries[0]),
                            ).classes('cursor-pointer font-bold shadow-sm')
                            ui.chip(
                                "Morphology Concordance",
                                icon='book',
                                color='secondary',
                                on_click=lambda: open_lexicon("ConcordanceMorphology", lexicalEntries[0]),
                            ).classes('cursor-pointer font-bold shadow-sm')
                            ui.chip(
                                "Book Concordance",
                                icon='book',
                                color='secondary',
                                on_click=lambda: open_lexicon("ConcordanceBook", lexicalEntries[0]),
                            ).classes('cursor-pointer font-bold shadow-sm')
                            ui.chip(
                                "Lexicon",
                                icon='book',
                                color='secondary',
                                on_click=lambda: open_lexicon(app.storage.user['hebrew_lexicon'] if b < 40 else app.storage.user['greek_lexicon'], lexicalEntries[-1]),
                            ).classes('cursor-pointer font-bold shadow-sm')