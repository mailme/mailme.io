# taken from sentry

import pkgutil
import sys


def import_submodules(context, root_module, path):
    """
    Import all submodules and register them in the ``context`` namespace.

    >>> import_submodules(globals(), __name__, __path__)
    """
    for loader, module_name, is_pkg in pkgutil.walk_packages(path):
        module = loader.find_module(module_name).load_module(module_name)
        for k, v in vars(module).items():
            if not k.startswith('_'):
                context[k] = v
        context[module_name] = module
        sys.modules['{0}.{1}'.format(root_module, module_name)] = module
