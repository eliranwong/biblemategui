from nicegui import ui

class Notepad:
    def __init__(self):
        self.text_content = ''
        
    def setup_ui(self):
        ui.label('Simple Notepad').classes('text-2xl font-bold mb-4')
        
        # Text area for editing
        self.textarea = ui.textarea(
            label='Your Notes',
            placeholder='Start typing your notes here...',
            value=self.text_content
        ).classes('w-full').props('rows=20 outlined')
        
        # Buttons row
        with ui.row().classes('gap-2 mt-4'):
            ui.button('Download', on_click=self.download_file, icon='download').props('color=primary')
            
            # File upload - files are saved to upload_dir first
            self.upload = ui.upload(
                on_upload=self.handle_upload,
                auto_upload=True
            ).props('accept=.txt')
            
            ui.button('Clear', on_click=self.clear_text, icon='delete').props('color=negative')
        
        ui.label('💡 Tip: Edit your text, download it, and upload later to continue!').classes('text-sm text-gray-600 mt-4')
    
    def download_file(self):
        """Download the current text as a .txt file"""
        content = self.textarea.value or ''
        if not content:
            ui.notify('Nothing to download! Write something first.', type='warning')
            return
        
        # Create a download with the current text content
        content_bytes = content.encode('utf-8')
        ui.download(content_bytes, 'notepad.txt')
        ui.notify('File downloaded successfully!', type='positive')
    
    async def handle_upload(self, e):
        """Handle file upload and load content into textarea"""
        try:
            # e.file is a SmallFileUpload object with async read() method
            content = await e.file.read()
            text = content.decode('utf-8')
            
            self.textarea.value = text
            ui.notify('File loaded successfully!', type='positive')
            self.upload.reset()
        except Exception as ex:
            ui.notify(f'Error loading file: {str(ex)}', type='negative')
            print(f"Full error: {ex}")
    
    def clear_text(self):
        """Clear all text from the notepad"""
        self.textarea.value = ''
        ui.notify('Notepad cleared!', type='info')

# Create and run the notepad app
notepad = Notepad()
notepad.setup_ui()

ui.run(title='Simple Notepad', port=9999)