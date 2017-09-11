create table if not exists wxuser
(
 id int unsigned primary key auto_increment,
 name varchar(64) not null,  /*企业微信号的name*/
 mobile varchar(32),         /*移动电话,不填就无法预订*/
 gender varchar(2) not null, /*性别0=female 1=male*/
 userid varchar(64) not null,/*企业微信号的userid*/
 telephone varchar(16),      /*座机*/
 avatar varchar(256)         /*头像url*/
) engine=InnoDB, charset=utf8;


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
 mobile int unsigned not null, /*用户mobile phone*/
 dish_id int unsigned not null, /*菜名id*/
 num     int unsigned not null, /*数量*/
 price   int unsigned not null, /*单价, 单位分*/
 unit    varchar(8) not null, /*单位: 斤 个 只 头 打*/
 time timestamp default CURRENT_TIMESTAMP,    /*下单的时间*/
 time1 timestamp,   /*预计取食品的时间*/
 time2 timestamp,   /*实际取食品的时间*/
 confirm int unsigned default 0,/*0=没有领取 1=已领取*/
 pay_status int unsigned default 0 /*支付状态 0=未支付 1=支付*/
) engine=InnoDB, charset=utf8;

/*菜的评论*/
create table if not exists dish_comment
(
 id int unsigned primary key auto_increment,
 dish_id int unsigned not null,                /*菜的id*/
 mobile varchar(16) not null,                  /*用户的mobile phone*/
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
