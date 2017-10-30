
function get_cookie_by_name(name)
{
    var start = document.cookie.indexOf(name);
    if (start != -1) {
        var res = "";
        var end  = document.cookie.indexOf(";", start+1);
        if (end == -1) {
            res = document.cookie.substring(start+name.length+1);
        } else {
            res = document.cookie.substring(start+name.length+1, end);
        }
        return res;
    }
    return "";
}
$('#confirm').click(function() {
        var src = $('input[name="src_day"]').val();
        var des = $('input[name="des_day"]').val();
        if (src == "") {
            alert("请选择要拷贝的周当中的某一天")
            return -1;
        }
        if (des == "") {
            alert("请选择要拷贝到具体某一周当中的任意一天")
            return -1;
        }
        if (src >= des) {
            alert("'源'里边的日期必须在'目的'里边日期前边");
            return -1;
        }
        var xsrf = get_cookie_by_name('_xsrf');
        $.ajax({
            url: '/copy_menu',
            type: 'POST',
            data: {'_xsrf':xsrf, 'src':src, 'des':des},
            success: function(e) {
                if (e == '0') {
                    alert('拷贝成功');
                    return -1;
                } else {
                    alert('目的周有数据或者源和目的在同一周是不能拷贝的');
                    return -1;
                }
            },
            error: function(e) {
                alert('系统错误');
            }
        });
});
