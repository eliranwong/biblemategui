from nicegui import ui

selected_text = ''

def on_selection(e):
    global selected_text
    selected_text = e.args
    ui.notify(f'Selected: {selected_text}' if selected_text else 'No text selected')

ui.on('selection_captured', on_selection)

def get_selected_text():
    ui.run_javascript('''
        const text = window.getSelection().toString();
        emitEvent("selection_captured", text);
    ''')

ui.html('<p>This is some <b>HTML content</b> you can select.</p>', sanitize=False)

with ui.card():
    ui.label('This is text inside a card that you can also select.')

ui.button('Get Selected Text', on_click=get_selected_text)

ui.run(port=9999)