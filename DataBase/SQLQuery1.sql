create database HotelSystem

use HotelSystem

create table guest (
  id int primary key identity(1,1),
  ssn varchar (15) not null,
  fname nvarchar(15) not null,
  lname nvarchar(15) not null,
  email varchar(50) not null,
  phone varchar(15) not null
);

ALTER TABLE guest ADD CONSTRAINT email_check CHECK (CHARINDEX('@', email) > 0);

create table floor(
  id int primary key identity(1,1),
  floor_number int
);

create table room (
  id int primary key identity(1,1),
  floor_id int references floor (id) not null,
  room_class_id int references room_class (id) not null ,
  status_id int references room_status (id) not null,
  room_number int not null
);

create table booking (
  id int primary key identity(1,1),
  guest_id int references guest (id) not null,
  checkindate date not null,
  checkoutdate date not null,
  number_of_rooms int not null,
  num_adults int,
  num_children int,
  booking_amount decimal(10,2),
  payment_status varchar(10) default 'pinding'
);

alter table booking add numberofdays as DATEDIFF(day, checkindate, checkoutdate)
alter table booking add constraint c2 check (checkindate < checkoutdate);

create table booking_room (
  booking_id int references booking (id),
  room_id int references room (id),
  primary key (booking_id, room_id)
);

create table room_class (
  id int primary key identity(1,1),
  name varchar(15),
  price decimal(10,2)
);

create table room_status (
  id int primary key identity(1,1),
  name varchar(15) default 'available'
);

-- Create trigger to update room status after checkout
CREATE TRIGGER UpdateRoomStatusAfterCheckout
ON booking
AFTER UPDATE
AS
BEGIN
    IF UPDATE(checkoutdate)
    BEGIN
        -- Update rooms to available where the booking has ended
        UPDATE room
        SET status_id = 1
        WHERE id IN (
            SELECT br.room_id
            FROM booking_room br
            JOIN inserted i ON br.booking_id = i.id
            WHERE i.checkoutdate < GETDATE()
        );
    END
END;


CREATE PROCEDURE get_available_rooms
    @checkindate DATE,
    @checkoutdate DATE
AS
BEGIN
    SELECT r.id, r.room_number, r.floor_id, r.room_class_id
    FROM room r
    WHERE NOT EXISTS (
        SELECT 1
        FROM booking_room br
        INNER JOIN booking b ON br.booking_id = b.id
        WHERE br.room_id = r.id
        AND b.checkindate < @checkoutdate  
        AND b.checkoutdate > @checkindate  
    );
END;


create table services (
  id int primary key identity(1,1),
  name varchar(50) not null ,
  price decimal(10,2) not null
);

create table booking_service (
  booking_id int references booking (id),
  service_id int references services (id),
  primary key (booking_id, service_id)
);

INSERT INTO floor (floor_number)
VALUES 
(1), 
(2), 
(3), 
(4);

INSERT INTO room_class (name, price)
VALUES 
('Standard', 100.00),
('Deluxe', 150.00),
('Suite', 200.00);

INSERT INTO room_status (name)
VALUES 
('available'), 
('occupied'), 
('maintenance');

INSERT INTO room (floor_id, room_class_id, status_id, room_number)
VALUES 
(1, 1, 1, 101), 
(2, 2, 1, 202), 
(3, 3, 1, 303),
(1, 1, 1, 102),
(1, 2, 1, 103),
(2, 3, 1, 201),
(2, 1, 1, 202),
(3, 2, 1, 301),
(3, 3, 1, 302),
(4, 1, 1, 401),
(4, 2, 1, 402),
(4, 3, 1, 403);

INSERT INTO services (name, price)
VALUES 
('Breakfast', 20.00), 
('Spa', 50.00), 
('Airport Pickup', 30.00),
('Launch', 20.00),
('Dinner', 50.00), 
('Snaks', 50.00), 
('Gym Access', 25.00),
('Laundry', 30.00),
('Room Service', 10.00),
('Wi-Fi', 5.00),
('Parking', 20.00),
('Swimming Pool Access', 30.00),
('Mini Bar', 35.00);