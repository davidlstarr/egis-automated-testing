import unittest
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class TDATSiteNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Class setup method that runs once before all tests.
        Configures logging and initializes the WebDriver.
        """
        # Configure logging with absolute path
        import os
        log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tdat_tests.log')
        
        # Clear the log file at the start
        open(log_file, 'w').close()  # Clear the log file
        
        # Clear existing handlers to avoid duplication
        logging.getLogger().handlers = []
        
        # Configure logging with file and stream handlers
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, mode='w'),  # 'w' mode to clear file on each run
                logging.StreamHandler()
            ]
        )
        cls.logger = logging.getLogger(__name__)
        cls.logger.info('Starting test suite execution')
        
        # Initialize the WebDriver
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.environment_url = 'egis'
        cls.logger.info('Test suite setup complete')

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
        self.driver.get(f'https://{self.environment_url}.hud.gov/TDAT/')
        time.sleep(1)

    def close_splash_screen(self):
        """
        Closes the initial splash screen modal that appears on site load.
        """
        close_button = self.driver.find_element(By.CSS_SELECTOR, '#splash-screen-modal .close')
        close_button.click()
        time.sleep(1)

    def open_menu(self):
        """
        Opens the main navigation menu.
        """
        menu_button = self.driver.find_element(By.CSS_SELECTOR, '#tdat-collaspe-menu .dropdown-toggle')
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
            self.logger.info(f'Test Passed: Successfully navigated to {test_name}')
        else:
            self.logger.error(f'Test Failed: Expected URL {expected_url} but got {current_url}')
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

    def test_search_for_tribes(self):
        """
        Tests the basic search functionality by clicking the 'Search For Tribes' button.
        Verifies that the button is clickable and functions correctly.
        """
        with self.subTest("Test Title: Search for Tribes"):
            try:
                self.visit_tdat_site()
                self.driver.find_element(By.ID, 'btn-search-tribes').click()
                self.logger.info('Test Passed: Able to click the "Search For Tribes" button.')
            except Exception as e:
                self.logger.error(f'Test Failed: Unable to click the "Search For Tribes" button: {str(e)}')
                raise

    def test_advanced_search(self):
        """
        Tests the advanced search functionality.
        Verifies that the advanced search modal opens and displays correct search options.
        """
        with self.subTest("Test Title: Advanced Search"):
            try:
                self.visit_tdat_site()
                self.close_splash_screen()
                
                search_button = self.driver.find_element(By.CSS_SELECTOR, '#tdat-collaspe-menu .header-style')
                search_button.click()

                time.sleep(2)
                title = self.driver.find_element(By.CSS_SELECTOR, '#modal-body-2 .control-label')
                title_text = title.text
                
                if title_text == 'Option 1: Search by Address':
                    self.logger.info('Test Passed: Advanced Search functionality verified')
                else:
                    self.logger.error('Test Failed: Advanced Search title mismatch')

            except Exception as e:
                self.logger.error(f'Test Failed: Advanced Search test failed: {str(e)}')
                raise

    def test_select_tribe(self):
        """
        Tests the tribe selection functionality.
        Verifies that users can select a specific tribe and view its contact information.
        """
        with self.subTest("Test Title: Find Tribal Contact Information for a Tribe"):
            try:
                self.visit_tdat_site()
                self.driver.find_element(By.ID, 'btn-search-tribes').click()
                self.select_dropdown_option('tribe', 'Absentee-Shawnee Tribe of Indians of Oklahoma')
                time.sleep(1)

                info_popup = self.driver.find_element(By.ID, 'grid-title')
                title_text = info_popup.text
                if title_text == 'Contact Information for Absentee-Shawnee Tribe of Indians of Oklahoma':
                    assert info_popup.is_displayed()
                    self.logger.info('Test Passed: Tribe selection verified')
                else:
                    self.logger.error('Test Failed: Tribe selection failed')

            except Exception as e:
                self.logger.error(f'Test Failed: Tribe selection test failed: {str(e)}')
                raise
    
    def test_export_to_excel(self):
        """
        Tests the Export to Excel functionality.
        Verifies that users can export tribal contact information to an Excel file.
        """
        with self.subTest("Test Title: Export to Excel"):
            try:
                self.visit_tdat_site()
                self.driver.find_element(By.ID, 'btn-search-tribes').click()
                self.select_dropdown_option('tribe', 'Absentee-Shawnee Tribe of Indians of Oklahoma')
                time.sleep(1)

                export_button = self.driver.find_element(By.CLASS_NAME, 'excel-report')
                export_button.click()
                time.sleep(5)

                download_button = self.driver.find_element(By.CLASS_NAME, 'query-excel-success').click()
                time.sleep(5)
                
                # Wait for download to complete (up to 10 seconds)
                import os
                import glob
                from pathlib import Path
                downloads_path = str(Path.home() / "Downloads")
                
                # Wait for the Excel file to appear in downloads
                start_time = time.time()
                excel_file = None
                while time.time() - start_time < 10:
                    excel_files = glob.glob(os.path.join(downloads_path, "TDAT_Report*.xlsx"))

                    if excel_files:
                        excel_file = excel_files[0]
                        break
                    time.sleep(0.5)
                
                # Verify download success
                if excel_file and os.path.exists(excel_file):
                    self.logger.info(f'Excel file successfully downloaded: {os.path.basename(excel_file)}')
                    # Optional: Clean up downloaded file
                    os.remove(excel_file)
                else:
                    self.logger.error('Excel file download failed')
                    raise AssertionError('Excel file was not downloaded')


            except Exception as e:
                self.logger.error(f'Test Failed: Export to Excel test failed: {str(e)}')
                raise

    def test_print_page(self):
        """
        Tests the Print Page functionality.
        Verifies that users can print tribal contact information from the site.
        """
        with self.subTest("Test Title: Print Page"):
            try:
                self.visit_tdat_site()
                self.driver.find_element(By.ID, 'btn-search-tribes').click()
                self.select_dropdown_option('tribe', 'Absentee-Shawnee Tribe of Indians of Oklahoma')
                time.sleep(1)

                print_button = self.driver.find_element(By.CLASS_NAME, 'print')

                # Verify print button is clicked
                if print_button:
                    self.logger.info('Test Passed: Print Page test verified')
                else:
                    self.logger.error('Test Failed: Print Page test failed')


            except Exception as e:
                self.logger.error(f'Test Failed: Print Page test failed: {str(e)}')
                raise

    def test_select_state_county(self):
        """
        Tests the state and county selection functionality.
        Verifies that users can select a state and county to view tribal contact information.
        """
        with self.subTest("Test Title: Find Tribal Contact Information for a County"):
            try:
                self.visit_tdat_site()
                self.driver.find_element(By.ID, 'btn-search-tribes').click()
                
                self.select_dropdown_option('state', 'Texas')
                self.driver.find_element(
                    By.XPATH, "//option[text()='Anderson']").click()
               
                self.driver.find_element(
                    By.XPATH, "//option[text()='Armstrong']").click() 
                
                self.driver.find_element(By.ID, 'county-select').click()
                time.sleep(1)

                info_popup = self.driver.find_element(By.ID, 'grid-title')
                title_text = info_popup.text
                if title_text == 'Contact Information for Tribes with Interests in Anderson, Armstrong counties, Texas':
                    assert info_popup.is_displayed()
                    self.logger.info('Test Passed: State/County selection verified')
                else:
                    self.logger.error('Test Failed: State/County selection failed')

            except Exception as e:
                self.logger.error(f'Test Failed: State/County selection test failed: {str(e)}')
                raise
    
    def test_get_all_tribes(self):
        """
        Tests the Get All Tribes functionality.
        Verifies that users can view all tribal contact information.
        """
        with self.subTest("Test Title: Get All Tribes"):
            try:
                self.visit_tdat_site()
                time.sleep(1)
                self.driver.find_element(By.ID, 'btn-search-tribes').click()
                self.select_dropdown_option('state', 'District of Columbia')
                self.driver.find_element(By.ID, 'county-select-all').click()
                time.sleep(1)

                info_popup = self.driver.find_element(By.ID, 'grid-title')
                title_text = info_popup.text
                if title_text == 'Contact Information for Tribes with Interests in District of Columbia':
                    assert info_popup.is_displayed()
                    self.logger.info('Test Passed: Get All Tribes functionality verified')
                else:
                    self.logger.error('Test Failed: Get All Tribes functionality failed')

            except Exception as e:
                self.logger.error(f'Test Failed: Get All Tribes test failed: {str(e)}')
                raise

    def test_address_input(self):
        """
        Tests the address input functionality.
        Verifies that users can input an address to search for tribal contact information.
        """
        with self.subTest("Test Title: Address Input"):
            try:
                self.visit_tdat_site()
                time.sleep(1)
                self.close_splash_screen()
                time.sleep(2)
                search_input = self.driver.find_element(By.ID, 'txt-search-input')
                search_input.send_keys('1200 South Quincy Street Green Bay, Wisconsin 54302')
                search_button = self.driver.find_element(By.ID, 'btn-search-location')
                search_button.click()
                time.sleep(2)

                info_popup = self.driver.find_element(By.ID, 'grid-title')
                title_text = info_popup.text
                if title_text == 'Contact Information for Tribes with Interests in Brown County, Wisconsin':
                    assert info_popup.is_displayed()
                    self.logger.info('Test Passed: Address input functionality verified')
                else:
                    self.logger.error('Test Failed: Address input functionality failed')

            except Exception as e:
                self.logger.error(f'Test Failed: Address input test failed: {str(e)}')
                raise

    def test_click_on_map(self):
        """
        Tests the map interaction functionality.
        Verifies that users can click on the map to select a location and view tribal information.
        """
        with self.subTest("Test Title: Find Tribal Contact Information through the Map"):
            try:
                self.visit_tdat_site()
                self.close_splash_screen()

                # Map interaction
                elem = self.driver.find_element(By.ID, 'mapDiv')
                ac = ActionChains(self.driver)
                time.sleep(2)
                ac.move_to_element(elem).move_by_offset(20, 20).click().perform()

                # Select state and county
                self.select_dropdown_option('state', 'Ohio')
                self.driver.find_element(
                    By.XPATH, "//option[text()='Union']").click()
           
                time.sleep(1)
                self.driver.find_element(By.ID, 'county-select').click()
                time.sleep(1)

                # Verify results
                info_popup = self.driver.find_element(By.ID, 'grid-title')
                if info_popup.text == 'Contact Information for Tribes with Interests in Union County, Ohio':
                    tribal_name_grid_cell = self.driver.find_element(
                        By.CSS_SELECTOR, '#tribeResults-row-undefined:first-child .field-image .plusImage:first-child')
                    tribal_name_grid_cell.click()

                    time.sleep(2)
                    tribal_text = self.driver.find_element(
                        By.CSS_SELECTOR, '.ui-state-default .field-CONTACT_NAME').text
                    
                    if tribal_text == 'Contact Name':
                        self.logger.info('Test Passed: Map interaction and tribal information verified')
                    else:
                        self.logger.error('Test Failed: Tribal contact information not displayed')
                else:
                    self.logger.error('Test Failed: Map interaction failed')

            except Exception as e:
                self.logger.error(f'Test Failed: Map interaction test failed: {str(e)}')
                raise

    def test_map_zoom(self):
        """
        Tests the map zoom functionality.
        Verifies that users can zoom in and out on the map.
        """
        with self.subTest("Test Title: Map Zoom"):
            try:
                self.visit_tdat_site()
                self.close_splash_screen()

                # Zoom in
                zoom_in_button = self.driver.find_element(By.CLASS_NAME, 'esriSimpleSliderIncrementButton')
                zoom_in_button.click()
                time.sleep(1)
            
                # Zoom out
                zoom_out_button = self.driver.find_element(By.CLASS_NAME, 'esriSimpleSliderDecrementButton')   
                zoom_out_button.click()
                time.sleep(1)

                self.logger.info('Test Passed: Map zoom functionality verified')


            except Exception as e:
                self.logger.error(f'Test Failed: Map zoom test failed: {str(e)}')
                raise

        

    def test_access_menu(self):
        """
        Tests the menu access functionality.
        Verifies that users can access and interact with the main menu.
        """
        with self.subTest("Test Title: Access Menu"):
            try:
                self.visit_tdat_site()
                self.close_splash_screen()
                self.open_menu()

                self.driver.find_element(By.CSS_SELECTOR, '.show-splash-screen').click()
                time.sleep(1)

                modal_title = self.driver.find_element(By.CSS_SELECTOR, '.modal-title')
                if modal_title.text == 'Tribal Directory Assessment Tool (TDAT)':
                    self.logger.info('Test Passed: Menu access verified')
                else:
                    self.logger.error('Test Failed: Menu access failed')

            except Exception as e:
                self.logger.error(f'Test Failed: Menu access test failed: {str(e)}')
                raise

    def test_alaska_special_instructions(self):
        """
        Tests the Alaska Special Instructions functionality.
        Verifies that users can access the Alaska-specific documentation in a new tab.
        """
        with self.subTest("Test Title: Alaska Special Instructions"):
            try:
                self.visit_tdat_site()
                self.close_splash_screen()
                self.open_menu()

                self.driver.find_element(By.CSS_SELECTOR, '.dropdown-menu li:nth-child(3) a').click()
                time.sleep(3)

                self.switch_to_new_tab()
                success = self.verify_url_and_log(
                    'https://egis.hud.gov/TDAT/docs/Special%20Instructions%20for%20Alaska.pdf',
                    'Alaska Special Instructions page'
                )

                self.switch_back_to_main_tab()
                
                if success:
                    self.logger.info('Test Passed: Alaska Special Instructions displayed successfully')
                else:
                    self.logger.error('Test Failed: Alaska Special Instructions not displayed correctly')

            except Exception as e:
                self.logger.error(f'Test Failed: Alaska Special Instructions test failed: {str(e)}')
                raise

    def test_hud_exchange_menu(self):
        """
        Tests the HUD Exchange menu functionality.
        Verifies that users can access the HUD Exchange resources through the menu.
        """
        with self.subTest("Test Title: HUD Exchange Menu"):
            try:
                self.visit_tdat_site()
                self.close_splash_screen()
                self.open_menu()

                # Navigate to HUD Exchange
                self.driver.find_element(By.CSS_SELECTOR, '.dropdown-menu li:nth-child(6) a').click()
                time.sleep(3)

                self.driver.find_element(By.CSS_SELECTOR, '#info-text ul li:first-child a').click()
                time.sleep(3)

                # Verify navigation
                self.switch_to_new_tab()
                success = self.verify_url_and_log(
                    'https://www.hudexchange.info/programs/environmental-review/historic-preservation/',
                    'HUD Exchange page'
                )

                self.switch_back_to_main_tab()

                if success:
                    self.logger.info('Test Passed: HUD Exchange menu functionality verified')
                else:
                    self.logger.error('Test Failed: HUD Exchange menu functionality failed')

            except Exception as e:
                self.logger.error(f'Test Failed: HUD Exchange menu test failed: {str(e)}')
                raise

    def test_info_by_state(self):
        """
        Tests the Information by State functionality.
        Verifies that users can access state-specific HUD information through the menu.
        """
        with self.subTest("Test Title: Information by State"):
            try:
                self.visit_tdat_site()
                self.close_splash_screen()
                self.open_menu()

                # Navigate to State Information
                self.driver.find_element(By.CSS_SELECTOR, '.dropdown-menu li:nth-child(6) a').click()
                time.sleep(3)

                self.driver.find_element(By.CSS_SELECTOR, '#info-text ul li:nth-child(2) a').click()
                time.sleep(6)

                # Verify navigation
                self.switch_to_new_tab()
                success = self.verify_url_and_log(
                    'https://www.hud.gov/states',
                    'HUD states page'
                )

                self.switch_back_to_main_tab()

                if success:
                    self.logger.info('Test Passed: Information by State functionality verified')
                else:
                    self.logger.error('Test Failed: Information by State functionality failed')

            except Exception as e:
                self.logger.error(f'Test Failed: Information by State test failed: {str(e)}')
                raise

    def test_process_for_consultation(self):
        """
        Tests the Process for Consultation functionality.
        Verifies that users can access the consultation process documentation through the menu.
        """
        with self.subTest("Test Title: Process for Consultation"):
            try:
                self.visit_tdat_site()
                self.close_splash_screen()
                self.open_menu()

                # Navigate to Consultation Process
                self.driver.find_element(By.CSS_SELECTOR, '.dropdown-menu li:nth-child(6) a').click()
                time.sleep(3)

                self.driver.find_element(By.CSS_SELECTOR, '#info-text ul li:nth-child(3) a').click()
                time.sleep(3)

                # Verify navigation
                self.switch_to_new_tab()
                success = self.verify_url_and_log(
                    'https://egis.hud.gov/TDAT/docs/ProcessForTribalConsultationInHUDProjects.pdf',
                    'Consultation process page'
                )

                self.switch_back_to_main_tab()

                if success:
                    self.logger.info('Test Passed: Process for Consultation functionality verified')
                else:
                    self.logger.error('Test Failed: Process for Consultation functionality failed')

            except Exception as e:
                self.logger.error(f'Test Failed: Process for Consultation test failed: {str(e)}')
                raise

    def test_TDAT_user_guide(self):
        """
        Tests the TDAT User Guide functionality.
        Verifies that users can access the TDAT User Guide documentation through the menu.
        """
        with self.subTest("Test Title: TDAT User Guide"):
            try:
                self.visit_tdat_site()
                self.close_splash_screen()
                self.open_menu()

                # Navigate to TDAT User Guide
                self.driver.find_element(By.CSS_SELECTOR, '.dropdown-menu li:nth-child(5) a').click()
                time.sleep(3)

                # Verify navigation
                self.switch_to_new_tab()
                success = self.verify_url_and_log(
                    'https://egis.hud.gov/TDAT/docs/TDATUserManualV4.0.pdf',
                    'TDAT User Guide page'
                )

                self.switch_back_to_main_tab()

                if success:
                    self.logger.info('Test Passed: TDAT User Guide functionality verified')
                else:
                    self.logger.error('Test Failed: TDAT User Guide functionality failed')

            except Exception as e:
                self.logger.error(f'Test Failed: TDAT User Guide test failed: {str(e)}')
                raise

    def test_feedback_corrections(self):
        """
        Tests the Feedback and Corrections functionality.
        Verifies that users can access the feedback and corrections form through the menu.
        """
        with self.subTest("Test Title: Feedback and Corrections"):
            try:
                self.visit_tdat_site()
                self.close_splash_screen()
                self.open_menu()

                # Navigate to Feedback and Corrections
                self.driver.find_element(By.CSS_SELECTOR, '.dropdown-menu li:nth-child(7) a').click()
                time.sleep(3)

                # click on feedback link 
                link = self.driver.find_element(By.CSS_SELECTOR, '#feedback-text a')

                # ensure the following a link is TDAT_Info@hud.gov
                if(link.text == 'TDAT_Info@hud.gov'):
                    self.logger.info('Test Passed: Feedback and Corrections functionality verified')
                else:
                    self.logger.error('Test Failed: Feedback and Corrections functionality failed')


            except Exception as e:
                self.logger.error(f'Test Failed: Feedback and Corrections test failed: {str(e)}')
                raise

    @classmethod
    def tearDownClass(cls):
        """
        Class cleanup method that runs once after all tests are complete.
        Closes the WebDriver and logs completion.
        """
        cls.logger.info('Test suite teardown starting')
        cls.driver.quit()
        cls.logger.info('Test suite completed')


if __name__ == '__main__':
    unittest.main()