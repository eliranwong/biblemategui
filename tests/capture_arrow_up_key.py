from nicegui import ui

def handle_key(e):
    # Check if input is empty and up arrow was pressed
    if e.args['key'] == 'ArrowUp' and not e.sender.value:
        ui.notify('Up arrow pressed on empty input!')
        # Your function here

input_field = ui.input('Type something').on('keydown', handle_key)

ui.run(port=9999)