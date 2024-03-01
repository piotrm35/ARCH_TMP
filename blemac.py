# blemac
# version: 2

import os

#================================================================================================================
# setup:

# Android 8:
LOG_FOLDER_1 = '/storage/emulated/0/TMP/scan_log_1/'
LOG_FOLDER_2 = '/storage/emulated/0/TMP/scan_log_2/'
RESULT_PATH = '/storage/emulated/0/TMP/res.txt'

# Log files must have ".csv" extensions.

#================================================================================================================
# functions:

def get_mac_address_list_from_BLE_Scanner_history_log(log_file_path):
    f = open(log_file_path, mode='r', encoding='utf-8')
    lines_list = f.readlines()
    f.close()
    mac_address_list = []
    for line in lines_list:
        tx_list = line.split(',')
        if len(tx_list) >= 4 and tx_list[2].strip() != 'MacAddress':
            mac_address_list.append(tx_list[2].strip())
    return mac_address_list

def get_mac_address_list_from_BLE_Scanner_history_logs(log_file_path_list):
    res_list = []
    for log_file_path in log_file_path_list:
        res_list += get_mac_address_list_from_BLE_Scanner_history_log(log_file_path)
    return list(set(res_list))

# this function gets log files paths from subfolders as well
def get_log_path_list(root_folder, extension):
    res_list = []
    for (dir_path, dir_names, file_names) in os.walk(root_folder):
        res_list += [(dir_path.replace('\\', '/') + '/' + f).replace('//', '/') for f in file_names if os.path.splitext(f)[1].upper() == extension]
    return res_list

def print_res(tx):
    print(tx)
    if res_file:
        res_file.write(tx + '\n')

#================================================================================================================
# work:

log_file_paths_1 = get_log_path_list(LOG_FOLDER_1, '.CSV')
log_file_paths_2 = get_log_path_list(LOG_FOLDER_2, '.CSV')
mac_address_list_1 = get_mac_address_list_from_BLE_Scanner_history_logs(log_file_paths_1)
mac_address_list_2 = get_mac_address_list_from_BLE_Scanner_history_logs(log_file_paths_2)

res_file = open(RESULT_PATH, 'w')

print_res('\n\n=========================================')
print_res('common part of two mac address lists:')
print_res('\n')
common_part_of_two_mac_address_list = [el for el in mac_address_list_1 if el in mac_address_list_2]
for mac_address in set(common_part_of_two_mac_address_list):
    print_res(mac_address)

print_res('\n\n=========================================')
print_res('mac_address_list_1 - mac_address_list_2:')
print_res('\n')
diff_of_two_mac_address_list = [el for el in mac_address_list_1 if el not in mac_address_list_2]
for mac_address in set(diff_of_two_mac_address_list):
    print_res(mac_address)

if res_file:
    res_file.close()

print('SCRIPT END')
  
#================================================================================================================