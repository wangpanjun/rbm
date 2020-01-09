## 基于Flask的 Redis 可视化管理应用


本项目是基于Flask的Redis可视化管理项目，开发此项目主要是因为目前市场上的可视化软件都是收费的，
所以开发了这一款B端的Redis可视化管理应用。欢迎clone和commit～

>目前此应用只提供基础数据的展示功能。


## 本地运行

1.克隆代码

```
git clone https://github.com/wangpanjun/rbm.git
```

2.安装依赖库(建议使用虚拟沙盒)

```
pip install -r requirements.txt
```

3.运行

```
python run.py
```

## docker 运行

1.拉取镜像

```
docker pull wangpanjun/rbm:latest
```

2 运行容器

```
docker run -d -p 0.0.0.0:5000:5000 wangpanjun/rbm:latest
```

## 使用建议
本地环境运行使用虚拟沙盒
 - virtualenv rbm -p python3
 - source rbm/bin/activate
 - python run.py
