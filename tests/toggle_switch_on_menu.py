from nicegui import app, ui, native

# --- 2. Custom Toggle Function (Used only for Full Screen now) ---

def create_toggle_menu_item(label_text: str, storage_key: str):
    """
    Creates a custom menu item with a label on the left and a toggle on the right.
    This structure is retained for the "Full Screen" feature.
    """

    # --- 1. NiceGUI Setup and Configuration ---

    # Ensure initial values exist in user storage
    # These values will persist across sessions for the same user
    app.storage.user['dark_mode'] = app.storage.user.get('dark_mode', False)
    app.storage.user['full_screen'] = app.storage.user.get('full_screen', False)

    # Apply initial dark mode setting when the app starts
    if app.storage.user['dark_mode']:
        #native.set_dark_mode(True)
        ...


    # Get the current value from storage
    initial_value = app.storage.user.get(storage_key, False)
    
    # ui.row allows us to use flexbox (justify-between) for positioning.
    with ui.row().classes('w-full justify-between items-center q-px-md q-py-sm cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700'):
        
        # Description on the left
        ui.label(label_text)
        
        # Toggle switch on the right
        toggle_switch = ui.switch(value=initial_value).bind_value(
            app.storage.user, storage_key
        ).props('dense color="primary"')

        # --- Specific Logic for Fullscreen ---
        
        if storage_key == 'full_screen':
            def toggle_full_screen(e):
                """Request or exit fullscreen mode via JavaScript."""
                if e.value:
                    # Request fullscreen
                    native.run_javascript('document.documentElement.requestFullscreen()')
                else:
                    # Exit fullscreen
                    native.run_javascript('if (document.exitFullscreen) { document.exitFullscreen(); }')

            toggle_switch.on_value_change(toggle_full_screen)

# --- 3. Dark Mode Menu Item Logic ---

def toggle_dark_mode_menu_item(text_label: ui.label):
    """
    Toggles dark mode, updates the user storage, and changes the menu item text.
    The function now accepts the ui.label reference directly.
    """
    # 1. Toggle the state in user storage
    is_dark = not app.storage.user['dark_mode']
    app.storage.user['dark_mode'] = is_dark
    
    # 2. Apply the setting
    #native.set_dark_mode(is_dark)
    
    # 3. Update the menu item text via the label
    new_text = 'Light Mode' if is_dark else 'Dark Mode'
    text_label.set_text(new_text)

# --- 4. Main Page Implementation ---

@ui.page('/')
def index():
    """Main page content with a simple header and the menu button."""
    
    with ui.header().classes('items-center'):
        ui.label('BibleMate AI').classes('text-2xl font-bold')
        ui.space()
        
        # The menu button
        with ui.button(icon='menu').classes('text-xl'):
            with ui.menu().props('auto-close'):
                
                # Standard Menu Items (Optional)
                ui.menu_item('Settings', lambda: ui.notify('Navigating to settings...'))
                ui.separator()
                
                # --- Dark Mode Menu Item (Standard) ---
                
                # Set initial text based on the current state
                is_dark_initial = app.storage.user['dark_mode']
                initial_text = 'Light Mode' if is_dark_initial else 'Dark Mode'
                
                # Create the menu item container
                with ui.menu_item() as dark_mode_menu_item:
                    dark_mode_label = ui.label(initial_text).classes('flex items-center')
                
                # Use on() to pass the label reference to the handler for text updating
                dark_mode_menu_item.on('click', lambda: toggle_dark_mode_menu_item(dark_mode_label))
                
                ui.separator()
                
                # --- Full Screen Toggle (Custom Switch) ---
                
                create_toggle_menu_item('Full Screen', 'full_screen')

ui.run(port=9999, storage_secret="testing")