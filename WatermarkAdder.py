#-*- coding: utf-8 -*-
#!/usr/bin/python3
#
#	WatermarkAdder.py
#
#	(C) 2021 非科学の河童, All Rights Reserved
#	This Script Is Following MIT License
#

# 金羿 EillesWan 2022
# 修改代码，使之ok

from PIL import Image, ImageDraw, ImageFont, ImageStat
import signal
import time
#import webp
import base64
import os
import sys
import shutil
import _thread
from pathlib import Path
import re
import random

def sighandler(signum, frame):
	_thread.exit()
	print("EXIT!")
	sys.exit(0)

signal.signal(signal.SIGINT, sighandler)
signal.signal(signal.SIGSEGV,sighandler)

# 源图片目录
source_pic_dir = os.path.join('..','postrc_source','watermark')
# 输出目录
destination_pic_dir = os.path.join('..','images','postrc')
# 站点
Site = 'https://bkryofu.xyz'
# 著作权人
Owner =  u'非科学の河童'

LicenseFollow = "CC BY-NC-SA 4.0"

#####################################################################################

# 宏
Light = 0
Dark = 1
Color = ["#00FFFF", "#0000FF"]

Year = time.strftime('%Y', time.localtime(time.time()))
CopyrightInfo = 'Follow '+ LicenseFollow +' \n© '+ Year + ' ' + Owner + '\nVisit ' + Site

# Creative Commons的图标的Base64，两种配色：#00FFFF与#0000FF，分辨率125x125
CCLOGO = ['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']


def getDireFiles(rsc_dire: str, endswith: str = '') -> list:
	'''返回目录`rsc_dire`中，指定后缀或全部的文件地址。'''
	files = []
	for i in os.listdir(rsc_dire):
		if (endswith and i.endswith(endswith))or(not endswith):
			files.append(os.path.join(rsc_dire,files))
	return files
		
allFonts = getDireFiles(os.path.join(os.path.dirname(__file__),"./font/"))

# 生成水印文字的图案
def text2img(text,font_path:str, font_color="White", font_size=20) -> Image:
	'''将文字`text`以字体`font_path`，颜色`font_color`，大小`font_size`渲染成图片。'''
	# 字体(ttf/otf)，其他设置应注意路径
	# 建议选择无版权或免费商用字体
	font = ImageFont.truetype(font_path, font_size)
	# 多行文字处理
	text = text.split('\n')
	mark_width = 0
	for  i in range(len(text)):
		(width, height) = font.getsize(text[i])
		if mark_width < width:
			mark_width = width
	mark_height = height * len(text)

	# 生成图片
	mark = Image.new('RGBA', (mark_width, mark_height))
	draw = ImageDraw.ImageDraw(mark, "RGBA")
	for i in range(len(text)):
		(width, height) = font.getsize(text[i])
		draw.text((0, i*height), text[i], fill=font_color, font=font)
	mark.save('i.tmp', 'png')
	return Image.open('i.tmp')

# 输出CCLOGO Image对象
# ColorMode: Light/Dark
def CCLogoOutput(ColorMode):
	LOGO = base64.b64decode(CCLOGO[ColorMode])
	open('cc.tmp', 'wb').write(LOGO)
	return Image.open('cc.tmp')

# 将两个图像排在一排
def Splicing2ImagesInRaw(img1, img2):
	width = img1.width + img2.width + 10
	if(img1.height > img2.height):
		height = img1.height
	else:
		height = img2.height
	
	target = Image.new('RGBA', (width, height))
	target.paste(img1, (0,0))
	target.paste(img2, (135,0))
	# 缩放
	#target = target.resize((int(width * zoom),int(height * zoom)), Image.ANTIALIAS)
	return target

def getWatermark(mode):
	return Splicing2ImagesInRaw(
		CCLogoOutput(mode), 
		text2img(CopyrightInfo,random.choice(allFonts), font_color=Color[mode], font_size=40))

# 返回图片明暗程度（0-255）
def BrightnessDetect(img):
	# 转换为灰度单通道
	imgGray = img.convert('L')
	# 裁剪 (左上x，左上y，右下x，右下y)
	box = (0,0,int(imgGray.size[0]*0.33),int(imgGray.size[1]*0.33))
	img = img.crop(box)
	
	return ImageStat.Stat(imgGray).mean[0]

# 水印添加
# img 	图片对象
# left	水印位于左	
# top	水印位于上
def PutOnWatermark(img, left = True, top = True):
	# 先取得一个水印样本
	watermark = getWatermark(0)
	p =  img.width / watermark.width
	watermark = watermark.resize((int(watermark.width * p * 0.25) , int(watermark.height * p * 0.25)))
	if(left and top):
		x = int(0.03125 * img.width)
		y = int(0.03125 * img.height)
	elif(left and not top):
		x = int(0.03125 * img.width)
		y = img.height - watermark.height - int(0.03125 * img.height)
	elif(top and not left):
		x = img.width - watermark.width - int(0.03125 * img.width)
		y = int(0.03125 * img.height)
	else: 
		x = img.width - watermark.width - int(0.03125 * img.width)
		y = img.height - watermark.height - int(0.03125 * img.height)
	box = (x, y, x + watermark.width, y + watermark.height)
	
	
	# 水印模式：灰度>127使用深色水印，灰度<127使用浅色水印
	watermarkmode = Light
	imgsample = img.crop(box)
	if(BrightnessDetect(imgsample) > 127):
		watermarkmode = Dark
	


	watermark = getWatermark(watermarkmode)
	p =  img.width / watermark.width
	watermark = watermark.resize((int(watermark.width * p * 0.25) , int(watermark.height * p * 0.25)))
	
	(r, g, b, a) = watermark.split()

	img.paste(watermark, ( x, y), mask=a)
	#return img

if __name__ == "__main__":
	DEST = os.path.join(sys.path[0], destination_pic_dir)

	# 受限于Git，上传时不会创建图片资源目录
	try:
		os.remove(DEST)
	except:
		pass

	try:
		os.mkdir(DEST)
	except:
		pass	

	# 直接转移不需要水印的图片站点静态文件目录下的postrc

	#os.chdir(os.path.join(sys.path[0], '..','postrc_source', 'pure'))

	for a in os.listdir(os.path.join(sys.path[0], '..','postrc_source', 'modify_needless')):
		if(a.split('.')[-1] == 'webp'):
			shutil.copy(os.path.join(sys.path[0], '..','postrc_source', 'modify_needless', a), DEST)
			#r = Image.open(os.path.join(sys.path[0], '..','postrc_source', 'pure', a))
			#while(r.size[0] > 2500 or r.size[1] > 2500):
			#	r = r.resize((int(r.size[0]*0.8), int(r.size[1]*0.8)))
			#r.save(os.path.join(sys.path[0], destination_pic_dir, a))
			print("PASS: "+ a)
			#time.sleep(0.25)
		else:
			pass



	for a in os.listdir(os.path.join(sys.path[0], '..','postrc_source', 'pure')):
		if(a.split('.')[-1] == 'webp'):
			#shutil.copy(os.path.join(sys.path[0], '..','postrc_source', 'pure', a), os.path.join(sys.path[0], destination_pic_dir))
			r = Image.open(os.path.join(sys.path[0], '..','postrc_source', 'pure', a))
			while(r.size[0] > 2500 or r.size[1] > 2500):
				r = r.resize((int(r.size[0]*0.8), int(r.size[1]*0.8)))
			r.save(os.path.join(sys.path[0], destination_pic_dir, a))
			print("PASS: "+ a)
			#time.sleep(0.25)
		else:
			pass

	# 添加水印
	# 我帮你加了多线程，记得先看看能不能用，再谢谢我

	for a in os.listdir(os.path.join(sys.path[0], '..','postrc_source', 'watermark')):
		if(a.split('.')[-1] == 'webp'):

			def ___():
				t = Image.open(os.path.join(sys.path[0], source_pic_dir, a))
				
				if(a.split('.')[1] != 'webp' and len(re.compile(r'0b..').findall(a.split('.')[1]))):
					b = int(a.split('.')[1].split('0b')[1],2)
					PutOnWatermark(t, bool(b >> 0b01), bool(b % 0b10))
				else:
					PutOnWatermark(t, True, True)

				
				while(t.size[0] > 1920 or t.size[1] > 1080):
					t = t.resize((int(t.size[0]*0.8), int(t.size[1]*0.8)))
				
				try:
					#webp.save_image(t, os.path.join(os.path.join(sys.path[0], destination_pic_dir, a)), quality=80)
					t.save(os.path.join(os.path.join(sys.path[0], destination_pic_dir, a)))
				except:
					print('IGONRE: ' + a)
				else:
					print('PASS: '+a)
			_thread.start_new_thread(___,(),)
			
		else:
			print('IGONRE: '+ a)

	