from collections import Counter


class Solution(object):
    def findDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        c = Counter(nums)
        return c.most_common(1)[0][0]
