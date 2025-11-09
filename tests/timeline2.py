from nicegui import ui

output_label = None

# Function to be triggered when the link is clicked
def show_verse_details(reference: str):
    """Updates the output label with information about the clicked reference."""
    global output_label
    # A UI element to display the output
    output_label = ui.label("Click a Bible link below to see its details.").classes('mt-4 text-lg text-green-700')
    print(f"Python function triggered for: {reference}")
    output_label.set_text(f"Details for {reference}: You clicked the link! In a real app, this function could load verse text from a database or API.")

# Function to create the clickable link component
def create_internal_link(reference: str):
    # 1. Create the ui.link component (it looks like a link)
    link_component = ui.link(
        text=reference,
        target='#' # Set target to '#' or omit it since we are not opening a URL
    ).classes('text-blue-600 hover:text-blue-800 underline')
    
    # 2. Attach the Python function to the 'click' event
    # We use a lambda to pass the specific 'reference' string argument to the function
    link_component.on('click', lambda: show_verse_details(reference))
    
    return link_component

@ui.page('/')
def main_page():
    global output_label
    ui.page_title('Internal Link Trigger')
    
    bible_events = [
        {'year': '2166 BC', 'event': 'Abram (later Abraham) born', 'reference': 'Gen 11:26'},
        {'year': '2066 BC', 'event': 'Isaac born', 'reference': 'Gen 21:5'},
        {'year': '33 AD', 'event': 'Crucifixion and Resurrection', 'reference': 'Acts 2:1-41'},
    ]

    with ui.card().classes('w-full max-w-lg'):
        ui.label('📜 Chronology with Internal Links').classes('text-2xl font-bold mb-4')
        
        with ui.timeline(side='right'):
            for item in bible_events:
                # Create the interactive link
                ref_link = create_internal_link(item['reference'])
                
                with ui.timeline_entry(
                    title=item['event'],
                    subtitle=item['year'],
                    icon='menu_book'
                ):
                    with ui.row():
                        ref_link
                        
        # The element whose text is updated by the function
        output_label
        
ui.run(port=55555)