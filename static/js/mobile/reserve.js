
function setTotal() {
    var allprice = 0; //总价
    var oprice = 0; //店铺总价
    var arrList = $(".from-order").find(".lt-rt");
    $(".from-order").find(".lt-rt").each(function () {
            var num = parseInt($(this).find(".num").val()); //得到菜品的数量

            var price = parseFloat($(this).parent().parent().parent().find(".price").text()); //得到菜品的单价
            oprice = num * price;

            $(this).parents('.operate').find(".oprice").text(oprice.toFixed(2));
            var oneprice = parseFloat($(this).find(".oprice").text());

            allprice += oprice; //计算所有店铺的总价
            });
    $("#AllTotal").text(allprice.toFixed(2)); //输出全部总价
}

function plus(a) {
    var t = $(a).prev();
    t.val(parseInt(t.val()) + 1);
    if (t.val() <= 0) {
        t.val(1);
    }
    setTotal();
}
function minus (a) {
    var t = $(a).next();
    t.val(parseInt(t.val()) - 1);
    if (t.val() <= 1) {
        t.val(0);
    }
    setTotal();
}

$('.form_datetime').datetimepicker({
    minView: "month", //选择日期后，不会再跳转去选择时分秒
    language: 'zh-CN',
    format: 'yyyy-mm-dd',
    todayBtn: 1,
    autoclose: 1,
}).on('changeDate', function() {
    var y = $(".datetimepicker-years").find(".active").text();
    var m = $(".datetimepicker-months").find(".active").text();
    m     = parseInt(m);
    m     = m < 10 ? '0' + m : '' + m;
    var d = $(".datetimepicker-days").find(".active").text();
    d     = parseInt(d);
    d     = d < 10 ? '0' + d : '' + d;
    day   = y + '-' + m + '-' + d;
    $.ajax({
        'url': '/reserve',
        'type': 'GET',
        'data': {'day':day, 'data':1},
        success: function(para) {
            var len = para['len'];
            var data = para['data'];
            $('#datalist').replaceWith(data);
            $('.plus').bind('on', plus);
            if (len > 0) {
                $('.re-older').removeAttr('disabled');
            } else {
                $('.re-older').attr('disabled', 'disabled');
            }
        },
        error: function(para) {
        }
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
$(function() {
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
        var num = [];
        $('.num').each(function() {
            var n = $(this).val();
            n = parseInt(n)
            num.push(n);
        });
        if (num.length == 0) {
            alert('没有选择数量, 下单失败');
            return -1;
        }
        $('#myModal').modal('hide');
        $(".modal").css({'display':'none'});
        $(".tijiao").css({'display':'none'});
        $(".tjsu").css({'display':'block'});
        var xsrf = get_cookie_by_name('_xsrf'); 
        var ids = [];
        $('a').each(function() {
            var url = $(this).attr('href');
            if (url.indexOf('dish') != -1) {
                var id = url.split('=')[1];
                id = parseInt(id);
                ids.push(id);
            }
        });
        ids = ids.join('\t');
        num = num.join('\t');
        var data = ids + '\r' + num;
        var day = $('.input-txt').val();
        $.ajax({
            'url': '/reserve',
            'type': 'POST',
            'data': {'_xsrf':xsrf, 'data':data, 'day':day},
            success: function(para) {
            },
            error: function(para) {
            }
        });
    })
    $(".from-order").find(".a").each(function () {
        var img=$(this).attr("href");
    });
    setTotal();
});