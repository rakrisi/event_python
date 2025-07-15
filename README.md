# 🎉 Flask Event Check-In App

A beautiful and responsive event check-in and feedback web application built with Flask, Firebase Firestore, Tailwind CSS, and QR codes.

## 🔒 Security Notice
**IMPORTANT**: This project uses Firebase service account credentials. The `firebase-service-account-key.json` file contains sensitive information and should **NEVER** be committed to version control. It is automatically excluded via `.gitignore`. Always keep your Firebase credentials secure!

## ✨ Features

### 🔐 Security Features
- **Admin Authentication**: Secure password protection for admin panel (password: `event@123`)
- **Session Management**: Persistent login sessions with secure logout
- **Protected Routes**: All admin functions require authentication
- **Access Control**: Clear separation between user and admin functionalities
- **Firebase Security**: Secure cloud database with proper authentication

### 🧑‍💼 Admin Features
- **Event Management**: Create and manage multiple events with dates and descriptions
- **Real-time QR Scanner**: Webcam-based QR code scanning for instant check-ins
- **Manual Check-in**: Backup manual check-in system using registration IDs
- **Participant Dashboard**: View all participants with real-time check-in and feedback status
- **Feedback Analytics**: Comprehensive feedback dashboard with ratings distribution charts
- **Export Capabilities**: Export feedback data to CSV, print reports, or copy to clipboard
- **Multi-event Support**: Manage multiple events simultaneously with separate participant lists
- **Cloud Sync**: Real-time data synchronization across devices with Firebase

### 🙋 User Features  
- **Quick Registration**: Simple 3-field form to register for any active event
- **Instant QR Generation**: Get downloadable QR codes immediately after registration
- **User Panel**: View all your registrations, QR codes, and feedback links in one place
- **Mobile-Optimized**: Perfect experience on smartphones and tablets
- **Feedback System**: Interactive 5-star rating with optional detailed comments
- **Cloud Storage**: All data stored securely in Firebase Firestore
- **Real-time Updates**: Instant updates across all devices and sessions

### 🎨 UI/UX Features
- **Modern Design**: Beautiful Tailwind CSS with gradient backgrounds and smooth animations
- **Responsive Layout**: Adapts perfectly to any screen size (mobile, tablet, desktop)
- **Interactive Elements**: Hover effects, button animations, and real-time feedback
- **Accessibility**: WCAG compliant with screen reader support and keyboard navigation
- **Progressive Enhancement**: Works without JavaScript, enhanced with it
- **Dark Mode Ready**: Prepared for easy dark mode implementation

## 🛠 Requirements
- Python 3.8+
- Flask 2.3.3
- qrcode 7.4.2
- pillow 10.0.1
- firebase-admin 6.2.0
- Firebase Project with Firestore enabled

## 🚀 Quick Setup

### 1. Firebase Setup (Required)
**⚠️ IMPORTANT: Firebase setup is mandatory before running the application.**

1. **Create Firebase Project:**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project
   - Enable Firestore Database in production mode

2. **Download Service Account Key:**
   - Go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Save as `firebase-service-account-key.json` in project root
   - **🔒 Security Notice**: This file contains sensitive credentials and is automatically ignored by git

3. **Configure Firestore Rules (Optional but Recommended):**
   ```javascript
   // Firestore Security Rules
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       // Allow read/write access to all documents
       match /{document=**} {
         allow read, write: if true;
       }
     }
   }
   ```

4. **For detailed Firebase setup instructions, see [FIREBASE_SETUP.md](FIREBASE_SETUP.md)**

### 2. Install Dependencies
```powershell
# Clone or download the project
git clone <your-repo-url>
cd event_python

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Environment Setup
1. **Verify Firebase Configuration:**
   - Ensure `firebase-service-account-key.json` is in the project root
   - Check that `firebase_config.py` exists and is properly configured

2. **Run the application:**
   ```powershell
   python main.py
   ```

3. **Open in browser:**
   ```
   http://127.0.0.1:5000
   ```

### 4. First-Time Setup
1. **Access Admin Panel:**
   - Navigate to `http://127.0.0.1:5000/admin/login`
   - Enter password: `event@123`
   - Create your first event to get started

## 📊 Database Architecture

**🔥 Firebase Firestore** - This application uses Firebase Firestore as the primary database.

### Collections Structure:
- **events**: Event information with document IDs as unique identifiers
- **registrations**: User registrations linked to events
- **feedback**: User feedback and ratings

### Migration from SQLite:
**Important:** If you have existing SQLite data (`event.db` file):
- The old `event.db` file is no longer used and can be safely removed
- Document IDs in Firestore replace integer primary keys from SQLite
- Existing QR codes with integer IDs will need to be regenerated
- See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for migration guidance

### Firebase Advantages:
- **Real-time sync**: Data updates across all devices instantly
- **Scalability**: Handles growth from 10 to 10,000+ users seamlessly
- **Reliability**: 99.99% uptime with automatic backups
- **Security**: Built-in authentication and security rules
- **Offline Support**: Works offline with automatic sync when reconnected

## 📱 Detailed How to Use

### 🎯 Use Cases

#### **Conference/Seminar Management**
- Create multiple sessions/tracks as separate events
- Track attendance for each session
- Collect session-specific feedback
- Generate attendance reports

#### **Workshop Registration**
- Manage limited-capacity workshops
- Quick check-in with QR codes
- Collect skill-level feedback
- Track completion rates

#### **Networking Events**
- Simple registration for networking sessions
- Fast check-in to track participation
- Gather feedback on venue and organization
- Export attendee lists for follow-ups

#### **Corporate Training**
- Track employee training attendance
- Collect training effectiveness feedback
- Generate completion certificates data
- Monitor engagement levels

### 🔧 Step-by-Step Usage Guide

#### **For Event Organizers (Admins)**

##### **Initial Setup:**
1. **Access Admin Panel:**
   - Go to `http://127.0.0.1:5000/admin/login`
   - Enter password: `event@123`
   - Click "Login as Admin"

2. **Create Your First Event:**
   - Navigate to Admin Panel (`/admin`)
   - Fill in the "Create New Event" form:
     - **Event Title**: e.g., "Tech Conference 2025"
     - **Description**: e.g., "Annual technology conference with industry leaders"
     - **Date**: Select event date
   - Click "Create Event"

##### **Managing Events:**
3. **View Event Participants:**
   - In Admin Panel, click "View Participants" for any event
   - See real-time status: registered, checked-in, feedback given
   - Access individual feedback and analytics

4. **Check-in Participants (Two Methods):**

   **Method A - QR Scanner:**
   - Click "QR Scanner" in Admin Panel
   - Allow camera access when prompted
   - Point camera at participant's QR code
   - Automatic check-in with success confirmation

   **Method B - Manual Check-in:**
   - Click "Manual Check-in" in Admin Panel
   - Enter the Registration ID number
   - Click "Check In" to verify manually

##### **Analytics & Reports:**
5. **View Feedback Analytics:**
   - Click "View Feedback" next to any event
   - See rating distribution charts
   - Read individual comments
   - Export data using "Export to CSV" or "Print Report"

#### **For Participants (Users)**

##### **Registration Process:**
1. **Register for Event:**
   - Visit the homepage (`http://127.0.0.1:5000`)
   - Click "Register for Event" 
   - Fill registration form:
     - **Full Name**: Your complete name
     - **Email**: Valid email address
     - **Select Event**: Choose from available events
   - Click "Register Now"

2. **Get Your QR Code:**
   - After registration, your QR code appears instantly
   - **Save Options:**
     - Click "Download QR Code" for a PNG file
     - Click "Share QR Code" to get a shareable link
     - Take a screenshot for backup

##### **Event Day:**
3. **Check-in Process:**
   - Arrive at the event venue
   - Show your QR code to event staff
   - Staff scans with their device
   - Receive confirmation and feedback link

##### **Post-Event:**
4. **Submit Feedback:**
   - Use the feedback link provided after check-in
   - Rate your experience (1-5 stars)
   - Add optional detailed comments
   - Submit to help improve future events

##### **Manage Your Registrations:**
5. **Access User Panel:**
   - Go to "User Panel" from homepage
   - Enter your email address
   - View all your registrations, QR codes, and feedback status
   - Re-download QR codes if needed

### 💡 Pro Tips

#### **For Admins:**
- **Pre-event**: Create events well in advance and share registration links
- **During event**: Use QR scanner for fastest check-ins, manual backup for technical issues
- **Post-event**: Review feedback analytics to improve future events
- **Multiple events**: Create separate events for different sessions/days

#### **For Users:**
- **Save QR codes**: Download and save to phone gallery for offline access
- **Email backup**: Email yourself the QR code link as backup
- **User panel**: Bookmark user panel for easy access to all registrations
- **Feedback**: Provide detailed feedback to help organizers improve

### 🚨 Troubleshooting

#### **Common Issues:**
- **QR Scanner not working**: Ensure camera permissions are granted
- **Can't find registration**: Use User Panel with exact email address used for registration
- **Admin login issues**: Verify password is exactly `event@123` (case-sensitive)
- **QR code not scanning**: Ensure good lighting and steady camera position

## 🔄 Workflow

```
1. Admin creates event
2. User registers → Gets QR code
3. Admin scans QR → User checked in
4. User receives feedback link
5. User submits rating & comments
```

## 💾 Local Storage Features

The app automatically saves:
- **Registration data** for QR code recovery
- **Feedback drafts** to prevent data loss
- **Scanner statistics** for analytics
- **Verification history** for tracking

## 🗂 Database Schema (Firebase Firestore)

### Collections:
- **events**: `{id, title, description, date, created_at}`
- **registrations**: `{id, event_id, name, email, checked_in, feedback_given, registration_date}`
- **feedback**: `{id, registration_id, rating, comment, feedback_date}`

### Document Structure:
```javascript
// events collection
{
  id: "auto-generated-doc-id",
  title: "Tech Conference 2025",
  description: "Annual technology conference",
  date: "2025-07-15",
  created_at: Timestamp
}

// registrations collection
{
  id: "auto-generated-doc-id", 
  event_id: "reference-to-event-doc",
  name: "John Doe",
  email: "john@example.com",
  checked_in: false,
  feedback_given: false,
  registration_date: Timestamp
}

// feedback collection
{
  id: "auto-generated-doc-id",
  registration_id: "reference-to-registration-doc", 
  rating: 5,
  comment: "Great event!",
  feedback_date: Timestamp
}
```

## 📁 Complete Project Structure

```
event_python/
├── main.py                          # Main Flask application with all routes
├── data_service.py                  # Firebase Firestore service layer
├── firebase_config.py               # Firebase configuration and initialization
├── firebase-service-account-key.json # Firebase credentials (ignored by git)
├── requirements.txt                 # Python dependencies
├── README.md                       # This comprehensive documentation
├── FIREBASE_SETUP.md               # Detailed Firebase setup instructions
├── event.db                        # Legacy SQLite database (can be removed)
├── .gitignore                      # Git ignore rules (includes Firebase keys)
├── templates/                      # HTML templates with Tailwind CSS
│   ├── index.html                 # Homepage - events list and navigation
│   ├── register.html              # Registration form with event selection
│   ├── qr.html                    # QR code display with download options
│   ├── user_panel.html            # User dashboard for all registrations
│   ├── verify.html                # Admin check-in verification page
│   ├── checked_in.html            # Check-in success confirmation
│   ├── feedback.html              # User feedback form with star rating
│   ├── thankyou.html              # Thank you page after feedback
│   ├── admin_login.html           # Admin authentication page
│   ├── admin.html                 # Admin panel - event management
│   ├── scan.html                  # QR scanner interface for admins
│   └── feedback_view.html         # Admin feedback analytics dashboard
├── static/                        # Static files (using Tailwind CDN)
└── __pycache__/                   # Python cache files (ignored by git)
```

### Key Files Explained:
- **`main.py`**: Core Flask application with routing and business logic
- **`data_service.py`**: Abstraction layer for Firebase Firestore operations
- **`firebase_config.py`**: Firebase SDK initialization and configuration
- **`firebase-service-account-key.json`**: 🔒 Sensitive Firebase credentials (never commit to git)
- **`event.db`**: Legacy SQLite database file (can be safely removed)

## 🎯 Enhanced API Routes

| Route | Method | Access | Description |
|-------|--------|--------|-------------|
| `/` | GET | Public | Homepage with active events list |
| `/register` | GET/POST | Public | User registration form and processing |
| `/qr/<reg_id>` | GET | Public | Generate and serve QR code image |
| `/user` | GET/POST | Public | User panel to view registrations |
| `/feedback/<reg_id>` | GET/POST | Public | User feedback form (requires check-in) |
| `/admin/login` | GET/POST | Public | Admin authentication |
| `/admin/logout` | GET | Admin | Admin logout |
| `/admin` | GET/POST | Admin | Admin panel and event creation |
| `/admin/feedback/<event_id>` | GET | Admin | Feedback analytics dashboard |
| `/verify/<reg_id>` | GET/POST | Admin | Check-in verification page |
| `/scan` | GET | Admin | QR code scanner interface |
| `/manual_checkin` | POST | Admin | Manual check-in processing |

## 🌟 Key Technologies

- **Backend**: Flask (Python web framework)
- **Database**: Firebase Firestore (NoSQL cloud database)
- **Authentication**: Firebase Admin SDK for secure database access
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **QR Generation**: python-qrcode + Pillow
- **QR Scanning**: html5-qrcode library
- **Storage**: Browser localStorage for drafts and analytics
- **Cloud Services**: Google Firebase platform for scalability and reliability

## 🔧 Configuration & Customization

### **Security Configuration**
- **Admin Password**: Change `ADMIN_PASSWORD = 'event@123'` in `main.py`
- **Secret Key**: Update `app.secret_key` for production (use environment variables)
- **Firebase Security**: Configure Firestore security rules for production
- **Session Security**: Configure session timeout if needed

### **Database Configuration**
- **Firebase Firestore**: Default cloud database with automatic scaling
- **Backup**: Firebase automatically handles backups and replication
- **Environment**: Use different Firebase projects for dev/staging/production
- **Security Rules**: Configure Firestore rules for data access control

### **Environment Variables**
```bash
# Recommended for production
FLASK_SECRET_KEY=your-production-secret-key
ADMIN_PASSWORD=your-secure-admin-password
FIREBASE_PROJECT_ID=your-firebase-project-id
```

### **UI Customization**
- **Colors**: Modify Tailwind classes in templates
- **Branding**: Update logos and text in templates
- **Layout**: Adjust responsive breakpoints and spacing
- **Animations**: Customize hover effects and transitions

### **Feature Extensions**
- **Email Notifications**: Add SMTP configuration for automated emails
- **Multiple Admins**: Extend authentication system
- **Event Categories**: Add event categorization
- **Payment Integration**: Add Stripe/PayPal for paid events
- **Advanced Analytics**: Add charts and more detailed reporting

### **Deployment Configuration**
```python
# Production settings in main.py
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'your-production-secret-key'
app.config['DATABASE_URL'] = 'your-production-database-url'
```

## 🎪 Real-World Examples

### **Example 1: Tech Conference**
```
Event: "AI & Machine Learning Summit 2025"
Participants: 200 attendees
Process:
1. Admin creates event 2 weeks before
2. Participants register online → 180 registrations
3. Event day: QR scanning at entrance → 165 check-ins
4. Post-event: 140 feedback submissions (85% response rate)
5. Analytics: Average rating 4.3/5, export for sponsors
```

### **Example 2: Corporate Training**
```
Event: "Cybersecurity Awareness Training"
Participants: 50 employees
Process:
1. HR creates training event
2. Employees register via company email
3. Training day: Manual check-in for compliance tracking
4. Immediate feedback collection for training effectiveness
5. Export completion data for HR records
```

### **Example 3: Workshop Series**
```
Events: Multiple small workshops (15-20 people each)
Process:
1. Create separate events for each workshop
2. Limited registration management
3. QR check-in for attendance tracking
4. Workshop-specific feedback collection
5. Compare feedback across different workshops
```

## 🚀 Production Deployment Guide

### **Preparation Checklist**
1. **Security Updates:**
   ```python
   # In main.py - use environment variables
   import os
   app.config['DEBUG'] = False
   app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback-key')
   ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'event@123')
   ```

2. **Firebase Configuration:**
   - Create separate Firebase projects for production
   - Generate new service account key for production
   - Configure Firestore security rules for production
   - Set up Firebase monitoring and alerts

3. **Environment Variables:**
   ```bash
   export FLASK_SECRET_KEY="your-complex-production-secret-key"
   export ADMIN_PASSWORD="your-secure-admin-password"
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/firebase-service-account-key.json"
   ```

4. **Dependencies:**
   ```bash
   pip install gunicorn python-dotenv
   ```

### **Deployment Options**

#### **Option 1: Google Cloud Run (Recommended for Firebase)**
```bash
# Create Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app

# Deploy to Cloud Run
gcloud run deploy event-app --source . --platform managed --region us-central1
```

#### **Option 2: Heroku**
```bash
# Create Procfile
echo "web: gunicorn main:app" > Procfile

# Add Firebase credentials as config vars
heroku config:set GOOGLE_APPLICATION_CREDENTIALS="firebase-service-account-key.json"

# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

#### **Option 3: Traditional VPS**
```bash
# Install dependencies
pip install gunicorn nginx

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app

# Set up Nginx reverse proxy
sudo nano /etc/nginx/sites-available/event-app
```

### **Firebase Production Setup**
1. **Create Production Firebase Project:**
   - Separate project from development
   - Configure production Firestore rules
   - Set up monitoring and alerts

2. **Security Rules Example:**
   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /events/{eventId} {
         allow read: if true;
         allow write: if request.auth != null;
       }
       match /registrations/{regId} {
         allow read, write: if request.auth != null;
       }
       match /feedback/{feedbackId} {
         allow read, write: if request.auth != null;
       }
     }
   }
   ```

### **Post-Deployment**
- Test all functionality thoroughly
- Monitor Firebase usage and billing
- Set up logging and error tracking
- Configure SSL certificates (handled automatically on most platforms)
- Set up monitoring for Firebase quotas and performance
- Monitor costs and set up budget alerts

## 🎨 Advanced Customization Examples

### **Custom Event Types**
```python
# Add to main.py - extend events table
c.execute('''ALTER TABLE events ADD COLUMN event_type TEXT DEFAULT 'general' ''')
c.execute('''ALTER TABLE events ADD COLUMN max_participants INTEGER DEFAULT 0''')
c.execute('''ALTER TABLE events ADD COLUMN registration_fee REAL DEFAULT 0.0''')
```

### **Email Integration**
```python
# Add email notifications
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

### **Custom Styling**
```html
<!-- Add to any template for custom branding -->
<style>
:root {
  --primary-color: #your-brand-color;
  --secondary-color: #your-accent-color;
}
</style>
```

### **API Extensions**
```python
# Add REST API endpoints
@app.route('/api/events', methods=['GET'])
def api_events():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()
    return jsonify([dict(event) for event in events])
```

## 🔍 Monitoring & Analytics

### **Built-in Analytics**
- Registration conversion rates
- Check-in success rates  
- Feedback response rates
- Rating distributions
- Event popularity metrics

### **Custom Analytics**
```python
# Add custom tracking
@app.route('/analytics')
@admin_required
def analytics():
    conn = get_db_connection()
    # Custom queries for insights
    conversion_rate = conn.execute('''
        SELECT 
            COUNT(DISTINCT r.id) as registered,
            COUNT(CASE WHEN r.checked_in = 1 THEN 1 END) as checked_in
        FROM registrations r
    ''').fetchone()
    return render_template('analytics.html', data=conversion_rate)
```

## 📄 License

MIT License - Feel free to use and modify!

---

**Built with ❤️ using Flask, Tailwind CSS, and modern web technologies**
