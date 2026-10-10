# 0001. Two Sum

- **LeetCode Link**: [1. Two Sum](https://leetcode.com/problems/two-sum/)
- **Difficulty**: Easy
- **Phase**: 1 (Foundations)
- **Category**: 01. Arrays, Two Pointers & Prefix Sums
- **Primary Concepts**: Array indexing, Complement search, Space-Time Trade-offs, Hash tables

---

## 1. Problem Statement

Given an array of integers `nums` and an integer `target`, return *indices of the two numbers such that they add up to `target`*.

You may assume that each input would have **exactly one solution**, and you may not use the same element twice.

You can return the answer in any order.

### Constraints
- $2 \le \text{nums.length} \le 10^4$
- $-10^9 \le \text{nums}[i] \le 10^9$
- $-10^9 \le \text{target} \le 10^9$
- **Only one valid answer exists.**

---

## 2. The Evolutionary Engineering Chain

```mermaid
flowchart TD
    V1["v1: Initial / Brute Force"] -->|Step 1: Avoid re-checking pairs| V2["v2: Pair Pruning"]
    V2 -->|Step 2: Transform to Lookup Table| V3["v3: Two-Pass Hash Table"]
    V3 -->|Step 3: Single Pass Interleaving| V4["v4: One-Pass Hash Table (Optimal)"]
    V4 -->|Step 4: Systems / Cache Tuning| V5["v5: C++ Pre-allocated Buckets & Zero-Copy"]
```

*(This section will document the exact step-by-step improvements and metric deltas as we iterate together).*

---

## 3. Python ➔ C++ Bridge Notes

*(Documenting key language differences, memory layouts, reference semantics, and runtime behaviors for each version).*
