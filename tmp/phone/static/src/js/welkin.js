jQuery.fn.extend({
    ContainerHeight:function(){
        var screenHeight = $(window).height();
        var headHeight = $('.header').height();
        var navTabsHeight = $('.wlk-container .nav-tabs').height();
        $("#grail-content .tab-content").css({
              'min-height':(screenHeight-headHeight-navTabsHeight-32)*1.5+'px'
         })
    }
});