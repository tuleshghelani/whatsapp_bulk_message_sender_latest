from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, 
                           QLabel, QHBoxLayout, QPushButton,
                           QSpinBox)
from PyQt6.QtCore import Qt

class MessageEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Message input
        msg_label = QLabel("Message:")
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Enter your message here...")
        
        # Buttons section
        buttons_layout = QHBoxLayout()
        
        # Add Poll button
        self.add_poll_btn = QPushButton("ADD POLL")
        self.add_poll_btn.clicked.connect(self.add_poll)
        
        # Add Button button
        self.add_button_btn = QPushButton("ADD BUTTON")
        self.add_button_btn.clicked.connect(self.add_button)
        
        buttons_layout.addWidget(self.add_poll_btn)
        buttons_layout.addWidget(self.add_button_btn)
        
        # Add widgets to main layout
        layout.addWidget(msg_label)
        layout.addWidget(self.message_input)
        layout.addLayout(buttons_layout)
        
        # Delay settings
        delay_label = QLabel("Delay Settings:")
        layout.addWidget(delay_label)
        
        # After messages delay
        after_delay = QHBoxLayout()
        after_delay.addWidget(QLabel("Wait"))
        self.after_min = QSpinBox()
        self.after_min.setValue(10)
        after_delay.addWidget(self.after_min)
        after_delay.addWidget(QLabel("to"))
        self.after_max = QSpinBox()
        self.after_max.setValue(20)
        after_delay.addWidget(self.after_max)
        after_delay.addWidget(QLabel("seconds after every"))
        self.after_msgs = QSpinBox()
        self.after_msgs.setValue(10)
        after_delay.addWidget(self.after_msgs)
        after_delay.addWidget(QLabel("Messages"))
        layout.addLayout(after_delay)
        
        # Before message delay
        before_delay = QHBoxLayout()
        before_delay.addWidget(QLabel("Wait"))
        self.before_min = QSpinBox()
        self.before_min.setValue(4)
        before_delay.addWidget(self.before_min)
        before_delay.addWidget(QLabel("to"))
        self.before_max = QSpinBox()
        self.before_max.setValue(8)
        before_delay.addWidget(self.before_max)
        before_delay.addWidget(QLabel("seconds before every message"))
        layout.addLayout(before_delay)
        
    def add_poll(self):
        # TODO: Implement poll functionality
        pass
        
    def add_button(self):
        # TODO: Implement button functionality
        pass
        
    def get_message(self) -> str:
        return self.message_input.toPlainText()
        
    def get_delay_settings(self) -> dict:
        return {
            'after_min': self.after_min.value(),
            'after_max': self.after_max.value(),
            'after_msgs': self.after_msgs.value(),
            'before_min': self.before_min.value(),
            'before_max': self.before_max.value()
        }