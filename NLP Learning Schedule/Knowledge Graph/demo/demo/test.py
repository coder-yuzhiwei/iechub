import csv
import json
import pymysql

from collections import defaultdict


class Solution(object):
    def insertionSortList(self, array):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        # array = []
        # if head is None:
        #     return head
        # while head:
        #     array.append(head.val)
        #     head = head.next
        for i in range(1, len(array)):
            flag = i
            tmp = array[flag]
            while flag >= 0:
                if tmp < array[flag-1] and flag != 0:
                    array[flag] = array[flag-1]
                    flag -= 1
                else:
                    array[flag] = tmp
                    break
        print(array)
        return array


if __name__ == '__main__':
    print(Solution().insertionSortList([4,2,1,3,5,8,9,21]))
    # conn = pymysql
