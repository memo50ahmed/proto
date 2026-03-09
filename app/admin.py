from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .models import db, Project, Certification, Competition, Course, Skill, Experience
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin credentials (in production, use database)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = generate_password_hash('admin123')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please login to access admin dashboard', 'danger')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin')
def index():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('admin.login'))

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Get counts for dashboard
    projects_count = Project.query.count()
    certifications_count = Certification.query.count()
    competitions_count = Competition.query.count()
    courses_count = Course.query.count()
    skills_count = Skill.query.count()
    experiences_count = Experience.query.count()
    
    # Get recent items
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
    recent_certifications = Certification.query.order_by(Certification.created_at.desc()).limit(5).all()
    recent_competitions = Competition.query.order_by(Competition.created_at.desc()).limit(5).all()
    recent_courses = Course.query.order_by(Course.created_at.desc()).limit(5).all()
    recent_skills = Skill.query.order_by(Skill.created_at.desc()).limit(5).all()
    recent_experiences = Experience.query.order_by(Experience.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         projects_count=projects_count,
                         certifications_count=certifications_count,
                         competitions_count=competitions_count,
                         courses_count=courses_count,
                         skills_count=skills_count,
                         experiences_count=experiences_count,
                         recent_projects=recent_projects,
                         recent_certifications=recent_certifications,
                         recent_competitions=recent_competitions,
                         recent_courses=recent_courses,
                         recent_skills=recent_skills,
                         recent_experiences=recent_experiences)

# PROJECTS MANAGEMENT
@admin_bp.route('/projects')
@admin_required
def projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=projects)

@admin_bp.route('/projects/add', methods=['GET', 'POST'])
@admin_required
def add_project():
    if request.method == 'POST':
        project = Project(
            title=request.form.get('title'),
            description=request.form.get('description'),
            technologies=request.form.get('technologies'),
            image_url=request.form.get('image_url'),
            live_url=request.form.get('live_url'),
            github_url=request.form.get('github_url'),
            featured='featured' in request.form
        )
        
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/project_form.html', action='Add')

@admin_bp.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.technologies = request.form.get('technologies')
        project.image_url = request.form.get('image_url')
        project.live_url = request.form.get('live_url')
        project.github_url = request.form.get('github_url')
        project.featured = 'featured' in request.form
        project.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/project_form.html', project=project, action='Edit')

@admin_bp.route('/projects/delete/<int:id>')
@admin_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.projects'))

# CERTIFICATIONS MANAGEMENT
@admin_bp.route('/certifications')
@admin_required
def certifications():
    certifications = Certification.query.order_by(Certification.created_at.desc()).all()
    return render_template('admin/certifications.html', certifications=certifications)

@admin_bp.route('/certifications/add', methods=['GET', 'POST'])
@admin_required
def add_certification():
    if request.method == 'POST':
        certification = Certification(
            title=request.form.get('title'),
            issuer=request.form.get('issuer'),
            issue_date=datetime.strptime(request.form.get('issue_date'), '%Y-%m-%d').date() if request.form.get('issue_date') else None,
            expiry_date=datetime.strptime(request.form.get('expiry_date'), '%Y-%m-%d').date() if request.form.get('expiry_date') else None,
            credential_id=request.form.get('credential_id'),
            credential_url=request.form.get('credential_url'),
            image_url=request.form.get('image_url'),
            description=request.form.get('description'),
            featured='featured' in request.form
        )
        
        db.session.add(certification)
        db.session.commit()
        flash('Certification added successfully!', 'success')
        return redirect(url_for('admin.certifications'))
    
    return render_template('admin/certification_form.html', action='Add')

@admin_bp.route('/certifications/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_certification(id):
    certification = Certification.query.get_or_404(id)
    
    if request.method == 'POST':
        certification.title = request.form.get('title')
        certification.issuer = request.form.get('issuer')
        certification.issue_date = datetime.strptime(request.form.get('issue_date'), '%Y-%m-%d').date() if request.form.get('issue_date') else None
        certification.expiry_date = datetime.strptime(request.form.get('expiry_date'), '%Y-%m-%d').date() if request.form.get('expiry_date') else None
        certification.credential_id = request.form.get('credential_id')
        certification.credential_url = request.form.get('credential_url')
        certification.image_url = request.form.get('image_url')
        certification.description = request.form.get('description')
        certification.featured = 'featured' in request.form
        certification.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Certification updated successfully!', 'success')
        return redirect(url_for('admin.certifications'))
    
    return render_template('admin/certification_form.html', certification=certification, action='Edit')

@admin_bp.route('/certifications/delete/<int:id>')
@admin_required
def delete_certification(id):
    certification = Certification.query.get_or_404(id)
    db.session.delete(certification)
    db.session.commit()
    flash('Certification deleted successfully!', 'success')
    return redirect(url_for('admin.certifications'))

# COMPETITIONS MANAGEMENT
@admin_bp.route('/competitions')
@admin_required
def competitions():
    competitions = Competition.query.order_by(Competition.created_at.desc()).all()
    return render_template('admin/competitions.html', competitions=competitions)

@admin_bp.route('/competitions/add', methods=['GET', 'POST'])
@admin_required
def add_competition():
    if request.method == 'POST':
        competition = Competition(
            title=request.form.get('title'),
            organization=request.form.get('organization'),
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else None,
            position=request.form.get('position'),
            project_name=request.form.get('project_name'),
            project_description=request.form.get('project_description'),
            image_url=request.form.get('image_url'),
            competition_url=request.form.get('competition_url'),
            featured='featured' in request.form
        )
        
        db.session.add(competition)
        db.session.commit()
        flash('Competition added successfully!', 'success')
        return redirect(url_for('admin.competitions'))
    
    return render_template('admin/competition_form.html', action='Add')

@admin_bp.route('/competitions/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_competition(id):
    competition = Competition.query.get_or_404(id)
    
    if request.method == 'POST':
        competition.title = request.form.get('title')
        competition.organization = request.form.get('organization')
        competition.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else None
        competition.position = request.form.get('position')
        competition.project_name = request.form.get('project_name')
        competition.project_description = request.form.get('project_description')
        competition.image_url = request.form.get('image_url')
        competition.competition_url = request.form.get('competition_url')
        competition.featured = 'featured' in request.form
        competition.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Competition updated successfully!', 'success')
        return redirect(url_for('admin.competitions'))
    
    return render_template('admin/competition_form.html', competition=competition, action='Edit')

@admin_bp.route('/competitions/delete/<int:id>')
@admin_required
def delete_competition(id):
    competition = Competition.query.get_or_404(id)
    db.session.delete(competition)
    db.session.commit()
    flash('Competition deleted successfully!', 'success')
    return redirect(url_for('admin.competitions'))

# COURSES MANAGEMENT
@admin_bp.route('/courses')
@admin_required
def courses():
    courses = Course.query.order_by(Course.created_at.desc()).all()
    return render_template('admin/courses.html', courses=courses)

@admin_bp.route('/courses/add', methods=['GET', 'POST'])
@admin_required
def add_course():
    if request.method == 'POST':
        course = Course(
            title=request.form.get('title'),
            provider=request.form.get('provider'),
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None,
            end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None,
            duration=request.form.get('duration'),
            certificate_url=request.form.get('certificate_url'),
            image_url=request.form.get('image_url'),
            description=request.form.get('description'),
            skills_learned=request.form.get('skills_learned'),
            featured='featured' in request.form
        )
        
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('admin.courses'))
    
    return render_template('admin/course_form.html', action='Add')

@admin_bp.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_course(id):
    course = Course.query.get_or_404(id)
    
    if request.method == 'POST':
        course.title = request.form.get('title')
        course.provider = request.form.get('provider')
        course.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None
        course.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None
        course.duration = request.form.get('duration')
        course.certificate_url = request.form.get('certificate_url')
        course.image_url = request.form.get('image_url')
        course.description = request.form.get('description')
        course.skills_learned = request.form.get('skills_learned')
        course.featured = 'featured' in request.form
        course.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('admin.courses'))
    
    return render_template('admin/course_form.html', course=course, action='Edit')

@admin_bp.route('/courses/delete/<int:id>')
@admin_required
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('admin.courses'))

# Skills Management Routes
@admin_bp.route('/skills')
@admin_required
def skills():
    skills = Skill.query.order_by(Skill.category, Skill.name).all()
    return render_template('admin/skills.html', skills=skills)

@admin_bp.route('/skills/add', methods=['GET', 'POST'])
@admin_required
def add_skill():
    if request.method == 'POST':
        skill = Skill(
            name=request.form.get('name'),
            category=request.form.get('category'),
            proficiency=int(request.form.get('proficiency', 50)),
            years_experience=float(request.form.get('years_experience')) if request.form.get('years_experience') else None,
            description=request.form.get('description'),
            featured='featured' in request.form
        )
        db.session.add(skill)
        db.session.commit()
        flash('Skill added successfully!', 'success')
        return redirect(url_for('admin.skills'))
    
    return render_template('admin/skill_form.html', action='Add')

@admin_bp.route('/skills/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_skill(id):
    skill = Skill.query.get_or_404(id)
    
    if request.method == 'POST':
        skill.name = request.form.get('name')
        skill.category = request.form.get('category')
        skill.proficiency = int(request.form.get('proficiency', 50))
        skill.years_experience = float(request.form.get('years_experience')) if request.form.get('years_experience') else None
        skill.description = request.form.get('description')
        skill.featured = 'featured' in request.form
        skill.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Skill updated successfully!', 'success')
        return redirect(url_for('admin.skills'))
    
    return render_template('admin/skill_form.html', skill=skill, action='Edit')

@admin_bp.route('/skills/delete/<int:id>')
@admin_required
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('admin.skills'))

# Experience Management Routes
@admin_bp.route('/experiences')
@admin_required
def experiences():
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    return render_template('admin/experiences.html', experiences=experiences)

@admin_bp.route('/experiences/add', methods=['GET', 'POST'])
@admin_required
def add_experience():
    if request.method == 'POST':
        experience = Experience(
            title=request.form.get('title'),
            company=request.form.get('company'),
            location=request.form.get('location'),
            employment_type=request.form.get('employment_type'),
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None,
            end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None,
            description=request.form.get('description'),
            responsibilities=request.form.get('responsibilities'),
            achievements=request.form.get('achievements'),
            technologies_used=request.form.get('technologies_used'),
            featured='featured' in request.form,
            current='current' in request.form
        )
        db.session.add(experience)
        db.session.commit()
        flash('Experience added successfully!', 'success')
        return redirect(url_for('admin.experiences'))
    
    return render_template('admin/experience_form.html', action='Add')

@admin_bp.route('/experiences/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_experience(id):
    experience = Experience.query.get_or_404(id)
    
    if request.method == 'POST':
        experience.title = request.form.get('title')
        experience.company = request.form.get('company')
        experience.location = request.form.get('location')
        experience.employment_type = request.form.get('employment_type')
        experience.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None
        experience.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None
        experience.description = request.form.get('description')
        experience.responsibilities = request.form.get('responsibilities')
        experience.achievements = request.form.get('achievements')
        experience.technologies_used = request.form.get('technologies_used')
        experience.featured = 'featured' in request.form
        experience.current = 'current' in request.form
        experience.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Experience updated successfully!', 'success')
        return redirect(url_for('admin.experiences'))
    
    return render_template('admin/experience_form.html', experience=experience, action='Edit')

@admin_bp.route('/experiences/delete/<int:id>')
@admin_required
def delete_experience(id):
    experience = Experience.query.get_or_404(id)
    db.session.delete(experience)
    db.session.commit()
    flash('Experience deleted successfully!', 'success')
    return redirect(url_for('admin.experiences'))
