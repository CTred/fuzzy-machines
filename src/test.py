# %%
from fuzz.kernel import Kernel
from fuzz.memb_funcs import Linear, Constant, Trapmf
from fuzz.rules import AND, OR, IS, NOT
from fuzz.engine import Engine

food = (
    Kernel(0,10)
        .add_memb_func('good', Linear(4, 10))
        .add_memb_func('rancid', Trapmf(-1, 0, 8, 4))
)

service = (
    Kernel(0,10)
        .add_memb_func('great', Linear(5, 10))
        .add_memb_func('poor', Linear(7, 3))
)

tips = (
    Kernel(10,30)
        .add_memb_func('low', Constant(10,15))
        .add_memb_func('average', Constant(15,25))
        .add_memb_func('high', Constant(25,30))
)

# %%
eng = (
    Engine()
        .add_kernel("food", food)
        .add_kernel("service", service)
        .add_inference_kernel(tips)
        .add_rule('low', IS({'food':'rancid'}))
        .add_rule('average', AND({"food": "good"}, {"service": "poor"}))
        .add_rule('high', AND({"food": "good"}, {"service": "great"}))
)

# %%
eng.run_defuzz({'food': 8, 'service': 3}, 1)
res = eng.gen_surface(20, 1)
# %%