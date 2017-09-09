var path = $('#path').val();
function OrgEdit(id){
    layer.open({
        type: 1,
        title: '修改',
        area: '566px',
        content: $('#modal-edit'),
        success: function (dom, index) {
            $.post(path +'/orglinkinfo/get.json', {
                id: id
            }, function (result) {
                if (result['success']) {
                    var data = result['result'];
                    $('#childOrg-edit').find('input').each(function (index, input) {
                        $(input).val(data[$(input).attr('name')]);
                    });
                    $('#childOrg-edit').find('select').each(function (index, select) {
                        $(select).val(data[$(select).attr('name')]);
                    });
                }
            })
        },
        btn: ['确认', '取消'],
        yes: function (index) {
            $.post(path + '/orglinkinfo/update.json', $('#childOrg-edit').serialize(), function (result) {
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
}
function OrgDelete(id) {
    layer.alert('确定删除吗?', {
        icon: 2, btn: ['确认', '取消'], yes: function (index) {
            $.post(path + '/orglinkinfo/delete.json', {
                id:id
            }, function (result) {
                if (result['success']) {
                    layer.close(index);
                    $('#data-query').click();
                }
            });
        }
    });
}

$(function () {

    //右侧扩展到底部
    var wHeight = $(window).innerHeight();
    console.log('wHeight:'+wHeight);
    $('.menu_table').css({
        height:wHeight-169
    })

    $(window).on('scroll',function () {
        navFixed();
    })

    //导航栏悬浮
    $(document).on('scroll', function () {
        navwith = $('.right_table').width();
        navFixed();

    })



    var orgOption = {
        hideId: "organizationId", showId: "orgName", treeSettings: {
            async: {
                enable: true,
                url: path + "/orglinkinfo/treebyid.json",
                autoParam: ["id"],
                dataFilter: function (treeId, parentNode, responseData) {
                    return responseData.result;
                }
            }, view: {
                showLine: true,
                dblClickExpand: true,
                selectedMulti: false
            }, data: {
                key: {
                    name: "name", //设置树节点的name，节点参数name必须和它匹配
                    children: "chlidren",
                    url: null //设置ztree点击节点不进行url跳转
                }, simpleData: {
                    enable: true, //开启树的层级结构
                    idKey: "id", //设置树节点id，节点参数id必须与之匹配
                    pIdKey: "parentId" //设置pid，节电参数pid必须与之匹配
                }
            },
        }
    };
    var orgtree = new Stree(orgOption);


    /**
     * 菜单树展示部分
     */
    var menuTree = {};
    //菜单树的设定
    var menuOption = {
        async: {
            enable: true,
            url: path + "/orglinkinfo/treeview.json",
            autoParam: ["id"],
            dataFilter: function (treeId, parentNode, responseData) {
                return responseData.result;
            }
        }, view: {
            showLine: true,
            dblClickExpand: true,
            selectedMulti: false
        }, data: {
            key: {
                name: "name", //设置树节点的name，节点参数name必须和它匹配
                children: "children",
                url: null //设置ztree点击节点不进行url跳转
            }, simpleData: {
                enable: true, //开启树的层级结构
                idKey: "id", //设置树节点id，节点参数id必须与之匹配
                pIdKey: "parentId" //设置pid，节电参数pid必须与之匹配
            }
        }, callback: {
            onClick: function (event, treeId, treeNode) {
                currSelectNode = treeNode;
                $.ajax({
                    url: path + "/orglinkinfo/getchild.json",
                    data: {
                        "id":treeNode.id
                    },
                    type: "post",
                    async: true,
                    success: function (data) {
                        $("#tbody").html("");
                        var results=data.result;
                        var childOrgHtml;
                        for(var i=0;i<results.length;i++){
                            var childOrg=results[i];
                            childOrgHtml+="<tr data-id="+childOrg.organizationId+">"+
                                "<td>"+childOrg.orgName+"</td>"+
                                "<td>"+childOrg.orgCode+"</td>"+
                                "<td>"+childOrg.orgType+"</td>"+
                                "<td>"+childOrg.orgLevel+"</td>"+
                                "<td>"+childOrg.orgAddress+"</td>"+
                                "<td>"+
                                "<a href='javascript:OrgEdit(\"" + childOrg.organizationId + "\");'>编辑</a>&nbsp;" +
                                "<a href='javascript:OrgDelete(\"" + childOrg.organizationId + "\");'>删除</a>&nbsp;" +
                                "<a href='javascript:OrgAuthority(\"" + childOrg.organizationId + "\");'>权限配置</a>&nbsp;" +
                                "<a href='javascript:OrgShare(\"" + childOrg.organizationId + "\");'>分润比例</a>&nbsp;" +
                                "</td>"+
                                "</tr>";

                        }
                        $("#tbody").html(childOrgHtml);

                    }, error: function (data) {
                        showMsg("新增" + menuname + "失败，通讯异常！" + data.statusText);
                    }
                });
            },
            onRightClick: function (event, treeId, treeNode) {
                /* alert("右键菜单展示!");*/
            },
            onAsyncSuccess:afterNodesRefresh
        }
    };

    menuTree = $.fn.zTree.init($("#ztree"), menuOption);

    /*保存刷新前的选中节点*/
    var selectnode=null;
    /*刷新左侧菜单树数据 在：编辑-更新、新增、启用/禁用 操作后，必须同步刷新*/
    function refreshNodes() {
        var treeNode=menuTree.getSelectedNodes();
        if(treeNode.length>0) {
            selectnode = treeNode[0];
        }
        menuTree.reAsyncChildNodes(null,"refresh",false);
        /* PS：局部刷新不启用：因后台暂无合适接口
         menuTree.reAsyncChildNodes(selectnode,"refresh",false);
         */
    }
    function afterNodesRefresh(event,treeId,treeNode,msg) {
        var flag=true;
        var nodes;
        if(selectnode) {
            /*如果选中的节点依然存在*/
            nodes = menuTree.getNodeByParam("id", selectnode.id);
            if(nodes) {
                flag=false;
            }else{
                /*如果选中的节点刷新后不存在了*/
                nodes = menuTree.getNodeByParam("id", selectnode.parentId);
                flag=!nodes;
            }
        }
        /*如果没有选中的节点*/
        if(flag){
            nodes=menuTree.getNodes()[0];
        }
        /*初始化左侧选中节点，并重新渲染右侧页面列表*/
        menuTree.selectNode(nodes);
        selectnode=null;
    }
    /**
     * 搜索/展开/收缩 左侧菜单树
     * */
    /*搜索树*/
    $("#left-search").click(function (){
        searchNode("name",$("#menu-search"), menuTree);
    });
    /*收缩树结构*/
    $("#left-combine").click(function (eve) {
        menuTree.expandAll ( false );
    });
    /*展开树结构*/
    $("#left-spread").click(function (eve) {
        menuTree.expandAll ( true );
    });
    /*查找节点*/
    function searchNode( name ,_$input, treeObj ) {
        var value=_$input.val();
        var contextNodes = treeObj.transformToArray( treeObj.getNodes () );
        if ( ! value || value==="请输入关键字" || value.trim()==="" ) {
            _$input.val("");
            treeObj.showNodes ( contextNodes );
            return;
        }
        treeObj.hideNodes ( contextNodes );
        var nodes = treeObj.getNodesByParamFuzzy ( name, value, null );
        /*递归父节点*/
        for ( var i = 0, l = nodes.length; i < l; i ++ ) {
            getParents ( nodes[ i ], nodes );
        }
        treeObj.showNodes ( nodes );
        treeObj.expandAll ( true );
    }
    /*获取父节点*/
    function getParents( nd, nodeList ) {
        if ( nd ) {
            var ndp = nd.getParentNode ();
            if ( ndp ) {
                if ( nodeList.indexOf ( ndp ) === - 1 ) {
                    nodeList.push ( ndp );
                }
                getParents ( ndp, nodeList );
            }
        }
    }
    /**
     * 按钮 隐藏左侧菜单
     * */
    $(document).on('click', '#fold-btn', foldAside);
    // 收缩侧边栏方法
    var toggle = true;
    function foldAside() {
        var root = $(this).parents('.wlk-grail');
        if (toggle) {
            $(this).html('<i class="iconfont icon-rtarrow"></i>');
            root.animate({
                'padding-left': '30px'
            })
        } else {
            $(this).html('<i class="iconfont icon-lfarrow"></i>');
            root.animate({
                'padding-left': '230px'
            })
        }
        toggle = !toggle;
    };
    function navFixed() {
        var scrollTop = $(window).scrollTop();
        console.log('scrolltop:' + scrollTop);
        console.log('widthz;' + navwith);
        if (scrollTop >= 100) {
            $('.query-operation').css({
                position: 'fixed',
                top: '0',
                width: navwith,
            });

            $('.views-nav').css({
                position: 'fixed',
                top: '0'
            });
        } else if (scrollTop >0 && scrollTop < 100 ) {
            $('.query-operation').css({
                position: 'fixed',
                top: 100-scrollTop,
                width: navwith
            });

            $('.views-nav').css({
                position: 'fixed',
                top: 100-scrollTop
            });
        } else {
            $('.query-operation').css({
                position: '',
                top: '',
                width: navwith
            });
            $('.views-nav').css({
                position: '',
                top: ''
            });

        }

    }
    //当前选中的节点
    var currSelectNode = {};




    /** 新增弹出框 */
    $('#data-add').on('click', function (e) {
        layer.open({
            type: 1,
            title: '增加',
            area: '566px',
            content: $('#modal-edit'),
            success: function (dom, index) {
                $('#childOrg-edit').find('input').each(function (index, input) {
                    $(input).val('');
                });
            },
            btn: ['确认', '取消'],
            yes: function (index) {
                $.post(path + '/orglinkinfo/add.json', $('#childOrg-edit').serialize(), function (result) {
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


    /*设置错误提示信息自动消失方法*/
    function errmsg(content, delay) {
        $('.error-msg.alert').addClass('show');
        $('.error-msg strong').text(content);
        setTimeout(function () {
            $('.error-msg.alert').removeClass('show');
            $('.error-msg.alert').alert();
        }, delay)

    }


});
