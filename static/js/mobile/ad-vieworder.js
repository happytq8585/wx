
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
$("#delevo").bind("click", function(){
//    $('#myModal').show();
//    $(".modal").show();
    //$(this).parent().parent().parent().parent().css({'display':'none'});
});
$(".complete").click(function(){
    $('#myModal').modal('show');
    $(".modal").css({'display':'block'});
   // 如果确定执行
    /*$(this).closest(".from-order").css({'display':'none'});*/
});

var orderid = "";
$(".pre").click(function(){
    $.ajax({
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
