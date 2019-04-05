#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    WiCC (Wireless Cracking Camp)
    GUI tool for wireless cracking on WEP and WPA/WPA2 networks.
    Project developed by Pablo Sanz Alguacil and Miguel Yanes Fernández, as the Group Project for the 3rd year of the
    Bachelor of Sicence in Computing in Digital Forensics and CyberSecurity, at TU Dublin - Blanchardstown Campus
"""
import threading
from tkinter import *
from tkinter import Tk, ttk, Frame, Button, Label, Entry, Text, Checkbutton, \
    Scale, Listbox, Menu, BOTH, RIGHT, RAISED, N, E, S, W, \
    HORIZONTAL, END, FALSE, IntVar, StringVar, messagebox, filedialog

from wicc_operations import Operation
from wicc_view_mac import ViewMac
from wicc_view_splash import Splash

class View:
    control = ""
    interfaces = ""
    networks = ""
    width = 830
    height = 420
    interfaces_old = []
    networks_old = []
    encryption_types = ('ALL', 'WEP', 'WPA')
    channels = ('ALL', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14')
    mac_spoofing_status = False
    icon_path = "Resources/icon.png"

    def __init__(self, control):
        self.control = control

    def build_window(self, headless=False, splash_image=True):
        if splash_image:
            self.splash = Splash()
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.notify_kill)
        # get screen width and height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        # calculate position x, y
        x = (ws / 2) - (self.width / 2)
        y = (hs / 2) - (self.height / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
        self.root.resizable(width=True, height=True)
        self.root.title('WiCC - Wifi Cracking Camp')
        icon = Image("photo", file=self.icon_path)
        self.root.call('wm', 'iconphoto', self.root._w, icon)

        # LABEL FRAME - ANALYSIS OPTIONS
        self.labelframe_analysis = LabelFrame(self.root, text="Analysis Options")
        self.labelframe_analysis.pack(fill="both", expand="yes")

        # LABEL FRAME - MORE FILTERS
        self.labelframe_more_options = LabelFrame(self.root, text="More Options")
        self.labelframe_more_options.pack(fill="both", expand="yes")

        # LABEL FRAME - AVAILABLE NETWORKS
        self.labelframe_networks = LabelFrame(self.root, text="Available Networks")
        self.labelframe_networks.pack(fill="both", expand="yes")

        # LABEL FRAME - START
        self.labelframe_start_stop = LabelFrame(self.root, text="Start/Stop")
        self.labelframe_start_stop.pack(fill="both", expand="yes")

        # LABEL - INTERFACES
        self.null_label0 = Message(self.labelframe_analysis, text="")
        self.null_label0.grid(column=0, row=0)
        self.label_interfaces = ttk.Label(self.labelframe_analysis, text="Interface: ")
        self.label_interfaces.grid(column=1, row=0)

        # COMBO BOX - NETWORK INTERFACES
        self.interfaceVar = StringVar()
        self.interfaces_combobox = ttk.Combobox(self.labelframe_analysis, textvariable=self.interfaceVar)
        self.interfaces_combobox['values'] = self.interfaces
        self.interfaces_combobox.bind("<<ComboboxSelected>>")
        self.interfaces_combobox.grid(column=2, row=0)
        self.null_label1 = Message(self.labelframe_analysis, text="")
        self.null_label1.grid(column=3, row=0)

        # LABEL - ENCRYPTIONS
        self.label_encryptions = ttk.Label(self.labelframe_analysis, text="Encryption: ")
        self.label_encryptions.grid(column=4, row=0)

        # COMBO BOX - ENCRYPTOION
        self.encryptionVar = StringVar()
        self.encryption_combobox = ttk.Combobox(self.labelframe_analysis, textvariable=self.encryptionVar)
        self.encryption_combobox['values'] = self.encryption_types
        self.encryption_combobox.current(0)
        self.encryption_combobox.bind("<<ComboboxSelected>>")
        self.encryption_combobox.grid(column=5, row=0)
        self.null_label2 = Message(self.labelframe_analysis, text="")
        self.null_label2.grid(column=6, row=0)

        # CHECKBUTTON - WPS
        self.wps_status = BooleanVar()
        self.wps_checkbox = ttk.Checkbutton(self.labelframe_analysis, text="Only WPS", variable=self.wps_status)
        self.wps_checkbox.grid(column=7, row=0)
        self.null_label3 = Message(self.labelframe_analysis, text="")
        self.null_label3.grid(column=8, row=0)

        # BUTTON - START SCAN
        self.button_start_scan = ttk.Button(self.labelframe_analysis, text='Start scan', command=self.start_scan)
        self.button_start_scan.grid(column=9, row=0)

        # BUTTON - STOP SCAN
        self.null_label9 = Message(self.labelframe_analysis, text="")
        self.null_label9.grid(column=10, row=0)
        self.button_stop_scan = ttk.Button(self.labelframe_analysis, text='Stop scan', state=DISABLED,
                                           command=self.stop_scan)
        self.button_stop_scan.grid(column=11, row=0)

        # LABEL - CHANNELS
        self.null_label4 = Message(self.labelframe_more_options, text="")
        self.null_label4.grid(column=0, row=0)
        self.label_channels = ttk.Label(self.labelframe_more_options, text="Channel: ")
        self.label_channels.grid(column=1, row=0)

        # COMBO BOX - CHANNELS
        self.channelVar = StringVar()
        self.channels_combobox = ttk.Combobox(self.labelframe_more_options, textvariable=self.channelVar)
        self.channels_combobox['values'] = self.channels
        self.channels_combobox.bind("<<ComboboxSelected>>")
        self.channels_combobox.current(0)
        self.channels_combobox.grid(column=2, row=0)
        self.null_label6 = Message(self.labelframe_more_options, text="")
        self.null_label6.grid(column=3, row=0, sticky=W)

        # CHECKBOX - CLIENTS
        self.clients_status = BooleanVar()
        self.clients_checkbox = ttk.Checkbutton(self.labelframe_more_options, text="Only clients",
                                                variable=self.clients_status)
        self.clients_checkbox.grid(column=4, row=0)
        self.null_label7 = Message(self.labelframe_more_options, text="")
        self.null_label7.grid(column=5, row=0)

        # BUTTON - CHANGE MAC
        self.button_mac_menu= ttk.Button(self.labelframe_more_options, text="MAC menu", state=ACTIVE,
                                         command=self.mac_menu)
        self.button_mac_menu.grid(column=6, row=0)
        self.null_label8 = Message(self.labelframe_more_options, text="")
        self.null_label8.grid(column=7, row=0)

        # BUTTON - CUSTOM WORDLIST
        self.custom_wordlist_path = ttk.Button(self.labelframe_more_options, text="Select wordlist",
                                               command=self.select_custom_wordlist)
        self.custom_wordlist_path.grid(column=8, row=0)

        # BUTTON - GENERATE WORDLIST
        self.null_label10 = Message(self.labelframe_more_options, text="")
        self.null_label10.grid(column=9, row=0)
        self.generate_wordlist = ttk.Button(self.labelframe_more_options, text="Generate wordlist")
        self.generate_wordlist.grid(column=10, row=0)

        # TREEVIEW - NETWORKS
        self.networks_treeview = ttk.Treeview(self.labelframe_networks)
        self.networks_treeview["columns"] = ("id", "bssid_col", "channel_col", "encryption_col", "power_col", "wps_col",
                                             "clients_col")
        self.networks_treeview.column("id", width=60)
        self.networks_treeview.column("bssid_col", width=150)
        self.networks_treeview.column("channel_col", width=60)
        self.networks_treeview.column("encryption_col", width=85)
        self.networks_treeview.column("power_col", width=70)
        self.networks_treeview.column("wps_col", width=60)
        self.networks_treeview.column("clients_col", width=60)

        self.networks_treeview.heading("id", text="ID")
        self.networks_treeview.heading("bssid_col", text="BSSID")
        self.networks_treeview.heading("channel_col", text="CH")
        self.networks_treeview.heading("encryption_col", text="ENC")
        self.networks_treeview.heading("power_col", text="PWR")
        self.networks_treeview.heading("wps_col", text="WPS")
        self.networks_treeview.heading("clients_col", text="CLNTS")

        self.scrollBar = Scrollbar(self.labelframe_networks)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.scrollBar.config(command=self.networks_treeview.yview)
        self.networks_treeview.config(yscrollcommand=self.scrollBar.set)

        self.networks_treeview.pack(fill=X)

        # BUTTON - ATTACK
        self.null_label2 = Message(self.labelframe_start_stop, text="")
        self.null_label2.grid(column=0, row=0)
        self.button_select = ttk.Button(self.labelframe_start_stop, text='Attack', command=self.select_network)
        self.button_select.grid(column=1, row=0)
        self.null_label3 = Message(self.labelframe_start_stop, text="")
        self.null_label3.grid(column=2, row=0)

        if not headless:
            self.root.mainloop()

    # Sends the selected interface to control
    def start_scan(self):
        self.disable_buttons()
        self.send_notify(Operation.SCAN_OPTIONS, self.apply_filters())
        self.send_notify(Operation.SELECT_INTERFACE, self.interfaceVar.get())

    # Sends a stop scanning order to control
    def stop_scan(self):
        self.enable_buttons()
        self.send_notify(Operation.STOP_SCAN, "")

    def disable_buttons(self):
        self.button_mac_menu['state'] = DISABLED
        self.custom_wordlist_path['state'] = DISABLED
        self.generate_wordlist['state'] = DISABLED
        self.interfaces_combobox['state'] = DISABLED
        self.encryption_combobox['state'] = DISABLED
        self.wps_checkbox['state'] = DISABLED
        self.channels_combobox['state'] = DISABLED
        self.clients_checkbox['state'] = DISABLED
        self.button_start_scan['state'] = DISABLED
        self.button_stop_scan['state'] = ACTIVE

    def enable_buttons(self):
        self.button_mac_menu['state'] = ACTIVE
        self.custom_wordlist_path['state'] = ACTIVE
        self.generate_wordlist['state'] = ACTIVE
        self.interfaces_combobox['state'] = ACTIVE
        self.encryption_combobox['state'] = ACTIVE
        self.wps_checkbox['state'] = ACTIVE
        self.channels_combobox['state'] = ACTIVE
        self.clients_checkbox['state'] = ACTIVE
        self.button_start_scan['state'] = ACTIVE
        self.button_stop_scan['state'] = DISABLED


    # Sends the selected network id to Control
    def select_network(self):
        current_item = self.networks_treeview.focus()
        network_id = self.networks_treeview.item(current_item)['values'][0]
        self.send_notify(Operation.SELECT_NETWORK, network_id)

    # Sends and order to kill all processes when X is clicked
    def notify_kill(self):
        self.send_notify(Operation.STOP_RUNNING, "")

    # Receives a notification to kill view
    def reaper_calls(self):
        self.root.destroy()


    # Shows a window to select a custom wordlist to use. Then sends the path to control.
    def select_custom_wordlist(self):
        select_window = filedialog.askopenfilename(parent=self.root, initialdir='/home/$USER', title='Choose file',
                                                   filetypes=[('Text files', '.txt'), ("All files", "*.*")])
        if select_window:
            try:
                self.send_notify(Operation.SELECT_CUSTOM_WORDLIST, select_window)
            except:
                messagebox.showerror("Open Source File", "Failed to read file \n'%s'" % select_window)
                return

    # Sends an order to randomize the interface MAC address
    def randomize_mac(self):
        if (self.interfaceVar.get() != ""):
            currentmac_alert = messagebox.askyesno("", "Your current MAC is: " + self.current_mac()
                                                   + "\n\nAre you sure you want to change it? ")
            if (currentmac_alert == True):
                self.send_notify(Operation.RANDOMIZE_MAC, self.interfaceVar.get())
                new_mac_alert = messagebox.showinfo("", "Your new MAC is: " + self.current_mac())
        else:
            self.show_warning_notification("No interface selected. Close the window and select one")

    def customize_mac(self, new_mac):
        if (self.interfaceVar.get() != ""):
            currentmac_alert = messagebox.askyesno("", "Your current MAC is: " + self.current_mac()
                                                   + "\n\nAre you sure you want to change it for\n" +
                                                   new_mac + " ?")
            if (currentmac_alert == True):
                self.send_notify(Operation.CUSTOMIZE_MAC, (self.interfaceVar.get(), new_mac))
                new_mac_alert = messagebox.showinfo("", "Your new MAC is: " + self.current_mac())
        else:
            self.show_warning_notification("No interface selected. Close the window and select one")

    def restore_mac(self):
        if (self.interfaceVar.get() != ""):
            currentmac_alert = messagebox.askyesno("", "Your current MAC is: " + self.current_mac()
                                                   + "\n\nAre you sure you want to restore original?")
            if (currentmac_alert == True):
                self.send_notify(Operation.RESTORE_MAC, self.interfaceVar.get())
                new_mac_alert = messagebox.showinfo("", "Your new MAC is: " + self.current_mac())
        else:
            self.show_warning_notification("No interface selected. Close the window and select one")

    def spoofing_mac(self, status):
        if (self.interfaceVar.get() != ""):
                self.send_notify(Operation.SPOOF_MAC, status)
        else:
            self.show_warning_notification("No interface selected. Close the window and select one")

    def mac_menu(self):
        self.disable_window(True)
        mac_menu_window = ViewMac(self, self.mac_spoofing_status)

    # Filters networks
    """
    [0]ENCRYPTION (string)
    [1]WPS (boolean)
    [2]CLIENTS (boolean)
    [3]CHANNEL (string)
    """
    def apply_filters(self):
        filters_status = ["ALL", False, False, "ALL"]
        if (self.encryptionVar.get() != "ALL"):
            print("ENCRYPTION FILTER ENABLED")
            filters_status[0] = self.encryptionVar.get()
        if (self.wps_status.get() == True):
            print("WPS FILTER ENABLED")
            filters_status[1] = True
        if (self.clients_status.get() == True):
            print("CLIENTS FILTER ENABLED")
            filters_status[2] = True
        if (self.channelVar.get() != "ALL"):
            print("CHANNELS FILTER ENABLED")
            filters_status[3] = self.channelVar.get()
        return filters_status

    def get_notify(self, interfaces, networks):
        if (self.interfaces_old != interfaces):
            self.interfaces_old = interfaces
            interfaces_list = []
            for item in interfaces:
                interfaces_list.append(item[0])
            self.interfaces_combobox['values'] = interfaces_list
            self.interfaces_combobox.update()

        if (self.networks_old != networks):
            self.networks_old = networks
            self.networks_treeview.delete(*self.networks_treeview.get_children())
            for item in networks:
                self.networks_treeview.insert("", END, text=item[13], values=(item[0], item[1], item[4], item[6],
                                                                              item[9] + " dbi", "yes", item[16]))
                self.networks_treeview.update()

    def current_mac(self):
        return str(self.control.mac_checker(self.interfaceVar.get()))

    def get_notify_mac(self, operation, value):
        if(operation == 0):     #custom MAC
            print("CUSTIMIZE MAC OPERATION")
            self.customize_mac(value)
        elif(operation == 1):    #random MAC
            print("RANDOMIZE MAC OPERATION")
            self.randomize_mac()
        elif(operation == 2):   #restore MAC
            print("RESTORE MAC OPERATION")
            self.restore_mac()
        elif(operation == 3):   #MAC spoofing
            print("MAC SPOOFING OPERATION: " + str(self.mac_spoofing_status))
            self.mac_spoofing_status = value
            self.spoofing_mac(value)

    def get_spoofing_status(self):
        return self.mac_spoofing_status


    ##########################################
    # SET NOTIFICATIONS TITLES AS PARAMETERS #
    ##########################################
    def show_warning_notification(self, message):
        warning_notification = messagebox.showwarning("Warning", message)
        print(warning_notification)

    def show_info_notification(self, message):
        info_notification = messagebox.showinfo("Info", message)
        print(info_notification)

    def send_notify(self, operation, value):
        self.control.get_notify(operation, value)
        return

    def disable_window(self, value):
        if value:
            self.disable_buttons()
            self.button_stop_scan['state'] = DISABLED
            self.button_select['state'] = DISABLED
        elif not value:
            self.enable_buttons()
            self.button_select['state'] = ACTIVE
