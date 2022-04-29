![](https://github.com/coder-yuzhiwei/iechub/blob/main/source/banner.jpg)

## 相关资料

### 知识图谱 ###

[相关概念介绍](https://zhuanlan.zhihu.com/p/441108118)

[基础知识学习视频](https://www.bilibili.com/video/BV17s411n75M?p=1)



## 知识图谱的构建和可视化展示系统

### 版本依赖

```
paddle 1.5
python 3.6.5
```

### 快速部署

1. 按照[使用手册](user_guide.docx)配置软件环境
2. 软件执行

```
启动conda服务
conda activate 709
启动uwsgi服务
uwsgi -x demo.xml
启动nginx服务
sudo /user/local/nginx/sbin/nginx
打开浏览器，输入前面配置的ip地址（默认为127.0.0.1）
```

