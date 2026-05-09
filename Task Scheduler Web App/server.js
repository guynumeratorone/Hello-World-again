// Task Scheduler Web App
// Uses Node.js to serve dynamic HTML pages and store task data locally.
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URLSearchParams } = require('url');

const PORT = 3000;
const DATA_FILE = path.join(__dirname, 'tasks.json');
const VIEWS_DIR = path.join(__dirname, 'views');
const PUBLIC_DIR = path.join(__dirname, 'public');

// Ensure the JSON data file exists before the server starts handling requests.
function initializeDataFile() {
    if (!fs.existsSync(DATA_FILE)) {
        fs.writeFileSync(DATA_FILE, JSON.stringify([], null, 2));
    }
}

// Read all saved tasks from the local JSON file.
function loadTasks() {
    initializeDataFile();

    try {
        const data = fs.readFileSync(DATA_FILE, 'utf8');
        return JSON.parse(data || '[]');
    } catch (error) {
        console.error('Could not load tasks:', error.message);
        return [];
    }
}

// Save the current task list back to the local JSON file.
function saveTasks(tasks) {
    fs.writeFileSync(DATA_FILE, JSON.stringify(tasks, null, 2));
}

// Generate a simple unique identifier for each task.
function createTaskId() {
    return `${Date.now()}-${Math.floor(Math.random() * 100000)}`;
}

// Escape user input before placing it into HTML.
function escapeHtml(value) {
    return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}

// Load a reusable HTML file from the views folder.
function loadTemplate(fileName) {
    return fs.readFileSync(path.join(VIEWS_DIR, fileName), 'utf8');
}

// Replace placeholder values inside the selected HTML template.
function renderTemplate(fileName, replacements = {}) {
    let template = loadTemplate(fileName);

    for (const [key, value] of Object.entries(replacements)) {
        template = template.replaceAll(`{{${key}}}`, value);
    }

    return template;
}

// Send an HTML response to the browser.
function sendHtml(response, html, statusCode = 200) {
    response.writeHead(statusCode, { 'Content-Type': 'text/html; charset=utf-8' });
    response.end(html);
}

// Redirect the browser to another route after a form action.
function redirect(response, location) {
    response.writeHead(303, { Location: location });
    response.end();
}

// Collect POST body data submitted by an HTML form.
function collectRequestBody(request) {
    return new Promise((resolve, reject) => {
        let body = '';

        request.on('data', chunk => {
            body += chunk.toString();

            if (body.length > 10000) {
                reject(new Error('Request body is too large.'));
                request.destroy();
            }
        });

        request.on('end', () => {
            resolve(new URLSearchParams(body));
        });

        request.on('error', reject);
    });
}

// Build task cards for the task list page.
function buildTaskCards(tasks) {
    if (tasks.length === 0) {
        return '<p class="empty-message">No tasks have been created yet.</p>';
    }

    return tasks.map(task => {
        const statusClass = task.completed ? 'complete' : 'incomplete';
        const statusText = task.completed ? 'Complete' : 'Incomplete';
        const runText = task.lastRun ? `Last simulated run: ${escapeHtml(task.lastRun)}` : 'Not simulated yet';

        return `
            <article class="task-card ${statusClass}">
                <div class="task-card-header">
                    <h3>${escapeHtml(task.name)}</h3>
                    <span class="status-badge">${statusText}</span>
                </div>
                <p><strong>Type:</strong> ${escapeHtml(task.type)}</p>
                <p><strong>Schedule:</strong> ${escapeHtml(task.schedule)}</p>
                <p><strong>Description:</strong> ${escapeHtml(task.description)}</p>
                <p class="run-note">${runText}</p>
                <div class="task-actions">
                    <form method="POST" action="/toggle-task">
                        <input type="hidden" name="id" value="${escapeHtml(task.id)}">
                        <button type="submit">Toggle Complete</button>
                    </form>
                    <form method="POST" action="/run-task">
                        <input type="hidden" name="id" value="${escapeHtml(task.id)}">
                        <button type="submit">Simulate Run</button>
                    </form>
                    <form method="POST" action="/delete-task">
                        <input type="hidden" name="id" value="${escapeHtml(task.id)}">
                        <button class="danger" type="submit">Delete</button>
                    </form>
                </div>
            </article>
        `;
    }).join('');
}

// Build a short dashboard preview of the newest tasks.
function buildRecentTaskList(tasks) {
    if (tasks.length === 0) {
        return '<li>No tasks have been created yet.</li>';
    }

    return tasks.slice(-3).reverse().map(task => {
        const status = task.completed ? 'complete' : 'incomplete';
        return `<li>${escapeHtml(task.name)} <span>(${status})</span></li>`;
    }).join('');
}

// Render the dashboard page using values calculated from saved tasks.
function handleDashboard(request, response) {
    const tasks = loadTasks();
    const completedCount = tasks.filter(task => task.completed).length;
    const incompleteCount = tasks.length - completedCount;

    const html = renderTemplate('dashboard.html', {
        totalTasks: String(tasks.length),
        completedTasks: String(completedCount),
        incompleteTasks: String(incompleteCount),
        recentTasks: buildRecentTaskList(tasks)
    });

    sendHtml(response, html);
}

// Render the form page used to create a new task.
function handleCreatePage(request, response) {
    const html = renderTemplate('create.html');
    sendHtml(response, html);
}

// Render the full task list page.
function handleTaskList(request, response) {
    const tasks = loadTasks();
    const html = renderTemplate('tasks.html', {
        taskCards: buildTaskCards(tasks)
    });

    sendHtml(response, html);
}

// Create and save a new task based on submitted form data.
async function handleCreateTask(request, response) {
    const form = await collectRequestBody(request);
    const tasks = loadTasks();

    const newTask = {
        id: createTaskId(),
        name: (form.get('name') || 'Untitled Task').trim(),
        type: (form.get('type') || 'General').trim(),
        schedule: (form.get('schedule') || 'Not scheduled').trim(),
        description: (form.get('description') || 'No description provided.').trim(),
        completed: false,
        lastRun: ''
    };

    tasks.push(newTask);
    saveTasks(tasks);
    redirect(response, '/tasks');
}

// Mark a task complete or incomplete.
async function handleToggleTask(request, response) {
    const form = await collectRequestBody(request);
    const id = form.get('id');
    const tasks = loadTasks();

    const updatedTasks = tasks.map(task => {
        if (task.id === id) {
            return { ...task, completed: !task.completed };
        }

        return task;
    });

    saveTasks(updatedTasks);
    redirect(response, '/tasks');
}

// Add a timestamp to show that the task was simulated.
async function handleRunTask(request, response) {
    const form = await collectRequestBody(request);
    const id = form.get('id');
    const tasks = loadTasks();
    const timestamp = new Date().toLocaleString();

    const updatedTasks = tasks.map(task => {
        if (task.id === id) {
            return { ...task, lastRun: timestamp };
        }

        return task;
    });

    saveTasks(updatedTasks);
    redirect(response, '/tasks');
}

// Remove a task from the JSON file.
async function handleDeleteTask(request, response) {
    const form = await collectRequestBody(request);
    const id = form.get('id');
    const tasks = loadTasks();
    const remainingTasks = tasks.filter(task => task.id !== id);

    saveTasks(remainingTasks);
    redirect(response, '/tasks');
}

// Serve the CSS file from the public folder.
function handleStaticFile(request, response) {
    const filePath = path.join(PUBLIC_DIR, 'styles.css');
    const css = fs.readFileSync(filePath, 'utf8');

    response.writeHead(200, { 'Content-Type': 'text/css; charset=utf-8' });
    response.end(css);
}

// Display a simple 404 page for unknown routes.
function handleNotFound(request, response) {
    sendHtml(response, `
        <h1>404 - Page Not Found</h1>
        <p>The requested page does not exist.</p>
        <p><a href="/">Return to Dashboard</a></p>
    `, 404);
}

// Route incoming browser requests to the correct handler.
async function handleRequest(request, response) {
    const url = new URL(request.url, `http://${request.headers.host}`);
    const route = url.pathname;

    try {
        if (request.method === 'GET' && route === '/') return handleDashboard(request, response);
        if (request.method === 'GET' && route === '/create') return handleCreatePage(request, response);
        if (request.method === 'GET' && route === '/tasks') return handleTaskList(request, response);
        if (request.method === 'GET' && route === '/styles.css') return handleStaticFile(request, response);

        if (request.method === 'POST' && route === '/create-task') return await handleCreateTask(request, response);
        if (request.method === 'POST' && route === '/toggle-task') return await handleToggleTask(request, response);
        if (request.method === 'POST' && route === '/run-task') return await handleRunTask(request, response);
        if (request.method === 'POST' && route === '/delete-task') return await handleDeleteTask(request, response);

        handleNotFound(request, response);
    } catch (error) {
        console.error('Server error:', error.message);
        sendHtml(response, '<h1>500 - Server Error</h1><p>Something went wrong.</p>', 500);
    }
}

initializeDataFile();

const server = http.createServer(handleRequest);

server.listen(PORT, () => {
    console.log(`Task Scheduler Web App running at http://localhost:${PORT}`);
});
