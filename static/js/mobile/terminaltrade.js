$(function () {
    var path = $('#path').val();

    $(".btn-edit-type").click(function(e){
        layer.open({
            type: 1,
            title: '修改',
            area: '440px',
            content: $('#modal-edit-transaction-type'),
            success: function (dom, index) {
                //初始化勾选框
                initTransactionTypeCheckBox();
            },
            btn: ['确认', '取消'],
            yes: function (index) {
                var checkList = [];
                $("#modal-edit-transaction-type .ckb-transaction-type:checked").each(function(){
                    var checkId = $(this).val();
                    checkList.push(checkId);
                });
                alert(checkList.join("_"));
                /*$.post(path + '/terminalstock/update.json', $('#form-edit').serialize(), function (result) {
                    if (result['success']) {
                        layer.close(index);
                        $('#data-query').click();
                    }
                });*/
            },
            btn2: function (index) {
                layer.close(index);
            }
        })
    });

    $(".btn-edit-auth").click(function(e){
        var id = $(this).parents('tr').data('id');
        var rtype = 3;      //3为终端
        layer.open({
            type: 1,
            title: '修改',
            area: '566px',
            content: $('#modal-edit-quotainfo'),
            success: function (dom, index) {
                $("#form-quotainfo-id").text(id);
                $('#form-edit-quotainfo').find('input,select').val("");

                var formData = {id: id, "rtype": rtype};
                $.post(path + '/terminaltrade/getQuotainfo.json', formData, function (result) {
                    var row = result.quotainfoVo;
                    if(!!row){
                        $('#form-edit-quotainfo').find('input,select').each(function (index, input) {
                            $(input).val(row[$(input).attr('name')]);
                        });
                    }
                });
            },
            btn: ['确认', '取消'],
            yes: function (index) {

            },
            btn2: function (index) {
                layer.close(index);
            }
        })
    });

    /*/!** 新增弹出框 *!/
    $('#data-add').on('click', function (e) {
        layer.open({
            type: 1,
            title: '增加',
            area: '566px',
            content: $('#modal-edit'),
            success: function (dom, index) {
                $('#form-edit').find('input').each(function (index, input) {
                    $(input).val('');
                });
            },
            btn: ['确认', '取消'],
            yes: function (index) {
                $.post(path + '/terminalstock/add.json', $('#form-edit').serialize(), function (result) {
                    if (result['success']) {
                        $('#data-query').click();
                    }
                    layer.close(index);
                });
            },
            btn2: function (index) {
                layer.close(index);
            }
        })
    });

    /!** 批量删除 *!/
    $('#data-delete-all').on('click', function (e) {
        var checkedInputs = $('.qurey-result table .check-ls:checked');
        if (checkedInputs.length > 0) {
            layer.alert('确定删除全部选中的数据吗?', {
                icon: 2, btn: ['确认', '取消'], yes: function (index) {
                    var ids = [];
                    checkedInputs.each(function (i, input) {
                        ids.push($(input).parents('tr').data('id'));
                    });
                    var form = ['<form>'];
                    $.each(ids, function (i, id) {
                        form.push('<input type="text" name="terminalstockIds" value="' + id + '">');
                    });
                    form.push('</form>');
                    $.post(path + '/terminalstock/batch_delete.json', $(form.join('')).serialize(), function (result) {
                        if (result['success']) {
                            $('#data-query').click();
                        }
                    });
                    layer.close(index);
                }
            });
        } else {
            errmsg('未选中任何数据', 2000);
        }
    });

    /!*修改弹出框*!/
    $('.data-modify').on('click', function (e) {
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
                        $('#form-edit').find('input,select').each(function (index, input) {
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

    /!*删除单个弹出框*!/
    $('.data-del').on('click', function (e) {
        layer.alert('确定删除吗?', {
            icon: 2, btn: ['确认', '取消'], yes: function (index) {
                $.post(path + '/terminalstock/delete.json', {
                    terminalstockId: $(e.target).parents('tr').data('id')
                }, function (result) {
                    if (result['success']) {
                        layer.close(index);
                        $('#data-query').click();
                    }
                });
            }
        });

    });

    $("#data-add-all").click(function(){
        alert("data-add-all: TODO");
    })
    $("#issued-all").click(function(){
        alert("issued-all: TODO");
    })
    $("#import-terminal").click(function(){
        alert("import-terminal: TODO");
    })

    /!*设置错误提示信息自动消失方法*!/
    function errmsg(content, delay) {
        $('.error-msg.alert').addClass('show');
        $('.error-msg strong').text(content);
        setTimeout(function () {
            $('.error-msg.alert').removeClass('show');
            $('.error-msg.alert').alert();
        }, delay)

    }

    /!*表格全选功能*!/
    $('.check-all').click(function () {
        var checkel = $('.qurey-result table .check-ls');
        if (this.checked) {
            checkel.prop('checked', true)
        } else {
            checkel.prop('checked', false)
        }
    })*/

    function initTransactionTypeCheckBox(){
        $("#modal-edit-transaction-type .ckb-transaction-type").val("");
    }

});
