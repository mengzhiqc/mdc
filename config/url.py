
controllerPrefix = 'controllers.'
urls = (
    '/', controllerPrefix + 'index.index',
    '/chart/(.*)',controllerPrefix + 'chart.index',
    '/rescutime',controllerPrefix + 'my.index'
        )