/**
 * Problem: 27. Remove Element
 * Category: 01 - Arrays, Two Pointers & Prefix Sums
 * Difficulty: Easy
 * URL: https://leetcode.com/problems/remove-element/
 *
 * Given an integer array nums and an integer val, remove all occurrences of val
 * in nums in-place. The order of the elements may be changed. Then return the
 * number of elements in nums which are not equal to val.
 */

#include <vector>
#include <utility>
#include <algorithm>

// =====================================================================
// 1. PRAVEEN'S SUBMISSION (Direct C++ Translation)
// =====================================================================
class MySolution {
public:
    /**
     * Praveen's initial approach: Single-pass Lomuto Swap.
     *
     * Invariants & Characteristics:
     * - In-place swap partitioning via std::swap.
     * - Returns write count k.
     * - Linear time O(N), auxiliary space O(1).
     */
    int removeElement(std::vector<int>& nums, int val) {
        int write = 0;
        int n = static_cast<int>(nums.size());

        for (int read = 0; read < n; ++read) {
            if (nums[read] != val) {
                std::swap(nums[write], nums[read]);
                write = write + 1;
            }
        }
        return write;
    }
};

// =====================================================================
// 2. INDEPENDENT EVOLUTIONARY LADDER (V1 Naive -> V4 Optimal)
// =====================================================================
class SolutionV1_InPlaceErase {
public:
    /**
     * V1: Naive In-Place Erase via std::vector::erase (Quadratic Trap).
     *
     * Complexity:
     * - Time:  O(N^2) memory shifting via repeated std::memmove().
     * - Space: O(1) auxiliary space.
     */
    int removeElement(std::vector<int>& nums, int val) {
        size_t i = 0;
        while (i < nums.size()) {
            if (nums[i] == val) {
                nums.erase(nums.begin() + i);  // Shifts all subsequent elements left!
            } else {
                ++i;
            }
        }
        return static_cast<int>(nums.size());
    }
};

class SolutionV2_ForwardOverwrite {
public:
    /**
     * V2: Fast & Slow Read/Write Pointers (Direct Overwrite).
     *
     * Systems Insight:
     * - Replaces swap with single forward assignment.
     * - Matches the canonical C++ STL algorithm `std::remove`.
     *
     * Complexity:
     * - Time:  O(N) single pass.
     * - Space: O(1) auxiliary space.
     * - Runtime: 0 ms / Beats 100%.
     */
    int removeElement(std::vector<int>& nums, int val) {
        int write = 0;
        int n = static_cast<int>(nums.size());

        for (int read = 0; read < n; ++read) {
            if (nums[read] != val) {
                nums[write++] = nums[read];
            }
        }
        return write;
    }
};

class SolutionV3_LomutoSwap {
public:
    /**
     * V3: Single-Pass Lomuto Swap (Praveen's Solution).
     *
     * Systems Insight:
     * - Preserves relative ordering while keeping val elements behind the boundary.
     * - std::swap lowers to CPU register exchange.
     *
     * Complexity:
     * - Time:  O(N) single pass.
     * - Space: O(1) auxiliary space.
     * - Runtime: 0 ms / Beats 100%.
     */
    int removeElement(std::vector<int>& nums, int val) {
        int write = 0;
        int n = static_cast<int>(nums.size());

        for (int read = 0; read < n; ++read) {
            if (nums[read] != val) {
                std::swap(nums[write++], nums[read]);
            }
        }
        return write;
    }
};

class SolutionV4_ConvergingTwoPointers {
public:
    /**
     * V4: Converging Two Pointers (Minimizing Writes When val is Rare).
     *
     * Systems & Hardware Architecture Insight:
     * - If val is rare (e.g. 1 occurrence in 10,000 items), V2/V3 performs
     *   9,999 memory store operations.
     * - V4 swaps the target with the last valid element and shrinks the tail.
     * - Exactly K memory writes (where K is count of val elements).
     *
     * Complexity:
     * - Time:  O(N) - at most N pointer steps.
     * - Space: O(1) auxiliary space.
     * - Writes: Minimal (at most K writes).
     * - Runtime: 0 ms / Beats 100%.
     */
    int removeElement(std::vector<int>& nums, int val) {
        int left = 0;
        int right = static_cast<int>(nums.size()) - 1;

        while (left <= right) {
            if (nums[left] == val) {
                nums[left] = nums[right];
                --right;
            } else {
                ++left;
            }
        }
        return left;
    }
};

// Default export alias
using Solution = SolutionV3_LomutoSwap;
