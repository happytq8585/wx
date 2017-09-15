/*
 *   所有也页面都需要的脚本
 * */
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
    var url = '/menu?day=' + day;
    $.ajax({
        'url': '/menu',
        'type': 'GET',
        'data': {'day':day, 'data':1},
        success: function(para) {
            $('#tabData').replaceWith(para);
        },
        error: function(para) {
        }
    });
});

$('.plus-dish').click(function(){
    var day = $('.form_datetime').children('input[name="day"]').val();
    if (day == null || day.length == 0) {
        alert('请选择时间');
        return -1;
    }
    location.href = '/add?day=' + day;
});

/*tab转换*/
$(function () {
    $('#myTab a:first').tab('show')
})


jQuery.fn.extend({
    GrailGrid: function () {
        var autoHeight = $(this).find('[data-height="auto"]')
        autoHeight.each(function () {
            var parent = $(this).parent();
            var bro = $(this).siblings();
            var broHeight = 0;
            $(bro).each(function () {
                var everyHeight = $(this).outerHeight();
                broHeight += everyHeight;
            });
            $(this).css({
                'box-sizing': 'border-box',
                'width': '100%',
                /* 'height': parent.height() - broHeight,
                 'overflow-y': 'auto',
                 'overflow-x': 'hidden'*/
            })
        })
        $(document).on('click', '#fold-btn', foldAside);
        var toggle = true;

        function foldAside() {
            var root = $(this).parents('.wlk-grail');

            if (toggle) {
                toggle = false;
                $(this).html('<i class="iconfont icon-rtarrow"></i>');
                root.animate({
                    'padding-left': '30px'
                })
            } else {
                toggle = true;
                $(this).html('<i class="iconfont icon-lfarrow"></i>');
                root.animate({
                    'padding-left': '194px'
                })

            }

        }
    }
});

