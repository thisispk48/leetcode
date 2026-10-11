"""
Problem: 26. Remove Duplicates from Sorted Array
Category: 01 - Arrays, Two Pointers & Prefix Sums
Difficulty: Easy
URL: https://leetcode.com/problems/remove-duplicates-from-sorted-array/

Given an integer array nums sorted in non-decreasing order, remove the duplicates
in-place such that each unique element appears only once. The relative order of the
elements should be kept the same. Then return the number of unique elements in nums.

Consider the number of unique elements of nums to be k, to get accepted, you need to:
- Change the array nums such that the first k elements of nums contain the unique elements.
- Return k.
"""

from typing import List


# =====================================================================
# 1. PRAVEEN'S SUBMISSION
# =====================================================================
class MySolution:
    """
    Praveen's initial submission: Read/Write pointer compaction.

    Strengths:
        - Instinctively identified Archetype 2 (Fast & Slow Pointers).
        - Maintained a write boundary (`write`) while scanning forward (`i`).
        - Zero auxiliary buffer allocations -> strict O(1) space.

    Diagnosed Bottlenecks & Bugs:
        - Initially omitted `return write + 1`, returning None by default.
        - Once `return write + 1` was added, achieved optimal 0 ms / Beats 100%.

    Verdict:
        Conceptually jumped straight to the optimal V3 (Fast/Slow Two Pointers),
        bypassing the auxiliary set (V1) and in-place pop trap (V2).
    """
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0
        write = 0
        for i in range(1, len(nums)):
            if nums[write] == nums[i]:
                continue
            else:
                write = write + 1
                nums[write] = nums[i]
        return write + 1


# =====================================================================
# 2. INDEPENDENT EVOLUTIONARY LADDER (V1 Naive -> V4 Optimal)
# =====================================================================
class SolutionV1_ExtraMemorySet:
    """
    V1: Auxiliary Hash Set / List Reconstruction (Naive Baseline).

    Rationale:
        Collects unique elements into a set, sorts them, and overwrites nums.

    Complexity:
        Time:  O(N log N) or O(N) depending on hash vs ordered set.
        Space: O(N) auxiliary space.
        Constraint Violation: Violates LeetCode's in-place O(1) memory requirement.
    """
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0
        unique = sorted(list(set(nums)))
        for i, val in enumerate(unique):
            nums[i] = val
        return len(unique)


class SolutionV2_InPlacePop:
    """
    V2: Naive In-Place Deletion via pop() (The Quadratic Trap).

    Rationale:
        Detects duplicates sequentially and calls nums.pop(i + 1).

    The Hidden Trap:
        In dynamic arrays (Python list, C++ std::vector), popping an element at
        index i requires shifting all (N - i) subsequent elements left by 1.
        Doing this inside a loop degrades time complexity to O(N^2).

    Complexity:
        Time:  O(N^2) - N * O(N) array shifts -> TLE on large arrays.
        Space: O(1) auxiliary space.
    """
    def removeDuplicates(self, nums: List[int]) -> int:
        i = 0
        while i < len(nums) - 1:
            if nums[i] == nums[i + 1]:
                nums.pop(i + 1)  # O(N) memory shift!
            else:
                i += 1
        return len(nums)


class SolutionV3_TwoPointers:
    """
    V3: Fast & Slow Read/Write Pointers (Optimal).

    Rationale:
        Overwrites duplicate positions in-place without shifting the remaining buffer:
        - `write`: Tracks the index of the latest unique element recorded.
        - `read`: Scans every element from index 1 to N - 1.
        When nums[read] != nums[write], increment write and record nums[read].

    Complexity:
        Time:  O(N) - single pass with exactly N comparisons.
        Space: O(1) auxiliary space.
        LeetCode: 0 ms / Beats 100.00% (Memory: 20.64 MB).
    """
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0

        write = 0
        for read in range(1, len(nums)):
            if nums[read] != nums[write]:
                write += 1
                nums[write] = nums[read]

        return write + 1


class SolutionV4_SelfAssignmentGuard:
    """
    V4: Two Pointers with Self-Assignment Guard (Systems Optimization).

    Rationale:
        If an array has no duplicates (e.g. [1, 2, 3, 4, 5]), V3 performs
        redundant self-writes (`nums[1] = nums[1]`, `nums[2] = nums[2]`).
        Adding `if write != read` avoids dirtying memory cache lines when
        the read and write pointers coincide.

    Complexity:
        Time:  O(N) - single pass with minimal write operations.
        Space: O(1) auxiliary space.
    """
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0

        write = 0
        for read in range(1, len(nums)):
            if nums[read] != nums[write]:
                write += 1
                if write != read:
                    nums[write] = nums[read]

        return write + 1


# Default export for verification
Solution = SolutionV3_TwoPointers
