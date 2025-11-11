from nicegui import ui

def update_url_param(key: str, value: str, replace: bool = False):
    """
    Updates a URL query parameter without reloading the page.
    
    :param key: The query parameter key (e.g., 'book', 'verse')
    :param value: The value to set
    :param replace: If True, uses replaceState (doesn't add to browser history stack).
                    If False, uses pushState (user can click 'back' to undo).
    """
    method = 'replaceState' if replace else 'pushState'
    js_code = f'''
        const url = new URL(window.location);
        url.searchParams.set("{key}", "{value}");
        window.history.{method}({{}}, '', url);
    '''
    ui.run_javascript(js_code)

@ui.page('/')
def main_page():
    ui.label('BibleMate AI - Deep Link Tester').classes('text-2xl font-bold')
    ui.label('Change the values below and watch the browser URL update without reloading.')

    with ui.row():
        ui.input('Book', on_change=lambda e: update_url_param('book', e.value))
        ui.number('Chapter', on_change=lambda e: update_url_param('chapter', e.value))

ui.run(port=9999)