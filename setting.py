import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import tkinter.messagebox as messagebox
# from login import login
# from main import login


# Default serial settings
serial_settings = {
    # 'port': 'COM16',  # หรือพอร์ตที่คุณใช้ เช่น COM4
    # 'baudrate': 9600,
    # 'parity': serial.PARITY_NONE,  # ไม่มี parity สำหรับ Arduino
    # 'bytesize': serial.EIGHTBITS,  # 8-bit data length
    # 'stopbits': serial.STOPBITS_ONE,  # 1 stop bit
    # 'timeout': 1  # ค่า timeout สำหรับการอ่าน

    'port': '16',  # COM4 For  JSIMs computer
    'baudrate': 9600,
    'parity': serial.PARITY_EVEN,
    'bytesize': serial.SEVENBITS,
    'stopbits': serial.STOPBITS_ONE,
    'timeout': 1
}

# Scan and list available serial ports with descriptions


def scan_ports():
    ports = serial.tools.list_ports.comports()
    return [f"{port.device}: {port.description}" for port in ports]


# def setting_login(parent_window):
#     # Perform login and get the result (True/False)
#     login_success = login(parent_window)
#     print(login_success)

#     if login_success:
#         print('setting Login successful')
#         open_settings_window(parent_window)

#     else:
#         print('setting Login failed')
#         return


def open_settings_window(parent_window):

    settings_window = tk.Toplevel(parent_window)
    settings_window.title("Serial Port Settings")
    # Increased height to accommodate the header
    settings_window.geometry("350x350")
    settings_window.configure(bg="#DDF3F8")

    # Header label
    header_label = ttk.Label(settings_window, text="Serial Port Settings", font=(
        "Arial", 14, "bold"), background="#DDF3F8")
    header_label.grid(row=0, column=0, columnspan=2,
                      padx=10, pady=10, sticky="w")

    # Port Combobox
    ttk.Label(settings_window, text="Port:", background="#DDF3F8").grid(
        row=1, column=0, padx=10, pady=5, sticky="e")
    port_var = tk.StringVar(value=serial_settings['port'])
    port_combobox = ttk.Combobox(settings_window, textvariable=port_var)
    port_combobox.grid(row=1, column=1, padx=10, pady=5)
    port_combobox['values'] = scan_ports()

    # Baudrate Combobox
    ttk.Label(settings_window, text="Baudrate:", background="#DDF3F8").grid(
        row=2, column=0, padx=10, pady=5, sticky="e")
    baudrate_var = tk.StringVar(value=serial_settings['baudrate'])
    baudrate_combobox = ttk.Combobox(settings_window, textvariable=baudrate_var, values=[
        9600, 19200, 38400, 57600, 115200])
    baudrate_combobox.grid(row=2, column=1, padx=10, pady=5)

    # Parity Combobox
    ttk.Label(settings_window, text="Parity:", background="#DDF3F8").grid(
        row=3, column=0, padx=10, pady=5, sticky="e")
    parity_var = tk.StringVar(value={serial.PARITY_EVEN: "Even", serial.PARITY_ODD: "Odd",
                                     serial.PARITY_NONE: "None"}[serial_settings['parity']])
    parity_combobox = ttk.Combobox(
        settings_window, textvariable=parity_var, values=["None", "Even", "Odd"])
    parity_combobox.grid(row=3, column=1, padx=10, pady=5)

    # Bytesize Combobox
    ttk.Label(settings_window, text="Bytesize:", background="#DDF3F8").grid(
        row=4, column=0, padx=10, pady=5, sticky="e")
    bytesize_var = tk.StringVar(value={serial.SEVENBITS: 7, serial.EIGHTBITS: 8}[
        serial_settings['bytesize']])
    bytesize_combobox = ttk.Combobox(
        settings_window, textvariable=bytesize_var, values=[7, 8])
    bytesize_combobox.grid(row=4, column=1, padx=10, pady=5)

    # Stopbits Combobox
    ttk.Label(settings_window, text="Stopbits:", background="#DDF3F8").grid(
        row=5, column=0, padx=10, pady=5, sticky="e")
    stopbits_var = tk.StringVar(value={serial.STOPBITS_ONE: "1", serial.STOPBITS_ONE_POINT_FIVE: "1.5", serial.STOPBITS_TWO: "2"}[
        serial_settings['stopbits']])
    stopbits_combobox = ttk.Combobox(
        settings_window, textvariable=stopbits_var, values=["1", "1.5", "2"])
    stopbits_combobox.grid(row=5, column=1, padx=10, pady=5)

    # Timeout Combobox
    ttk.Label(settings_window, text="Timeout:", background="#DDF3F8").grid(
        row=6, column=0, padx=10, pady=5, sticky="e")
    timeout_var = tk.StringVar(value=serial_settings['timeout'])
    timeout_combobox = ttk.Combobox(
        settings_window, textvariable=timeout_var, values=[0.1, 0.5, 1, 2, 5])
    timeout_combobox.grid(row=6, column=1, padx=10, pady=5)

    # Save settings function
    def save_settings():
        serial_settings['port'] = port_combobox.get().split(
            ":")[0]  # Extract port name from the description
        serial_settings['baudrate'] = int(baudrate_combobox.get())
        serial_settings['parity'] = {
            "None": serial.PARITY_NONE, "Even": serial.PARITY_EVEN, "Odd": serial.PARITY_ODD}[parity_combobox.get()]
        serial_settings['bytesize'] = int(bytesize_combobox.get())
        serial_settings['stopbits'] = {
            "1": serial.STOPBITS_ONE, "1.5": serial.STOPBITS_ONE_POINT_FIVE, "2": serial.STOPBITS_TWO}[stopbits_combobox.get()]
        serial_settings['timeout'] = float(timeout_combobox.get())
        settings_window.destroy()

    # Reset settings function
    def reset_settings():
        port_combobox.set(serial_settings['port'])
        baudrate_combobox.set(serial_settings['baudrate'])
        parity_combobox.set({serial.PARITY_EVEN: "Even", serial.PARITY_ODD: "Odd",
                            serial.PARITY_NONE: "None"}[serial_settings['parity']])
        bytesize_combobox.set({serial.SEVENBITS: 7, serial.EIGHTBITS: 8}[
            serial_settings['bytesize']])
        stopbits_combobox.set({serial.STOPBITS_ONE: "1", serial.STOPBITS_ONE_POINT_FIVE: "1.5",
                               serial.STOPBITS_TWO: "2"}[serial_settings['stopbits']])
        timeout_combobox.set(serial_settings['timeout'])

    # Scan ports function
    def scan_ports_action():
        available_ports = scan_ports()
        if available_ports:
            ports_info = "\n".join(available_ports)
            messagebox.showinfo(
                "Port Scan", f"Available ports:\n{ports_info}")
        else:
            messagebox.showinfo("Port Scan", "No ports found.")

    # Create buttons
    save_button = ttk.Button(
        settings_window, text="Save", command=save_settings)
    save_button.grid(row=7, column=0, padx=10, pady=10)

    scan_button = ttk.Button(
        settings_window, text="Scan Ports", command=scan_ports_action)
    scan_button.grid(row=7, column=1, padx=10, pady=10)

    reset_button = ttk.Button(
        settings_window, text="Reset", command=reset_settings)
    reset_button.grid(row=7, column=2, padx=10, pady=10)
