import web
render = web.template.render("templates",base="layout")

class index:
    def GET(self,cid):
        return render.chartindex(cid,"Chart Center")
