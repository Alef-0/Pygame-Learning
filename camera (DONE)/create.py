from random import shuffle, randrange
from os import path
CWD = path.dirname(__file__)
 
def make_maze(w = 16, h = 8):
    vis = [[False] * w + [True] for _ in range(h)] + [[True] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]
 
    def walk(x, y):
        vis[y][x] = True
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]

        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+  "
            if yy == y: ver[y][max(x, xx)] = "   "
            walk(xx, yy)
        
 
    walk(randrange(w), randrange(h))
 
    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
        
    return s
 
def make_map(width=15,height=15):
    with open(path.join(CWD,"maze.txt"),"w") as f: f.write(make_maze(width,height))

if __name__=="__main__": print(make_maze(15,15))
