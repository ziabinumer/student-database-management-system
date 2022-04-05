# STUDENT DATABASE MANAGEMENT SYSTEM
#### Video Demo:  <URL https://www.youtube.com/watch?v=A6CLFTNRg1o>

#### Description:
For my final project, I worked to build a student database management system using Flask, SQL and JavaScript. Other languages used are HTML, CSS and Jinja Templating. Initially, I wanted to do the project using Django but after spending some time learning it, i dropped that idea because that was too much for now. I would like to admit that w3schools, geeksforgeeks and some other websites had been very useful and reused some of their codes in front end. I used Bootstrap as CSS framework. Backend purely is written by myself. My brother has an online academy and I saw him struggling with storing data of students and teachers which motivated me to build a simple student database management application. I had a few ideas in mind such as implementing fees, salaries and attendance but I dropped them later on when I felt I am not that good with database. After Completing this course, I will learn databases and then come again and implement those feature and make myself proud.
* Languages used are:
    * Flask: Template Rendering, redirects, form validation and storing data in database
    * SQL: Inserting, retrieving and updating data from database
    * JavaScript: Events, Search and Edit
    * HTML&CSS: For front end design
* Pages:
    * Homepage: Provides overview of school. Number of students, teachers, total fees and salaries
    * Students: Provides student details i.e Name, Gender .... It also has option to edit or delete a student
    * Teachers: Provides teacher details and ability to edit a teacher
    * Add: You can use this page to add a student or a teacher.
    * Import: import a database which was created using this application. Required tables: Student, Teacher. Required   columns can be viewed from student page.
    * Export databaase: All student and teacher records can be exported using this page

* Files:
    * requirements.txt: contains names of required libraries
    * app.py: Contains main python code which works as backend of application. Handles all operations. Has a few imports declared in requirements.txt. Requires login.py to work
    * login.py: Definiton of login - a decorated function to check whether user is logged in or not. Redirects to /login in case user is not logged in
    * database.db: It is created by app.py and is used to store user information and the data of students and teachers

    * static/script.js: A javascript file. It performs operations such as setting up counter on homepage and has definition of function edit which is used to provide data to form on student and teacher page
    * static/search.js: Implements search functionality using Javascript and jquery
    * static/styles.css: used to style the application

    * templates: It has multiple files such as layout.html, index.html and student.html which are used to provide a front end to user on application. Most of them are dynamically created using app.py

### Thank you David Malan and CS50 Team

### #### This was CS50

