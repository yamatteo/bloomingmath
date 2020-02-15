# from logging import warning, error
# from os import path, getcwd
# from typing import Callable, List, Optional
#
# from fastapi import FastAPI
# from starlette.templating import Jinja2Templates
# from starlette.responses import HTMLResponse
#
#
# class RenderEngine:
#     jinja2templates: List[Jinja2Templates] = None
#
#     def init_app(self, app: FastAPI, template_directory: str = "templates",
#                  template_directories: Optional[List[str]] = None):
#         if template_directories is not None:
#             self.jinja2templates = [
#                 Jinja2Templates(directory=path.join(getcwd(), directory)) for directory in template_directories
#             ]
#         else:
#             self.jinja2templates = [Jinja2Templates(directory=path.join(getcwd(), template_directory)), ]
#
#
# render_engine = RenderEngine()
#
#
# def get_render() -> Callable:
#     def render(*args, **kwargs):
#         for j2t in render_engine.jinja2templates:
#             try:
#                 return j2t.TemplateResponse(*args, **kwargs)
#             except Exception as exc:
#                 warning(f"Render function -- {type(exc)}", exc_info=True)
#         error("render function -- No valid templates engine provided.")
#         return HTMLResponse('<html><body><h1 style="text-align: center;margin-top: 40px;">Rendering engine error</h1></body></html>')
#
#     return render
