
controllerPrefix = 'controllers.'
urls = (
    '/', controllerPrefix + 'index.index',
    '/chart/(.*)',controllerPrefix + 'chart.index',
    '/rescutime',controllerPrefix + 'my.index',
    '/prd',controllerPrefix + 'prd.index',
    '/prd/edit/(.*)/',controllerPrefix + 'prd.edit',
    '/resizepic', controllerPrefix + 'prd.resizepic',
    '/upload', controllerPrefix + 'prd.upload',
        )
