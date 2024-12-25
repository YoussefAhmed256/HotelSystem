import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyodbc
from tkcalendar import DateEntry
from datetime import datetime


class HotelBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Booking Application")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f8ff")

        # Database connection
        self.conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=Youssef;'
            'DATABASE=HotelSystem;'
        )
        self.cursor = self.conn.cursor()

        # Initialize shared data
        self.guest_data = {}
        self.services_data = {}
        self.rooms_data = {}

        # Load services from database
        self.services = self.load_services()

        self.create_home_page()

    def load_services(self):
        """Load services from database"""
        self.cursor.execute("SELECT id, name, price FROM services")
        return {row.name: {"id": row.id, "price": row.price} for row in self.cursor.fetchall()}

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_home_page(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="Welcome to Luxury Hotel",
            font=("Helvetica", 32, "bold"),
            bg="#f0f8ff",
            fg="#34495e"
        ).pack(pady=20)

        description = """Experience luxury like never before at our 5-star hotel.

        • Elegant rooms with stunning views
        • World-class dining experiences
        • State-of-the-art fitness center and spa
        • 24/7 concierge service
        • Infinity pool
        • Premium facilities"""

        tk.Label(
            self.root,
            text=description,
            font=("Helvetica", 14),
            bg="#f0f8ff",
            fg="#34495e",
            justify="left"
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Book Now",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#3498db",
            command=self.create_guest_data_page,
            width=15,
            height=2
        ).pack(pady=30)

    def create_guest_data_page(self):
        self.clear_window()
        tk.Label(self.root, text="Guest Details", font=("Helvetica", 24, "bold"), bg="#f0f8ff", fg="#34495e").pack(
            pady=20)

        form_frame = tk.Frame(self.root, bg="#f0f8ff")
        form_frame.pack(pady=10)

        fields = [
            ("First Name*", tk.StringVar()),
            ("Last Name*", tk.StringVar()),
            ("Email*", tk.StringVar()),
            ("Phone*", tk.StringVar()),
            ("SSN*", tk.StringVar()),
        ]

        self.guest_data = {name.replace('*', ''): var for name, var in fields}

        for i, (label, var) in enumerate(fields):
            tk.Label(form_frame, text=label, font=("Helvetica", 14), bg="#f0f8ff", fg="#34495e").grid(row=i, column=0,
                                                                                                      sticky="e",
                                                                                                      padx=20, pady=5)
            tk.Entry(form_frame, textvariable=var, font=("Helvetica", 14)).grid(row=i, column=1, padx=20, pady=5)

        tk.Label(form_frame, text="* Required fields", font=("Helvetica", 10), bg="#f0f8ff", fg="red").grid(
            row=len(fields), column=0, columnspan=2, pady=10)

        button_frame = tk.Frame(self.root, bg="#f0f8ff")
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Back to Home",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#e67e22",
            command=self.create_home_page
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Next",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#3498db",
            command=self.validate_guest_data
        ).pack(side="left", padx=10)

    def validate_guest_data(self):
        for key, var in self.guest_data.items():
            if not var.get():
                messagebox.showerror("Error", f"{key} is required.")
                return

        if '@' not in self.guest_data['Email'].get():
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        self.create_services_page()

    def create_services_page(self):
        self.clear_window()
        tk.Label(self.root, text="Select Additional Services", font=("Helvetica", 24, "bold"), bg="#f0f8ff",
                 fg="#34495e").pack(pady=20)

        services_frame = tk.Frame(self.root, bg="#f0f8ff")
        services_frame.pack(pady=10)

        self.services_data = {}
        for i, (service_name, service_info) in enumerate(self.services.items()):
            var = tk.BooleanVar()
            self.services_data[service_name] = var
            tk.Checkbutton(
                services_frame,
                text=f"{service_name} (${service_info['price']:.2f})",
                variable=var,
                font=("Helvetica", 14),
                bg="#f0f8ff",
                fg="#34495e"
            ).grid(row=i // 2, column=i % 2, sticky="w", padx=20, pady=5)

        button_frame = tk.Frame(self.root, bg="#f0f8ff")
        button_frame.pack(side="bottom", pady=20)

        tk.Button(
            button_frame,
            text="Back",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#e67e22",
            command=self.create_guest_data_page
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Next",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#3498db",
            command=self.create_rooms_data_page
        ).pack(side="left", padx=10)

    def get_available_rooms(self, check_in, check_out, room_type):
        """Get number of available rooms for a specific room type and dates"""
        self.cursor.execute("""
            SELECT COUNT(r.id) 
            FROM room r
            JOIN room_class rc ON r.room_class_id = rc.id
            WHERE rc.name = ?
            AND r.id NOT IN (
                SELECT br.room_id
                FROM booking_room br
                JOIN booking b ON br.booking_id = b.id
                WHERE (? < b.checkoutdate AND ? > b.checkindate)
            )
            AND r.status_id = 1
        """, room_type, check_in, check_out)
        return self.cursor.fetchone()[0]

    def create_rooms_data_page(self):
        self.clear_window()
        tk.Label(self.root, text="Room Details", font=("Helvetica", 24, "bold"), bg="#f0f8ff", fg="#34495e").pack(
            pady=20)

        form_frame = tk.Frame(self.root, bg="#f0f8ff")
        form_frame.pack(pady=10)

        self.rooms_data = {
            "Check-in Date": tk.StringVar(),
            "Check-out Date": tk.StringVar(),
            "Room Type": tk.StringVar(),
            "Number of Rooms": tk.IntVar(value=1),
            "Number of Adults": tk.IntVar(value=1),
            "Number of Children": tk.IntVar(value=0),
        }

        # Date Selection
        check_in_date = DateEntry(
            form_frame,
            textvariable=self.rooms_data["Check-in Date"],
            font=("Helvetica", 14),
            date_pattern='yyyy-mm-dd',
            mindate=datetime.now()
        )
        check_in_date.grid(row=0, column=1, padx=20, pady=5)

        check_out_date = DateEntry(
            form_frame,
            textvariable=self.rooms_data["Check-out Date"],
            font=("Helvetica", 14),
            date_pattern='yyyy-mm-dd',
            mindate=datetime.now()
        )
        check_out_date.grid(row=1, column=1, padx=20, pady=5)

        # Room Type Selection
        self.cursor.execute("SELECT name FROM room_class")
        room_types = [row.name for row in self.cursor.fetchall()]
        room_type_combo = ttk.Combobox(
            form_frame,
            textvariable=self.rooms_data["Room Type"],
            values=room_types,
            state="readonly",
            font=("Helvetica", 14)
        )
        room_type_combo.grid(row=2, column=1, padx=20, pady=5)
        if room_types:
            room_type_combo.set(room_types[0])

        # Available Rooms Label
        available_rooms_label = tk.Label(form_frame, text="", font=("Helvetica", 12), bg="#f0f8ff", fg="#27ae60")
        available_rooms_label.grid(row=2, column=2, padx=20, pady=5)

        def update_available_rooms(*args):
            try:
                check_in = self.rooms_data["Check-in Date"].get()
                check_out = self.rooms_data["Check-out Date"].get()
                room_type = self.rooms_data["Room Type"].get()

                if check_in and check_out and room_type:
                    available = self.get_available_rooms(check_in, check_out, room_type)
                    available_rooms_label.config(
                        text=f"Available: {available} rooms",
                        fg="#27ae60" if available > 0 else "#e74c3c"
                    )
                    # Update max value for number of rooms spinbox
                    rooms_spinbox.config(to=min(5, available))
            except Exception as e:
                print(f"Error updating available rooms: {e}")

        # Bind update function to variable changes
        self.rooms_data["Check-in Date"].trace('w', update_available_rooms)
        self.rooms_data["Check-out Date"].trace('w', update_available_rooms)
        self.rooms_data["Room Type"].trace('w', update_available_rooms)

        # Labels and Spinboxes
        labels = ["Check-in Date*", "Check-out Date*", "Room Type*", "Number of Rooms*",
                  "Number of Adults", "Number of Children"]

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, font=("Helvetica", 14), bg="#f0f8ff", fg="#34495e").grid(
                row=i, column=0, sticky="e", padx=20, pady=5)

        rooms_spinbox = tk.Spinbox(
            form_frame,
            from_=1,
            to=5,
            textvariable=self.rooms_data["Number of Rooms"],
            font=("Helvetica", 14)
        )
        rooms_spinbox.grid(row=3, column=1, padx=20, pady=5)

        tk.Spinbox(
            form_frame,
            from_=1,
            to=10,
            textvariable=self.rooms_data["Number of Adults"],
            font=("Helvetica", 14)
        ).grid(row=4, column=1, padx=20, pady=5)

        tk.Spinbox(
            form_frame,
            from_=0,
            to=10,
            textvariable=self.rooms_data["Number of Children"],
            font=("Helvetica", 14)
        ).grid(row=5, column=1, padx=20, pady=5)

        tk.Label(form_frame, text="* Required fields", font=("Helvetica", 10), bg="#f0f8ff", fg="red").grid(
            row=6, column=0, columnspan=2, pady=10)

        button_frame = tk.Frame(self.root, bg="#f0f8ff")
        button_frame.pack(side="bottom", pady=20)

        tk.Button(
            button_frame,
            text="Back",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#e67e22",
            command=self.create_services_page
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Submit",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#27ae60",
            command=self.submit_booking
        ).pack(side="left", padx=10)

    def update_room_status(self, booking_id, room_type, num_rooms, check_in, check_out):
        """Update room status and create booking_room entries"""
        # First get the available room IDs
        self.cursor.execute("""
            SELECT TOP (?) r.id
            FROM room r
            JOIN room_class rc ON r.room_class_id = rc.id
            WHERE rc.name = ?
            AND r.id NOT IN (
                SELECT br.room_id
                FROM booking_room br
                JOIN booking b ON br.booking_id = b.id
                WHERE (? < b.checkoutdate AND ? > b.checkindate)
            )
            AND r.status_id = 1
        """, num_rooms, room_type, check_in, check_out)

        room_ids = [row.id for row in self.cursor.fetchall()]

        if len(room_ids) < num_rooms:
            raise ValueError(f"Not enough available rooms of type {room_type}")

        # Update room status to occupied (status_id = 2)
        for room_id in room_ids:
            self.cursor.execute("""
                UPDATE room 
                SET status_id = 2 
                WHERE id = ?
            """, room_id)

            self.cursor.execute("""
                INSERT INTO booking_room (booking_id, room_id)
                VALUES (?, ?)
            """, booking_id, room_id)
    def calculate_total_price(self):
        # Get room price
        self.cursor.execute("SELECT price FROM room_class WHERE name = ?", self.rooms_data["Room Type"].get())
        room_price = self.cursor.fetchone().price

        # Calculate number of days
        checkin = datetime.strptime(self.rooms_data["Check-in Date"].get(), '%Y-%m-%d')
        checkout = datetime.strptime(self.rooms_data["Check-out Date"].get(), '%Y-%m-%d')
        num_days = (checkout - checkin).days

            # Calculate room total
        room_total = room_price * self.rooms_data["Number of Rooms"].get() * num_days

            # Calculate services total
        services_total = sum(
            self.services[service]["price"] * num_days
            for service, var in self.services_data.items()
            if var.get()
        )

        return room_total + services_total

    def submit_booking(self):
            # Validate required fields
        if not all([
            self.rooms_data["Check-in Date"].get(),
            self.rooms_data["Check-out Date"].get(),
            self.rooms_data["Room Type"].get(),
            self.rooms_data["Number of Rooms"].get()
        ]):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        try:
                # Insert guest first to get guest_id
            self.cursor.execute("""
                INSERT INTO guest (ssn, fname, lname, email, phone)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?)
            """,
                                self.guest_data["SSN"].get(),
                                self.guest_data["First Name"].get(),
                                self.guest_data["Last Name"].get(),
                                self.guest_data["Email"].get(),
                                self.guest_data["Phone"].get()
                                )

                # Get the guest ID immediately after insert
            guest_id = self.cursor.fetchval()

            if not guest_id:
                raise ValueError("Failed to insert guest data")

                # Calculate total price
            total_price = self.calculate_total_price()

                # Insert booking with the obtained guest_id
            self.cursor.execute("""
                INSERT INTO booking 
                (guest_id, checkindate, checkoutdate, number_of_rooms, num_adults, num_children, booking_amount)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                                guest_id,
                                self.rooms_data["Check-in Date"].get(),
                                self.rooms_data["Check-out Date"].get(),
                                self.rooms_data["Number of Rooms"].get(),
                                self.rooms_data["Number of Adults"].get(),
                                self.rooms_data["Number of Children"].get(),
                                total_price
                                )

                # Get the booking ID immediately after insert
            booking_id = self.cursor.fetchval()

            if not booking_id:
                raise ValueError("Failed to insert booking data")

                # Update room status and create booking_room entries
            self.update_room_status(
                booking_id,
                self.rooms_data["Room Type"].get(),
                self.rooms_data["Number of Rooms"].get(),
                self.rooms_data["Check-in Date"].get(),
                self.rooms_data["Check-out Date"].get()
            )

                # Insert selected services
            for service_name, var in self.services_data.items():
                if var.get():
                    self.cursor.execute("""
                        INSERT INTO booking_service (booking_id, service_id) 
                        VALUES (?, ?)
                    """,
                                        booking_id,
                                        self.services[service_name]["id"]
                                        )

                # Commit all changes
            self.conn.commit()

                # Show success message
            messagebox.showinfo(
                "Booking Successful",
                f"Your booking has been confirmed!\nTotal Price: ${total_price:.2f}\n\n" +
                f"Booking Details:\n" +
                f"---------------\n" +
                f"Guest: {self.guest_data['First Name'].get()} {self.guest_data['Last Name'].get()}\n" +
                f"Check-in: {self.rooms_data['Check-in Date'].get()}\n" +
                f"Check-out: {self.rooms_data['Check-out Date'].get()}\n" +
                f"Room Type: {self.rooms_data['Room Type'].get()}\n" +
                f"Number of Rooms: {self.rooms_data['Number of Rooms'].get()}\n" +
                f"Guests: {self.rooms_data['Number of Adults'].get()} Adults, {self.rooms_data['Number of Children'].get()} Children\n\n" +
                f"Selected Services:\n" +
                f"-----------------\n" +
                f"{', '.join(service for service, var in self.services_data.items() if var.get())}"
            )

                # Return to home page
            self.create_home_page()

        except Exception as e:
                # Rollback transaction in case of any error
            self.conn.rollback()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            print(f"Error details: {e}")

    def __del__(self):
        """Cleanup database connection"""
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelBookingApp(root)
    root.mainloop()