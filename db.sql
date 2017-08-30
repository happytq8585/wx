create table if not exists wxuser
(
 id int unsigned primary key auto_increment,
 real_name varchar(64) not null,/*真实姓名必填*/
 nick_name varchar(64) not null,/*昵称必填*/
 real_img_url varchar(128),
 nick_img_url varchar(128),
 office_phone varchar(32),
 mobile_phone varchar(32),/*移动电话,不填就无法预订*/
 password varchar(32) not null, /*密码必填*/
 role int unsigned default 5
 /*0=总管理员  1=食堂管理员 2=会议管理员 3=公告管理员 4=物业管理员 5=普通行员 6=领导*/
) engine=InnoDB, charset=utf8;

insert into wxuser(id, real_name, nick_name, mobile_phone, password, role) values(1, "admin_real", "admin_nick", "13777776666", "123", 0);

/*菜的数据库表*/
create table if not exists dish
(
 id int unsigned primary key auto_increment,
 name varchar(128) not null,           /*菜的名字*/
 pic_loc  varchar(256),                /*菜图片存放的位置*/
 time date not null,                   /*菜的日期 年-月-日*/
 material varchar(128),                /*菜的食材*/
 kind int unsigned default 0,          /*0x0000=可预订 0x0010=早餐 0x0100=午餐 0x1000=晚餐*/
 price int unsigned default 0,         /*菜的单价，分为单位*/
 unit    varchar(8) not null,          /*单位: 斤 个 只 头 打*/
 score int unsigned default 0,         /*菜的总分*/
 num   int unsigned default 0          /*评分次数*/
) engine=InnoDB, charset=utf8;


/*订单信息*/
create table if not exists order_info
(
 id int unsigned primary key auto_increment,
 user_id int unsigned not null, /*用户id*/
 dish_id int unsigned not null, /*菜名id*/
 num     int unsigned not null, /*数量*/
 price   int unsigned not null, /*单价, 单位分*/
 unit    varchar(8) not null, /*单位: 斤 个 只 头 打*/
 time timestamp default CURRENT_TIMESTAMP,    /*下单的时间*/
 time1 timestamp default CURRENT_TIMESTAMP,   /*预计取食品的时间*/
 time2 timestamp default CURRENT_TIMESTAMP,   /*实际取食品的时间*/
 remove int unsigned default 0,/*0=没有删除 1=删除*/
 pay_staus int unsigned default 0 /*支付状态 0=未支付 1=支付*/
) engine=InnoDB, charset=utf8;

/*菜的评论*/
create table if not exists dish_comment
(
 id int unsigned primary key auto_increment,
 dish_id int unsigned not null,                /*菜的id*/
 user_id int unsigned not null,                /*用户的id*/
 real_name varchar(64),
 nick_name varchar(64),
 real_img_url   varchar(128),
 nick_img_url   varchar(128),
 stars  int unsigned default 1,                /*用户对该菜评价了几颗星*/
 time timestamp default CURRENT_TIMESTAMP,     /*评论的时间*/
 content varchar(512)                          /*评价的内容*/
) engine=InnoDB, charset=utf8;

DELIMITER $
create trigger dish_trigger after insert
on dish_comment for each row 
update
    `dish`
set
    `score` = `score` + new.stars,
    `num`   = `num` + 1
where
    `id` = new.dish_id;
$
DELIMITER ';'
