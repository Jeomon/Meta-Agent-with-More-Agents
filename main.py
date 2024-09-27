from fasthtml.common import *

app,route=fast_app()

@route('/')
def get():
    return Div(P("Hello World"),hx_get='/change')

@route('/change')
def get():
    return Div(P('Hi'))