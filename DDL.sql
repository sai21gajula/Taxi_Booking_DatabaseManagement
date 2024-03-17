use taxi_booking;

CREATE TABLE Trip_requests 
(trip_id int NOT NULL AUTO_INCREMENT, 
pickup_loc varchar(255) NOT NULL, 
dropoff_loc varchar(255) NOT NULL, 
distance float NOT NULL, 
estfare float NOT NULL, 
request_time timestamp NOT NULL, 
Pickup_time_estimationpickup_id int NOT NULL, 
Rider_detailsrider_id int NOT NULL, 
pickup_time_estimate int NOT NULL, 
Pickup_time_estimationDriverdriver_id int NOT NULL, 
request_status VARCHAR(255) NOT NULL,
PRIMARY KEY (trip_id));

CREATE TABLE Incomplete_trips 
(incomplete_id int NOT NULL AUTO_INCREMENT, 
booking_time timestamp NOT NULL, 
cancel_time timestamp NOT NULL, 
reason varchar(255) NOT NULL, 
Trip_requeststrip_id int NOT NULL, 
PRIMARY KEY (incomplete_id));

CREATE TABLE Completed_trips 
(completed_id int NOT NULL AUTO_INCREMENT, 
driver_arrived_at timestamp NOT NULL, 
pickup_time timestamp NOT NULL, 
dropoff_time timestamp NOT NULL, 
duration int NOT NULL, 
actfare float NOT NULL, 
tip float NOT NULL, 
Trip_requeststrip_id int NOT NULL, 
PRIMARY KEY (completed_id));

CREATE TABLE Rating 
(customer_rating int CHECK (customer_rating >= 1 AND customer_rating <= 5), 
customer_feedback varchar(2000), 
Completed_tripscompleted_id int NOT NULL, 
PRIMARY KEY (Completed_tripscompleted_id));

CREATE TABLE Offers 
(offer_id int NOT NULL AUTO_INCREMENT, 
promo_code varchar(255) UNIQUE, 
promo_discount float, 
Rider_detailsrider_id int NOT NULL, 
PRIMARY KEY (offer_id));

CREATE TABLE Surge 
(surge_id int NOT NULL AUTO_INCREMENT, 
surge_cost float, 
Trip_requeststrip_id int NOT NULL, 
PRIMARY KEY (surge_id));

CREATE TABLE Driver 
(driver_id int NOT NULL AUTO_INCREMENT, 
driver_first_name varchar(255) NOT NULL, 
driver_last_name varchar(255) NOT NULL, 
working_hours int NOT NULL, 
license_no varchar(10) NOT NULL UNIQUE, 
phone_num varchar(15) NOT NULL, 
driver_email varchar(50) NOT NULL,
driver_pass varchar(255) NOT NULL, 
rating float, 
PRIMARY KEY (driver_id));

CREATE TABLE Rider_details 
(rider_id int NOT NULL AUTO_INCREMENT, 
num_riders int NOT NULL CHECK (num_riders >= 0), 
Customer_detailscustomer_id int NOT NULL, 
PRIMARY KEY (rider_id));

CREATE TABLE Customer_details 
(customer_id int NOT NULL AUTO_INCREMENT,
Customer_email varchar(50) NOT NULL,
Customer_pass varchar(255) NOT NULL, 
customer_first_name varchar(255) NOT NULL, 
customer_last_name varchar(255) NOT NULL, 
phone_num varchar(15) NOT NULL, 
date_of_birth date NOT NULL,
PRIMARY KEY (customer_id));

CREATE TABLE Cab_details 
(licence_plate_no varchar(20) NOT NULL UNIQUE, 
model varchar(50) NOT NULL, 
brand varchar(50) NOT NULL, 
max_seats int NOT NULL, 
manufacture_year int NOT NULL, 
Driverdriver_id int NOT NULL, 
PRIMARY KEY (licence_plate_no));

CREATE TABLE Car_records 
(service_id int NOT NULL AUTO_INCREMENT, 
insurance_status varchar(15) NOT NULL, 
service_date int NOT NULL, 
service_records varchar(255), 
Cab_detailslicence_plate_no varchar(20) NOT NULL UNIQUE, 
PRIMARY KEY (service_id));

CREATE TABLE Pickup_time_estimation 
(pickup_id int NOT NULL, 
driver_location varchar(255) NOT NULL, 
Driverdriver_id int NOT NULL, 
PRIMARY KEY (pickup_id, Driverdriver_id));

CREATE TABLE Payment_info (
    payment_info_id INT NOT NULL AUTO_INCREMENT,
    card_no VARCHAR(20) NOT NULL,
    cvv INT NOT NULL,
    exp_date DATE NOT NULL,
    card_type VARCHAR(20) NOT NULL,
    billing_address_street VARCHAR(255) NOT NULL,
    billing_address_apt VARCHAR(255) NOT NULL,
    billing_address_city VARCHAR(255) NOT NULL,
    billing_address_zip INT NOT NULL,
    PRIMARY KEY (payment_info_id)
);

CREATE TABLE Payment_method (
    payment_id INT NOT NULL AUTO_INCREMENT,
    payment_info_id INT NOT NULL,
    acc_type VARCHAR(50) NOT NULL,
    Completed_tripscompleted_id INT NOT NULL,
    FOREIGN KEY (payment_info_id) REFERENCES Payment_info (payment_info_id),
    FOREIGN KEY (Completed_tripscompleted_id) REFERENCES Completed_trips (completed_id),
    PRIMARY KEY (payment_id)
);


ALTER TABLE Car_records ADD CONSTRAINT service_details FOREIGN KEY (Cab_detailslicence_plate_no) REFERENCES Cab_details (licence_plate_no);
ALTER TABLE Cab_details ADD CONSTRAINT owns FOREIGN KEY (Driverdriver_id) REFERENCES Driver (driver_id);
ALTER TABLE Pickup_time_estimation ADD CONSTRAINT has FOREIGN KEY (Driverdriver_id) REFERENCES Driver (driver_id);
ALTER TABLE Trip_requests ADD CONSTRAINT pickup_time_estimator FOREIGN KEY (Pickup_time_estimationpickup_id, Pickup_time_estimationDriverdriver_id) REFERENCES Pickup_time_estimation (pickup_id, Driverdriver_id);
ALTER TABLE Rider_details ADD CONSTRAINT riders FOREIGN KEY (Customer_detailscustomer_id) REFERENCES Customer_details (customer_id);
ALTER TABLE Offers ADD CONSTRAINT discount FOREIGN KEY (Rider_detailsrider_id) REFERENCES Rider_details (rider_id);
ALTER TABLE Surge ADD CONSTRAINT surge_fee FOREIGN KEY (Trip_requeststrip_id) REFERENCES Trip_requests (trip_id);
ALTER TABLE Trip_requests ADD CONSTRAINT trip FOREIGN KEY (Rider_detailsrider_id) REFERENCES Rider_details (rider_id);
ALTER TABLE Payment_method ADD CONSTRAINT payment FOREIGN KEY (Completed_tripscompleted_id) REFERENCES Completed_trips (completed_id);
ALTER TABLE Incomplete_trips ADD CONSTRAINT FKIncomplete446588 FOREIGN KEY (Trip_requeststrip_id) REFERENCES Trip_requests (trip_id);
ALTER TABLE Completed_trips ADD CONSTRAINT FKCompleted_494052 FOREIGN KEY (Trip_requeststrip_id) REFERENCES Trip_requests (trip_id);
ALTER TABLE Rating ADD CONSTRAINT giving_rating FOREIGN KEY (Completed_tripscompleted_id) REFERENCES Completed_trips (completed_id);
