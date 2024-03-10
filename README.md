# usb_tvp5150
使用 tvp5150 采集CVBS的视频， 传输给cpld，再传输给cy7c68013, 电脑上用python进行采集

capture_app ----- python脚本（需要安装pyusb和cv2）

dirver -------- 驱动， libusb方案

firmware ------ 68013的keil代码

hdl  ------- cpld代码

pcb ------ CPLD板子原理图（TVP5150是另外模块）



采集命令

python  usbvideo.py new0.bin

python -u yuv422_display.py 722 570  new0.bin



采集的效果如图：

![](https://github.com/11tools/usb_tvp5150/blob/main/full.png?raw=true)

