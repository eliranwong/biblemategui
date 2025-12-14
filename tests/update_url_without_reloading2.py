from nicegui import ui

@ui.page('/')
def bible_app():
    ui.label('BibleMate AI Reader').classes('text-2xl font-bold mb-4')
    
    # Label to display current selection
    status = ui.label('Current: Genesis Chapter 1')

    def change_chapter(chapter_num):
        # 1. Update the UI content normally
        status.set_text(f'Current: Genesis Chapter {chapter_num}')
        
        # 2. Update the Browser URL & History without reloading
        # This changes the URL to /?chapter=X
        new_url = f'/?chapter={chapter_num}'
        ui.run_javascript(f"window.history.pushState({{}}, '', '{new_url}')")

    with ui.row():
        ui.button('Chapter 1', on_click=lambda: change_chapter(1))
        ui.button('Chapter 2', on_click=lambda: change_chapter(2))
        ui.button('Chapter 3', on_click=lambda: change_chapter(3))

ui.run(port=9999)