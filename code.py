import web

urls = (
    '/', 'index.index',
    '/chart/(.*)','chart.index',
    '/rescutime','my.index'
        )

app = web.application(urls,globals())

render = web.template.render('templates/')

class index:
    def GET(self,name):
        i = web.input(name=None)
        return render.index(i.name)



if __name__ == "__main__":
    app.run()
