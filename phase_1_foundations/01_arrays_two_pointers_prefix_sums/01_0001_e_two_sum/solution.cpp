/**
 * 0001. Two Sum
 * LeetCode: https://leetcode.com/problems/two-sum/
 * 
 * 1. Praveen's MySolution (C++ Equivalent)
 * 2. Independent Evolutionary Ladder from V1 (Brute Force) to V5 (Systems Optimized)
 */

#include <vector>
#include <unordered_map>

// ============================================================================
// 1. PRAVEEN'S SUBMISSION
// ============================================================================
class MySolution {
public:
    std::vector<int> twoSum(const std::vector<int>& nums, int target) {
        int n = nums.size();
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (i != j && nums[i] + nums[j] == target) {
                    return {i, j};
                }
            }
        }
        return {};
    }
};

// ============================================================================
// 2. INDEPENDENT EVOLUTIONARY LADDER (V1 -> V5)
// ============================================================================

// V1: Naive Full Cartesian Grid Search
class SolutionV1_CartesianProduct {
public:
    std::vector<int> twoSum(const std::vector<int>& nums, int target) {
        int n = nums.size();
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (i != j && nums[i] + nums[j] == target) {
                    return {i, j};
                }
            }
        }
        return {};
    }
};

// V2: Upper Triangular Pruning
class SolutionV2_UpperTrianglePruning {
public:
    std::vector<int> twoSum(const std::vector<int>& nums, int target) {
        int n = nums.size();
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                if (nums[i] + nums[j] == target) {
                    return {i, j};
                }
            }
        }
        return {};
    }
};

// V3: Two-Pass Hash Map
class SolutionV3_TwoPassHashMap {
public:
    std::vector<int> twoSum(const std::vector<int>& nums, int target) {
        std::unordered_map<int, int> lookup;
        int n = nums.size();

        for (int i = 0; i < n; ++i) {
            lookup[nums[i]] = i;
        }

        for (int i = 0; i < n; ++i) {
            int complement = target - nums[i];
            auto it = lookup.find(complement);
            if (it != lookup.end() && it->second != i) {
                return {i, it->second};
            }
        }
        return {};
    }
};

// V4: Single-Pass Interleaved Hash Map (Optimal Algorithm)
class SolutionV4_OnePassHashMap {
public:
    std::vector<int> twoSum(const std::vector<int>& nums, int target) {
        std::unordered_map<int, int> seen;
        int n = nums.size();

        for (int i = 0; i < n; ++i) {
            int complement = target - nums[i];
            auto it = seen.find(complement);
            if (it != seen.end()) {
                return {it->second, i};
            }
            seen[nums[i]] = i;
        }
        return {};
    }
};

// V5: Systems & Cache Optimized (Pre-allocated Buckets)
class SolutionV5_SystemsOptimized {
public:
    std::vector<int> twoSum(const std::vector<int>& nums, int target) {
        std::unordered_map<int, int> seen;
        seen.reserve(nums.size()); // Pre-allocate buckets to eliminate rehashing

        int n = nums.size();
        for (int i = 0; i < n; ++i) {
            int complement = target - nums[i];
            auto it = seen.find(complement);
            if (it != seen.end()) {
                return {it->second, i};
            }
            seen.emplace(nums[i], i);
        }
        return {};
    }
};

// Default alias
using Solution = SolutionV5_SystemsOptimized;
