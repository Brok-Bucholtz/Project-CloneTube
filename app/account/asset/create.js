function create_account() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var createAccountRequest = new XMLHttpRequest();
    
    createAccountRequest.open("POST", "/api/v1/accounts", true);
    createAccountRequest.setRequestHeader("Content-Type", "application/json");
    createAccountRequest.send(JSON.stringify({username: username, password: password}));
}
