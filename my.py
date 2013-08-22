import web
render = web.template.render("templates",base="layout")

class index:
    def GET(self):
        return render.myindex()
