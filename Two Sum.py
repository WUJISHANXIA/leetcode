"https://leetcode.com/problems/two-sum/?tab=Description"
"2017.2.26"
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for index,item in enumerate(nums):
            start_index=index
            end_index=False
            for target_value_index,target_value in enumerate(nums[start_index+1:]):
                if target-item==target_value:
                    end_index=target_value_index+start_index+1
                    break
            if end_index!=False:
                break
        return [start_index,end_index]
solution=Solution()
nums=[2, 7, 11, 15,16]
target=23
rtype=solution.twoSum(nums,target)
print rtype