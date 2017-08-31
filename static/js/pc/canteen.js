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
var r_num=0;
var r_price=0;
var r_did=0;
function order_dish(obj, did) {
    r_did = parseInt(did);
    $('.Reserve').css({display:'block'});
    var day = get_day('-');
    var unit =  $(obj).prev().children('.canteenmenuMaterial').html().split('/')[1];
    unit.replace(/^\s+|\s+$/g, '');
    $('#unit').html(unit + '数');
    var price = $(obj).prev().children('.canteenmenuMaterial').html().split('元')[0];
    $('#reservePrice').html($(obj).prev().children('.canteenmenuMaterial').html());
    $('#reserveTime').html(day);
}
function fill_canteen(day) {
    var xsrf = get_cookie_by_name('_xsrf');
    $.ajax({
        'url':'/canteen',
        'type':'POST',
        'data':{'_xsrf':xsrf, 'day':day},
        success: function(para) {
            $('.canteenLeft').empty();
            $('.canteenLeft').append(para);
            $('input[name="_xsrf"]').val(xsrf);
            $('input[name="day"]').val(day);
            $('.canteenmenuBtn').bind('click', function() {
                    var did = $(this).attr('value');
                    order_dish(this, did);
            });
        },
        error: function(para) {
        }
    });
}
$(function () {
    var today ;
    today = $('#calendar').find('.item-curDay').attr("data");
    today += "食堂菜谱";
    $('.Canteen').find('h3').html(today);
    today = get_day('-'); 
    fill_canteen(today);
    $('.item-curMonth').click('on',function () {
        var day = get_day('');
        $('.Canteen').find('h3').html(day + "食堂菜谱");
        day = get_day('-');
        fill_canteen(day);
    });
    $('.item-curDay').click('on',function () {
        var day = get_day('');
        $('.Canteen').find('h3').html(day + "食堂菜谱");
        day = get_day('-');
        fill_canteen(day);
    });
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
        var g_time = $('#input1').val();
        if (g_time == null || g_time == '') {
            alert('请确认取单时间');
            return -1;
        }
        var xsrf   = get_cookie_by_name('_xsrf');
        var unit   = $('#reservePrice').html().split('/')[1];
        r_price    = $('#reservePrice').html().split('元')[0];
        r_price    = parseFloat(r_price)*100;
        r_num      = $('#allnum').val();
        if (r_num == null) {
            alert('请确认下单数目');
            return -1;
        }
        r_num      = parseInt(r_num);
        if (r_did == null) {
            alert('请选择要订的食品');
            return -1;
        }
        var dish_time = $('#reserveTime').html();
        if (dish_time > g_time) {
            alert('取单时间应在菜的时间之后');
            return -1;
        }
        var D = {'r_did':r_did, 'num': r_num, 'r_price': r_price, 'g_time':g_time, 'unit':unit, '_xsrf':xsrf};
        $.ajax({
            url: '/order',
            type: 'POST',
            data: D,
            success: function(para) {
                r_did = null;
                alert('下单成功');
            },
            error: function(para) {
                r_did = null;
                alert('下单失败');
            }
        });
    })


    $('input:file').change("on",function (e) {
        console.log(e.target.value);
        $('.upimg').find('img').attr("src",e.target.value);
    })

    $('#allnum').change('on',function () {
        var price = $('#reservePrice').html().split('元')[0];
        price = parseFloat(price)*100;
        var num = $(this).val();
        num = parseInt(num);
        var sum = num*price;
        sum = parseFloat(sum)/100.0;
        sum = sum.toFixed(2);
        $('#allPrice').html(sum+'元');
    })

    $('.calendar-date').find('.item').click('on',function () {
        console.log($(this).attr('data'));
    })

    //取单时间
    $('#input1').shijian({
        okfun:function(sjObj){//确认时间时候执行事件
            Reservetime = $(sjObj).val();
        },
    });
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
//删除指定的菜
function delMenu(e, id){
    var xsrf = get_cookie_by_name('_xsrf');
    $.ajax({
        url: '/delete',
        type:'POST',
        data: {'id': id, '_xsrf': xsrf},
        success: function(para) {
            alert('delete success');
        },
        error: function(para) {
            if (para.status == 400) {
                alert("该菜已经有人预定了,不能删除了!");
            }
            else {
                alert('delete failed!');
            }
        }
    });
}
