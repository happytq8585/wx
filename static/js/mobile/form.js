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


$("#file-0").fileinput({
    'allowedFileExtensions' : ['jpg', 'png','gif'],
});

var kind = 0;
$("input[type='radio']").click(function(){
        var radios = document.getElementsByName('style');
        for (var i = 0, length = radios.length; i < length; i++) {
            if (radios[i].checked) {
                kind = radios[i].value;
                break;
        }
    }

})

/*
提交方式*/

//菜谱上传js
$(function () {
    $('#data-query').on('click',function () {
        var name     = $('#add-name').val(); //dish name
        if (name == null || name.length == 0) {
            alert('没有正确填写菜名');
            return -1;
        }
        var style    = $('#add-style').val();//dish material
        if (style == null || style.length == 0) {
            alert('没有正确填写食材/口味');
            return -1;
        }
        var unit     =$('#add-unit').val();  //dish unit

        var price    = $('#add-price').val();//dish price
        price    = parseInt(price);

        //var kind     = $('input[name="style"]').val();//0=reserved 16=breakfast 256=lunch 4096=dinner
        kind     = parseInt(kind);

        if (price == null || price.length == 0 || parseInt(price) == 0) {
            if (kind != 256) {
                alert("价格不正确: 1元应该填写100, 这里单位为分");
                return -1;
            }
        }
        var tk  = location.href.split('?')[1];
        if (tk == null) {
            alert("没有时间");
            return -1;
        }
        var day = tk.split('=')[1];
        if (day == null) {
            alert("没有时间");
            return -1;
        }
        var xsrf = get_cookie_by_name('_xsrf');
        var formdata = new FormData($('#form_img')[0]);
        formdata.append('name', name);
        formdata.append('material', style);
        formdata.append('unit', unit);
        formdata.append('price', price);
        formdata.append('kind', kind);
        formdata.append('day', day);
        formdata.append('_xsrf', xsrf);
        $.ajax({
            type: "POST",
            Cookie: document.cookie,
            url: "/up",
            data: formdata,
            contentType: false,
            processData: false,
            data: formdata,
            success: function (result) {
                alert('上传成功');
            },
            error: function (data) {
            }
        });
    })
})

