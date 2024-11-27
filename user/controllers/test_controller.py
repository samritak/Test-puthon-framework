from user.models.test import Test


def get_all_tests():
    return Test.query.order_by(Test.id.desc()).limit(10)

def get_aarp_tests():
    aarp_tests = Test.query.filter(Test.test_ticket.like('AARP%')).order_by(Test.id.desc()).limit(10)
    return aarp_tests
