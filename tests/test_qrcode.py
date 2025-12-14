import base64
import io
import qrcode
from nicegui import ui

# --- Helper Function: Generate QR Code as Base64 ---
def generate_qr_base64(data: str) -> str:
    """
    Generates a QR code for the given string and returns it 
    as a base64 encoded data URL for use in ui.image().
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save image to a memory buffer (avoiding file creation)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    # Return standard data URL format
    return f'data:image/png;base64,{img_str}'

@ui.page('/')
def index():
    ui.label('BibleMate AI - Share Page').classes('text-2xl font-bold mb-4')

    # --- The Dialog (Popup) ---
    # We define the dialog once, but leave the specific content container empty 
    # so we can refresh it dynamically when the button is clicked.
    with ui.dialog() as dialog, ui.card().classes('items-center text-center p-6'):
        ui.label('Page URL & QR Code').classes('text-xl font-bold')
        
        # Container to hold dynamic content (URL label + QR image)
        qr_container = ui.column().classes('items-center gap-4')
        
        ui.button('Close', on_click=dialog.close).props('flat')

    # --- Event Handler ---
    async def show_url_popup():
        # 1. Get the current URL from the user's browser
        # We must await this because it requires a round-trip to the client
        current_url = await ui.run_javascript('window.location.href')
        
        # 2. Update the dialog content
        qr_container.clear() # Clear previous content
        with qr_container:
            # Show URL (clickable link)
            ui.link(current_url, current_url).classes('text-blue-600 break-all max-w-[300px]')
            
            # Show QR Code
            # We generate it on the fly based on the fetched URL
            base64_img = generate_qr_base64(current_url)
            ui.image(base64_img).style('width: 250px; height: 250px')
            
        # 3. Open the dialog
        dialog.open()

    # --- Main Button ---
    ui.button('Share / Show QR', on_click=show_url_popup, icon='qr_code')

ui.run(port=9999)