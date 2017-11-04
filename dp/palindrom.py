'''
Longest palindrom subsequence
'''

def palin_dp(s):
    # lookup(i, j) is longest palindrom starting on 'i' and ending on 'j'
    lookup = [[0 for i in range(len(s))] for i in range(len(s))]
    
    for i in range(len(s)):
        for j in range(len(s) - 1, i - 1, -1):
            lookup[i][j] = 1
    
    # end of string
    for j in range(1, len(s)):
        # start of string
        for i in range(j - 1, -1, -1):
            if (s[i] == s[j]):
                lookup[i][j] = 2 + lookup[i+1][j-1]
            else:
                lookup[i][j] = max(lookup[i+1][j], lookup[i][j-1])
    
    # solution for whole string
    return lookup[0][len(s)-1]

def p(i, j, s):
    # base case 1: dist(i, j) == 0
    if (i == j):
        return 1
    
    # base case 2: dist(i, j) == 1
    if (s[i] == s[j] and i + 1 == j):
        return 2

    if (s[i] == s[j]):
        return 2 + p(i+1, j-1, s)
    else:
        return max(p(i+1, j, s), p(i, j-1, s))

def palin(s):
    return p(0, len(s) - 1, s)

def p_memo(i, j, s, memo):
    if ((i, j) in memo):
        return memo[(i, j)]

    # base case 1: dist(i, j) == 0
    if (i == j):
        memo[(i, j)] = 1
        return memo[(i, j)]
    
    # base case 2: dist(i, j) == 1
    if (s[i] == s[j] and i + 1 == j):
        memo[(i, j)] = 2
        return memo[(i, j)]

    if (s[i] == s[j]):
        memo[(i, j)] = 2 + p_memo(i+1, j-1, s, memo)
    else:
        memo[(i, j)] = max(p_memo(i+1, j, s, memo), p_memo(i, j-1, s, memo))
    return memo[(i, j)]

def palin_m(s):
    return p_memo(0, len(s) - 1, s, {})

s1 = 'ABCCBA'
print('Expect 6')
print(palin(s1))
print(palin_m(s1))
print(palin_dp(s1))

s2 = 'ABCDCBA'
print('Expect 7')
print(palin(s2))
print(palin_m(s2))
print(palin_dp(s2))

s3 = 'ABCB'
print('Expect 3')
print(palin(s3))
print(palin_m(s3))
print(palin_dp(s3))

s4 = ' AABCDEBAZ'
print('Expect 5')
print(palin(s4))
print(palin_m(s4))
print(palin_dp(s4))

s5 = 'GEEKSFORGEEKS'
print('Expect 5')
print(palin(s5))
print(palin_m(s5))
print(palin_dp(s5))


s6 = 'akokafffewfelaaafewfewfafewfewfaaa'
print('Expect 19')
# print(palin(s6)) takes long, no memoization
print(palin_m(s6))
print(palin_dp(s6))

