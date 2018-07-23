from chainer_computational_cost.cost_calculators import register

from chainer.functions.normalization.batch_normalization \
    import FixedBatchNormalization
from chainer.functions.normalization.local_response_normalization \
    import LocalResponseNormalization


@register(FixedBatchNormalization)
def calc_fixed_bn(func, in_data, **kwargs):
    x, _, _, mean, var = in_data
    x = in_data[0]
    n_elements = len(x.flatten())
    flops = n_elements * 2    # *2 <- scale and shift
    mread = n_elements + len(mean) + len(var)
    mwrite = n_elements
    return (flops, mread, mwrite, {'eps': func.eps})


@register(LocalResponseNormalization)
def calc_lrn(func, in_data, **kwargs):
    x, = in_data

    c = x.shape[1]
    s = c * func.k - (func.k // 2) * 2
    flops_square = x.size
    flops_neighbor_sum = x.size * s + x.size * 3
    flops_total = flops_square + flops_neighbor_sum + x.size
    flops = flops_total
    mread = x.size + x.shape[1] * x.shape[2] * s
    mwrite = x.size
    params = {
        'n': func.n, 'k': func.k,
        'alpha': func.alpha, 'beta': func.beta
    }
    return (flops, mread, mwrite, params)
