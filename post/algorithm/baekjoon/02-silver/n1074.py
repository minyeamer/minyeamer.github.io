def z_order(n, y, x, idx):
    if n < 1:
        return idx
    end = 2**n
    mid = end//2
    quad_idx = (end**2)//4

    if y < mid:
        if x < mid:
            return z_order(n-1, y, x, idx-quad_idx*3)
        else:
            return z_order(n-1, y, x-mid, idx-quad_idx*2)
    else:
        if x < mid:
            return z_order(n-1, y-mid, x, idx-quad_idx)
        else:
            return z_order(n-1, y-mid, x-mid, idx)


N, r, c = map(int, input().split())
print(z_order(N, r, c, ((2**N)**2)-1))
