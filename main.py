from functools import reduce

import PIL.Image

print('----------')
file = input('Enter the file name you want to pixelate:')
print('----------')
strength = int(input('Set strength value for pixelation:'))
im = PIL.Image.open(file)
size = im.size
pixels = list(im.getdata())
pix = []
for i in range(size[1]):
    pix.append(pixels[i * size[0]:i * size[0] + size[0] // strength * strength])
pix = pix[:len(pix) // strength * strength]
pix = sum(pix, [])
size = tuple(map(lambda x: x // strength * strength, size))
newsize = tuple(map(lambda x: x // strength, size))
im2 = PIL.Image.new('RGB', newsize)
data = [[[] for _ in range(size[0] // strength)] for _ in range(size[1] // strength)]
for i in range(size[0] * size[1]):
    # x = i % size[0] // strength
    # y = i // size[0] // strength
    data[i // size[0] // strength][i % size[0] // strength].append(pix[i])
data = sum(data, [])
for index, i in enumerate(data):
    data[index] = tuple(reduce(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]), i))
    data[index] = tuple(list(map(lambda x: x // len(i), data[index])))
print('----------')
scale = int(input(f'Set the image size you want relative to 1/{strength} x original: '))
newdata, c, b = [], 0, []
for i in range(len(data) + 1):
    if i == len(data):
        c += 1
        b *= scale
        newdata.append(b)
        b = []
    elif c != i // newsize[0]:
        c += 1
        b *= scale
        newdata.append(b)
        b = []
        b += [data[i]] * scale
    elif i != len(data):
        b += [data[i]] * scale
newdata = sum(newdata, [])
newsize = tuple(map(lambda x: x * scale, newsize))
im2 = im2.resize(newsize)
im2.putdata(newdata)  # change {im2 size} relative to {newdata}
print('----------')
newfile = input('Give the new file a name (with extension):')
im2.save(newfile)
im.close()
im2.close()
