import pickle

def make_grid():
    grid = []       
    f = []
    for i in range(95):
        for o in range(700):
            m = (i + 500)*(1100/(1000 + o))/540
            f.append([0.0,m ** 0.4,0.0,0.0,m**0.7,m**0.8,m])
        grid.append(f)
    gridsigns = []
    b = []
    c = []
    d = []
    for i in range(8):
        for j in range(4):
            for k in range(3):
                for l in range(2):
                    d.append(1.0)
                c.append(d)
            b.append(c)
        gridsigns.append(b)
    outfile = open('pokergrid2','wb')
    pickle.dump(grid,outfile)
    outfile.close

    outfile = open('pokersuits2','wb')
    pickle.dump(gridsigns,outfile)
    outfile.close
make_grid()
            
