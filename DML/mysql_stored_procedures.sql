
-- Stored Procedure to Calculate Estimated Fare
DELIMITER //
CREATE PROCEDURE Calculate_Estimated_Fare(IN distance FLOAT, OUT est_fare FLOAT)
BEGIN
  DECLARE base_fare FLOAT;
  DECLARE per_mile_rate FLOAT;
  SET base_fare = 5.0; -- Base fare for the trip
  SET per_mile_rate = 2.0; -- Rate per mile
  SET est_fare = base_fare + (distance * per_mile_rate);
  -- Check for surge pricing and apply if necessary
  IF HOUR(CURRENT_TIME()) BETWEEN 17 AND 20 THEN
    SET est_fare = est_fare * 1.2; -- Assuming a 20% surge
  END IF;
END //
DELIMITER ;

-- Stored Procedure to Record a New Trip
DELIMITER //
CREATE PROCEDURE Record_New_Trip(IN pickup_loc VARCHAR(255), IN dropoff_loc VARCHAR(255), IN rider_id INT)
BEGIN
  DECLARE distance FLOAT;
  DECLARE est_fare FLOAT;
  DECLARE driver_id INT;
  -- Dummy distance calculation
  SET distance = 10; -- Assume a fixed distance for this example
  CALL Calculate_Estimated_Fare(distance, est_fare);
  -- Select an available driver (dummy selection for this example)
  SET driver_id = (SELECT driver_id FROM Driver LIMIT 1);
  -- Insert the new trip
  INSERT INTO Trip_requests(pickup_loc, dropoff_loc, distance, estfare, request_time, Rider_detailsrider_id, Pickup_time_estimationDriverdriver_id)
  VALUES(pickup_loc, dropoff_loc, distance, est_fare, CURRENT_TIMESTAMP, rider_id, driver_id);
END //
DELIMITER ;

-- Stored Procedure to Update Trip Status
DELIMITER //
CREATE PROCEDURE Update_Trip_Status(IN trip_id INT, IN new_status VARCHAR(50))
BEGIN
  IF new_status = 'Completed' THEN
    -- Update the trip to completed and record the completion details
    UPDATE Trip_requests
    SET status = new_status
    WHERE trip_id = trip_id;
    -- Assume dummy values for completion details
    INSERT INTO Completed_trips(driver_arrived_at, pickup_time, dropoff_time, duration, actfare, tip, Trip_requeststrip_id)
    VALUES(CURRENT_TIMESTAMP, DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 5 MINUTE), DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 30 MINUTE), 25, 30.0, 5.0, trip_id);
  ELSE
    -- Update the trip status for other statuses
    UPDATE Trip_requests
    SET status = new_status
    WHERE trip_id = trip_id;
  END IF;
END //
DELIMITER ;

-- Stored Procedure to Generate Monthly Driver Report
DELIMITER //
CREATE PROCEDURE Monthly_Driver_Report(IN driver_id INT, IN report_month INT, IN report_year INT)
BEGIN
  SELECT driver_id, COUNT(*) AS total_trips, SUM(actfare) AS total_earnings, AVG(rating) AS avg_rating
  FROM Completed_trips
  JOIN Driver ON Completed_trips.Trip_requeststrip_id = Driver.driver_id
  WHERE MONTH(dropoff_time) = report_month AND YEAR(dropoff_time) = report_year AND Driver.driver_id = driver_id
  GROUP BY driver_id;
END //
DELIMITER ;
