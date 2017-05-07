## 介绍

AprilBlog2017 顾名思义是我在 17 年 4 月份写的 Django 项目。

16 年 4 月曾参照其它项目写过一个 AprilBlog，初学时对很多模块还不熟悉，对于整个博客站点的思路还不清晰。

时隔一年，“Django By Example”一书使我对 Django 有了更全面的了解。

博客的数据流模型非常简单，大多数时间是花在前端上的。



## 特点

这个简单的项目最有价值的地方在于以下流程： Markdown 文本 render 成代码高亮的页面。

鉴于习惯了静态网站生成器，我并不是在 admin 页面编辑文本，而是用户上传 markdown 格式文件，后端用 `markdown2` 渲染成带 css 的 html。

文章内容只来源于该 markdown 文件，便于文章的备份与迁移。

## 目标

多写 Blog，记录生活、技术，见证自己的成长。