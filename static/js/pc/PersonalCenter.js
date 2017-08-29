
function get_cookie_by_name(name)
{
    var start = document.cookie.indexOf(name);
    if (start != -1) {
        var res = '';
        var end  = document.cookie.indexOf(';', start+1);
        if (end == -1) {
            res = document.cookie.substring(start+name.length+1);
        } else {
            res = document.cookie.substring(start+name.length+1, end);
        }
        return res;
    }
    return '';
}
$(function () {
    var xsrf = get_cookie_by_name("_xsrf");
    $('input[name="_xsrf"]').val(xsrf);
    $('.SurePassword').click('on',function () {
            var first    = $('input[name="init_password"]').val();
            var second   = $('input[name="new_password"]').val();
            var third    = $('input[name="confirm_password"]').val();
            if (second != third) {
                alert("新密码两次输入不一致!");
                return -1;
            }
            var xsrf = get_cookie_by_name('_xsrf');
            $.ajax({
                url: '/personal',
                type: 'POST',
                data: {'action':'password', 'old_pass':first, 'new_pass': second, '_xsrf':xsrf},
                success: function(para) {
                    alert(para);
 //                   alert("密码修改成功!");
                    window.location.reload();
                },
                error: function(para) {
                    alert(para);
                    //alert("密码修改失败!");
                }
            });
    })
    $('#upCenter').click('on',function () {
        $('.PersonalCenterBox').css({display:'block'});
        $('.uplistBox').css({display:'none'});
    })
})
function showPreview(source) {
    var file = source.files[0];
    if(window.FileReader) {
        var fr = new FileReader();
        fr.onloadend = function(e) {
            document.getElementById("portrait").src = e.target.result;
        };
        fr.readAsDataURL(file);
    }
}
function editCenter(){
    $('.PersonalCenterBox').css({display:'none'});
    $('.uplistBox').css({display:'block'});
}
