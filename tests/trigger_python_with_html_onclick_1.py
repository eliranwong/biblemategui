from nicegui import ui

def handle_click(item_name: str):
    """Function triggered when a link is clicked"""
    ui.notify(f'You clicked on: {item_name}', type='positive')
    # You can add any Python logic here
    print(f'Processing: {item_name}')

def create_html_with_links():
    # Create HTML content with clickable links
    html_content = '''
    <div style="padding: 20px; background-color: #f0f0f0; border-radius: 8px;">
        <h2>Product List</h2>
        <p>Click on any product to see details:</p>
        <ul>
            <li><a href="#" onclick="return false;" id="product1">Product A</a></li>
            <li><a href="#" onclick="return false;" id="product2">Product B</a></li>
            <li><a href="#" onclick="return false;" id="product3">Product C</a></li>
        </ul>
    </div>
    '''
    
    html_element = ui.html(html_content, sanitize=False)
    
    # Attach click handlers to the links
    html_element.on('click', lambda e: handle_click('Product A'), ['#product1'])
    html_element.on('click', lambda e: handle_click('Product B'), ['#product2'])
    html_element.on('click', lambda e: handle_click('Product C'), ['#product3'])

# Run the app
with ui.card():
    create_html_with_links()
    
    # Add a label to show dynamic updates
    status = ui.label('Click a product above')
    
    def update_status(name: str):
        status.text = f'Last clicked: {name}'
        ui.notify(f'Selected: {name}')
    
    # Alternative approach with more detail
    ui.html('''
        <div style="margin-top: 20px; padding: 15px; border: 2px solid #333;">
            <h3>Navigation Menu</h3>
            <a href="#" id="home-link" style="margin-right: 15px;">Home</a>
            <a href="#" id="about-link" style="margin-right: 15px;">About</a>
            <a href="#" id="contact-link">Contact</a>
        </div>
    ''', sanitize=False).on('click', lambda e: update_status('Home'), ['#home-link']) \
        .on('click', lambda e: update_status('About'), ['#about-link']) \
        .on('click', lambda e: update_status('Contact'), ['#contact-link'])

ui.run(port=9999)