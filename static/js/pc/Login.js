function get_cookie_by_name(name) {
    var start = document.cookie.indexOf(name);
    if (start != -1) {
        var res = "";
        var end = document.cookie.indexOf(";", start+1);
        if (end == -1) {
            res = document.cookie.substring(start+name.length+1);
        } else {
            res = document.cookie.substring(start+name.length+1, end);
        }
        return res;
    }
    return "";
}

function login() {
    var username = $('input[name="username"]').val();
    var password = $('input[name="password"]').val();
    if (username == "" || password == "") {
        $('.Login-word').html('请输出手机号码或密码');
        return -1;
    }
    var xsrf = get_cookie_by_name('_xsrf');
    $.ajax({
        'url': '/admin',
        'type': 'POST',
        'data': {'username': username, 'password': password, '_xsrf':xsrf},
        success: function(e) {
            if (e == '0') {
                window.location.href = '/';
            } else if (e == '1') {
                alert('手机号或密码不对');
            }
        },
        error: function(e) {
            alert(e);
        }
    });
}
$(function () {
    $('.Login-btn').click('on', login);
})
function clearword(){
    $('.Login-word').html('');
}
