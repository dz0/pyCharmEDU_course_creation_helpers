from test_helper import run_common_tests, failed, passed, get_answer_placeholders
from test_helper_4automation import check_placeholder

#### task: $name
def test_answer_placeholders():
    placeholders = get_answer_placeholders()

    # placeholder tests
$rendered_children

if __name__ == '__main__':
    run_common_tests()
    test_answer_placeholders()       # TODO: uncomment test call

