## Quick Start

Follow these steps to set up and run the project:

### 1. Clone the Repository
```bash
# Clone the repository
git clone https://github.com/Jerald011003/AI-Learn-Story.git

# Navigate into the project directory
cd AI-Learn-Story

# Move into the server directory
cd server

# Install Python dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Start the Django server
python manage.py runserver

# Navigate to the frontend directory
cd ../webv2

# Install Node.js dependencies
npm install

# Run the development server
npm run dev
