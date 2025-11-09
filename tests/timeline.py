from nicegui import ui

# Sample Bible Chronology Data (you would use your complete list here)
bible_events = [
    {'year': '2166 BC', 'event': 'Abram (later Abraham) born (Gen 11:26)'},
    {'year': '2091 BC', 'event': 'Abram moves from Haran to Canaan (Gen 12:4)'},
    {'year': '2080 BC', 'event': 'Ishmael born (Gen 16:16)'},
    {'year': '2066 BC', 'event': 'Isaac born (Gen 21:5)'},
    {'year': '1991 BC', 'event': 'Abraham dies (Gen 25:7)'},
    {'year': '1446 BC', 'event': 'Exodus from Egypt (1 Kgs 6:1)'},
    {'year': '1040 BC', 'event': 'David born (2 Sam 5:2)'},
    {'year': '967 BC', 'event': 'Temple construction begun by Solomon (1 Kgs 6:1)'},
    {'year': '445 BC', 'event': 'Walls of Jerusalem rebuilt by Nehemiah (Neh 6:15)'},
    {'year': '2 BC', 'event': 'Birth of Jesus; Flight to Egypt (Matt 2:15)'},
    {'year': '33 AD', 'event': 'Crucifixion and Resurrection; Pentecost (Acts 2:1-41)'},
    {'year': '70 AD', 'event': 'Titus takes Jerusalem (Ant. 20:250)'},
]

@ui.page('/')
def main_page():
    ui.page_title('Bible Chronology Timeline')
    
    with ui.card().classes('w-full max-w-lg'):
        ui.label('📜 Bible Chronology').classes('text-2xl font-bold mb-4')
        
        # The core component: ui.timeline
        with ui.timeline(side='right'):
            # Loop through your events and create a ui.timeline_entry for each
            for item in bible_events:
                # The 'title' is the main event description
                # The 'subtitle' is the year, automatically positioned
                ui.timeline_entry(
                    title=item['event'],
                    subtitle=item['year'],
                    icon='calendar_today' # Using a NiceGUI/Material icon
                )

# To run the app: python your_file_name.py
ui.run(port=53535)