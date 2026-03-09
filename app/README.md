# Portfolio Website

A modern, responsive portfolio website built with HTML, CSS, JavaScript frontend and Flask backend.

## Features

- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern UI**: Clean, professional design with smooth animations and transitions
- **Contact Form**: Functional contact form with validation
- **Project Showcase**: Dynamic project display with filtering capabilities
- **Skills Section**: Animated skill bars showing technical proficiencies
- **About Page**: Personal information and experience timeline
- **Social Links**: Integrated social media links

## Tech Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations and transitions
- **JavaScript**: Interactive features and form handling
- **Font Awesome**: Icon library

### Backend
- **Flask**: Python web framework
- **Jinja2**: Template engine
- **python-dotenv**: Environment variable management

## Project Structure

```
protofile/
├── app/                   # Main application package
│   ├── static/           # Static files
│   │   ├── css/
│   │   │   └── style.css # Main stylesheet
│   │   ├── js/
│   │   │   └── main.js   # JavaScript functionality
│   │   └── images/       # Image assets
│   ├── templates/       # HTML templates
│   │   ├── base.html     # Base template
│   │   ├── index.html    # Home page
│   │   ├── about.html    # About page
│   │   ├── projects.html # Projects page
│   │   └── contact.html  # Contact page
│   ├── __init__.py       # App factory and configuration
│   ├── routes.py         # Route definitions
│   ├── run.py           # Application runner
│   ├── .env             # Environment variables
│   ├── requirements.txt  # Python dependencies
│   └── README.md        # This file
└── venv/                # Virtual environment (outside app folder)
```

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Edit the `.env` file and update the following variables:
- `PORTFOLIO_NAME`: Your name
- `PORTFOLIO_EMAIL`: Your email address
- `GITHUB_URL`: Your GitHub profile URL
- `LINKEDIN_URL`: Your LinkedIn profile URL
- `TWITTER_URL`: Your Twitter profile URL

### 5. Navigate to App Folder and Run
```bash
cd app
python run.py
```

The application will be available at `http://localhost:5000`

## Customization

### Adding Projects
Edit the `projects` list in `__init__.py` to add your own projects:

```python
projects = [
    {
        'id': 1,
        'title': 'Your Project Title',
        'description': 'Project description',
        'technologies': ['Python', 'Flask', 'HTML', 'CSS'],
        'image': 'project-image.jpg',
        'live_url': 'https://your-project-url.com',
        'github_url': 'https://github.com/yourusername/project'
    }
]
```

### Updating Skills
Edit the `skills` list in `__init__.py` to reflect your technical skills:

```python
skills = [
    {'name': 'Python', 'level': 90, 'category': 'Programming'},
    {'name': 'JavaScript', 'level': 85, 'category': 'Programming'}
]
```

### Customizing Styles
- Edit `static/css/style.css` to modify colors, fonts, and layout
- The CSS is well-organized with clear sections for easy customization

### Adding Images
- Add your images to the `static/images/` directory
- Update the image paths in the templates and CSS

## API Endpoints

The application provides the following API endpoints:

- `GET /api/projects` - Returns all projects as JSON
- `GET /api/skills` - Returns all skills as JSON
- `POST /api/contact` - Handles contact form submissions

## Deployment

### Heroku
1. Create a `Procfile` with: `web: python app.py`
2. Set environment variables in Heroku dashboard
3. Deploy using Heroku CLI

### Vercel
1. Install Vercel CLI
2. Run `vercel` in project directory
3. Configure environment variables in Vercel dashboard

### Docker
A `Dockerfile` can be created for containerized deployment.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

If you have any questions or need support, feel free to reach out through the contact form on the website or via email.

---

**Built with ❤️ using Flask, HTML, CSS, and JavaScript**
