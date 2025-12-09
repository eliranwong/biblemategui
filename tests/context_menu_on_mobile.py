from nicegui import ui

def create_page():
    selected = {'text': ''}
    
    ui.html('''
        <div id="text-container" style="padding: 20px; font-size: 18px; line-height: 2; user-select: text;">
            <p>This is some sample text that you can select. 
            Select any text and a menu will appear.</p>
        </div>
    ''', sanitize=False)
    
    # Popup menu that appears near selection
    with ui.card().classes('fixed shadow-lg z-50 hidden').props('id="selection-menu"') as popup:
        with ui.row().classes('gap-1 p-1'):
            ui.button('📋', on_click=lambda: copy_text()).props('flat dense')
            ui.button('🔍', on_click=lambda: ui.notify(f'Search: {selected["text"]}')).props('flat dense')
            ui.button('📖', on_click=lambda: ui.notify(f'Define: {selected["text"]}')).props('flat dense')
    
    def copy_text():
        if selected['text']:
            escaped = selected['text'].replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
            ui.run_javascript(f'navigator.clipboard.writeText(`{escaped}`)')
            ui.notify('Copied!')
    
    async def on_selection(e):
        selected['text'] = e.args.get('text', '')
    
    ui.on('text_selected', on_selection)
    
    ui.run_javascript('''
        const container = document.getElementById('text-container');
        const menu = document.getElementById('selection-menu');
        
        document.addEventListener('selectionchange', () => {
            const selection = window.getSelection();
            const text = selection.toString().trim();
            
            if (text && container.contains(selection.anchorNode)) {
                emitEvent('text_selected', { text: text });
                
                // Position menu above selection
                const range = selection.getRangeAt(0);
                const rect = range.getBoundingClientRect();
                
                menu.style.left = rect.left + (rect.width / 2) - 50 + 'px';
                menu.style.top = (rect.top - 45 + window.scrollY) + 'px';
                menu.classList.remove('hidden');
            } else {
                menu.classList.add('hidden');
            }
        });
        
        // Hide menu when clicking elsewhere
        document.addEventListener('mousedown', (e) => {
            if (!menu.contains(e.target)) {
                menu.classList.add('hidden');
            }
        });
        
        document.addEventListener('touchstart', (e) => {
            if (!menu.contains(e.target)) {
                // Small delay to allow selection to complete
                setTimeout(() => {
                    const selection = window.getSelection().toString().trim();
                    if (!selection) {
                        menu.classList.add('hidden');
                    }
                }, 100);
            }
        });
    ''')

ui.page('/')(create_page)
ui.run(port=9999)