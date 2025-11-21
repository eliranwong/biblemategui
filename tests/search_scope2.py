from nicegui import ui

# Bible books abbreviations (66 books)
BIBLE_BOOKS = [
    'Gen', 'Exo', 'Lev', 'Num', 'Deu', 'Jos', 'Jdg', 'Rut', '1Sa', '2Sa',
    '1Ki', '2Ki', '1Ch', '2Ch', 'Ezr', 'Neh', 'Est', 'Job', 'Psa', 'Pro',
    'Ecc', 'Son', 'Isa', 'Jer', 'Lam', 'Eze', 'Dan', 'Hos', 'Joe', 'Amo',
    'Oba', 'Jon', 'Mic', 'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal', 'Mat',
    'Mar', 'Luk', 'Joh', 'Act', 'Rom', '1Co', '2Co', 'Gal', 'Eph', 'Phi',
    'Col', '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm', 'Heb', 'Jas', '1Pe',
    '2Pe', '1Jo', '2Jo', '3Jo', 'Jud', 'Rev'
]

def create_search_page():
    # Create options list with All and None at the beginning
    options = ['All', 'None'] + BIBLE_BOOKS
    
    # Track current selection
    selected_books = []
    
    def generate_sql_query():
        """Generate SQL query based on selected books"""
        if not selected_books or 'None' in selected_books:
            return "SELECT * FROM Verses WHERE 1=0"  # No results
        elif 'All' in selected_books or len(selected_books) == 66:
            return "SELECT * FROM Verses"
        elif len(selected_books) == 1:
            book_index = BIBLE_BOOKS.index(selected_books[0]) + 1
            return f"SELECT * FROM Verses WHERE Book={book_index}"
        else:
            # Multiple books selected
            book_indices = [str(BIBLE_BOOKS.index(book) + 1) for book in selected_books]
            return f"SELECT * FROM Verses WHERE Book IN ({', '.join(book_indices)})"
    
    def on_selection_change(e):
        """Handle selection changes"""
        nonlocal selected_books
        new_selection = e.value if isinstance(e.value, list) else []
        
        # Handle "All" selection
        if 'All' in new_selection and 'All' not in selected_books:
            # "All" was just selected
            selected_books = ['All'] + BIBLE_BOOKS.copy()
            book_select.set_value(selected_books)
        
        # Handle "None" selection
        elif 'None' in new_selection:
            # "None" was selected
            selected_books = []
            book_select.set_value([])
        
        # Handle "All" deselection
        elif 'All' not in new_selection and 'All' in selected_books:
            # "All" was deselected, remove all books
            selected_books = []
            book_select.set_value([])
        
        # Handle individual book selections
        else:
            # Filter out "All" and "None" from selection
            selected_books = [book for book in new_selection if book not in ['All', 'None']]
            
            # Auto-select "All" if all 66 books are selected
            if len(selected_books) == 66:
                selected_books = ['All'] + selected_books
                book_select.set_value(selected_books)
            else:
                book_select.set_value(selected_books)
        
        # Update SQL query label
        sql_query = generate_sql_query()
        query_label.set_text(sql_query)
        
        # Notify about the change
        print(f"Selection changed: {len([b for b in selected_books if b not in ['All', 'None']])} books selected")
        print(f"Current query: {sql_query}")
    
    with ui.row().classes('items-center gap-4 w-full'):
        # Search input
        search_input = ui.input(
            label='Search',
            placeholder='Enter search term...'
        ).classes('flex-grow')
        
        # Multi-select dropdown for books
        book_select = ui.select(
            options=options,
            multiple=True,
            label='Search Scope',
            on_change=on_selection_change
        ).classes('w-64')
    
    # SQL query label
    query_label = ui.label('SELECT * FROM Verses WHERE 1=0').classes('text-sm text-gray-600 mt-4')
    
    return search_input, book_select, query_label

# Create the page
create_search_page()

ui.run(port=9999)