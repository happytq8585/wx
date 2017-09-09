$(function () {
    $(function(){
        $ ( '#plan-add' ).on ( 'click', function ( e ) {
            layer.open ( {
                type : 1, title : '新增', area : ['900px', '500px'], content : $ ( '#modal-edit' ),
                skin: 'layui-layer-molv',
                success : function ( dom, index ) {
                    $ ( '#form-edit' ).find ( 'input' ).each ( function ( index, input ) {
                        $ ( input ).val ( '' );
                    } );
                }, btn : [ '确认', '取消' ], yes : function ( index ) {
                    //$ ( '#form-edit' ).submit();

                    if ( planConfigValidate () ) {
                        $.post ( baseUri + '', $ ( '#form-edit' ).serialize (),
                            function ( result ) {
                                if ( result[ 'success' ] ) {
                                    layer.close ( index );
                                    errmsg ( "新增成功", 4000 );
                                    search ();
                                } else {
                                    layer.alert ( "新增失败：原因是" + result.message );
                                }
                            } );
                    }
                }, btn2 : function ( index ) {
                    layer.close ( index );
                }
            } )
        } );
    });
    $(function(){
        $('#plan-delete').on('click',function () {
            layer.open({
                icon: 3,
                content:"确定要删除吗？",
                btn: ['确定', '关闭'],
                yes: function(index, layero){
                    layer.close(index);
                }
            })
        })
    });
    $(function(){
        $('#plan-detail').on('click',function () {
            layer.open({
                type:1,
                title:'详情',
                content:$('#modal-detail'),
                area: ['900px', '500px'],
                btn: ['确定', '关闭'],
                yes: function(index, layero){
                    layer.close(index);
                }

            })
        })
    });

})