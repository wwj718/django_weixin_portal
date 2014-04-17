##django_weixin_portal
一直打算自己写一个第三方微信管理平台,恰好看到这个项目，用的又是我所熟悉的django,于是决定以它为基础做进一步的开发。

该项目最初是由 亿米CH 开源的`开源的第三方微信开发者账号管理平台`,开源协议为BSD

将其放到github里,对项目做了一些修改，欢迎有兴趣的同学们来fork，一起为这个项目贡献代码。


###基础服务：
*自动回复
*图文编辑
*无匹配回复
*自定义菜单
*以及扩展功能：

###微信的图文列表
*分类以及微网站服务
*活动管理
*预约开户（基金行业）
*申请模拟账号
*在线咨询

###亿米CH开源的代码包括：

*Python的所有业务逻辑
*前端的呈现代码（响应式设计和移动端自适应的代码）
*所有依赖的代码库和应用的第三方代码（如：ueditor等）

###开通账号流程
1.admin后台开通账号，并新建app_item，并绑定
2.客户账号登陆http://mp.weixin.qq.com/,填写url (token,app_item.id)，token验证得到appid, app_secrect, 填入app_item中

###运行项目

*  `pip install -r requlirements.txt`
*  后台帐号:admin . 密码：admin

