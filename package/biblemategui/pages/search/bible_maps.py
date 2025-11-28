from biblemategui.data.bible_locations import BIBLE_LOCATIONS
from biblemategui.fx.location_finder import LocationFinder
from agentmake.plugins.uba.lib.BibleBooks import BibleBooks
from agentmake.plugins.uba.lib.BibleParser import BibleVerseParser
from nicegui import ui, app
import math, re


# --- Data: 66 Bible Books & ID Mapping ---
BIBLE_BOOKS = [BibleBooks.abbrev["eng"][str(i)][0] for i in range(1,67)]

# Create a dictionary for Dropdown options: {ID: "Name (ID)"}
# This handles duplicate names by ensuring the value passed is the unique ID
LOCATION_OPTIONS = {
    uid: data[0] for uid, data in BIBLE_LOCATIONS.items()
}

# --- 2. HELPER FUNCTIONS ---

def haversine_distance(coord1, coord2, unit='km'):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers
    
    distance = c * r
    
    if unit == 'miles':
        return distance * 0.621371
    return distance

# --- 3. UI LAYOUT ---

def search_bible_maps(gui=None, q='', **_):

    def exlbl(event):
        nonlocal gui
        app.storage.user['tool_query'], *_ = event.args
        gui.select_empty_area2_tab()
        gui.load_area_2_content(title='Locations')
    ui.on('exlbl', exlbl)

    parser = BibleVerseParser(False)
    finder = LocationFinder()

    location_multiselect = None
    # Apply a full height column with no wrap so the map can stretch
    with ui.column().classes('w-full h-screen no-wrap p-4 gap-4'):

        # Dictionary to keep track of added layers {loc_id: layer}
        # Leaflet in NiceGUI doesn't have a direct "get_marker_by_id", so we track them locally
        active_markers = {} 

        def update_map_markers(selected_ids):
            """
            Synchronizes the map markers with the list of selected IDs.
            """
            current_ids = set(active_markers.keys())
            target_ids = set(selected_ids)

            # 1. Remove markers that are no longer selected
            to_remove = current_ids - target_ids
            for uid in to_remove:
                bible_map.remove_layer(active_markers[uid])
                del active_markers[uid]

            # 2. Add new markers
            to_add = target_ids - current_ids
            for uid in to_add:
                name, lat, lon = BIBLE_LOCATIONS[uid]
                # Add marker with popup
                marker = bible_map.marker(latlng=(lat, lon))
                marker.run_method('bindPopup', f'''<b>{name}</b><br>[<ref onclick="emitEvent('exlbl', ['{uid}']); return false;">{uid}</ref>]''')
                
                active_markers[uid] = marker
                
            # If we added exactly one new marker, pan to it
            if len(to_add) == 1:
                uid = list(to_add)[0]
                lat, lon = BIBLE_LOCATIONS[uid][1], BIBLE_LOCATIONS[uid][2]
                bible_map.set_center((lat, lon))
                bible_map.set_zoom(9)

        # ==========================================
        # CONTROLS
        # ==========================================
        with ui.card().classes('w-full'):
            #ui.label('📍 Map Explorer').classes('text-sm font-bold text-gray-500')
            
            with ui.row().classes('w-full items-center gap-4'):
                
                # Prepare options for multiselect with "All" and "None"
                # Using special keys that we can intercept
                multi_options = {
                    'CMD_ALL': 'All', 
                    'CMD_NONE': 'None'
                }
                multi_options.update(LOCATION_OPTIONS)

                # Multi-select dropdown
                location_multiselect = ui.select(
                    multi_options, 
                    label='Select', 
                    multiple=True,
                    with_input=True
                ).classes('w-30') # min-w-[40px]

                # Text Input for quick search
                search_input = ui.input(
                    label='Search',
                    value=q,
                    autocomplete=list(LOCATION_OPTIONS.values())+BIBLE_BOOKS,
                    placeholder='Enter name(s) or verse reference(s)...',
                ).classes('flex-grow')
                
                def on_search_enter():
                    """Finds a location by name and adds it to the multiselect (which triggers map update)"""
                    query = search_input.value.strip()
                    if not query: return

                    current_vals = location_multiselect.value or []

                    # when users enter verse reference(s)
                    if verseList := parser.extractAllReferences(query, tagged=False):
                        combinedLocations = []
                        for reference in verseList:
                            combinedLocations += finder.getLocationsFromReference(reference)
                        if found_id := sorted(list(set(combinedLocations))):
                            location_multiselect.value = list(set(current_vals + found_id))
                            ui.notify(f"{len(found_id)} locations found!")
                            search_input.value = ""
                            return
                    
                    # when users enter location id(s)
                    if re.search("^BL[0-9BL, ]+?$", query):
                        found_id = [i.strip() for i in query.split(",") if i.strip() in BIBLE_LOCATIONS]
                        if found_id:
                            location_multiselect.value = list(set(current_vals + found_id))
                            ui.notify(f"{len(found_id)} locations found!")
                            search_input.value = ""
                            if len(found_id) == 2:
                                loc1_select.value, loc2_select.value = found_id
                                calculate()
                            return

                    # when users enter location name(s)
                    query = search_input.value.lower()

                    found_id = []
                    for i in query.split(","):
                        i = i.strip()
                        if not i: continue
                        for uid, data in BIBLE_LOCATIONS.items():
                            if i in data[0].lower():
                                found_id.append(uid)
                                break
                    
                    if found_id:
                        # This update will trigger the on_value_change event
                        location_multiselect.value = list(set(current_vals + found_id))
                        ui.notify(f"{len(found_id)} locations found!")
                        search_input.value = "" # clear input
                    else:
                        ui.notify("Location not found", type='warning')

                search_input.on('keydown.enter', on_search_enter)

                # Intercept selection to handle "All" and "None" logic
                def handle_selection_change(e):
                    selected_values = e.value
                    
                    # Handle "All"
                    if 'CMD_ALL' in selected_values:
                        all_real_ids = list(LOCATION_OPTIONS.keys())
                        location_multiselect.value = all_real_ids
                        update_map_markers(all_real_ids)
                        return

                    # Handle "None"
                    if 'CMD_NONE' in selected_values:
                        location_multiselect.value = []
                        update_map_markers([])
                        return

                    # Normal update
                    update_map_markers(selected_values)

                # Bind the custom handler
                location_multiselect.on_value_change(handle_selection_change)

        # ==========================================
        # DISTANCE CALCULATOR
        # ==========================================
        with ui.card().classes('w-full'):
            #ui.label('📏 Bible Location Distance Calculator').classes('text-lg font-bold text-gray-700 mb-2')
            
            with ui.row().classes('w-full items-center gap-4'):
                # Location Selectors
                loc1_select = ui.select(LOCATION_OPTIONS, label='From', with_input=True).classes('w-35')
                loc2_select = ui.select(LOCATION_OPTIONS, label='To', with_input=True).classes('w-35')
                
                # Unit Toggle
                unit_radio = ui.radio(['km', 'miles'], value='km').props('inline')
                
                # Result Label
                result_label = ui.label('Distance').classes('text-lg font-medium text-secondary ml-auto mr-4')

                # Calculation Logic
                def calculate():
                    #nonlocal location_multiselect, result_label
                    if loc1_select.value and not loc1_select.value in location_multiselect.value:
                        location_multiselect.value = location_multiselect.value + [loc1_select.value]
                    if loc2_select.value and not loc2_select.value in location_multiselect.value:
                        location_multiselect.value = location_multiselect.value + [loc2_select.value]
                    if not loc1_select.value or not loc2_select.value:
                        result_label.text = "Select one more"
                        return
                    
                    # Get coordinates from ID
                    id1 = loc1_select.value
                    id2 = loc2_select.value
                    
                    coord1 = (BIBLE_LOCATIONS[id1][1], BIBLE_LOCATIONS[id1][2])
                    coord2 = (BIBLE_LOCATIONS[id2][1], BIBLE_LOCATIONS[id2][2])
                    
                    dist = haversine_distance(coord1, coord2, unit_radio.value)
                    unit_label = "km" if unit_radio.value == 'km' else "miles"
                    
                    result_label.text = f"{dist:.2f} {unit_label}"

                # Trigger calculation on button click or change
                #ui.button('Calculate', on_click=calculate).classes('bg-blue-600 text-white')
                
                # Auto-calculate when inputs change
                loc1_select.on_value_change(calculate)
                loc2_select.on_value_change(calculate)
                unit_radio.on_value_change(calculate)

        # ==========================================
        # LEAFLET MAP
        # ==========================================
        # center on Jerusalem approx
        bible_map = ui.leaflet(center=(31.777, 35.235), zoom=9).classes('w-full flex-grow rounded-lg shadow-md')

        if q:
            on_search_enter()