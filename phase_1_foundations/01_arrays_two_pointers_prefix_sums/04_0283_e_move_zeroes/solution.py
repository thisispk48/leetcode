"""
Problem: 283. Move Zeroes
Category: 01 - Arrays, Two Pointers & Prefix Sums
Difficulty: Easy
URL: https://leetcode.com/problems/move-zeroes/

Given an integer array nums, move all 0's to the end of it while maintaining
the relative order of the non-zero elements.

Note that you must do this in-place without making a copy of the array.

Follow up: Could you minimize the total number of operations done?
"""

from typing import List


# =====================================================================
# 1. PRAVEEN'S SUBMISSION
# =====================================================================
class MySolution:
    """
    Praveen's initial submission: Adjacent bubble swap intuition.

    Strengths:
        - Correctly recognizes that zeros can be moved to the end via pairwise swaps.
        - Correctly aims for in-place array mutation without auxiliary memory.

    Diagnosed Bottlenecks & Bugs:
        1. IndexError Bug:
           The inner loop executes for j in range(len(nums)). When j reaches
           the final index (len(nums) - 1), nums[j + 1] accesses an out-of-bounds
           index, raising `IndexError: list index out of range`.
        2. Quadratic Time Complexity:
           Nested loops iterate N * N times -> O(N^2) time.
           For N = 10^4, N^2 = 10^8 operations -> Guaranteed TLE on LeetCode.

    Verdict:
        Textbook implementation of V1 (Bubble Sort / Adjacent Swaps), but with
        an out-of-bounds index boundary bug.
    """
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        for i in range(len(nums)):
            for j in range(len(nums)):
                if nums[j] == 0 and nums[j + 1] != 0:
                    temp = nums[j]
                    nums[j] = nums[j + 1]
                    nums[j + 1] = temp


# =====================================================================
# 2. INDEPENDENT EVOLUTIONARY LADDER (V1 Naive -> V4 Optimal)
# =====================================================================
class SolutionV1_BubbleSort:
    """
    V1: Corrected Adjacent Bubble Sort (Brute Force).

    Rationale:
        Fixes the IndexError in MySolution by bounding j to len(nums) - 1 - i.
        Repeatedly bubbles adjacent zeros to the right.

    Complexity:
        Time:  O(N^2) - N * (N - 1) / 2 comparisons and swaps.
        Space: O(1) auxiliary space.
        LeetCode: Time Limit Exceeded (TLE) on large inputs.
    """
    def moveZeroes(self, nums: List[int]) -> None:
        n = len(nums)
        for i in range(n):
            swapped = False
            for j in range(n - 1 - i):
                if nums[j] == 0 and nums[j + 1] != 0:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
                    swapped = True
            if not swapped:
                break


class SolutionV2_TwoPassOverwrite:
    """
    V2: Two-Pass Read/Write Pointer + Zero Fill (Linear Time).

    Rationale:
        Pass 1: A read pointer scans the buffer; non-zero values are written
                to `write_idx` in compact sequence.
        Pass 2: Remaining positions from `write_idx` to N - 1 are filled with 0.

    Complexity:
        Time:  O(N) - 2 linear passes across the array.
        Space: O(1) auxiliary space.
        Writes: Exactly N total memory write operations.
    """
    def moveZeroes(self, nums: List[int]) -> None:
        write_idx = 0
        n = len(nums)

        # Pass 1: Compact non-zero elements
        for read_idx in range(n):
            if nums[read_idx] != 0:
                nums[write_idx] = nums[read_idx]
                write_idx += 1

        # Pass 2: Zero-fill trailing positions
        for i in range(write_idx, n):
            nums[i] = 0


class SolutionV3_SinglePassSwap:
    """
    V3: Single-Pass Swap (Lomuto Partitioning).

    Rationale:
        Replaces the separate zero-filling pass with in-place swapping.
        When read_idx encounters a non-zero element, it swaps it with write_idx.
        Zeros naturally drift backward behind the write pointer in a single pass.

    Complexity:
        Time:  O(N) - single pass through the array.
        Space: O(1) auxiliary space.
        LeetCode: 6 ms / Beats 45.14% (Memory: 20.43 MB / Beats 63.14%).
    """
    def moveZeroes(self, nums: List[int]) -> None:
        write_idx = 0
        for read_idx in range(len(nums)):
            if nums[read_idx] != 0:
                nums[write_idx], nums[read_idx] = nums[read_idx], nums[write_idx]
                write_idx += 1


class SolutionV4_OptimizedNoSelfSwap:
    """
    V4: Single-Pass Lomuto Swap with Self-Swap Guard (Optimal).

    Improvement over V3:
        Addresses LeetCode's follow-up: "Minimize total operations done".
        If an array begins with non-zero elements (e.g. [1, 2, 3, 0, 4]),
        write_idx == read_idx. Performing a self-swap (nums[i] with nums[i])
        wastes CPU cycles and dirties memory cache lines unnecessarily.
        Guard: Only swap when write_idx != read_idx.

    Complexity:
        Time:  O(N) - single pass with minimal write operations.
        Space: O(1) auxiliary space.
    """
    def moveZeroes(self, nums: List[int]) -> None:
        write_idx = 0
        for read_idx in range(len(nums)):
            if nums[read_idx] != 0:
                if write_idx != read_idx:
                    nums[write_idx], nums[read_idx] = nums[read_idx], nums[write_idx]
                write_idx += 1


# Default export for verification
Solution = SolutionV4_OptimizedNoSelfSwap
