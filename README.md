# Memory image auto-analyzer
## 一个雏形，一个基于Volatility进行可视化、自动化内存镜像分析的工具

目前面对Windows平台的内存数据，后端基于Volatility2

后端Volatiliy2，基于在环境中已经安装的Volatility2（即直接运行vol.py）

## TODO - 项目规划-windows
- 建立一键分析，包括imageinfo，pslist，pstree，filescan（加入常见目录筛选），ishistory和cmdscan
- pslist和pstree整合进树状组件，支持选中进程进行dump（memdump和procdump）
- 加入网络分析，包含netscan
- 加入环境信息分析，包含注册表printkey，环境变量envars
- 加入凭据分析，包含lsadump，hashdump和mimikatz（需要处理crypto库）
- filescan加入常见结果筛选，加入正则搜索，加入提取功能
- 加入常见信息提取，如剪贴板，桌面截图

## 正则示例
```shell
vol.py -f GULF-PC-20220321-064240.raw --profile=Win7SP1x64 filescan | grep -iE "flag|.zip$|.rar$|.7z$|.txt$|.png$|.jpg$|.gif$|.pdf$|.doc$|.docx$|.pcap$|.pcapng$|.raw$|.kdbx$|Desktop\\\{1}.+"
```