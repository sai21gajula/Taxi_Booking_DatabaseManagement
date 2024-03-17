-- Change the delimiter
DELIMITER $$

-- Trigger to Update Driver Rating After Customer Feedback
CREATE TRIGGER update_driver_rating
AFTER INSERT ON Rating
FOR EACH ROW
BEGIN
  UPDATE Driver
  SET rating = (SELECT AVG(customer_rating)
                FROM Rating
                JOIN Completed_trips ON Rating.Completed_tripscompleted_id = Completed_trips.completed_id
                WHERE Completed_trips.Trip_requeststrip_id = NEW.Completed_tripscompleted_id)
  WHERE driver_id = (SELECT Trip_requeststrip_id FROM Completed_trips WHERE completed_id = NEW.Completed_tripscompleted_id);
END
$$
DELIMITER ;

DELIMITER $$
-- Trigger to Record Cancellation in Incomplete_trips
CREATE TRIGGER record_incomplete_trip
AFTER UPDATE ON Trip_requests
FOR EACH ROW
BEGIN
  IF OLD.request_status = 'Booked' AND NEW.request_status = 'Cancelled' THEN
    INSERT INTO Incomplete_trips (booking_time, cancel_time, reason, Trip_requeststrip_id)
    VALUES (NEW.request_time, CURRENT_TIMESTAMP, 'Cancelled by user', NEW.trip_id);
  END IF;
END;
$$
DELIMITER ;



DELIMITER $$
-- Trigger to Apply Surge Pricing
CREATE TRIGGER apply_surge_pricing
BEFORE INSERT ON Trip_requests
FOR EACH ROW
BEGIN
  IF HOUR(NEW.request_time) BETWEEN 17 AND 20 THEN
    SET NEW.estfare = NEW.estfare * 1.2; -- Assuming a 20% surge
  END IF;
END;

$$
DELIMITER ;


  

DELIMITER $$
-- Trigger for Auto-archiving Completed Trips
CREATE TRIGGER archive_completed_trips
BEFORE INSERT ON Completed_trips
FOR EACH ROW
BEGIN
  INSERT INTO Completed_trips_archive
  SELECT * FROM Completed_trips
  WHERE YEAR(dropoff_time) < YEAR(CURRENT_DATE) - 1;
END;

$$
DELIMITER ;
