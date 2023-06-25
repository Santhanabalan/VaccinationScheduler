# Vaccination Booking Website - DevRev Task

The Vaccination Booking Website is an online platform designed to facilitate the process of scheduling vaccination appointments. It allows users to search for vaccination centers, book available slots, and manage their appointments conveniently.

## Live Website

Check out the live Vaccination Booking Website [here](https://covax.santhanabalan.ml/).

## Features

- Search for vaccination centers based on name or address
- View vaccination center details including working hours
- Book available slots for vaccination appointments
- Admin Dashboard - Add/Remove Vaccination Center and Slots

## Steps to Run

1. **Clone the Repository**
   - Open a terminal and navigate to the desired directory.
   - Run the following command to clone the repository:
     ```
     git clone https://github.com/Santhanabalan/VaccinationScheduler.git
     ```
   - Change into the project directory:
     ```
     cd VaccinationScheduler
     ```

2. **Install Dependencies**
   - Make sure you have Python and pip installed on your system.
   - Run the following command to install the required dependencies:
     ```
     pip install -r requirements.txt
     ```

3. **Database Setup**
   - Run the following command to apply database migrations:
     ```
     python manage.py makemigrations
     python manage.py migrate
     ```

4. **Start the Development Server**
   - Start the development server by running the following command:
     ```
     python manage.py runserver
     ```

5. **Access the Website**
   - Open a web browser and visit `http://localhost:8000` to access the Vaccination Booking Website.
   - You can now use the website to search for vaccination centers, book slots, and manage appointments.

## Screenshots

Here are some screenshots from the Vaccination Booking Website:

![Home Page](/Screenshots/Home.png)
*Home Page*

![Search Page](/Screenshots/Search.png)
*Search Page*

![Booking Page](/Screenshots/Book.png)
*Booking a Vaccination Slot*

![User Profile](/Screenshots/Profile.png)
*User Profile with Appointments*

![Admin Dashboard](/Screenshots/Dashboard.png)
*Admin Dashboard*

![Center Details](/Screenshots/Center_Details.png)
*Vaccination Center Details*
