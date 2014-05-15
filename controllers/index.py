# coding:utf-8 
import web,os,time
from lib.util import git
from models.models import Devices
render = web.template.render("templates",base="layout")
data = {}
data['deviceTypeDic'] = {1:'手机',2:'平板',3:'主机',4:'显示器'}
data['deviceBelongDic'] = {1:'iOS开发团队',2:'android开发团队',3:'测试团队',4:'api团队'}

IMAGE_PREFIX = "static/ui/"

class index:
    def GET(self):
        i = web.input(name=None)
        devices = web.ctx.orm.query(Devices).all()
        data['devices'] = devices

        return render.index(data)


class new:
	def GET(self):
		data['deviceInfo'] = None
		return render.new(data)

class create:
	def POST(self):
		i = web.input()
		deviceName = i.get('device_name')
		deviceUser = i.get('device_user')
		deviceType = i.get('device_type')
		udid = i.get('udid')
		belong = i.get('belong')
		description = i.get('description')
		createTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		device = Devices(deviceName=deviceName,deviceUser=deviceUser,udid=udid,deviceType=deviceType,belong=belong,description=description,createTime=createTime);
		web.ctx.orm.add(device)
		raise web.seeother('/')

class edit:
	def GET(self,id):
		device = web.ctx.orm.query(Devices).get(id)
		data['deviceInfo'] = device
		return render.new(data)

	def POST(self,id):
		i= web.input()
		preDevice = web.ctx.orm.query(Devices).get(id)

		isChanged = 0

		if preDevice.device_name != i.get('device_name'):
			preDevice.device_name = i.get('device_name')
			isChanged = 1

		if preDevice.device_user != i.get('device_user'):
			preDevice.device_user = i.get('device_user')
			isChanged = 1

		if preDevice.udid != i.get('udid'):
			preDevice.udid = i.get('udid')
			isChanged = 1

		if preDevice.device_type != i.get('device_type'):
			preDevice.device_type = i.get('device_type')
			isChanged = 1

		if preDevice.belong != i.get('belong'):
			preDevice.belong = i.get('belong')
			isChanged = 1

		if preDevice.description != i.get('description'):
			preDevice.description = i.get('description')
			isChanged = 1

		if isChanged == 1:
			preDevice.updated_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

		web.ctx.orm.commit()

		raise web.seeother('/')

class delete:
	def GET(self,id):
		device = web.ctx.orm.query(Devices).get(id)
		web.ctx.orm.delete(device)
		raise web.seeother('/')
