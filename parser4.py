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
        self.ignition_failure = False
        self.verify_audio_failure = False

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

    def check_if_audio_failure(self, test_step):
        ts_command = test_step.find("./command").text
        # print("ts_command is",ts_command)
        if "VERIFY_AUDIO" in ts_command:
            return True
        return False

    def process_test_steps(self):
        list_steps = self.find_test_steps()
        self.num_total_steps = len(list_steps)
        for ts in list_steps:
            ts_result = ts.find("./result")
            if ts_result.text == "SUCCESS":
                ts_case_obj.num_passed_test_steps += 1
            elif ts_result.text == "FAILURE":
                ts_case_obj.num_failed_test_steps += 1
                self.verify_audio_failure = self.check_if_audio_failure(ts)

    def find_function_units(self):
        list_function_units = self.ts_case_element.findall("./functionUnit")
        # print("len of func units is ",len(list_func_units))
        return list_function_units

    def process_func_units(self):
        elements = ('functionUnitName', 'functionUnitResult')
        list_f_units = self.find_function_units()
        for f_unit in list_f_units:
            f_uname = f_unit.find(elements[0])
            f_result = f_unit.find(elements[1])
            self.check_if_func_unit_has_ignition(f_uname, f_result)

    def check_if_func_unit_has_ignition(self, func_unit_name, func_unit_result):
        if "Ignition" in func_unit_name.text:
            print("Func unit name ", func_unit_name.text, func_unit_result.text)
            if func_unit_result.text == "FAILURE":
                self.ignition_failure = True


if __name__ == '__main__':
    tree = etree.parse(sys.argv[1])

    list_test_case = tree.findall(".//TestCase")
    print("Num of test cases is", len(list_test_case))

    for ts_case in list_test_case:
        ts_case_obj = TestCase(ts_case)
        ts_case_obj.process_test_steps()
        ts_case_obj.process_func_units()

        print("test_pack : tc_id : tc_req_id : tc_result", ts_case_obj.find_test_caseid(),
              ts_case_obj.find_test_case_reqid(), ts_case_obj.find_test_case_result(),
              ts_case_obj.find_test_pack_details())
        print(" Total steps :%d passed steps : %d Failed test steps :%d has ignition failure %d" % (
            ts_case_obj.num_total_steps, ts_case_obj.num_passed_test_steps,
            ts_case_obj.num_failed_test_steps, ts_case_obj.ignition_failure))
        if ts_case_obj.verify_audio_failure:
            print("Audio verification failed")

        # list_func_units = ts_case.xpath('./functionUnit[functionUnitName[contains(text(),"Ignition")]]')
        ts_case_obj = None
