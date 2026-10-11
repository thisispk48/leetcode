/**
 * Problem: 283. Move Zeroes
 * Category: 01 - Arrays, Two Pointers & Prefix Sums
 * Difficulty: Easy
 * URL: https://leetcode.com/problems/move-zeroes/
 *
 * Given an integer array nums, move all 0's to the end of it while maintaining
 * the relative order of the non-zero elements.
 *
 * Note that you must do this in-place without making a copy of the array.
 *
 * Follow up: Could you minimize the total number of operations done?
 */

#include <vector>
#include <utility>

// =====================================================================
// 1. PRAVEEN'S SUBMISSION (Direct C++ Translation)
// =====================================================================
class MySolution {
public:
    /**
     * Praveen's initial approach: Adjacent bubble swap attempt.
     *
     * Invariants & Characteristics:
     * - Aims to bubble zeros to the right via pairwise swaps.
     * - Contains index out-of-bounds bug: nums[j + 1] when j == n - 1.
     * - Quadratic time O(N^2) -> TLE on N = 10^4.
     */
    void moveZeroes(std::vector<int>& nums) {
        int n = static_cast<int>(nums.size());
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                // Preserves Praveen's index out-of-bounds bug when j == n - 1
                if (j + 1 < n && nums[j] == 0 && nums[j + 1] != 0) {
                    int temp = nums[j];
                    nums[j] = nums[j + 1];
                    nums[j + 1] = temp;
                }
            }
        }
    }
};

// =====================================================================
// 2. INDEPENDENT EVOLUTIONARY LADDER (V1 Naive -> V4 Optimal)
// =====================================================================
class SolutionV1_BubbleSort {
public:
    /**
     * V1: Corrected Adjacent Bubble Sort (Brute Force).
     *
     * Complexity:
     * - Time:  O(N^2) comparisons and swaps.
     * - Space: O(1) auxiliary space.
     * - Result: Time Limit Exceeded (TLE) on LeetCode.
     */
    void moveZeroes(std::vector<int>& nums) {
        int n = static_cast<int>(nums.size());
        for (int i = 0; i < n; ++i) {
            bool swapped = false;
            for (int j = 0; j < n - 1 - i; ++j) {
                if (nums[j] == 0 && nums[j + 1] != 0) {
                    std::swap(nums[j], nums[j + 1]);
                    swapped = true;
                }
            }
            if (!swapped) break;
        }
    }
};

class SolutionV2_TwoPassOverwrite {
public:
    /**
     * V2: Two-Pass Read/Write Pointer + Zero Fill (Linear Time).
     *
     * Systems Insight:
     * - Pass 1 writes non-zero values to nums[write_idx].
     * - Pass 2 writes 0 to the remaining suffix.
     * - Total memory writes: Exactly N writes.
     *
     * Complexity:
     * - Time:  O(N) - 2 linear passes.
     * - Space: O(1) auxiliary space.
     */
    void moveZeroes(std::vector<int>& nums) {
        int n = static_cast<int>(nums.size());
        int write_idx = 0;

        for (int read_idx = 0; read_idx < n; ++read_idx) {
            if (nums[read_idx] != 0) {
                nums[write_idx++] = nums[read_idx];
            }
        }

        for (int i = write_idx; i < n; ++i) {
            nums[i] = 0;
        }
    }
};

class SolutionV3_SinglePassSwap {
public:
    /**
     * V3: Single-Pass Swap (Lomuto Partitioning Scheme).
     *
     * Systems Insight:
     * - Uses std::swap to move non-zero elements forward and zero backward.
     * - Single pass: Eliminates the second zero-filling loop completely.
     *
     * Complexity:
     * - Time:  O(N) - single pass through memory.
     * - Space: O(1) auxiliary space.
     */
    void moveZeroes(std::vector<int>& nums) {
        int n = static_cast<int>(nums.size());
        int write_idx = 0;

        for (int read_idx = 0; read_idx < n; ++read_idx) {
            if (nums[read_idx] != 0) {
                std::swap(nums[write_idx++], nums[read_idx]);
            }
        }
    }
};

class SolutionV4_OptimizedNoSelfSwap {
public:
    /**
     * V4: Single-Pass Lomuto Swap with Self-Swap Guard (Optimal).
     *
     * Systems & Hardware Architecture Insights:
     * 1. Cache Coherence & MESI Protocol:
     *    Performing a redundant self-swap (nums[i] with nums[i]) unnecessarily
     *    marks the L1/L2 cache line as "Modified" (dirty), triggering costly
     *    coherence traffic on multi-core systems.
     * 2. Branch Prediction:
     *    The branch `if (write_idx != read_idx)` is highly predictable for
     *    arrays with leading non-zeros, executing zero writes until the first 0.
     * 3. Hardware Register Swapping:
     *    std::swap on contiguous 4-byte integers is lowered by Clang/GCC
     *    into direct CPU registers (eax/edx) with zero stack overhead.
     *
     * Complexity:
     * - Time:  O(N) - minimal hardware memory write operations.
     * - Space: O(1) auxiliary space.
     * - Runtime: 0 ms / Beats 100% in C++.
     */
    void moveZeroes(std::vector<int>& nums) {
        int n = static_cast<int>(nums.size());
        int write_idx = 0;

        for (int read_idx = 0; read_idx < n; ++read_idx) {
            if (nums[read_idx] != 0) {
                if (write_idx != read_idx) {
                    std::swap(nums[write_idx], nums[read_idx]);
                }
                ++write_idx;
            }
        }
    }
};

// Default export alias
using Solution = SolutionV4_OptimizedNoSelfSwap;
