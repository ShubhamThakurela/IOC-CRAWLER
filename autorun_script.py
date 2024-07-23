import schedule
import time
from main.ioc_service import IocService
import functools


def run_script(excel_file_path_param):
    try:
        run_file = IocService.crawl_by_file(excel_file_path_param)
        if run_file:
            print("Success", "Your Daily task ran Successfully")
        else:
            print("failed", "Please try again and check the logs")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    excel_file_path = input("please enter the source file path:")
    # Create a partial function with the desired arguments
    scheduled_function = functools.partial(run_script, excel_file_path)
    # Schedule the function to run every 3 days
    # schedule.every(1).minutes.do(scheduled_function)
    schedule.every(3).days.do(scheduled_function)
    while True:
        schedule.run_pending()
        time.sleep(1)
