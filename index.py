import web
render = web.template.render("templates")
class index:
    def GET(self):
        i = web.input(name=None)
        return render.index(i.name)
