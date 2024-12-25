
# Hotel Management System

This is a Hotel Management System (HMS) designed to manage guest bookings, room availability, and services within a hotel. The project consists of a database backend and a GUI for user interaction. 

## Table of Contents
1. [Project Overview](#project-overview)
2. [Database Schema](#database-schema)
3. [GUI Overview](#gui-overview)
4. [Screenshots](#screenshots)
5. [Installation](#installation)
6. [Usage](#usage)
7. [License](#license)

---

## Project Overview

The Hotel Management System provides a simple and effective way to manage hotel operations including:

- Guest information management
- Room availability and status tracking
- Booking management (with check-in and check-out dates)
- Service management for additional amenities (e.g., breakfast, spa, gym)
- Room and service booking

---

## Database Schema

The database is built using Microsoft SQL Server and contains several tables to store information related to guests, rooms, bookings, and services.

### Tables:

1. **Guest**: Stores guest details (SSN, name, email, phone).
2. **Floor**: Stores floor information for the hotel.
3. **Room**: Stores room details, including floor, room class, and status.
4. **Booking**: Records booking details, including the guest, check-in/check-out dates, number of rooms, and total amount.
5. **Booking_Room**: Represents the many-to-many relationship between bookings and rooms.
6. **Room_Class**: Contains information about room classes (Standard, Deluxe, Suite) and their prices.
7. **Room_Status**: Defines room statuses (e.g., Available, Occupied, Maintenance).
8. **Services**: Stores services offered by the hotel, such as breakfast, spa, etc.
9. **Booking_Service**: Represents the many-to-many relationship between bookings and services.

### Key Features:

- **Triggers**: Updates room status automatically after a guest checks out.
- **Stored Procedures**: Retrieves available rooms based on check-in and check-out dates.

### Database Diagram

<!-- Place your database diagram image here -->
![Database Diagram]([DataBase/Youssef.HotelSystem - Diagram_0_ - Microsoft SQL Server Management Studio 12_25_2024 10_25_14 PM.png](https://github.com/YoussefAhmed256/HotelSystem/blob/main/DataBase/Youssef.HotelSystem%20-%20Diagram_0_%20-%20Microsoft%20SQL%20Server%20Management%20Studio%2012_25_2024%2010_25_14%20PM.png?raw=true))

---

## GUI Overview

The Hotel Management System features a user-friendly Graphical User Interface (GUI) for interacting with the database. The GUI allows the user to:

- Add, update, and view guest information
- Make and manage room bookings
- View available rooms and services
- Manage room statuses and services

### Key Features:
- **Login Screen**: Secure login for hotel staff.
- **Dashboard**: Main interface for managing hotel operations.
- **Booking Management**: Allows users to search for available rooms and create bookings.
- **Room Management**: Allows users to update room statuses (e.g., available, occupied, under maintenance).
- **Service Management**: Manage hotel services that can be added to bookings.

### Technologies Used:
- **Backend**: C# and .NET for handling database operations and business logic.
- **Frontend**: Windows Forms or WPF for the graphical user interface.

---

## Screenshots

Below are some screenshots of the program in action.

### Home Page
![Login Screen]([path_to_your_screenshot.png](https://github.com/YoussefAhmed256/HotelSystem/blob/main/GUI/HomePage.png))

### Guest Data
![Dashboard]([path_to_your_screenshot.png](https://github.com/YoussefAhmed256/HotelSystem/blob/main/GUI/GuestData.png))

### Service Booking
![Booking Management]([path_to_your_screenshot.png](https://github.com/YoussefAhmed256/HotelSystem/blob/main/GUI/Service%20Booking.png))

### Room Availability
![Room Availability]([path_to_your_screenshot.png](https://github.com/YoussefAhmed256/HotelSystem/blob/main/GUI/RoomDetails.png))

### booking confirmation
![Booking Management]([path_to_your_screenshot.png](https://github.com/YoussefAhmed256/HotelSystem/blob/main/GUI/Booking%20Confirmation.png))

---

## Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/your-username/HotelManagementSystem.git
   ```

2. **Install Dependencies**:
   - Ensure you have .NET Core or .NET Framework installed on your machine.
   - Install Microsoft SQL Server or any compatible SQL database.

3. **Set up the Database**:
   - Run the SQL scripts provided (`hotel_system.sql`) to create the necessary tables and relationships in your SQL database.
   - Adjust the connection string in the application’s settings to match your database configuration.

4. **Run the Application**:
   - Open the solution file (`HotelManagementSystem.sln`) in Visual Studio or your preferred C# IDE.
   - Build and run the application.

---

## Usage

1. **Login**: Use the credentials provided by the system administrator to log into the hotel management system.
2. **Manage Guests**: Add or update guest information.
3. **Book Rooms**: Search for available rooms and create new bookings.
4. **Track Room Statuses**: Update the status of rooms based on occupancy or maintenance.
5. **Services**: Add services (e.g., breakfast, spa) to bookings.
6. **View Reports**: Generate reports based on bookings and services.

---

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
