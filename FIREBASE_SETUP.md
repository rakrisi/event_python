# Firebase Setup Guide

## Prerequisites
Before running the application, you need to set up Firebase and download the service account key.

## Steps to Set Up Firebase

### 1. Create a Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter your project name (e.g., "event-management")
4. Follow the setup wizard to create your project

### 2. Enable Firestore Database
1. In your Firebase project console, go to "Firestore Database"
2. Click "Create database"
3. Choose "Start in production mode" (you can change rules later)
4. Select a location for your database (choose one close to your users)

### 3. Create a Service Account
1. In Firebase Console, go to Project Settings (gear icon)
2. Click on the "Service accounts" tab
3. Click "Generate new private key"
4. Download the JSON file
5. Rename it to `firebase-service-account-key.json`
6. Place it in the root directory of your project (same folder as main.py)

### 4. Alternative Setup with Environment Variable
Instead of placing the file in the project directory, you can:
1. Place the JSON file anywhere on your system
2. Set an environment variable: `FIREBASE_SERVICE_ACCOUNT_KEY=path/to/your/service-account-key.json`

## Firestore Database Structure
The application will create the following collections automatically:

### Events Collection
- Document ID: Auto-generated
- Fields:
  - title: string
  - description: string
  - date: string
  - created_at: timestamp

### Registrations Collection
- Document ID: Auto-generated
- Fields:
  - event_id: string (reference to event document)
  - name: string
  - email: string
  - checked_in: boolean
  - feedback_given: boolean
  - created_at: timestamp

### Feedback Collection
- Document ID: Auto-generated
- Fields:
  - registration_id: string (reference to registration document)
  - rating: number
  - comment: string
  - created_at: timestamp

## Security Rules (Optional)
For production, consider setting up Firestore security rules. Go to Firestore Database > Rules and update as needed.

## Installation
1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Make sure your Firebase service account key is properly configured

3. Run the application:
   ```
   python main.py
   ```

## Troubleshooting

### Firebase Import Errors
If you get import errors for firebase_admin, make sure you've installed the requirements:
```
pip install firebase-admin==6.2.0
```

### Authentication Errors
- Ensure your service account key file exists and is properly named
- Check that the path in the environment variable is correct
- Verify that the service account has Firestore permissions

### Permission Errors
- Make sure your Firebase project has Firestore enabled
- Check that your service account has the necessary permissions (typically "Firebase Admin SDK Service Agent")

## Migration from SQLite
If you have existing SQLite data and want to migrate it to Firebase, you would need to:
1. Export data from SQLite
2. Transform the data format (remove auto-increment IDs, adjust data types)
3. Import data into Firestore collections

The new system uses Firebase document IDs instead of integer primary keys, so any existing QR codes or links with integer IDs would need to be regenerated.
