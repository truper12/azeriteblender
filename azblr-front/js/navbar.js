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
                url: API_HOST+'/api/auth/logout',
                type: 'post',
                headers: _headers
            })
            sessionStorage.clear()
            location.reload()
        })
    }
    $(document).ready(function(){
        $("#man-modal").load("./man-modal.html")       
    });
})