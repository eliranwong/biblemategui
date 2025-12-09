from nicegui import ui

def create_page():
    selected = {'text': ''}
    
    html = ui.html('''
        <div id="text-container" style="padding: 20px; font-size: 18px; line-height: 2;">
            <p>This is some sample text that you can select and right-click on. 
            Try selecting different words or phrases to see the context menu in action.</p>
            <p>Hold <strong>Shift</strong> and right-click to open the default browser context menu.</p>
        </div>
    ''', sanitize=False)
    
    # Custom context menu with ID so we can control it
    menu = ui.context_menu()
    with menu:
        ui.menu_item('📋 Copy', lambda: ui.notify(f'Copy: {selected["text"]}'))
        ui.menu_item('🔍 Search', lambda: ui.notify(f'Search: {selected["text"]}'))
        ui.menu_item('📖 Define', lambda: ui.notify(f'Define: {selected["text"]}'))
    
    async def on_context(e):
        selected['text'] = e.args.get('text', '')
        if selected['text']:
            ui.notify(f'Selected: "{selected["text"]}"', type='info')
    
    ui.on('custom_context', on_context)
    
    # JavaScript to handle shift+right-click
    ui.run_javascript(f'''
        const container = document.getElementById('text-container');
        const menuId = 'c' + {menu.id};
        
        container.addEventListener('contextmenu', (e) => {{
            const selection = window.getSelection().toString().trim();
            emitEvent('custom_context', {{ text: selection }});
            
            if (e.shiftKey) {{
                // Prevent custom menu, allow default
                e.stopPropagation();
            }}
        }}, true);  // Use capture phase
    ''')

ui.page('/')(create_page)
ui.run(port=9999)