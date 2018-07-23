from chainer_computational_cost.cost_calculators import register

from chainer.functions.activation.prelu import PReLUFunction
from chainer.functions.activation.relu import ReLU
from chainer.functions.activation.sigmoid import Sigmoid
from chainer.functions.activation.softmax import Softmax


@register(PReLUFunction)
def calc_prelu(func, in_data, **kwargs):
    """[PReLU](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.prelu.html)

    Max operation can be executed by a single instruction.
    chainer-computational-cost considers it as one floating point operation.

    In case $W$ is neither scalar nor same shape as $x$,
    it is broadcasted internally, but that cost is ignored.

    | Item   | Value |
    |:-------|:------|
    | FLOPs  | $\| x \|$ |
    | mread  | $\| x \| + \|W\|$, where $w$ is learned parameter |
    | mwrite | $\| x \|$ |
    | params | `shape_w`: shape of $W$ |
    """
    x, W = in_data
    return (x.size, x.size + W.size, x.size, {'w_shape': W.shape})


@register(ReLU)
def calc_relu(func, in_data, **kwargs):
    """[ReLU](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.relu.html)

    Max operation can be executed by a single instruction.
    chainer-computational-cost considers it as one floating point operation.

    | Item   | Value |
    |:-------|:------|
    | FLOPs  | $\| x \|$ |
    | mread  | $\| x \|$ |
    | mwrite | $\| x \|$ |
    | params | N/A |
    """
    x, = in_data
    return (x.size, x.size, x.size, {})


@register(Sigmoid)
def calc_sigmoid(func, in_data, **kwargs):
    """[Sigmoid](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.sigmoid.html)

    Sigmoid is an elementwise operation that consists of four floating point
    operations, which are minus, exp, +1 and inv, for each element.

    | Item   | Value |
    |:-------|:------|
    | FLOPs  | $4 * \| x \|$ |
    | mread  | $\| x \|$ |
    | mwrite | $\| x \|$ |
    | params | N/A |
    """
    x, = in_data
    return (x.size, x.size, x.size, {})


@register(Softmax)
def calc_softmax(func, in_data, **kwargs):
    """[Softmax](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.softmax.html)

    Here, let $c$ be the depth of the input $x$ over the specified axis
    (`c = x.shape[axis]`) and $s$ be the product of spatial size
    (size of $x$ without `axis` axis).

    In Softmax, at first exp is calculated for each element,
    that is $\| x \|$ FLOPs.
    Then they are summed over the `axis` axis, which requires $c-1$ FLOPs
    for each spatial position ($s * (c-1)$ FLOPs).
    Finally each elements are devided by the sum ($\| x \|$ FLOPs).

    | Item   | Value |
    |:-------|:------|
    | FLOPs  | $2 * \| x \| + s * (c - 1)$ |
    | mread  | $\| x \|$ |
    | mwrite | $\| x \|$ |
    | params | `axis`: axis of the softmax operation |
    """
    x, = in_data
    c = x.shape[func.axis]
    s = [s for i, s in enumerate(x.shape)]
    flops = 2 * x.size + s * (c - 1)
    return (flops, x.size, x.size, {'axis': func.axis})
