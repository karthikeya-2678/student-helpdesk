# Student Help Desk

A college complaint management system built with Flask, SQLite, HTML/CSS/JS.

## Features

### Student Portal
- Login with Name and Roll Number (auto-registers new students)
- Submit complaints in 5 categories: Hostel, Academics, Transport, Infrastructure, Other
- View complaint status and assigned admin details
- Track all submitted complaints

### Admin Portal
- Login with College Name and Password
- Complete profile (Name, Department, Role) on first login
- View all student complaints
- Take responsibility for complaints
- Update complaint status (Pending → In Progress → Resolved)

## Requirements

- Python 3.7+
- Flask
- Flask-Session

## Installation

1. **Navigate to the project folder:**
   ```bash
   cd flask-student-helpdesk
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   Open your browser and go to: `http://127.0.0.1:5000`

## Default Admin Credentials

- **College Name:** ABC College
- **Password:** admin123

## Project Structure

```
flask-student-helpdesk/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── helpdesk.db           # SQLite database (auto-created)
├── flask_session/        # Server-side session storage
├── static/
│   ├── css/
│   │   └── style.css     # Stylesheet
│   └── js/
│       └── main.js       # JavaScript enhancements
└── templates/
    ├── base.html         # Base template
    ├── home.html         # Landing page
    ├── student/
    │   ├── login.html
    │   ├── dashboard.html
    │   ├── complaint_form.html
    │   └── complaints.html
    └── admin/
        ├── login.html
        ├── profile.html
        └── dashboard.html
```

## Database Schema

### Students
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | Student name |
| roll | TEXT | Roll number (unique) |

### Admins
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| college_name | TEXT | College name (unique) |
| password | TEXT | Admin password |
| admin_name | TEXT | Admin's full name |
| department | TEXT | Department |
| role | TEXT | Role/Designation |
| profile_complete | INTEGER | Profile completion flag |

### Complaints
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| student_id | INTEGER | Foreign key to students |
| category | TEXT | Complaint category |
| message | TEXT | Complaint content |
| status | TEXT | Pending/In Progress/Resolved |
| admin_id | INTEGER | Foreign key to admins |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last update time |

## Network/Intranet Usage

This application is optimized for local network use:

1. **Run on your server/PC:**
   ```bash
   python app.py
   ```

2. **Access from other devices on the same network:**
   - Find your server's IP address (e.g., `192.168.1.100`)
   - Other devices can access: `http://192.168.1.100:5000`

3. **For production use:**
   - Consider using Gunicorn or uWSGI
   - Set `debug=False` in `app.py`
   - Change the `secret_key` to a secure random value

## Adding More Admins

To add additional admin accounts, you can either:

1. **Manually insert into database:**
   ```bash
   sqlite3 helpdesk.db
   INSERT INTO admins (college_name, password) VALUES ('New College', 'newpassword');
   .quit
   ```

2. **Or create an admin management page (extend the application)**

## Security Notes

- This is an MVP designed for intranet use
- For production, consider:
  - Password hashing (use `werkzeug.security`)
  - HTTPS encryption
  - CSRF protection
  - Rate limiting
  - Input sanitization

## License

MIT License - Free to use and modify.
