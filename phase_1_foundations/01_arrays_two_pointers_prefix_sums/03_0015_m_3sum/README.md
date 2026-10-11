# 15. 3Sum (Medium)

---

## 1. Problem Statement & Constraints

Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that:
* `i != j`, `i != k`, and `j != k`
* `nums[i] + nums[j] + nums[k] == 0`

**Constraint:** The solution set must **not** contain duplicate triplets.

### Constraints:
* `3 <= nums.length <= 3000`
* `-10^5 <= nums[i] <= 10^5`

---

## 2. MySolution Analysis & Verdict

### Praveen's Initial Submission:
```python
class MySolution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        triplets = []
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                for k in range(j + 1, len(nums)):
                    if (i != j) and (j != k) and (i != k) and (nums[i] + nums[j] + nums[k] == 0):
                        triplets.append([nums[i], nums[j], nums[k]])
        return triplets
```

### Strengths:
* **Strict Index Ordering:** By initializing `j = i + 1` and `k = j + 1`, the loop ranges naturally enforce `i < j < k`.
* **Zero Premature Assumptions:** Built directly on the first principles of combination generation: evaluating all triples from the power set.

### Diagnosed Bottlenecks & Bugs:
1. **The Duplicate Triplet Bug:**
   * Having unique indices does not guarantee unique values.
   * If `nums = [-1, 0, 1, 2, -1, -4]`, index combinations `(0, 1, 2)` and `(1, 2, 4)` both evaluate to triplets with elements `{-1, 0, 1}`. Without canonical normalization, identical triplets are appended multiple times.
2. **Cubic Computational Complexity:**
   * Checks `C(N, 3) = N * (N - 1) * (N - 2) / 6` combinations.
   * For `N = 3000`, this evaluates to `~4.5 * 10^9` loop iterations, triggering an immediate **Time Limit Exceeded (TLE)**.
3. **Redundant Conditionals:**
   * `(i != j) and (j != k) and (i != k)` is strictly redundant because `i < j < k` is already guaranteed by the loop index progression.

### The Verdict:
`MySolution` cleanly implements the raw **V1 (Brute Force Combinations)** baseline, but fails on LeetCode due to missing deduplication and cubic runtime.

---

## 3. Python Flow (The Evolutionary Ladder)

### Summary Evolution Table

| Version | Implementation | Time Complexity | Memory Complexity | Core Rationale | LeetCode Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MySolution** | 3-Loop Combination Scan | `O(N^3)` | `O(1)` aux | Naive baseline; no deduplication | Fails (Duplicates + TLE) |
| **V1** | 3 Loops + Set of Sorted Tuples | `O(N^3)` | `O(K)` set | Normalizes trios to canonical form `(a, b, c)` with `a <= b <= c` | TLE (`~4.5 * 10^9` ops) |
| **V2** | Pivot `i` + Inner Hash Set | `O(N^2)` | `O(N)` aux | Space-Time Trade-off (Two Sum lookup for `-nums[i] - nums[j]`) | Slow / TLE (`~2500 ms`) |
| **V3** | Presorting + Two Pointers | `O(N^2)` | `O(1)` aux | Transform-and-Conquer: In-place two pointers + symmetric skip | **474 ms / Beats 92.90%** |

---

### Nuances & Step-by-Step Evolution

#### From MySolution to V1: Canonical Normalization (Why Tuples?)
* In Python, `list` is mutable and lacks a hash function (`__hash__ = None`). You cannot insert a `list` into a `set()`.
* A `tuple` is immutable and hashable, but tuple equality is **positional/ordered**: `(-1, 0, 1) != (0, 1, -1)`.
* Therefore, sorting the 3 numbers creates a **canonical form**: `tuple(sorted([a, b, c]))`. Both permutations map to `(-1, 0, 1)`, allowing `set.add()` to filter duplicates.

#### From V1 to V2: Space-Time Trade-off (The Two Sum Reduction)
* Rewriting the identity: `nums[j] + nums[k] == -nums[i]`.
* Fixing `nums[i]` reduces the inner search to **Two Sum (0001)** targeting `complement = -nums[i] - nums[j]`.
* An inner `seen = set()` eliminates the third nested loop, cutting time from `O(N^3)` to `O(N^2)`.
* **Bottleneck:** Allocating 3,000 hash tables on the heap and continuously sorting 3-tuples causes severe memory churn in Python (`~2,500 ms` or TLE).

#### From V2 to V3: Transform-and-Conquer Presorting (The Optimal Leap)
* Sorting the array once (`nums.sort()`) takes `O(N log N)`, which is dominated by `O(N^2)`.
* **Infinite Loop Trap:** When `nums[i] + nums[left] + nums[right] == 0`, pointers `left` and `right` must both advance (`left += 1`, `right -= 1`). Failing to move them creates an infinite loop that crashes with **Memory Limit Exceeded (MLE)**.
* **Symmetric Duplicate Pruning:**
  - Outer Pivot: `if i > 0 and nums[i] == nums[i - 1]: continue`
  - Left Pointer: `while left < right and nums[left] == nums[left - 1]: left += 1`
  - Right Pointer: `while left < right and nums[right] == nums[right + 1]: right -= 1`
* **Early Pruning:** If `nums[i] > 0`, break immediately because 3 positive numbers in a non-decreasing array can never sum to zero.

---

## 4. C++ Flow: Systems & Low-Level Mechanics

### Summary Systems Table

| Version | Implementation | Time Complexity | Memory Complexity | Systems / Memory Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **MySolution** | 3-Loop Scan | `O(N^3)` | `O(1)` aux | Direct translation of raw baseline |
| **V1** | 3 Loops + `std::set` | `O(N^3 log K)` | `O(K)` heap | Red-black tree node allocations per triplet insert |
| **V2** | Pivot + `std::unordered_set` | `O(N^2)` | `O(N)` heap | Hash table rehashing per pivot; free-store churn |
| **V3** | `std::sort` + Two Pointers | `O(N^2)` | `O(1)` aux | Cache-line streaming, branch pruning, zero heap churn |
| **V4** | Systems Tuned (`reserve`) | `O(N^2)` | `O(1)` aux | Pre-allocated vector capacity, zero reallocations |

---

### Systems Deep Dive: Why C++ Runs This 15x Faster

```text
Python Memory Layout:
List -> [ PyObject* -> 28-byte int, PyObject* -> 28-byte int, ... ]  (Pointer chasing, cache misses)

C++ Memory Layout:
std::vector<int> -> [ 4-byte int ][ 4-byte int ][ 4-byte int ]...     (Contiguous cache lines)
```

1. **Hardware Cache Locality:**
   * In C++, `std::sort` and two-pointer traversal stream contiguous 4-byte integers across CPU cache lines (64 bytes = 16 integers per L1 line).
   * Spatial prefetching results in near 100% L1/L2 cache hit rates.
2. **Eliminating Heap Node Allocations:**
   * In V1/V2, `std::set` (Red-Black Tree) allocates a new 32-to-48-byte heap node for every unique triplet.
   * V3 operates strictly in `O(1)` auxiliary space on the existing memory buffer, executing in **~30 ms** on LeetCode.
3. **Branch Prediction & Heuristic Capacity:**
   * The condition `if (nums[i] > 0) break;` provides a predictable branch for modern speculative execution units.
   * `results.reserve(...)` in V4 eliminates multiple vector exponential re-allocations (`doubling strategy: 1 -> 2 -> 4 -> 8...`).

---

## 5. Parity Audit (`solution.py` vs `solution.cpp`)

| Class | Python Implementation (`solution.py`) | C++ Implementation (`solution.cpp`) | Parity Status | Verification Notes |
| :--- | :--- | :--- | :--- | :--- |
| **`MySolution`** | 3-loop combination check with redundant conditionals | 3-loop combination check with redundant conditionals | **Full Parity** | Exact bug preservation (duplicate triplets, cubic runtime) |
| **`SolutionV1_BruteForceSet`** | 3 loops + sorted tuples into `set()` | 3 loops + sorted vectors into `std::set` | **Full Parity** | Red-black tree node insertion mirrors Python hash set deduplication |
| **`SolutionV2_HashSet`** | Fixed pivot `i` + inner Two Sum `set()` | Fixed pivot `i` + `std::unordered_set<int>` | **Full Parity** | Both implement Space-Time Trade-off Two Sum lookup on suffix |
| **`SolutionV3_TwoPointers`** | `nums.sort()` + Two Pointers + symmetric skips | `std::sort()` + Two Pointers + symmetric skips | **Full Parity** | Identical invariant enforcement, branch pruning, and pointer advancement |
| **`SolutionV4_SystemsOptimized`** | *(N/A - Python uses dynamic lists)* | Capacity heuristic via `.reserve()` + local value caching | **C++ Extension** | Low-level systems tuning to eliminate vector heap re-allocation doubling |

---

## 6. Conclusions & Key Takeaways

1. **Presorting is Not Cheating (Transform-and-Conquer):**
   * Pre-processing unsorted data with an `O(N log N)` sort is a fundamental algorithmic design strategy when the subsequent phase takes `O(N^2)`.
   * The sort adds **zero asymptotic cost** while reducing auxiliary space from `O(N)` to `O(1)`.
2. **The Invariant of Duplicate Skipping:**
   * The first occurrence of a duplicate element (e.g. at index `i`) must be processed so it can pair with other duplicates via `left`.
   * Subsequent identical pivots are strictly redundant subsets and must be skipped.
3. **The Sum Trilogy Complete:**
   * **Two Sum (0001):** Hash map Space-Time Trade-off on unsorted input (`O(N)` time, `O(N)` space).
   * **Two Sum II (0167):** Two Pointers on sorted input (`O(N)` time, `O(1)` space).
   * **3Sum (0015):** Transform-and-Conquer Presorting + Fixed Pivot + Two Sum II (`O(N^2)` time, `O(1)` space).
