def bresenhams_line(x1, y1, x2, y2):
    ''' Bresenhams algorithm as described here:
    http://eduinf.waw.pl/inf/utils/002_roz/2008_06.php'''

    line = []
    #result = x if a > b else y
    kx = 1 if x1 <= x2 else -1
    ky = 1 if y1 <= y2 else -1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    x = x1
    y = y1
    line.append([x,y])
    #K06
    if(dx >= dy):
        #dx >> 1
        e = dx/2
        for i in range(0,dx):
            x = x+kx
            e = e - dy
            #K11
            if(e<0):
                y=y+ky
                e = e + dx
            line.append([x,y])
    #K16
    else:
        e = dy / 2
        for i in range(0,dy):
            y = y+kx
            e = e-dx
            if(e < 0):
                x = x+kx
                e = e+dy
            line.append[x,y]
    return line