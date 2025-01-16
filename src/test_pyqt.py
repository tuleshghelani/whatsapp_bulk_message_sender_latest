import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

def test_pyqt():
    try:
        app = QApplication(sys.argv)
        window = QWidget()
        label = QLabel("PyQt6 is working!", window)
        window.show()
        print("PyQt6 initialized successfully!")
        app.quit()
        return True
    except Exception as e:
        print(f"PyQt6 test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_pyqt() 