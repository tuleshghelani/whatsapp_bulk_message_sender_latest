from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QMessageBox, QPushButton
from PyQt6.QtCore import Qt, QTimer, QMetaObject, pyqtSlot
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whatsapp_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WhatsAppLoginWindow(QWidget):
    def __init__(self, whatsapp_controller, parent=None):
        super().__init__(parent)
        self.whatsapp = whatsapp_controller
        self.whatsapp.login_window = self  # Set reference to this window
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("WhatsApp Login")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "WhatsApp Web is opening in your browser.\n"
            "Please scan the QR code with your phone:\n\n"
            "1. Open WhatsApp on your phone\n"
            "2. Tap Menu or Settings\n"
            "3. Select WhatsApp Web\n"
            "4. Point your phone to the QR code\n\n"
            "This window will close automatically after successful login."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)
        
        # Status label
        self.status_label = QLabel("Opening WhatsApp Web...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        
        # Initialize WhatsApp
        QTimer.singleShot(100, self.initialize_whatsapp)
        
    def initialize_whatsapp(self):
        try:
            self.clear_buttons()  # Clear any existing buttons
            self.status_label.setText("Connecting to WhatsApp...")
            self.progress.setRange(0, 0)
            self.whatsapp.initialize()
            
        except Exception as e:
            logger.error(f"Login window error: {str(e)}")
            QMessageBox.critical(
                self,
                "Connection Error",
                f"Failed to connect to WhatsApp Web:\n{str(e)}"
            )
    
    @pyqtSlot()
    def handle_success(self):
        self.status_label.setText("WhatsApp Web connected successfully!")
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        self.add_close_button()
    
    @pyqtSlot()
    def handle_failure(self):
        self.status_label.setText("Connection failed. Please try again.")
        self.progress.setRange(0, 1)
        self.progress.setValue(0)
        self.add_retry_button()
    
    def add_close_button(self):
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.hide)  # Hide instead of close
        self.layout().addWidget(close_btn)
    
    def add_retry_button(self):
        retry_btn = QPushButton("Retry Connection")
        retry_btn.clicked.connect(self.initialize_whatsapp)
        self.layout().addWidget(retry_btn)
    
    def closeEvent(self, event):
        # Clean up when window is closed
        if not self.whatsapp.is_logged_in:
            self.whatsapp._cleanup_driver()
        super().closeEvent(event) 
    
    def clear_buttons(self):
        """Remove any existing buttons from previous attempts"""
        layout = self.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                layout.removeWidget(widget)
                widget.deleteLater() 