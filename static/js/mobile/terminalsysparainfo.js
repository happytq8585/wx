$(function () {
    var path = $('#path').val();

    $('.data-app-configure').on('click', function (e) {
        layer.open({
            type: 1,
            title: '应用配置',
            area: '566px',
            content: $('#modal-edit'),
            success: function (dom, index) {
                $.post(path + '/terminalsysparainfo/listApplicationmanager.json', {
                    id: $(e.target).parents('tr').data('id')
                }, function (result) {
                    if (result['success']) {
                        var data = result['result'];
                        var html;
                        html = "<div class='col-md-2'>";
                        for(var i=0; i<data.length;i++){
                            html+="<input type='checkbox'/></div>"+
                            "<div class='col-md-8'>"+
                            "<span type='text' name='name' id='name' >"+data[i].name+"</span></div>";
                        }
                        $('#applist').append(html)
                    }

                })
            },
            btn: ['确认', '取消'],
            yes: function (index) {
                $.post(path + '/terminalsysparainfo/update.json', $('#form-edit').serialize(), function (result) {
                    if (result['success']) {
                        layer.close(index);
                        $('#data-query').click();
                    }
                });
            },
            btn2: function (index) {
                layer.close(index);
            }
        })
    });


    /*设置错误提示信息自动消失方法*/
    function errmsg(content, delay) {
        $('.error-msg.alert').addClass('show');
        $('.error-msg strong').text(content);
        setTimeout(function () {
            $('.error-msg.alert').removeClass('show');
            $('.error-msg.alert').alert();
        }, delay)

    }

    /*表格全选功能*/
    $('.check-all').click(function () {
        var checkel = $('.qurey-result table .check-ls');
        if (this.checked) {
            checkel.prop('checked', true)
        } else {
            checkel.prop('checked', false)
        }
    })


});
