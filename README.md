# 🇮🇳 Attendance Management System - भारतीय कर्मचारी उपस्थिति प्रबंधन

A complete Django web application for managing employee attendance with Indian localization, INR currency support, and user-friendly interface designed for Indian businesses.

## ✨ Features

- **🔐 Authentication System**: User registration and login with Indian phone numbers
- **👥 Employee Management**: Add, view, and manage employees with Indian names and INR salaries
- **📅 Attendance Marking**: Mark daily attendance for all employees
- **📊 Reports & Analytics**: View monthly reports with charts and statistics
- **📤 Export Functionality**: Download reports as CSV
- **📱 Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **🇮🇳 Indian Localization**: INR currency, Indian date format (DD/MM/YYYY), IST timezone
- **🏢 Business Ready**: Perfect for Indian companies and organizations

## Tech Stack

- **Backend**: Django 5.x
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML, Bootstrap 5, Chart.js
- **Deployment**: Heroku-ready

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd attendance_app
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
```bash
# Copy environment file
cp env.example .env

# Edit .env file with your settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## Usage

### 1. Registration & Login
- Register a new account or login with existing credentials
- After login, you'll be redirected to the dashboard

### 2. Employee Management
- Add new employees with their details (name, ID, role, salary)
- View all employees in a clean table format
- Each employee gets a unique ID for tracking

### 3. Mark Attendance
- Select a date (defaults to today)
- Mark attendance for all employees (Present/Absent/Leave/Holiday)
- System prevents duplicate entries for the same date
- Success messages confirm attendance submission

### 4. View Reports
- Select month and year for reports
- View attendance summary with statistics
- Interactive charts show attendance patterns
- Click on employee names for detailed daily records
- Export reports as CSV files

## Deployment

### Heroku Deployment

1. **Install Heroku CLI**
2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

6. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   ```

7. **Create Superuser**
   ```bash
   heroku run python manage.py createsuperuser
   ```

### Other Platforms

The application is also ready for deployment on:
- **Railway**
- **Render**
- **DigitalOcean App Platform**
- **AWS Elastic Beanstalk**

## Project Structure

```
attendance_app/
├── attendance_app/          # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── attendance/                # Main app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/              # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── mark_attendance.html
│   ├── attendance_report.html
│   ├── employee_detail.html
│   └── registration/
│       ├── login.html
│       └── register.html
├── static/                 # Static files (CSS, JS, Images)
├── requirements.txt
├── Procfile               # Heroku deployment
├── runtime.txt           # Python version
├── manage.py
└── README.md
```

## Features in Detail

### Authentication
- User registration with username, phone number, and password
- Secure login/logout functionality
- Session-based authentication

### Employee Management
- Add employees with complete details
- Unique employee IDs
- Role and salary tracking
- Employee listing with search and filter

### Attendance System
- Daily attendance marking
- Four status types: Present, Absent, Leave, Holiday
- Date picker for selecting attendance dates
- Prevention of duplicate entries
- Bulk attendance marking

### Reporting & Analytics
- Monthly attendance reports
- Attendance percentage calculations
- Visual charts (bar and pie charts)
- Individual employee details
- Low attendance highlighting (< 75%)
- CSV export functionality

### User Interface
- Responsive Bootstrap 5 design
- Mobile-friendly interface
- Clean and professional layout
- Intuitive navigation
- Success/error message system

## Customization

### Adding New Features
1. Create new models in `attendance/models.py`
2. Add corresponding views in `attendance/views.py`
3. Create templates in `templates/` directory
4. Update URL patterns in `attendance/urls.py`

### Styling
- Modify `templates/base.html` for global styles
- Add custom CSS in `static/css/` directory
- Update Bootstrap classes in templates

### Database
- Change database settings in `attendance_app/settings.py`
- Run migrations after model changes
- Use PostgreSQL for production

## Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic
   ```

3. **Permission Errors**
   - Ensure proper file permissions
   - Check virtual environment activation

4. **Database Issues**
   - Delete `db.sqlite3` and run migrations again
   - Check database settings in `settings.py`

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Django documentation
3. Check application logs for errors

## License

This project is open source and available under the MIT License.
