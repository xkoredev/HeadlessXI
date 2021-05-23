import time
from client import Client

def main():
    # Create a client and log in
    client = Client("admin", "admin", "localhost")
    client.login()

    # Wait a while for login
    time.sleep(10)

    # Send GM commands
    client.send_tell("!bring Testtwo")

    # Goodbye
    client.logout()

if __name__ == "__main__":
    main()
