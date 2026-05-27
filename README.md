
# Smart Counter Analytics System

A smart counter management and analytics system built using Arduino and Python.

## 🚀 Features

- Live counter status monitoring
- LCD display interface
- LED indicators
- Melody-based buzzer alerts
- Customer service time tracking
- Idle time tracking
- Real-time desktop analytics dashboard
- CSV data logging

## 🛠 Technologies Used

### Embedded Hardware
- Arduino UNO
- I2C LCD
- Push Buttons
- LEDs
- Passive Buzzer

### Software
- Python
- CustomTkinter
- Pandas
- Serial Communication

## 💡 Project Idea

The system is designed for service counters such as:
- banks
- reception desks
- customer support counters

Staff manually update whether the counter is occupied or free using push buttons.

The system tracks:
- customer handling duration
- counter idle duration
- operational analytics

## 📊 Dashboard Features

- Live counter status
- Total customers served
- Average service time
- Average idle time
- Timestamp logging

<img width="1919" height="808" alt="Dashboard" src="https://github.com/user-attachments/assets/4de79ed3-6f64-4d35-9344-f13e3c650275" />


## Hardware Demonstration

### 🟢 Counter Free State

<img width="600" height="300" alt="counter_free" src="https://github.com/user-attachments/assets/bf5aa7d0-20c2-4472-8a22-184e59786a28" />


### 🔴 Counter Occupied State

<img width="600" height="300" alt="counter_busy" src="https://github.com/user-attachments/assets/8e5578b9-a68b-4d98-bd72-cbebf07e35a5" />

## How It Works
The sensor detects whether a seat/space is occupied. 
Arduino sends the status through serial communication, and the Python script logs and displays the data in real time.

## Project Structure
- `arduino_code.ino` → Arduino logic
- `logger.py` → Python serial logger

## 📁 Future Improvements

- Multi-counter support
- Web dashboard
- RFID staff login
- Queue/token management
- Cloud analytics integration

## 👩‍💻 Developed By

K Subitsha 
