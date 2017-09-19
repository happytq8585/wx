/*$(".delevo").click(function(){
    var fr=$(this).parent().parent().parent().parent().css({'display':'none'});
});*/
var ORDERID = "";
$(".pre").click(function(){
    $('#myModal').modal('hide');
    $(".modal").css({'display':'none'});
    delete_order(ORDERID);
});
function set_oid(oid) {
    ORDERID = oid;
}
$(".dele").click(function(e){
     $(e.target).parent().parent().parent().parent().css({'display':'none'});
     ORDERID = $(e.target).orderid;
});


$(".edit-view").click(function(){
    /*每个菜品的名称 */
    var forder=$(this).closest(".from-order");
        forder.each(function () {
        var dishName = $(this).find(".d-name").text(); //菜品的名称
        var  orderTime= $(this).find(".xiadan").text();//下单时间
        var  amount= $(this).find(".amount").text();//下单时间
        var takeTime=$(this).find(".qudan").text(); //取单时间
        var atotle=$(this).find(".atotle").text();//菜品单价
        var state=$(this).find(".state").text();//状态

    });
});

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
function delete_order(oid) {
    var xsrf = get_cookie_by_name('_xsrf');
    $.ajax({
        'url': '/delorder',
        'type': 'POST',
        'data': {'_xsrf': xsrf, 'id': oid},
        success: function(para) {
            alert('delete success!')
            $('#' + oid).remove();
        },
        error: function(para) {
        }
    });
}
$('.tab-current').click(function() {
    fill_tab_admin(0);
});
$('.tab-history').click(function() {
    fill_tab_admin(1);
});
function fill_tab_admin(i) {
    $.ajax({
        'url': '/order',
        'type': 'GET',
        'data': {'loc': i, 'data':1},
        success: function(para) {
            if (i == 0) {//left
                $('#current').empty();
                $('#current').append(para);
            } else if (i == 1){ //middle
                $('#history').empty();
                $('#history').append(para);
            }
        },
        error: function(para) {
        }
    });
}
fill_tab_admin(0);
