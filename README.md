
# DjangoBlog

A simple Blog with django and python.

## How to run

To run Blog in development mode; Just use steps below:

1. Install `python3`, `pip` in your system.
2. Clone the project `https://github.com/farhadmpr/djangoblog`.
3. Make development environment ready using commands below;

  ```bash
  git clone https://github.com/farhadmpr/djangoblog && cd djangoblog
  python -m venv venv  # Create virtualenv named venv
  source venv/bin/activate
  pip install -r requirements.txt
  python manage.py migrate  # Create database tables
  ```

4. Run `DjangoBlog` using `python manage.py runserver`
5. Go to [http://localhost:8000](http://localhost:8000) to see blog.
