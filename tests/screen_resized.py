from nicegui import ui

class UIState:
    def __init__(self):
        self._is_half = False

    @property
    def height_style(self):
        # Return the CSS string for height based on the boolean
        return 'height: 50vh' if self._is_half else 'height: 100vh'

    def toggle(self):
        self._is_half = not self._is_half

# Initialize your state
app_state = UIState()

@ui.page('/')
def main():
    
    # 1. MAIN CONTAINER
    # Note: We REMOVED 'h-screen' from .classes() and use .bind_style() instead.
    # We assign it to 'main_box' just in case we need to reference it, though binding handles the updates.
    main_box = ui.column().classes('w-full no-wrap gap-0 bg-gray-50') \
        .bind_style_from(app_state, 'height_style')
    
    with main_box:
        # Header
        with ui.row().classes('w-full bg-blue-600 p-4 text-white shrink-0 items-center justify-between'):
            ui.label('BibleMate AI')
            # A switch to test the resizing
            ui.switch('Half Screen Mode', on_change=lambda: main_box.update()).bind_value(app_state, '_is_half')

        # Middle (Scrollable)
        with ui.column().classes('w-full flex-grow overflow-hidden border-4 border-red-500'):
            with ui.scroll_area().classes('w-full h-full p-4'):
                for i in range(20):
                    ui.label(f'Verse content line {i}...')

        # Footer
        with ui.row().classes('w-full bg-gray-200 p-4 shrink-0'):
            ui.label('Footer Content')

ui.run(port=9999)