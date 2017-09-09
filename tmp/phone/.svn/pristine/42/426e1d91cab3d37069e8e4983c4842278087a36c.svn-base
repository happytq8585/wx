$(function () {
    var path = $('#path').val();

    $('.data-type').click(function(e){
        var mname = $(this).parent().siblings().eq(2).html();
        layer.open({
            type: 1,
            title: '修改',
            area: '440px',
            content: $('#modal-edit-type'),
            success: function (dom, index) {
                $('#mname').text(mname);
                initTransactionTypeCheckBox();
            },
            btn: ['确认', '取消'],
            yes: function (index) {
                var checkList = [];
                $("#modal-edit-type .ckb-transaction-type").each(function(){
                    var checkId = $(this).val();
                    checkList.push(checkId);
                });
            },
            btn2: function (index) {
                layer.close(index);
            }
        })
    });

    /*$(".data-type").on('click', function (e){
       /!* var mername = $(this).parent().siblings().eq(2).val();
        console.log(mername);*!/
        layer.open({
            type: 1,
            title: '修改',
            area: '440px',
            content: $('#modal-edit-type'),
            success: function (dom, index) {
                console.log(1111);
                /!*$("#mername").text(mername);
                //初始化勾选框
                initTransactionTypeCheckBox();*!/
            },
            btn: ['确认', '取消'],
            yes: function (index) {
                /!*var checkList = [];
                $("#modal-edit-transaction-type .ckb-transaction-type:checked").each(function(){
                    var checkId = $(this).val();
                    checkList.push(checkId);
                });*!/
                alert(checkList.join("_"));
                /!*$.post(path + '/terminalstock/update.json', $('#form-edit').serialize(), function (result) {
                 if (result['success']) {
                 layer.close(index);
                 $('#data-query').click();
                 }
                 });*!/
            },
            btn2: function (index) {
                layer.close(index);
            }
        })
    });*/

    $(".data-limit").click(function(e){
        var id = $(this).parents('tr').data('id');
        var merchantname = $(this).parent().siblings().eq(2).html();
        var rtype = 3;      //3为终端
        layer.open({
            type: 1,
            title: '修改',
            area: '566px',
            content: $('#modal-edit-quotainfo'),
            success: function (dom, index) {
                $("#form-quotainfo-merchantname").text(merchantname);
                $('#form-edit-quotainfo').find('input,select').val("");

                var formData = {id: id, "rtype": rtype};
                $.post(path + '/terminaltrade/getQuotainfo.json', formData, function (result) {
                    var row = result.quotainfoVo;
                    if(!!row){
                        $('#form-edit-limit').find('input,select').each(function (index, input) {
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
    function initTransactionTypeCheckBox(){
        $("#modal-edit-type .ckb-transaction-type").val("");
    }
});

