def get_constant(indicator_value):
    """
    Return constant for wrong indicator

    indicator is wrong when it is < 0 or > 100

    Example:
    indicator = -12

    if indicator < 0 then return abs(indicator_value)

    indicator + abs(min_indicator) = 0

    indicator = 105
    if indicator > 100 then return -(indicator % 100)
    -(indicator % 100) = 5
    indicator + -(indicator % 100) = 100


    :param int|float indicator_value: Indicator`s wrong value
    :return: int|float Constant for wrong indicator
    """
    if indicator_value < 0:
        return abs(indicator_value)
    return -(indicator_value % 100)


def check_group_indicators(group_indicator):
    """Return dictionary with correct indicators
    by adding constant

    if indicator is < 0 then constant is positive number
    and by adding constant this indicator become 0

    if is indicator is > 100 then constant is negative number
    and by adding constant this indicator become 100

    :param dict group_indicator: Dictionary with group indicators
    :return:dict Dictionary with correct indicators
    """
    for indicator in group_indicator:
        if not 0 < group_indicator[indicator] < 100:
            group_indicator[indicator] += get_constant(
                group_indicator[indicator])

    return group_indicator


def get_list_of_results(group_result):
    """
    Return list with lists of users answers
    each element of this list is list of user answer for each question

    :param list group_result: List with dictionaries of users in group results
    :return: list List with lists of users answers
    like [[first_user_fist_answer, first_user_second_answer, ...], ...]
    """
    list_of_answer = []
    for i in range(len(group_result)):
        list_of_answer.append([result['a_num'] for result in group_result[i]])
    return list_of_answer


def get_average_results(list_of_answer):
    """
    Return list of average for each answer
    each element in this list is average value for list inside list_of_answer

    :param list list_of_answer: List with lists of users answers
    :return: list List of average result for each answer
    """
    number_of_questions = 24
    avg_list = []
    for i in range(number_of_questions):
        avg_list.append(sum([result[i] for result in list_of_answer]) / len(
            list_of_answer))
    return avg_list


def get_indicators_values(answers_list):
    """
    Return value for each indicator by formulas

    PDI = 35(m07 – m02) + 25(m20 – m23) + C(pd)
    IDV = 35(m04 – m01) + 35(m09 – m06) + C(ic)
    MAS = 35(m05 – m03) + 35(m08 – m10) + C(mf)
    UAI = 40(m18 - m15) + 25(m21 – m24) + C(ua)
    LTO = 40(m13 – m14) + 25(m19 – m22) + C(ls)
    IVR = 35(m12 – m11) + 40(m17 – m16) + C(ir)

    Where C is a constant we use when indicator value is < 0 or > 100
    and C shift value between 0 and 100

    :param list answers_list: list of answers
    :return: dict dictionary with value for each indicator
    """
    group = {'pdi': round(35 * (answers_list[6] - answers_list[1]) + 25 * (
            answers_list[19] - answers_list[22]), 2),
             'idv': round(35 * (answers_list[3] - answers_list[0]) + 35 * (
                     answers_list[8] - answers_list[5]), 2),
             'mas': round(35 * (answers_list[4] - answers_list[2]) + 35 * (
                     answers_list[7] - answers_list[9]), 2),
             'uai': round(40 * (answers_list[17] - answers_list[14]) + 25 * (
                     answers_list[20] - answers_list[23]), 2),
             'lto': round(40 * (answers_list[12] - answers_list[13]) + 25 * (
                     answers_list[18] - answers_list[21]), 2),
             'ivr': round(35 * (answers_list[11] - answers_list[10]) + 40 * (
                     answers_list[16] - answers_list[15]), 2)}
    return group
