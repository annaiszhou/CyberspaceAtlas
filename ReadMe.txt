Author: Zhou Weiwei,Zhang Jun
Date： 2017/11/20
How to use:
1.	This is a demo for the visualization of cyberspace atlas. Run the CyberspaceAtlas.py, then choose the data source file. There are two processed data source file for demo, which is new_IP_Coordinates.txt and new_IP_Coordinates_2.txt
2.	Open the file. Then the image initialized. Different colors represent different ASN numbers. White color represent that the IP address is not used. (No data at this point). The pixel of initialization image is 255.255.255.255/16, which means the pixel is correct to the top 16 digits of IP address and every pixel is corresponding to 65536 IP addresses (2^(32-16)=65536). And so on, for other pixels.
3.	Click the left button of the mouse on each point of the image. Then the corresponding IP address will be shown in the status bar below that point.
------------------------------------------------------------------------------------------------------------------------------------------
Author: Zhou Weiwei,Zhang Jun
Date： 2017/11/20
简介：
使用：
1. 运行程序，首先会得选择源数据文件，本程序为演示程序，已提供两份演示用的处理过的源数据文件，分别为new_IP_Coordinates.txt和new_IP_Coordinates_2.txt；
2. 打开文件后会得到初始化图像，不同颜色代表不同的ASN（自治域号码），白色代表该点IP未使用（在此处代表该点无数据），初始化图像分辨率为255.255.255.255/16，即分辨率精确到IP的前16位，每一个像素点对应2^(32-16)=65536个IP，其他分辨率如此类推；
3. 鼠标左键单击图像任一点下方状态栏会显示该点对应的IP；
