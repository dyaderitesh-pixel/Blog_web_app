# BWA Blog

Simple blog application built with Django, MySQL, and HTML/CSS.

## Features

- User registration, login, logout, password change
- User profiles (name, bio, profile picture URL)
- Posts with CRUD, slugs, and permissions (author or admin only)
- Comments and likes per post (one like per user per post)
- Pagination on index
- Django admin for users, posts, comments, likes
- Sample data management command
- Basic unit tests for models and permissions

## Setup

1. Create and activate virtual environment (already created here as `venv` in this project in the example):

   ```bash
   python -m venv venv
   venv\\Scripts\\activate  # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure MySQL database and user. Example configuration:

   ```sql
   CREATE DATABASE bwa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'root'@'localhost' IDENTIFIED BY 'your-password-here';
   GRANT ALL PRIVILEGES ON bwa.* TO 'root'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. Update `bwa/bwa/settings.py` or use environment variables as in `.env.example` for database credentials.

5. Run migrations:

   ```bash
   cd bwa
   ..\\venv\\Scripts\\python.exe manage.py migrate
   ```

6. Create superuser (example from spec):

   ```bash
   ..\\venv\\Scripts\\python.exe manage.py createsuperuser --username Shubham_18 --email chavanshubham2905@gmail.com
   ```

7. (Optional) Create demo data:

   ```bash
   ..\\venv\\Scripts\\python.exe manage.py seed_demo
   ```

8. Run the development server:

   ```bash
   ..\\venv\\Scripts\\python.exe manage.py runserver
   ```

Then open http://127.0.0.1:8000/ in your browser.

## Running tests

From the `bwa` directory:

```bash
..\\venv\\Scripts\\python.exe manage.py test
```

## How likes and comments work

- On each post detail page, authenticated users see a like/unlike button. A `Like` record links the user and the post, enforced unique per (post, user).
- The like count is computed via the `Post.like_count` property (reverse relation to `Like`).
- Comments are created by posting the comment form on the detail page. Each comment stores `post`, `author`, `body`, and `created_at`, and they are listed in chronological order under the post.

## Extensibility notes

- To add image upload for posts, extend the `Post` model with an `ImageField` and configure media files.
- To add categories/tags, create additional models and relations from `Post`.
- To add search/filtering, create list views with query parameters filtering the `Post` queryset.
