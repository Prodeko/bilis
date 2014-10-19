import os.path
from django.conf import settings
from django import template

register = template.Library()

@register.tag(name="image_or_empty")
def do_image_or_empty(parser, token):
    tag_name, path = token.split_contents()
    return ImageNode(path)
    
    
class ImageNode(template.Node):
    def __init__(self, path):
        self.path = path

    def render(self, context):
        self.path = self.path.replace("'","").replace("\"", "")
        print(self.path)
        if(os.path.isfile(settings.STATIC_ROOT + self.path)):
            return self.build_html(settings.STATIC_URL + self.path)
        else:
            return ""
    def build_html(self, full_path):
        return "<img class='top-banner' src='{}'>".format(full_path)