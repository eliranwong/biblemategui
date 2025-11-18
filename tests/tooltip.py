#!/usr/bin/env python3
"""
NiceGUI app with dynamic hover tooltips loaded from SQLite database
"""

from nicegui import ui, app
import sqlite3
from pathlib import Path
import json

# Initialize database
def init_database():
    """Create and populate sample database"""
    conn = sqlite3.connect('tooltips.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tooltips (
            word TEXT PRIMARY KEY,
            description TEXT,
            links TEXT
        )
    ''')
    
    # Sample data (links stored as JSON)
    sample_data = [
        ('Python', 'A high-level programming language', json.dumps([
            {'text': 'Official Documentation', 'url': 'https://docs.python.org'},
            {'text': 'Python Tutorial', 'url': 'https://www.python.org/about/gettingstarted/'},
            {'text': 'PyPI', 'url': 'https://pypi.org'}
        ])),
        ('NiceGUI', 'A Python UI framework', json.dumps([
            {'text': 'NiceGUI Docs', 'url': 'https://nicegui.io'},
            {'text': 'GitHub Repo', 'url': 'https://github.com/zauberzeug/nicegui'},
            {'text': 'Examples', 'url': 'https://nicegui.io/documentation'}
        ])),
        ('SQLite', 'A lightweight database engine', json.dumps([
            {'text': 'SQLite Home', 'url': 'https://www.sqlite.org'},
            {'text': 'Documentation', 'url': 'https://www.sqlite.org/docs.html'},
            {'text': 'Tutorial', 'url': 'https://www.sqlitetutorial.net'}
        ])),
        ('JavaScript', 'A programming language for the web', json.dumps([
            {'text': 'MDN Web Docs', 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript'},
            {'text': 'JavaScript.info', 'url': 'https://javascript.info'},
            {'text': 'W3Schools', 'url': 'https://www.w3schools.com/js/'}
        ]))
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO tooltips VALUES (?, ?, ?)', sample_data)
    conn.commit()
    conn.close()

def get_tooltip_data(word):
    """Fetch tooltip data from database"""
    conn = sqlite3.connect('tooltips.db')
    cursor = conn.cursor()
    cursor.execute('SELECT description, links FROM tooltips WHERE word = ?', (word,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        description, links_json = result
        links = json.loads(links_json)
        return {'description': description, 'links': links}
    return None

# Initialize the database
init_database()

# Create the NiceGUI app
@ui.page('/')
def main():
    # Add custom CSS for tooltips
    ui.add_head_html('''
    <style>
        .tooltip-word {
            color: #0066cc;
            cursor: help;
            text-decoration: underline dotted;
            position: relative;
            display: inline-block;
        }
        
        .tooltip-content {
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            min-width: 250px;
            z-index: 1000;
            margin-bottom: 8px;
            display: none;
        }
        
        .tooltip-content.active {
            display: block;
        }
        
        .tooltip-content::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: white transparent transparent transparent;
        }
        
        .tooltip-description {
            margin-bottom: 10px;
            color: #333;
            font-size: 14px;
        }
        
        .tooltip-links {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        
        .tooltip-link {
            color: #0066cc;
            text-decoration: none;
            font-size: 13px;
            padding: 4px 8px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }
        
        .tooltip-link:hover {
            background-color: #f0f0f0;
        }
        
        .loading {
            color: #666;
            font-style: italic;
        }
    </style>
    ''')
    
    # JavaScript for handling tooltips
    ui.add_body_html('''
    <script>
        let currentTooltip = null;
        let tooltipCache = {};
        let tooltipTimeout = null;
        
        async function fetchTooltipData(word) {
            // Check cache first
            if (tooltipCache[word]) {
                return tooltipCache[word];
            }
            
            try {
                const response = await fetch(`/api/tooltip/${encodeURIComponent(word)}`);
                if (response.ok) {
                    const data = await response.json();
                    tooltipCache[word] = data;
                    return data;
                }
            } catch (error) {
                console.error('Error fetching tooltip:', error);
            }
            return null;
        }
        
        async function showTooltip(element, word) {
            // Clear any pending hide timeout
            if (tooltipTimeout) {
                clearTimeout(tooltipTimeout);
                tooltipTimeout = null;
            }
            
            // Hide current tooltip if different element
            if (currentTooltip && currentTooltip !== element) {
                hideTooltip();
            }
            
            // Check if tooltip already exists
            let tooltip = element.querySelector('.tooltip-content');
            if (!tooltip) {
                // Create tooltip container
                tooltip = document.createElement('div');
                tooltip.className = 'tooltip-content';
                tooltip.innerHTML = '<div class="loading">Loading...</div>';
                element.appendChild(tooltip);
                
                // Fetch data
                const data = await fetchTooltipData(word);
                
                if (data) {
                    // Build tooltip content
                    let html = `<div class="tooltip-description">${data.description}</div>`;
                    html += '<div class="tooltip-links">';
                    for (const link of data.links) {
                        html += `<a href="${link.url}" target="_blank" class="tooltip-link">${link.text}</a>`;
                    }
                    html += '</div>';
                    tooltip.innerHTML = html;
                } else {
                    tooltip.innerHTML = '<div class="loading">No information available</div>';
                }
                
                // Keep tooltip visible when hovering over it
                tooltip.addEventListener('mouseenter', () => {
                    if (tooltipTimeout) {
                        clearTimeout(tooltipTimeout);
                        tooltipTimeout = null;
                    }
                });
                
                tooltip.addEventListener('mouseleave', () => {
                    tooltipTimeout = setTimeout(hideTooltip, 300);
                });
            }
            
            // Show tooltip
            tooltip.classList.add('active');
            currentTooltip = element;
        }
        
        function hideTooltip() {
            if (currentTooltip) {
                const tooltip = currentTooltip.querySelector('.tooltip-content');
                if (tooltip) {
                    tooltip.classList.remove('active');
                }
                currentTooltip = null;
            }
        }
        
        function initTooltips() {
            // Find all tooltip words and add event listeners
            document.querySelectorAll('.tooltip-word').forEach(element => {
                const word = element.dataset.word;
                
                element.addEventListener('mouseenter', () => {
                    showTooltip(element, word);
                });
                
                element.addEventListener('mouseleave', () => {
                    // Add delay before hiding to allow moving to tooltip
                    tooltipTimeout = setTimeout(hideTooltip, 300);
                });
            });
        }
        
        // Initialize tooltips when DOM is ready
        document.addEventListener('DOMContentLoaded', initTooltips);
        
        // Reinitialize after dynamic content changes
        const observer = new MutationObserver(() => {
            initTooltips();
        });
        observer.observe(document.body, { childList: true, subtree: true });
    </script>
    ''')
    
    # API endpoint for tooltip data
    @app.get('/api/tooltip/{word}')
    async def tooltip_api(word: str):
        data = get_tooltip_data(word)
        if data:
            return data
        return {'error': 'Not found'}, 404
    
    # Main UI
    ui.markdown('# Dynamic Tooltip Demo')
    
    # HTML content with tooltip words
    html_content = '''
    <div style="font-size: 16px; line-height: 1.8; padding: 20px; background: #f9f9f9; border-radius: 8px;">
        <h2>Welcome to Programming</h2>
        <p>
            Learning <span class="tooltip-word" data-word="Python">Python</span> is a great way to start your programming journey. 
            You can build beautiful web interfaces using <span class="tooltip-word" data-word="NiceGUI">NiceGUI</span>, 
            which makes it easy to create interactive applications.
        </p>
        <p>
            For data storage, <span class="tooltip-word" data-word="SQLite">SQLite</span> is a popular choice for small to medium applications. 
            When you need client-side interactivity, <span class="tooltip-word" data-word="JavaScript">JavaScript</span> comes in handy.
        </p>
        <p>
            Hover over the highlighted words to see more information and useful links!
        </p>
    </div>
    '''
    
    ui.html(html_content, sanitize=False)
    
    # Additional controls
    with ui.card().style('margin-top: 20px'):
        ui.label('Add New Tooltip Entry').classes('text-h6')
        
        with ui.row():
            word_input = ui.input('Word', placeholder='Enter word')
            desc_input = ui.input('Description', placeholder='Enter description')
        
        links_container = ui.column()
        
        def add_link_input():
            with links_container:
                with ui.row():
                    ui.input('Link Text', placeholder='Link text').classes('link-text')
                    ui.input('URL', placeholder='https://...').classes('link-url')
        
        ui.button('Add Link Field', on_click=add_link_input)
        add_link_input()  # Start with one link field
        
        def save_tooltip():
            word = word_input.value.strip()
            description = desc_input.value.strip()
            
            if not word or not description:
                ui.notify('Please enter word and description', color='negative')
                return
            
            # Collect links
            links = []
            link_rows = links_container.default_slot.children
            for row in link_rows:
                if hasattr(row, 'default_slot'):
                    inputs = row.default_slot.children
                    if len(inputs) >= 2:
                        text = inputs[0].value.strip() if hasattr(inputs[0], 'value') else ''
                        url = inputs[1].value.strip() if hasattr(inputs[1], 'value') else ''
                        if text and url:
                            links.append({'text': text, 'url': url})
            
            # Save to database
            conn = sqlite3.connect('tooltips.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT OR REPLACE INTO tooltips VALUES (?, ?, ?)',
                (word, description, json.dumps(links))
            )
            conn.commit()
            conn.close()
            
            # Clear cache for this word
            ui.run_javascript(f'delete tooltipCache["{word}"];')
            
            ui.notify(f'Tooltip for "{word}" saved successfully!', color='positive')
            
            # Clear inputs
            word_input.value = ''
            desc_input.value = ''
            links_container.clear()
            add_link_input()
        
        ui.button('Save Tooltip', on_click=save_tooltip, color='primary')
    
    # Display current tooltips in database
    with ui.card().style('margin-top: 20px'):
        ui.label('Current Tooltips in Database').classes('text-h6')
        
        def load_tooltips():
            conn = sqlite3.connect('tooltips.db')
            cursor = conn.cursor()
            cursor.execute('SELECT word, description FROM tooltips ORDER BY word')
            tooltips = cursor.fetchall()
            conn.close()
            
            with ui.column():
                for word, desc in tooltips:
                    ui.label(f'• {word}: {desc}').classes('text-body2')
        
        tooltip_list = ui.column()
        with tooltip_list:
            load_tooltips()
        
        ui.button('Refresh List', on_click=lambda: (tooltip_list.clear(), tooltip_list.__enter__(), load_tooltips()))

# Run the app
ui.run(title='Dynamic Tooltip Demo', port=9999)