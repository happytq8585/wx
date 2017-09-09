$(function () {
    var path = $('#path').val();

    /** 新增弹出框 */
    $('#data-add').on('click', function (e) {
        layer.open({
            type: 1,
            title: '增加',
            area: '566px',
            content: $('#modal-edit'),
            success: function (dom, index) {
                $('#id_qo').removeAttr('readonly');
                $('#form-edit').find('input').each(function (index, input) {
                    $(input).val('');
                });

            },
            btn: ['确认', '取消'],
            yes: function (index) {
                var specialfunction = "";
                $('.checkbox-inline input[type=checkbox]').each(function(){
                    var flag = ($(this).is(":checked")) ? 1 : 0;
                    specialfunction += flag;
                })
                $("#form-specialfunction").val(specialfunction);
                $.post(path + '/transactiontypeinfo/add.json', $('#form-edit').serialize(), function (result) {
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

    /*修改弹出框*/
    $('.data-modify').on('click', function (e) {
        layer.open({
            type: 1,
            title: '修改',
            area: '566px',
            content: $('#modal-edit'),
            success: function (dom, index) {
                $('#id_qo').attr("readonly","readonly");
                $.post(path + '/transactiontypeinfo/get.json', {
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
                var specialfunction = "";
                $('.checkbox-inline input[type=checkbox]').each(function(){
                    var flag = ($(this).is(":checked")) ? 1 : 0;
                    specialfunction += flag;
                })
                $("#form-specialfunction").val(specialfunction);
                $.post(path + '/transactiontypeinfo/update.json', $('#form-edit').serialize(), function (result) {
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

    /** 勾选修改 */
    $('#data-update').on('click', function (e) {
        var checkedInputs = $('.qurey-result table .check-ls:checked');
        if (checkedInputs.length == 1){
            layer.open({
                type: 1,
                title: '修改',
                area: '566px',
                content: $('#modal-edit'),
                success: function (dom, index) {
                    $('input[name="id"]').attr("readonly","readonly");
                    $.post(path + '/transactiontypeinfo/get.json', {
                        id: $('.qurey-result table .check-ls:checked').parents('tr').data('id')
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
                    $.post(path + '/transactiontypeinfo/update.json', $('#form-edit').serialize(), function (result) {
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
        } else {
            errmsg('请选中一条数据', 2000);
        }
    });
    /** 批量删除 */
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
                        form.push('<input type="text" name="ids" value="' + id + '">');
                    });
                    form.push('</form>');
                    $.post(path + '/transactiontypeinfo/delete_all.json', $(form.join('')).serialize(), function (result) {
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

    /*/!*修改弹出框*!/
    $('#data-update').on('click', function (e) {
        layer.open({
            type: 1,
            title: '修改',
            area: '566px',
            content: $('#modal-edit'),
            success: function (dom, index) {
                $.post(path + '/transactiontypeinfo/get.json', {
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
                $.post(path + '/transactiontypeinfo/update.json', $('#form-edit').serialize(), function (result) {
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
    });*/

    /*删除单个弹出框*/
    $('.data-del').on('click', function (e) {
        layer.alert('确定删除吗?', {
            icon: 2, btn: ['确认', '取消'], yes: function (index) {
                $.post(path + '/transactiontypeinfo/delete.json', {
                    transactiontypeinfoId: $(e.target).parents('tr').data('id')
                }, function (result) {
                    if (result['success']) {
                        layer.close(index);
                        $('#data-query').click();
                    }
                });
            }
        });

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
