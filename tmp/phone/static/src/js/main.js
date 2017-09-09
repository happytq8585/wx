/*
 *   所有也页面都需要的脚本
 * */

$(".form_datetime").datetimepicker({
    format: "dd MM yyyy - hh:ii",
    autoclose: true,
    todayBtn: true,
    pickerPosition: "bottom-left"
});

/*tab转换*/
$(function () {
    $('#myTab a:first').tab('show')
})


$(".cd").click(function(){
    $(".cd").parent().parent().parent().parent().parent().remove();
})




/*/!*评分星星*!/
jQuery(document).ready(function () {
    var $inp = $('#rating-input');
    $inp.rating({
        min: 0,
        max: 5,
        step: 1,
        size: 'md',
        showClear: false
    });
    $('#btn-rating-input').on('click', function () {
        $inp.rating('refresh', {
            showClear: true,
            disabled: !$inp.attr('disabled')
        });
    });
    $('.btn-danger').on('click', function () {
        $("#kartik").rating('destroy');
    });

    $('.btn-success').on('click', function () {
        $("#kartik").rating('create');
    });


});*/



/*
$(document).ready(function() {
    $('#defaultForm')
        .bootstrapValidator({
            message: 'This value is not valid',
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                username: {
                    message: '用户名无效',
                    validators: {
                        notEmpty: {
                            message: '用户名是必需的，不能是空的'
                        },
                        stringLength: {
                            min: 6,
                            max: 30,
                            message: '用户名必须大于6，小于30字符长'
                        },
                        /!*remote: {
                            url: 'remote.php',
                            message: 'The username is not available'
                        },*!/
                       /!* regexp: {
                            regexp: /^[a-zA-Z0-9_\.]+$/,
                            message: '用户名只能由字母、数字、点和下划线组成'
                        }*!/
                    }
                },
                password: {
                    validators: {
                        notEmpty: {
                            message: '密码是必需的，不能是空的'
                        }
                    }
                }
            }
        })
        .on('success.form.bv', function(e) {
            // Prevent form submission
            e.preventDefault();

            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
            var bv = $form.data('bootstrapValidator');

            // Use Ajax to submit form data
            $.post($form.attr('action'), $form.serialize(), function(result) {
                console.log(result);
            }, 'json');
        });
});*/

/*
 *   圣杯布局左侧边栏固定宽度可收缩布局插件
 *   $('.wlk-grail').GrailGrid
 * */
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

