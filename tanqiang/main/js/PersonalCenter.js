$(function () {
    $('.SurePassword').click('on',function () {
        $('.PersonalCenterBox').find('input').not('.SurePassword').map(function (index,data) {
            // console.log($(data).val(),index); 
            // $(data).val()  三次输入密码的数值   按顺序
        })
    })
    $('#upCenter').click('on',function () {
        $('.PersonalCenterBox').css({display:'block'});
        $('.uplistBox').css({display:'none'});
    })
})
function showPreview(source) {
    var file = source.files[0];
    if(window.FileReader) {
        var fr = new FileReader();
        fr.onloadend = function(e) {
            document.getElementById("portrait").src = e.target.result;
        };
        fr.readAsDataURL(file);
    }
}
function editCenter(){
    $('.PersonalCenterBox').css({display:'none'});
    $('.uplistBox').css({display:'block'});
}