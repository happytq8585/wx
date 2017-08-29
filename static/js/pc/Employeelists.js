function reload(loc) {
    var host = window.location.host
    window.location.href = 'http://' + host + loc;
}
function get_cookie_by_name(name)
{
    var start = document.cookie.indexOf(name);
    if (start != -1) {
        var res = '';
        var end  = document.cookie.indexOf(';', start+1);
        if (end == -1) {
            res = document.cookie.substring(start+name.length+1);
        } else {
            res = document.cookie.substring(start+name.length+1, end);
        }
        return res;
    }
    return '';
}
    var delnum ;
    //删除表格数据 可将x改为删除时所需要的数据
    function ondelete(obj,x){
        console.log(obj,x);
        delnum = x;
        $('.Sure').css({display:'block'});
    }
    //取消删除
    function surecancel(){
        $('.Sure').css({display:'none'});
    }
    function suredelete(){
        surecancel();
        //delnum为要删除的数据
        var xsrf = get_cookie_by_name('_xsrf');
        $.ajax({
            url:'/personal',
            type:'POST',
            data:{'action':'delete', 'user_id':delnum, '_xsrf': xsrf},
            success: function(para){
                alert(para);
                reload('/personal?action=management');
            },
            error: function(para) {
                alert('删除失败');
            }
        });
    }
    function closeedit(){
        $('.Edituser').css({display:'none'});
    }
    function openedit(obj, id){
        $('.Edituser').css({display:'block'});
        $('input[name="user_id"]').val(id); 
        var xsrf = get_cookie_by_name('_xsrf');
        $('input[name="_xsrf"]').val(xsrf);
    }


