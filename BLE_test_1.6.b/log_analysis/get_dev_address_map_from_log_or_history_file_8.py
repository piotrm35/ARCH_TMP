import time, datetime
import os


DEV_ADDRESS_MAP_FILE_PATH_PREFIX = './DEV_ADDRESS_MAP_'
dev_address_map = {}
DESC_TX = 'test'


def get_current_datetime_str():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%d_%m_%Y_%H_%M_%S')


def get_dev_address_list_from_BLE_test_log(log_file_path):
    print('function get_dev_address_list_from_BLE_test_log: ' + log_file_path)
    f = open(log_file_path, mode='r', encoding='utf-8')
    lines_list = f.readlines()
    f.close()
    i = 1
    dev_address_list = []
    for line in lines_list:
        tx_list = line.split(' -> ')
        if len(tx_list) > 1:
##            print(str(i) + ')\t' + line.strip())
            dev_address_list.append(tx_list[1].split(',')[0])
            i += 1
    return dev_address_list


def get_dev_address_list_from_BLE_test_logs(log_file_path_list):
    res_list = []
    for log_file_path in log_file_path_list:
        res_list += get_dev_address_list_from_BLE_test_log(log_file_path)
    return list(set(res_list))


def get_dev_address_list_from_BLEScanner_history(log_file_path):
    print('function get_dev_address_list_from_BLEScanner_history: ' + log_file_path)
    f = open(log_file_path, mode='r', encoding='utf-8')
    lines_list = f.readlines()
    f.close()
    i = 1
    dev_address_list = []
    for line in lines_list:
        tx_list = line.split(',')
        if len(tx_list) == 5 and tx_list[2][2] == ':':
##            print(str(i) + ')\t' + line.strip())
            dev_address_list.append(tx_list[2])
            i += 1
    return dev_address_list


def get_dev_address_list_from_BLEScanner_histories(log_file_path_list):
    res_list = []
    for log_file_path in log_file_path_list:
        res_list += get_dev_address_list_from_BLEScanner_history(log_file_path)
    return list(set(res_list))


def get_dev_address_list_from_Bluetooth_4_0_Scanner_log_CSV(log_file_path):
    print('function get_dev_address_list_from_Bluetooth_4_0_Scanner_log_CSV: ' + log_file_path)
    f = open(log_file_path, mode='r', encoding='utf-8')
    lines_list = f.readlines()
    f.close()
    i = 1
    dev_address_list = []
    for line in lines_list:
        tx_list = line.split(',')
        if len(tx_list) >= 4 and tx_list[3] != 'deviceAddress':
##            print(str(i) + ')\t' + line.strip())
            dev_address_list.append(tx_list[3])
            i += 1
    return dev_address_list


def get_dev_address_list_from_Bluetooth_4_0_Scanner_log_CSVs(log_file_path_list):
    res_list = []
    for log_file_path in log_file_path_list:
        res_list += get_dev_address_list_from_Bluetooth_4_0_Scanner_log_CSV(log_file_path)
    return list(set(res_list))


# this function gets log files paths from subfolders as well
def get_log_path_list(root_folder, extension):      # log_file_paths = get_log_path_list('./', '.TXT')
    res_list = []
    for (dir_path, dir_names, file_names) in os.walk(root_folder):
        res_list += [(dir_path.replace('\\', '/') + '/' + f).replace('//', '/') for f in file_names if os.path.splitext(f)[1].upper() == extension]
    return res_list


#================================================================================================================
# setup:


dev_address_list = get_dev_address_list_from_BLE_test_log('../arch_log/total_number_dev_logs_05.08.2022-06_39_26.txt')


#================================================================================================================


print('\n\n==========================\n\n')
dev_address_list = list(set(dev_address_list))  # duplicates remove
i = 1
for dev_address in dev_address_list:
    dev_address_map[dev_address] = DESC_TX
    print(str(i) + ')\t' + dev_address)
    i += 1


print('\n\n==========================\n\n')
dev_address_map_str = str(dev_address_map)
dev_address_map_str = dev_address_map_str.replace('{', '{\n\t\t')
dev_address_map_str = dev_address_map_str.replace(', ', ', \n\t\t')
dev_address_map_str = dev_address_map_str.replace('}', '\n\t}')
print('DEV_ADDRESS_MAP = ' + dev_address_map_str)
f = open(DEV_ADDRESS_MAP_FILE_PATH_PREFIX + get_current_datetime_str() + '.txt', 'w')
f.write('DEV_ADDRESS_MAP = ' + dev_address_map_str)
f.close()
