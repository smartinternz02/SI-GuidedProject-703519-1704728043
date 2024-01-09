$(document).ready(function () {
    console.log("Document ready!");

    // Image preview and upload
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            };
            reader.readAsDataURL(input.files[0]);
        }
    }

    // Trigger file input on button click
    $("#btn-upload").click(function () {
        console.log("Upload button clicked!");
        $("#imageUpload").click();
    });

    // Handle file input change
    $("#imageUpload").change(function () {
        console.log("File input changed!");
        $('.image-section').show();
        $('#btn-predict').show();
        $('.result-section').hide();
        readURL(this);
    });

    // Predict button click
    $("#btn-predict").click(function () {
        console.log("Predict button clicked!");
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                console.log('Success!');
                console.log(data);
                $('.result-section').show();
                $('#result').html(data);
            },
        });
    });
});
