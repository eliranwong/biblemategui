from nicegui import ui

# --- Mock Data ---
# In your real app, this would likely come from a database or API.
# Dictionary mapping Hebrew words (or IDs) to audio URLs.
# Note: These are placeholder URLs. You will need real .mp3 files hosted or local.
WORD_DATA = {
    "בְּרֵאשִׁית": {"transliteration": "Bereshit", "audio": "https://example.com/bereshit.mp3"},
    "bārā": {"transliteration": "Bara", "audio": "https://example.com/bara.mp3"}, # Using keys usually requires unique IDs, but using text for demo
}

# A sample verse: Genesis 1:1
verse_words = [
    "בְּרֵאשִׁית", 
    "בָּרָא", 
    "אֱלֹהִים", 
    "אֵת", 
    "הַשָּׁמַיִם", 
    "וְאֵת", 
    "הָאָרֶץ"
]

class BibleAudioPlayer:
    def __init__(self):
        self.dialog = None
        self.audio_element = None
        self.current_word_label = None
        
    def show_player(self, word: str):
        """
        Opens the dialog and plays audio for the specific word.
        """
        # 1. Update the UI inside the dialog
        self.current_word_label.set_text(word)
        
        # 2. Logic to fetch the correct URL
        # In a real app, you might look up the word ID in your DB.
        # For this demo, we generate a dummy URL or use the dict.
        audio_url = f"https://example.com/audio/{word}.mp3" 
        
        # 3. Update audio source and play
        self.audio_element.set_source(audio_url)
        
        # Open the dialog
        self.dialog.open()
        
        # Optional: Auto-play when popup opens
        # self.audio_element.play() 

def main():
    player = BibleAudioPlayer()

    # --- Custom CSS for Hebrew Font & Styling ---
    ui.add_head_html('''
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Suez+One&display=swap');
            
            .hebrew-text {
                font-family: 'Suez One', serif;
                font-size: 2rem;
                cursor: pointer;
                transition: color 0.2s;
                padding: 0 4px;
            }
            .hebrew-text:hover {
                color: #1976D2; /* NiceGUI Blue */
                background-color: #f0f0f0;
                border-radius: 4px;
            }
            .verse-container {
                direction: rtl; /* Crucial for Hebrew layout */
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                justify-content: center;
            }
        </style>
    ''')

    # --- Header ---
    with ui.header().classes(replace='row items-center') as header:
        ui.icon('menu_book', size='32px').classes('text-white')
        ui.label('BibleMate AI').classes('text-h5 font-bold text-white')

    # --- Main Content ---
    with ui.column().classes('w-full items-center justify-center q-pa-md'):
        
        ui.label('Genesis 1:1').classes('text-h4 q-mb-lg text-gray-600')

        # --- The Hebrew Text Container ---
        # We loop through words to create individual clickable elements
        with ui.element('div').classes('verse-container max-w-screen-md'):
            for word in verse_words:
                # We use ui.label for the word
                lbl = ui.label(word).classes('hebrew-text')
                
                # We bind the click event. 
                # Note: We use a lambda with a default argument (w=word) to capture the current word in the loop scope.
                lbl.on('click', lambda _, w=word: player.show_player(w))

        ui.label('Click a word to hear pronunciation').classes('text-caption text-gray-400 q-mt-md')

    # --- The Popup Player (Dialog) ---
    # We define this once and reuse it (more efficient than creating new dialogs every click)
    with ui.dialog() as player.dialog, ui.card().classes('items-center justify-center min-w-[300px]'):
        
        # Close button
        with ui.row().classes('w-full justify-end'):
            ui.button(icon='close', on_click=player.dialog.close).props('flat round dense')
            
        # Large Hebrew Word display
        player.current_word_label = ui.label('').classes('text-h3 hebrew-text q-mb-md text-primary')
        
        # Transliteration placeholder (Static for demo, dynamic in real app)
        ui.label('Pronunciation Guide').classes('text-caption text-gray-500')
        
        # Audio Player Component
        # controls=True gives the user the play/pause/timeline UI
        player.audio_element = ui.audio('about:blank', controls=True).classes('w-full q-my-md')
        
        ui.label('Note: Audio URL is a placeholder for this demo.').classes('text-xs text-red-400')

    ui.run(title='BibleMate Audio Demo', port=9999)

if __name__ in {"__main__", "__mp_main__"}:
    main()