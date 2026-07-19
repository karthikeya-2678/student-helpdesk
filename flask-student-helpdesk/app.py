"""
Student Help Desk - Flask Backend
A college complaint management system for students and administration.
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_session import Session
import sqlite3
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'student-helpdesk-secret-key-change-in-production'

# Server-side session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session'
app.config['SESSION_PERMANENT'] = False
Session(app)

DATABASE = 'helpdesk.db'

# ===== DATABASE HELPERS =====

def get_db():
    """Get database connection with row factory."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with required tables."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Admins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            college_name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            admin_name TEXT,
            department TEXT,
            role TEXT,
            profile_complete INTEGER DEFAULT 0
        )
    ''')
    
    # Complaints table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            admin_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (admin_id) REFERENCES admins(id)
        )
    ''')
    
    # Insert default admin account if not exists
    cursor.execute('''
        INSERT OR IGNORE INTO admins (college_name, password)
        VALUES ('ABC College', 'admin123')
    ''')
    
    conn.commit()
    conn.close()

# ===== AUTH DECORATORS =====

def student_required(f):
    """Decorator to require student login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'student_id' not in session:
            flash('Please login as a student first.', 'error')
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login as an administrator first.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ===== ROUTES: HOME =====

@app.route('/')
def home():
    """Landing page with role selection."""
    return render_template('home.html')

# ===== ROUTES: STUDENT =====

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    """Student login page."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        roll = request.form.get('roll', '').strip()
        
        if not name or not roll:
            flash('Please enter both name and roll number.', 'error')
            return redirect(url_for('student_login'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if student exists
        cursor.execute('SELECT * FROM students WHERE roll = ?', (roll,))
        student = cursor.fetchone()
        
        if student:
            # Verify name matches
            if student['name'].lower() != name.lower():
                flash('Name does not match the roll number.', 'error')
                conn.close()
                return redirect(url_for('student_login'))
        else:
            # Create new student
            cursor.execute('INSERT INTO students (name, roll) VALUES (?, ?)', (name, roll))
            conn.commit()
            cursor.execute('SELECT * FROM students WHERE roll = ?', (roll,))
            student = cursor.fetchone()
        
        session['student_id'] = student['id']
        session['student_name'] = student['name']
        session['student_roll'] = student['roll']
        
        conn.close()
        flash('Login successful!', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('student/login.html')

@app.route('/student/dashboard')
@student_required
def student_dashboard():
    """Student dashboard with complaint categories."""
    return render_template('student/dashboard.html', 
                         student_name=session.get('student_name'))

@app.route('/student/complaint/<category>', methods=['GET', 'POST'])
@student_required
def student_complaint(category):
    """Complaint submission form."""
    categories = ['Hostel', 'Academics', 'Transport', 'Infrastructure', 'Other']
    
    if category not in categories:
        flash('Invalid category.', 'error')
        return redirect(url_for('student_dashboard'))
    
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        
        if not message:
            flash('Please enter your complaint.', 'error')
            return redirect(url_for('student_complaint', category=category))
        
        if len(message) > 2000:
            flash('Complaint message is too long (max 2000 characters).', 'error')
            return redirect(url_for('student_complaint', category=category))
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO complaints (student_id, category, message)
            VALUES (?, ?, ?)
        ''', (session['student_id'], category, message))
        conn.commit()
        conn.close()
        
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('student_complaints'))
    
    return render_template('student/complaint_form.html', category=category)

@app.route('/student/complaints')
@student_required
def student_complaints():
    """View student's complaints with status and admin info."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.*, a.admin_name, a.department, a.role
        FROM complaints c
        LEFT JOIN admins a ON c.admin_id = a.id
        WHERE c.student_id = ?
        ORDER BY c.created_at DESC
    ''', (session['student_id'],))
    complaints = cursor.fetchall()
    conn.close()
    
    return render_template('student/complaints.html', complaints=complaints)

@app.route('/student/logout')
def student_logout():
    """Student logout."""
    session.pop('student_id', None)
    session.pop('student_name', None)
    session.pop('student_roll', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

# ===== ROUTES: ADMIN =====

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if request.method == 'POST':
        college_name = request.form.get('college_name', '').strip()
        password = request.form.get('password', '').strip()
        
        if not college_name or not password:
            flash('Please enter college name and password.', 'error')
            return redirect(url_for('admin_login'))
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM admins WHERE college_name = ? AND password = ?
        ''', (college_name, password))
        admin = cursor.fetchone()
        conn.close()
        
        if not admin:
            flash('Invalid credentials.', 'error')
            return redirect(url_for('admin_login'))
        
        session['admin_id'] = admin['id']
        session['admin_college'] = admin['college_name']
        session['profile_complete'] = admin['profile_complete']
        
        flash('Login successful!', 'success')
        
        if not admin['profile_complete']:
            return redirect(url_for('admin_profile'))
        
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/login.html')

@app.route('/admin/profile', methods=['GET', 'POST'])
@admin_required
def admin_profile():
    """Admin profile completion form."""
    if request.method == 'POST':
        admin_name = request.form.get('admin_name', '').strip()
        department = request.form.get('department', '').strip()
        role = request.form.get('role', '').strip()
        
        if not admin_name or not department or not role:
            flash('Please fill all fields.', 'error')
            return redirect(url_for('admin_profile'))
        
        if len(admin_name) > 100 or len(department) > 100 or len(role) > 100:
            flash('Field values are too long (max 100 characters).', 'error')
            return redirect(url_for('admin_profile'))
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE admins 
            SET admin_name = ?, department = ?, role = ?, profile_complete = 1
            WHERE id = ?
        ''', (admin_name, department, role, session['admin_id']))
        conn.commit()
        conn.close()
        
        session['profile_complete'] = 1
        session['admin_name'] = admin_name
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admins WHERE id = ?', (session['admin_id'],))
    admin = cursor.fetchone()
    conn.close()
    
    return render_template('admin/profile.html', admin=admin)

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard showing all complaints."""
    if not session.get('profile_complete'):
        flash('Please complete your profile first.', 'warning')
        return redirect(url_for('admin_profile'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.*, s.name as student_name, s.roll as student_roll,
               a.admin_name as assigned_admin
        FROM complaints c
        JOIN students s ON c.student_id = s.id
        LEFT JOIN admins a ON c.admin_id = a.id
        ORDER BY 
            CASE c.status 
                WHEN 'Pending' THEN 1 
                WHEN 'In Progress' THEN 2 
                ELSE 3 
            END,
            c.created_at DESC
    ''')
    complaints = cursor.fetchall()
    conn.close()
    
    return render_template('admin/dashboard.html', complaints=complaints)

@app.route('/admin/take/<int:complaint_id>', methods=['POST'])
@admin_required
def admin_take_complaint(complaint_id):
    """Admin takes responsibility for a complaint."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if complaint exists and is not already assigned
    cursor.execute('SELECT * FROM complaints WHERE id = ?', (complaint_id,))
    complaint = cursor.fetchone()
    
    if not complaint:
        flash('Complaint not found.', 'error')
        conn.close()
        return redirect(url_for('admin_dashboard'))
    
    if complaint['admin_id']:
        flash('This complaint is already assigned.', 'warning')
        conn.close()
        return redirect(url_for('admin_dashboard'))
    
    cursor.execute('''
        UPDATE complaints 
        SET admin_id = ?, status = 'In Progress', updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (session['admin_id'], complaint_id))
    conn.commit()
    conn.close()
    
    flash('You have taken responsibility for this complaint.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/status/<int:complaint_id>', methods=['POST'])
@admin_required
def admin_update_status(complaint_id):
    """Admin updates complaint status."""
    status = request.form.get('status', '').strip()
    valid_statuses = ['Pending', 'In Progress', 'Resolved']
    
    if status not in valid_statuses:
        flash('Invalid status.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Verify admin is assigned to this complaint
    cursor.execute('SELECT * FROM complaints WHERE id = ?', (complaint_id,))
    complaint = cursor.fetchone()
    
    if not complaint:
        flash('Complaint not found.', 'error')
        conn.close()
        return redirect(url_for('admin_dashboard'))
    
    if complaint['admin_id'] != session['admin_id']:
        flash('You can only update complaints assigned to you.', 'error')
        conn.close()
        return redirect(url_for('admin_dashboard'))
    
    cursor.execute('''
        UPDATE complaints 
        SET status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (status, complaint_id))
    conn.commit()
    conn.close()
    
    flash(f'Status updated to {status}.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    """Admin logout."""
    session.pop('admin_id', None)
    session.pop('admin_college', None)
    session.pop('admin_name', None)
    session.pop('profile_complete', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

# ===== MAIN =====

if __name__ == '__main__':
    # Create database tables
    init_db()
    print("Database initialized.")
    print("Default admin: College Name='ABC College', Password='admin123'")
    print("\nStarting server at http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
