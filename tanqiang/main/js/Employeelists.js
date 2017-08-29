
    var delnum ;
    //删除表格数据 可将x改为删除时所需要的数据
    function ondelete(obj,x){
        console.log(obj,x);
        delnum = x;
        $('.Sure').css({display:'block'});
        $.ajax({
            
        });
    }
    //取消删除
    function surecancel(){
        $('.Sure').css({display:'none'});
    }
    function suredelete(){
        surecancel();
        //delnum为要删除的数据
        $.ajax({
            
        })
    }
    function closeedit(){
        $('.Edituser').css({display:'none'});
    }
    function openedit(){
        $('.Edituser').css({display:'block'});
        
    }


