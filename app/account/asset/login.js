function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var createAccountRequest = new XMLHttpRequest();

    createAccountRequest.open("POST", "/api/v1/accounts/login", true);
    createAccountRequest.setRequestHeader("Content-Type", "application/json");
    createAccountRequest.send(JSON.stringify({username: username, password: password}));
}
