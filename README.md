 **Here's a polished version with improved formatting and visual appeal:**

** Welcome to the Dodi Assessment! **

** Get ready to bring the cinema to life with this exciting Django API project!**

**⭐️ Key Technologies:**

- **Django Ninja:** Blazing-fast API development for Pythonistas
- **Python 12:** Embrace the latest Python features for efficient coding
- **Redis:** Lightning-fast in-memory data store for caching and task queues
- **Celery:** A powerhouse for handling asynchronous tasks
- **Poetry:** Dependency management made simple and elegant

** Project Goal:**

- Build an API endpoint to seamlessly add new movies to the cinema program

** Up and Running:**

1. **Install Python 12**
2. **Install pip**
3. **Install and Start Redis:**
   - Follow platform-specific instructions ([link for Windows, macOS, or Linux instructions])
   - Test with `redis-cli ping`
4. **Create a Virtual Environment:**
   - Activate it for a clean setup
5. **Clone the Repository:**
   - Grab the project code from its rightful home
6. **Install Dependencies:**
   - `pip install -r requirements.txt`

** Let's Have a Show!:**

1. **Start the Django Development Server:**
   - Terminal 1: `python manage.py runserver`
2. **Unleash Celery:**
   - Terminal 2: `celery -A cinema.celery beat --loglevel=info`
   - Terminal 3: `celery -A cinema.celery worker --pool=solo --loglevel=info`
3. **Run Tests (Ensure Cinematic Quality):**
   - Terminal 1: `pytest`

** Test apis:**
   **While the server is running:** 
   - On your Brower: [127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs)
**✨ Now, let's make movie magic! ✨**

**⭐️ Questions and Answers:**
1. **How would you design and implement content-based and collaborative filtering recommendation algorithms?   What databases would you use for efficient storage and querying of user preferences and movie metadata?**
    - Ans:
2. **How would you design and implement content-based and collaborative filtering recommendation algorithms?   What databases would you use for efficient storage and querying of user preferences and movie metadata?**
    - Ans:
3. **How would you design and implement content-based and collaborative filtering recommendation algorithms?   What databases would you use for efficient storage and querying of user preferences and movie metadata?**
    - Ans: