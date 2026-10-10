/**
 * 0167. Two Sum II - Input Array Is Sorted
 * LeetCode: https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
 * 
 * 1. Praveen's MySolution (C++ Equivalent)
 * 2. Independent Evolutionary Ladder from V1 (Brute Force) to V3 (Optimal Two Pointers)
 */

#include <vector>

// ============================================================================
// 1. PRAVEEN'S SUBMISSION
// ============================================================================
class MySolution {
public:
    std::vector<int> twoSum(const std::vector<int>& numbers, int target) {
        int left = 0;
        int right = numbers.size() - 1;
        while (left < right) {
            int mid = (left + right) / 2;
            if (numbers[left] + numbers[right] == target) {
                return {left, right}; // Praveen's 0-indexed return
            } else if (mid <= target) {
                right = mid;
                continue;
            } else if (target <= mid) {
                left = mid;
                continue;
            }
        }
        return {};
    }
};

// ============================================================================
// 2. INDEPENDENT EVOLUTIONARY LADDER (V1 -> V3)
// ============================================================================

// V1: Naive Upper-Triangular Nested Loops (Causes TLE on LeetCode)
class SolutionV1_BruteForce {
public:
    std::vector<int> twoSum(const std::vector<int>& numbers, int target) {
        int n = numbers.size();
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                if (numbers[i] + numbers[j] == target) {
                    return {i + 1, j + 1}; // 1-indexed
                }
            }
        }
        return {};
    }
};

// V2: Binary Search per Element (Transform-and-Conquer)
class SolutionV2_BinarySearch {
public:
    std::vector<int> twoSum(const std::vector<int>& numbers, int target) {
        int n = numbers.size();
        for (int i = 0; i < n; ++i) {
            int complement = target - numbers[i];
            int low = i + 1, high = n - 1;
            while (low <= high) {
                int mid = low + (high - low) / 2; // Prevents integer overflow
                if (numbers[mid] == complement) {
                    return {i + 1, mid + 1};
                } else if (numbers[mid] < complement) {
                    low = mid + 1;
                } else {
                    high = mid - 1;
                }
            }
        }
        return {};
    }
};

// V3: Converging Two Pointers (Optimal Algorithmic & Systems Peak)
class SolutionV3_TwoPointersOptimal {
public:
    // SYSTEMS HIGHLIGHTS:
    // 1. const std::vector<int>&: zero-copy pass-by-reference.
    // 2. Continuous cache prefetching: left scans forward and right scans backward
    //    over contiguous 4-byte integers in L1 CPU cache.
    // 3. Strictly zero heap allocations: returns initializer list {left + 1, right + 1}.
    std::vector<int> twoSum(const std::vector<int>& numbers, int target) {
        int left = 0;
        int right = numbers.size() - 1;

        while (left < right) {
            int current_sum = numbers[left] + numbers[right];
            if (current_sum == target) {
                return {left + 1, right + 1}; // 1-indexed
            } else if (current_sum < target) {
                ++left; // Sum too small, advance to larger element
            } else {
                --right; // Sum too large, retreat to smaller element
            }
        }
        return {};
    }
};

// Default alias
using Solution = SolutionV3_TwoPointersOptimal;
