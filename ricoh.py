import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

#GET request, needs 1 param via string.format() function


ID_URL = "https://columbiauniversity.ikontrac.com/external/kiosks/mail/pickup/getEmployeeId.cfm?loginType=custom09&id={}"

#POST with studentid={uni} as param
UNI_URL = "https://columbiauniversity.ikontrac.com/external/kiosks/mail/pickup/index.cfm?"




class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize, 
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def package_info(uni):
    uni_data = {"studentid":uni}
    
    s = requests.Session()
    s.mount('https://', MyAdapter())




    response = s.post(UNI_URL,data=uni_data, verify=False)

    index = response.text.find('displayMessage("')
   
    if index == -1: #card not found
        return None 

    if response.text.find('have not received') !=-1:
        return False

    if response.text.find('have received') != -1:
        return True    

    return None


def uni_from_id(id_num):
    
    s = requests.Session()
    s.mount('https://', MyAdapter())

    formatted_url = ID_URL.format(id_num)
    response = s.get(formatted_url)
    return response.text.strip() 

