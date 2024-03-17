from flask import Flask, render_template, request, redirect, url_for,session
import requests
import pymysql.cursors
import random
import time,json
from datetime import datetime, timedelta  # Add this import at the top of your app.py file
import base64
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure




app = Flask(__name__)
app.secret_key = 'abcdefg'
# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Siri1969' #password
app.config['MYSQL_DB'] = 'taxi_booking'

# Define MySQL connection function
def create_mysql_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Initialize MySQL
mysql = create_mysql_connection()


#Routes
@app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    
    return render_template('login.html', msg=msg)

#session sto
@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        try:
            with mysql.cursor() as cursor:
                # Retrieve user data from the table
                sql = "SELECT * FROM customer_details WHERE customer_first_name = %s AND Customer_pass = %s"
                cursor.execute(sql, (username, password))
                account = cursor.fetchone()

                if account:
                    session['loggedin'] = True
                    session['customer_id'] = account['customer_id']
                    session['username'] = account['customer_first_name']
                    msg = 'Logged in successfully !'
                    return render_template('customer_home.html', msg=msg)
                else:
                    msg = 'Incorrect username / password !'
        except Exception as e:
            return f"An error occurred: {str(e)}"
            print(e)
    return render_template('userlogin.html', msg=msg)

@app.route('/driverlogin', methods=['GET', 'POST'])
def driverlogin():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        total_earnings = 0  # Add this line

        try:
            with mysql.cursor() as cursor:
                # Retrieve user data from the table
                sql = "SELECT * FROM Driver WHERE driver_first_name = %s AND driver_pass = %s"
                cursor.execute(sql, (username, password))
                account = cursor.fetchone()

                if account:
                    session['loggedin'] = True
                    session['driver_id'] = account['driver_id']
                    session['username'] = account['driver_first_name']
                    session['license'] = account['license_no']
                    msg = 'Logged in successfully !'
                else:
                    msg = 'Incorrect username / password !'

                cab_details = None
                car_data = []
                
                driver_id = session.get('driver_id')
                print("driverid -----",driver_id)
                cursor.execute("SELECT * FROM Driver WHERE driver_id = %s", (driver_id,))
                cab_details = cursor.fetchone()
                print(cab_details)
                cursor.execute("SELECT * FROM Cab_details WHERE Driverdriver_id = %s", (driver_id,))
                car_data = cursor.fetchall()
                print(car_data)
                cursor.execute(" SELECT SUM(estfare) AS total_earnings  FROM Trip_requests  WHERE request_status = 'booked'  AND Pickup_time_estimationDriverdriver_id = %s", (driver_id,))
                total_earnings_result = cursor.fetchone()
                if total_earnings_result and total_earnings_result['total_earnings']:
                    total_earnings = total_earnings_result['total_earnings']
                    total_earnings=round(total_earnings,2)

                return render_template('driver_home.html', cab_details=cab_details or {}, data=car_data, total_earnings=total_earnings)
               
        except Exception as e:
            return f"An error occurred: {str(e)}"
       

    return render_template('driverlogin.html', msg=msg)



@app.route('/signupuser', methods=['GET', 'POST'])
def signupuser():
    conn = create_mysql_connection()  # Assuming create_mysql_connection() creates your connection
    with conn.cursor() as cursor:
        if request.method == 'POST':
            username = request.form['username']
            surname = request.form['last_name']
            phn_no = request.form['Phone_num']
            email = request.form['email']
            DOB = request.form['dob']
            password = request.form['password']

            cursor.execute("INSERT INTO Customer_details (customer_first_name, customer_last_name, phone_num, Customer_email, date_of_birth, Customer_pass) VALUES (%s, %s, %s, %s, %s, %s)", (username, surname, phn_no, email, DOB, password))

            conn.commit()  # Commit changes to the database

            return redirect(url_for('login'))
            

    conn.close()  # Close the connection
    return render_template('signupuser.html')

@app.route('/signupdriver', methods=['GET', 'POST'])
def signupdriver():
    conn = create_mysql_connection()  # Assuming create_mysql_connection() creates your connection

    with conn.cursor() as cursor:
        if request.method == 'POST':
            # Get form data
            username = request.form['username']
            surname = request.form['last_name']
            phn_no = request.form['Phone_num']
            email = request.form['email']
            licenseno = request.form['licenseno']
            password = request.form['password']
            hours=random.randint(1, 10)
            # Insert data into MySQL
            cursor.execute("INSERT INTO Driver (driver_first_name, driver_last_name, phone_num, driver_email,driver_pass,license_no,working_hours) VALUES (%s, %s, %s, %s, %s, %s,%s)", (username, surname, phn_no, email,password,licenseno,hours))
            
            conn.commit()  # Commit changes to the database

            return redirect(url_for('login'))

    conn.close()  # Close the connection
    return render_template('signupdriver.html')


@app.route('/customer_home', methods=['GET', 'POST'])
def customer_home():
    conn = create_mysql_connection()  # Assuming create_mysql_connection() creates your connection

    with conn.cursor() as cursor:
        if request.method == 'POST':
            # Get form data

            pickup_loc = request.form['pickup_loc']
            dropoff_loc = request.form['dropoff_loc']
            num_riders = request.form['num_riders']
            Customer_detailscustomer_id=session['customer_id']
            cursor.execute("INSERT INTO Rider_details (num_riders, Customer_detailscustomer_id) VALUES (%s, %s)", (num_riders, Customer_detailscustomer_id))
            sql = "SELECT * FROM Rider_details WHERE Customer_detailscustomer_id = %s"
            cursor.execute(sql, (Customer_detailscustomer_id))
            account_c = cursor.fetchone()
            Rider_detailsrider_id=account_c['rider_id'] 
            Pickup_time_estimationDriverdriver_id=1 #random.randint(1, 1) # we randomly assign a driver 
            pickup_time_estimate=random.randint(1, 10)
            request_status='Booked'


            
            # Generate random distance and time
            #estfare = 0
            # round(random.uniform(5, 100), 2)  # Generating fare between $5 and $100
            pickup_id=random.randint(1, 100000)

            MAPQUEST_API_KEY = 'C3bzjoCsRVywDUaG3vrcwuC3tHK9ZRbX'
            
            from_location = pickup_loc
            to_location = dropoff_loc
            
            if not from_location or not to_location:
                return jsonify({'error': 'Missing parameters'}), 400
            
            url = 'http://www.mapquestapi.com/directions/v2/route'
            params = {
                'key': MAPQUEST_API_KEY,
                'from': from_location,
                'to': to_location
                }

            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get('info', {}).get('statuscode') == 0:
                distance = data['route']['distance']
            else:
                return jsonify({'error': 'Unable to calculate distance'}), 500
          
            args = [distance, 0]

            cursor.execute("SET @est_fare = 0;")
            cursor.execute(f"CALL Calculate_Estimated_Fare({distance}, @est_fare);")
            cursor.execute("SELECT @est_fare;")
            result = cursor.fetchone()

            # est_fare_row = cursor.fetchone()
            est_fare = result['@est_fare']

            # for fare in est_fare_row:
            #     est_fare = fare

            est_fare = float(est_fare)  # Convert string to float
            est_fare = round(est_fare, 2)


            print("========resutls---------",est_fare)
           

            cursor.execute("INSERT INTO Pickup_time_estimation  (pickup_id, driver_location, Driverdriver_id) VALUES (%s,%s,%s)",(pickup_id,'Nearby',Pickup_time_estimationDriverdriver_id));
            cursor.execute("INSERT INTO Trip_requests (pickup_loc, dropoff_loc, distance, estfare, Pickup_time_estimationpickup_id, Rider_detailsrider_id, Pickup_time_estimationDriverdriver_id,pickup_time_estimate, request_time,request_status) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, NOW(),%s)",
               (pickup_loc, dropoff_loc, distance, est_fare, pickup_id, Rider_detailsrider_id, Pickup_time_estimationDriverdriver_id,pickup_time_estimate,request_status))

            
            print("executed") 
            query = "SELECT * FROM Driver d join Cab_details cd ON d.driver_id = cd.Driverdriver_id where d.driver_id = 1"
            cursor.execute(query)

            data = {}  # Initializes 'data' as a dictionary
            data = cursor.fetchone()
            print(type(data))  # Output: <class 'int'>



            data['pickup_loc'] = pickup_loc
            data['dropoff_loc'] = dropoff_loc
            data['estfare'] = est_fare
            data['pickup_time_estimate'] = pickup_time_estimate
            query = "SELECT trip_id FROM Trip_requests where Pickup_time_estimationpickup_id=%s"
            cursor.execute(query, (pickup_id))
            data1 = {} 
            data1 = cursor.fetchone()
            


            print(data1,type(data1))
            trip_id=data1['trip_id']
            print("------trip_id----------------:",trip_id)
            print("------distance----------------:",distance )
            query = "SELECT * from detailed_trip_info where trip_id=%s"
            cursor.execute(query, (trip_id))
            tripdetails_data= cursor.fetchone();  
            #trip_id= data1.trip_id

            data['trip_id'] = trip_id



            conn.commit()  # Commit changes to the database
            return render_template('customer_book.html',data=data)

    conn.close()  # Close the connection
    return render_template('customer_home.html')


@app.route('/customer_review',methods=['GET', 'POST'])
def customer_review():
    conn = create_mysql_connection()  # Assuming create_mysql_connection() creates your connection
    with conn.cursor() as cursor:
        if request.method == 'POST':
            feedback = request.form['c_feedback']
            rating = request.form['c_rating']
            sql="INSERT INTO Rating(customer_rating, customer_feedback,Completed_tripscompleted_id) VALUES(%s,%s,%s)"
            cursor.execute(sql, (feedback,rating,11))
            conn.commit()

            return render_template('customer_home.html', show_popup=True)
     
    return render_template('customer_review.html', show_popup=True)

@app.route('/cancel_ride', methods=['POST'])
def cancel_ride():

    data = json.loads(request.data)
    conn = create_mysql_connection()  # Assuming create_mysql_connection() creates your connection

    with conn.cursor() as cursor:
        # Extract the trip_id and status from the request data
        trip_id = data.get('trip_id')
        status = data.get('status')
        print("-----21212121------",data)
        cursor.execute("UPDATE Trip_requests SET request_status = %s WHERE trip_id = %s",(status,trip_id))
        conn.commit()  # Commit changes to the database
    
    return redirect(url_for('customer_home'))  # Redirect to the payment page

@app.route('/customer_book', methods=[ 'POST'])
def customer_book():
    conn = create_mysql_connection()  # Assuming create_mysql_connection() creates your connection
    data = request.get_json()
    status = data.get('status')
    est_fare=data.get('estfare')
    trip_id=data.get('trip_id')
    
    print("-----21212121------",data)
    # if(status!='cancelled'):
    #     now = datetime.now()
    #     driver_arrived_at = now - timedelta(minutes=random.randint(5, 30))
    #     pickup_time = now
    #     dropoff_time = now + timedelta(minutes=random.randint(15, 60))
    #     duration = (dropoff_time - pickup_time).total_seconds() / 60  # Duration in minutes
    #     tip=random.randint(1,10)
    #     # Insert into database
    #     print(trip_id,driver_arrived_at, pickup_time, dropoff_time, duration, est_fare,tip, trip_id)
    #     with conn.cursor() as cursor:
    #         sql = " INSERT INTO completed_trips_archive (driver_arrived_at, pickup_time, dropoff_time, duration, actfare, tip,Trip_requeststrip_id)  VALUES (%s,%s,  %s, %s,%s, %s, %s) "
    #         cursor.execute(sql, (driver_arrived_at, pickup_time, dropoff_time, duration, est_fare,tip, trip_id))
    #         sql = " INSERT INTO completed_trips (driver_arrived_at, pickup_time, dropoff_time, duration, actfare, tip,Trip_requeststrip_id)  VALUES (%s,%s,  %s, %s,%s, %s, %s) "
    #         cursor.execute(sql, (driver_arrived_at, pickup_time, dropoff_time, duration, est_fare,tip, trip_id))
    #         conn.commit()

    # conn.close()
    return render_template('customer_payment.html',data=data)

# Add a new route for the customer payment page


@app.route('/customer_payment', methods=['GET', 'POST'])
def customer_payment():
    if request.method == 'POST':
        card_no = request.form['card_no']
        cvv = request.form['cvv']
        exp_date = request.form['exp_date']
        card_type = request.form['card_type']
        billing_address_street = request.form['billing_address_street']
        billing_address_apt = request.form['billing_address_apt']
        billing_address_city = request.form['billing_address_city']
        billing_address_zip = request.form['billing_address_zip']
        # Insert data into Payment_info table
        try:
            conn = create_mysql_connection()  # Assuming create_mysql_connection() creates your connection

            with conn.cursor() as cursor:
                sql = "INSERT INTO Payment_info (card_no, cvv, exp_date, card_type, billing_address_street, billing_address_apt, billing_address_city, billing_address_zip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (card_no, cvv, exp_date, card_type, billing_address_street, billing_address_apt, billing_address_city, billing_address_zip))
                conn.commit()

                # Get the inserted payment_info_id
                payment_info_id = cursor.lastrowid

                # # Insert data into Payment_method table
                # sql = "INSERT INTO Payment_method (payment_info_id, acc_type, Completed_tripscompleted_id) VALUES (%s, %s, %s)"
                # cursor.execute(sql, (payment_info_id, card_type, 24))  # Replace '0' with the appropriate Completed_tripscompleted_id
                # conn.commit()

            conn.close()
            return render_template('customer_payment.html', show_popup=True)

        except Exception as e:
            return str(e)  # Handle any exceptions here

    return render_template('customer_payment.html')

@app.route('/driver_home')
def driver_home():
    conn = create_mysql_connection()
    cab_details = None
    car_data = []

    try:
        with conn.cursor() as cursor:
            driver_id = session.get('driver_id')
            print(driver_id)
            cursor.execute("SELECT * FROM Driver WHERE driver_id = %s", (driver_id,))
            cab_details = cursor.fetchone()
            print(cab_details)

            cursor.execute("SELECT * FROM Cab_details WHERE Driverdriver_id = %s", (driver_id,))
            car_data = cursor.fetchall()
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        conn.close()

    return render_template('driver_home.html', cab_details=cab_details or {}, data=car_data)

# @app.route('/driver_home', methods=['GET', 'POST'])
# def driver_home():
#     conn = create_mysql_connection()  # Assuming create_mysql_connection() creates your connection
    
#     with conn.cursor() as cursor:
#         if request.method == 'GET':
#             # Get form data
#             Customer_detailscustomer_id=session['customer_id']
#             driver_id=session['driver_id']
#             #licenseno=session['license']
#             licenseno='JWY2751'
#             sql = "SELECT * FROM Cab_details WHERE licence_plate_no = %s"
#             cursor.execute(sql, (licenseno))
#             cab_details = cursor.fetchone()
            
#             return render_template('driver_home.html', cab_details=cab_details)
#     conn.close()  # Close the connection
#     return render_template('signupdriver.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('login.html')

@app.route('/home')
def home():
    session.pop('username', None)
    return render_template('customer_home.html')
 
@app.route("/display")
def display():
    if 'loggedin' in session:
        with mysql.cursor() as cursor:
            cursor.execute('SELECT * FROM customer_details WHERE customer_id = % s',
                        (session['customer_id'], ))
            account = cursor.fetchone()
        return render_template("display.html", account=account)
    return redirect(url_for('login'))

@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))
 


@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and'address' in request.form and 'city' in request.form and 'country'in request.form and 'postalcode' in request.form and 'organisation' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            organisation = request.form['organisation']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            postalcode = request.form['postalcode']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM accounts WHERE username = % s',
                      (username, ))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE accounts SET username =% s,\
                password =% s, email =% s, organisation =% s, \
                address =% s, city =% s, state =% s, \
                country =% s, postalcode =% s WHERE id =% s', (
                    username, password, email, organisation, 
                  address, city, state, country, postalcode, 
                  (session['id'], ), ))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg=msg)
    return redirect(url_for('login'))

@app.route('/customer_profile')
def profile():

    conn = create_mysql_connection()  # Assuming create_mysql_connection() creates your connection
    username = session.get('username')

    cursor = conn.cursor()

    # Use parameterized query to avoid SQL injection
    query = "SELECT * FROM Customer_details where customer_first_name=%s"
    cursor.execute(query, (username,))

    # Fetch all the results
    Customer_data = cursor.fetchall()
    print(Customer_data)

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    return render_template('customer_profile.html', data = Customer_data)

@app.route('/profile_update', methods=['POST'])
def profile_update():
    try:
        username = session.get('username')

        first_name = request.form['c_first_name']
        last_name = request.form['c_last_name']
        phone_number = request.form['c_phone_number']
        dob = request.form['c_dob']
        email = request.form['c_email']
        conn = create_mysql_connection()  # Assuming create_mysql_connection() creates your connection

        with conn.cursor() as cursor:
            update_query = "UPDATE Customer_details SET customer_first_name = %s, customer_last_name = %s, " \
                           "phone_num = %s, date_of_birth = %s WHERE customer_first_name = %s;"
            cursor.execute(update_query, (first_name, last_name, phone_number, dob, username))
            conn.commit()

        return redirect(url_for('index'))  # Redirect to the profile page or any other page after updating
    except Exception as e:
        return f'Error updating profile: {str(e)}'
    finally:
        conn.close()

@app.route('/driver_ride_history')
def driver_ride_history():
    conn = create_mysql_connection()  # Assuming create_mysql_connection() creates your connection

    with conn.cursor() as cursor:
        driver_id = session['driver_id']
        print(driver_id)
        query = " SELECT tr.trip_id,tr.pickup_loc,tr.dropoff_loc,tr.request_status,tr.request_time,tr.estfare FROM Trip_requests tr WHERE tr.request_status = 'booked' AND tr.Pickup_time_estimationDriverdriver_id = %s"
        cursor.execute(query, (driver_id,))
        data = cursor.fetchall()
        print(data)
        conn.commit()
        # Render the template with the retrieved data
    conn.close()
    return render_template('driver_history.html', data=data)




@app.route('/customer_history')
def history():
    conn = create_mysql_connection()  # Assuming create_mysql_connection() creates your connection
    username = session.get('username')

    cursor = conn.cursor()

    # Use parameterized query to avoid SQL injection
    query = "SELECT * FROM Customer_details cd JOIN Rider_details rd ON cd.customer_id = rd.rider_id JOIN Trip_requests tr ON rd.rider_id = tr.Rider_detailsrider_id WHERE cd.customer_first_name = %s"
    cursor.execute(query, (username,))

    # Fetch all the results
    history_data = cursor.fetchall()
    print(history_data)

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    return render_template('customer_history.html', data=history_data)

    # Close the cursor and database connection
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Get form data
#         username = request.form['username']
#         password = request.form['password']

#         # Check user credentials in MySQL
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM Customer_details WHERE customer_first_name = %s AND password = %s", (username, password))
#         user = cur.fetchone()
#         cur.close()

#         if user:
#             # User found, redirect to dashboard or another page
#             return "Login successful"
#         else:
#             # User not found or incorrect credentials
#             return "Invalid username or password"

#     return render_template('login.html')



@app.route('/analysis')
def analysis():
    conn = create_mysql_connection()  # Assuming create_mysql_connection() creates your connection

    with conn.cursor() as cursor:
        # Histogram for Driver Ratings
        sql_query = "SELECT rating FROM Driver;"
        cursor.execute(sql_query)
        ratings = cursor.fetchall()
        ratings_list = [rating['rating'] for rating in ratings]

        plt.figure(figsize=(8, 6))
        plt.hist(ratings_list, bins=5, alpha=0.7, color='blue', edgecolor='black')
        plt.xlabel('Driver Ratings')
        plt.ylabel('Frequency')
        plt.title('Distribution of Driver Ratings')
        driver_ratings = io.BytesIO()
        plt.savefig(driver_ratings, format='png')
        driver_ratings.seek(0)
        driver_ratings_b64 = base64.b64encode(driver_ratings.getvalue()).decode('utf8')

        # Histogram for Trip Distances
        query_distances = "SELECT distance FROM Trip_requests"
        cursor.execute(query_distances)
        distances = cursor.fetchall()
        distance_values = [distance['distance'] for distance in distances]

        plt.figure(figsize=(8, 6))
        plt.hist(distance_values, bins=20, color='skyblue', edgecolor='black')
        plt.title('Distribution of Trip Distances')
        plt.xlabel('Distance')
        plt.ylabel('Frequency')
        plt.grid(True)
        trip_distances = io.BytesIO()
        plt.savefig(trip_distances, format='png')
        trip_distances.seek(0)
        trip_distances_b64 = base64.b64encode(trip_distances.getvalue()).decode('utf8')

        # Scatter Plot for Distance vs Estimated Fare
        cursor.execute("SELECT distance, estfare FROM Trip_requests;")
        distances = cursor.fetchall()
        distance_values = [distance['distance'] for distance in distances]
        estfare_values = [distance['estfare'] for distance in distances]

        plt.figure(figsize=(8, 6))
        plt.scatter(distance_values, estfare_values, alpha=0.5)
        plt.title('Relationship between Distance and Estimated Fare')
        plt.xlabel('Distance')
        plt.ylabel('Estimated Fare')
        plt.grid(True)
        distance_estfare = io.BytesIO()
        plt.savefig(distance_estfare, format='png')
        distance_estfare.seek(0)
        distance_estfare_b64 = base64.b64encode(distance_estfare.getvalue()).decode('utf8')

    conn.close()
    return render_template('analysis.html', driver_ratings=driver_ratings_b64, trip_distances=trip_distances_b64, distance_estfare=distance_estfare_b64)



if __name__ == '__main__':
    app.run(debug=True)
