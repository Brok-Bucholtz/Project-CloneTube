function upload_video() {
    var formData = new FormData();
    var createAccountRequest = new XMLHttpRequest();

    formData.append('title', document.getElementById('title').value);
    formData.append('file', document.getElementById('file').files[0]);

    createAccountRequest.open("POST", "/api/v1/videos", true);
    createAccountRequest.send(formData);
}
