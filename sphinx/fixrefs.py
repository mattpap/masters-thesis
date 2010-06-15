#!/usr/bin/env python

import sys

INPUT = sys.argv[1]

with open(INPUT) as f:
    s = f.read()

i = -1

while 1:
    i = s.find('\\hypertarget', i+1)

    if i == -1:
        break

    a = s.find('{', i)
    b = s.find('}', i)

    ref = s[a+1:b]

    j = b + 1
    cnt = 0

    while 1:
        if s[j] == '}':
            cnt -= 1

            if not cnt:
                break
        elif s[j] == '{':
            cnt += 1

        j += 1

    if s[j+1:j+15] != '\\begin{figure}':
        continue

    k = s.find('\\caption', i)

    if k == -1:
        continue

    cnt = 0

    while 1:
        if s[k] == '}':
            cnt -= 1

            if not cnt:
                break
        elif s[k] == '{':
            cnt += 1

        k += 1

    s = s[:k] + ('\\label{%s}' % ref) + s[k:]
    s = s[:i] + s[j+1:]

i = -1

while 1:
    i = s.find('\\hyperlink', i+1)

    if i == -1:
        break

    a = s.find('{', i)
    b = s.find('}', i)

    ref = s[a+1:b]

    j = b + 1
    cnt = 0

    while 1:
        if s[j] == '}':
            cnt -= 1

            if not cnt:
                break
        elif s[j] == '{':
            cnt += 1

        j += 1

    s = s[:i] + ('\\ref{%s}' % ref) + s[j+1:]

i = -1

while 1:
    i = s.find('\\hypertarget', i+1)

    if i == -1:
        break

    a = s.find('{', i)
    b = s.find('}', i)

    ref = s[a+1:b]

    j = b + 1
    cnt = 0

    while 1:
        if s[j] == '}':
            cnt -= 1

            if not cnt:
                break
        elif s[j] == '{':
            cnt += 1

        j += 1

    if ref.find('--doc-src') != -1:
        s = s[:i] + s[j+1:]
        continue

    while 1:
        if s[j+1] == '\\':
            break
        else:
            j += 1

    if s[j+1:j+10] != '\\chapter{' and s[j+1:j+10] != '\\section{' and s[j+1:j+13] != '\\subsection{' and s[j+1:j+16] != '\\subsubsection{':
        continue

    k = j + 1
    cnt = 0

    while 1:
        if s[k] == '}':
            cnt -= 1

            if not cnt:
                break
        elif s[k] == '{':
            cnt += 1

        k += 1

    s = s[:k+1] + ('\\label{%s}' % ref) + s[k+1:]
    s = s[:i] + s[j+1:]

with open(INPUT, 'w') as f:
    f.write(s)

