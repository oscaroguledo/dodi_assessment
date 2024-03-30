** ✨ Cinema Program Assessment! ✨ **

**⭐️ Key Technologies:**

- **Django Ninja:** 
- **Python 12:** 
- **Redis:** 
- **Celery:** 
- **Poetry:** 
- **PostGres:** 

** ✨ Project Goal:✨ **

- Build an API endpoint to seamlessly add new movies to the cinema program

**✨ Set Up: Manually✨ **

1. **Install Python 12**
2. **Install pip**
3. **Install and Start Redis:**
   - Windows 
      - Enable WSL2: Search for "Turn Windows features on or off" and enable "Virtual Machine Platform" and "Optional feature directory - Subsystem for Linux". Reboot if prompted.
      - Install WSL2 Kernel: Open a PowerShell window as administrator and run **wsl --install -d Ubuntu **(replace Ubuntu with your preferred Linux distribution)
      - Open Ubuntu: Search for "Ubuntu" in the Start menu.
      - Update Package Manager: Run **sudo apt update**
      - Install Redis: Run **sudo apt install redis-server**
      - Start Redis: Run sudo redis-server (consider using a service manager for automatic startup)
   - Mac 
   ```shell
      brew install redis
   ```
   - Linux
   ```bash
      # Debian/Ubuntu: 
      sudo apt update && sudo apt install redis-server
      # CentOS/RHEL: 
      sudo yum update && sudo yum install redis
      # Fedora: 
      sudo dnf update && sudo dnf install redis
   ```
   
4. **Clone the Repository:**
   - `git clone https://github.com/oscaroguledo/dodi_assessment.git`
5. **Install Dependencies:**
   - `pip install -r requirements.txt`

6. **Start the Django Development Server:**
   - Your `.env` file should be in same directory as your `manage.py` file
   - Terminal 1: `python manage.py runserver`
7. **Unleash Celery:**
   - Terminal 2: `celery -A cinema.celery beat --loglevel=info`
   - Terminal 3: `celery -A cinema.celery worker --pool=solo --loglevel=info`
8. **Run Tests :**
   - Terminal 1: `pytest`


**✨ Set Up: Docker✨ **
1. **Clone the Repository:**
   - `git clone https://github.com/oscaroguledo/dodi_assessment.git`
2. **Install Dependencies:**
   - `pip install -r requirements.txt`
3. **run the command in terminal**
      ``` 
      # docker-compose up
      ```
4. **Run Tests :**
   - Terminal 1: `pytest`


**✨ Test apis: ✨ **
   **While the server is running:** 
   - On your Brower: [127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs)


**⭐️ Questions and Answers:**
1. **How would you design and implement content-based and collaborative filtering recommendation algorithms?   What databases would you use for efficient storage and querying of user preferences and movie metadata?**
    - Ans:
    1. I would analyze the feautures of the content(in this case, movies) eg, their ratings and protagonist
    2. Secondly, I would build a user profile based on their preferences and the movies they have seen.
    3. Lastly, i would recommend movies based on the user profile preferences.
    4. As for the database, I would use a combination of SQL and NoSQL databases as No SQL can handle divers data due to its flexible schema and flexibility. While SQL can handle structured data, such as tables and relations.eg Ids, ratings, preference etc

2. **How would you optimize database performance for a social networking platform using Postgres, Neo4j, and Qdrant for structured, graph-based, and similarity search data?**
    - Ans:
    1. I would use PostgreSQL for storing structured user data, posts, comments, etc.
    2. I would then leverage Neo4j for modeling social connections, groups, and complex relationships between users, posts, and comments.
    3. Finally, I would use Qdrant for efficient similarity search based on user interests or content analysis.

3. **Describe using Celery for asynchronous task processing in a Django application, ensuring reliability and fault tolerance, especially for tasks that may fail or need to be retried**
    - Ans:
      Using Celery for asynchronous task processing in a Django application is an effective approach to remove time-consuming or resource-intensive processes from the main application flow. Celery lets you run your Django application asynchronously, which keeps it scalable and responsive. You can use a number of ways to guarantee fault tolerance and reliability, particularly for tasks that might fail or require retries. Some of the common ways include:
      1. **Use a task queue to retry failed tasks.**
         Celery assigns jobs to several workers via a distributed task queue. Celery manages the task queue by default using a message broker that is either Redis or RabbitMQ.By ensuring that jobs are completed asynchronously, task queues allow your Django application to focus on processing other requests.
      2. **Retries**
         Celery offers built-in assistance for retrying jobs that are unsuccessful because of failures or exceptions. For every assignment, you may set the maximum number of tries and the interval between tries.To set up retry behavior, use the max_retries and retry_delay options in the Celery job specification.
      3. **Error Handling**
         In order to gracefully handle failures, incorporate strong error handling into your Celery activities. You may identify specific exceptions in your tasks and determine whether to log the problem, try the operation again, or might adopt different course of action.To automatically retry jobs when specified exceptions occur, use Celery's retry decorator.
      4. **Task Time Outs**
         Give lengthy jobs timeouts to avoid them consuming all of the workers' resources. To guarantee that every task is finished in a fair amount of time, set a maximum execution time for each one.To gracefully handle task timeouts, use Celery's SoftTimeLimitExceeded and TimeLimitExceeded exceptions.