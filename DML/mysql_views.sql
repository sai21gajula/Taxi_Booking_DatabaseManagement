
-- View to display detailed information about each trip
CREATE VIEW Detailed_Trip_Info AS
SELECT 
    t.trip_id, 
    t.pickup_loc, 
    t.dropoff_loc, 
    t.distance, 
    t.estfare, 
    t.request_time, 
    d.driver_first_name, 
    d.driver_last_name, 
    c.customer_first_name, 
    c.customer_last_name
FROM 
    Trip_requests t
JOIN 
    Driver d ON t.Pickup_time_estimationDriverdriver_id = d.driver_id
JOIN 
    Rider_details r ON t.Rider_detailsrider_id = r.rider_id
JOIN 
    Customer_details c ON r.Customer_detailscustomer_id = c.customer_id;

-- View to summarize completed trips and earnings by driver
CREATE VIEW Driver_Summary AS
SELECT 
    d.driver_id, 
    d.driver_first_name, 
    d.driver_last_name, 
    COUNT(ct.completed_id) AS total_trips, 
    SUM(ct.actfare) AS total_earnings
FROM 
    Driver d
JOIN 
    Completed_trips ct ON d.driver_id = ct.Trip_requeststrip_id
GROUP BY 
    d.driver_id;

-- View to list all incomplete trips with reasons
CREATE VIEW Incomplete_Trip_Details AS
SELECT 
    it.incomplete_id, 
    it.booking_time, 
    it.cancel_time, 
    it.reason, 
    t.pickup_loc, 
    t.dropoff_loc
FROM 
    Incomplete_trips it
JOIN 
    Trip_requests t ON it.Trip_requeststrip_id = t.trip_id;

-- View for customer feedback and ratings for each completed trip
CREATE VIEW Customer_Feedback AS
SELECT 
    ct.completed_id, 
    r.customer_rating, 
    r.customer_feedback, 
    t.pickup_loc, 
    t.dropoff_loc
FROM 
    Completed_trips ct
JOIN 
    Rating r ON ct.completed_id = r.Completed_tripscompleted_id
JOIN 
    Trip_requests t ON ct.Trip_requeststrip_id = t.trip_id;
