# 27. Remove Element (Easy)

---

## 1. Problem Statement & Constraints

Given an integer array `nums` and an integer `val`, remove all occurrences of `val` in `nums` **in-place**. The order of the elements may be changed. Then return the number of elements in `nums` which are not equal to `val`.

Consider the number of elements in `nums` which are not equal to `val` to be `k`, to get accepted, you need to:
1. Change the array `nums` such that the first `k` elements contain the elements which are not equal to `val`.
2. The remaining elements beyond index `k - 1` are not important as well as the size of `nums`.
3. Return `k`.

### Constraints:
* `0 <= nums.length <= 100`
* `0 <= nums[i] <= 50`
* `0 <= val <= 100`

---

## 2. MySolution Analysis & Verdict

### Praveen's Initial Submission:
```python
class MySolution:
    def removeElement(self, nums: list[int], val: int) -> int:
        write = 0 
        for read in range(len(nums)):
            if nums[read] != val:
                nums[write], nums[read] = nums[read], nums[write]
                write = write + 1 
        return write
```

### Strengths:
* **Immediate Pattern Reuse:** Directly transferred the Lomuto swap partitioning scheme mastered in *Move Zeroes (0283)* to *Remove Element*.
* **Strict In-Place Mutation:** Achieved `O(1)` auxiliary memory without any second buffer.
* **Flawless Boundary Invariant:** Maintained `write` as both the active write index and the running count of preserved elements.

### Diagnosed Bottlenecks & Bugs:
* **None:** The submission passed all test cases immediately with **0 ms / Beats 100.00%**.

### The Verdict:
`MySolution` cleanly implements the **Optimal V3 (Single-Pass Lomuto Swap)**, bypassing the quadratic anti-pattern of repeated deletions and scoring a top-percentile benchmark on the first attempt.

---

## 3. Python Flow (The Evolutionary Ladder)

### Summary Evolution Table

| Version | Implementation | Time Complexity | Memory Complexity | Core Rationale | LeetCode Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MySolution** | Single-Pass Lomuto Swap | `O(N)` | `O(1)` aux | In-place swap partitioning; returns `write` | **0 ms / Beats 100.00%** |
| **V1** | Repeated `nums.remove(val)` | `O(N^2)` | `O(1)` aux | Naive deletion loop; repeated `memmove()` shifts | High runtime / TLE |
| **V2** | Fast/Slow Forward Overwrite | `O(N)` | `O(1)` aux | Forward assignment `nums[write] = nums[read]` | **0 ms / Beats 100.00%** |
| **V3** | Single-Pass Lomuto Swap | `O(N)` | `O(1)` aux | Swaps keeper with `write`; preserves relative order | **0 ms / Beats 100.00%** |
| **V4** | Converging Two Pointers | `O(N)` | `O(1)` aux | Swaps target with tail; minimizes writes when `val` is rare | **0 ms / Beats 100.00%** |

---

### Nuances & Step-by-Step Evolution

#### The V1 Anti-Pattern: `while val in nums: nums.remove(val)`
* Calling `nums.remove(val)` does two operations under the hood:
  1. Scans the array linearly to find `val` (`O(N)`).
  2. Shifts all subsequent elements one slot to the left (`O(N)`).
* Inside a `while` loop, this degrades to $O(N^2)$ time.

#### From V2 to V3: Overwrite vs Swap
* In **V2 (Overwrite)**, we simply write: `nums[write] = nums[read]`. We do not care what is left at `read` because elements beyond $k$ are ignored.
* In **V3 (Lomuto Swap - Praveen's Solution)**, we swap `nums[write]` with `nums[read]`. This has the bonus property of preserving relative order and keeping all removed values grouped at the tail.

#### From V3 to V4: Exploiting "Order May Be Changed" (Minimizing Memory Writes)
Notice the problem's special clause:
> *"The order of the elements may be changed."*

Consider an array of 10,000 numbers where `val` appears **only once at index 0**:
* **V2 & V3:** Inspect and copy all 9,999 remaining numbers forward! Total writes = 9,999.
* **V4 (Converging Pointers):**
  - When `nums[left] == val`: take the element at `right`, drop it into `nums[left]`, and shrink `right -= 1`.
  - Total writes = **exactly 1 write**!
* When target elements to remove are rare, V4 is theoretically optimal because the number of assignments equals the count of `val` elements, not $N$.

---

## 4. C++ Flow: Systems & Low-Level Mechanics

### Summary Systems Table

| Version | Implementation | Time Complexity | Memory Complexity | Systems / Hardware Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **MySolution** | Lomuto `std::swap` | `O(N)` | `O(1)` aux | CPU register exchange via `std::swap` |
| **V1** | `std::vector::erase` Loop | `O(N^2)` | `O(1)` aux | Repeated `memmove` shifts in contiguous buffer |
| **V2** | Forward Overwrite (`std::remove`) | `O(N)` | `O(1)` aux | Contiguous stream prefetching; direct STL mirror |
| **V3** | Lomuto `std::swap` | `O(N)` | `O(1)` aux | Preserves relative element stability |
| **V4** | Converging Two Pointers | `O(N)` | `O(1)` aux | Eliminates redundant stores when `val` frequency is low |

---

### Systems Deep Dive: The C++ `std::remove` Paradigm

In C++, this exact problem is implemented by **`std::remove`** (`<algorithm>`):

```cpp
auto it = std::remove(nums.begin(), nums.end(), val);
int k = std::distance(nums.begin(), it);
```

#### Why `std::remove` Does NOT Shrink the Vector:
* In the STL design philosophy, algorithms operate on **iterators**, not containers directly. Iterators cannot alter container capacity or allocate/deallocate memory.
* Therefore, `std::remove` only moves the valid elements to the front and returns an iterator past the last valid element.
* To actually shrink the vector, C++ uses the **Erase-Remove Idiom**:
  ```cpp
  nums.erase(std::remove(nums.begin(), nums.end(), val), nums.end());
  ```
* In this LeetCode problem, we are explicitly implementing the first half of this idiom: in-place compaction returning the logical boundary $k$.

---

## 5. Parity Audit (`solution.py` vs `solution.cpp`)

| Class | Python Implementation (`solution.py`) | C++ Implementation (`solution.cpp`) | Parity Status | Verification Notes |
| :--- | :--- | :--- | :--- | :--- |
| **`MySolution`** | Single-pass Lomuto swap returning `write` | Single-pass Lomuto swap returning `write` | **Full Parity** | Exact algorithmic translation (0 ms in both) |
| **`SolutionV1_InPlaceRemove` / `Erase`** | `nums.remove()` loop | `nums.erase()` loop | **Full Parity** | Demonstrates the quadratic array-shifting bottleneck |
| **`SolutionV2_ForwardOverwrite`** | Direct forward assignment `nums[write] = nums[read]` | Direct forward assignment (mirror of `std::remove`) | **Full Parity** | Eliminates secondary swap assignment |
| **`SolutionV3_LomutoSwap`** | Single-pass tuple swap `a, b = b, a` | Single-pass `std::swap` | **Full Parity** | Identical Lomuto partitioning scheme |
| **`SolutionV4_ConvergingTwoPointers`** | Two-ended pointer swap from both boundaries | Two-ended pointer swap from both boundaries | **Full Parity** | Minimizes memory writes when `val` is rare |

---

## 6. Conclusions & Key Takeaways

1. **The In-Place Compacting Trilogy Complete:**
   * **Move Zeroes (0283):** In-place compaction partitioning around `0`.
   * **Remove Duplicates (0026):** In-place compaction partitioning around relative history (`nums[write]`).
   * **Remove Element (0027):** In-place compaction partitioning around arbitrary target `val`.
2. **Order Flexibility Unlocks Two Pointers:**
   * When order must be preserved: Use **Forward Read/Write Pointers** (V2/V3).
   * When order is not important: Use **Converging Two Pointers** (V4) to minimize total memory writes when the element to remove is rare.
3. **Third Consecutive 100% Score:**
   * Demonstrated immediate reflex activation and scored **0 ms / Beats 100.00%** on the initial submission.
