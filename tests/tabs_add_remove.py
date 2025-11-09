from nicegui import ui

# Global variable to track current layout
current_layout = 1  # 1, 2, or 3
area1_container = None
area2_container = None
area1_wrapper = None
area2_wrapper = None
splitter = None
is_lt_sm = False

# Tab panels and active tab tracking
area1_tabs = None
area2_tabs = None
area1_tab_panels = {}  # Dictionary to store tab panels by name
area2_tab_panels = {}
area1_tab_panels_container = None
area2_tab_panels_container = None
area1_tab_counter = 3  # Counter for new tabs in Area 1
area2_tab_counter = 5  # Counter for new tabs in Area 2

@ui.page('/')
def page_home(q: str | None = None):
    create_menu()
    create_content_areas()

def create_menu():
    """Create horizontal navigation bar at the top"""
    with ui.header().classes('items-center'):
        with ui.row().classes('items-center gap-4'):
            ui.button('Swap Layout', on_click=swap_layout, icon='swap_horiz')
            ui.button('Example Page 1', on_click=load_area_1_content, icon='description')
            ui.button('Example Page 2', on_click=load_area_2_content, icon='article')
            ui.separator().props('vertical')
            ui.button('Add Tab Area 1', on_click=add_tab_area1, icon='add')
            ui.button('Remove Tab Area 1', on_click=remove_tab_area1, icon='remove')
            ui.separator().props('vertical')
            ui.button('Add Tab Area 2', on_click=add_tab_area2, icon='add')
            ui.button('Remove Tab Area 2', on_click=remove_tab_area2, icon='remove')

def check_breakpoint(ev):
    global is_lt_sm, splitter
    # prefer the well-known attributes
    width = getattr(ev, 'width', None)
    # fallback: some versions wrap data inside an attribute (try common names)
    if width is None:
        for maybe in ('args', 'arguments', 'data', 'payload'):
            candidate = getattr(ev, maybe, None)
            if isinstance(candidate, dict) and 'width' in candidate:
                width = candidate['width']
                break
    if width is None:
        print('Could not determine width from event:', ev)
        return
    is_lt_sm = width < 640   # tailwind sm = 640px
    if splitter:
        if is_lt_sm:
            splitter.props('horizontal')
        else:
            splitter.props(remove='horizontal')

def create_content_areas():
    """Create two scrollable areas with responsive layout"""
    global area1_wrapper, area2_wrapper, splitter, is_lt_sm
    global area1_tabs, area2_tabs, area1_tab_panels, area2_tab_panels
    global area1_tab_panels_container, area2_tab_panels_container
    # listen to the resize event
    ui.on('resize', check_breakpoint)
    # Create splitter
    splitter = ui.splitter(value=100, horizontal=is_lt_sm).classes('w-full').style('height: calc(100vh - 64px)')
    
    # Area 1 with 4 tabs
    with splitter.before:
        area1_wrapper = ui.column().classes('w-full h-full')
        with area1_wrapper:
            area1_tabs = ui.tabs().classes('w-full')
            with area1_tabs:
                ui.tab('tab1_1', label='Bible 1')
                ui.tab('tab1_2', label='Bible 2')
                ui.tab('tab1_3', label='Bible 3')
            
            area1_tab_panels_container = ui.tab_panels(area1_tabs, value='tab1_1').classes('w-full h-full')
            
            with area1_tab_panels_container:
                with ui.tab_panel('tab1_1'):
                    area1_tab_panels['tab1_1'] = ui.scroll_area().classes('w-full h-full p-4')
                    with area1_tab_panels['tab1_1']:
                        ui.label('Bible Area').classes('text-2xl font-bold mb-4')
                        ui.label('Bible content is placed here.').classes('text-gray-600')
                
                with ui.tab_panel('tab1_2'):
                    area1_tab_panels['tab1_2'] = ui.scroll_area().classes('w-full h-full p-4')
                    with area1_tab_panels['tab1_2']:
                        ...
                
                with ui.tab_panel('tab1_3'):
                    area1_tab_panels['tab1_3'] = ui.scroll_area().classes('w-full h-full p-4')
                    with area1_tab_panels['tab1_3']:
                        ...
    
    # Area 2 with 5 tabs
    with splitter.after:
        area2_wrapper = ui.column().classes('w-full h-full')
        with area2_wrapper:
            area2_tabs = ui.tabs().classes('w-full')
            with area2_tabs:
                ui.tab('tab2_1', label='Tool 1')
                ui.tab('tab2_2', label='Tool 2')
                ui.tab('tab2_3', label='Tool 3')
                ui.tab('tab2_4', label='Tool 4')
                ui.tab('tab2_5', label='Tool 5')
            
            area2_tab_panels_container = ui.tab_panels(area2_tabs, value='tab2_1').classes('w-full h-full')
            
            with area2_tab_panels_container:
                with ui.tab_panel('tab2_1'):
                    area2_tab_panels['tab2_1'] = ui.scroll_area().classes('w-full h-full p-4')
                    with area2_tab_panels['tab2_1']:
                        ui.label('Tool Area').classes('text-2xl font-bold mb-4')
                        ui.label('Tool content is placed here.').classes('text-gray-600')
                
                with ui.tab_panel('tab2_2'):
                    area2_tab_panels['tab2_2'] = ui.scroll_area().classes('w-full h-full p-4')
                    with area2_tab_panels['tab2_2']:
                        ...
                
                with ui.tab_panel('tab2_3'):
                    area2_tab_panels['tab2_3'] = ui.scroll_area().classes('w-full h-full p-4')
                    with area2_tab_panels['tab2_3']:
                        ...
                
                with ui.tab_panel('tab2_4'):
                    area2_tab_panels['tab2_4'] = ui.scroll_area().classes('w-full h-full p-4')
                    with area2_tab_panels['tab2_4']:
                        ...
                
                with ui.tab_panel('tab2_5'):
                    area2_tab_panels['tab2_5'] = ui.scroll_area().classes('w-full h-full p-4')
                    with area2_tab_panels['tab2_5']:
                        ...
    
    # Set initial visibility (Area 1 visible, Area 2 hidden)
    update_visibility()

def swap_layout():
    """Swap between three layout modes"""
    global current_layout
    
    current_layout = (current_layout % 3) + 1
    update_visibility()
    ui.notify(f'Switched to Layout {current_layout}')

def update_visibility():
    """Update visibility of areas based on current layout"""
    global current_layout, area1_wrapper, area2_wrapper, splitter
    
    if current_layout == 1:
        # Area 1 visible, Area 2 invisible - maximize Area 1
        area1_wrapper.set_visibility(True)
        area2_wrapper.set_visibility(False)
        splitter.set_value(100)  # Move splitter to maximize Area 1
    elif current_layout == 2:
        # Both areas visible - 50/50 split
        area1_wrapper.set_visibility(True)
        area2_wrapper.set_visibility(True)
        splitter.set_value(50)  # Move splitter to middle
    elif current_layout == 3:
        # Area 1 invisible, Area 2 visible - maximize Area 2
        area1_wrapper.set_visibility(False)
        area2_wrapper.set_visibility(True)
        splitter.set_value(0)  # Move splitter to maximize Area 2

def get_active_area1_tab():
    """Get the currently active tab in Area 1"""
    global area1_tab_panels_container
    return area1_tab_panels_container.value

def get_active_area2_tab():
    """Get the currently active tab in Area 2"""
    global area2_tab_panels_container
    return area2_tab_panels_container.value

def load_area_1_content(content, title="Bible"):
    """Load example content in the active tab of Area 1"""
    global area1_tab_panels, area1_tabs
    
    # Get the currently active tab
    active_tab = get_active_area1_tab()
    # Get the active tab's scroll area
    active_panel = area1_tab_panels[active_tab]
    # Clear and load new content
    active_panel.clear()
    with active_panel:
        # load content here
        content()
    # Update tab label to reflect new content
    for child in area1_tabs:
        if hasattr(child, '_props') and child._props.get('name') == active_tab:
            child.props(f'label="{title}"')
            break
    #ui.notify(f'Loaded content in Area 1 - {active_tab}')

def load_area_2_content(content, title="Tool"):
    """Load example content in the active tab of Area 2"""
    global area2_tab_panels, area2_tabs
    
    # Get the currently active tab
    active_tab = get_active_area2_tab()
    # Get the active tab's scroll area
    active_panel = area2_tab_panels[active_tab]
    # Clear and load new content
    active_panel.clear()
    with active_panel:
        content()
    # Update tab label to reflect new content
    for child in area2_tabs:
        if hasattr(child, '_props') and child._props.get('name') == active_tab:
            child.props(f'label="{title}"')
            break
    #ui.notify(f'Loaded content in Area 2 - {active_tab}')

def add_tab_area1():
    """Dynamically add a new tab to Area 1"""
    global area1_tab_counter, area1_tabs, area1_tab_panels, area1_tab_panels_container
    
    area1_tab_counter += 1
    new_tab_name = f'tab1_{area1_tab_counter}'
    # Add new tab
    with area1_tabs:
        ui.tab(new_tab_name, label=f'Bible {area1_tab_counter}')
    # Add new tab panel
    with area1_tab_panels_container:
        with ui.tab_panel(new_tab_name):
            area1_tab_panels[new_tab_name] = ui.scroll_area().classes('w-full h-full p-4')
            with area1_tab_panels[new_tab_name]:
                ...
    #ui.notify(f'Added Tab {area1_tab_counter} to Area 1')

def remove_tab_area1():
    """Remove the currently active tab from Area 1"""
    global area1_tab_panels, area1_tabs, area1_tab_panels_container
    
    active_tab = get_active_area1_tab()
    # Don't allow removing if it's the last tab
    if len(area1_tab_panels) <= 1:
        ui.notify('Cannot remove the last tab!', type='warning')
        return
    # Find and remove the tab
    tab_to_remove = None
    for child in area1_tabs:
        if hasattr(child, '_props') and child._props.get('name') == active_tab:
            tab_to_remove = child
            break
    if tab_to_remove:
        # Switch to a different tab before removing
        remaining_tabs = [k for k in area1_tab_panels.keys() if k != active_tab]
        if remaining_tabs:
            area1_tab_panels_container.set_value(remaining_tabs[0])
        # Remove the tab
        area1_tabs.remove(tab_to_remove)
        # Remove the tab panel
        if active_tab in area1_tab_panels:
            area1_tab_panels[active_tab].parent_slot.parent.delete()
            del area1_tab_panels[active_tab]
        #ui.notify(f'Removed {active_tab} from Area 1')

def add_tab_area2():
    """Dynamically add a new tab to Area 2"""
    global area2_tab_counter, area2_tabs, area2_tab_panels, area2_tab_panels_container
    
    area2_tab_counter += 1
    new_tab_name = f'tab2_{area2_tab_counter}'
    # Add new tab
    with area2_tabs:
        ui.tab(new_tab_name, label=f'Tool {area2_tab_counter}')
    # Add new tab panel
    with area2_tab_panels_container:
        with ui.tab_panel(new_tab_name):
            area2_tab_panels[new_tab_name] = ui.scroll_area().classes('w-full h-full p-4')
            with area2_tab_panels[new_tab_name]:
                ...
    #ui.notify(f'Added Tab {area2_tab_counter} to Area 2')

def remove_tab_area2():
    """Remove the currently active tab from Area 2"""
    global area2_tab_panels, area2_tabs, area2_tab_panels_container
    
    active_tab = get_active_area2_tab()
    # Don't allow removing if it's the last tab
    if len(area2_tab_panels) <= 1:
        ui.notify('Cannot remove the last tab!', type='warning')
        return
    # Find and remove the tab
    tab_to_remove = None
    for child in area2_tabs:
        if hasattr(child, '_props') and child._props.get('name') == active_tab:
            tab_to_remove = child
            break
    if tab_to_remove:
        # Switch to a different tab before removing
        remaining_tabs = [k for k in area2_tab_panels.keys() if k != active_tab]
        if remaining_tabs:
            area2_tab_panels_container.set_value(remaining_tabs[0])
        # Remove the tab
        area2_tabs.remove(tab_to_remove)
        # Remove the tab panel
        if active_tab in area2_tab_panels:
            area2_tab_panels[active_tab].parent_slot.parent.delete()
            del area2_tab_panels[active_tab]
        #ui.notify(f'Removed {active_tab} from Area 2')

# Run the app
ui.run(port=9999)