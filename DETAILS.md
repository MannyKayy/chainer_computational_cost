# Details of theoretical computational costs

This document explains how chainer-computational-cost estimates
theoretical computational cost of each type of layer.
Unless otherwise specified, <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20x"/> stands for the input to the layer and
<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20y"/> is output. <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%20%5C%7C%20x%20%5C%7C%20"/> is the number of elements in <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20x"/>
(equivalent to `x.size`), if <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20x"/> is empty or does not exist,
<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C%20%3D%200"/>.

The basic strategy of how the "theoretical computational cost" is defined
is written in [README.md](README.md).


## Table of contents

* [Activation](#activation)
  * [PReLUFunction](#prelufunction)
  * [ReLU](#relu)
  * [Sigmoid](#sigmoid)
  * [Softmax](#softmax)
* [Array](#array)
  * [Concat](#concat)
  * [Reshape](#reshape)
  * [ResizeImages](#resizeimages)
  * [Transpose](#transpose)
* [Basic math](#basic-math)
  * [Add](#add)
  * [AddConstant](#addconstant)
  * [Div](#div)
  * [DivFromConstant](#divfromconstant)
  * [Mul](#mul)
  * [MulConstant](#mulconstant)
  * [Sub](#sub)
  * [SubFromConstant](#subfromconstant)
* [Connection](#connection)
  * [Convolution2DFunction](#convolution2dfunction)
  * [Deconvolution2DFunction](#deconvolution2dfunction)
  * [LinearFunction](#linearfunction)
  * [Shift](#shift)
* [Normalization](#normalization)
  * [FixedBatchNormalization](#fixedbatchnormalization)
  * [LocalResponseNormalization](#localresponsenormalization)
* [Pooling](#pooling)
  * [AveragePooling2D](#averagepooling2d)
  * [MaxPooling2D](#maxpooling2d)


## Activation

### [PReLUFunction](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.prelu.html)

Max operation can be executed by a single instruction.
chainer-computational-cost considers it as one floating point operation.

In case <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20W"/> is neither scalar nor same shape as <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20x"/>, it is broadcasted
internally, but cost for broadcasting operation is ignored.

| Item   | Value |
|:-------|:------|
| FLOPs  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> |
| mread  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C%20%2B%20%5C%7CW%5C%7C"/>, where <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20W"/> is learned parameter |
| mwrite | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> |
| params | `w_shape`: shape of <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20W"/> |


### [ReLU](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.relu.html)

Max operation can be executed by a single instruction.
chainer-computational-cost considers it as one floating point operation.

| Item   | Value |
|:-------|:------|
| FLOPs  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> |
| mread  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> |
| mwrite | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> |
| params | N/A |


### [Sigmoid](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.sigmoid.html)

Sigmoid is an elementwise operation that consists of four floating point
operations, which are minus, exp, +1 and inv, for each element.

| Item   | Value |
|:-------|:------|
| FLOPs  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%204%20%5C%7C%20x%20%5C%7C"/> |
| mread  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> |
| mwrite | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> |
| params | N/A |


### [Softmax](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.softmax.html)

Here, let <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20c"/> be the depth of the input <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20x"/> over the specified axis
(`c = x.shape[axis]`) and <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20s"/> be the product of spatial size
(size of <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20x"/> without `axis` axis).

In Softmax, at first exp is calculated for each element,
that is <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> FLOPs.
Then they are summed over the `axis` axis, which requires <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20c-1"/> FLOPs
for each spatial position (<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20s%20%2A%20%28c-1%29"/> FLOPs).
Finally each elements are devided by the sum (<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> FLOPs).

| Item   | Value |
|:-------|:------|
| FLOPs  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%202%20%5C%7C%20x%20%5C%7C%20%2B%20s%28c-1%29"/> |
| mread  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> |
| mwrite | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> |
| params | `axis`: axis of the softmax operation |


## Array

### [Concat](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.concat.html)

Concatenation is just a memory copy, hense no floating point
operation will be conducted.
Depending on concatenation axis, index calculation might be needed
but chainer-computational-cost ignores such operations.

| Item   | Value |
|:-------|:------|
| FLOPs  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%200%20"/> |
| mread  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5Csum_%7Bi%7D%20%5C%7Cx_%7Bi%7D%5C%7C"/> |
| mwrite | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5Csum_%7Bi%7D%20%5C%7Cx_%7Bi%7D%5C%7C"/> |
| params | `axis`: concatenation axis |


### [Reshape](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.reshape.html)

Reshape operation basically neither changes nor reads the data.
It just makes an array with same data reference with different metadata.

If your environment cannot do in-place reshape, consider overwriting
by a custom cost calculator (refer README.md).

| Item   | Value |
|:-------|:------|
| FLOPs  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%200%20"/> |
| mread  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%200%20"/> |
| mwrite | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%200%20"/> |
| params | `in_shape`: input shape, `out_shape`: output shape |


### [ResizeImages](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.resize_images.html)

In bilinear resize operation, each output pixel value is calculated by
4 neighboring source pixels in the input image.

In order to know where the source pixel is, a few index calculations
including floating point arithmetic is needed, but these are ignored since
chainer-computational-cost ignores such index calculations.

To calculate an output value from 4 source pixels,
first 3 FLOPs is spent for horizontal interpolation from 2 source pixels,
then another 3 FLOPs for vertical, and finally 3 FLOPs for inter-axis
interpolation, therefore in total 9 FLOPs for each output pixel.

As for memory access, especially in case of expanding the source image,
duplicated memory read will happen. For example, if the input image is 8x8
and the output size is 32x32, naively reading memory runs 4096 times,
even though the actual size of the input is only 64.
In order to avoid such a contradiction, chainer-computational-cost
introduces a policy to treat such case as if it loads the entire input
data only once.

Conversely, in case not all the image is needed (for example input is
32x32 and the output is 8x8, where memory read is only 128),
chainer-computational-cost simply counts 4 memory reads for each output
pixel.

Either smaller number is used for memory read estimation.
In other words, memory read is formulated as
<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%20%5Cmax%284%20%5C%7C%20y%5C%7C%2C%20%5C%7Cx%5C%7C%29%20"/>.

Considering extreme cases like shrinking horizontally and expanding
vertically, this logic should be much complicated, but for simplicity
chainer-computational-cost only uses the above formula.

| Item   | Value |
|:-------|:------|
| FLOPs  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%209%20%5C%7C%20y%20%5C%7C%20"/> |
| mread  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5Cmin%284%20%5C%7C%20y%5C%7C%2C%20%5C%7Cx%5C%7C%29%20"/> |
| mwrite | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5C%7C%20y%20%5C%7C%20"/> |
| params | `size`: output size |


### [Transpose](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.transpose.html)

Transpose operation is just copying memory with no FLOPs.

| Item   | Value |
|:-------|:------|
| FLOPs  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%200%20"/> |
| mread  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5C%7C%20x%20%5C%7C%20"/> |
| mwrite | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5C%7C%20x%20%5C%7C%20"/> |
| params | `axes`: transpose axes |


## Basic math

### [Add](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.add.html)

Elementwise Add operation.
In case shape of inputs are different, broadcast will run and then
elementwise arithmetic is conducted.
Cost for broadcasting is ignored.
For simplicity, it assumes all the arrays are first broadcasted to the
output size then elementwise sum is calculated.
The output size is the largest size of the input.

| Item   | Value |
|:-------|:------|
| FLOPs  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%28N-1%29%20%5Cmax_%7Bi%7D%5E%7BN%7D%20%5C%7C%20x_%7Bi%7D%20%5C%7C%20"/> |
| mread  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5Csum_%7Bi%7D%5E%7BN%7D%20%5C%7C%20x_%7Bi%7D%20%5C%7C%20"/> |
| mwrite | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5Cmax_%7Bi%7D%5E%7BN%7D%20%5C%7C%20x_%7Bi%7D%20%5C%7C%20"/> |
| params | N/A |


### [AddConstant](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.add.html)

AddConstant is elementwise Add operation where the operand is a constant
(not a chainer.Variable but a numpy.array or a cupy.array).

In case shape of inputs are different, broadcast will run and then
elementwise arithmetic is conducted.  Cost for broadcasting is ignored.
The output size is same as the larger one of either the input (<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20x"/>) or the
operand (`<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20c"/>`).

| Item   | Value |
|:-------|:------|
| FLOPs  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5Cmax%28%5C%7C%20x%20%5C%7C%2C%20%5C%7C%20c%20%5C%7C%29%20%5C%7C%20"/> |
| mread  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5C%7C%20x%20%5C%7C%20%2B%20%5C%7C%20c%20%5C%7C%20"/> |
| mwrite | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5Cmax%28%5C%7C%20x%20%5C%7C%2C%20%5C%7C%20c%20%5C%7C%29%20%5C%7C%20"/> |
| params | N/A |


### [Div](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.add.html)

See the documentation for [Add](#add)


### [DivFromConstant](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.add.html)

See the documentation for [AddConstant](#addconstant)


### [Mul](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.add.html)

See the documentation for [Add](#add)


### [MulConstant](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.add.html)

See the documentation for [AddConstant](#addconstant)


### [Sub](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.add.html)

See the documentation for [Add](#add)


### [SubFromConstant](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.add.html)

See the documentation for [AddConstant](#addconstant)


## Connection

### [Convolution2DFunction](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.convolution_2d.html)

Convolution operator essentially calculates an output value by convolving
the input feature map by a corresponding filter whose size is
<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20k_%7Bh%7D%20k_%7Bw%7D%20%7Bc_%7B%5Cmathrm%7Bin%7D%7D%7D"/>.
The computational cost is <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%202%20k_%7Bh%7D%20k_%7Bw%7D%20%7Bc_%7B%5Cmathrm%7Bin%7D%7D%7D%20-%201"/> FLOPs
for each output pixel. Including bias, it becomes simply
<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%202%20k_%7Bh%7D%20k_%7Bw%7D%20%7Bc_%7B%5Cmathrm%7Bin%7D%7D%7D"/>.
So in total <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%202%20k_%7Bh%7D%20k_%7Bw%7D%20%7Bc_%7B%5Cmathrm%7Bin%7D%7D%7D%20h_%7B%5Cmathrm%7Bout%7D%7D%20w_%7B%5Cmathrm%7Bout%7D%7D%20c_%7B%5Cmathrm%7Bout%7D%7D%20"/>.
Here, output size <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20h_%7B%5Cmathrm%7Bout%7D%7D"/> and <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20w_%7B%5Cmathrm%7Bout%7D%7D"/> can be
calculated by
[chainer.utils.get_conv_outsize](https://docs.chainer.org/en/v4.3.0/reference/util/generated/chainer.utils.get_conv_outsize.html).

If there is no bias, it will be
<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%20%282%20k_%7Bh%7D%20k_%7Bw%7D%20%7Bc_%7B%5Cmathrm%7Bin%7D%7D%7D-1%29%20h_%7B%5Cmathrm%7Bout%7D%7D%20w_%7B%5Cmathrm%7Bout%7D%7D%20c_%7B%5Cmathrm%7Bout%7D%7D%20"/> FLOPs.

In case of grouped convolution, it can be considered as just concatenating
result of convolution whose input has <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20c_%7B%5Cmathrm%7Bin%7D%7D/G"/> channels and
output is <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20c_%7B%5Cmathrm%7Bout%7D%7D/G"/> channels.
Each group costs <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%202%20k_%7Bh%7D%20k_%7Bw%7D%20c_%7B%5Cmathrm%7Bin%7D%7D%20h_%7B%5Cmathrm%7Bout%7D%7D%20w_%7B%5Cmathrm%7Bout%7D%7D%20c_%7B%5Cmathrm%7Bout%7D%7D/G%5E2%20"/> FLOPs/group,
so in total <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%202%20k_%7Bh%7D%20k_%7Bw%7D%20c_%7B%5Cmathrm%7Bin%7D%7D%20h_%7B%5Cmathrm%7Bout%7D%7D%20w_%7B%5Cmathrm%7Bout%7D%7D%20c_%7B%5Cmathrm%7Bout%7D%7D%20/%20G%20"/> FLOPs.

If `fma_1flop` is set to `True`,
it will be <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%20k_%7Bh%7D%20k_%7Bw%7D%20c_%7B%5Cmathrm%7Bin%7D%7D%20h_%7B%5Cmathrm%7Bout%7D%7D%20w_%7B%5Cmathrm%7Bout%7D%7D%20c_%7B%5Cmathrm%7Bout%7D%7D%20/%20G%20"/> FLOPs.
Exsistence of bias does not matter this case.

Dilated convolution does not change theoretical computational cost
explained above, although it usually significantly affects to the actual
performance.

Although a source pixel can be read multiple times in the most native
convolution implementation, chainer-computational-cost counts them only
once, therefore the memory read is counted as if the entire input data and
parameters (weights, biases) are loaded from memory only at once.
Padding is ignored, too.

FMA option can be switched by `fma_1flop: bool` keyword argument specified
to ComputationalCostHook.

| Item                | Value |
|:--------------------|:------|
| FLOPs(FMA)          | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20c_%7B%5Cmathrm%7Bin%7D%7D%20c_%7B%5Cmathrm%7Bout%7D%7D%20k_%7Bh%7D%20k_%7Bw%7D%20h_%7B%5Cmathrm%7Bout%7D%7D%20w_%7B%5Cmathrm%7Bout%7D%7D%20/%20G%20"/> |
| FLOPs(no-FMA)       | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%202%20c_%7B%5Cmathrm%7Bin%7D%7D%20c_%7B%5Cmathrm%7Bout%7D%7D%20k_%7Bh%7D%20k_%7Bw%7D%20h_%7B%5Cmathrm%7Bout%7D%7D%20w_%7B%5Cmathrm%7Bout%7D%7D%20/%20G%20"/> |
| FLOPs(no-FMA nobias)| <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20G%282%20%28c_%7B%5Cmathrm%7Bin%7D%7D/G%29%20%28c_%7B%5Cmathrm%7Bout%7D%7D/G%29-1%29%20k_%7Bh%7D%20k_%7Bw%7D%20h_%7B%5Cmathrm%7Bout%7D%7D%20w_%7B%5Cmathrm%7Bout%7D%7D%20"/> |
| mread               | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C%20%2B%20%5C%7C%20W%20%5C%7C%20%2B%20%5C%7C%20b%20%5C%7C"/> |
| mwrite              | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20c_%7B%5Cmathrm%7Bout%7D%7D%20h_%7B%5Cmathrm%7Bout%7D%7D%20w_%7B%5Cmathrm%7Bout%7D%7D"/> |
| params              | conv parameters `k`, `s`, `p`, `d`, `groups`, `nobias` |


### [Deconvolution2DFunction](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.deconvolution_2d.html)

Deconvolution, also as known as transposed convolution, can be thought as
going backward to the convolution operation.
Each input pixel is multiplied to convolution filter kernel
(<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%28c_%7B%5Cmathrm%7Bout%7D%7D%2C%20k_h%2C%20k_w%29"/>).
Its result is summed up on the output tensor, among adjacent result and
result of other filters (there are <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20c_%7B%5Cmathrm%7Bin%7D%7D"/> filters),
then bias is added if exists.

In order to understand the behavior of this operation and why it is called
"transposed" convolution, these materials are helpful.
* [Up-sampling with Transposed Convolution - Towards Data Science](https://towardsdatascience.com/9ae4f2df52d0)
* [Convolution arithmetic tutorial - Theano 1.0.0 documentation](http://deeplearning.net/software/theano/tutorial/conv_arithmetic.html)

The theoretical computational cost is
<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%202%20c_%7B%5Cmathrm%7Bout%7D%7D%20k_h%20k_w%20h_%7B%5Cmathrm%7Bin%7D%7D%20w_%7B%5Cmathrm%7Bin%7D%7D%20c_%7B%5Cmathrm%7Bin%7D%7D"/>FLOPs.

In case of `groups` is not 1, similarly to convolution, it becomes
<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%202%20c_%7B%5Cmathrm%7Bout%7D%7D%20k_h%20k_w%20h_%7B%5Cmathrm%7Bin%7D%7D%20w_%7B%5Cmathrm%7Bin%7D%7D%20c_%7B%5Cmathrm%7Bin%7D%7D%20/%20G"/> FLOPs.

| Item                | Value |
|:--------------------|:------|
| FLOPs(FMA)          | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%202%20c_%7B%5Cmathrm%7Bin%7D%7D%20c_%7B%5Cmathrm%7Bout%7D%7D%20k_h%20k_w%20h_%7B%5Cmathrm%7Bin%7D%7D%20w_%7B%5Cmathrm%7Bin%7D%7D%20/%20G%20"/> |
| FLOPs(no-FMA)       | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20c_%7B%5Cmathrm%7Bin%7D%7D%20c_%7B%5Cmathrm%7Bout%7D%7D%20k_h%20k_w%20h_%7B%5Cmathrm%7Bin%7D%7D%20w_%7B%5Cmathrm%7Bin%7D%7D%20/%20G%20"/> |
| mread               | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C%20%2B%20%5C%7C%20W%20%5C%7C%20%2B%20%5C%7C%20b%20%5C%7C"/> |
| mwrite              | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20c_%7B%5Cmathrm%7Bout%7D%7D%20h_%7B%5Cmathrm%7Bout%7D%7D%20w_%7B%5Cmathrm%7Bout%7D%7D"/> |
| params              | conv parameters `k`, `s`, `p`, `d`, `groups`, `nobias` |


### [LinearFunction](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.linear.html)

Let <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20n_%7B%5Cmathrm%7Bin%7D%7D"/> be the input size and <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20n_%7B%5Cmathrm%7Bout%7D%7D"/> be the
output size.
Each output value is calculated by <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20n_%7B%5Cmathrm%7Bin%7D%7D"/> product and
<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20n_%7B%5Cmathrm%7Bin%7D%7D%20-%201"/> sum operations.
So, in case `fma_1flop==False`, <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%202%20n_%7B%5Cmathrm%7Bin%7D%7D%20-%201"/> FLOPs/element,
or <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%202%20%2A%20n_%7B%5Cmathrm%7Bin%7D%7D"/> if there is bias.
In FMA mode <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20n_%7B%5Cmathrm%7Bin%7D%7D"/> FLOPs (regardress of existence of bias).

FMA option can be switched by `fma_1flop: bool` keyword argument specified
to ComputationalCostHook.

| Item                  | Value |
|:----------------------|:------|
| FLOPs(FMA)            | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20n_%7B%5Cmathrm%7Bin%7D%7D%20n_%7B%5Cmathrm%7Bout%7D%7D%20%5C%7C"/> |
| FLOPs(no-FMA)         | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%202%20n_%7B%5Cmathrm%7Bin%7D%7D%20n_%7B%5Cmathrm%7Bout%7D%7D%20%5C%7C"/> |
| FLOPs(no-FMA no-bias) | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20%282%20n_%7B%5Cmathrm%7Bin%7D%7D%20-%201%29%20n_%7B%5Cmathrm%7Bout%7D%7D%20%5C%7C"/> |
| mread                 | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7Cx%5C%7C%20%2B%20%5C%7CW%5C%7C%20%2B%20%5C%7Cb%5C%7C"/>, where <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20W"/> and <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20b"/> are learned parameter |
| mwrite                | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7Cy%5C%7C"/> |
| params                | `nobias` |


### [Shift](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.shift.html)

Shift only conducts memory read, index calculation and memory write.
There might be unnecessary memory read around corners, but for simplicity
chainer-computational-cost treats it as just reading the entire data.

| Item   | Value |
|:-------|:------|
| FLOPs  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%200%20"/> |
| mread  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> |
| mwrite | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> |
| params | shift parameters `k` and `d` |


## Normalization

### [FixedBatchNormalization](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.fixed_batch_normalization.html)

Test-mode batch normalization.
It consists of normalization part (using <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5Cmu"/> and <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5Csigma"/>) and
bias part (<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5Cgamma"/> and <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5Cbeta"/>), both are composed of
elementwise scale and shift. However this can actually be fused into single
scale and shift operation.
Therefore, regardless of existence of bias (<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5Cgamma"/> and <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5Cbeta"/>),
computational cost is always <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%202%20%5C%7Cx%5C%7C"/> FLOPs.

Since scale-and-shift operation can be done by FMA,
it becomes <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5C%7Cx%5C%7C"/> FLOPs if `fma_1flop` is set to `True`.

Due to the same reason as explained above, reading learned scale and shift
parameter is required only once (not twice) regardless of bias existence.
Both are 1-dimensional array with <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20c_%7B%5Cmathrm%7Bin%7D%7D"/> elements.

| Item          | Value |
|:--------------|:------|
| FLOPs(FMA)    | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5C%7C%20x%20%5C%7C%20"/> |
| FLOPs(no-FMA) | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%202%20%5C%7C%20x%20%5C%7C%20"/> |
| mread         | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5C%7Cx%5C%7C%20%2B%202%20c_%7B%5Cmathrm%7Bin%7D%7D%20"/> |
| mwrite        | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5C%7C%20x%20%5C%7C%20"/> |
| params        | `eps`: epsilon for BN |


### [LocalResponseNormalization](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.local_response_normalization.html)

Let <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20c"/>, <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20h"/> and <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20w"/> be the shape of <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20x"/>, so <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5C%7Cx%5C%7C%20%3D%20chw"/>
First all the values are squared (<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20chw"/> FLOPs).
Then it is integrated among the channel axis
(<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%28c%20-%201%29hw"/> FLOPs).
Sum of a local response for a value can be calculated by a subtraction
(in total <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20chw"/> FLOPs).
Then elementwise multiplication of <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5Calpha"/>, addition of <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20k"/> and
power by <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5Cbeta"/> are conducted (<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%203chw"/> FLOPs, or <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%202chw"/> if
`fma_1flop` is set to `True`, as <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%5Calpha"/> and <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20k"/> can be done by FMA).

In total, FLOPs will be sum of them,
<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20chw%20%2B%20%28c-1%29hw%20%2B%20chw%20%2B%203chw%20%3D%3D%20%286c-1%29hw"/> FLOPs with no-FMA and
<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20%285c-1%29hw"/> with FMA.

| Item          | Value |
|:--------------|:------|
| FLOPs(FMA)    | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%285c-1%29hw%20"/> |
| FLOPs(no-FMA) | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%286c-1%29hw%20"/> |
| mread         | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20chw%20%3D%3D%20%5C%7C%20x%20%5C%7C%20"/> |
| mwrite        | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20chw%20%3D%3D%20%5C%7C%20x%20%5C%7C%20"/> |
| params        | `n`, `k`, `alpha` and `beta` |


## Pooling

### [AveragePooling2D](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.average_pooling_2d.html)

Each output pixel is calculated by averaging <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20k%20%2A%20k"/> elements from the
input (<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20k%2Ak"/> FLOPs). Output size is calculated by
[chainer.utils.get_conv_outsize](https://docs.chainer.org/en/v4.3.0/reference/util/generated/chainer.utils.get_conv_outsize.html).

| Item   | Value |
|:-------|:------|
| FLOPs  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5C%7C%20y%20%5C%7C%20k_%7B%5Cmathrm%7Bw%7D%7D%20k_%7B%5Cmathrm%7Bh%7D%7D%20"/> |
| mread  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> |
| mwrite | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20y%20%5C%7C"/> |
| params | AvgPooling parameter `k`, `s` and `p` |


### [MaxPooling2D](https://docs.chainer.org/en/v4.3.0/reference/generated/chainer.functions.max_pooling_2d.html)

Each output pixel is calculated by taking max of <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20k%20%2A%20k"/> elements from the
input (<img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B100%7D%20%5Cnormal%20k%2Ak%20-%201"/> FLOPs). Output size is calculated by
[chainer.utils.get_conv_outsize](https://docs.chainer.org/en/v4.3.0/reference/util/generated/chainer.utils.get_conv_outsize.html).

| Item   | Value |
|:-------|:------|
| FLOPs  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%20%5C%7C%20y%20%5C%7C%20%28k_%7B%5Cmathrm%7Bw%7D%7D%20k_%7B%5Cmathrm%7Bh%7D%7D%20-%201%29%20"/> |
| mread  | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20x%20%5C%7C"/> |
| mwrite | <img src="https://latex.codecogs.com/png.latex?%5Cdpi%7B130%7D%20%5Cnormal%20%5C%7C%20y%20%5C%7C"/> |
| params | AvgPooling parameter `k`, `s` and `p` |
