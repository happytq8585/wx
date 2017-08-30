
$(function () {
    $(document).keydown(function(event) {
            if (event.keyCode == 13) {
                $('.logBtn').trigger('click');
            }
    });
    //立即登录按钮事件以及判断
    $('.logBtn').click('on',function () {
        console.log($('.logname').val(),$('.logpass').val());
        var logname = $('.logname').val();
        var logpass = $('.logpass').val();
        if(logname==''&&logpass==''){
            $('.errorword').html('用户名，密码不能为空');
            $('.errorword').css({display:'block'});
        }else if(logname==''&&logpass!=''){
            $('.errorword').html('用户名不能为空');
            $('.errorword').css({display:'block'});
            console.log($('.errorword').val());
        }else if(logname!=''&&logpass==''){
            $('.errorword').html('密码不能为空');
            $('.errorword').css({display:'block'});
            console.log($('.errorword').val());
        }else{
            //将用户名，密码发送给后台经行验证，返回结果，判断是否正确
            var xsrf = get_cookie_by_name('_xsrf');
            $.ajax({
                'Cookie': document.cookie,
                url: '/login',
                type: 'POST',
                data: {'_xsrf':xsrf, 'real_name':logname, 'password':logpass},
                success: function(para) {
                    var root = window.location.hostname + ':' + window.location.port + '/';
                    window.location.href =  'http://' + root + 'canteen';
                },
                error: function(para) {
                    if (para.status == 400) {
                        alert("login failed!");
                    }
                    else {
                        alert("login error!");
                    }
                }
            });
        }
    })


    $('.loginput').find('input').focus(function () {
        $('.errorword').css({display:'none'});
    })
})
