$(function () {

	var dropSwitch = false;
	$('.system').on('click', function () {
		if(dropSwitch){	// 收缩
			$('.second-level-menu').slideUp('fast', function () {
				$('.menu-second').hide();
				dropSwitch = false;
			});
		}else { // 展开
			$('.second-level-menu').show();
			$('.menu-second').slideDown('fast', function () {
				dropSwitch = true;
			})
		}
	});



	// $(window).on('scroll', function () {
	// 	$('.quickstart_size').slideUp('fast', function () {
	// 		$('#navdrop-menu').hide();
	// 		dropSwitch = false;
	// 	});
	// });


	menuStart();
	/*请求菜单数据*/
	function menuStart() {
		var menus;
		$.ajax({
			url: contextPath+"/menu/getchilds.json",
			dataType: "json",
			async: false,
			data: {"menuCode": "crm.menu"},
			type: "POST",
			success: function (data) {
				if (data.success) {
					menushtml(data);
				} else {
					showMsgCommon("后台错误无法加载菜单项！");
				}
			},
			error: function (xhr,textStatue,errorThrown) {
				showMsgCommon("系统错误无法加载菜单项！");
			}
		});

	}

	function menushtml(menus){
		var tpl = [
			"{@each result as it}",
			"{@if it.isEnable }",
			"<li class='list-group-item q_item \${it.menuCode}'>",
			"{@if !it.isParent}",
			"<a  class='q_link' href='","{@if !it.menuAction}","#","{@else}",contextPath,"\${it.menuAction}","{@/if}","'>\${it.menuName}</a>",
			"{@else}",
			"<a  class='q_link'><div><img src='src/assets/images/\${it.menuCode}.png' alt=''/></div><div>\${it.menuName}</div></a>",
			"{@/if}",
			"<div class=\"second-level-menu\">",
			"<ul class='list-group menu-second'>",
			"{@each it.childMenuVos as item}",
			"{@if item.isEnable}",
			"<li class='list-group-item'>",
			"<a class='item_link' href='","{@if !item.menuAction}","#","{@else}",contextPath,"\${item.menuAction}","{@/if}","'>\${item.menuName}</a>",
			"</li>",
			"{@/if}",
			"{@/each}",
			"</ul>",
			"</div>",
			"</div>",
			"{@/if}",
			"{@/each}"].join("");
		var menushtml = juicer(tpl, menus);
		$(".quickstart_size").append(menushtml);
	}

	/*生成并填充菜单html片段*/
	// function menushtml(menus){
	// 	var tpl = [
	// 		"{@each result as it}",
	// 		"{@if it.isEnable }",
	// 		"<li class='list-group-item q_item \${it.menuCode}'>",
	// 		"{@if !it.isParent}",
	// 		"<a  class='q_link' href='","{@if !it.menuAction}","#","{@else}",contextPath,"\${it.menuAction}","{@/if}","'>\${it.menuName}</a>",
	// 		"{@else}",
	// 		"<a>\${it.menuName}<img src='src/assets/images/\${it.menuCode}.png' alt=''/></a>",
	// 		"{@/if}",
	// 		"<div class=\"second-level-menu\">",
	// 			"<ul class='list-group menu-second'>",
	// 			"{@each it.childMenuVos as item}",
	// 				"{@if item.isEnable}",
	// 				"<li class='list-group-item'>",
	// 					"<a href='","{@if !item.menuAction}","#","{@else}",contextPath,"\${item.menuAction}","{@/if}","'>\${item.menuName}</a>",
	// 				"</li>",
	// 				"{@/if}",
	// 			"{@/each}",
	// 			"</ul>",
	// 		"</div>",
	// 		"</div>",
	// 		"{@/if}",
	// 		"{@/each}"].join("");
	// 	var menushtml = juicer(tpl, menus);
	// 	$(".quickstart_size").append(menushtml);
	// }

	// 用户信息显示
	$('#my-account-btn').on('click',function () {
		$('.my-account').fadeToggle();
	})
});



