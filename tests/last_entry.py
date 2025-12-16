from nicegui import ui

# Simple history storage
history = []

def save_and_clear():
    if text_input.value:
        history.append(text_input.value)
        text_input.value = ''
        ui.notify('Saved to history')

def retrieve_last():
    if history:
        # Get the last item
        text_input.value = history[-1]
    else:
        ui.notify('History is empty', type='warning')

with ui.row().classes('w-full justify-center'):
    text_input = ui.input(placeholder='Type and press Enter')
    
    # 1. Desktop Logic: Bind Enter and Up Arrow
    text_input.on('keydown.enter', save_and_clear)
    text_input.on('keydown.up', retrieve_last)

    # 2. Mobile Logic: Add a clickable icon inside the input
    with text_input.add_slot('append'):
        # This icon acts as the "Up Arrow" for mobile users
        ui.icon('history') \
            .on('click', retrieve_last) \
            .classes('text-sm cursor-pointer text-gray-500 hover:text-black').tooltip('Restore last entry')

ui.run(port=9999)