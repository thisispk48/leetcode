# Category 01: Arrays, Two Pointers & Prefix Sums

> **Phase 1: Foundational DSA**  
> *Connecting discrete 1D signals, coordinate shrinking, and discrete integration.*

---

# 📘 PART 1: BEFORE STARTING (Theory, Intuition & Python Tips)

---

## 1. Mathematical Framing & Levitin's Lens

An array is fundamentally a **discrete 1D signal** $x[n]$ mapped to contiguous memory addresses. Because index lookup $x[i]$ is purely address arithmetic ($\text{base} + i \times \text{size}$), random access is strictly $O(1)$. 

In this category, we solve search and aggregation problems over arrays using three core design techniques from Anany Levitin's taxonomy:

1. **Space-Time Trade-offs:**  
   Instead of testing all pairs $(i, j)$ in $O(N^2)$ time, we spend $O(N)$ auxiliary memory (a hash table or prefix array) to reduce the query time to $O(1)$.
2. **Transform-and-Conquer:**  
   An unsorted array has high entropy. By sorting it first ($O(N \log N)$), we enforce a **monotonic invariant**. Once monotonicity is established, we can discard vast regions of the search space using two pointers without inspecting them.
3. **Discrete Integration (Prefix Sums):**  
   Just as the Fundamental Theorem of Calculus states that $\int_a^b f(x)\,dx = F(b) - F(a)$, in discrete mathematics:
   $$\sum_{k=i}^{j} A[k] = P[j+1] - P[i] \quad \text{where } P[m] = \sum_{k=0}^{m-1} A[k]$$
   This pre-computation turns any range sum query from an $O(N)$ loop into a single $O(1)$ subtraction.

---

## 2. The 3 Core Archetypes in this Category

```mermaid
flowchart TD
    A["Problem on 1D Array"] --> B{"What is the goal?"}
    B -->|"Find pair/triplet meeting sum/target"| C{"Is array sorted or sortable?"}
    C -->|Yes: O(1) space preferred| D["Converging Two Pointers (L ➔, 🠔 R)"]
    C -->|No: Original indices needed| E["Hash Map Complement Lookup (Space-Time)"]
    B -->|"In-place mutation / compacting"| F["Fast & Slow Pointers (Read/Write)"]
    B -->|"Subarray sums / range queries"| G["Prefix Sums + Hash Map"]
```

### Archetype A: Converging Two Pointers ($L \to, \gets R$)
* **Precondition:** The array must be sorted (monotonic).
* **The Invariant:**
  * Initialize `left = 0` (minimum element) and `right = len(nums) - 1` (maximum element).
  * Compute `current_sum = nums[left] + nums[right]`.
  * If `current_sum < target`: Because `nums[right]` is already the largest available value, no element paired with `nums[left]` can ever reach `target`. Therefore, `nums[left]` is eliminated forever $\implies$ `left += 1`.
  * If `current_sum > target`: By symmetric reasoning, `nums[right]` can never participate $\implies$ `right -= 1`.
* **Complexity:** Eliminates one element per step $\implies$ exactly $O(N)$ time with $O(1)$ space.

### Archetype B: Fast & Slow (Read & Write) Pointers
* **Goal:** In-place compaction (e.g., *Remove Duplicates*, *Move Zeroes*) without allocating a new array.
* **The Invariant:**
  * `slow` (Write pointer): Demarcates the boundary of the processed, valid prefix. Everything to the left of `slow` is guaranteed to be correct.
  * `fast` (Read pointer): Scans ahead through the raw data frontier.
  * When `fast` discovers a valid element, copy it to `nums[slow]` and advance `slow += 1`.
* **Complexity:** Single pass $O(N)$ time, strictly $O(1)$ auxiliary space.

### Archetype C: Prefix Sums & Complement Lookup
* **Goal:** Finding contiguous subarrays satisfying a condition (e.g., sum equals $K$).
* **The Insight:**
  * Let $P[i]$ be the cumulative sum up to index $i$.
  * A subarray from $i+1$ to $j$ has sum equal to $K$ if and only if:
    $$P[j] - P[i] = K \iff P[i] = P[j] - K$$
  * As we compute $P[j]$ sequentially, we store previous prefix sums in a Hash Map. Finding a matching subarray reduces to checking if $(P[j] - K)$ exists in our map.
* **Complexity:** Drops an $O(N^2)$ brute-force subsegment search down to $O(N)$ time.

---

## 3. Essential Python Tips for This Category

1. **Avoid Slicing Inside Loops:**
   * `nums[i:j]` creates a **shallow copy** of that slice in memory ($O(K)$ time and space). Doing this inside a loop turns an $O(N)$ algorithm into $O(N^2)$.
   * Use indices or pointers instead of slicing whenever possible.
2. **In-Place Mutation Syntax:**
   * If a problem asks you to modify `nums` in place, assigning `nums = result` merely rebinds the local variable name. The caller will still see the old list.
   * To overwrite in place: `nums[:] = result` or mutate via index `nums[write_idx] = val`.
3. **Idiomatic Index & Value Pairing:**
   * Always use `for idx, val in enumerate(nums):` instead of manual counter variables.
4. **Dictionary Lookup Performance:**
   * Checking `key in my_dict` is $O(1)$ average time.
   * Use `my_dict.get(key, default)` to avoid explicit `if key in my_dict` checks when updating frequencies.
5. **No 32-Bit Overflow in Python (Mental Note for C++):**
   * Python handles arbitrarily large integers automatically. 
   * However, keep in mind that when porting to C++, numbers exceeding $\approx 2 \times 10^9$ will overflow standard 32-bit `int` and require `long long` (64-bit).

---

# 🧠 PART 2: AFTER COMPLETING (Retrospective & Mind Map)

*(This section will be populated as we finish the problems in this category. It will serve as your permanent cheat sheet and decision tree).*

### Pattern Decision Tree
*(To be compiled upon category completion)*

### Common Edge Cases & Pitfalls
*(To be compiled upon category completion)*

### Python ➔ C++ Translation Highlights
*(To be compiled upon category completion)*
