## 产品简介
​		本产品是一个关于国家标准数据库的数据展示系统，可以展示紧固件 弹簧 联轴器 轴承等器件的国家标准参数图片等信息。供生产方参考
​    

## 开发环境

+ 操作系统：Windows
+ 编译器：Pycharm + Nginx
+ 编程语言：Python 3.7 + Vue.js 


## 运行环境

+ 操作系统： CentOS 7
+ 辅助工具：Python 3.7解释器 + Nginx


## 安装说明

1. 安装Python 3.7环境  
2. 从 github 中用 git clone 命令下载项目到服务器目录 /root  
3. 进入 /root/gb  
4. 执行 python install -r requirements.txt  
5. 执行 nohup python3 run.py > out.file 2>1 &  
   **后台到此部署完成**  

6. 安装nginx环境  
7. 从github用 git clone 命令下载项目到nginx规定的 www 目录下  
   **前台部署完毕**   

8. 上传数据 将中机数据文件夹放入和run.py 同级的目录。/root/gb/中级数据  
   **部署完毕**  
   
   
## 注意事项

1. 数据目录结构一共三层，第一层目录名叫中机数据 第二层目录有四个子目录，分别为紧固件、联轴器、弹簧和联轴器。 对于这四个目录的任意目录是具体每个器件的标准，目录名为器件名。


## 设计思路