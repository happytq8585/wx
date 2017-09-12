$(function() {
    $('.form_datetime').datetimepicker({
        minView: "month", //选择日期后，不会再跳转去选择时分秒
        language: 'zh-CN',
        format: 'yyyy-mm-dd',
        todayBtn: 1,
        autoclose: 1,
    }).on('changeDate',function(){
        var day = $('.input-text').val();
    });

    /*点击预定按钮*/
    $(".re-older").click(function(){
        $(".menu-edit").show();
        $(".zongjia").show();
        $(".tijiao").show();
        $(".yuding").css({'display':'none'});
    });
   /* 点击提交按钮*/
    $(".subm").click(function(){
        $('#myModal').modal('show');
        $(".modal").css({'display':'block'});
    });


   /* 点击确定按钮菜单传入的ajax*/
    $(".pre").click(function(){
        $(".modal-backdrop").hide();
        $('#myModal').hide();
        $(".modal").css({'display':'none'});
     /*   $(".menu-edit").css({'display':'none'});
        $(".zongjia").css({'display':'none'});
        $(".tijiao").css({'display':'none'});
        $(".yuding").css({'display':'block'});*/
     $(".tijiao").css({'display':'none'});
     $(".tjsu").css({'display':'block'});

    })







    // 数量减
    $(".minus").click(function () {
        var t = $(this).parent().find('.num');
        t.text(parseInt(t.text()) - 1);
        if (t.text() <= 0) {
            t.text(0);
        }
        setTotal();
    });
    // 数量加
    $(".plus").click(function () {
        var t = $(this).parent().find('.num');
        t.text(parseInt(t.text()) + 1);
        if (t.text() <= 1) {
            t.text(1);
        }
        setTotal();
    });

    function setTotal() {
        var allprice = 0; //总价
        var oprice = 0; //店铺总价

        var arrList = $(".from-order").find(".lt-rt");


        $(".from-order").find(".lt-rt").each(function () {
            /*  if ($(this).find(".num").text() >0) {*/

            var num = parseInt($(this).find(".num").text()); //得到菜品的数量

            var price = parseInt($(this).parent().find(".price").text()); //得到菜品的单价

            oprice = num * price;


            /*     }*/
            $(this).parents('.operate').find(".oprice").text(oprice.toFixed(2));
            var oneprice = parseFloat($(this).find(".oprice").text());

            allprice += oprice; //计算所有店铺的总价
            console.log(allprice)

        });


        //  var oneprice = parseFloat($(this).find(".oprice").text());
        //  allprice += oneprice; //计算所有店铺的总价


        $("#AllTotal").text(allprice.toFixed(2)); //输出全部总价
    }
    setTotal();







});
