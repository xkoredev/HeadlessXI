import time
from headlessxi import HeadlessXIClient

def main():
    # Create a client and log in
    hxi_client = HeadlessXIClient("admin", "admin", "localhost")
    hxi_client.login()

    # Wait a while for login
    time.sleep(10)

    # Send GM commands
    hxi_client.send_say("!bring Testtwo")
    time.sleep(5)

    # Send /say messages
    hxi_client.send_say("Hello from HeadlessXIClient!")
    time.sleep(5)

    # Goodbye
    hxi_client.logout()

if __name__ == "__main__":
    main()
