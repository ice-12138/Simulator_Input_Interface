# Simulator_Input_Interface

.ui文件——>.py文件
pyuic5 -o XX.py XX.ui

- 上传新添加文件文件 [ADD] + detail 
- 修改已有功能 [CHG] + detail 
- 删除功能或者文件 [DEL] + detail

运行main.py文件启动


打包代码：
- cd到所需打包程序的文件夹
- pyinstaller -F -w demo.py

每次上传前运行delCache.py文件删除所有python运行缓存