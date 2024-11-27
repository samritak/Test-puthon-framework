import pytest, time
import importlib

# Test that runs for dynamically imported classes
@pytest.mark.nondestructive
def test_aarp_test_dynamic(cls):
    instance = cls()
    instance.test_run_test_case()
    time.sleep(15)

# Hook for dynamically generating tests
def pytest_generate_tests(metafunc):
    if "cls" in metafunc.fixturenames:
        test_names_input = metafunc.config.getoption("inputtests")
        print(test_names_input)
        test_names = ''.join(test_names_input)
        tests = test_names.split(',')
        print("TESTS TO EXEC")
        print(test_names)
        classes = []
        for test in tests:
            test = "test_" + test.replace("-", "_")
            test_name = importlib.import_module(test)
            class_name = test.replace("_", " ").title()
            class_name = class_name.replace(" ", "")
            cls = getattr(test_name, class_name)
            classes.append(cls)
        metafunc.parametrize("cls", classes)

