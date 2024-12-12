import unittest
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class TDMTSiteNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Class setup method that runs once before all tests.
        Configures logging and initializes the WebDriver.
        """
        # Configure logging with absolute path
        import os

        log_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "tdat_tests.log"
        )

        # Clear the log file at the start
        open(log_file, "w").close()  # Clear the log file

        # Clear existing handlers to avoid duplication
        logging.getLogger().handlers = []

        # Configure logging with file and stream handlers
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(
                    log_file, mode="w"
                ),  # 'w' mode to clear file on each run
                logging.StreamHandler(),
            ],
        )
        cls.logger = logging.getLogger(__name__)
        cls.logger.info("Starting test suite execution")

        # Initialize the WebDriver
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.environment_url = "egis"
        cls.logger.info("Test suite setup complete")

    def setUp(self):
        """
        Instance setup method that runs before each test.
        Initializes WebDriverWait for explicit waits.
        """
        self.wait = WebDriverWait(self.driver, 10)

    # Helper Methods
    def visit_tdat_site(self):
        """
        Navigates to the TDAT website and waits for initial load.
        """
        self.driver.get(f"https://{self.environment_url}.hud.gov/TDMT/")
        time.sleep(1)

    def close_splash_screen(self):
        """
        Closes the initial splash screen modal that appears on site load.
        """
        close_button = self.driver.find_element(
            By.CSS_SELECTOR, "#splash-screen-modal .close"
        )
        close_button.click()
        time.sleep(1)

    def open_menu(self):
        """
        Opens the main navigation menu.
        """
        menu_button = self.driver.find_element(
            By.CSS_SELECTOR, "#tdat-collaspe-menu .dropdown-toggle"
        )
        menu_button.click()
        time.sleep(1)

    def switch_to_new_tab(self):
        """
        Switches WebDriver focus to newly opened tab.
        Returns: The window handle of the new tab.
        """
        new_window = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_window)
        return new_window

    def switch_back_to_main_tab(self):
        """
        Closes current tab and switches focus back to the main window.
        """
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def verify_url_and_log(self, expected_url, test_name):
        """
        Verifies current URL matches expected URL and logs result.
        Args:
            expected_url (str): The URL that should be loaded
            test_name (str): Name of the test for logging purposes
        Returns:
            bool: True if URLs match, False otherwise
        """
        current_url = self.driver.current_url
        if current_url == expected_url:
            self.logger.info(f"Test Passed: Successfully navigated to {test_name}")
        else:
            self.logger.error(
                f"Test Failed: Expected URL {expected_url} but got {current_url}"
            )
        return current_url == expected_url

    def select_dropdown_option(self, dropdown_id, option_text):
        """
        Selects an option from a dropdown menu.
        Args:
            dropdown_id (str): The ID of the dropdown element
            option_text (str): The text of the option to select
        """
        dropdown = self.driver.find_element(By.ID, dropdown_id)
        dropdown.click()
        time.sleep(1)
        option = self.driver.find_element(By.XPATH, f"//option[text()='{option_text}']")
        option.click()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        """
        Class cleanup method that runs once after all tests are complete.
        Closes the WebDriver and logs completion.
        """
        cls.logger.info("Test suite teardown starting")
        cls.driver.quit()
        cls.logger.info("Test suite completed")


if __name__ == "__main__":
    unittest.main()

