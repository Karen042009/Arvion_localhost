# Arvion - Medical Information Management System

## 📋 Overview

Arvion is a comprehensive Django-based web application designed for secure medical information management and patient-doctor collaboration. The system implements facial recognition technology for identity verification and provides comprehensive medical record management capabilities.

## ✨ Core Features

### Patient Features

- **Secure Registration & Authentication**
  - Email-based registration with strong password requirements
  - Two-role system (Patient/Doctor)
  - Secure session management
- **Medical Profile Management**
  - Complete health profile with personal information
  - Medical history tracking
  - Emergency contact information
  - Biometric data (height, weight)
- **Health Records**
  - Track diagnosed conditions with dates
  - Medication management with dosages
  - Surgical history documentation
  - Allergy tracking
  - Blood group information
- **Biometric Features**
  - Upload and manage facial recognition images
  - Automatic face detection validation
  - QR code generation for profile sharing
  - Unique public profile ID
- **Photo Management**
  - Upload multiple facial images for training recognition models
  - Delete unwanted photos
  - Image validation

### Doctor Features

- **Patient Discovery**
  - Search patients by facial recognition
  - Advanced face matching with confidence scores
- **Patient Access**
  - View detailed patient medical records
  - Access complete health history
  - Review all medical conditions, medications, surgeries
- **Profile Management**
  - Maintain professional credentials
  - Store specialization and license information
  - Update workplace information

### System Features

- **Face Recognition Engine**
  - FaceNet-based facial embedding extraction
  - SVM and KNN classification models
  - Automatic model selection based on user count
  - Confidence-based matching
- **Database Management**
  - Comprehensive Django ORM implementation
  - Support for SQLite and PostgreSQL
  - Transaction-based data consistency
- **File Storage**
  - Local filesystem support for development
  - Cloudinary integration for production
  - Organized media structure by user email

## 🏗️ Project Architecture

### Directory Structure

```
Arvion_localhost/
├── Arvion/                              # Django Project Configuration
│   ├── __init__.py
│   ├── asgi.py                         # ASGI application configuration
│   ├── settings.py                     # Django settings (DB, middleware, apps)
│   ├── urls.py                         # Project-level URL routing
│   └── wsgi.py                         # WSGI application configuration
│
├── main/                                # Main Django Application
│   ├── __init__.py
│   ├── admin.py                        # Django admin configuration
│   ├── apps.py                         # Application configuration
│   ├── models.py                       # Database models (234 lines)
│   ├── views.py                        # HTTP request handlers (440 lines)
│   ├── tests.py                        # Unit tests
│   ├── urls.py                         # Application URL patterns
│   ├── face_recognition_service.py     # Face recognition logic
│   ├── management/
│   │   └── commands/
│   │       └── train_face_model.py    # Model training management command
│   ├── handlers/                       # Request handlers
│   │   ├── chat_handlers.py
│   │   ├── common_handlers.py
│   │   ├── learning_handlers.py
│   │   ├── settings_handlers.py
│   │   └── translate_handlers.py
│   ├── keyboards/                      # UI components
│   │   ├── inline.py
│   │   └── reply.py
│   ├── middlewares/                    # Custom middleware
│   │   └── localization.py
│   ├── services/                       # Business logic
│   │   ├── gemini_service.py
│   │   └── tts_service.py
│   ├── states/                         # Application states
│   │   └── app_states.py
│   └── utils/                          # Utility functions
│       └── message_utils.py
│
├── templates/                           # HTML Templates
│   ├── arvion.html
│   ├── about_project.html
│   ├── register.html
│   ├── login.html
│   ├── profile.html
│   ├── settings.html
│   ├── add_photo.html
│   ├── search_patient_by_photo.html
│   ├── patient_details.html
│   ├── qr_code.html
│   └── find_hospital.html
│
├── static/                              # Static Files
│   └── css/
│       └── styles.css
│
├── manage.py                            # Django management script
├── create_admin.py                      # Admin user creation script
├── requirements.txt                     # Python dependencies
├── build.sh                             # Build script
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

## 🗄️ Database Models

### User Management Models

#### CustomUser (Extended Django User)

```python
- username, email, password (inherited from Django)
- first_name, last_name
- date_of_birth
- gender (ForeignKey)
- phone_number
- address
- emergency_contact_phone
- profile_picture (ImageField)
- public_profile_id (UUID - for QR codes)
- date_joined, last_login
```

#### PatientProfile (OneToOne with CustomUser)

```python
- user (OneToOne)
- blood_group (ForeignKey)
- weight_kg (Decimal)
- height_cm (Decimal)
- other_notes (TextField)
- conditions (ManyToMany through PatientCondition)
- medications (ManyToMany through PatientMedication)
- surgeries (ManyToMany through PatientSurgery)
- allergies (ManyToMany)
```

#### DoctorProfile (OneToOne with CustomUser)

```python
- user (OneToOne)
- specialty (CharField)
- license_number (CharField, Unique)
- workplace (CharField)
- biography (TextField)
```

### Medical Data Models

#### Gender

```python
- name (CharField, Unique)
```

#### BloodGroup

```python
- group_name (CharField, Unique)
```

#### Condition (BaseMedicalTerm)

```python
- name (CharField, Unique, Abstract base)
- Subclasses: Condition, Medication, Surgery, Allergy
```

#### Medication (BaseMedicalTerm)

```python
- name (CharField, Unique)
```

#### Surgery (BaseMedicalTerm)

```python
- name (CharField, Unique)
```

#### Allergy (BaseMedicalTerm)

```python
- name (CharField, Unique)
```

### Relationship Models

#### PatientCondition

```python
- patient (ForeignKey to PatientProfile)
- condition (ForeignKey to Condition)
- diagnosis_date (DateField)
- unique_together = ('patient', 'condition')
```

#### PatientMedication

```python
- patient (ForeignKey to PatientProfile)
- medication (ForeignKey to Medication)
- dosage (CharField)
- start_date (DateField)
- notes (TextField)
- unique_together = ('patient', 'medication')
```

#### PatientSurgery

```python
- patient (ForeignKey to PatientProfile)
- surgery (ForeignKey to Surgery)
- surgery_date (DateField)
- notes (TextField)
- unique_together = ('patient', 'surgery')
```

#### UserFaceImage (For Face Recognition)

```python
- user (ForeignKey to CustomUser)
- image (ImageField)
- uploaded_at (DateTimeField, auto_now_add)
- Ordering: -uploaded_at
```

## 🔧 Technologies & Dependencies

### Backend Framework

- **Django 5.2+** - Web framework
- **Python 3.10+** - Programming language

### Database

- **SQLite3** - Development database
- **PostgreSQL** - Production database (with dj-database-url)

### Face Recognition & ML

- **FaceNet** (keras_facenet) - Facial embedding extraction
- **OpenCV (cv2)** - Image processing
- **scikit-learn** - Machine learning
  - SVM (Support Vector Machine) for multi-user classification
  - KNN (K-Nearest Neighbors) for single-user scenarios
- **NumPy** - Numerical computing

### File & Storage

- **Cloudinary** - Cloud storage (production)
- **WhiteNoise** - Static file serving

### Utilities

- **python-dotenv** - Environment variable management
- **qrcode** - QR code generation
- **Pillow** - Image processing
- **requests** - HTTP requests

### Development Tools

- **Django Debug Toolbar** - Debugging
- **pytest-django** - Testing framework

## 🚀 Installation Guide

### Prerequisites

```bash
- Python 3.10 or higher
- pip or conda
- Virtual environment tool (venv)
- Git
```

### Step-by-Step Setup

1. **Clone and Navigate**

```bash
cd Arvion_localhost
```

2. **Create Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
   Create `.env` file in project root:

```env
SECRET_KEY=your-secret-key-generate-one
DEBUG=1
DATABASE_URL=postgresql://user:password@localhost:5432/arvion
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
CLOUDINARY_URL=cloudinary://api-key:api-secret@cloud-name
RENDER_EXTERNAL_HOSTNAME=your-domain.com
```

5. **Database Initialization**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create Superuser**

```bash
# Option 1: Interactive
python manage.py createsuperuser

# Option 2: Script
python create_admin.py
```

7. **Train Face Recognition Model**

```bash
python manage.py train_face_model
```

8. **Run Development Server**

```bash
python manage.py runserver
```

Access: `http://localhost:8000`

## 📡 API Endpoints

### Authentication Endpoints

| Method | Endpoint      | Purpose               |
| ------ | ------------- | --------------------- |
| POST   | `/api/login/` | User login (JSON)     |
| GET    | `/logout/`    | User logout           |
| POST   | `/register/`  | New user registration |

### Patient Endpoints

| Method | Endpoint              | Purpose                           |
| ------ | --------------------- | --------------------------------- |
| GET    | `/`                   | Homepage                          |
| GET    | `/profile/`           | View own profile (requires login) |
| POST   | `/settings/`          | Update profile information        |
| POST   | `/add-photo/`         | Upload facial recognition image   |
| DELETE | `/delete-photo/<id>/` | Remove photo                      |
| GET    | `/qr-code/`           | Generate QR code (requires login) |
| POST   | `/find-hospital/`     | Hospital finder                   |

### Doctor Endpoints

| Method | Endpoint         | Purpose                              |
| ------ | ---------------- | ------------------------------------ |
| POST   | `/search/photo/` | Search patient by facial recognition |
| GET    | `/patient/<id>/` | View patient details                 |

### Public Endpoints

| Method | Endpoint           | Purpose              |
| ------ | ------------------ | -------------------- |
| GET    | `/about/`          | About project        |
| GET    | `/how-it-works/`   | How it works guide   |
| GET    | `/terms-privacy/`  | Terms and privacy    |
| GET    | `/security/`       | Security information |
| GET    | `/status/`         | System status        |
| GET    | `/profile/<uuid>/` | Public profile view  |

## ⚙️ Management Commands

### Train Face Recognition Model

```bash
python manage.py train_face_model
```

**Functionality:**

- Collects all user face images from database
- Downloads images from Cloudinary if in production
- Extracts FaceNet embeddings from each image
- Trains appropriate model:
  - **SVM** if 2+ users (advanced classification)
  - **KNN** if 1 user (simple classification)
- Saves model to `face_models/facenet_model.pkl`

**Output:**

- Total faces processed count
- Unique users identified
- Model type and accuracy metrics
- Model saved location

## 🔒 Security Features

### Authentication & Authorization

- CSRF protection on all forms
- Secure password hashing (PBKDF2)
- Session-based authentication
- Role-based access control (Patient/Doctor)
- Login required decorators on sensitive views
- Django's built-in user authentication

### Data Protection

- SQL injection prevention through ORM
- SQL parameterization for all queries
- Secure file upload validation
- Face detection before image storage
- Email validation on registration

### Network Security

- HTTPS support (production)
- Secure cookie settings (production)
- SSL/TLS enforcement (production)
- X-Frame-Options header
- Security middleware stack

### File Security

- Organized media storage by user email
- Secure file path generation
- Image validation (face detection)
- Unique file naming with user context

## 🎯 Face Recognition System

### How It Works

1. **Image Upload**
   - User uploads facial photo
   - Automatic face detection validation
   - Image stored in media/face/<email>/ directory

2. **Embedding Extraction**
   - FaceNet extracts 128-dimensional facial embedding
   - Uses Keras-FaceNet pre-trained model
   - Handles face detection and normalization

3. **Model Training**
   - Management command processes all images
   - Creates embedding dataset with user IDs
   - Trains classification model

4. **Face Recognition**
   - Doctor uploads search photo
   - Embedding extracted from search image
   - Compared against trained model
   - Returns matching patient with confidence score

### Model Selection

- **SVM (2+ users)**: Advanced classification with probability scores
- **KNN (1 user)**: Simple single-user identification

### Confidence Thresholds

- SVM: 75% minimum confidence
- KNN: Distance threshold of 0.7

## 📊 Configuration Details

### Django Settings (settings.py)

- **BASE_DIR**: Project base directory
- **SECRET_KEY**: Loaded from environment
- **DEBUG**: Environment-dependent
- **ALLOWED_HOSTS**: localhost, 127.0.0.1, and external hostname
- **INSTALLED_APPS**: 10 apps including Django core and project apps
- **MIDDLEWARE**: 8 middleware components for security and functionality

### Database Configuration

- **Development**: SQLite3
- **Production**: PostgreSQL via DATABASE_URL
- **Connection pooling**: 600 second max age

### Static & Media Files

- **STATIC_ROOT**: staticfiles/
- **STATIC_URL**: /static/
- **MEDIA_ROOT**: media/ (local) or Cloudinary (production)
- **MEDIA_URL**: /media/
- **Storage**: WhiteNoise (compressed) for production

### Templates

- **DIRS**: templates/
- **APP_DIRS**: Enabled
- **Context Processors**: debug, request, auth, messages

## 🧪 Testing

### Running Tests

```bash
python manage.py test
```

### Test Files

- `main/tests.py` - Application tests

## 📦 Requirements.txt Dependencies

Core dependencies include:

- Django framework and extensions
- PostgreSQL driver (psycopg2)
- Face recognition libraries (keras-facenet, cv2)
- ML libraries (scikit-learn)
- Cloudinary integration
- QR code generation
- Image processing (Pillow)
- Environment management (python-dotenv)
- Static file handling (whitenoise)

## 🐛 Troubleshooting

### Face Recognition Issues

```bash
# Issue: No faces detected
# Solution: Ensure clear, frontal photos
# Retrain model:
python manage.py train_face_model

# Issue: Low confidence scores
# Solution: Add more training images
python manage.py train_face_model
```

### Database Issues

```bash
# Reset migrations
python manage.py migrate --fake main zero
python manage.py migrate

# Create fresh database
python manage.py flush  # WARNING: Deletes all data
python manage.py migrate
```

### Static Files Issues

```bash
# Collect static files
python manage.py collectstatic --noinput

# Check static files location
ls staticfiles/
```

### Image Upload Issues

```bash
# Check media directory permissions
chmod -R 755 media/

# Verify Cloudinary configuration
python manage.py shell
# Then test: from django.conf import settings; print(settings.DEFAULT_FILE_STORAGE)
```

## 📝 Usage Examples

### Register as Patient

1. Navigate to `/register/`
2. Select "Patient" role
3. Enter personal information
4. Create secure password
5. Verify registration success

### Upload Face Photos

1. Login as patient
2. Go to `/add-photo/`
3. Upload clear facial photo
4. System validates face detection
5. Photo stored for training

### Search Patient (Doctor)

1. Login as doctor
2. Go to `/search/photo/`
3. Upload patient facial photo
4. System performs recognition
5. View matched patient details

### Generate QR Code

1. Login as any user
2. Go to `/qr-code/`
3. QR code displays public profile link
4. Share code with others for profile access

## 🔄 Development Workflow

### Adding New Features

1. Create/modify models in `main/models.py`
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Add views in `main/views.py`
5. Add URLs in `main/urls.py`
6. Create templates in `templates/`
7. Test thoroughly

### Database Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration history
python manage.py showmigrations

# Reverse migration
python manage.py migrate main 0001  # Specific version
```

## 📄 License

Proprietary - Authorized use only. All rights reserved.

## 👥 Support & Contact

For technical support, bug reports, or feature requests, contact the development team.

## 📅 Version History

| Version | Date        | Notes                              |
| ------- | ----------- | ---------------------------------- |
| 1.0.0   | Feb 4, 2026 | Initial release - Production ready |

## 🎓 Project Status

- **Status**: Production Ready ✅
- **Last Updated**: February 4, 2026
- **Maintained By**: Development Team
- **Language**: Armenian/English
- **Locale Support**: Multiple languages via locale files

---

**Arvion Medical System** - Secure, intelligent, patient-centric healthcare management.
