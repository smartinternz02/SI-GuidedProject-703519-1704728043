// main.js
document.addEventListener('DOMContentLoaded', function () {
    // Add event listener to the file input element
    var fileInput = document.querySelector('input[type="file"]');
    fileInput.addEventListener('change', handleFileSelect);

    // Set up SocketIO connection
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Receive video frames from the server
    socket.on('video_frame', function (frame) {
        var img = document.getElementById('video');
        img.src = 'data:image/jpeg;base64,' + frame;
    });

    // Request the video feed when the page is loaded
    socket.emit('video_feed');
});

function handleFileSelect(event) {
    // Get the selected file
    var file = event.target.files[0];

    // Display the selected image preview (optional)
    var preview = document.getElementById('image-preview');
    preview.src = URL.createObjectURL(file);
    preview.style.display = 'block';
}

var socket = io.connect('http://' + document.domain + ':' + location.port);


document.getElementById('start-recognition').addEventListener('click', function () {
    // Turn on the webcam when the button is clicked
    startWebcam();
});

function startWebcam() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            var video = document.getElementById('video');
            video.srcObject = stream;
            
            var canvas = document.getElementById('canvas');
            var context = canvas.getContext('2d');
            
            video.addEventListener('loadeddata', function () {
                video.style.display = 'block';
                canvas.style.display = 'block';

                setInterval(function () {
                    context.drawImage(video, 0, 0, 640, 480);
                    sendFrame();
                }, 1000 / 10);
            });
        })
        .catch(function (error) {
            console.log("Error accessing webcam: ", error);
            resultText.innerText = "Error accessing webcam.";
        });
}

function sendFrame() {
    var resultText = document.getElementById('result');
    var frameData = canvas.toDataURL('image/jpeg');
    socket.emit('video_frame', frameData);
}

socket.on('classification_result', function (data) {
    document.getElementById('classification').innerText = data.alpha + ' (Confidence: ' + data.confidence.toFixed(2) + '%)';
});