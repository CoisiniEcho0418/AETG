# -*- coding:utf-8 -*-
import csv
import random
import itertools  # 排列组合的工具包


def test_jingdong():
    options = [
        '品牌',
        '能效等级',
        '支持IPv6',
        '类型',
        '处理器',
        '厚度',
        '机身材质',
        '内存容量',
        '屏幕尺寸',
        'Pairs',
    ]
    # options = ['品牌', '能效等级', '支持IPv6', '类型', 'Pairs']
    brand = [
        'hp',
        'thinkpad',
        'lenovo',
        'huawei',
        'apple',
        'dell',
        'asus',
        'haier',
        'honor',
        'acer',
        'mi',
        'mechrevo',
    ]
    power = ['一级能效', '二级能效', '三级能效', '五级能效']
    ipv6_support = ['yes', 'no']
    laptop_type = ['轻薄本', '游戏本', '高端轻薄本', '高端游戏本', '高性能轻薄本']
    cpu = [
        '麒麟',
        'AMD 速龙',
        'intel i5',
        '兆芯',
        '飞腾',
        '龙芯',
        'Apple M2',
        'intel i7',
        'intel i9',
        'intel i3',
        'AMD R5',
        'AMD R7',
        'AMD R9',
        'AMD R3',
        '高通',
        'Apple M1',
        'Apple M1 Pro',
        'Apple M1 Max',
        'intel 赛扬',
        'intel 至强',
        'intel 奔腾',
    ]
    thickness = ['15.0mm 及以下', '15.1-18.0mm', '18.1-20.0mm', '20.0mm 以上']
    material = ['金属', '金属+复合材质', '复合材质', '含碳纤维']
    memory = [
        '4GB',
        '6GB',
        '48GB',
        '8GB',
        '12GB',
        '16GB',
        '20GB',
        '24GB',
        '32GB',
        '36GB',
        '40GB',
        '64GB',
        '128GB',
    ]
    size = [
        '13.0英寸以下',
        '13.0-13.9英寸',
        '14.0-14.9英寸',
        '15.0-15.9英寸',
        '16.0-16.9英寸',
        '17英寸',
        '17.3英寸',
        '18.4英寸',
    ]

    test_factors = [
        len(brand),
        len(power),
        len(ipv6_support),
        len(laptop_type),
        len(cpu),
        len(thickness),
        len(material),
        len(memory),
        len(size),
    ]
    print("test_factors: " + str(test_factors))

    cover_array, cover_array_count = aetg(test_factors, 2)
    print("cover_array: " + str(cover_array))

    jd_csv = open("jingdong.csv", "w+", encoding='utf-8', newline='')
    jd_writer = csv.writer(jd_csv)
    jd_writer.writerow(options)

    for idx, array in enumerate(cover_array):
        final_cover_array = [
            brand[array[0]],
            power[array[1]],
            ipv6_support[array[2]],
            laptop_type[array[3]],
            cpu[array[4]],
            thickness[array[5]],
            material[array[6]],
            memory[array[7]],
            size[array[8]],
            cover_array_count[idx],
        ]
        jd_writer.writerow(final_cover_array)

    jd_csv.close()


def test_xiecheng():
    options = ['出发地', '目的地', '仅看直飞', '舱型', '乘客类型']
    start = ['国内', '国际·中国港澳台热门', '亚洲', '欧洲', '美洲', '非洲', '大洋洲']
    end = ['国内', '国际·中国港澳台热门', '亚洲', '欧洲', '美洲', '非洲', '大洋洲']
    direct_only = ['yes', 'no']
    board_type = ['经济/超经舱', '公务/头等舱', '公务舱', '头等舱']
    customer = ['仅成人', '成人与儿童', '成人与婴儿', '成人与儿童与婴儿']

    test_factors = [
        len(start),
        len(end),
        len(direct_only),
        len(board_type),
        len(customer),
    ]
    print("test_factors: " + str(test_factors))

    cover_array, cover_array_count = aetg(test_factors, 3)
    print("cover_array: " + str(cover_array))

    xc_csv = open("xiecheng.csv", "w+", encoding='utf-8', newline='')
    xc_writer = csv.writer(xc_csv)
    xc_writer.writerow(options)

    for idx, combination in enumerate(cover_array):
        final_cover_array = [
            start[combination[0]],
            end[combination[1]],
            direct_only[combination[2]],
            board_type[combination[3]],
            customer[combination[4]],
            cover_array_count[idx],
        ]
        xc_writer.writerow(final_cover_array)

    xc_csv.close()


def aetg(factors, t):
    num_factors = len(factors)
    # 生成所有 t-length 的 pairs 对，其形式如下：[ [-1,2,3,-1], [-1,2,4,-1],... ]
    uncovered_pairs = generate_all_t_size_pairs(factors, num_factors, t)
    # print("uncovered pairs")
    # for pairs in uncovered_pairs:
    #     print(str(pairs))

    m = 50  # 找M个候选项
    r = 10  # 重复R次找最小

    # 最优的cover array 和 对应的cover count
    optimal_cover_array = []
    optimal_cover_array_count = []

    for i in range(r):
        # 为了避免一次循环污染建模相关数据列表的初始值，每次循环都要copy一份，然后对这份内容进行操作
        # covered_pairs 和 uncovered_pairs 都是如下的形式[-1,-1,3,2,-1,1,-1]，-1代表未选择
        inner_covered_pairs = []  # 初始化为空
        inner_uncovered_pairs = uncovered_pairs.copy()  # 每次循环前都复制一份
        cover_array = []  # 每次循环产生的最终cover array
        cover_array_count = []  # 每次循环产生的对应cover array 每项的cover count
        # 循环填充直至全覆盖
        while len(inner_uncovered_pairs) > 0:
            print("uncovered pairs' length: " + str(len(inner_uncovered_pairs)))
            best_candidate_array_group = []  # 可能存在多个最优解，所以要设成列表取随机值
            max_cover_count = 0
            # 循环M次，选最优的候选项
            for j in range(m):
                factor_array = [-1] * num_factors  # 所有factor对应value取值列表（一个候选项，初始化全为-1）
                cover_count = 0  # 涵盖uncovered_pairs的数量，用于最后选出最优的判断依据
                # 先确定第一个factor和它对应的value
                first_factor_index, first_value = find_first_factor_and_value(
                    inner_uncovered_pairs, factors, num_factors
                )
                # print("First:" + str(first_factor_index) + " and" + str(first_value))
                factor_array[first_factor_index] = first_value
                selected_factors_cnt = 1  # 已经确定的factor的数量
                # 未被确定和已经确定的factor的集合（对应factors下标的列表）
                (
                    unselected_factors_group,
                    selected_factors_group,
                ) = find_unselected_and_selected_factors(factor_array)
                # 再确定剩下的factor
                while selected_factors_cnt < num_factors:
                    selected_factors_cnt += 1
                    next_factor_index = random.choice(unselected_factors_group)
                    if selected_factors_cnt <= t:
                        # 选出该参数最适合的值
                        best_value = find_best_value_for_small_condition(
                            inner_uncovered_pairs,
                            next_factor_index,
                            selected_factors_group,
                            factors,
                            factor_array,
                        )
                        factor_array[next_factor_index] = best_value
                        # 将下一个factor的index加入到selected_factors_group
                        selected_factors_group.append(next_factor_index)
                        # 从unselected_factors_group中删去next_factor_index
                        unselected_factors_group.remove(next_factor_index)
                        # selected_factors_cnt == T 时，也要计算cover_count
                        if selected_factors_cnt == t:
                            for pair in inner_uncovered_pairs:
                                is_include = True
                                for index in selected_factors_group:
                                    if pair[index] != factor_array[index]:
                                        is_include = False
                                        break
                                if is_include:
                                    cover_count += 1

                    else:
                        best_value, best_count = find_best_value_for_large_condition(
                            inner_uncovered_pairs,
                            next_factor_index,
                            selected_factors_group,
                            factors,
                            factor_array,
                            t,
                        )
                        factor_array[next_factor_index] = best_value
                        # 将下一个factor的index加入到selected_factors_group
                        selected_factors_group.append(next_factor_index)
                        # 从unselected_factors_group中删去next_factor_index
                        unselected_factors_group.remove(next_factor_index)
                        # 修改cover_count
                        cover_count += best_count

                if cover_count > max_cover_count:
                    # 清空原来的列表，重新赋值
                    best_candidate_array_group.clear()
                    best_candidate_array_group.append(factor_array)
                    max_cover_count = cover_count
                elif cover_count == max_cover_count:
                    best_candidate_array_group.append(factor_array)
            # 把每一次的最优候选项加入到最终的cover_array中
            best_candidate_array = random.choice(best_candidate_array_group)
            cover_array.append(best_candidate_array)
            cover_array_count.append(max_cover_count)
            # 修改 inner_uncovered_pairs 和 inner_covered_pairs
            for iucps in inner_uncovered_pairs:
                is_covered = True
                for index in range(num_factors):
                    if (
                        iucps[index] != -1
                        and iucps[index] != best_candidate_array[index]
                    ):
                        is_covered = False
                        break
                if is_covered:
                    # 使用循环删除包含相同元素的子列表
                    inner_uncovered_pairs = [
                        sublist for sublist in inner_uncovered_pairs if sublist != iucps
                    ]
                    inner_covered_pairs.append(iucps)

        # 输出当前循环的 cover_array 和 cover_array_count
        print(f"\nResults after {i + 1} iterations:")
        print("Cover Array and Count:")
        for idx, (array, count) in enumerate(zip(cover_array, cover_array_count)):
            print(f"{idx + 1}. {array} - {count}")

        # print("\nCover Array Count:")
        # for idx, count in enumerate(cover_array_count):
        #     print(f"{idx + 1}. {count}")

        # 比价R次的结果，选出所需要的覆盖组数最小的（这里不再采用随机，当出现多组最优解时，取第一组）
        if len(optimal_cover_array) == 0 or len(cover_array) < len(optimal_cover_array):
            optimal_cover_array = cover_array
            optimal_cover_array_count = cover_array_count

    # 输出最终的 cover_array 和 cover_array_count
    print("\nFinal Results:")
    print("Optimal Cover Array and Count:")
    for idx, (array, count) in enumerate(
        zip(optimal_cover_array, optimal_cover_array_count)
    ):
        print(f"{idx + 1}. {array} - {count}")

    # print("\nCover Array Count:")
    # for idx, count in enumerate(optimal_cover_array_count):
    #     print(f"{idx + 1}. {count}")

    return optimal_cover_array, optimal_cover_array_count


"""
    itertools.combinations():
    Return successive t-length combinations of elements in the iterable.
    combinations(range(4), 3) --> (0,1,2), (0,1,3), (0,2,3), (1,2,3)
"""


# 获取某一个整数列表的所有t个元素的组合，并以列表的形式返回
def get_combinations(lst, t):
    if t < 0 or t > len(lst):
        return []
    combinations = list(itertools.combinations(lst, t))
    return combinations


# 生成所有t-length的pairs
def generate_all_t_size_pairs(factors, num_factors, t):
    # 先生成 factors 下标取值的列表
    index_lst = []
    for i in range(num_factors):
        index_lst.append(i)
    # 调用 get_combinations() 来生成 t-length 的所有下标组合
    t_size_index_list = get_combinations(index_lst, t)
    # for indices in t_size_index_list:
    #     print(indices)
    # 存储最终返回的t-length的pairs对（也就是其中元素为列表的列表），其形式如下[ [-1,2,3,-1], [-1,2,4,-1],... ]
    t_size_pairs = []
    for indices in t_size_index_list:
        current_pair = []
        for i in range(num_factors):
            if i in indices:
                current_pair.append(list(range(factors[i])))
            else:
                current_pair.append([-1])
        t_size_pairs.extend(list(itertools.product(*current_pair)))

    return t_size_pairs


# 找到第一个参数和它的取值，使得其在未覆盖对集中出现频率最高，有可能会出现相同的情况，所以要随机取
def find_first_factor_and_value(uncovered_pairs, factors, num_factors):
    first_factor_index_group = []
    first_value_group = []
    max_count = 0
    for factor_index in range(num_factors):
        for value in range(factors[factor_index]):
            count = 0
            for pairs in uncovered_pairs:
                if pairs[factor_index] == value:
                    count += 1
            if count > max_count:
                # 先清空原列表再赋值
                first_factor_index_group.clear()
                first_value_group.clear()
                first_factor_index_group.append(factor_index)
                first_value_group.append(value)
                max_count = count
            elif count == max_count:
                first_factor_index_group.append(factor_index)
                first_value_group.append(value)

    first_factor_index = random.choice(first_factor_index_group)
    first_value = random.choice(first_value_group)
    return first_factor_index, first_value


# 找到剩余未被确定和已经确定的factor group
def find_unselected_and_selected_factors(factor_array):
    unselected_factors_group = []
    selected_factors_group = []
    for index, factor_value in enumerate(factor_array):
        if factor_value == -1:
            unselected_factors_group.append(index)
        else:
            selected_factors_group.append(index)
    return unselected_factors_group, selected_factors_group


# 寻找selected_factors_cnt<=t的情况下，factor的最佳取值
def find_best_value_for_small_condition(
    inner_uncovered_pairs,
    next_factor_index,
    selected_factors_group,
    factors,
    factor_array,
):
    max_include_count = 0  # 被uncovered_pairs包含的最大count
    best_value_group = []  # 可能存在重复的局部最优解，这时需要采用随机选取
    for value in range(factors[next_factor_index]):
        include_count = 0
        for uncovered_pair in inner_uncovered_pairs:
            if uncovered_pair[next_factor_index] == value:
                is_same = True  # 是否相同的标志
                for index in selected_factors_group:
                    if uncovered_pair[index] != factor_array[index]:
                        is_same = False
                        break
                if is_same:
                    include_count += 1
        if include_count > max_include_count:
            # 清空原来的列表，重新赋值
            best_value_group.clear()
            best_value_group.append(value)
            max_include_count = include_count
        elif include_count == max_include_count:
            best_value_group.append(value)
    best_value = random.choice(best_value_group)
    return best_value


# 寻找selected_factors_cnt>t的情况下，factor的最佳取值以及覆盖的pairs的值
def find_best_value_for_large_condition(
    inner_uncovered_pairs,
    next_factor_index,
    selected_factors_group,
    factors,
    factor_array,
    t,
):
    best_value_group = []  # 可能存在重复的局部最优解，这时需要采用随机选取
    max_count = 0
    # 获取selected_factors_group中所有t-1个元素的组合
    t_minus_one_size_index_list = get_combinations(selected_factors_group, t - 1)
    for value in range(factors[next_factor_index]):
        count = 0
        for index_list in t_minus_one_size_index_list:
            for pair in inner_uncovered_pairs:
                if pair[next_factor_index] == value:
                    is_include = True
                    for index in index_list:
                        if pair[index] != factor_array[index]:
                            is_include = False
                            break
                    if is_include:
                        count += 1

        if count > max_count:
            best_value_group.clear()
            best_value_group.append(value)
            max_count = count
        elif count == max_count:
            best_value_group.append(value)

    best_value = random.choice(best_value_group)
    return best_value, max_count


if __name__ == '__main__':
    # t=2 的测试用例：
    test_jingdong()

    # t=3 的测试用例：
    # test_xiecheng()

    # 普通测试用例
    # test_factors = [12, 4, 2, 21]
    # n = 2
    # aetg(test_factors, 2)
