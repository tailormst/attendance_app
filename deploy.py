#!/usr/bin/env python
"""
Deployment script for Attendance Management System
Handles common deployment tasks
"""

import os
import sys
import subprocess
import django
from django.conf import settings

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_environment():
    """Setup the environment for deployment"""
    print("🚀 Setting up Attendance Management System for deployment...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        return False
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_app.settings')
    django.setup()
    
    return True

def deploy_local():
    """Deploy locally"""
    print("\n📦 Local Deployment")
    print("-" * 30)
    
    commands = [
        ("python manage.py makemigrations", "Creating migrations"),
        ("python manage.py migrate", "Running migrations"),
        ("python manage.py collectstatic --noinput", "Collecting static files"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    print("\n✅ Local deployment completed!")
    print("Run 'python manage.py runserver' to start the development server")
    return True

def deploy_heroku():
    """Deploy to Heroku"""
    print("\n☁️ Heroku Deployment")
    print("-" * 30)
    
    # Check if Heroku CLI is installed
    try:
        subprocess.run("heroku --version", shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ Heroku CLI not found. Please install it first.")
        return False
    
    commands = [
        ("git add .", "Staging files"),
        ("git commit -m 'Deploy attendance system'", "Committing changes"),
        ("git push heroku main", "Pushing to Heroku"),
        ("heroku run python manage.py migrate", "Running migrations on Heroku"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    print("\n✅ Heroku deployment completed!")
    print("Your app should be available at: https://your-app-name.herokuapp.com")
    return True

def main():
    """Main deployment function"""
    if not setup_environment():
        return
    
    print("Choose deployment option:")
    print("1. Local deployment")
    print("2. Heroku deployment")
    print("3. Both")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        deploy_local()
    elif choice == "2":
        deploy_heroku()
    elif choice == "3":
        deploy_local()
        deploy_heroku()
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
