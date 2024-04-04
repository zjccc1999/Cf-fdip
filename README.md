# 安卓和linux使用教程
 👋👋👋 给CM杨幂点点关注👋👋👋https://github.com/cmliu
 
测速指令后面加了 -dd，需要测速的自己删除
感觉没必要测速，测个延迟就行了，能通就行
1. 下载[GeoLite2-Country](https://github.com/P3TERX/GeoLite.mmdb)
2. 下载[CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest)
3. 运行脚本。

**要安装什么库我忘记了**

### 要查看Linux系统的架构，你可以使用以下命令之一：

- 用 uname 命令：`uname -m`
- 这将显示机器的硬件架构信息，例如 x86_64 表示 64 位架构，i386 表示 32 位架构。
- 然后github [CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest) 去下载对应的版本的测速文件。（我这里的是arm64）

- 装jq，你可以使用以下命令：`pkg install jq`
  这将使用Termux的包管理器pkg来安装jq。安装完成后，你就可以在Termux中使用jq来处理JSON数据了。

- 脚本和测速文件都给满777
- 这个是Termux的根目录，下载后的东西放这里面/data/data/com.termux/files/home/(可能和我的不一样，以你自己的为主，是根目录就行)
- #识别国家地区还是推荐用Python，秒出。用api有点慢。
- GeoLite2-Country和libmaxminddb-tools

方法:把GeoLite2-Country复制到termux根目录/data/data/com.termux/files/home/ ，然后输入`pkg install libmaxminddb-tools`。

#### Termux一键下载运行指令:

- `curl -sSL -o ~/GeoLite2-Country.mmdb https://raw.githubusercontent.com/zjccc1999/Cf-fdip/main/linux/GeoLite2-Country.mmdb && chmod +x ~/GeoLite2-Country.mmdb`

- `curl -sSL -o ~/zjccc.sh https://raw.githubusercontent.com/zjccc1999/Cf-fdip/main/linux/zjccc.sh && chmod +x ~/zjccc.sh && bash ~/zjccc.sh`

- 代理加速Termux一键下载运行指令:

- `curl -sSL -o ~/GeoLite2-Country.mmdb https://mirror.ghproxy.com/https://raw.githubusercontent.com/zjccc1999/Cf-fdip/main/linux/GeoLite2-Country.mmdb && chmod +x ~/GeoLite2-Country.mmdb`

- `curl -sSL -o ~/zjccc.sh https://mirror.ghproxy.com/https://raw.githubusercontent.com/zjccc1999/Cf-fdip/main/linux/zjccc.sh && chmod +x ~/zjccc.sh && bash ~/zjccc.sh`

  ### 标准Linux一键下载运行指令:

- `wget https://raw.githubusercontent.com/zjccc1999/Cf-fdip/main/linux/GeoLite2-Country.mmdb -O ~/GeoLite2-Country.mmdb && chmod +x ~/GeoLite2-Country.mmdb`

- `wget https://raw.githubusercontent.com/zjccc1999/Cf-fdip/main/linux/zjccc.sh -O ~/zjccc.sh && chmod +x ~/zjccc.sh && bash ~/zjccc.sh`

- 代理加速标准Linux一键下载运行指令:

- `wget https://mirror.ghproxy.com/https://raw.githubusercontent.com/zjccc1999/Cf-fdip/main/linux/GeoLite2-Country.mmdb -O ~/GeoLite2-Country.mmdb && chmod +x ~/GeoLite2-Country.mmdb`

- `wget https://mirror.ghproxy.com/https://raw.githubusercontent.com/zjccc1999/Cf-fdip/main/linux/zjccc.sh -O ~/zjccc.sh && chmod +x ~/zjccc.sh && bash ~/zjccc.sh`

#### 安卓版叫做Pydroid3:

- https://blog.qaiu.top/archives/pydroid3v70

  [移动云空间网盘分享_Pydroid3v7.0汉化整合版主程序](https://www.ecpan.cn/web/#/yunpanProxy?path=%2F%23%2Fdrive%2Foutside&data=6e482b26b7355ce276ff53e58b77d03aE&isShare=1)

  [移动云空间网盘分享_Pydroid3权限插件](https://www.ecpan.cn/web/#/yunpanProxy?path=%2F%23%2Fdrive%2Foutside&data=e7f868d1d5c5f6661de9f7a0e558c892efCU&isShare=1)

  

- 将2-1py脚本和GeoLite2-Country.mmdb放在/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/目录下

- 在Windows系统下，可以通过安装**Git Bash**执行.sh，就是测速那里需要改一下。CloudflareSpeedTest 要替换


# 电脑版教程
安装Python
要安装os、geoip2、requests、zipfile、socket、re 和 tkinter，运行失败自己去下载库

推荐使用IDLE

右键没有的话使用文件夹中的reg更改注册表

自己右键编辑去替换目录   这是我的目录D:\\PY\\pythonw.exe

4个1开头的是4种获取IP的方法，推荐1-1

剩下的名字都有说明不多解释了。

# https://github.com/P3TERX/GeoLite.mmdb

有时间替换下这个，这个是识别地区用的

# 图片

[文件目录](https://github.com/zjccc1999/Cf-fdip/blob/main/%E5%9B%BE%E7%89%87/%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95.jpg)

[Termux](https://github.com/zjccc1999/Cf-fdip/blob/main/%E5%9B%BE%E7%89%87/Termux.jpg)

[Pydroid 3](https://github.com/zjccc1999/Cf-fdip/blob/main/%E5%9B%BE%E7%89%87/Python.jpg)





