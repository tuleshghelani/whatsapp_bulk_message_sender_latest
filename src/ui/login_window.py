from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QMessageBox, QPushButton
from PyQt6.QtCore import Qt, QTimer
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
    def __init__(self, whatsapp_controller):
        super().__init__()
        self.whatsapp = whatsapp_controller
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
            self.status_label.setText("Checking WhatsApp connection...")
            self.progress.setRange(0, 0)
            
            def callback(success: bool):
                if success:
                    self.status_label.setText("WhatsApp Web connected!")
                    self.progress.setRange(0, 100)
                    self.progress.setValue(100)
                    QTimer.singleShot(1500, self.close)
                else:
                    self.status_label.setText("Connection failed. Please check your internet and try again.")
                    self.progress.setRange(0, 1)
                    self.progress.setValue(0)
                    # Add retry button
                    retry_btn = QPushButton("Retry Connection")
                    retry_btn.clicked.connect(self.initialize_whatsapp)
                    self.layout().addWidget(retry_btn)
            
            self.whatsapp.initialize(callback=callback)
            
        except Exception as e:
            logger.error(f"Login window error: {str(e)}")
            QMessageBox.critical(
                self,
                "Connection Error",
                f"Failed to connect to WhatsApp Web:\n{str(e)}\n\nPlease check your internet connection."
            ) 