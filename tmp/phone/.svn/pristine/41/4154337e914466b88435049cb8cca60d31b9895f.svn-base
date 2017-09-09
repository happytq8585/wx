$(function () {
    var path = $('#path').val();

    /** 新增弹出框 */
    /** 批量删除 */

    /**发行*/
    $('.data-issue').on('click',function(e){
            var status = $(e.target).parent("td").prev().html();
            console.log(status);
            if(status == '未启用'){
                $.post(path + '/terminalstatus/issue.json',{
                    id: $(e.target).parents('tr').data('id')
                },function(result){
                    if (result['success']) {
                        $('#data-query').click();
                    }
                });
            }else{
                errmsg('只有入库的终端才可以发行操作', 2000);
            }
    });
    /**启用*/
    $('.data-start').on('click',function(e){
        var status = $(e.target).parent("td").prev().html();
        if(status == '停用'){
            $.post(path + '/terminalstatus/start.json' ,{
                id:$(e.target).parents('tr').data('id')
            },function (result){
                if(result['success']){
                    $('#data-query').click();
                }
            });
        }else{
            errmsg('只有停用的终端才可以启用操作', 2000);
        }
    });
    /**停用*/
    $('.data-stop').on('click',function(e){
        var status = $(e.target).parent('td').prev().html();
        if(status == '启用'){
            $.post(path+'/terminalstatus/stop.json' , {
                id:$(e.target).parents('tr').data('id')
            },function(result){
                if(result['success']){
                    $('#data-query').click();
                }
            });
        }else{
            errmsg('只有启用的终端才可以停用操作',2000);
        }
    });
    /**注销*/
    $('.data-cancel').on('click',function(e){
        var status = $(e.target).parent('td').prev().html();
            if(status == '停用'){
                $.post(path+'/terminalstatus/cancel.json',{
                    id: $(e.target).parents('tr').data('id')
                },function(result){
                    if (result['success']) {
                        $('#data-query').click();
                    }
                });
            }else{
                errmsg('只有停用的终端才可以发行操作', 2000);
        }
    });
    /**回收*/


    /*修改弹出框*/
    $('#data-update').on('click', function (e) {
        layer.open({
            type: 1,
            title: '修改',
            area: '566px',
            content: $('#modal-edit'),
            success: function (dom, index) {
                $.post(path + '/terminalstock/get.json', {
                    id: $(e.target).parents('tr').data('id')
                }, function (result) {
                    if (result['success']) {
                        var data = result['result'];
                        $('#form-edit').find('input').each(function (index, input) {
                            $(input).val(data[$(input).attr('name')]);
                        });
                    }
                })
            },
            btn: ['确认', '取消'],
            yes: function (index) {
                $.post(path + '/terminalstock/update.json', $('#form-edit').serialize(), function (result) {
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

    /*删除单个弹出框*/


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
