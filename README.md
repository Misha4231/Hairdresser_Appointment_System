# Hairdresser Appointment System ✂️💇‍♀️

This project is a Telegram bot and Django-based web application designed for managing hairdresser appointments. It allows users to book, cancel, and view their appointments, while administrators can accept or reject appointments, manage blocked dates, and view all appointments. The backend for both the Telegram bot and Django web application is powered by an SQLite database.


## Screenshots 📸

### Example Telegram Bot Interface:
![Telegram Bot Example](./bot%201.png)
![Telegram Bot Example](./bot%202.png)
![Telegram Bot Example](./bot%203.png)
![Telegram Bot Example](./bot%204.png)
![Telegram Bot Example](./bot%205.png)

### Django Website:
![Django Website](./website%201.png)
![Django Website](./website%202.png)

## Features 🛠️

### Telegram Bot (Aiogram) 🤖
- **Make an appointment**: Users can select the date, time, category, and service to schedule an appointment. 📅
- **Cancel an appointment (User)**: Users can cancel their own appointments. ❌
- **Cancel an appointment (Admin)**: Admins can cancel any appointment. 🚫
- **Block dates (Admin)**: Admins can block specific days so that users can't make appointments on those dates. 🛑
- **View appointments**: Admins can view all scheduled appointments. 👀
- **Appointment approval**: When someone tries to make an appointment, the admin must accept or reject it. ✅❌

### Django Website 🌐
- **Fixture with mock data**: The website comes with a fixture to populate the database with mock data for testing. 🧪
- **Homepage**: Displays the basic information about the service and allows users to view appointments and services. 🏠
- **Reviews**: Users can view and add reviews for the services. ⭐
- **Paginated list**: The available categories and haircuts are displayed in a paginated list for easy browsing. 📑
- **Same database**: Both the bot and website share the same SQLite3 database, ensuring consistent data between the two platforms. 🔄

## Installation ⚙️

1. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Provide telegram bot token**:
    - Create bot in `BotFather` 🤖
    - Rename `.env.example` to `.env`
    - Paste a bot token and your user ID inside the `.env` file

3. **Set up the database**:
    - Go to the Django app directory:
      ```bash
      cd my_site
      ```
    - Run the following to apply migrations:
      ```bash
      python manage.py migrate
      ```
    - Load mock data:
      ```bash
      python manage.py loaddata fixtures/db.json
      ```

4. **Create a superuser for the Django app** (for admin access):
    ```bash
    python manage.py createsuperuser
    ```

5. **Run the server**:
    ```bash
    python manage.py runserver
    ```

6. **Run the Telegram bot**:
    - Make sure you have the bot token configured.
    - In the root directory, run:
    ```bash
    python main.py
    ```

## Usage 🚀

- **Telegram Bot**: Interact with the bot to book, cancel, and manage appointments.
- **Django Website**: Use the web interface to view available services, appointments, and reviews.

## Database 🗄️

Both the Telegram bot and Django application are powered by an **SQLite3 database**, ensuring that all data (appointments, users, services) is shared between both platforms.

## Technologies Used 💻

- **Telegram Bot**: Aiogram
- **Backend**: Django
- **Database**: SQLite3
