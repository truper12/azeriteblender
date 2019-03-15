$(document).ready(function() {
    // nav bar - login/out
    var tk = sessionStorage.getItem("azblr-tk")
    var _headers = {}
    _headers['Authorization'] = tk
    if (tk == null) {
        $('#login-button').removeClass('d-none')
    } else {
        $('#logout-button').removeClass('d-none')
        $('#logout-button').click(function() {
            $.ajax({
                url: 'http://localhost:5000/api/auth/logout',
                type: 'post',
                headers: _headers,
                success: function(data) {
                    sessionStorage.removeItem("azblr-tk")
                    location.reload()
            }
            })
        })
    }
    $(document).ready(function(){
        $("#man-modal").load("/man-modal.html")       
    });
})