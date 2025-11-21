from nicegui import ui

# --- Data: 66 Bible Books & ID Mapping ---
BIBLE_BOOKS = [
    "Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth", "1Sam", "2Sam",
    "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps", "Prov",
    "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos", "Joel", "Amos",
    "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal",
    "Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph",
    "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Philem", "Heb",
    "Jas", "1Pet", "2Pet", "1John", "2John", "3John", "Jude", "Rev"
]

# Logic Sets
OT_BOOKS = BIBLE_BOOKS[:39]
NT_BOOKS = BIBLE_BOOKS[39:]
SET_OT = set(OT_BOOKS)
SET_NT = set(NT_BOOKS)

# Map abbreviations to Book IDs (1-66)
BOOK_MAP = {book: i + 1 for i, book in enumerate(BIBLE_BOOKS)}

def search_page():
    # --- State Management ---
    # Initialize with full selection state
    initial_selection = ['All', 'OT', 'NT'] + BIBLE_BOOKS
    state = {'previous': initial_selection}

    with ui.column().classes('w-full max-w-3xl mx-auto p-4 gap-4'):
        ui.markdown('## Bible Verse Search')

        # --- Search Row ---
        with ui.row().classes('w-full items-start gap-4'):
            # 1. Search Input
            search_input = ui.input(
                label='Search term', 
                placeholder='e.g. "Light" or "Grace"'
            ).classes('flex-grow')

            # 2. Scope Dropdown
            # Options: All, None, OT, NT, then the books
            options = ['All', 'None', 'OT', 'NT'] + BIBLE_BOOKS
            
            scope_select = ui.select(
                options=options,
                label='Search Scope',
                multiple=True,
                with_input=True
            ).classes('w-64')

        # --- SQL Query Feedback Label ---
        ui.label('Generated Query:').classes('text-gray-500 text-sm mt-4')
        query_label = ui.label('SELECT * FROM Verses').classes('font-mono bg-gray-100 p-2 rounded w-full')

        # --- Logic Functions ---

        def update_query_label(selected_values):
            """Generates the SQLite query based on selection."""
            term = search_input.value
            
            # Filter to keep ONLY the actual book strings (ignore All/None/OT/NT)
            real_books = [b for b in selected_values if b in BIBLE_BOOKS]
            book_ids = [str(BOOK_MAP[b]) for b in real_books]
            
            base_query = "SELECT * FROM Verses"
            where_clauses = []

            # Handle Book Logic
            if 'All' in selected_values:
                pass 
            elif not real_books:
                where_clauses.append("1=0")
            elif len(real_books) == 1:
                where_clauses.append(f"Book={book_ids[0]}")
            else:
                # Optimization: check if it's exactly OT or NT for cleaner SQL?
                # (Optional, but strictly sticking to IDs is safer for the engine)
                where_clauses.append(f"Book IN ({', '.join(book_ids)})")

            # Handle Search Term
            if term:
                where_clauses.append(f"Text LIKE '%{term}%'")

            # Assemble
            full_query = base_query
            if where_clauses:
                full_query += " WHERE " + " AND ".join(where_clauses)
            
            query_label.set_text(full_query)

        def handle_scope_change(e):
            """
            Handles complex logic for All, None, OT, NT and individual books.
            """
            current = e.value if e.value else []
            previous = state['previous']
            
            # 1. Determine Triggers
            added = set(current) - set(previous)
            removed = set(previous) - set(current)
            
            # Start with the currently selected actual books
            selected_books = set(x for x in current if x in BIBLE_BOOKS)

            # 2. Apply High-Level Triggers
            # Priority: None > All > OT/NT > Individual removals

            if 'None' in added:
                selected_books.clear()
            
            elif 'All' in added:
                selected_books = set(BIBLE_BOOKS)
            
            elif 'OT' in added:
                selected_books.update(SET_OT)
            
            elif 'NT' in added:
                selected_books.update(SET_NT)
            
            # Handle Removals of Groups
            # We only remove the group's books if the group TAG was explicitly removed
            elif 'All' in removed and len(removed) == 1:
                 # User clicked 'All' to uncheck it -> Clear all
                 selected_books.clear()
            
            elif 'OT' in removed:
                # Check if OT tag was explicitly removed (not just because a child book was clicked)
                # If a child was clicked, 'removed' contains {'ChildBook'}.
                # If OT tag was clicked, 'removed' contains {'OT'}.
                # Note: NiceGUI might remove OT from 'current' automatically if child removed,
                # but 'removed' set captures the diff.
                if not (removed & SET_OT): # If no individual OT books were in the removed set
                    selected_books -= SET_OT

            elif 'NT' in removed:
                if not (removed & SET_NT):
                    selected_books -= SET_NT

            # 3. Reconstruct Selection State
            # We rebuild the list from scratch based on the books we decided are selected
            new_selection = []
            
            # Helper: Check completeness
            has_ot = SET_OT.issubset(selected_books)
            has_nt = SET_NT.issubset(selected_books)
            has_all = len(selected_books) == 66
            is_empty = len(selected_books) == 0

            # Add Meta Tags
            if has_all:
                new_selection.append('All')
            if is_empty:
                new_selection.append('None')
            if has_ot:
                new_selection.append('OT')
            if has_nt:
                new_selection.append('NT')

            # Add Books (maintain order)
            for book in BIBLE_BOOKS:
                if book in selected_books:
                    new_selection.append(book)

            # 4. Update UI and State
            if set(new_selection) != set(current):
                scope_select.value = new_selection
                state['previous'] = new_selection
                update_query_label(new_selection)
                return

            state['previous'] = current
            update_query_label(current)

        # --- Bindings ---
        scope_select.on_value_change(handle_scope_change)
        search_input.on_value_change(lambda e: update_query_label(scope_select.value))

        # Initialize
        scope_select.value = initial_selection

# Run the app
if __name__ in {"__main__", "__mp_main__"}:
    search_page()
    ui.run(title="BibleMate AI Search", port=9999)