fetch("http://127.0.0.1:8000/api/users/")
  .then(response => response.json())
  .then(data => {
    let usersDiv = document.getElementById('users');
    data.forEach(user => {
        let userElement = document.createElement('div');
        userElement.textContent = user.username; 
        usersDiv.appendChild(userElement);
    });
  })
 
