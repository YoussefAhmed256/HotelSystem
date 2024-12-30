# Hotel Booking Application

## Introduction

This project is a hotel booking system that allows users to book rooms, select additional services, and manage guest information. It includes an interactive Graphical User Interface (GUI) built using Python's `Tkinter` library and connects to a Microsoft SQL Server database to store and manage guest, room, booking, and service data.

The system features functionalities like room availability checking, booking rooms, and adding extra services to a booking. It uses triggers and stored procedures to manage room status and ensure the availability of rooms during bookings.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Database Schema](#database-schema)
3. [Features](#features)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)
8. [Contributors](#contributors)

## Project Structure

- **hotel_booking_app.py**: Main Python script for the Tkinter-based GUI application.
- **database_schema.sql**: SQL script for creating the database and tables for the hotel system.
- **requirements.txt**: File listing all Python dependencies.

## Database Schema

The database consists of multiple tables to manage guests, rooms, bookings, and services:

1. **guest**: Stores guest details such as name, SSN, email, and phone number.
2. **floor**: Represents hotel floors.
3. **room**: Represents rooms in the hotel, linked to the floor and room class.
4. **room_class**: Defines the types of rooms (e.g., Standard, Deluxe, Suite) and their prices.
5. **room_status**: Manages the status of rooms (e.g., available, occupied).
6. **booking**: Contains booking details like check-in/check-out dates, number of rooms, and payment status.
7. **booking_room**: Associates rooms with bookings.
8. **services**: Lists additional services (e.g., breakfast, gym access) available for booking.
9. **booking_service**: Maps additional services to bookings.
10. **Triggers and Procedures**:
    - **UpdateRoomStatusAfterCheckout**: Updates room status after checkout.
    - **get_available_rooms**: Retrieves available rooms for a given date range.

## Features

- **Booking Flow**: Allows users to enter guest details, select room types, choose additional services, and finalize bookings.
- **Room Availability Check**: The application checks the availability of rooms based on the selected check-in and check-out dates.
- **Additional Services**: Users can select additional services like breakfast, spa, and airport pickup during booking.
- **Payment Calculation**: The system calculates the total price for bookings based on the selected room type, number of rooms, services, and stay duration.
- **Database Integration**: Uses SQL Server for data management, with triggers and stored procedures to ensure integrity and data consistency.

## Installation

### Prerequisites

1. Python 3.x
2. Microsoft SQL Server
3. Python libraries:
   - `pyodbc`
   - `tkinter`
   - `tkcalendar`

### Steps to Install

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**:
   Create a `virtualenv` and install the required packages.
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the Database**:
   1. Open SQL Server Management Studio (SSMS).
   2. Run the `database_schema.sql` script to create the necessary tables and stored procedures.
   3. Make sure the database `HotelSystem` is created and the necessary tables are populated.

4. **Run the Application**:
   ```bash
   python hotel_booking_app.py
   ```

## Usage

- When you run the application, the **Home Page** will be displayed, offering options to book a room.
- **Guest Data**: Enter personal details including name, email, phone number, and SSN.
- **Service Selection**: Choose from a list of additional services such as breakfast, spa, etc.
- **Room Selection**: Select your room type and dates, and check availability.
- **Booking Confirmation**: View the booking details and total cost before confirming the booking.

## Configuration

- **Database Connection**: The application connects to SQL Server using the following connection string:
  ```python
  self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Youssef;DATABASE=HotelSystem;')
  ```
  You may need to adjust the `SERVER` parameter to point to your local or remote SQL Server instance.

## Troubleshooting

- **Issue: Database Connection Error**
  - Check the SQL Server instance and ensure it is running.
  - Verify the database name `HotelSystem` exists and that your connection string is correct.
  - Ensure that the necessary Python libraries (`pyodbc`, `tkinter`, `tkcalendar`) are installed.

- **Issue: No Available Rooms**
  - Ensure that rooms are available for the selected dates and that the `room_status` for available rooms is set to 1 (available).

- **Issue: Application Crashes/Freezes**
  - Check the logs in the terminal or console for error messages and debug accordingly.

## Contributors

- **Youssef Ahmed**: Developer and Project Lead.

If you have any questions or would like to contribute to this project, please feel free to open an issue or submit a pull request.
