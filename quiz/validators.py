import json

from django.core.exceptions import ValidationError


class ResultValidator:
    @staticmethod
    def validate_result_json(result):
        error_message = """Result must be a list of 24 integer values between \
         1 and 5"""
        result_list = json.loads(result)
        if isinstance(result_list, list) and len(result_list) == 24:
            for answer in result_list:
                if isinstance(answer, int) and 1 <= answer <= 5:
                    return json.dumps(result_list, ensure_ascii=False)
                raise ValidationError(error_message)
        raise ValidationError(error_message)
