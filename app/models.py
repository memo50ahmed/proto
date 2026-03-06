from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(500), nullable=False)  # Comma-separated list
    image_url = db.Column(db.String(500), nullable=True)
    live_url = db.Column(db.String(500), nullable=True)
    github_url = db.Column(db.String(500), nullable=True)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Project {self.title}>'
    
    def get_technologies_list(self):
        """Convert technologies string to list"""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',')]
        return []
    
    def set_technologies_list(self, tech_list):
        """Convert list to technologies string"""
        self.technologies = ', '.join(tech_list) if tech_list else ''

class Certification(db.Model):
    __tablename__ = 'certifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=True)
    credential_id = db.Column(db.String(100), nullable=True)
    credential_url = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Certification {self.title}>'

class Competition(db.Model):
    __tablename__ = 'competitions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    organization = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    position = db.Column(db.String(100), nullable=True)  # e.g., "First Place", "Finalist"
    project_name = db.Column(db.String(200), nullable=True)
    project_description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    competition_url = db.Column(db.String(500), nullable=True)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Competition {self.title}>'

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    provider = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    duration = db.Column(db.String(100), nullable=True)  # e.g., "3 months", "40 hours"
    certificate_url = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    skills_learned = db.Column(db.String(500), nullable=True)  # Comma-separated list
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Course {self.title}>'
    
    def get_skills_list(self):
        """Convert skills_learned string to list"""
        if self.skills_learned:
            return [skill.strip() for skill in self.skills_learned.split(',')]
        return []
    
    def set_skills_list(self, skills_list):
        """Convert list to skills_learned string"""
        self.skills_learned = ', '.join(skills_list) if skills_list else ''

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)  # e.g., 'Programming', 'Design', 'Tools'
    proficiency = db.Column(db.Integer, nullable=False, default=50)  # 0-100 percentage
    years_experience = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=True)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Skill {self.name} ({self.proficiency}%)>'
    
    def get_proficiency_level(self):
        """Return proficiency level as text"""
        if self.proficiency >= 90:
            return "Expert"
        elif self.proficiency >= 75:
            return "Advanced"
        elif self.proficiency >= 60:
            return "Intermediate"
        elif self.proficiency >= 40:
            return "Beginner"
        else:
            return "Learning"

class Experience(db.Model):
    __tablename__ = 'experiences'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    employment_type = db.Column(db.String(50), nullable=True)  # Full-time, Part-time, Contract, Freelance, Internship
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)  # Null for current position
    description = db.Column(db.Text, nullable=True)
    responsibilities = db.Column(db.Text, nullable=True)  # Bullet points of responsibilities
    achievements = db.Column(db.Text, nullable=True)  # Bullet points of achievements
    technologies_used = db.Column(db.String(500), nullable=True)  # Comma-separated list
    featured = db.Column(db.Boolean, default=False)
    current = db.Column(db.Boolean, default=False)  # Currently working here
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Experience {self.title} at {self.company}>'
    
    def get_technologies_list(self):
        """Convert technologies_used string to list"""
        if self.technologies_used:
            return [tech.strip() for tech in self.technologies_used.split(',')]
        return []
    
    def set_technologies_list(self, technologies_list):
        """Convert list to technologies_used string"""
        self.technologies_used = ', '.join(technologies_list) if technologies_list else ''
    
    def get_duration(self):
        """Calculate duration of employment"""
        if not self.start_date:
            return "Unknown"
        
        end = self.end_date or datetime.now().date()
        start = self.start_date
        
        years = end.year - start.year
        months = end.month - start.month
        
        if months < 0:
            years -= 1
            months += 12
        
        if years > 0:
            return f"{years} year{'s' if years != 1 else ''} {months} month{'s' if months != 1 else ''}" if months > 0 else f"{years} year{'s' if years != 1 else ''}"
        else:
            return f"{months} month{'s' if months != 1 else ''}"
    
    def is_current(self):
        """Check if this is a current position"""
        return self.current or self.end_date is None

# Helper function to create all tables
def create_tables():
    """Create all database tables"""
    db.create_all()

# Helper function to drop all tables
def drop_tables():
    """Drop all database tables"""
    db.drop_all()
