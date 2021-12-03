#!/usr/bin/env python

import os
import argparse


def deploy():
    # 1. Copy service from a develop dir to the systemd directory
    # 2. Reload systemd manager configuration
    # 3. Start the sysprog service
    os.system(
        """
        sudo cp .service /etc/systemd/system/sysprog.service \
        && sudo systemctl daemon-reload \
        && sudo systemctl start sysprog
        """
    )


def start():
    os.system("sudo systemctl start sysprog")


def stop():
    os.system("sudo systemctl stop sysprog")


def restart():
    os.system("sudo systemctl restart sysprog")


def show_status():
    os.system("systemctl status sysprog")


def show_logs():
    os.system("journalctl -u sysprog -f")


def run_client():
    os.system("python sysprog_client.py")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-d", "--deploy", action="store_true", help="Deploy the service.")
    parser.add_argument("-q", "--stop", action="store_true", help="Stop the service.")
    parser.add_argument("-r", "--start", action="store_true", help="Start the service.")
    parser.add_argument("-R", "--restart", action="store_true", help="Restart the service.")
    parser.add_argument("-l", "--logs", action="store_true", help="Show service logs.")
    parser.add_argument("-s", "--status", action="store_true", help="Show service status.")
    parser.add_argument("-c", "--client", action="store_true", help="Run the client.")
    args = parser.parse_args()

    if args.deploy:
        print("Deploying...")
        deploy()
    elif args.start:
        print("Starting...")
        start()
    elif args.stop:
        print("Stopping...")
        stop()
    elif args.restart:
        print("Stopping...")
        stop()
    elif args.logs:
        print("Showing logs...")
        show_logs()
    elif args.status:
        print("Showing status...")
        show_status()
    elif args.client:
        print("Running client...")
        run_client()
    print("Done.")

