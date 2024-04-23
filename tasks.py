from scrapper import Scrapper
from robocorp.tasks import task

@task
def order_robots_process():
    # 'https://robotsparebinindustries.com/#/robot-order'
    scrapper = Scrapper()
    site_url = scrapper.ask_user_for_url()
    scrapper.open_robot_order_website(site_url)
    orders = scrapper.get_orders('https://robotsparebinindustries.com/orders.csv')
    for row in orders:
        scrapper.close_constitutional_rights_modal()
        scrapper.fill_the_form(row)
        scrapper.submit_order()
        scrapper.store_receipt_and_preview_as_pdf(row['Order number'])
        scrapper.order_another_robot()
    scrapper.archive_receipts()
    