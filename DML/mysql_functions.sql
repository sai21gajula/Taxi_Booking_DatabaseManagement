
-- Function to calculate total fare with surge pricing
DELIMITER //
CREATE FUNCTION CalculateTotalFare(distance FLOAT, isSurge BOOLEAN) RETURNS FLOAT
DETERMINISTIC
BEGIN
  DECLARE baseFare FLOAT;
  DECLARE perMileRate FLOAT;
  DECLARE totalFare FLOAT;
  SET baseFare = 5.0; -- Base fare for the trip
  SET perMileRate = 2.0; -- Rate per mile
  SET totalFare = baseFare + (distance * perMileRate);
  IF isSurge THEN
    SET totalFare = totalFare * 1.2; -- Applying a 20% surge
  END IF;
  RETURN totalFare;
END //
DELIMITER ;


-- Function to count total trips by a driver
DELIMITER //
CREATE FUNCTION TotalTripsByDriver(driverId INT) RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE totalTrips INT;
  SELECT COUNT(*) INTO totalTrips FROM Completed_trips WHERE Trip_requeststrip_id = driverId;
  RETURN totalTrips;
END //
DELIMITER ;

-- Function to calculate average driver rating
DELIMITER //
CREATE FUNCTION AverageDriverRating(driverId INT) RETURNS FLOAT
DETERMINISTIC
BEGIN
  DECLARE avgRating FLOAT;
  SELECT AVG(customer_rating) INTO avgRating
  FROM Rating
  JOIN Completed_trips ON Rating.Completed_tripscompleted_id = Completed_trips.completed_id
  WHERE Completed_trips.Trip_requeststrip_id = driverId;
  RETURN avgRating;
END //
DELIMITER ;
