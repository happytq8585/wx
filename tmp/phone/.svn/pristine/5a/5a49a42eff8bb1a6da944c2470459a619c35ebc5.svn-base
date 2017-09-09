$(function () {
    $('#datetimepicker-two').datetimepicker({
        language:'zh-CN',
        autoclose: true
    });
    var orgOption = {
        //stree的id号(（同一个页面，多个stree,必须指定不同的id）)
        streeId:"streeId1",
        //tree的配置选项（里面参数参考ztree)
        treeSettings : {
            check:{
                chkboxType:{"Y":"s","N":"s"},
                chkStyle:"checkbox",
                enable:true
            },
            async : {
                url : "",
                dataType : "json",
                enable : true,
                autoParam : ["id","type"],
                dataFilter :function (treeId, parentNode, responseData) {
                    return responseData.result;
                }
            },
            callback : {
                onClick : function( e, treeId, treeNode){
                    orgtree.onClicks(e, treeId, treeNode, function () {
                    })
                },
                onCheck:function( e, treeId, treeNode) {
                    orgtree.onChecks(e, treeId, treeNode, function () {
                    })
                }
            }
        }
    };
    var data=[{name:"湖北",id:"ww",
        children:[
            {id:"22",name:"武汉",
                children:[
                    {id:221,name:"青山",checked:true},
                    {id:"222",name:"汉中",checked:true}
                ]
            },
            {id:"333",name:"宜昌",
                children:[
                    {id:222,name:"宜兴",checked:true},
                    {id:"334",name:"大新",checked:true}]}]
    }
    ];
    var orgtree= new Stree(orgOption,data);

    $ ( '#aps-add' ).on ( 'click', function ( e ) {
        layer.open ( {
            type : 1, title : '新增计划配置', area : '566px', content : $ ( '#modal-edit' ),
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
                                errmsg ( "新增计划配置成功", 4000 );
                                search ();
                            } else {
                                layer.alert ( "新增计划配置失败：原因是" + result.message );
                            }
                        } );
                }
            }, btn2 : function ( index ) {
                layer.close ( index );
            }
        } )
    } );

})