"https://leetcode.com/problems/reverse-integer/?tab=Description"
class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        str_int=str(x)
        if str_int[0]=="-":
            str_int=str_int+"-"
            str_int=str_int[1:]
            str_int=str_int[::-1]
        else:
            str_int=str_int[::-1]
        if str_int<-2147483648 and str_int>2147483647:
            return 0
        return str_int
solution=Solution()
print solution.reverse(123)
