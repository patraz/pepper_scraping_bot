import os

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

FILE_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(FILE_PATH)
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")


class Template:
    template_name = None
    context = None

    def __init__(self, template_name='', context={}, *args, **kwargs):
        self.template_name = template_name
        self.context = context

    def get_template(self):
        template_path = os.path.join(TEMPLATE_DIR, self.template_name)

        if not os.path.exists(template_path):
            raise Exception("this path does not exists")
        template_string = ''

        with open(template_path, "r") as f:
            template_string = f.read()
        return template_string

    def render(self, context={}):
        render_ctx = {}
        if self.context != None:
            render_ctx = self.context
        if not isinstance(render_ctx, dict):
            render_ctx = {}
        template_string = self.get_template()
        return template_string.format(**render_ctx)
