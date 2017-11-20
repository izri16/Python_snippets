from cmath import exp, pi
from numpy import fft


def closest_power_of_two(target):
    if target > 1:
        for i in range(1, int(target)):
            if (2 ** i >= target):
                return 2 ** i
    else:
        return 1

def number_to_vector(x):
    return [int(i) for i in reversed(str(x))]


def add_zeros(arr, max_len):
    ret = []
    N = len(arr)
    for i in range(max_len):
        if (i < N):
            ret.append(arr[i])
        else:
            ret.append(0)
    return ret


def fft_custom(x, inverse=False):
    N = len(x)
    if N <= 1: return x
    
    even = fft_custom(x[0::2], inverse)
    odd = fft_custom(x[1::2], inverse)
    
    sign = 1 if inverse else -1

    T= [exp(sign*2j*pi*k/N) for k in range(N)]

    half = N // 2
    return [even[k] + T[k]*odd[k] for k in range(half)] + \
            [even[k-half] + T[k]*odd[k-half] for k in range(half, N)]
                                                 

def ifft_custom(x):
    return [(item/len(x)) for item in fft_custom(x, inverse=True)]


arr = [1,1,1,1,0,0,0,0]
arr_f = fft_custom(arr)
print('Input array', arr)
print('FFT ...')
print(' '.join('%5.3f' % abs(item) for item in fft.fft(arr)))
print(' '.join('%5.3f' % abs(item) for item in arr_f))
print('IFFT ...')
print(' '.join('%5.3f' % abs(item) for item in fft.ifft(arr_f)))
print(' '.join('%5.3f' % abs(item) for item in ifft_custom(arr_f)))


# POLYNOMIAL MULTIPLICATION USING FFT
poly1 = [-7,3]
poly2 = [5, 8]

closest_exp = closest_power_of_two(len(poly1) * (len(poly2)))

poly1_z = add_zeros(poly1, closest_exp)
poly2_z = add_zeros(poly2, closest_exp)

f1 = fft_custom(poly1_z)
f2 = fft_custom(poly2_z)
f_mul = [f1[i] * f2[i] for i in range(len(f1))]

# for polynomial multiplication we want 'pure real part' not just 'abs'
print('\nPoly 1', poly1)
print('Poly 2', poly2)
print('Resulting polynomial (a_0, a_1, ...)')
print(' '.join('%5.3f' % item.real for item in ifft_custom(f_mul)))


# MULTIPLICATION OF POSITIVE INTEGERS USING FFT
# can be easily generalized to negative and real numbers
n1 = 124
n2 = 7845

n1_v = number_to_vector(n1)
n2_v = number_to_vector(n2)

closest_exp = closest_power_of_two(len(n1_v) * len(n2_v))
n1_z = add_zeros(n1_v, closest_exp)
n2_z = add_zeros(n2_v, closest_exp)

f1 = fft_custom(n1_z)
f2 = fft_custom(n2_z)
f_mul = [f1[i] * f2[i] for i in range(len(f1))]

real_part = [round(item.real) for item in ifft_custom(f_mul)]

res = []
carry = 0
for r in real_part:
    res.append(str((r + carry) % 10))
    carry = (r + carry) // 10

print('\n{} * {} = {}'.format(n1, n2, int(''.join(reversed(res)))))

