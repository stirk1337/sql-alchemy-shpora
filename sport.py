def two_numbers_have_equal_sign(a: int, b: int) -> bool:
    if a < 0 and b < 0:
        return True
    if a > 0 and b > 0:
        return True
    return False


def solve():
    n = int(input())
    a = list(map(int, input().split()))

    ans_sum = 0
    maximum_in_block = a[0]

    for i in range(1, n):
        if two_numbers_have_equal_sign(a[i], a[i - 1]):
            maximum_in_block = max(maximum_in_block, a[i])
        else:
            ans_sum += maximum_in_block
            maximum_in_block = a[i]

    ans_sum += maximum_in_block

    print(ans_sum)


for _ in range(int(input())):
    solve()
