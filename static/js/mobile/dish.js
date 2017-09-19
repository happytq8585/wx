function get_cookie_by_name(name)
{
    var start = document.cookie.indexOf(name);
    if (start != -1) {
        var res = "";
        var end  = document.cookie.indexOf(";", start+1);
        if (end == -1) {
            res = document.cookie.substring(start+name.length+1);
        } else {
            res = document.cookie.substring(start+name.length+1, end);
        }
        return res;
    }
    return "";
}

$('.evaluate').click(function() {
        var cnt   = $('#evaluate').val();
        var star  = $('#rating').val();
        if (star == null) {
            alert("没有评等级");
            return -1; 
        }   
        if (cnt == null) {
            alert("没有评论内容");
            return -1; 
        }
        $('.canteenListCenter').attr('hidden', 'hidden');
        var xsrf = get_cookie_by_name("_xsrf");
        var did  = $('.identifier').attr('id');
        $.ajax({
            'url': '/comment',
            'type': 'POST',
            'data': {'_xsrf':xsrf, 'content':cnt, 'num':star, 'did':did},
            success: function(para) {
                //alert('评论成功');
                window.location.reload();
            },
            error: function(para) {
            }
        });
});

function delete_dish(did) {
    var xsrf = get_cookie_by_name("_xsrf");
    $.ajax({
        'url': '/delete',
        'type': 'POST',
        'data': {'_xsrf': xsrf, 'id': did},
        success: function(para) {
            //alert('删除成功');
            window.location.reload();
        },
        error: function(para) {
        }
    });
}
