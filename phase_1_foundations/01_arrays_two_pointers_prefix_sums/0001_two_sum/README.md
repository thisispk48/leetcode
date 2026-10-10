# 0001. Two Sum

* **LeetCode Link**: [1. Two Sum](https://leetcode.com/problems/two-sum/)
* **Difficulty**: Easy
* **Phase**: 1 (Foundations)
* **Category**: 01. Arrays, Two Pointers & Prefix Sums
* **Primary Concepts**: Array Indexing, Space-Time Trade-off, Hash Tables, Memory Pre-allocation

---

## 1. Problem Statement

Given an array of integers `nums` and an integer `target`, return *indices of the two numbers such that they add up to `target`*.

You may assume that each input would have **exactly one solution**, and you may not use the same element twice. You can return the answer in any order.

### Constraints
* `2 <= nums.length <= 10^4`
* `-10^9 <= nums[i] <= 10^9`
* `-10^9 <= target <= 10^9`
* Only one valid answer exists.

---

## 2. Python Flow

### Summary Evolution Table

| Version | Implementation | Time | Memory | Core Rationale |
| :---: | :--- | :---: | :---: | :--- |
| **V1** | Cartesian Grid Search | `O(N^2)` | `O(1)` | Baseline intuition: checks all `N * N` pairs with an `i != j` guard. |
| **V2** | Upper Triangular Pruning | `O(N^2)` | `O(1)` | Commutative symmetry: starts `j` at `i + 1`, cutting checks by ~50% to `N * (N - 1) / 2`. |
| **V3** | Two-Pass Hash Map | `O(N)` | `O(N)` | Space-Time trade-off: uses a dictionary to turn inner scan loop into `O(1)` lookups. |
| **V4** | One-Pass Hash Map (Optimal) | `O(N)` | `O(N)` | Interleaves lookup and insertion: single loop, early exit, handles duplicates naturally. |

---

### Nuances & Step-by-Step Python Evolution

#### V1: Cartesian Grid Search (Your Initial Solution)
* **Logic:** Two nested loops over `range(len(nums))`.
* **Nuance / Bottleneck:**
  1. **Self-Pairing:** Checks `(0, 0)`, `(1, 1)`, etc. Requires an explicit `if (i != j)` branch check to prevent adding an element to itself.
  2. **Symmetric Duplicate Work:** Addition is commutative (`A + B == B + A`). Checking pair `(0, 1)` and later checking `(1, 0)` is 100% duplicate computation.
* **Operation Count:** Exactly `N * N` iterations.

#### V1 ➔ V2: Upper Triangular Pruning
* **What Changed:** The inner loop starts at `j = i + 1` instead of `0`.
* **Why:** Restricts the search grid strictly to pairs where `j > i`.
* **Nuance:** Because `j > i` is guaranteed, `i` and `j` can never be equal. The `(i != j)` condition is completely deleted.
* **Operation Count:** Drops from `N * N` down to `N * (N - 1) / 2`. For `N = 10,000`, operations drop from 100,000,000 to 49,995,000 (~50% reduction).
* **Limitation:** Still asymptotically `O(N^2)`.

#### V2 ➔ V3: Space-Time Trade-off (Two-Pass Hash Map)
* **What Changed:** Replaces the inner `for j` scanning loop with a Python dictionary (`lookup = {}`).
* **Why:** For each number, we already know what we need: `complement = target - nums[i]`. Instead of scanning `O(N)` remaining numbers with a loop, a dictionary look-up takes `O(1)` average time.
* **Nuance:** Pass 1 populates the entire dictionary (`lookup[num] = i`). Pass 2 checks `complement in lookup`. We must verify `lookup[complement] != i` to avoid using the same index twice.

#### V3 ➔ V4: Single-Pass Interleaving & Early Exit (Optimal)
* **What Changed:** Merges building and querying into a single loop. We check if the complement was already seen in our visited history *before* inserting the current number.
* **Nuance:**
  1. **Early Termination:** If the answer is in the first two elements, it terminates in 2 iterations without reading the rest of the array.
  2. **Handles Duplicate Numbers Automatically:** If `nums = [3, 3]` and `target = 6`: at `i = 1`, it looks back and finds the previous `3` at index 0 already in the map. No key-overwrite issues.
  3. **Result:** Achieves **0 ms / Beats 100%** on LeetCode.

---

## 3. C++ Flow

### Summary Systems Table

| Version | Implementation | Time | Memory | Systems / Memory Rationale |
| :---: | :--- | :---: | :---: | :--- |
| **V1** | Cartesian Grid Search | `O(N^2)` | `O(1)` | Direct nested loops over `std::vector<int>`. |
| **V2** | Upper Triangular Pruning | `O(N^2)` | `O(1)` | Pruned inner loop starting at `i + 1`. Zero extra allocations. |
| **V3** | Two-Pass `std::unordered_map` | `O(N)` | `O(N)` | Standard hash table lookup using iterator `find()`. |
| **V4** | One-Pass `std::unordered_map` | `O(N)` | `O(N)` | Single-pass lookback with early return. |
| **V5** | Systems & Cache Optimized | `O(N)` | `O(N)` | Calls `.reserve(N)` to eliminate bucket rehashing and heap reallocation pauses. |

---

### Nuances & Systems Deep Dive in C++

#### Nuance 1: Zero-Copy Arguments (`const std::vector<int>&`)
* In Python, passing `nums` passes an object reference handle (`O(1)` time).
* In C++, writing `twoSum(std::vector<int> nums)` passes by **value**. C++ will pause, allocate heap memory, and copy all `N` integers.
* **Systems Fix:** Always pass by `const std::vector<int>& nums`. The `&` passes by reference (zero copies), and `const` guarantees read-only safety.

#### Nuance 2: Memory Layout (Python PyObject vs. C++ Contiguous Primitives)
* In Python, every integer is a `PyObject` (~28 bytes) allocated on the heap. Python dictionary nodes store pointers to these objects, consuming ~20 MB of RAM on LeetCode.
* In C++, an `int` is a compact 4-byte scalar stored contiguously on CPU cache lines. Memory usage drops by half (~10 MB total).

#### Nuance 3: Map Lookup Mechanics (`std::unordered_map`)
* In Python, we write `if complement in seen:`.
* In C++, writing `seen[complement]` will **accidentally insert a default value (0)** if the key does not exist!
* **Idiomatic C++:** Use `auto it = seen.find(complement); if (it != seen.end())` to query existence safely.

#### Nuance 4: The Rehashing Bottleneck & V5 Optimization
* In C++, `std::unordered_map` starts with a default small bucket count (typically 8 slots).
* As elements are inserted, the load factor exceeds the threshold. C++ must allocate a larger bucket array on the heap, re-hash every single existing key, and deallocate the old bucket array.
* **The V5 Fix:** `seen.reserve(nums.size());`  
  Pre-allocates all required bucket capacity up front in a single allocation. Eliminates 100% of runtime rehashing pauses.

---

## 4. Conclusions & Key Takeaways

1. **The Fundamental Law of Space-Time Trade-offs:**  
   To eliminate a nested search loop from `O(N^2)` to `O(N)`, you must spend `O(N)` memory in the form of a Hash Map.
2. **Single-Pass Lookback Pattern:**  
   Always ask: *"Can I check past history before recording the present element?"* This eliminates two-pass passes, avoids duplicate key overwrites, and unlocks early loop termination.
3. **C++ Systems Discipline:**  
   * Always pass large containers by `const &` to avoid hidden `O(N)` deep copies.
   * Always consider container capacity: calling `.reserve()` on hash tables or vectors avoids dynamic heap reallocations.
