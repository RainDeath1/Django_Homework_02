document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById('loginForm');
    const tasksSection = document.getElementById('tasksSection'); 
    const loginSection = document.getElementById('loginSection'); 

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        fetch('http://127.0.0.1:8000/api/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => response.json())
        .then(data => {
            localStorage.setItem('access', data.access);
            loginSection.style.display = 'none';
            tasksSection.style.display = 'block';
            loadTasks();
        })
        .catch(error => {
            console.error('Ошибка при аутентификации:', error);
        });
    });


    loadTasks();

    document.getElementById('taskForm').addEventListener('submit', function(e) {
        e.preventDefault();
        saveTask();
    });
});

function loadTasks() {
    let access = localStorage.getItem('access');
    fetch('http://127.0.0.1:8000/api/tasks/', {
        headers: {
            'Authorization': 'Bearer ' + access 
        }
    })
    .then(response => response.json())
    .then(data => {
       
    });
}


function loadTasks() {
    fetch('http://127.0.0.1:8000/tasks/api/')
        .then(response => response.json())
        .then(data => {
            let tasksList = document.getElementById('tasksList');
            tasksList.innerHTML = '';

            data.forEach(task => {
                let li = document.createElement('li');
                li.textContent = task.title;
                li.setAttribute('data-id', task.id);
                
                let deleteBtn = document.createElement('button');
                deleteBtn.textContent = 'Delete';
                deleteBtn.addEventListener('click', function() {
                    deleteTask(task.id);
                });
                li.appendChild(deleteBtn);
                
                let editBtn = document.createElement('button');
                editBtn.textContent = 'Edit';
                editBtn.addEventListener('click', function() {
                    editTask(task.id);
                });
                li.appendChild(editBtn);

                tasksList.appendChild(li);
            });
        });
}



function editTask(id) {
    fetch('/api/tasks/' + id + '/')
    .then(response => response.json())
    .then(data => {
        document.getElementById('taskId').value = data.id;
        document.getElementById('taskTitle').value = data.title;
    });
}



function saveTask() {
    let taskId = document.getElementById('taskId').value;
    let taskTitle = document.getElementById('taskTitle').value;

    let url, method;

    if (taskId) {
        url = 'http://127.0.0.1:8000/tasks/api/' + taskId + '/';
        method = 'PUT';
    } else {
        url = 'http://127.0.0.1:8000/tasks/api/';
        method = 'POST';
    }

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: taskTitle }),
    })
    .then(response => {
        loadTasks();
        document.getElementById('taskForm').reset();
        document.getElementById('taskId').value = '';
    });
}