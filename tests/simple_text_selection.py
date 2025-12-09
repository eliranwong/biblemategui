from nicegui import ui

async def get_selected_text():
    result = await ui.run_javascript('window.getSelection().toString()')
    if result:
        ui.notify(f'Selected: {result}')
    else:
        ui.notify('No text selected')

ui.html('<p>This is some <b>HTML content</b> you can select.</p>', sanitize=False)

with ui.card():
    ui.label('This is text inside a card that you can also select.')

ui.label('And this is a regular label with selectable text.')

ui.button('Get Selected Text', on_click=get_selected_text)

ui.run(port=9999)