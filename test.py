import unittest
import os
from fileUpload import form_argument
from inspectStats import get_content, read_summary_file, summary_dictionary, inspect_summary


class Testing(unittest.TestCase):

    # def form_argument(var):
    #     passed_argument = ''
    #     for i in range(1, len(var)):
    #         passed_argument += var[i]
    #         passed_argument += ' '
    #     return passed_argument

    def test_form_argument_equal(self):
        self.assertEqual(form_argument(['python', 'laba', 'diena']), 'laba diena ')
        self.assertEqual(form_argument(['2', '3', '4']), '3 4 ')
        self.assertEqual(form_argument(['SUMMARY', 'Raw_data_dumps']), 'Raw_data_dumps ')

    def test_form_argument_not_equal(self):
        self.assertNotEqual(form_argument(['SUMMARY', 'Raw_data_dumps']), 'Raw_data_dumps')
        self.assertNotEqual(form_argument(['SUMMARY', 'Raw_data_dumps', 'Raw_data_files']), 'laba diena ')

    def test_form_argument_is_none(self):
        self.assertIsNone(form_argument(['hi']), "Test value is none.")

    # ---------------------------------------------------------------------------------------------------------------

    # # funkcija failo turinio informacijai perskiatyti
    # def get_content(tempdir, new_name):
    #     os.chdir(os.path.join(tempdir + '/' + new_name))
    #     with open("SUMMARY", "r") as f:
    #         content = f.read()
    #     return content

    def test_get_content_existent_file(self):
        f = open(r"D:\Users\Arnas\Desktop\scriptnew\upload_files\diagnose_20220426.154240\SUMMARY", "r")
        content = f.read()
        self.assertIsNotNone(content, "Test value is none.")
        self.assertEqual(get_content(r'D:\Users\Arnas\Desktop\scriptnew\upload_files', 'diagnose_20220426.154240'), content)
        self.assertNotEqual(get_content(r'D:\Users\Arnas\Desktop\scriptnew\upload_files', 'diagnose_20220426.073045'), content)

    def test_get_content_none_existent_file(self):
        content = None
        self.assertIsNone(content, "Test value is none.")
        self.assertNotEqual(get_content(r'D:\Users\Arnas\Desktop\scriptnew\upload_files', 'diagnose_20220426.154240'), content)

    # ---------------------------------------------------------------------------------------------------------------

    # funkcija summary failo perskaitymui - perskaito ir isaugo eilutes su konkreciomis reiksmemis jose
    # def read_summary_file(tempdir, new_name):
    #     os.chdir(os.path.join(tempdir + '/' + new_name))

    #     open_read = open('SUMMARY', 'r')
    #     wanted_values = ['BOARD', 'FIRMUX', 'BUILD', 'LOAD', 'RAM', 'print', 'UPTIME']
    #     summary_file_content = []

    #     for line in open_read:
    #         for value in wanted_values:
    #             if value in line:
    #                 summary_file_content.append(line)     
    #     return summary_file_content

    def test_read_summary_file(self):
        f = open(r"D:\Users\Arnas\Desktop\scriptnew\upload_files\diagnose_20220426.154240\SUMMARY", "r")
        content = f.read()
        self.assertNotEqual(read_summary_file(r"D:\Users\Arnas\Desktop\scriptnew\upload_files', 'diagnose_20220426.154240'), content)

    def test_read_summary_file_key_values(self):
        content = read_summary_file(r'D:\Users\Arnas\Desktop\scriptnew\upload_files', 'diagnose_20220426.154240')
        self.assertIn('BOARD', content[0])
        self.assertIn('FIRMUX', content[1])
        self.assertIn('BUILD', content[2])
        self.assertIn('LOAD', content[3])
        self.assertIn('RAM', content[4])
        self.assertIn('UPTIME', content[5])

    def test_read_summary_file_not_key_values(self):
        content = read_summary_file(r'D:\Users\Arnas\Desktop\scriptnew\upload_files', 'diagnose_20220426.154240')
        self.assertNotIn('BOARD', content[1])
        self.assertNotIn('RAM', content[5])
        self.assertNotIn('print', content[5])

    # ---------------------------------------------------------------------------------------------------------------

    # funkcija summary failo analizei - isrenka aktualia informacija pagal raktines reiksmes
    # def summary_dictionary(tempdir, new_name):
    #     summary_file_content = read_summary_file(tempdir, new_name)
    #     summary_dict = {}
        
    #     size = len(summary_file_content)
    #     for i in range(size):
    #         partitioned_string = summary_file_content[i].partition('=')
    #         summary_dict[partitioned_string[0]] = partitioned_string[2]
    #         if partitioned_string[0] == 'LOAD':
    #             summary_dict['CPU LOAD'] = summary_dict.pop('LOAD')
    #     return summary_dict

    def test_summary_dictionary_existent_file(self):
        f = open(r'D:\Users\Arnas\Desktop\scriptnew\upload_files\diagnose_20220426.154240\SUMMARY", "r")
        content = f.read()
        # self.assertEqual(summary_dictionary(r'D:\Users\Arnas\Desktop\scriptnew\upload_files', 'diagnose_20220426.154240'), content)
        self.assertNotEqual(summary_dictionary(r'D:\Users\Arnas\Desktop\scriptnew\upload_files', 'diagnose_20220426.154240'), content)

    def test_summary_dictionary_none_existent_file(self):
        content = summary_dictionary(r'D:\Users\Arnas\Desktop\scriptnew\upload_files', 'diagnose_20220426.154240')
        keys = [k for k, v in content.items() if v == '0.25 0.13 0.12 1/104 2107\n']
        self.assertNotIn('LOAD', keys)
        self.assertIn('CPU LOAD', keys)

    # ---------------------------------------------------------------------------------------------------------------

    # funkcija ram ir cpu reiksmem grazinti
    # def inspect_summary(tempdir, new_name):
    #     summary_dict = summary_dictionary(tempdir, new_name)
        
    #     for j in summary_dict:
    #         if j == 'RAM':
    #             ram_kb =  summary_dict[j].partition(' ')
    #         if j == 'CPU LOAD':
    #             cpu_load = summary_dict[j].split(' ')
        
    #     return ram_kb, cpu_load

    def test_inspect_summary_existent_file(self):
        f = open(r"D:\Users\Arnas\Desktop\scriptnew\upload_files\diagnose_20220426.154240\SUMMARY", "r")
        content = f.read()
        # self.assertEqual(summary_dictionary(r'D:\Users\Arnas\Desktop\scriptnew\upload_files', 'diagnose_20220426.154240'), content)
        self.assertNotEqual(inspect_summary(r'D:\Users\Arnas\Desktop\scriptnew\upload_files', 'diagnose_20220426.154240'), content)

    def test_inspect_summary_none_existent_file(self):
        ram_kb, cpu_load = inspect_summary(r'D:\Users\Arnas\Desktop\scriptnew\upload_files', 'diagnose_20220426.154240')
        content = summary_dictionary(r'D:\Users\Arnas\Desktop\scriptnew\upload_files', 'diagnose_20220426.154240')
        ram_kb_str = "".join([str(item) for item in ram_kb])
        cpu_load_str = " ".join([str(item) for item in cpu_load])

        self.assertEqual(ram_kb_str, content['RAM'])
        self.assertEqual(cpu_load_str, content['CPU LOAD'])


if __name__ == '__main__':
    unittest.main()