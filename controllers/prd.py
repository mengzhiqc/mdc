import web
render = web.template.render("templates",base="layout")

class index:
    def GET(self):
        return render.prdindex("PRD LIST")

class edit:
    def GET(self,prdId):
        data = {}
        data['id'] = prdId
        return render.prdedit(data,"Edit PRD")

class resizepic:
	def GET(self):
		data = {}
		return render.prdresizepic(data,"Rize Your Picture")

class upload:
	def POST(self):
		data = {}
		x = web.input(imagefile={})
		print x
		filedir = './static/upload'
		if 'imagefile' in x:
			filepath = x.imagefile.filename.replace('\\','/')
			filename = filepath.split('/')[-1]
			fout = open(filedir + '/' + filename, 'w')
			fout.write(x.imagefile.file.read())
			fout.close()
			web.header('content-type','text/plain')
			imageUrl = '/static/upload/' + filename
			return '<img src="'+imageUrl+'" id="toHandleImage" name="toHandleImage" />'
		return '' 

	def GET(self):
		return "this is get"