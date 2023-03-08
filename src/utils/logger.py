import os
import json
import allure
from random import randint
from allure import attachment_type


class Logs:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    RESULT_DIR = 'results_reports'
    LOGS_DIR = 'logs'
    LOGS_DIR_PATH = os.path.join(BASE_DIR, RESULT_DIR, LOGS_DIR)

    def __init__(self, web_browser):
        self.browser = web_browser

    def get_recursively(self, search_dict, field):
        """
        Takes a dict with nested lists and dicts,
        and searches all dicts for a key of the field
        provided.
        """
        fields_found = []

        for key, value in search_dict.items():

            if key == field:
                fields_found.append(value)

            elif isinstance(value, dict):
                results = self.get_recursively(value, field)
                for result in results:
                    fields_found.append(result)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        more_results = self.get_recursively(item, field)
                        for another_result in more_results:
                            fields_found.append(another_result)
        return fields_found

    def get_log_browser(self, type_log):
        type_logs = ["performance", 'browser', 'driver']
        return self.browser.get_log(type_logs[type_log])

    def process_browser_log_entry(self, entry):
        response = json.loads(entry['message'])
        return response

    def sorting_logs_browser(self, logs):
        events = [self.process_browser_log_entry(entry) for entry in logs]
        sorting_json = []
        for line in events:
            if "XHR" in self.get_recursively(line, 'type'):
                try:
                    if len(self.get_recursively(line, 'Authorization')) > 0:
                        var = {"request": {
                            'Authorization': line['message']['params']['request']['headers']['Authorization'],
                            'timestamp': line['message']['params']['timestamp']},
                               'type': "XHR"}
                        sorting_json.append(var)
                    if len(self.get_recursively(line, 'response')) > 0:
                        var = {"response": {'url': line['message']['params']['response']['url'],
                                            'status': line['message']['params']['response']['status'],
                                            'timestamp': line['message']['params']['timestamp']},
                               'type': "XHR"}
                        sorting_json.append(var)
                    if len(self.get_recursively(line, 'request')) > 0:
                        var = {"request": {'url': line['message']['params']['request']['url'],
                                           'method': line['message']['params']['request']['method'],
                                           'timestamp': line['message']['params']['timestamp']},
                               'type': "XHR"}
                        sorting_json.append(var)
                except KeyError:
                    pass
        return sorting_json

    def write_log_browser(self, type_log=1):
        """
        :param type_log: Тип записанных логов. 1 - все логи, 2 - логи консоли, 3 - остортированные логи
        :return:
        """
        if type_log == 1:
            logs = self.get_log_browser(type_log=0)
            path_logs = os.path.join(Logs.LOGS_DIR_PATH, f"{randint(0, 99999)}_all_logs.json")
            logs_write_to_write = self.sorting_logs_browser(logs)
            self.write_logs(logs_write_to_write, path_logs)
            allure.attach.file(source=path_logs, name='Полные_логи',  attachment_type=attachment_type.JSON)
            return path_logs
        elif type_log == 2:
            logs = self.get_log_browser(type_log=1)
            path_logs = os.path.join(Logs.LOGS_DIR_PATH, f"{randint(0, 99999)}_console_logs.json")
            self.write_logs(logs, path_logs)
            allure.attach.file(source=path_logs, name='Логи консоли',  attachment_type=attachment_type.JSON)
            return path_logs

    def write_logs(self, logs, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)
            f.close()