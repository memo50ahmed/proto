from flask import Blueprint, render_template, request, jsonify
from .models import Project, Certification, Competition, Course, Skill,Experience

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    # Get featured projects for homepage
    featured_projects = Project.query.filter_by(featured=True).order_by(Project.created_at.desc()).all()
    
    # Get featured skills for homepage
    featured_skills = Skill.query.filter_by(featured=True).order_by(Skill.proficiency.desc()).limit(6).all()
    
    return render_template('index.html', featured_projects=featured_projects, featured_skills=featured_skills)

@main_bp.route('/about')
def about():
    # Get data for about page
    certifications = Certification.query.filter_by(featured=True).order_by(Certification.created_at.desc()).limit(3).all()
    competitions = Competition.query.filter_by(featured=True).order_by(Competition.created_at.desc()).limit(3).all()
    courses = Course.query.filter_by(featured=True).order_by(Course.created_at.desc()).limit(3).all()
    skills = Skill.query.filter_by(featured=True).order_by(Skill.proficiency.desc()).limit(8).all()
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    return render_template('about.html', 
                         certifications=certifications,
                         competitions=competitions,
                         courses=courses,
                         skills=skills,
                         experiences=experiences)

@main_bp.route('/projects')
def projects_page():
    # Get all projects from database
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('projects.html', projects=projects)

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/api/contact', methods=['POST'])
def contact_form():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        # Here you would typically send an email or save to database
        # For now, just return success response
        return jsonify({
            'success': True,
            'message': 'Thank you for your message! I\'ll get back to you soon.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Sorry, there was an error sending your message.'
        }), 400

@main_bp.route('/api/projects')
def api_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return jsonify([{
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'technologies': project.get_technologies_list(),
        'image': project.image_url,
        'live_url': project.live_url,
        'github_url': project.github_url,
        'featured': project.featured
    } for project in projects])

@main_bp.route('/api/skills')
def api_skills():
    from flask import current_app
    return jsonify(current_app.jinja_env.globals['skills'])
from datetime import datetime
from .models import db, Experience, Skill, Course, Certification, Project

@main_bp.route('/seed-all-data')
def seed_all_data():
    try:
        # مسح الداتا القديمة لضمان عدم التكرار

        # 1. المهارات (Skills)
        skills = [
            Skill(name='Python (Flask)', category='Backend', proficiency=90, featured=True),
            Skill(name='Microsoft SQL Server', category='Database', proficiency=85, featured=True),
            Skill(name='HTML & CSS', category='Frontend', proficiency=95, featured=True),
            Skill(name='JavaScript', category='Frontend', proficiency=80, featured=True),
            Skill(name='Web Accessibility', category='Specialized', proficiency=90, featured=True),
            Skill(name='Jinja2', category='Templating', proficiency=85, featured=True)
        ]
        # 4. إضافة الكورسات (Courses)
        courses = [
            Course(
                title='Digital Egypt Marvels Initiative (DEMI)',
                provider='MCIT Egypt',
                description='Advanced software engineering track.',
                featured=True
            )
        ]
        
        # 2. الخبرات (Experience)
        experiences = [
            Experience(
                title='Python Developer',
                company='Exploratory Education Center',
                description='Developed projects using Python from basic to advanced concepts. Enhanced problem-solving skills through competitions.',
                start_date=datetime(2023, 5, 1),
                featured=True
            ),
            Experience(
                title='Software Engineering Student',
                company='Ministry of Communications (MCIT)',
                description='Hands-on experience with Flask, HTML, CSS, and JavaScript. Studied game development using Godot Engine.',
                start_date=datetime(2023, 8, 1),
                end_date=datetime(2024, 5, 1),
                featured=True
            )
        ]

        db.session.add_all(experiences)
  
        
        db.session.commit()
        return "🔥 كدة كله تمام! الخبرات والمهارات والشهادات والمشاريع انضافت بنجاح."

    except Exception as e:
        db.session.rollback()
        return f"❌ حصل خطأ: {str(e)}"