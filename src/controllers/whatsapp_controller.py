from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
from typing import Callable
import os
import sys
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

class WhatsAppController:
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
        
    def initialize(self, callback: Callable[[bool], None] = None):
        def _initialize():
            try:
                logger.info("Starting WhatsApp initialization...")
                
                # Setup Chrome options
                options = webdriver.ChromeOptions()
                options.add_argument('--start-maximized')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                options.add_experimental_option('detach', True)
                
                try:
                    logger.info("Initializing Chrome driver...")
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=options)
                    logger.info("Chrome driver initialized successfully")
                    
                    logger.info("Navigating to WhatsApp Web...")
                    self.driver.get('https://web.whatsapp.com')
                    
                    # Increased wait time to 60 seconds
                    wait = WebDriverWait(self.driver, 60)
                    
                    try:
                        # First check for side panel which indicates logged in state
                        logger.info("Checking for existing login...")
                        side_panel = wait.until(EC.presence_of_element_located((
                            By.CSS_SELECTOR, 
                            'div#side, div[data-testid="chat-list"]'
                        )))
                        
                        logger.info("Already logged in")
                        self.is_logged_in = True
                        if callback:
                            callback(True)
                            
                    except TimeoutException:
                        # If not logged in, look for QR code
                        logger.info("Not logged in, checking for QR code...")
                        try:
                            qr_code = wait.until(EC.presence_of_element_located((
                                By.CSS_SELECTOR,
                                'div[data-testid="qrcode"], canvas'
                            )))
                            logger.info("QR code found, waiting for scan...")
                            
                            # Wait for successful login after QR scan
                            side_panel = wait.until(EC.presence_of_element_located((
                                By.CSS_SELECTOR,
                                'div#side, div[data-testid="chat-list"]'
                            )))
                            
                            logger.info("Login successful")
                            self.is_logged_in = True
                            if callback:
                                callback(True)
                                
                        except TimeoutException:
                            logger.error("Failed to detect either QR code or login state")
                            if callback:
                                callback(False)
                            self._cleanup_driver()
                            
                except Exception as e:
                    logger.error(f"Error during WhatsApp initialization: {str(e)}")
                    if callback:
                        callback(False)
                    self._cleanup_driver()
                
            except Exception as e:
                logger.error(f"Critical error: {str(e)}")
                if callback:
                    callback(False)
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
            logger.error(f"Error during driver cleanup: {str(e)}")
        finally:
            self.driver = None
            self.is_logged_in = False
    
    def is_ready(self) -> bool:
        try:
            return self.driver is not None and self.is_logged_in
        except Exception as e:
            logger.error(f"Error checking ready state: {str(e)}")
            return False