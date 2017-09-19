
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
function fill_tab_admin(i) {
    $.ajax({
        'url': '/order',
        'type': 'GET',
        'data': {'loc': i, 'data':1},
        success: function(para) {
            if (i == 0) {//left
                $('#ad-current').empty();
                $('#ad-current').append(para);
            } else if (i == 1){ //middle
                $('#ad-statistics').empty();
                $('#ad-statistics').append(para);
            } else if (i == 2) { //right
                $('#ad-history').empty();
                $('#ad-history').append(para);
            }
        },
        error: function(para) {
        }
    });
}

var orderid = "";
var xsrf = get_cookie_by_name('_xsrf');

$(".pre").click(function(){
    $('#myModal').css({'display':'none'});
    $('.modal-backdrop').css({'display': 'none'});
    $('.tjsu').css({'display':'none'});
    var tmp = orderid.split('-');
    var mobile = tmp[tmp.length-1];
    $.ajax({
        'url': '/orderconfirm',
        'type': 'POST',
        'data': {'_xsrf': xsrf, 'orderid':orderid},
        success: function(para) {
            $('#' + orderid).remove();
            alert('订单号:' + orderid + '已取单');
            var cnt = '您的订单号' + orderid + '已经取单了';
            $.ajax({
                'url': '/msgsend',
                'type': 'POST',
                'data': {'_xsrf':xsrf, 'mobile': mobile, 'content': cnt},
                success: function(para) {
                },
                error: function(para) {
                }
            });
        },
        error: function(para) {
        }
    });
});
$(".tab-current").click(function(){
    fill_tab_admin(0);
});
$(".tab-statistics").click(function(){
    fill_tab_admin(1);
});
$(".tab-history").click(function(){
    fill_tab_admin(2);
})
fill_tab_admin(0);

  
function _confirm(oid) {
    orderid = oid;
}
