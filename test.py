# -*- coding: utf-8 -*-

t = [
    (2.5, 1),
    (4, 1),
    (3, 1.7),
    (0.375, 3.1),
    (2, 2.5),
    (2, 2.3),
    (2, 4),
    (2, 3.8),
    (1.5, 4.2),
    (1, 4),
    (0.5, 4),
    (1, 2.7),
    (3, 3.1),
    (0.5, 4),
    (1, 3.6),
    (1, 3.9),

    (2, 3.6),
    (2.5, 2.4),
    (3, 2.9),
    (2, 4),
    (2, 3.2),
    (2.5, 3.4),
    (1.5, 4),
    (1, 4.5),
    (2, 3.8),
    (1, 3.2),
    (0.5, 4),
    (0.5, 4.4),
    (1, 3.8),
    (0.5, 4)
]

sum_a = sum([pair[0] for pair in t])
sum_b = sum([pair[0]*pair[1] for pair in t])
avg = float(sum_b) / sum_a

sum_c = sum([pair[1] * 10 + 50 for pair in t]) / len(t) * 1.0

print '平均绩点为: %s' % avg
print '平均成绩为: %s' % sum_c

import os
for parent,dirnames,filenames in os.walk('/Users/kangtian/Documents/Master/paper_plane/res/aiml-en-us-foundation-alice.v1-9'):
    for file_name in filenames:
        print '<learn>' + file_name +'</learn>'

