# encoding=utf8

import Image as image
#等比例压缩图片
def resizeImg(**args):
	args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q':75}
	arg = {}

	for key in args_key:
		if key in args:
			arg[key] = args[key]

	im = image.open(arg['ori_img'])
	ori_w,ori_h = im.size
	widthRatio = heightRatio = None
	ratio = 1
	if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
		if arg['dst_w'] and ori_w > arg['dst_w']:
			widthRatio = float(arg['dst_w']) / ori_w

		if arg['dst_h'] and ori_h > arg['dst_h']:
			heightRatio = float(arg['dst_h']) / ori_h

		if widthRatio and heightRatio:
			if widthRatio < heightRatio:
				ratio = widthRatio
			else:
				ratio = heightRatio

		if widthRatio and not heightRatio:
			ratio = widthRatio

		if heightRatio and not widthRatio:
			ratio = heightRatio

		newWidth = int(ori_w * ratio)
		newHeight = int(ori_h * ratio)

	else:
		newWidth = ori_w
		newHeight = ori_h

	im.resize((newWidth,newHeight),image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])

#裁剪图片
def clipResizeImg(**args):
	args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q':75}
	arg = {}
	for key in args_key:
		if key in args:
			arg[key] = args[key]

	im = image.open(arg['ori_img'])
	ori_w,ori_h = im.size

	dst_scale = float(arg['dst_h']) / arg['dst_w']
	ori_scale = float(ori_h) / ori_w

	if ori_scale >= dst_scale:
		#Too height
		width = ori_w
		height = int(width*dst_scale)

		x = 0
		y = (ori_h - height) / 3

	else:
		#Too width
		height = ori_h
		width = int(height*dst_scale)

		x = (ori_w - width) / 2
		y = 0

	box = (x, y , width+x, height+y)
	newIm = im.crop(box)
	im = None

	ratio = float(arg['dst_w']) / width
	newWidth = int(width * ratio)
	newHeight = int(height * ratio)
	newIm.resize((newWidth,newHeight),image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])



	#缩放图片
def scaleImage(**args):
	args_key = {'ori_img':'','dst_img':'','scale':'','save_q':75}
	arg = {}
	for key in args_key:
		if key in args:
			arg[key] = args[key]

	im = image.open(arg['ori_img'])
	ori_w,ori_h = im.size

	newWidth = int(ori_w * arg['scale'])
	newHeight = int(ori_h * arg['scale'])

	im.resize((newWidth,newHeight),image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])


#水印
def waterMark(**args):
	args_key = {'ori_img':'','dst_img':'','mark_img':'','water_opt':''}
	arg = {}
	for key in args_key:
		if key in args:
			arg[key] = args[key]

	im = image.open(arg['ori_img'])
	ori_w,ori_h = im.size

	mark_im = image.open(arg['mark_img'])
	mark_w,mark_h = mark_im.size
	option = {'leftup':(0,0),'rightup':(ori_w-mark_w,0),'leftlow':(0,ori_h-mark_h),'rightlow':(ori_w-mark_w,ori_h-mark_h)}
	im.paste(mark_im,option[arg['water_opt']],mark_im.convert('RGBA'))
	im.save(arg['dst_img'])



#Demo
#源图片
#ori_img = 'D:/xx.jpg'
#mark_img = 'D:/mark.png'
#water_opt = 'rightlow'
#dst_img = 'D:/python_2.jpg'
#dst_w = 94
#dst_h = 94
#save_q = 35
#clipResizeImg(ori_img=ori_img,dst_img=dst_img,dst_w=dst_w,dst_h=dst_h,save_q=save_q)