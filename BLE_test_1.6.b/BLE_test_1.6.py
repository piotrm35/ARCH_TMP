import os
import time, datetime
import asyncio
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


try:
    from aux_maps.DEV_MAP import DEV_ADDRESS_MAP
except:
    print('EXCEPTION: DEV_ADDRESS_MAP = {}')
    DEV_ADDRESS_MAP = {}
dev_address_map_keys = list(DEV_ADDRESS_MAP.keys())

try:
    from aux_maps.DEV_MAP import DEV_ADVERTISEMENT_DATA_MAP
except:
    print('EXCEPTION: DEV_ADVERTISEMENT_DATA_MAP = {}')
    DEV_ADVERTISEMENT_DATA_MAP = {}
dev_advertisement_data_map_keys = list(DEV_ADVERTISEMENT_DATA_MAP.keys())

try:
    from aux_maps.UUIDS_DESCRIPTION_MAP import UUIDS_DESCRIPTION_MAP
except:
    print('EXCEPTION: UUIDS_DESCRIPTION_MAP = {}')
    UUIDS_DESCRIPTION_MAP = {}
uuids_description_map_keys = list(UUIDS_DESCRIPTION_MAP.keys())

devices_dict = {}
first_dev_log_time_list = []
first_dev_log_idx = 1
total_number_logs_dict = {}
FIRST_DEV_LOG_MAX_DELAY = 5
MAX_UNIQUE_KEY_IDX = 5
TOTAL_NUMBER_DEV_LOGS_CHANGE_FILE_PERIOD = 1 * 60
last_total_number_dev_logs_change_timestamp = time.time()
script_start_datetime_str = None
match_ind_dict = {}


def simple_callback(device: BLEDevice, advertisement_data: AdvertisementData):
    global first_dev_log_idx
    advertisement_data_str = str(advertisement_data)
    advertisement_data_str = get_normalized_advertisement_data_str(advertisement_data_str)
    device_name = str(device.name).replace('None', '-')
    known_name = '-'
    if device.address in dev_address_map_keys:
        known_name = ':' + DEV_ADDRESS_MAP[device.address] + ':'
    else:
        known_name = get_known_name_from_advertisement_data_match(advertisement_data_str)
    advertisement_data_str = add_uuid_description_to_advertisement_data_str(advertisement_data_str)
    if device.address not in first_dev_log_time_list:
        f = open(FIRST_DEV_LOG_TIME_FILE_PATH, 'a')
        f.write(
                str(first_dev_log_idx) + ') ' +
                get_current_time_str() + ' -> ' +
                device.address + ', ' +
                str(device.rssi) + ', ' +
                device_name + ', ' +
                known_name + ', ' +
                advertisement_data_str +
                '\n'
            )
        f.close()
        first_dev_log_idx += 1
        first_dev_log_time_list.append(device.address)
    total_number_logs_dict_keys = list(total_number_logs_dict.keys())
    if device.address not in total_number_logs_dict_keys:
        total_number_logs_dict[device.address] = {
                'max_RSSI': device.rssi,
                'first_log_datatime': get_current_datetime_str(),
                'last_log_datetime': get_current_datetime_str(),
                'log_count': 1,
                'device_name': device_name,
                'known_name': known_name,
                'advertisement_data': advertisement_data_str
            }
    else:
        if total_number_logs_dict[device.address]['max_RSSI'] < device.rssi:
            total_number_logs_dict[device.address]['max_RSSI'] = device.rssi
        total_number_logs_dict[device.address]['log_count'] += 1
        if total_number_logs_dict[device.address]['device_name'] == '-':
            total_number_logs_dict[device.address]['device_name'] = device_name
        if len(total_number_logs_dict[device.address]['known_name']) < len(known_name):
            total_number_logs_dict[device.address]['known_name'] = known_name
        total_number_logs_dict[device.address]['last_log_datetime'] = get_current_datetime_str()
        stored_advertisement_data_dict = get_advertisement_data_dict(total_number_logs_dict[device.address]['advertisement_data'])
        stored_advertisement_data_dict_keys = list(stored_advertisement_data_dict.keys())
        stored_advertisement_data_dict_values = list(stored_advertisement_data_dict.values())
        new_advertisement_data_dict = get_advertisement_data_dict(advertisement_data_str)
        new_advertisement_data_dict_keys = list(new_advertisement_data_dict.keys())
        for new_advertisement_data_dict_key in new_advertisement_data_dict_keys:
            if new_advertisement_data_dict[new_advertisement_data_dict_key] not in stored_advertisement_data_dict_values:
                unique_key_idx = get_unique_key_idx_in_list(new_advertisement_data_dict_key, stored_advertisement_data_dict_keys)
                if unique_key_idx <= MAX_UNIQUE_KEY_IDX:
                    if unique_key_idx == 0:
                        total_number_logs_dict[device.address]['advertisement_data'] += ', ' + new_advertisement_data_dict_key + '=' + new_advertisement_data_dict[new_advertisement_data_dict_key]
                    elif unique_key_idx == MAX_UNIQUE_KEY_IDX:
                        total_number_logs_dict[device.address]['advertisement_data'] += ', ' + new_advertisement_data_dict_key + '_MAX_UNIQUE_KEY_IDX=' + new_advertisement_data_dict[new_advertisement_data_dict_key]
                    else:
                        total_number_logs_dict[device.address]['advertisement_data'] += ', ' + new_advertisement_data_dict_key + '_' + str(unique_key_idx) + '=' + new_advertisement_data_dict[new_advertisement_data_dict_key]
    devices_dict[device.address] = {
            'RSSI': device.rssi,
            'device_name': device_name,
            'known_name': known_name,
            'timestamp': time.time(),
            'advertisement_data': advertisement_data_str
        }


async def main(service_uuids):
    global last_total_number_dev_logs_change_timestamp
    scanner = BleakScanner(service_uuids=service_uuids)
    scanner.register_detection_callback(simple_callback)
    while True:
        await scanner.start()
        await asyncio.sleep(1.0)
        await scanner.stop()
        devices_dict_keys = list(devices_dict.keys())
        for key in devices_dict_keys:
            delay = int(time.time() - devices_dict[key]['timestamp'])
            if delay > FIRST_DEV_LOG_MAX_DELAY:
                del devices_dict[key]
            elif delay > 1:
                devices_dict[key]['RSSI'] = 'N/S'
        devices_dict_keys = list(devices_dict.keys())
        devices_dict_keys.sort(key=devices_dict_sort_by_RSSI_func, reverse=True)
        i = 1
        os.system('cls')
        print(get_current_time_str())
        for key in devices_dict_keys:
            print(
                    str(i) + ') -> ' +
                    key + ', ' +
                    str(devices_dict[key]['RSSI']) + ', ' +
                    str(devices_dict[key]['device_name']) + ', ' +
                    str(devices_dict[key]['known_name']) + ', ' +
                    str(devices_dict[key]['advertisement_data'])
                )
            i += 1
        if time.time() - last_total_number_dev_logs_change_timestamp > TOTAL_NUMBER_DEV_LOGS_CHANGE_FILE_PERIOD:
            total_number_logs_dict_keys = list(total_number_logs_dict.keys())
            total_number_logs_dict_keys.sort(key=total_number_logs_dict_sort_by_log_count_func, reverse=True)
            i = 1
            f = open(TOTAL_NUMBER_DEV_LOGS_FILE_PATH, 'w')
            f.write('START: ' + script_start_datetime_str + '\n')
            f.write('STOP: ' + get_current_datetime_str() + '\n\n')
            for key in total_number_logs_dict_keys:
                f.write(
                        str(i) + ') -> ' +
                        key + ', ' +
                        str(total_number_logs_dict[key]['max_RSSI']) + ', ' +
                        '[' +  str(total_number_logs_dict[key]['first_log_datatime']) + '], ' +
                        '[' +  str(total_number_logs_dict[key]['last_log_datetime']) + '], ' +
                        str(total_number_logs_dict[key]['log_count']) + ', ' +
                        str(total_number_logs_dict[key]['device_name']) + ', ' +
                        str(total_number_logs_dict[key]['known_name']) + ', ' +
                        str(total_number_logs_dict[key]['advertisement_data']) + 
                        '\n'
                    )
                i += 1
            f.close()
            last_total_number_dev_logs_change_timestamp = time.time()


def get_normalized_advertisement_data_str(advertisement_data_str):
    advertisement_data_str = advertisement_data_str.replace('AdvertisementData(', '')
    advertisement_data_str = advertisement_data_str[0:-1]
    advertisement_data_str = advertisement_data_str.replace("`", '')
    advertisement_data_str = advertisement_data_str.replace("'", '')
    advertisement_data_str = advertisement_data_str.replace("\"", '')
    advertisement_data_str = advertisement_data_str.replace("\\x", '_')
    advertisement_data_str = advertisement_data_str.replace(': b', ': ')
    return advertisement_data_str


def add_uuid_description_to_advertisement_data_str(advertisement_data_str): # service_data={00003802-0000-1000-8000-00805f9b34fb: _bc._f6_bc_c6_a3} service_uuids=[00001011-0000-1000-8000-00805f9b34fb, 00001012-0000-1000-8000-00805f9b34fb, 0000e011-0000-1000-8000-00805f9b34fb]
    if 'service_uuids=[' in advertisement_data_str:
        tmp_list = advertisement_data_str.split('service_uuids=[')
        tmp_data = tmp_list[1].split(']')[0]
        desc = ''
        for uuid in uuids_description_map_keys:
            if uuid in tmp_data:
                if len(desc) > 0:
                    desc += ', '
                desc += UUIDS_DESCRIPTION_MAP[uuid]
        if len(desc) > 0:
            advertisement_data_str = advertisement_data_str.replace('service_uuids=[' + tmp_data + ']', 'service_uuids=[' + tmp_data + ']=>[' + desc + ']')
    if 'service_data={' in advertisement_data_str:
        tmp_list = advertisement_data_str.split('service_data={')
        tmp_data = tmp_list[1].split('}')[0]
        desc = ''
        for uuid in uuids_description_map_keys:
            if uuid in tmp_data:
                if len(desc) > 0:
                    desc += ', '
                desc += UUIDS_DESCRIPTION_MAP[uuid]
        if len(desc) > 0:
            advertisement_data_str = advertisement_data_str.replace('service_data={' + tmp_data + '}', 'service_data={' + tmp_data + '}=>[' + desc + ']')
    return advertisement_data_str
        

def get_name_shortcut(name):
    res = ''
    name_list = name.split('_')
    for k in name_list:
        res += k[0]
    return res


def get_unique_key_idx_in_list(key, keys_list):
    if key not in keys_list:
        return 0
    i = 1
    while key + '_' + str(i) in keys_list:
        i += 1
    if i == MAX_UNIQUE_KEY_IDX and key + '_MAX_UNIQUE_KEY_IDX' in keys_list:
        return MAX_UNIQUE_KEY_IDX + 1
    return i


def get_advertisement_data_dict(advertisement_data_str):
    advertisement_data_dict = {}
    for advertisement_data_str_item in advertisement_data_str.split(', '):
        advertisement_data_str_item_list = advertisement_data_str_item.split('=')
        if len(advertisement_data_str_item_list) == 2:
            advertisement_data_dict[advertisement_data_str_item_list[0]] = advertisement_data_str_item_list[1]
    return advertisement_data_dict

            
def get_known_name_from_advertisement_data_match(advertisement_data_str):
    if len(dev_advertisement_data_map_keys) > 0:
        global match_ind_dict
        match_ind_dict = {}
        advertisement_data_dict = get_advertisement_data_dict(advertisement_data_str)
        advertisement_data_dict_keys = list(advertisement_data_dict.keys())
        for dev_advertisement_data_map_key in dev_advertisement_data_map_keys:
            dev_advertisement_data_map_key_dict = get_advertisement_data_dict(dev_advertisement_data_map_key)                
            dev_advertisement_data_map_key_dict_keys = list(dev_advertisement_data_map_key_dict.keys())
            match_ind = ''
            if len(dev_advertisement_data_map_key_dict_keys) > 0:
                for key in advertisement_data_dict_keys:
                    if is_key_prefix_in_keys_list(key, dev_advertisement_data_map_key_dict_keys):
                        if is_equality_in_key_and_key_prefix_dicts(key, advertisement_data_dict, dev_advertisement_data_map_key_dict):
                            if len(match_ind) > 0:
                                match_ind += ','
                            match_ind += get_name_shortcut(key)
                        else:
                            match_ind = ''
                            break
            match_ind_dict[dev_advertisement_data_map_key] = match_ind
        match_ind_dict_keys = list(match_ind_dict.keys())
        match_ind_dict_keys.sort(key=match_ind_dict_sort_by_list_len_func, reverse=True)
        if len(match_ind_dict[match_ind_dict_keys[0]]) > 0:
            return DEV_ADVERTISEMENT_DATA_MAP[match_ind_dict_keys[0]] + '(' + match_ind_dict[match_ind_dict_keys[0]] + ')'
    return '-'


def is_equality_in_key_and_key_prefix_dicts(key, key_dict, key_prefix_dict):
    key_prefix_dict_keys = list(key_prefix_dict.keys())
    for key_prefix_dict_key in key_prefix_dict_keys:
        if key_prefix_dict_key.startswith(key):
            if key_dict[key] == key_prefix_dict[key_prefix_dict_key]:
                return True
    return False


def is_key_prefix_in_keys_list(key_prefix, keys_list):
    for key in keys_list:
        if key.startswith(key_prefix):
            return True
    return False


def devices_dict_sort_by_RSSI_func(k):
    if devices_dict[k]['RSSI'] != 'N/S':
        return devices_dict[k]['RSSI']
    else:
        return -9999


def total_number_logs_dict_sort_by_log_count_func(k):
    return total_number_logs_dict[k]['log_count']


def match_ind_dict_sort_by_list_len_func(k):
    tmp = match_ind_dict[k].split(',')
    i = 0
    for el in tmp:
        if len(el) > 0:
            i += 1
    return i


def get_current_time_str():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')


def get_current_datetime_str():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%d.%m.%Y-%H:%M:%S')


def get_current_datetime_str_for_filename():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%d.%m.%Y-%H_%M_%S')


script_start_datetime_str = get_current_datetime_str()
current_datetime_str_for_filename = get_current_datetime_str_for_filename()
FIRST_DEV_LOG_TIME_FILE_PATH = './first_dev_log_time_' + current_datetime_str_for_filename + '.txt'
TOTAL_NUMBER_DEV_LOGS_FILE_PATH = './total_number_dev_logs_' + current_datetime_str_for_filename + '.txt'
f = open(FIRST_DEV_LOG_TIME_FILE_PATH, 'a')
f.write('\n\n\n=========================================================================\n')
f.write(get_current_datetime_str() + '\n\n')
f.close()
asyncio.run(main([]))
