from extended_selenium import ExtendedSelenium
from locators import Locators
from RPA.HTTP import HTTP
from RPA.Tables import Tables, Table
from RPA.PDF import PDF
from RPA.Archive import Archive
from RPA.FileSystem import FileSystem
from SeleniumLibrary.errors import ElementNotFound
import logging
from retry import retry

class Scrapper:

    def __init__(self) -> None:
        self.browser = ExtendedSelenium()
        self.logger = logging.getLogger(__name__)

    def open_robot_order_website(self, url:str) -> None:
        """Open the robot order webiste.

        Args:
            url (str): URL to the 'Build and order your robot!' pages.
        """
        self.browser.start_driver(url, headless=False, maximized=True)

    @staticmethod
    def get_orders(url:str) -> Table:
        """Downloads the order CSV file, reads it and return the file content.

        Args:
            url (str): CSV download url.
        """
        http = HTTP()
        http.download(url, 'output/orders.csv', overwrite=True)
        
        library = Tables()
        return library.read_table_from_csv(
            'output/orders.csv', header=True
        )
    
    def close_constitutional_rights_modal(self) -> None:
        """Closes the constitutional rights modal that always shows up.
        """
        self.browser.wait_element_enabled_and_click(Locators.CLOSE_MODAL_BTN)

    def fill_the_form(self, row:dict) -> None:
        """Fill the bot ordering form.
        """
        self.browser.select_from_list_by_value(Locators.HEAD_SELECT, row['Head'])
        self.browser.wait_element_enabled_and_click(f'{Locators.BODY_INPUT}{row["Body"]}')
        self.browser.wait_element_enabled_and_input_text(Locators.LEGS_INPUT, row['Legs'])
        self.browser.wait_element_enabled_and_input_text(Locators.SHIPPING_ADDRESS, row['Address'])
        self.browser.wait_element_enabled_and_click(Locators.PREVIEW_BTN)

    @retry(exceptions=ElementNotFound, tries=5, delay=1)
    def submit_order(self) -> None:
        """Click que order robot but and checks for server errors.
        """
        self.browser.wait_element_enabled_and_click(Locators.ORDER_BTN)
        if self.browser.find_element(Locators.ORDER_ANOTHER_BTN):
            return
    
    def store_receipt_and_preview_as_pdf(self, order_number:str) -> None:
        """Export the data to a pdf file

        Args:
            order_number (str): Robot order number.
        """
        receipt_html = self.browser.wait_element_enabled_and_get_attribute(Locators.RECEIPT_DIV, 'innerHTML')
        pdf = PDF()
        pdf_path = f'output/receipts/receipt_order_number_{order_number}.pdf'
        pdf.html_to_pdf(receipt_html, pdf_path)

        screen_shot_path = f'output/preview_shot_{order_number}.png'
        self.browser.capture_element_screenshot(Locators.ROBOT_PREVIEW_DIV, screen_shot_path)

        pdf.add_files_to_pdf(
            files=[screen_shot_path],
            target_document=pdf_path,
            append=True
        )

        file_system = FileSystem()
        file_system.remove_file(screen_shot_path)

    @staticmethod
    def archive_receipts() -> None:
        """Zip all the pdf receipts"""
        lib = Archive()
        lib.archive_folder_with_zip('output/receipts', 'output/receipts.zip')
        file_system = FileSystem()
        file_system.empty_directory('output/receipts')
        file_system.remove_directory('output/receipts')

    def order_another_robot(self) -> None:
        """Click in on the 'Order another robot' button"""
        self.browser.wait_element_enabled_and_click(Locators.ORDER_ANOTHER_BTN)