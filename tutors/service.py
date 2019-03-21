from tutors.models import Questions, Answers

__all__ = ['get_min_missing_value', 'get_numbers', ]


def get_min_missing_value(model, filter_id):
    """
    Function looks for the least missed value of the number to the question
    in the test among the created questions.
    :return: minimum missing value
    """
    list_of_number = get_numbers(model, filter_id)
    if not list_of_number:
        return 1
    max_value = int(max(list_of_number))
    for value in range(1, max_value + 1):
        if value not in list_of_number:
            return value
    return max_value + 1


def get_numbers(model, filter_id):
    """
    :return: values from column 'question_number'/ 'answer_number' as a
    tuple of values.
    """
    if isinstance(model, Questions):
        return list(Questions.objects.filter(quiz=filter_id).values_list(
            'question_number', flat=True).order_by('question_number'))
    return list(Answers.objects.filter(question=filter_id).values_list(
        'answer_number', flat=True).order_by('answer_number'))
