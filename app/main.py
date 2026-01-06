import pprint
import requests
import os

from dotenv import load_dotenv

from atlassian import Jira
from atlassian import ServiceDesk

###############################################################################
#
# Environment
#
###############################################################################
load_dotenv()  # take environment variables from .env file


###############################################################################
#
# Print
#
###############################################################################
def print_service_desks(jsm: ServiceDesk) -> None:
    service_desks = jsm.get_service_desks()
    print("== Service Desks available ==")
    print(f"{'ID':4}{'Name':40}{'Key':12}")
    print("-" * 60)
    for sd in service_desks:
        print(f"{sd['id']:4}{sd['projectName']:40}{sd['projectKey']:12}")
    print("")

def print_menu() -> None:
    print("\n\n\tMenu options:")
    print("1. List Service Desks")
    print("2. Exit")


###############################################################################
#
# main
#
###############################################################################
if __name__ == "__main__":
    jsm = ServiceDesk(
        url='https://qs-cloud.atlassian.net',
        username=os.getenv('USERNAME'),
        password=os.getenv('TOKEN'),
        cloud=True)

    print_service_desks(jsm)

    while True:
        print_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            print_service_desks(jsm)
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
