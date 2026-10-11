# 283. Move Zeroes (Easy)

---

## 1. Problem Statement & Constraints

Given an integer array `nums`, move all `0`'s to the end of it while maintaining the relative order of the non-zero elements.

**Constraints:**
* You must do this **in-place** without making a copy of the array.
* `1 <= nums.length <= 10^4`
* `-2^31 <= nums[i] <= 2^31 - 1`

**Follow up:** Could you minimize the total number of operations done?

---

## 2. MySolution Analysis & Verdict

### Praveen's Initial Submission:
```python
class MySolution:
    def moveZeroes(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        for i in range(len(nums)):
            for j in range(len(nums)):
                if nums[j] == 0 and nums[j + 1] != 0: 
                    temp = nums[j]
                    nums[j] = nums[j + 1]
                    nums[j + 1] = temp
```

### Strengths:
* **In-place Intuition:** Aims to solve the problem directly on the input array in `O(1)` auxiliary space without allocating a second buffer.
* **Bubble Sorting Analogy:** Correctly recognizes that zeros can be shifted to the tail by repeatedly swapping adjacent elements `(0, non-zero)`.

### Diagnosed Bottlenecks & Bugs:
1. **The Out-of-Bounds `IndexError` Bug:**
   * The inner loop runs `for j in range(len(nums)):`.
   * When `j = len(nums) - 1`, the expression `nums[j + 1]` attempts to access index `len(nums)`, immediately raising `IndexError: list index out of range`.
2. **Quadratic Time Complexity (`O(N^2)`):**
   * Two nested loops execute `N * N` times.
   * For the upper constraint `N = 10,000`, this requires `10^8` operations, which triggers **Time Limit Exceeded (TLE)** on LeetCode.

### The Verdict:
`MySolution` cleanly implements the core mental model of **V1 (Bubble Sort / Adjacent Swaps)**, but contains an off-by-one boundary bug on `nums[j + 1]` and suffers from quadratic runtime.

---

## 3. Python Flow (The Evolutionary Ladder)

### Summary Evolution Table

| Version | Implementation | Time Complexity | Memory Complexity | Core Rationale | LeetCode Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MySolution** | Adjacent Bubble Swaps | `O(N^2)` | `O(1)` aux | Naive nested loops with adjacent pairwise swapping | Fails (`IndexError` + TLE) |
| **V1** | Corrected Bounded Bubble Sort | `O(N^2)` | `O(1)` aux | Fixes inner bound to `N - 1 - i` with early break | TLE (`~10^8` ops) |
| **V2** | Two-Pass Overwrite & Zero Fill | `O(N)` | `O(1)` aux | Read/Write pointer compaction + trailing zero fill | Beats ~80% (`N` writes) |
| **V3** | Single-Pass Lomuto Swap | `O(N)` | `O(1)` aux | Swaps non-zero at `read` with `write`; zeros drift backward | **6 ms / Beats 45.14%** |
| **V4** | Lomuto Swap with Self-Swap Guard | `O(N)` | `O(1)` aux | Skips self-swaps when `write == read`; minimizes writes | **0 ms / Beats 100%** |

---

### Nuances & Step-by-Step Evolution

#### From MySolution to V1: Fixing the Loop Boundary
* In bubble sort, the inner loop must never exceed `len(nums) - 1 - i` so that `j + 1` remains strictly within bounds.
* Adding a `swapped` boolean allows early termination if the array becomes sorted early.
* However, quadratic time `O(N^2)` is fundamentally unviable for stream/array compacting.

#### From V1 to V2: The Read/Write Pointer Pattern (Archetype 2)
* We decouple reading from writing:
  * **`write_idx`:** Points to the destination slot where the next non-zero belongs.
  * **`read_idx`:** Scans every element from index `0` to `N - 1`.
* **Pass 1:** Whenever `nums[read_idx] != 0`, copy it forward: `nums[write_idx] = nums[read_idx]`, then `write_idx += 1`.
* **Pass 2:** Fill all remaining indices from `write_idx` to `N - 1` with `0`.
* **Complexity:** Exactly $2N$ operations $\to$ `O(N)` time and `O(1)` auxiliary memory.
* **Drawback:** Requires two passes across memory and performs $N$ total write operations.

#### From V2 to V3: Single-Pass Lomuto Partitioning
* Can we do everything in one pass?
* Instead of copying and zero-filling later, we **swap** `nums[write_idx]` with `nums[read_idx]`!
* When `nums[read_idx] != 0`:
  * Swap puts the non-zero value at `write_idx`.
  * The zero originally at `write_idx` is moved to `read_idx`.
  * As the scan progresses, all zeroes are automatically pushed backward behind `write_idx` in a single pass.

#### From V3 to V4: Answering the Follow-Up (Minimizing Operations)
* Consider `nums = [1, 2, 3, 0, 4]`.
* For the first three elements, `write_idx == read_idx`. Performing `nums[i], nums[i] = nums[i], nums[i]` performs redundant self-swaps!
* Adding a single guard:
  ```python
  if write_idx != read_idx:
      nums[write_idx], nums[read_idx] = nums[read_idx], nums[write_idx]
  ```
  completely eliminates unnecessary writes when leading non-zeros are already in place.

---

## 4. C++ Flow: Systems & Low-Level Mechanics

### Summary Systems Table

| Version | Implementation | Time Complexity | Memory Complexity | Systems / Hardware Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **MySolution** | Nested Loop Scan | `O(N^2)` | `O(1)` aux | Direct translation with boundary guard |
| **V1** | Bounded Bubble Sort | `O(N^2)` | `O(1)` aux | In-place pairwise swapping |
| **V2** | Two-Pass Read/Write | `O(N)` | `O(1)` aux | Forward stream overwrite; $N$ cache line write hits |
| **V3** | `std::swap` Lomuto | `O(N)` | `O(1)` aux | Single pass; hardware register register exchange |
| **V4** | Self-Swap Guarded | `O(N)` | `O(1)` aux | Prevents cache line dirtying under MESI coherence protocol |

---

### Systems Deep Dive: Cache Lines & The MESI Protocol

#### 1. Why Self-Swapping Hurts Multi-Core Hardware
In modern multi-core CPUs, cache lines (typically 64 bytes) follow the **MESI (Modified, Exclusive, Shared, Invalid)** coherence protocol:
* If an array is already partially packed (e.g. `[1, 2, 3, ...]`), reading `nums[i]` brings the cache line in as **Shared** or **Exclusive**.
* If you execute a redundant self-swap (`nums[i] = nums[i]`), the CPU's memory management unit marks the cache line as **Modified (Dirty)**!
* Marking a cache line as dirty forces the CPU to broadcast coherence invalidations across the interconnect and eventually write the cache line back to L3 or RAM, even though the data never changed!
* The `if (write_idx != read_idx)` guard in V4 keeps the cache line clean and avoids unnecessary bus traffic.

#### 2. Hardware Register Swapping
In C++, `std::swap(nums[write_idx], nums[read_idx])` on primitive `int`s is inlined by Clang/GCC directly into CPU register instructions:
```text
mov eax, dword ptr [rdi + rcx*4]   ; Load nums[read_idx] into register eax
mov edx, dword ptr [rdi + rsi*4]   ; Load nums[write_idx] into register edx
mov dword ptr [rdi + rsi*4], eax   ; Store to nums[write_idx]
mov dword ptr [rdi + rcx*4], edx   ; Store to nums[read_idx]
```
Zero heap allocation, zero stack frames, executing in **0 ms (Beats 100%)**.

---

## 5. Parity Audit (`solution.py` vs `solution.cpp`)

| Class | Python Implementation (`solution.py`) | C++ Implementation (`solution.cpp`) | Parity Status | Verification Notes |
| :--- | :--- | :--- | :--- | :--- |
| **`MySolution`** | Adjacent swap attempt with `IndexError` risk | Adjacent swap attempt with boundary guard | **Full Parity** | Preserves quadratic complexity and raw approach |
| **`SolutionV1_BubbleSort`** | Bounded bubble sort with `swapped` flag | Bounded bubble sort with `swapped` flag | **Full Parity** | Both implement identical early-exit bubble sort |
| **`SolutionV2_TwoPassOverwrite`** | Two-pass compact + trailing slice/loop zero-fill | Two-pass compact + trailing zero loop | **Full Parity** | Identical 2-pass structure and $N$ memory writes |
| **`SolutionV3_SinglePassSwap`** | Single-pass tuple swap `a, b = b, a` | Single-pass `std::swap` | **Full Parity** | Both implement textbook Lomuto partitioning |
| **`SolutionV4_OptimizedNoSelfSwap`** | Single-pass swap guarded by `write != read` | Single-pass `std::swap` guarded by `write != read` | **Full Parity** | Optimal implementation minimizing memory writes |

---

## 6. Conclusions & Key Takeaways

1. **Archetype 2 Unlocked: Fast & Slow (Read/Write) Pointers:**
   * This problem is the foundational blueprint for all in-place stream filtering algorithms (`removeElement`, `removeDuplicates`, NaN tensor sanitization).
   * Maintain a write boundary while a fast read pointer inspects the future stream.
2. **Lomuto Partitioning Generalization:**
   * Swapping non-zeros forward is identical to partitioning around a pivot `0` in QuickSort.
   * Turns a two-pass algorithm into a clean single-pass algorithm.
3. **Hardware-Aware Engineering:**
   * Avoiding redundant self-swaps (`write != read`) is not just an algorithmic detail; it directly preserves CPU cache line states under hardware coherence protocols.
