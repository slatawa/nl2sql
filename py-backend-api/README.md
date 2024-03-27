# Development
## Running Development Server Locally

1. Navigate to the `py-backend-api` directory:
   ```bash
   cd py-backend-api
   ```

2. Create environment: 
  - Use Python 3.10 (recommended using `pyenv` to install and manage Python versions)
  - `python3 -m venv venv`
  - `source venv/bin/activate`
  
3. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Backend server locally:
   ```bash
   flask run
   ```
   OR
   ```bash
   python app.py
   ````

   By default, the app will be running on [http://localhost:5000/](http://localhost:5000/).


