# Blog_proj

## Based on [Flask-Blog-Tutorial by Tech with Tim](https://github.com/techwithtim/Flask-Blog-Tutorial)

- Performed feature:
  - Login  
  - Logout
  - Sign Up
  - Post CRUD
  - Comment CRUD
  - Like

## New feature & New Page

- New feature
  - Upload image(Profile-personal photo, Post-image)
  - Edit personal info(username, password)
  - Add [Summernote Text Editor](https://summernote.org/)
- New Page
  - Profile page

## Resources Used

**Python Version :** 3.9.4  
**IDE :** VSCode  
**Requirements :**

- Install [requirements](https://github.com/JohnnyHsieh1020/Blog_proj/blob/main/requirements.txt)

```terminal
pip install -r requirements.txt
```

## DataBase

Connect to PostgreSQL:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user_name:password@IP:PORT/db_name'
```

1. Create User table, with 6 columns.
   - id (P-key)
   - username
   - email
   - password
   - image_name
   - date_created
   - **posts**
   - **comments**
   - **likes**
2. Create Post table, with 5 columns.
   - id (P-key)
   - content
   - image_name
   - date_created
   - author_id (F-key, ref to User-id)
   - **comments**
   - **likes**
3. Create Comment table, with 5 columns.
   - id (P-key)
   - content
   - date_created
   - author_id (F-key, ref to User-id)
   - post_id (F-key, ref to Post-id)
4. Create Like table, with 3 columns.
   - id (P-key)
   - author_id (F-key, ref to User-id)
   - post_id (F-key, ref to Post-id)

## Deploy to Heroku

- Create app on [Heroku](https://www.heroku.com/).
- Needs
  - Procfile

    ```txt
    web: gunicorn blog.__init__:'create_app()'
    ```

  - requirements
  - runtime

    ```txt
    python-3.9.4
    ```

- Command
  
  ```terminal
  heroku login
  heroku git:remote -a {app_name}
  git add .
  git commit -m “...”
  git push heroku master/main(choose one)

  heroku config:add TZ="Asia/Taipei" // Set timezone
  ```
