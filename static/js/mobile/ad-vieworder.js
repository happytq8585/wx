$(".delevo").click(function(){
    $(this).parent().parent().parent().parent().css({'display':'none'});
});
$(".complete").click(function(){
    $('#myModal').modal('show');
    $(".modal").css({'display':'block'});
   // 如果确定执行
    /*$(this).closest(".from-order").css({'display':'none'});*/
});
$(".pre").click(function(){
    /*$(".modal-backdrop").hide();*/
    /*$('#myModal').hide();*/
   /* $(".modal").css({'display':'none'});*/
  /* reverse.js这里改成如下这样*/
    $('#myModal').modal('hide');
    $(".modal").css({'display':'none'});

});
$(".tab-current").click(function(){

});
$(".tab-statistics").click(function(){

});
$(".tab-history").click(function(){

})