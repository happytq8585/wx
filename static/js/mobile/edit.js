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

$('#file-0a').click(function() {
    $('#img_original').hide();
});

$('#data-edit').click(function() {
        var kind = 0;
        var radios = document.getElementsByName('style');
        for (var i = 0, length = radios.length; i < length; i++) {
            if (radios[i].checked) {
                kind = radios[i].value;
                break;
            }
        }

        var name     = $('#edit-name').val(); //dish name
        if (name == null || name.length == 0) {
            alert('没有正确填写菜名');
            return -1;
        }
        var style    = $('#edit-style').val();//dish material
        if (style == null || style.length == 0) {
            alert('没有正确填写食材/口味');
            return -1;
        }
        var unit     =$('#edit-unit').val();  //dish unit

        var price    = $('#edit-price').val();//dish price
        price    = parseInt(price);

        //var kind     = $('input[name="style"]').val();//0=reserved 16=breakfast 256=lunch 4096=dinner
        kind     = parseInt(kind);

        if (price == null || price.length == 0 || parseInt(price) == 0) {
            if (kind != 256) {
                alert("价格不正确: 1元应该填写100, 这里单位为分");
                return -1;
            }
        }
        var old_img = $('#img_original').attr('src');
        var day = $('#form_img').attr('date');
        if (day == null) {
            alert("没有时间");
            return -1;
        }
        var new_img = $('.file-preview-frame').find('img').attr('src');
        if (new_img != null) {
            old_img = ''
        }
        var did = $('#data-edit').attr('dish');
        var xsrf = get_cookie_by_name('_xsrf');
        var formdata = new FormData($('#form_img')[0]);
        formdata.append('name', name);
        formdata.append('material', style);
        formdata.append('unit', unit);
        formdata.append('price', price);
        formdata.append('kind', kind);
        formdata.append('day', day);
        formdata.append('_xsrf', xsrf);
        formdata.append('old_img', old_img);
        formdata.append('did', did);
        $.ajax({
            type: "POST",
            Cookie: document.cookie,
            url: "/edit",
            data: formdata,
            contentType: false,
            processData: false,
            data: formdata,
            success: function (result) {
                alert('编辑成功');
            },
            error: function (data) {
            }
        });
});
