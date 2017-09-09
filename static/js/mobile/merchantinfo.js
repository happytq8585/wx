$(function () {
    var path = $('#path').val();
    $.ajax({
        url: path + "/regioninfo/list.json",
        data: {
            regionlevel:1,
        },
        type: "post",
        async: true,
        success: function (result) {
            if (result['success']) {
                var data = result['result'];
                var html;
                html+="<option value='0000'>请选择</option>";
                for(var i=0; i<data.length;i++){
                    html+="<option value="+data[i].regionid+">"+data[i].regionname+"</option>";
                }
                $('#province_qo').append(html)
                $.ajax({
                    url: path + "/regioninfo/list.json",
                    data: {
                        regionlevel: 2,
                        regionid:$('#province_qo option:selected').val()
                    },
                    type: "post",
                    async: true,
                    success: function (result) {
                        if (result['success']) {
                            var html;
                            var city_val=$('#city_1').val();
                            var city_text=$('#city_1').text();
                            $('#city_qo').html("");
                            var data = result['result'];
                            if(city_text!=null&&city_text!=""){
                                html+="<option value="+city_val+">"+city_text+"</option>";
                            }
                            html+="<option value=''>请选择</option>"
                            for(var i=0; i<data.length;i++){
                                html+="<option value="+data[i].regionid+"'>"+data[i].regionname+"</option>";
                            }
                            $('#city_qo').append(html)
                        }
                    }, error: function (data) {
                        errmsg("通信失败", 4000);
                    }
                });
            }
        }, error: function (data) {
            errmsg("通信失败", 4000);
        }
    });

    $('#province_qo').on('change',function (e) {
        $.ajax({
            url: path + "/regioninfo/list.json",
            data: {
                regionlevel: 2,
                regionid:$('#province_qo option:selected') .val()
            },
            type: "post",
            async: true,
            success: function (result) {
                if (result['success']) {
                    $('#city_qo').html("<option value=''>请选择</option>");
                    var data = result['result'];
                    var html;
                    for(var i=0; i<data.length;i++){
                        html+="<option value="+data[i].regionid+"'>"+data[i].regionname+"</option>";
                    }
                    $('#city_qo').append(html)
                }
            }, error: function (data) {
                errmsg("通信失败", 4000);
            }
        });
    })

    $('.date').datetimepicker({
            language:'zh-CN',
            format :'yyyy-mm-dd',
            minView:4,
            autoclose:true,
            todayHighlignt:true,
    });

    $('.data-start').on('click', function (e) {
        var sta=$(e.target).parents('tr').data('status')
        if(sta!='0'){
            errmsg("不能启用",4000);
            return;
        }
        layer.alert('确定启用吗?', {
            icon: 2, btn: ['确认', '取消'], yes: function (index) {
                $.post(path + '/merchantinfo/changestatus.json', {
                    id: $(e.target).parents('tr').data('id'),
                    status:'1'
                }, function (result) {
                    if (result['success']) {
                        layer.close(index);
                        $('#data-query').click();
                    }
                });
            }
        });
    });

    $('#data-stop').on('click', function (e) {
        var sta=$(e.target).parents('tr').data('status')
        if(sta!='1'){
            errmsg("不允许停用",4000);
            return;
        }
        layer.alert('确定停用吗?', {
            icon: 2, btn: ['确认', '取消'], yes: function (index) {
                $.post(path + '/merchantinfo/changestatus.json', {
                    id: $(e.target).parents('tr').data('id'),
                    status:'2'
                }, function (result) {
                    if (result['success']) {
                        layer.close(index);
                        $('#data-query').click();
                    }
                });
            }
        });
    });
    $('#data-cancel').on('click', function (e) {
        var sta=$(e.target).parents('tr').data('status')
        if(sta!='9'){
            errmsg("不允许停用",4000);
            return;
        }
        layer.alert('确定注销吗?', {
            icon: 2, btn: ['确认', '取消'], yes: function (index) {
                $.post(path + '/merchantinfo/changestatus.json', {
                    id: $(e.target).parents('tr').data('id'),
                    status:'9'
                }, function (result) {
                    if (result['success']) {
                        layer.close(index);
                        $('#data-query').click();
                    }
                });
            }
        });
    });


    $('#data-rate').on('click', function (e) {
        layer.open({
            type: 1,
            title: '费率',
            zIndex:999,
            area: '566px',
            content: $('#modal-rate'),
            success: function (dom, index) {
                $('#form-edit').find('input').each(function (index, input) {
                    $(input).val('');
                });
            },
            yes: function (index) {
                $.post(path + '/merchantinfo/add.json', $('#form-edit').serialize(), function (result) {
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

    /** 新增弹出框 */
    $('#data-add').on('click', function (e) {
        layer.open({
            type: 1,
            title: '增加',
            area: ['900px', '500px'],
            zIndex:-99000,
            content: $('#modal-edit'),
            skin:'layui-layer-molv',
            success: function (dom, index) {
                $('#form-edit').find('input').each(function (index, input) {
                    $(input).val('');
                });
            },
            btn: ['确认', '取消'],
            yes: function (index) {
                $.post(path + '/merchantinfo/add.json', $('#form-edit').serialize(), function (result) {
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
                    $.post(path + '/merchantinfo/batch_delete.json', $(form.join('')).serialize(), function (result) {
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

    /*修改弹出框*/
    $('.data-modify').on('click', function (e) {
        layer.open({
            type: 1,
            title: '修改',
            area: ['900px', '500px'],
            content: $('#modal-edit'),
            success: function (dom, index) {
                $.post(path +'/merchantinfo/get.json', {
                    mid: $(e.target).parents('tr').data('id')
                }, function (result) {
                    if (result['success']) {
                        var data = result['result'];
                        $('#form-edit').find('input').each(function (index, input) {
                            $(input).val(data[$(input).attr('name')]);
                        });
                        $('#form-edit').find('select').each(function (index, select) {
                            $(select).val(data[$(select).attr('name')]);
                        });
                    }
                })
            },
            btn: ['确认', '取消'],
            yes: function (index) {
                $.post(path +'/merchantinfo/update.json', $('#form-edit').serialize(), function (result) {
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

    /*详情弹出框*/
    $('.data-details').on('click', function (e) {
        layer.open({
            type: 1,
            zIndex:  999,
            title: '修改',
            area: ['900px', '500px'],
            content: $('#modal-details'),
            success: function (dom, index) {
                $.post(path +'/merchantinfo/get.json', {
                    mid: $(e.target).parents('tr').data('id')
                }, function (result) {
                    if (result['success']) {
                        var data = result['result'];
                        $('#form-detail').find('input').each(function (index, input) {
                            $(input).val(data[$(input).attr('name')]);
                        });
                        $('#form-detail').find('select').each(function (index, select) {
                            $(select).val(data[$(select).attr('name')]);
                        });
                    }
                })
            },
        })
    });


    /*删除单个弹出框*/
    $('.data-del').on('click', function (e) {
        layer.alert('确定删除吗?', {
            icon: 2, btn: ['确认', '取消'], yes: function (index) {
                $.post(path + '/merchantinfo/delete.json', {
                    ids: $(e.target).parents('tr').data('id')
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

    $('.btn-reset').click(function () {
        $("#id_qo").val("");
        $("#province_qo").val("0000");
        $("#city_qo").val("");
        $("#merchantname_qo").val("");
        $("#status_qo").val("");
        $("#cardtype_qo").val("");
    })
});
