import serial
import customtkinter as ctk
from tkinter import ttk
import pandas as pd
from datetime import datetime

# =========================
# SERIAL CONNECTION
# =========================
arduino = serial.Serial('COM3', 9600)

# =========================
# APP SETTINGS
# =========================
ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")

# =========================
# WINDOW
# =========================
root = ctk.CTk()

root.title("Smart Counter Dashboard")

root.geometry("950x650")

# =========================
# DATA
# =========================
logs = []

total_duration = 0

total_idle = 0

# =========================
# TITLE
# =========================
title = ctk.CTkLabel(
    root,
    text="SMART COUNTER ANALYTICS",
    font=("Arial", 30, "bold")
)

title.pack(pady=20)

# =========================
# TOP FRAME
# =========================
top_frame = ctk.CTkFrame(root)

top_frame.pack(
    pady=10,
    padx=20,
    fill="x"
)

# =========================
# STATUS
# =========================
status_label = ctk.CTkLabel(
    top_frame,
    text="🟢 COUNTER FREE",
    font=("Arial", 20, "bold")
)

status_label.grid(
    row=0,
    column=0,
    padx=30,
    pady=20
)

# =========================
# CUSTOMER COUNT
# =========================
customer_label = ctk.CTkLabel(
    top_frame,
    text="Customers: 0",
    font=("Arial", 20)
)

customer_label.grid(
    row=0,
    column=1,
    padx=30
)

# =========================
# AVG SERVICE TIME
# =========================
avg_service_label = ctk.CTkLabel(
    top_frame,
    text="Avg Service: 0 sec",
    font=("Arial", 20)
)

avg_service_label.grid(
    row=0,
    column=2,
    padx=30
)

# =========================
# AVG IDLE TIME
# =========================
avg_idle_label = ctk.CTkLabel(
    top_frame,
    text="Avg Idle: 0 sec",
    font=("Arial", 20)
)

avg_idle_label.grid(
    row=0,
    column=3,
    padx=30
)

# =========================
# TABLE FRAME
# =========================
table_frame = ctk.CTkFrame(root)

table_frame.pack(
    pady=20,
    padx=20,
    fill="both",
    expand=True
)

# =========================
# TABLE
# =========================
columns = (
    "Customer ID",
    "Service Time",
    "Idle Time",
    "Timestamp"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=18
)

for col in columns:

    table.heading(col, text=col)

    table.column(
        col,
        width=180,
        anchor="center"
    )

table.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# =========================
# SERIAL FUNCTION
# =========================
def read_serial():

    global total_duration
    global total_idle

    if arduino.in_waiting:

        line = arduino.readline().decode().strip()

        print("Received:", line)

        # =========================
        # LIVE STATUS
        # =========================
        if line == "BUSY":

            status_label.configure(
                text="🔴 COUNTER BUSY"
            )

        if line == "FREE":

            status_label.configure(
                text="🟢 COUNTER FREE"
            )

        # =========================
        # LOG DATA
        # =========================
        if line.startswith("LOG"):

            parts = line.split(",")

            customer = int(parts[1])

            duration = int(parts[2])

            idle = int(parts[3])

            current_time = datetime.now().strftime("%H:%M:%S")

            # =========================
            # UPDATE ANALYTICS
            # =========================
            customer_label.configure(
                text=f"Customers: {customer}"
            )

            total_duration += duration

            total_idle += idle

            avg_service = round(
                total_duration / customer,
                1
            )

            avg_idle = round(
                total_idle / customer,
                1
            )

            avg_service_label.configure(
                text=f"Avg Service: {avg_service} sec"
            )

            avg_idle_label.configure(
                text=f"Avg Idle: {avg_idle} sec"
            )

            # =========================
            # ADD TABLE ROW
            # =========================
            table.insert(
                "",
                "end",
                values=(
                    customer,
                    str(duration) + " sec",
                    str(idle) + " sec",
                    current_time
                )
            )

            # =========================
            # SAVE CSV
            # =========================
            logs.append({
                "Customer": customer,
                "Service Time": duration,
                "Idle Time": idle,
                "Timestamp": current_time
            })

            df = pd.DataFrame(logs)

            df.to_csv(
                "counter_logs.csv",
                index=False
            )

    root.after(100, read_serial)

# =========================
# START
# =========================
read_serial()

root.mainloop()