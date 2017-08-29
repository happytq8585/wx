
function get_day(slice) {
    var datatime = $('.item-selected').attr('data');
    if (datatime == null) {
        datatime = $('.item-curDay').attr('data');
    }
     //日期数组【年，月，日】
    var dataarr = [datatime.substring(0,4),datatime.substring(4,6),datatime.substring(6)];
    return dataarr.join(slice);
}
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
function order_dish(obj) {
    $('.Reserve').css({display:'block'});
    var day = $('#date').attr('date');
    var price = $('.price').html();
    $('#reservePrice').html(price);
    $('#reserveTime').html(day);
}
$(function () {
    //打开预定弹窗
    $('.canteenmenuBtn').click('on',function () {
        order_dish(this);
    })

    //关闭预定弹窗
    $('.ReserveClose').click('on',function(){
        $('.Reserve').css({display:'none'});
    })
    //确定预定弹窗
    $('.ReserveBtn').click('on',function () {
        $('.Reserve').css({display:'none'});
        var num = $('#allnum').val();
        if (num == null) {
            alert('数目不正确');
            return -1;
        }
        var did = $('img').attr('id');
        if (did == null) {
            alert('菜的id不正确');
            return -1;
        }
        var g_time = $('#input1').val();
        if (g_time == null) {
            alert('取单时间不正确');
            return -1;
        }
        var price = $('.price').html().split('元')[0];
        if (price == null) {
            alert('价格不正确');
            return -1;
        }
        price = parseFloat(price)*100;
        price = parseInt(price);
        var unit  = $('.price').html().split('/')[1];
        if (unit == null) {
            alert('单位不正确');
            return -1;
        }
        var xsrf  = get_cookie_by_name('_xsrf');
        var D = {'r_did':did, 'num':num, 'r_price': price, 'g_time': g_time, 'unit':unit, '_xsrf':xsrf};
        $.ajax({
            url: '/order',
            type: 'POST',
            data: D,
            success: function(para) {
                alert('下单成功');
            },
            error: function(para) {
                alert('下单失败');
            }
        });
    });


    $('#allnum').change('on',function () {
        var price = $('#reservePrice').html().split('元')[0];
        price = parseFloat(price);
        $('#allPrice').html($(this).val()*price+'元');
    })

    //提交评论
    $('.UpdataBtn').click('on',function () {
        var star  = $('#rating').val();   //评论星星的数量；
        var words = $('#evaluate').val(); //评论文字的内容；
        if (star == null) {
            alert("没有评等级");
            return -1;
        }
        if (words == null) {
            alert("没有评论内容");
            return -1;
        }
        $(".star").removeAttr("onMouseOver");
        $(".star").removeAttr("onMouseOut");
        $(".star").attr("href", "");
        var id = $("img").attr("id");
        var xsrf = get_cookie_by_name("_xsrf");
        $.ajax({
            'Cookie': document.cookie,
            url:"/comment",
            type: "POST",
            data: {"id":id, "star":parseInt(star), "words":words, "_xsrf":xsrf},
            success: function(para) {
                alert(para);
                window.location.reload();
            },
            error: function(para) {
                alert(para);
                window.location.reload();
            }
        });
        //alert("OK");
    })
})
