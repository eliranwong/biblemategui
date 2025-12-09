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
    
    menu = ui.context_menu()
    with menu:
        ui.menu_item('📋 Copy', lambda: copy_text())
        ui.menu_item('🔍 Search', lambda: ui.notify(f'Search: {selected["text"]}'))
        ui.menu_item('📖 Define', lambda: ui.notify(f'Define: {selected["text"]}'))
    
    def copy_text():
        if selected['text']:
            # Escape quotes and newlines for JavaScript
            escaped = selected['text'].replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
            ui.run_javascript(f'navigator.clipboard.writeText(`{escaped}`)')
            ui.notify(f'Copied: "{selected["text"]}"')
        else:
            ui.notify('No text selected', type='warning')
    
    async def on_context(e):
        selected['text'] = e.args.get('text', '')
    
    ui.on('custom_context', on_context)
    
    ui.run_javascript(f'''
        const container = document.getElementById('text-container');
        
        container.addEventListener('contextmenu', (e) => {{
            const selection = window.getSelection().toString().trim();
            emitEvent('custom_context', {{ text: selection }});
            
            if (e.shiftKey) {{
                e.stopPropagation();
            }}
        }}, true);
    ''')

ui.page('/')(create_page)
ui.run(port=9999)