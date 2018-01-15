use test;
/* 创建数据表*/
create table azvtes (`dp` varchar(10),`times` date,`ASIN` varchar(10),`SKU`varchar(255),`country` varchar(5),`Sessions` int,`Sessions_Percentage` float,`Page_Views` int,`PV_Percentage` float,`BuyBox_Percentage` float,`Unit` int,`Sales` float,	`Orders` int);

/* 创建店铺产品信息*/
create table cpinfo (`dp` varchar(10),`dpsku` varchar(255),`ASIN` varchar(10),`cp_state` varchar(20),`cpsku` varchar(255),`onelm` varchar(255),`towlm` varchar(255),`threelm` varchar(255) ,primary key(`dp`,`dpsku`))

/*查询数据店铺-时间-三级类目-销售额（降序）*/
select azvtes.dp,azvtes.times,cpinfo.threelm, azvtes.Sales 
from azvtes,cpinfo 
where azvtes.dp=cpinfo.dp and azvtes.SKU= cpinfo.dpsku 
group by azvtes.times, cpinfo.threelm  order by times,Sales desc;