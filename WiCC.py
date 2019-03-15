from wicc_control import Control
import sys
import os
import time
import threading


if __name__ == '__main__':
    # check root privilege
    if os.getuid() != 0:
        print("\n\tError: script must be executed as root\n")
        sys.exit(1)

    # checks python version
    if sys.version_info[0] < 3:
        print("\n\tError: Must be executed with Python 3\n")
        sys.exit(1)

    control = Control()

    software, some_missing = control.check_software()
    if some_missing:
        print("The required software is not installed:\n")
        for i in range(0, len(software)):
            if not software[i]:
                if i == 0:
                    print("\t***Missing ifconfig")
                elif i == 1:
                    print("\t***Missing aircrack-ng")
                elif i == 2:
                    print("\t***Missing pyrit")
                elif i == 3:
                    print("\t***Missing cowpatty")

        print("\n")
        sys.exit(1)

    exit = False

    print("\n\tStarting WiCC\n")

    view_thread = threading.Thread(target=control.start_view)
    view_thread.start()
    view_thread.join(1)
    while not exit:
        if control.has_selected_interface():
            print("Selected interface: " + control.selectedInterface)
            control.scan_networks()
            print("Start scanning available networks...")
            time.sleep(3)
            while control.selectedNetwork == "":
                time.sleep(1)
                print("\t... Scanning networks ...")
                control.filter_networks()
            print("Selected network: " + str(control.selectedNetwork))
            print("\nStarting attack...\n")
            sys.exit(0)
        else:
            print("Scanning interfaces")
            control.scan_interfaces()
        time.sleep(1)
