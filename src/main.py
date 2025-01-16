import sys
import traceback

def main():
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.main_window import MainWindow
        from qt_material import apply_stylesheet
        
        app = QApplication(sys.argv)
        apply_stylesheet(app, theme='dark_purple.xml')
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
        
    except ImportError as e:
        print("Error importing required modules:")
        print(str(e))
        print("\nTraceback:")
        print(traceback.format_exc())
        print("\nPlease ensure you have:")
        print("1. Installed Visual C++ Redistributable")
        print("2. Created and activated a virtual environment")
        print("3. Installed all requirements correctly")
        sys.exit(1)
    except Exception as e:
        print("Unexpected error:")
        print(str(e))
        print("\nTraceback:")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main() 