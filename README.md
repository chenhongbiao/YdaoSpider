# YdaoSpider 有道云读书共享笔记 爬虫
Scraping Youdao Note - Public shared notes

##抓取网站页面样例

- 网站主页 [http://note.youdao.com/dushu/web/index.html]
- 笔记文件夹页面 [http://note.youdao.com/share/?id=81c26805eb409c777f75ab97ad5335f8&type=notebook]
- 笔记页面 [http://note.youdao.com/share/?id=81c26805eb409c777f75ab97ad5335f8&type=notebook#/WEBe016b328c746a17506221e33260a36ac]
- 笔记页面 [http://note.youdao.com/share/?id=1fd4202c537d210098dcf5be064e8574&type=note ]

##项目文件说明

- getBnoteLinks: 在主页页面上，获取所有的笔记或笔记本链接；
- HomePageGo：   在主页页面上，翻页到下一页 ；（模拟浏览器实现）
- getNoteLinks： 在笔记本页面上，获取所有的笔记链接；（正则表达式实现（弃坑），格式化为JSON分析实现）
- oneReadNote：  在笔记页面上，获取笔记分享人的名字，头像，笔记标题和内容，阅读量，点赞数，更新时间；
- **allReadNote**：  在主页页面开始，获取所有的笔记链接和笔记（集成上述模块实现）。

##程序开发环境：

>IDE: Visual Studio 2015;

##程序运行环境：
1. Python 3.5.2；
2. Beautiful Soup 4；
3. Selenium + PhantomJS； （模拟浏览器动态操作）

>//注意：修改程序里你的 PhantomJS 或者其他浏览器的路径！！！

4. mysql 5.7；
5. pymysql；（操作数据库）

>//注意：在运行程序之前，请按照allReadNote文件夹下的init_database.sql文件创建相应的数据库

>//注意：修改程序里你的 mysql 用户名和密码！！！
