"""
Cost calculator auto discovery mechanism.
It automatically finds all the cost calculation methods whose signature is
'calc_XXXX(func: Type, in_data, **kwargs)'.
"""

import glob
import importlib
import inspect
import os


def _check_sig(p):
    if len(p) != 3 or list(p.keys()) != ['func', 'in_data', 'kwargs']:
        return False

    if p['func'].annotation == inspect._empty:
        return False

    if p['kwargs'].kind != inspect.Parameter.VAR_KEYWORD:
        return False

    return True


calculators = dict()

calc_pys = glob.glob(os.path.join(os.path.dirname(__file__), '*.py'))
calc_pys = [py for py in calc_pys if '__init__.py' not in py]
for full_py in calc_pys:
    py = os.path.basename(full_py)
    name = os.path.splitext(py)[0]

    fmt = 'chainer_computational_cost.cost_calculators.{}'.format(name)
    m = importlib.import_module(fmt)
    func_names = [f for f in dir(m) if f.startswith('calc_')]

    for func_name in func_names:
        func = getattr(m, func_name)
        p = inspect.signature(func).parameters

        if not _check_sig(p):
            sig = inspect.formatargspec(*inspect.getfullargspec(func))
            print("Warning: cost calculator signature mismatch: {}{}"
                  .format(func_name, sig))
            continue

        annot = p['func'].annotation
        if annot in calculators:
            old_name = calculators[annot].__name__
            print("Warning: cost calculator for {} already exists ({}). "
                  "Replace by {}".format(annot.__name__, old_name, func_name))
        calculators[annot] = func
