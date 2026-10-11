"""
Problem: 15. 3Sum
Category: 01 - Arrays, Two Pointers & Prefix Sums
Difficulty: Medium
URL: https://leetcode.com/problems/3sum/

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.
"""

from typing import List


# =====================================================================
# 1. PRAVEEN'S SUBMISSION
# =====================================================================
class MySolution:
    """
    Praveen's initial submission: 3-loop combination search.

    Strengths:
        - Correctly establishes strict index ordering (j = i + 1, k = j + 1),
          ensuring i < j < k by construction.
        - Correctly targets the fundamental identity nums[i] + nums[j] + nums[k] == 0.

    Diagnosed Bottlenecks & Bugs:
        1. Duplicate Triplets:
           Distinct index combinations can evaluate to identical numerical triplets
           when duplicate numbers exist in nums (e.g. nums[0] == nums[4] == -1).
        2. Cubic Time Complexity:
           Evaluates C(N, 3) = N * (N - 1) * (N - 2) / 6 combinations.
           For N = 3000, ~4.5 * 10^9 operations -> Guaranteed TLE.
        3. Redundant Conditionals:
           (i != j) and (j != k) and (i != k) is strictly redundant because
           loop ranges already enforce i < j < k.

    Verdict:
        Aligns conceptually with V1 (Naive Brute Force), but lacks canonical
        representation / deduplication to satisfy the problem's uniqueness contract.
    """
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        triplets = []
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                for k in range(j + 1, len(nums)):
                    if (i != j) and (j != k) and (i != k) and (nums[i] + nums[j] + nums[k] == 0):
                        triplets.append([nums[i], nums[j], nums[k]])
        return triplets


# =====================================================================
# 2. INDEPENDENT EVOLUTIONARY LADDER (V1 Naive -> V3 Optimal)
# =====================================================================
class SolutionV1_BruteForceSet:
    """
    V1: Brute Force with Canonical Tuple Normalization & Hash Set.

    Rationale:
        Fixes the duplicate-triplet bug of MySolution by sorting each valid trio
        into an immutable tuple and filtering through a set.

    Why Tuple and not List?
        Python set elements must implement __hash__. Mutable lists have __hash__ = None.
        Tuples are immutable, guaranteeing invariant hash codes.

    Complexity:
        Time:  O(N^3) - C(N, 3) iterations with O(1) tuple construction.
        Space: O(N) to O(N^3) - set to hold unique triplets.
        Result: Time Limit Exceeded (TLE) on LeetCode.
    """
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        triplets = set()

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        canonical = tuple(sorted([nums[i], nums[j], nums[k]]))
                        triplets.add(canonical)

        return [list(t) for t in triplets]


class SolutionV2_HashSet:
    """
    V2: Pivot-and-Complement Hash Set (Space-Time Trade-off).

    Rationale:
        Fixes pivot nums[i] and reduces the remaining subproblem to Two Sum (0001):
            nums[j] + nums[k] == -nums[i]
        For each fixed i, runs a single-pass hash lookup on the suffix j in [i + 1 .. N - 1].
        A seen set tracks visited elements for the current i pass.

    Complexity:
        Time:  O(N^2) - N outer iterations * O(N) inner hash lookups.
        Space: O(N) - seen hash set per pivot + output set.
        Result: Slow (~2500 ms) or TLE on large inputs due to Python heap churn
                (allocating 3000 sets and repeatedly sorting 3-tuples).
    """
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        triplets = set()

        for i in range(n):
            seen = set()
            for j in range(i + 1, n):
                complement = -nums[i] - nums[j]
                if complement in seen:
                    canonical = tuple(sorted([nums[i], nums[j], complement]))
                    triplets.add(canonical)
                seen.add(nums[j])

        return [list(t) for t in triplets]


class SolutionV3_TwoPointers:
    """
    V3: Presorting + Two Pointers with Symmetric Duplicate Pruning (Optimal).

    Rationale (Transform-and-Conquer):
        Sorting the array once in O(N log N) unlocks:
        1. Monotonicity: Two pointers (left, right) shrink the search space in O(N).
        2. Adjacent duplicates: Identical values cluster together, enabling
           O(1) auxiliary space deduplication without any hash sets or tuples.
        3. Early Pruning: If nums[i] > 0, three non-decreasing numbers can never sum to 0.

    Deduplication Mechanics:
        - Pivot: if i > 0 and nums[i] == nums[i - 1]: continue
        - Left:  while left < right and nums[left] == nums[left - 1]: left += 1
        - Right: while left < right and nums[right] == nums[right + 1]: right -= 1

    Complexity:
        Time:  O(N^2) - O(N log N) sort + N passes of O(N) two pointers.
        Space: O(1) auxiliary space (excluding returned output list).
        LeetCode: 474 ms / Beats 92.90% (Memory: 22.34 MB / Beats 33.62%).
    """
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        results = []
        nums.sort()
        n = len(nums)

        for i in range(n - 2):
            # Early pruning: 3 positive numbers in sorted array cannot sum to 0
            if nums[i] > 0:
                break

            # Skip duplicate pivot values
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left = i + 1
            right = n - 1

            while left < right:
                total = nums[i] + nums[left] + nums[right]

                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    results.append([nums[i], nums[left], nums[right]])

                    left += 1
                    right -= 1

                    # Skip duplicate left values
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1

                    # Skip duplicate right values (symmetric pruning)
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1

        return results


# Default export for verification
Solution = SolutionV3_TwoPointers
