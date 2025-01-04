def merge_sort_with_custom_order(arr):
    def merge_sort(arr, indices, left, right):
        if right - left > 1:
            mid = (left + right) // 2
            merge_sort(arr, indices, left, mid)
            merge_sort(arr, indices, mid, right)
            merge(arr, indices, left, mid, right)

    def merge(arr, indices, left, mid, right):
        left_half = arr[left:mid]
        right_half = arr[mid:right]
        left_indices = indices[left:mid]
        right_indices = indices[mid:right]

        i = j = 0
        k = left
        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                arr[k] = left_half[i]
                indices[k] = left_indices[i]
                i += 1
            else:
                arr[k] = right_half[j]
                indices[k] = right_indices[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            indices[k] = left_indices[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            indices[k] = right_indices[j]
            j += 1
            k += 1

    n = len(arr) // 2
    indices = list(range(len(arr)))

    # 对整个数组进行归并排序，并获取排序后的序数
    merge_sort(arr, indices, 0, len(arr))

    # 创建序数列表
    ranks = [0] * len(arr)
    for rank, index in enumerate(indices):
        ranks[index] = rank  # 修改为从0开始

    # 使用归并排序对前 n 项和后 n 项分别排序
    merge_sort(ranks, indices, 0, n)  # 排序前 n 项
    merge_sort(ranks, indices, n, len(arr))  # 排序后 n 项

    return ranks

"""
arr = [0, 3, 4, 6, 8, 10, 1, 2, 5, 7, 9, 11]
print(merge_sort_with_custom_order(arr))  # 输出: [2, 3, 1, 4, 2, 3]
"""
# 示例

