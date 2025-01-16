from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PyQt6.QtCore import QObject, QTimer
import threading
from typing import Callable
import logging

logger = logging.getLogger(__name__)

class WhatsAppController(QObject):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.is_logged_in = False
        self.login_window = None

    def initialize(self):
        def _initialize():
            try:
                logger.info("Starting WhatsApp initialization...")
                
                options = webdriver.ChromeOptions()
                options.add_argument('--start-maximized')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                
                try:
                    logger.info("Initializing Chrome driver...")
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=options)
                    
                    logger.info("Navigating to WhatsApp Web...")
                    self.driver.get('https://web.whatsapp.com')
                    
                    wait = WebDriverWait(self.driver, 30)
                    
                    try:
                        element = wait.until(EC.presence_of_element_located((
                            By.CSS_SELECTOR, 
                            'div#side, div[data-testid="chat-list"]'
                        )))
                        logger.info("WhatsApp Web loaded successfully")
                        self.is_logged_in = True
                        QTimer.singleShot(0, self.login_window.handle_success)
                    except TimeoutException:
                        logger.error("Failed to detect WhatsApp Web state")
                        QTimer.singleShot(0, self.login_window.handle_failure)
                        self._cleanup_driver()
                        
                except Exception as e:
                    logger.error(f"Chrome driver error: {str(e)}")
                    QTimer.singleShot(0, self.login_window.handle_failure)
                    self._cleanup_driver()
                    
            except Exception as e:
                logger.error(f"Initialization error: {str(e)}")
                QTimer.singleShot(0, self.login_window.handle_failure)
                self._cleanup_driver()

        thread = threading.Thread(target=_initialize)
        thread.daemon = True
        thread.start()
    
    def _cleanup_driver(self):
        """Helper method to safely cleanup the driver"""
        try:
            if self.driver:
                logger.info("Cleaning up Chrome driver...")
                self.driver.quit()
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")
        finally:
            self.driver = None
            self.is_logged_in = False
    
    def is_ready(self) -> bool:
        try:
            return self.driver is not None and self.is_logged_in
        except Exception as e:
            logger.error(f"Error checking ready state: {str(e)}")
            return False