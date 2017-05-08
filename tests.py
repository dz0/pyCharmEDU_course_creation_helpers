from test_helper import run_common_tests, failed, passed, get_answer_placeholders
from test_helper import check_placeholder

#### task:  if Number
def test_answer_placeholders():
    placeholders = get_answer_placeholders()

    check_placeholder(placeholders[0], 'money'
                      ,human_nr=3
                      
                      )


if __name__ == '__main__':
    run_common_tests()
    test_answer_placeholders()       # TODO: uncomment test call


