from xml.etree import ElementTree as etree

from _data_process import ave_filter

class sensor_session:
    '''Reading the xml session file and get access of session data.'''

    def __init__(self, file_name):
        '''Reading the xml file specified by file_name.

        sesor_dict is a dict of which the key is the sensor physical id and value
        is the sensor data list
        '''
        self.sensor_dict = dict()
        tree = etree.parse(file_name)
        root = tree.getroot()

        # get all the sensor node
        nodes = root[0].getchildren()

        for node in nodes:
            self.sensor_dict[node.get('phyId')] = node.getchildren()

    def get_ids(self):
        return self.sensor_dict.keys()

    def get_datas(self):
        return self.sensor_dict.values()

    def get_data_of_id(self, sensor_id):
        return self.sensor_dict.get(sensor_id)

    def get_specific_data_of_id(self, sensor_id, data_info):
        datas = self.get_data_of_id(sensor_id)

        if data_info is "Ax":
            return [value.get("Ax") for value in datas]
        if data_info is "Ay":
            return [value.get("Ay") for value in datas]
        if data_info is "Az":
            return [value.get("Az") for value in datas]

        if data_info is "Mx":
            return [value.get("Mx") for value in datas]
        if data_info is "My":
            return [value.get("My") for value in datas]
        if data_info is "Mz":
            return [value.get("Mz") for value in datas]

        if data_info is "Gx":
            return [value.get("Gx") for value in datas]
        if data_info is "Gy":
            return [value.get("Gy") for value in datas]
        if data_info is "Gz":
            return [value.get("Gz") for value in datas]

        if data_info is "Rw":
            return [value.get("Rw") for value in datas]
        if data_info is "Rx":
            return [value.get("Rx") for value in datas]
        if data_info is "Ry":
            return [value.get("Ry") for value in datas]
        if data_info is "Rz":
            return [value.get("Rz") for value in datas]

        return []
