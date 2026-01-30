# BloodShare

A responsive web application that connects blood donors and recipients, built with Django, HTML, CSS, and vanilla JavaScript.

## Features

### Public Features
- **Modern Landing Page**: Conversion-focused design with clear CTAs
- **How It Works**: 3-step process explanation
- **Live Stats**: Display of active donors, lives saved, and active requests
- **Testimonials**: Social proof section
- **Responsive Navigation**: Mobile-friendly hamburger menu

### Authentication
- **Sign Up**: Full registration with profile creation
  - Full name, email, password validation
  - Password strength indicator
  - Optional: phone, blood group, city, avatar
  - Terms agreement required
- **Sign In**: Email and password authentication
  - Remember me option
  - Secure password handling
- **Sign Out**: CSRF-protected logout with confirmation message

### Authenticated Dashboard
- **Profile Management**: View and edit profile information
- **Availability Toggle**: AJAX-powered toggle to mark availability
- **Donation Requests**: 
  - Create new donation requests
  - View your requests
  - Browse active requests from other users
- **Profile Card**: Display phone, city, blood group, last donation date

## Technology Stack

- **Backend**: Django 4.2
- **Database**: SQLite (development)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: Django Auth System
- **Image Handling**: Pillow

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create sample users** (optional):
   ```bash
   python create_sample_users.py
   ```
   This creates 5 sample users with various blood groups and cities.
   Password for all sample users: `SamplePass123!`

6. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Sample Users

After running `create_sample_users.py`, you can login with:

| Email | Blood Group | City | Available |
|-------|-------------|------|-----------|
| alice.johnson@example.com | O+ | New York | Yes |
| bob.smith@example.com | A+ | Los Angeles | Yes |
| charlie.brown@example.com | B+ | Chicago | No |
| diana.prince@example.com | AB+ | Houston | Yes |
| edward.norton@example.com | O- | Phoenix | Yes |

**Password for all**: `SamplePass123!`

## Project Structure

```
BloodShare/
├── bloodshare/              # Main Django app
│   ├── models.py           # Profile and DonationRequest models
│   ├── views.py            # View functions
│   ├── forms.py            # Django forms
│   ├── urls.py             # App URL routing
│   ├── tests.py            # Unit tests
│   └── fixtures/           # Sample data fixtures
├── bloodshare_project/     # Django project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI configuration
├── templates/              # HTML templates
│   └── bloodshare/
│       ├── base.html
│       ├── landing.html
│       ├── signup.html
│       ├── login.html
│       └── dashboard.html
├── static/                 # Static files
│   ├── css/
│   │   └── main.css        # Main stylesheet
│   └── js/
│       └── app.js          # Main JavaScript
├── media/                  # User-uploaded files (avatars)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Design & Accessibility

### Color Scheme
- **Primary Red**: #d9534f (soft red accent)
- **Maroon**: #8b1538 (deep maroon for headers)
- **Neutrals**: Warm grays and whites
- **Success/Error**: Standard semantic colors

### Typography
- **Font**: Poppins (Google Fonts)
- **Headings**: Large, legible, rounded sans-serif
- **Body**: Clean, readable text

### UI Patterns
- Cards with subtle shadows
- Pill-shaped buttons
- Micro-interactions (hover effects, fade-ins)
- Mobile-first responsive design

### Accessibility Features
- ARIA labels and roles
- Keyboard navigation support
- Focus indicators
- Semantic HTML
- Screen reader friendly
- Reduced motion support

## Security Features

- **Password Hashing**: Django's PBKDF2 password hashing
- **CSRF Protection**: All forms protected with CSRF tokens
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **XSS Protection**: Django template auto-escaping
- **Secure Authentication**: Django's built-in auth system

## Testing

Run the test suite:

```bash
python manage.py test
```

The test suite includes:
- Model behavior tests (Profile, DonationRequest)
- Signup flow tests
- Login flow tests
- Dashboard access tests

## API Endpoints

### Authenticated Endpoints

- `POST /api/profile/toggle-availability/` - Toggle donor availability
  - Returns JSON: `{success: true, is_available: boolean, message: string}`

## Development Notes

### Static Files
Static files are served from the `static/` directory. In production, run:
```bash
python manage.py collectstatic
```

### Media Files
User-uploaded avatars are stored in `media/avatars/`. Make sure the `media/` directory exists.

### Database
The project uses SQLite for development. For production, configure PostgreSQL or MySQL in `settings.py`.

## Future Enhancements (Stretch Goals)

- Password reset functionality
- Email notifications
- Donor-recipient matching algorithm
- Search and filter functionality
- Donation history tracking
- Third-party authentication (OAuth)
- Real-time notifications
- Mobile app API

## License

This project is created for educational/demonstration purposes.

## Contributing

This is a demonstration project. For production use, consider:
- Adding comprehensive error handling
- Implementing rate limiting
- Adding email verification
- Setting up proper logging
- Configuring production database
- Setting up CI/CD pipeline
- Adding more comprehensive tests

## Support

For issues or questions, please refer to the Django documentation or create an issue in the repository.

