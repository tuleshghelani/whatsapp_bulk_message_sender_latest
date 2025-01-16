from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QTableWidget, QTabWidget, QSpinBox,
                           QMessageBox, QFileDialog, QTableWidgetItem)
from PyQt6.QtCore import Qt
from controllers.whatsapp_controller import WhatsAppController
from .message_editor import MessageEditor
from .login_window import WhatsAppLoginWindow
from controllers.excel_controller import ExcelController
import time
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wasender 3.5.0")
        self.setMinimumSize(1200, 800)
        
        # Initialize controllers
        self.whatsapp = WhatsAppController()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Add WhatsApp login button
        login_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login to WhatsApp")
        self.login_btn.clicked.connect(self.show_login)
        login_layout.addWidget(self.login_btn)
        login_layout.addStretch()
        layout.addLayout(login_layout)
        
        # Create tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_campaign_tab(), "Campaign")
        tabs.addTab(self.create_contacts_tab(), "Contacts")
        
        layout.addWidget(tabs)
    
    def create_campaign_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add message editor
        self.message_editor = MessageEditor()
        layout.addWidget(self.message_editor)
        
        # Add buttons
        buttons_layout = QHBoxLayout()
        start_btn = QPushButton("Start Campaign")
        start_btn.clicked.connect(self.start_campaign)
        buttons_layout.addWidget(start_btn)
        
        layout.addLayout(buttons_layout)
        return widget
    
    def create_contacts_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add import button
        import_btn = QPushButton("Import Excel File")
        import_btn.clicked.connect(self.import_contacts)
        layout.addWidget(import_btn)
        
        # Add contact list table
        self.contacts_table = QTableWidget()
        self.contacts_table.setColumnCount(2)
        self.contacts_table.setHorizontalHeaderLabels(['Name', 'Phone'])
        layout.addWidget(self.contacts_table)
        
        return widget
    
    def show_login(self):
        try:
            self.login_window = WhatsAppLoginWindow(self.whatsapp)
            self.login_window.show()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error opening WhatsApp login: {str(e)}\n\n"
                "Please ensure you have installed all requirements correctly."
            )
    
    def start_campaign(self):
        if not self.whatsapp.is_ready():
            QMessageBox.warning(
                self,
                "Login Required",
                "Please login to WhatsApp before starting the campaign."
            )
            return
            
        try:
            message = self.message_editor.get_message()
            if not message:
                QMessageBox.warning(self, "Error", "Please enter a message")
                return
            
            contacts = []
            for row in range(self.contacts_table.rowCount()):
                name = self.contacts_table.item(row, 0).text()
                phone = self.contacts_table.item(row, 1).text()
                contacts.append({'name': name, 'phone': phone})
            
            if not contacts:
                QMessageBox.warning(self, "Error", "Please import contacts first")
                return
            
            self.send_messages(contacts, message)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error starting campaign: {str(e)}")

    def send_messages(self, contacts, message):
        delay_settings = self.message_editor.get_delay_settings()
        msg_count = 0
        
        for contact in contacts:
            try:
                success = self.whatsapp.send_message(contact['phone'], message)
                
                if success:
                    print(f"Message sent to {contact['name']} ({contact['phone']})")
                    msg_count += 1
                    
                    if msg_count % delay_settings['after_msgs'] == 0:
                        delay = random.randint(
                            delay_settings['after_min'],
                            delay_settings['after_max']
                        )
                        time.sleep(delay)
                    else:
                        delay = random.randint(
                            delay_settings['before_min'],
                            delay_settings['before_max']
                        )
                        time.sleep(delay)
                        
            except Exception as e:
                print(f"Error sending to {contact['name']}: {str(e)}")
                continue
        
        QMessageBox.information(
            self,
            "Campaign Complete",
            f"Campaign finished. Sent {msg_count} out of {len(contacts)} messages."
        )
    
    def import_contacts(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Import Contacts", "", "Excel Files (*.xlsx *.xls)"
            )
            
            if file_path:
                contacts = ExcelController.read_contacts(file_path)
                self.contacts_table.setRowCount(len(contacts))
                
                for row, contact in enumerate(contacts):
                    self.contacts_table.setItem(row, 0, QTableWidgetItem(contact['name']))
                    self.contacts_table.setItem(row, 1, QTableWidgetItem(contact['phone']))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error importing contacts: {str(e)}") 