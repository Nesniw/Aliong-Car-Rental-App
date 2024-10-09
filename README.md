# Aliong Car Rental App 

## Overview
Aliong Car Rental Application is a web-based platform that enables users to rent vehicles for their transportation needs. 
Built using Python and JavaScript, this application offers a user-friendly interface for browsing & renting available vehicles for customer, and managing rental operation for admin.

## Features
Admin Side :
- **Car Rental Management**: Add, update, and delete cars data which available to rental.
- **Car Return Confirmation**: Confirm the returned rented cars from customer.
- **Booking History Management**: View and filter booking history based on date or with no filter.
- **Report Generation**: Generate PDF reports summarizing booking data.
- **Email Blast / Newsletter**: send newsletters or messages to selected customers all at the same time.

Customer Side :
- **Car Search & Booking**: View and browse available cars to book / rent. The selected car can be booked / rented based on the options available.
- **Car Return Confirmation**: Confirm the returned rented cars from customer.
- **Booking History**: View past and upcoming booking history.

## Technologies Used 
- **HTML5**: Structure and layout of the app.
- **CSS3**: Styling and responsive design.
- **JavaScript**: Dynamic content and interaction.
- **Python**: Booking / rental process & management logic.
- **MySQL**: Storing & managing car rental data.

## Preview 
![Aliongs 1](https://github.com/user-attachments/assets/10c44ed7-6888-4580-ac3d-27987b857710) <br> <br>
![Aliongs 2](https://github.com/user-attachments/assets/72053532-b874-40e7-82c2-2b5cd4c01c4c) <br> <br>
![Aliongs 3](https://github.com/user-attachments/assets/13cb9e78-9ead-4fc9-b14c-66d3b58a2000)

## Installation
Follow these steps to set up and run the project locally:

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/Nesniw/Aliong-Car-Rental-App.git
    cd Aliong-Car-Rental-App
    ```
    
2. **Ensure Python is installed and create virtual env for python project**
   ```bash
   python -m venv venv
   ```
3. **Install flask with every required libraries**
    ```bash
    pip install Flask Flask-Mail PyMySQL Jinja2 ReportLab Werkzeug pdfkit
    ```
4. **Configure specific settings**
   - app.py
   ```bash
   app.secret_key = YOUR_SECRET_KEY'

   MAIL_USERNAME = 'your_email@example.com'  # User needs to replace this
   MAIL_PASSWORD = 'your_password'  # User needs to replace this
   ```
   - model.py
   ```bash
   return pymysql.connect(host="localhost", user="YOUR_USER_NAME", password="YOUR_PASSWORD", database="YOUR_DATABASE_NAME")
   ```
5. **Run this command in the terminal**
   ```bash
   python -m flask run
   ```
   or
   ```bash
   flask run
   ```
    
## Thank You

Thank you for visiting Aliong Car Rental! 😊

By Winsen Wiradinata <br> <br>
<a href="https://www.linkedin.com/in/winsen-wiradinata/"><img src="https://img.shields.io/badge/-Winsen%20Wiradinata-0077B5?style=flat&logo=Linkedin&logoColor=white"/></a>
<a href="mailto:winsenwiradinata@gmail.com"><img src="https://img.shields.io/badge/-winsenwiradinata@gmail.com-D14836?style=flat&logo=Gmail&logoColor=white"/></a>
