import time
from client import Client

user = "admin"
password = "admin"
server = "localhost"
char_slot = 1 # Note: 1-based

def main():
    client = Client("admin", "admin", "localhost", 0)
    client.login()
    time.sleep(10)
    client.send_tell("Hello!")
    time.sleep(5)
    client.logout()

if __name__ == "__main__":
    main()
