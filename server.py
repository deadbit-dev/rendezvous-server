import os
import argparse
import socket
import logging

DEFAULT_IP = '0.0.0.0'
DEFAULT_PORT = 9999

def get_arguments():
    """Setup and parse arguments."""
    parser = argparse.ArgumentParser(description='P2P Server')
    parser.add_argument('-i', '--ip', type=str, required=False, default=DEFAULT_IP)
    parser.add_argument('-p', '--port', type=int, required=False, default=DEFAULT_PORT)

    return parser.parse_args()


def address_to_message(ip, port):
    """Format ip and port value to string."""
    return '{}:{}'.format(ip, str(port)).encode('utf-8')


def main():
    """Entry point module."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler(os.sys.stdout)]
    )

    args = get_arguments()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.ip, args.port))

    addresses = []

    error_buf = None
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            logging.info(f'Connection from: {addr}')
            addresses.append(addr)

            if len(addresses) >= 2:
                logging.info(f'Server send client {addresses[1]} info to {addresses[0]}')
                sock.sendto(address_to_message(*addresses[1]), addresses[0])
                logging.info(f'Server send client {addresses[0]} info to {addresses[1]}')
                sock.sendto(address_to_message(*addresses[0]), addresses[1])
                addresses.clear()

        except Exception as error:
            message = f'Server crash: {error}'
            if error_buf != message:
                error_buf = message
                logging.error(message)


if __name__ == '__main__':
    main()