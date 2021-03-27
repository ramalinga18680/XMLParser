from lxml import etree
import sys


class TestCase():
    def __init__(self, ts_case_element, out=sys.stdout):
        self.req_id = ""
        self.test_case_id = ""
        self.result = ""
        self.test_pack = ""
        self.ts_case_element = ts_case_element
        self.num_total_steps = 0
        self.num_passed_test_steps = 0
        self.num_failed_test_steps = 0

    def find_test_caseid(self):
        elem_test_case_id = self.ts_case_element.find("./testCaseID")
        return elem_test_case_id.text

    def find_test_case_reqid(self):
        elem_test_case_req_id = self.ts_case_element.find("./requirementID")
        return elem_test_case_req_id.text

    def find_test_case_result(self):
        elem_test_case_result = self.ts_case_element.find("./result")
        return elem_test_case_result.text

    def find_test_pack_details(self):
        elem_test_pack_result = self.ts_case_element.find("./testPack")
        return elem_test_pack_result.text

    def find_test_steps(self):
        list_test_steps = self.ts_case_element.findall(".//TestStep")
        return list_test_steps

    def process_test_steps(self):
        list_steps = self.find_test_steps()
        self.num_total_steps = len(list_steps)
        for ts in list_steps:
            ts_result = ts.find("./result")
            if ts_result.text == "SUCCESS":
                ts_case_obj.num_passed_test_steps += 1
            elif ts_result.text == "FAILURE":
                ts_case_obj.num_failed_test_steps += 1


if __name__ == '__main__':
    tree = etree.parse(sys.argv[1])
    '''
    test_case_element = tree.find(".//TestCase")
    print(test_case_element)
    list_test_steps = test_case_element.findall(".//TestStep")
    print(len(list_test_steps))
    for ts in list_test_steps:
        ts_result = ts.find("./result")
        print("test case reult is", ts_result.text)
    '''

    list_test_case = tree.findall(".//TestCase")
    print("Num of test cases is", len(list_test_case))

    for ts_case in list_test_case:
        ts_case_obj = TestCase(ts_case)
        ts_case_obj.process_test_steps()
        print("test_pack : tc_id : tc_req_id : tc_result", ts_case_obj.find_test_caseid(),
              ts_case_obj.find_test_case_reqid(), ts_case_obj.find_test_case_result(),
              ts_case_obj.find_test_pack_details())
        print(" Total steps :%d passed steps : %d Failed test steps :%d" % (
        ts_case_obj.num_total_steps, ts_case_obj.num_passed_test_steps,
        ts_case_obj.num_failed_test_steps))
        ts_case_obj = None
    # print("test case reult is", ts_result.text)
    # print("test case reult is", ts_result.text)
