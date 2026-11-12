# Network – Social Networking Web Application

A social networking application inspired by platforms such as Twitter and Threads, built using Django, JavaScript, HTML, and CSS.

Users can create posts, interact with other users, follow profiles, and manage their own content through a dynamic web interface.

## Features

### 1. Authentication
- User registration and login.
- Logout functionality.
- Authenticated users can access interactive features.
- Visitors who aren't logged in can browse posts but cannot create or interact with them.

### 2. Posts
- Create new posts.
- Display posts in reverse chronological order.
- View posts from all users.
- Edit your own posts without refreshing the page.

### 3. Likes
- Like and unlike posts asynchronously.
- Like counts update dynamically.
- Users can like their own posts.
- Database constraints prevent duplicate likes.

### 4. Profiles
- Individual profile pages for each user.
- Display all posts created by a particular user.
- View follower and following counts.
- Follow and unfollow other users.

### 5. Following Feed
- Dedicated page displaying posts from users you follow.
- Posts are displayed in reverse chronological order.

### 6. Pagination
- Posts are divided into pages.
- Each page displays a maximum of 10 posts.
- Bootstrap pagination navigation with Previous, Next, and page numbers.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| SQLite | Database |
| JavaScript | Dynamic frontend interactions |
| HTML5 | Page structure |
| CSS3 | Styling |
| Bootstrap | UI components and styling |
| Fetch API | Asynchronous HTTP requests |
| JSON | Communication between frontend and backend |

## Key Concepts Practiced

- Django Models and ORM
- Foreign Key relationships
- Database constraints
- Django views and URL routing
- User authentication and authorization
- QuerySets and database filtering
- JavaScript DOM manipulation
- Event listeners and event handling
- Fetch API and asynchronous JavaScript
- JSON responses
- CSRF protection
- Django pagination
- Dynamic frontend updates without full page reloads

## Running Locally

1. Clone the repository:

   ```bash
   git clone YOUR_REPOSITORY_URL
   ```

2. Navigate to the project directory:

   ```bash
   cd network
   ```

3. Install Django:

   ```bash
   pip install django
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Open the local development URL:

   ```text
   http://127.0.0.1:8000/
   ```

## Project Context

This project was developed as part of **CS50's Web Programming with Python and JavaScript** by Harvard University.

The primary goal was to apply backend and frontend concepts to build a functional social networking application, with particular emphasis on Django, database relationships, and asynchronous JavaScript interactions.

