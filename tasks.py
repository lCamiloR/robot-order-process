from scrapper import Scrapper
from robocorp.tasks import task

@task
def order_robots_process():
    scrapper = Scrapper()
    scrapper.open_robot_order_website('https://robotsparebinindustries.com/#/robot-order')
    orders = scrapper.get_orders('https://robotsparebinindustries.com/orders.csv')
    for row in orders:
        scrapper.close_constitutional_rights_modal()
        scrapper.fill_the_form(row)
        scrapper.submit_order()
        scrapper.store_receipt_and_preview_as_pdf(row['Order number'])
        scrapper.order_another_robot()
    scrapper.archive_receipts()
    