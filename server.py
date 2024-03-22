from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os

def hello_world(request):
    name = os.environ.get('NAME', 'world')
    message = f"Hello, {name}!\n"
    return Response(message)

def show_html(request):
    # Path to the HTML file
    html_path = os.path.join(os.path.dirname(__file__), 'src', 'templates', 'index.html')
    try:
        with open(html_path, 'r') as file:
            html_content = file.read()
        return Response(html_content, content_type='text/html')
    except FileNotFoundError:
        return Response("Error: HTML file not found", status=500)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        
        # Add route and view for serving HTML page
        config.add_route('html', '/html')
        config.add_view(show_html, route_name='html')
        
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    print(f"Server running on port {port}")
    server.serve_forever()
