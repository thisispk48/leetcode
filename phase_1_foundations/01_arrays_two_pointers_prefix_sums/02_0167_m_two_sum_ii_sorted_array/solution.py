"""
0167. Two Sum II - Input Array Is Sorted
LeetCode: https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

1. Praveen's MySolution
2. Independent Evolutionary Ladder from V1 (Brute Force) to V3 (Optimal Converging Two Pointers)
"""


# =====================================================================
# 1. PRAVEEN'S SUBMISSION
# =====================================================================
class MySolution:
    """
    Praveen's Initial Submission:
    - Intuition: Two pointers with midpoint bisection on sorted array.
    - Status: Conceptually advanced, but contained syntax/indexing bugs.
    - Bugs Diagnosed:
        1. Index vs Value Comparison: Compared `mid` (index) to `target` (value).
        2. Pointer Updates: Shifted pointers to `mid` instead of checking the sum `numbers[left] + numbers[right]`.
        3. Indexing: Returned 0-indexed instead of 1-indexed.
    - Verdict: Conceptually targeted the optimal V3 archetype directly!
    """
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


# =====================================================================
# 2. INDEPENDENT EVOLUTIONARY LADDER (V1 -> V3)
# =====================================================================
class SolutionV1_BruteForce:
    """
    V1: Naive Upper-Triangular Nested Loops (Baseline Comparison).
    
    Approach:
        Check all pairs (i, j) where j > i.
        Completely ignores the sorted order.
        
    Complexity:
        Time:  O(N^2) - exact iterations: N * (N - 1) / 2.
               For N = 30,000 (~450 million operations), causes Time Limit Exceeded (TLE).
        Space: O(1)   - strictly zero extra memory.
    """
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        n = len(numbers)
        for i in range(n):
            for j in range(i + 1, n):
                if numbers[i] + numbers[j] == target:
                    return [i + 1, j + 1]  # 1-indexed
        return []


class SolutionV2_BinarySearch:
    """
    V2: Transform-and-Conquer (Binary Search per Element).
    
    Approach:
        For each element numbers[i], search for `complement = target - numbers[i]`
        in the remaining sorted subarray numbers[i + 1 .. N - 1] via bisection.
        
    Complexity:
        Time:  O(N log N) - N elements, each triggering an O(log N) bisection search.
        Space: O(1)       - only scalar pointer indices.
    """
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        n = len(numbers)
        for i in range(n):
            complement = target - numbers[i]
            low, high = i + 1, n - 1
            while low <= high:
                mid = (low + high) // 2
                if numbers[mid] == complement:
                    return [i + 1, mid + 1]
                elif numbers[mid] < complement:
                    low = mid + 1
                else:
                    high = mid - 1
        return []


class SolutionV3_TwoPointersOptimal:
    """
    V3: Monotonic Boundary Contraction (Converging Two Pointers - Optimal).
    
    Approach:
        Maintain two pointers: left at index 0 (minimum), right at N - 1 (maximum).
        Compute current_sum = numbers[left] + numbers[right].
        - If sum == target: match found! Return [left + 1, right + 1].
        - If sum < target: sum is too small; advance left += 1.
        - If sum > target: sum is too large; decrement right -= 1.
        
    Complexity:
        Time:  O(N) - single pass, at most N pointer movements (3 ms / Beats 87.6%).
        Space: O(1) - strictly zero extra heap memory allocated.
    """
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left = 0
        right = len(numbers) - 1

        while left < right:
            current_sum = numbers[left] + numbers[right]
            if current_sum == target:
                return [left + 1, right + 1]
            elif current_sum < target:
                left += 1
            else:
                right -= 1

        return []


# Default export
Solution = SolutionV3_TwoPointersOptimal
