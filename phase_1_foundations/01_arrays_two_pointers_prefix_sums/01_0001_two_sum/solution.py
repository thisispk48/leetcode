"""
0001. Two Sum
LeetCode: https://leetcode.com/problems/two-sum/

Evolutionary Implementations from V1 (Brute Force) to V4 (Optimal Single-Pass).
"""


class SolutionV1_CartesianProduct:
    """
    V1: Naive Full Cartesian Grid Search.
    
    Approach:
        Check every pair (i, j) in {0..N-1} x {0..N-1}.
        Uses explicit `i != j` guard to avoid self-pairing.
        
    Complexity:
        Time:  O(N^2) - exact iteration count: N * N.
        Space: O(1)   - only scalar loop indices allocated.
    """
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        n = len(nums)
        for i in range(n):
            for j in range(n):
                if (i != j) and (nums[i] + nums[j] == target):
                    return [i, j]
        return []


class SolutionV2_UpperTrianglePruning:
    """
    V2: Upper Triangular Pruning (Commutative Symmetry).
    
    Improvement over V1:
        Because A + B == B + A, searching j < i is redundant.
        Start inner loop at j = i + 1. 
        Guarantees j > i, eliminating the `i != j` branch condition.
        
    Complexity:
        Time:  O(N^2) - exact iteration count: N * (N - 1) / 2 (~50% reduction).
        Space: O(1)   - zero extra memory allocated.
    """
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []


class SolutionV3_TwoPassHashMap:
    """
    V3: Space-Time Trade-off (Two-Pass Hash Map).
    
    Improvement over V2:
        Eliminates the inner `for j` scanning loop completely.
        Pass 1: Store all elements in a hash map {number: index}.
        Pass 2: Look up `complement = target - num` in O(1) average time.
        
    Complexity:
        Time:  O(N) - two sequential passes of size N.
        Space: O(N) - dictionary stores up to N key-value pairs.
    """
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        lookup = {}
        # Pass 1: Build dictionary
        for i, num in enumerate(nums):
            lookup[num] = i

        # Pass 2: Query complement
        for i, num in enumerate(nums):
            complement = target - num
            if complement in lookup and lookup[complement] != i:
                return [i, lookup[complement]]
        return []


class SolutionV4_OnePassHashMap:
    """
    V4: Single-Pass Interleaved Hash Map (Optimal).
    
    Improvement over V3:
        Interleaves insertion and lookup in a single pass.
        Checks if complement was already observed in past history.
        Enables early termination as soon as the valid pair is encountered.
        Naturally handles duplicates (e.g. nums=[3, 3], target=6) without key-overwrite issues.
        
    Complexity:
        Time:  O(N) - single pass with early exit (0 ms / Beats 100%).
        Space: O(N) - worst-case dictionary size N.
    """
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []


# Default export for testing
Solution = SolutionV4_OnePassHashMap
