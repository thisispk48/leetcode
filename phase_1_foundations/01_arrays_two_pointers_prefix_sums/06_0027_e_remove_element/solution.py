"""
Problem: 27. Remove Element
Category: 01 - Arrays, Two Pointers & Prefix Sums
Difficulty: Easy
URL: https://leetcode.com/problems/remove-element/

Given an integer array nums and an integer val, remove all occurrences of val
in nums in-place. The order of the elements may be changed. Then return the
number of elements in nums which are not equal to val.

Consider the number of elements in nums which are not equal to val be k, to get
accepted, you need to:
- Change the array nums such that the first k elements of nums contain the elements
  which are not equal to val.
- The remaining elements of nums are not important as well as the size of nums.
- Return k.
"""

from typing import List


# =====================================================================
# 1. PRAVEEN'S SUBMISSION
# =====================================================================
class MySolution:
    """
    Praveen's initial submission: Single-pass Lomuto Swap partitioning.

    Strengths:
        - Reused the Lomuto swap mental model mastered in Move Zeroes (0283).
        - Single pass, strictly in-place with O(1) auxiliary memory.
        - Naturally packs non-val elements to index write while drifting val to tail.
        - Returns write directly as element count k.

    Complexity:
        Time:  O(N) - single pass through the array.
        Space: O(1) auxiliary space.
        LeetCode: 0 ms / Beats 100.00% (Memory: 19.28 MB / Beats 58.81%).

    Verdict:
        Instantly achieved the optimal 0 ms / Beats 100% benchmark on initial submission.
    """
    def removeElement(self, nums: List[int], val: int) -> int:
        write = 0
        for read in range(len(nums)):
            if nums[read] != val:
                nums[write], nums[read] = nums[read], nums[write]
                write = write + 1
        return write


# =====================================================================
# 2. INDEPENDENT EVOLUTIONARY LADDER (V1 Naive -> V4 Optimal)
# =====================================================================
class SolutionV1_InPlaceRemove:
    """
    V1: Naive list.remove() Loop (The Quadratic Anti-Pattern).

    Rationale:
        Repeatedly searches for val and calls nums.remove(val).

    The Hidden Trap:
        nums.remove() performs an O(N) linear search followed by an O(N) memory shift.
        Calling it inside a while loop degrades time complexity to O(N^2).

    Complexity:
        Time:  O(N^2) - repeated linear scans and array shifts.
        Space: O(1) auxiliary space.
        LeetCode: High runtime / TLE on large arrays.
    """
    def removeElement(self, nums: List[int], val: int) -> int:
        while val in nums:
            nums.remove(val)
        return len(nums)


class SolutionV2_ForwardOverwrite:
    """
    V2: Fast & Slow Read/Write Pointers (Direct Overwrite).

    Rationale:
        Direct overwrite instead of swapping:
        When nums[read] != val, simply copy nums[write] = nums[read] and advance write.
        Unlike Lomuto swap, direct assignment skips the secondary write of swapping
        val to the back (since elements beyond k can be ignored).

    Complexity:
        Time:  O(N) - single pass.
        Space: O(1) auxiliary space.
    """
    def removeElement(self, nums: List[int], val: int) -> int:
        write = 0
        for read in range(len(nums)):
            if nums[read] != val:
                nums[write] = nums[read]
                write += 1
        return write


class SolutionV3_LomutoSwap:
    """
    V3: Single-Pass Lomuto Swap (Praveen's Solution).

    Rationale:
        Swaps keeper elements with write slot.
        Preserves relative ordering while keeping val elements behind the write boundary.

    Complexity:
        Time:  O(N) - single pass.
        Space: O(1) auxiliary space.
        LeetCode: 0 ms / Beats 100.00%.
    """
    def removeElement(self, nums: List[int], val: int) -> int:
        write = 0
        for read in range(len(nums)):
            if nums[read] != val:
                nums[write], nums[read] = nums[read], nums[write]
                write += 1
        return write


class SolutionV4_ConvergingTwoPointers:
    """
    V4: Two Pointers from Both Ends (Minimizing Writes When Elements are Rare).

    Rationale:
        The problem explicitly states: "The order of the elements may be changed."
        If nums has 10,000 elements and val occurs only once at index 0:
        - V2/V3 will copy all 9,999 elements forward!
        - V4 takes the LAST element (nums[right]), moves it to index 0, and shrinks right.
        Total operations: exactly 1 write instead of 9,999!

    Invariant:
        left: Scans from beginning.
        right: Points to current valid tail boundary.
        When nums[left] == val, copy nums[right] into nums[left] and decrement right.
        (Do NOT advance left, because the copied element must be evaluated).

    Complexity:
        Time:  O(N) - at most N total pointer steps.
        Space: O(1) auxiliary space.
        Writes: At most K assignments (where K is the number of elements to remove).
    """
    def removeElement(self, nums: List[int], val: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            if nums[left] == val:
                nums[left] = nums[right]
                right -= 1
            else:
                left += 1

        return left


# Default export for verification
Solution = SolutionV3_LomutoSwap
