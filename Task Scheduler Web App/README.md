# Overview
I created a task scheduler web app that lets a user create, view, update, and delete simple scheduled tasks. The app uses a Node.js server to serve HTML pages and store task information in a local JSON file. The dashboard shows task totals, the create page provides a form for adding new tasks, and the task list page displays saved tasks with options to mark them complete, simulate a run, or delete them.

To launch the local server I have to:
Go to the location of the local project in the console: cd "C:\Users\<usernamehere>\Desktop\VScode\Applied Programming 310\Task Scheduler Web App"
Then launch the node server with teh following command also entered in to the console: node server.js
If successful, you should get the following prompt in console: Task Scheduler Web App running at http://localhost:3000
You should be able to hold shift and left click on the Hyperlink for: http://localhost:3000
If not, then just copy the link, and open a new tab in a web browser, then paste the link manually and hit enter. You should then land on the project that should be running locally.

My purpose for writing the software was to expose myself to other programming languages and to build something that I can apply to another personal projects future feature.

[Software Demo Video](https://youtu.be/ZjWo_zM7V9E)

# Web Pages

The app contains three main pages: Dashboard, Create Task, and Task List.

The Dashboard page is the first page shown when opening the app. It displays a summary of the saved task data, including the total number of tasks, the number of completed tasks, and the number of incomplete tasks. It also shows a short list of the most recent tasks. These values are dynamically created from the local tasks.json file.

The Create Task page contains a form where the user can enter a task name, task type, schedule, and description. When the form is submitted, the server receives the data, creates a new task object, saves it to the JSON file, and redirects the user to the Task List page.

The Task List page displays all saved tasks. Each task card is dynamically generated from the JSON data file. The user can mark a task complete or incomplete, simulate running the task, or delete the task. After each action, the server updates the saved data and reloads the task list.

The navigation menu at the top of each page allows the user to move between the Dashboard, Create Task, and Task List pages.

# Development Environment

I developed this project using Visual Studio Code as the code editor. I used a local terminal to run the Node.js server and tested the web app in a browser through localhost.

The project was written with JavaScript, HTML, CSS, and JSON. JavaScript was used for the server logic, routing, form handling, dynamic page rendering, and reading and writing task data. HTML was used for the page templates, CSS was used for styling, and JSON was used for local task storage.

The app uses Node.js with built-in modules, including http, fs, path, and url. No external web framework was used.

# Useful Websites

* [Node.js v26.1.0 documentation](https://nodejs.org/docs/latest/api/)
* [Mozilla Developer Network](https://developer.mozilla.org/en-US/docs/Learn/Forms)
* [W3Schools Node.js Tutorial](https://www.w3schools.com/nodejs/)

# Future Work

* Add edit functionality so users can update an existing task without deleting and recreating it.
* Add stronger form validation to prevent empty or poorly formatted task data from being saved.
* Improve the scheduling system so tasks can use real dates, times, and recurring schedule options.