from django.conf import settings
from django.utils import module_loading


def autoload(submodules):
    for app in settings.INSTALLED_APPS:
        mod = module_loading.import_module(app)
        for submodule in submodules:
            try:
                module_loading.import_module("{}.{}".format(app, submodule))
            except:
                if module_loading.module_has_submodule(mod, submodule):
                    raise


def run():
    autoload(["signals"])
