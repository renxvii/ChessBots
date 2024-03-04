import pickle

def make_grid():
    grid = []       
    a = []
    b = [1.0]
    c = []
    d = []
    e = [1.0]
    f = [1.0]
    for i in range(13):
        for j in range(13):
            for k in range(13):
                for l in range(13):
                    for m in range(13):
                        for n in range(13):
                            for o in range(13):
                                f.append(1.0)
                            e.append(f)
                        d.append(e)
                    c.append(d)
                b.append(c)
            a.append(b)
        grid.append(a)
    gridsigns = []
    b = []
    c = []
    d = []
    for i in range(8):
        for j in range(8):
            for k in range(8):
                for l in range(8):
                    d.append(1.0)
                c.append(d)
            b.append(c)
        gridsigns.append(b)
    outfile = open('pokergrid','wb')
    pickle.dump(grid,outfile)
    outfile.close

    outfile = open('pokersuits','wb')
    pickle.dump(gridsigns,outfile)
    outfile.close
make_grid()
            
