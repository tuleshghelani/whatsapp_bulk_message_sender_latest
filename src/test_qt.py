import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt

def test_qt():
    try:
        app = QApplication(sys.argv)
        window = QMainWindow()
        window.setWindowTitle("PyQt6 Test")
        window.setGeometry(100, 100, 300, 200)
        
        label = QLabel("PyQt6 is working!", window)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        window.setCentralWidget(label)
        
        window.show()
        print("PyQt6 initialized successfully!")
        return app.exec()
    except Exception as e:
        print(f"PyQt6 test failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(test_qt()) 