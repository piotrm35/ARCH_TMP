# blemac
# version: 6

import os

#================================================================================================================
# setup:

# Log files must have ".csv" extensions.

# Android 8:
LOG_FOLDER_1 = '/storage/emulated/0/TMP/scan_log_1/'
LOG_FOLDER_2 = '/storage/emulated/0/TMP/scan_log_2/'
RESULT_PATH = '/storage/emulated/0/TMP/res.txt'
RESULT_LIMIT = 10

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
        res_list += [os.path.join(dir_path, f) for f in file_names if os.path.splitext(f)[1].upper() == extension]
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
common_part_mac_address_list = [el for el in mac_address_list_1 if el in mac_address_list_2]
common_part_mac_address_set = set(common_part_mac_address_list)
i = 1
for mac_address in common_part_mac_address_set:
    if i <= RESULT_LIMIT:
        print_res(str(i) + ') ' + mac_address)
        i += 1
    else:
        print_res('AND ' + str(len(common_part_mac_address_set) - RESULT_LIMIT) + ' MORE...')
        break

print_res('\n\n=========================================')
print_res('mac_address_list_1 - mac_address_list_2:')
print_res('\n')
diff_mac_address_list = [el for el in mac_address_list_1 if el not in mac_address_list_2]
diff_mac_address_set = set(diff_mac_address_list)
i = 1
for mac_address in diff_mac_address_set:
    if i <= RESULT_LIMIT:
        print_res(str(i) + ') ' + mac_address)
        i += 1
    else:
        print_res('AND ' + str(len(diff_mac_address_set) - RESULT_LIMIT) + ' MORE...')
        break

if res_file:
    res_file.close()

print('\n\nSCRIPT END')
  
#================================================================================================================
