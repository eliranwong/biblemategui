"""
Bible Morphology Word Cards Page
A beautiful display of verse words with their linguistic data
"""

from nicegui import ui
import sqlite3
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class WordData:
    word_id: int
    clause_id: int
    book: str
    chapter: int
    verse: int
    word: str  # Hebrew/Greek word
    lexical_entry: str
    morphology_code: str
    morphology: str  # Full morphology description
    lexeme: str
    transliteration: str
    pronunciation: str
    interlinear: str
    translation: str
    gloss: str


# Color mapping for different parts of speech
POS_COLORS = {
    'verb': {'bg': '#1a365d', 'border': '#3182ce', 'badge': '#4299e1'},
    'noun': {'bg': '#234e52', 'border': '#38b2ac', 'badge': '#4fd1c5'},
    'preposition': {'bg': '#744210', 'border': '#d69e2e', 'badge': '#ecc94b'},
    'conjunction': {'bg': '#553c9a', 'border': '#9f7aea', 'badge': '#b794f4'},
    'article': {'bg': '#702459', 'border': '#d53f8c', 'badge': '#ed64a6'},
    'adjective': {'bg': '#285e61', 'border': '#4fd1c5', 'badge': '#81e6d9'},
    'pronoun': {'bg': '#3c366b', 'border': '#7c3aed', 'badge': '#a78bfa'},
    'adverb': {'bg': '#92400e', 'border': '#f59e0b', 'badge': '#fbbf24'},
    'particle': {'bg': '#065f46', 'border': '#10b981', 'badge': '#34d399'},
    'default': {'bg': '#1f2937', 'border': '#6b7280', 'badge': '#9ca3af'},
}


def get_pos_from_morphology(morphology: str) -> str:
    """Extract part of speech from morphology string."""
    morph_lower = morphology.lower()
    for pos in POS_COLORS.keys():
        if pos in morph_lower:
            return pos
    return 'default'


def parse_morphology(morphology: str) -> List[str]:
    """Parse morphology string into individual components."""
    return [m.strip() for m in morphology.split(',') if m.strip()]


def get_words_for_verse(db_path: str, book: str, chapter: int, verse: int) -> List[WordData]:
    """Fetch all words for a specific verse from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT wordID, clauseID, book, chapter, verse, word, 
               lexicalEntry, morphologyCode, morphology, lexeme,
               transliteration, pronunciation, interlinear, translation, gloss
        FROM words
        WHERE book = ? AND chapter = ? AND verse = ?
        ORDER BY wordID
    """, (book, chapter, verse))
    
    words = []
    for row in cursor.fetchall():
        words.append(WordData(*row))
    
    conn.close()
    return words


# Sample data for demonstration
SAMPLE_WORDS = [
    WordData(1, 1, 'Genesis', 1, 1, 'בְּ', 'E70001,H9003', 'prep', 'preposition', 'בְּ', 'bĕ', 'bᵊ', 'in', 'In', 'in'),
    WordData(2, 1, 'Genesis', 1, 1, 'רֵאשִׁ֖ית', 'E70002,H7225', 'subs.f.sg.a', 'noun,feminine,singular,absolute', 'רֵאשִׁית', 'rēšît', 'rēšˌîṯ', 'beginning', 'the beginning', 'beginning'),
    WordData(3, 1, 'Genesis', 1, 1, 'בָּרָ֣א', 'E70003,H1254', 'verb.qal.perf.p3.m.sg', 'verb,qal,perfect,third person,masculine,singular', 'ברא', 'bārā', 'bārˈā', '[he]+ create', 'created', 'create'),
    WordData(4, 1, 'Genesis', 1, 1, 'אֱלֹהִ֑ים', 'E70004,H430', 'subs.m.pl.a', 'noun,masculine,plural,absolute', 'אֱלֹהִים', 'ʾĕlōhîm', 'ʔᵉlōhˈîm', 'god [pl.]', 'God', 'god(s)'),
    WordData(5, 1, 'Genesis', 1, 1, 'אֵ֥ת', 'E70005,H853', 'prep', 'preposition', 'אֵת', 'ʾēt', 'ʔˌēṯ', '[object marker]', '[object marker]', ''),
    WordData(6, 1, 'Genesis', 1, 1, 'הַ', 'E70006,H9009', 'art', 'article', 'הַ', 'ha', 'ha', 'the', 'the', 'the'),
    WordData(7, 1, 'Genesis', 1, 1, 'שָּׁמַ֖יִם', 'E70007,H8064', 'subs.m.pl.a', 'noun,masculine,plural,absolute', 'שָׁמַיִם', 'šāmayim', 'ššāmˌayim', 'heavens', 'heavens', 'heavens'),
    WordData(8, 1, 'Genesis', 1, 1, 'וְ', 'E70008,H9000', 'conj', 'conjunction', 'וְ', 'wĕ', 'wᵊ', 'and', 'and', ''),
    WordData(9, 1, 'Genesis', 1, 1, 'אֵ֥ת', 'E70005,H853', 'prep', 'preposition', 'אֵת', 'ʾēt', 'ʔˌēṯ', '[object marker]', 'and', '[object marker]'),
    WordData(10, 1, 'Genesis', 1, 1, 'הָ', 'E70006,H9009', 'art', 'article', 'הַ', 'hā', 'hā', 'the', 'the', 'the'),
    WordData(11, 1, 'Genesis', 1, 1, 'אָֽרֶץ', 'E70009,H776', 'subs.u.sg.a', 'noun,unknown,singular,absolute', 'אֶרֶץ', 'ʾāreṣ', 'ʔˈāreṣ', 'earth', 'earth.', 'earth'),
]


def create_morphology_page():
    """Create the morphology analysis page."""
    
    # Custom CSS for the page
    ui.add_head_html('''
    <link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@400;500;700&family=Noto+Sans+Hebrew:wght@400;500;600;700&family=Source+Sans+3:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0f1a;
            --bg-secondary: #111827;
            --bg-card: #1a202c;
            --text-primary: #f7fafc;
            --text-secondary: #a0aec0;
            --text-muted: #718096;
            --accent-gold: #d69e2e;
            --accent-blue: #4299e1;
            --border-subtle: rgba(255, 255, 255, 0.08);
        }
        
        body {
            background: linear-gradient(135deg, var(--bg-primary) 0%, #0f172a 50%, #1a1a2e 100%);
            min-height: 100vh;
        }
        
        .hebrew-word {
            font-family: 'Noto Sans Hebrew', 'Frank Ruhl Libre', serif;
            font-size: 2.5rem;
            font-weight: 500;
            line-height: 1.2;
            direction: rtl;
            background: linear-gradient(135deg, #fefcbf 0%, #f6e05e 50%, #ecc94b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 40px rgba(236, 201, 75, 0.3);
        }
        
        .word-card {
            background: linear-gradient(145deg, rgba(26, 32, 44, 0.9) 0%, rgba(17, 24, 39, 0.95) 100%);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            backdrop-filter: blur(10px);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .word-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--card-accent, linear-gradient(90deg, #4299e1, #9f7aea));
            opacity: 0.8;
        }
        
        .word-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 
                        0 0 60px rgba(66, 153, 225, 0.1);
            border-color: rgba(255, 255, 255, 0.15);
        }
        
        .morphology-badge {
            font-family: 'Source Sans 3', sans-serif;
            font-size: 0.7rem;
            font-weight: 500;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            padding: 4px 10px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: var(--text-secondary);
            transition: all 0.2s ease;
        }
        
        .morphology-badge:hover {
            background: rgba(255, 255, 255, 0.12);
            transform: scale(1.05);
        }
        
        .pos-badge {
            font-family: 'Source Sans 3', sans-serif;
            font-size: 0.65rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            padding: 4px 12px;
            border-radius: 4px;
        }
        
        .data-label {
            font-family: 'Source Sans 3', sans-serif;
            font-size: 0.65rem;
            font-weight: 500;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--text-muted);
        }
        
        .data-value {
            font-family: 'Source Sans 3', sans-serif;
            font-size: 0.95rem;
            font-weight: 400;
            color: var(--text-primary);
        }
        
        .transliteration {
            font-family: 'Source Sans 3', sans-serif;
            font-style: italic;
            color: var(--accent-gold);
            font-size: 1.1rem;
        }
        
        .gloss-text {
            font-family: 'Frank Ruhl Libre', serif;
            font-size: 1.3rem;
            font-weight: 500;
            color: var(--text-primary);
        }
        
        .verse-header {
            font-family: 'Frank Ruhl Libre', serif;
            background: linear-gradient(135deg, rgba(26, 32, 44, 0.8) 0%, rgba(17, 24, 39, 0.9) 100%);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }
        
        .verse-ref {
            font-family: 'Frank Ruhl Libre', serif;
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #f7fafc 0%, #e2e8f0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .word-number {
            font-family: 'Source Sans 3', sans-serif;
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--text-muted);
            position: absolute;
            top: 12px;
            right: 12px;
            opacity: 0.6;
        }
        
        .lexical-code {
            font-family: 'SF Mono', 'Fira Code', monospace;
            font-size: 0.75rem;
            color: var(--text-muted);
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 8px;
            border-radius: 4px;
        }
        
        .divider {
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, var(--border-subtle) 50%, transparent 100%);
            margin: 12px 0;
        }
        
        .cards-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .word-card {
            animation: fadeInUp 0.5s ease forwards;
        }
        
        .full-verse-text {
            font-family: 'Noto Sans Hebrew', serif;
            font-size: 1.4rem;
            direction: rtl;
            line-height: 2;
            color: var(--text-secondary);
        }
        
        .full-verse-text .word-highlight {
            cursor: pointer;
            padding: 2px 4px;
            border-radius: 4px;
            transition: all 0.2s ease;
        }
        
        .full-verse-text .word-highlight:hover {
            background: rgba(214, 158, 46, 0.2);
            color: var(--accent-gold);
        }
    </style>
    ''')
    
    # Page container
    with ui.column().classes('w-full min-h-screen p-4 md:p-8'):
        
        # Header section
        with ui.row().classes('w-full items-center justify-between mb-6 verse-header p-4'):
            with ui.column().classes('gap-1'):
                ui.label('Word Analysis').classes('text-xs uppercase tracking-widest text-gray-500')
                ui.label('Genesis 1:1').classes('verse-ref')
            
            # Verse selector (simplified for demo)
            with ui.row().classes('gap-2 items-center'):
                ui.select(
                    options=['Genesis', 'Exodus', 'Leviticus'],
                    value='Genesis',
                    label='Book'
                ).classes('w-32').props('dark dense outlined')
                
                ui.number(label='Chapter', value=1, min=1, max=50).classes('w-20').props('dark dense outlined')
                ui.number(label='Verse', value=1, min=1, max=50).classes('w-20').props('dark dense outlined')
                
                ui.button(icon='search', color='amber').props('flat dense')
        
        # Full verse display
        with ui.card().classes('w-full mb-6 verse-header p-4'):
            ui.label('בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃').classes('full-verse-text text-center')
            ui.label('In the beginning God created the heavens and the earth.').classes('text-center text-gray-400 mt-2 italic')
        
        # Word cards grid
        with ui.element('div').classes('cards-container'):
            for idx, word in enumerate(SAMPLE_WORDS):
                create_word_card(word, idx)


def create_word_card(word: WordData, index: int):
    """Create a single word card with morphology data."""
    pos = get_pos_from_morphology(word.morphology)
    colors = POS_COLORS.get(pos, POS_COLORS['default'])
    morph_parts = parse_morphology(word.morphology)
    
    # Apply animation delay based on index
    delay = index * 0.08
    
    with ui.card().classes('word-card p-4 relative').style(
        f'animation-delay: {delay}s; --card-accent: linear-gradient(90deg, {colors["border"]}, {colors["badge"]})'
    ):
        # Word number indicator
        ui.label(f'#{index + 1}').classes('word-number')
        
        # Main Hebrew word
        with ui.column().classes('items-center gap-2 mb-3'):
            ui.label(word.word).classes('hebrew-word')
            ui.label(word.transliteration).classes('transliteration')
        
        # Part of speech badge
        with ui.row().classes('justify-center mb-3'):
            ui.label(pos.upper()).classes('pos-badge').style(
                f'background: {colors["bg"]}; color: {colors["badge"]}; border: 1px solid {colors["border"]}'
            )
        
        # Divider
        ui.element('div').classes('divider')
        
        # Morphology badges
        if len(morph_parts) > 1:
            with ui.row().classes('flex-wrap gap-1 justify-center mb-3'):
                for part in morph_parts[1:]:  # Skip first (POS already shown)
                    if part.strip():
                        ui.label(part).classes('morphology-badge')
        
        # Divider
        ui.element('div').classes('divider')
        
        # Data rows
        with ui.column().classes('gap-3 mt-2'):
            # Gloss / Translation
            with ui.column().classes('gap-0'):
                ui.label('MEANING').classes('data-label')
                ui.label(word.gloss or word.translation or word.interlinear).classes('gloss-text')
            
            # Lexeme
            with ui.row().classes('justify-between items-center'):
                with ui.column().classes('gap-0'):
                    ui.label('LEXEME').classes('data-label')
                    ui.label(word.lexeme).classes('data-value').style('font-family: "Noto Sans Hebrew", serif; font-size: 1.1rem;')
                
                with ui.column().classes('gap-0 text-right'):
                    ui.label('PRONUNCIATION').classes('data-label')
                    ui.label(word.pronunciation).classes('data-value text-gray-300')
            
            # Lexical Entry (Strong's numbers etc)
            with ui.row().classes('justify-center mt-2'):
                for entry in word.lexical_entry.split(','):
                    if entry.strip():
                        ui.label(entry.strip()).classes('lexical-code')


def main():
    """Main entry point."""
    
    @ui.page('/')
    def index():
        create_morphology_page()
    
    @ui.page('/morphology')
    def morphology():
        create_morphology_page()

main()

ui.run(title='Bible Morphology Analysis', favicon='📖', port=9999)

