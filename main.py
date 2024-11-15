import webbrowser
import tkinter as tk
from tkinter import scrolledtext, messagebox
import serial
import threading



from setting import open_settings_window, serial_settings

# ตั้งค่า COM port และ baud rate
ser = None
reading_flag = False  # ใช้ควบคุมการทำงานของ thread
version = "New version"


def open_about_window():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    # ปรับขนาดหน้าต่างให้รองรับข้อมูลเพิ่มเติม
    about_window.geometry("380x320")
    about_window.configure(bg="#DDF3F8")

    # ข้อมูลเกี่ยวกับโปรแกรม
    about_label = tk.Label(about_window, text="Tkinter-ComPortMonitor", font=(
        "Arial", 16, "bold"), background="#DDF3F8")
    about_label.pack(pady=10)

    version_label = tk.Label(
        about_window, text=f"Version: {version}", background="#DDF3F8")
    version_label.pack(pady=5)

    author_label = tk.Label(
        about_window, text="Author: sitthisukchara", background="#DDF3F8")
    author_label.pack(pady=5)

    description_label = tk.Label(
        about_window,
        text="This application is sample Tkinter-ComPortMonitor",
        wraplength=300,
        background="#DDF3F8"
    )
    description_label.pack(pady=10)

    # เพิ่มข้อมูลการติดต่อ
    contact_label = tk.Label(
        about_window, text="Contact: sitthisukchara@gmail.com", background="#DDF3F8")
    contact_label.pack(pady=5)

    # ปุ่มปิดหน้าต่าง About
    close_button = tk.Button(
        about_window,
        text="Close",
        command=about_window.destroy,
        bg="#006CEB",
        fg="#FFFFFF",
        font=("Arial", 12),
        width=10
    )
    close_button.pack(pady=10)


def read_from_port():
    global reading_flag, ser
    try:
        while reading_flag:
            if ser and ser.in_waiting > 0:  # ตรวจสอบว่า ser เปิดอยู่
                # print(ser.read_until(b'\x03'))
                data = ser.readline().decode('utf-8').rstrip()
                print(data)
                if data:
                    text_area.insert(tk.END, data + '\n')
                    text_area.yview(tk.END)  # เลื่อนลงอัตโนมัติ
                else:
                    continue  # ไม่มีข้อมูล รอจนกว่าจะมีข้อมูลใหม่
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Serial error: {e}")
        stop_reading()  # หยุดการอ่านเมื่อเกิดข้อผิดพลาด


# ฟังก์ชันเริ่มการอ่านข้อมูล
def start_reading():
    global reading_flag, ser
    if not reading_flag:
        try:
            # เปิดพอร์ต COM ด้วยการใช้ค่าจาก serial_settings
            ser = serial.Serial(**serial_settings)
            reading_flag = True
            thread = threading.Thread(target=read_from_port)
            thread.daemon = True
            thread.start()
        except serial.SerialException as e:
            text_area.insert(tk.END, f"Error: {e}\n")


# ฟังก์ชันหยุดการอ่านข้อมูล
def stop_reading():
    global reading_flag, ser
    if reading_flag:
        reading_flag = False
        if ser is not None:
            ser.close()  # ปิดการเชื่อมต่อ COM port
            ser = None
        text_area.insert(tk.END, "Stopped reading and closed the port.\n")


def clear_text_area():
    text_area.delete(1.0, tk.END)  # ลบเนื้อหาทั้งหมดใน text_area


def send_data():
    ser.write(b'Hello, World\r\n')


# สร้างหน้าต่างหลักของ Tkinter
root = tk.Tk()
root.title("COM Port Reader")
root.geometry("400x300")

menu_bar = tk.Menu(root,  foreground="#000080")
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open Data", command="open_and_print_credentials")
file_menu.add_command(label="Load Data", command="load_data")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)


setting_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="settings", menu=setting_menu)
setting_menu.add_command(label="Open Settings",
                         command=lambda: open_settings_window(root))


help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=open_about_window)
# help_menu.add_command(label="Check for Updates", command=ota.check_for_update)
root.config(menu=menu_bar)

# สร้างส่วนแสดงข้อความ
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
text_area.pack(padx=10, pady=10)

# ปุ่มเริ่มอ่านข้อมูล
start_button = tk.Button(root, text="Start Reading", command=start_reading)
start_button.pack(pady=5)

# ปุ่มหยุดอ่านข้อมูล
stop_button = tk.Button(root, text="Stop Reading", command=stop_reading)
stop_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear", command=clear_text_area)
clear_button.pack(pady=5)

send_button = tk.Button(root, text="Send data", command=send_data)
send_button.pack(pady=5)

# root.after(1000, lambda: ota.check_for_update())
# เริ่มต้น Tkinter loop
root.mainloop()

# ปิดการเชื่อมต่อเมื่อปิดโปรแกรม
if ser is not None:
    ser.close()
