from nicegui import ui

selected_text = {'value': ''}

ui.add_body_html('''
<script>
document.addEventListener('selectionchange', () => {
    const selection = window.getSelection().toString();
    if (selection) {
        emitEvent('selection_changed', { text: selection });
    }
});
</script>
''')

async def on_selection(e):
    selected_text['value'] = e.args['text']
    print(f"Selected: {selected_text['value']}")

ui.on('selection_changed', on_selection)

ui.label('Select some text from this paragraph to see it captured. You can select any text on the page and it will be stored in the variable.')

ui.button('Show Selection', on_click=lambda: ui.notify(selected_text['value'] or 'Nothing selected'))

ui.run(port=9999)