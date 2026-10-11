/**
 * Problem: 26. Remove Duplicates from Sorted Array
 * Category: 01 - Arrays, Two Pointers & Prefix Sums
 * Difficulty: Easy
 * URL: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
 *
 * Given an integer array nums sorted in non-decreasing order, remove the duplicates
 * in-place such that each unique element appears only once. The relative order of the
 * elements should be kept the same. Then return the number of unique elements in nums.
 */

#include <vector>
#include <set>
#include <algorithm>

// =====================================================================
// 1. PRAVEEN'S SUBMISSION (Direct C++ Translation)
// =====================================================================
class MySolution {
public:
    /**
     * Praveen's initial approach: Read/Write pointer compaction.
     *
     * Invariants & Characteristics:
     * - Fast & Slow pointer in-place write boundary.
     * - Returns write + 1 as count of unique items.
     * - Linear time O(N) and O(1) auxiliary space.
     */
    int removeDuplicates(std::vector<int>& nums) {
        if (nums.empty()) return 0;
        int write = 0;
        int n = static_cast<int>(nums.size());

        for (int i = 1; i < n; ++i) {
            if (nums[write] == nums[i]) {
                continue;
            } else {
                write = write + 1;
                nums[write] = nums[i];
            }
        }
        return write + 1;
    }
};

// =====================================================================
// 2. INDEPENDENT EVOLUTIONARY LADDER (V1 Naive -> V4 Optimal)
// =====================================================================
class SolutionV1_ExtraMemorySet {
public:
    /**
     * V1: Extra Buffer with std::set (Space-Time Trade-off / Violation).
     *
     * Complexity:
     * - Time:  O(N log N) tree insertions.
     * - Space: O(N) heap node allocations (violates in-place requirement).
     */
    int removeDuplicates(std::vector<int>& nums) {
        if (nums.empty()) return 0;
        std::set<int> unique_set(nums.begin(), nums.end());

        int idx = 0;
        for (int val : unique_set) {
            nums[idx++] = val;
        }
        return static_cast<int>(unique_set.size());
    }
};

class SolutionV2_InPlaceErase {
public:
    /**
     * V2: In-Place Deletion via std::vector::erase (The Quadratic Trap).
     *
     * Systems Insight:
     * - std::vector is a contiguous array.
     * - Calling `erase()` moves all subsequent elements via std::memmove().
     * - Erasing K duplicates costs O(K * N) -> O(N^2) time -> TLE.
     *
     * Complexity:
     * - Time:  O(N^2) memory shifting.
     * - Space: O(1) auxiliary space.
     */
    int removeDuplicates(std::vector<int>& nums) {
        if (nums.empty()) return 0;
        size_t i = 0;
        while (i < nums.size() - 1) {
            if (nums[i] == nums[i + 1]) {
                nums.erase(nums.begin() + i + 1);  // Expensive memory copy!
            } else {
                ++i;
            }
        }
        return static_cast<int>(nums.size());
    }
};

class SolutionV3_TwoPointers {
public:
    /**
     * V3: Fast & Slow Read/Write Pointers (Optimal).
     *
     * Systems Insight:
     * - Single contiguous pass through memory.
     * - Hardware prefetcher easily streams cache lines.
     * - Direct mirror of the STL algorithm `std::unique`.
     *
     * Complexity:
     * - Time:  O(N) - exactly N - 1 comparisons.
     * - Space: O(1) auxiliary space.
     * - Runtime: 0 ms / Beats 100% in C++.
     */
    int removeDuplicates(std::vector<int>& nums) {
        if (nums.empty()) return 0;

        int write = 0;
        int n = static_cast<int>(nums.size());

        for (int read = 1; read < n; ++read) {
            if (nums[read] != nums[write]) {
                nums[++write] = nums[read];
            }
        }

        return write + 1;
    }
};

class SolutionV4_SelfAssignmentGuard {
public:
    /**
     * V4: Two Pointers with Self-Assignment Guard (Systems Optimization).
     *
     * Systems & Hardware Architecture Insights:
     * - Guarding `if (write != read)` prevents unnecessary cache-line writes
     *   when an array has few or no duplicates.
     * - Avoids marking cache lines as "Modified" in L1/L2 cache.
     *
     * Complexity:
     * - Time:  O(N) single pass.
     * - Space: O(1) auxiliary space.
     */
    int removeDuplicates(std::vector<int>& nums) {
        if (nums.empty()) return 0;

        int write = 0;
        int n = static_cast<int>(nums.size());

        for (int read = 1; read < n; ++read) {
            if (nums[read] != nums[write]) {
                ++write;
                if (write != read) {
                    nums[write] = nums[read];
                }
            }
        }

        return write + 1;
    }
};

// Default export alias
using Solution = SolutionV3_TwoPointers;
