# 0001. Two Sum

- **LeetCode Link**: [1. Two Sum](https://leetcode.com/problems/two-sum/)
- **Difficulty**: Easy
- **Phase**: 1 (Foundations)
- **Category**: 01. Arrays, Two Pointers & Prefix Sums
- **Primary Concepts**: Array indexing, Space-Time Trade-off, Hash tables, Pre-allocation

---

## 1. Problem Statement

Given an array of integers `nums` and an integer `target`, return *indices of the two numbers such that they add up to `target`*.

You may assume that each input would have **exactly one solution**, and you may not use the same element twice. You can return the answer in any order.

### Constraints
* $2 \le \text{nums.length} \le 10^4$
* $-10^9 \le \text{nums}[i] \le 10^9$
* $-10^9 \le \text{target} \le 10^9$
* Only one valid answer exists.

---

## 2. The 5-Step Evolutionary Engineering Chain

| Version | Implementation | Time | Memory | Core Rationale |
| :---: | :--- | :---: | :---: | :--- |
| **V1** | Cartesian Product Brute Force | `O(N^2)` | `O(1)` | Baseline intuition: checks all $N \times N$ pairs with `i != j` guard. |
| **V2** | Upper Triangular Pruning | `O(N^2)` | `O(1)` | Symmetrical pruning ($j > i$): drops checks by ~50% to $N(N-1)/2$. |
| **V3** | Two-Pass Hash Map | `O(N)` | `O(N)` | Space-Time trade-off: replaces inner `j` scan loop with $O(1)$ dictionary lookups. |
| **V4** | One-Pass Hash Map (Optimal) | `O(N)` | `O(N)` | Interleaves lookup and insertion: single loop, early exit, handles duplicates. |
| **V5** | Systems / Pre-allocated Buckets | `O(N)` | `O(N)` | C++ low-level optimization: `.reserve(N)` eliminates hash map rehashing. |

---

### Step-by-Step Breakdown

#### Step 1 $\to$ Step 2: Eliminating Commutative Symmetry
* **Bottleneck:** V1 checks $(i, j)$ and later checks $(j, i)$. Because addition is commutative ($A + B = B + A$), this performs 100% duplicate work.
* **Isolated Change:** Start the inner loop at `j = i + 1`.
* **Impact:** Cuts operations from $N^2$ down to $N(N-1)/2$. Eliminates the need for the `i != j` branch check since $j > i$ is guaranteed.

#### Step 2 $\to$ Step 3: Space-Time Trade-off
* **Bottleneck:** Finding the complement `target - nums[i]` requires walking through the remaining array with an $O(N)$ linear loop.
* **Isolated Change:** Allocate an auxiliary Hash Map (`dict` in Python, `std::unordered_map` in C++) storing `{value: index}`.
* **Impact:** Replaces the inner $O(N)$ scan loop with an $O(1)$ average-time bucket lookup. Drops total time from $O(N^2)$ to $O(N)$.

#### Step 3 $\to$ Step 4: Single Pass & Early Exit
* **Bottleneck:** V3 runs two full sequential passes (Pass 1 builds the entire dictionary, Pass 2 queries it). V3 also risks key-overwrite collisions on duplicates (e.g. `nums = [3, 3]`).
* **Isolated Change:** Query the dictionary for the complement *before* inserting the current number into the dictionary.
* **Impact:** Single pass. Enables early exit on the first valid pair. Solves duplicate keys naturally because the second instance finds the first instance already stored in history.

#### Step 4 $\to$ Step 5: Eliminating Rehashing in C++
* **Bottleneck:** In C++, default `std::unordered_map` starts with a small bucket count (e.g., 8). As elements are inserted, it dynamically allocates larger arrays on the heap and re-hashes every existing element.
* **Isolated Change:** Call `seen.reserve(nums.size())` up front.
* **Impact:** Allocates all buckets in a single heap operation. Zero runtime rehashing.

---

## 3. Python ➔ C++ Bridge Notes

### Memory Layout
* **Python:** Every integer is a `PyObject` (~28 bytes) allocated on the heap. A Python `dict` adds significant pointer and hash-entry overhead (~20 MB total memory on LeetCode).
* **C++:** Integers are compact 4-byte primitives (`sizeof(int) == 4`). Memory is stored contiguously on hardware cache lines (~10 MB total memory).

### Zero-Copy Arguments
* **Python:** Arguments are passed by object reference (lightweight pointer handles).
* **C++:** Always declare the input parameter as `const std::vector<int>& nums`. Omitting the `&` causes C++ to deep-copy the entire array into the function frame, wasting $O(N)$ time and memory.

### Map Operations
| Concept | Python (`dict`) | C++ (`std::unordered_map`) |
| :--- | :--- | :--- |
| **Lookup** | `complement in seen` | `seen.find(complement) != seen.end()` |
| **Insert** | `seen[n] = i` | `seen.emplace(n, i)` or `seen[n] = i` |
| **Pre-allocation** | Not exposed in standard dict | `seen.reserve(N)` |
