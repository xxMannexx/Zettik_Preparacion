import math
print(f"{'n':>10} {'O(log n)':>10} {'O(n)':>14} {'O(n log n)':>16} {'O(n^2)':>20}")
for n in [10, 1000, 100000, 1000000]:
    print(f"{n:>10} {math.log2(n):>10.0f} {n:>14,} {n*math.log2(n):>16,.0f} {n**2:>20,}")
# Se observa la divergencia: O(n^2) explota mientras O(n) y O(log n) crecen modestamente.
