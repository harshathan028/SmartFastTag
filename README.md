This project is an enhanced FastTag system designed to simplify toll payments and balance management. It includes features like:
	•	User Authentication: Secure login system with SQLite database.
	•	Balance Management: Recharge and deduct balance directly through the interface.
	•	Auto-Pay: Automatically recharges the balance when it drops below ₹100.
	•	Low-Balance Alerts: Notifies users when their balance is low.
	•	Database Integration: Stores user data, including username and password.

◉ How to Run
1. Clone the repository
       git clone <repository_url>
       cd FastTagpro

2. Install dependencies
       pip install flask sqlite3

3. Run the app
       python3 app.py
   
4. Access the app
       Open your browser and go to http://localhost:5000

◉ The database (users.db) stores user credentials. To manually add users:

sqlite3 users.db
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
INSERT INTO users (username, password) VALUES ('admin', 'password123');
SELECT * FROM users;


◉ Future Improvements
	•	Add user registration.
	•	Implement secure password hashing.
	•	Integrate FastTag API for real-world toll processing.
