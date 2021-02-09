import os

if os.path.isfile('genre_db2.csv'):
    os.remove('genre_db2.csv')

with open('genre_db.csv', 'r') as og:
    lines = []

    for line in og.readlines():
        if not line.startswith(';'):
            lines.append(line)

    with open('genre_db2.csv', 'a') as cp:
        for line in lines:
            cp.write(line)
