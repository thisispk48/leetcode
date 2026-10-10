# 0167. Two Sum II - Input Array Is Sorted

* **LeetCode Link**: [167. Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
* **Difficulty**: Medium
* **Phase**: 1 (Foundations)
* **Category**: 01. Arrays, Two Pointers & Prefix Sums
* **Primary Concepts**: Converging Two Pointers, Monotonicity Invariant, Space Optimization (O(1) Memory)

---

## 1. Problem Statement

Given a **1-indexed** array of integers `numbers` that is already **sorted in non-decreasing order**, find two numbers such that they add up to a specific `target` number.

Return the indices of the two numbers, `index1` and `index2`, added by one as an integer array `[index1, index2]` of length 2.

The tests are generated such that there is **exactly one solution**. You may not use the same element twice.

Your solution must use only **constant extra space O(1)**.

### Constraints
* `2 <= numbers.length <= 3 * 10^4`
* `-1000 <= numbers[i] <= 1000`
* `numbers` is sorted in **non-decreasing order**.
* `-1000 <= target <= 1000`
* Only one valid answer exists.

---

## 2. MySolution Analysis & Verdict

### Praveen's Submission
```python
class MySolution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left = 0
        right = len(numbers) - 1
        while left < right:
            mid = int((left + right) / 2)
            if numbers[left] + numbers[right] == target:
                return [left, right]
            elif mid <= target:
                right = mid
                continue
            elif target <= mid:
                left = mid
                continue
        return []
```

### Diagnosis
1. **Strengths:** 
   * Immediately recognized that the array is sorted and established converging boundary pointers: `left = 0`, `right = len(numbers) - 1`.
   * Formulated the correct termination condition: `numbers[left] + numbers[right] == target`.
   * Successfully recognized that the search space could be contracted from the boundaries inward without allocating auxiliary memory (`O(1)` space).
2. **Bugs / Pitfalls Diagnosed:**
   * **Index vs. Value Comparison:** Compared the array index `mid` directly against the target sum `target` (`mid <= target`), mixing up index position with element values.
   * **Pointer Step Assignment:** Attempted to jump pointers to `mid` instead of checking whether the boundary sum `numbers[left] + numbers[right]` was too small or too large.
   * **1-Indexed Return:** The problem requires 1-based indexing, requiring `+ 1` on return.

### The Verdict
> **`MySolution` conceptually targeted the optimal `V3 (Converging Two Pointers)` archetype directly**, skipping the inferior $O(N^2)$ brute-force and $O(N \log N)$ binary search approaches. Fixing the pointer step condition and index adjustment brings it straight to the optimal solution (**3 ms / Beats 87.6%**).

---

## 3. Python Flow (The Evolutionary Ladder)

### Summary Evolution Table

| Version | Implementation | Time | Memory | Core Rationale |
| :---: | :--- | :---: | :---: | :--- |
| **V1** | Upper-Triangular Brute Force | `O(N^2)` | `O(1)` | Scans all pairs; ignores sorted order completely (causes **TLE** on LeetCode with ~450M operations). |
| **V2** | Binary Search for Complement | `O(N log N)` | `O(1)` | Exploits sorted order via bisection search for `target - numbers[i]`. |
| **V3** | Converging Two Pointers (Optimal) | `O(N)` | `O(1)` | Monotonic boundary contraction: shrinks search space by one element per step (**3 ms / Beats 87.6%**). |

---

### Nuances & Step-by-Step Python Evolution

#### V1: Upper-Triangular Brute Force
* **Logic:** Standard nested loops checking all `(i, j)` where `j > i`.
* **Bottleneck:** Fails to utilize the sorted property of the input array.
* **Operation Count:** `N * (N - 1) / 2`. For `N = 30,000`, this requires up to **450,000,000 operations**, immediately triggering **Time Limit Exceeded (TLE)**.

#### V1 ➔ V2: Transform-and-Conquer (Binary Search per Element)
* **What Changed:** Instead of a linear scan for the complement, we perform a Binary Search (`low, high, mid`) on the remaining subarray `numbers[i + 1 .. N - 1]`.
* **Why:** The array is sorted! Any lookup in a sorted 1D array can be done in `O(log N)` time.
* **Complexity:** `N` elements each triggering an `O(log N)` search $\implies$ `O(N log N)` time, `O(1)` space.
* **Limitation:** While it passes within time limits, it restarts a search from scratch on every iteration.

#### V2 ➔ V3: Converging Two Pointers (Optimal)
* **What Changed:** Eliminate the inner binary search loop completely. Compare the sum of the two extreme boundaries directly against the target:
  ```python
  current_sum = numbers[left] + numbers[right]
  ```
* **The Monotonic Invariant:**
  * **If `current_sum == target`:** Match found! Return `[left + 1, right + 1]`.
  * **If `current_sum < target` (Too Small):** Because `numbers[right]` is already the largest element available, pairing `numbers[left]` with any other element yields an even smaller sum. Thus, `numbers[left]` can never participate $\implies$ advance `left += 1`.
  * **If `current_sum > target` (Too Big):** By symmetric reasoning, `numbers[right]` cannot participate $\implies$ retreat `right -= 1`.
* **Result:** Blazing fast **3 ms / Beats 87.64%** on LeetCode Medium!

---

## 4. C++ Flow

### Summary Systems Table

| Version | Implementation | Time | Memory | Systems / Memory Rationale |
| :---: | :--- | :---: | :--- | :--- |
| **V1** | Upper-Triangular Brute Force | `O(N^2)` | `O(1)` | Nested loops scanning vector; cache misses and TLE. |
| **V2** | Binary Search per Element | `O(N log N)` | `O(1)` | Repeated bisection on contiguous vector using index arithmetic. |
| **V3** | Converging Two Pointers | `O(N)` | `O(1)` | Zero-copy pass by reference, bidirectional cache streaming, zero heap allocations (**0 ms / Beats 100%**). |

---

### Nuances & Systems Deep Dive in C++

#### Nuance 1: Zero-Copy Argument Passing (`const std::vector<int>&`)
* Input vector has up to 30,000 integers (`~120 KB`).
* Passing `twoSum(std::vector<int> numbers)` by value forces C++ to allocate memory and copy all 30,000 integers.
* **Systems Fix:** `const std::vector<int>& numbers` passes the reference directly, guaranteeing `O(1)` argument overhead.

#### Nuance 2: Cache Locality & Hardware Prefetching
* In V3, `left` moves forward (`0 -> 1 -> 2 ...`) while `right` moves backward (`N-1 -> N-2 ...`).
* Because `std::vector<int>` stores elements contiguously in physical RAM, the CPU hardware prefetcher loads sequential cache lines into L1 cache ahead of time.
* Unlike hash map lookups (which hop across fragmented memory buckets), the Two Pointer approach streams memory linearly with near-zero cache miss penalties.

#### Nuance 3: Integer Overflow Prevention in Midpoint Calculation
* When calculating midpoint:
  ```cpp
  int mid = low + (high - low) / 2; // Safe: never overflows 32-bit signed int
  ```
* Writing `(low + high) / 2` risks 32-bit signed integer overflow when indices approach $2 \times 10^9$.

---

## 5. Parity Audit (`solution.py` ⟷ `solution.cpp`)

| Evolutionary Step | `solution.py` Class | `solution.cpp` Class | Parity Status | Implementation Notes |
| :--- | :--- | :--- | :---: | :--- |
| **Praveen's Submission** | `MySolution` | `MySolution` | ✅ Exact Parity | Initial midpoint bisection attempt with index comparison. |
| **V1: Brute Force** | `SolutionV1_BruteForce` | `SolutionV1_BruteForce` | ✅ Exact Parity | Upper-triangular nested loops ($O(N^2)$ baseline). |
| **V2: Binary Search** | `SolutionV2_BinarySearch` | `SolutionV2_BinarySearch` | ✅ Exact Parity | Bisection search for complement in remaining subarray ($O(N \log N)$). |
| **V3: Two Pointers Optimal** | `SolutionV3_TwoPointersOptimal` | `SolutionV3_TwoPointersOptimal` | ✅ Exact Parity | Optimal converging two pointers ($O(N)$ time, $O(1)$ space). |

---

## 6. Conclusions & Key Takeaways

1. **Monotonicity Destroys Time Complexity:**  
   In Problem 1 (Unsorted), we had to spend `O(N)` memory on a Hash Map to achieve `O(N)` time.  
   In Problem 2 (Sorted), the sorted invariant allows us to achieve `O(N)` time with **strictly `O(1)` memory**.
2. **Boundary Contraction Pattern:**  
   Whenever a dataset is sorted and you need to find a pair satisfying a sum/target constraint, **Converging Two Pointers** is the primary archetype.
3. **Space Complexity Clarification:**  
   "Constant extra space `O(1)`" measures auxiliary memory allocated by your algorithm, excluding the input data. Simple scalar variables (`left`, `right`, `current_sum`) satisfy this invariant completely.
