import tornado.web
import tornado.ioloop
import os
import pickle
from datetime import datetime
import constants as constants
import macmatcher as macmatcher
import victim as vctm


opentime = datetime.now()

# Initializing the instances of the victims, as well as the victims dic.
victims_instance = vctm.Victims.get_instance()
victim_1 = vctm.Victim('78:44:76:bf:8d:6f', '192.168.1.1')
victim_2 = vctm.Victim('94:0e:6b:3f:5a:6d', '192.168.1.2')

# Adding the victims to the victims_dic.
victims_instance.add_to_victim_dic(victim_1)
victims_instance.add_to_victim_dic(victim_2)

# Associating each victims mac address with a mac vendor.
victim_1.associate_victim_mac_to_vendor(victim_1.vmac_address)
victim_2.associate_victim_mac_to_vendor(victim_2.vmac_address)


class ConnectionTimeHandler(tornado.web.RequestHandler):
    """Handler of the connectiontime request."""
    def get(self):
        # For now, this function calculates the uptime of the server.
        presentime = datetime.now()
        connectiontime = ((presentime-opentime).total_seconds())/60
        response = {'Time the victim has spent to the web page: ':
                    connectiontime}
        self.write(response)


class NumberOfVictimsHandler(tornado.web.RequestHandler):
    """Handler of the numberofvictims request."""
    def get(self):
        # We simply count the number of keys in the victims dictionary.
        response = {'number of connected victims': len(victims_instance.
                    victims_dic.keys())}
        self.write(response)
        response.clear()


class ConnectedVictimsHandler(tornado.web.RequestHandler):
    """Handler of the connectedvictims request."""
    def get(self):
        # First we initialize the JSON format of the response.
        response = {'victims': []}

        for key in victims_instance.victims_dic:
            # Then for every value in the victims dict, we add a victim
            # to the JSON response with the appropriate format.
            response['victims'].append({'IP': victims_instance.
                                        victims_dic[key].ip_address,
                                        'MAC': victims_instance.
                                        victims_dic[key].vmac_address,
                                        'Manufacturer': victims_instance.
                                        victims_dic[key].vendor})
        self.write(response)
        response.clear()


class VictimInfoHandler(tornado.web.RequestHandler):
    """Handler of the victiminfo request."""
    def get(self):
        MAC = self.get_argument('macaddress')
        response = {}
        #macmatcher_object = macmatcher.MACMatcher(constants.MAC_PREFIX_FILE)

        for key in victims_instance.victims_dic:
            # We simply search the dict to find the specific MAC address.
            # Then we print the info of the specific victim.
            if victims_instance.victims_dic[key].vmac_address == MAC:
                response.update({'IP': victims_instance.victims_dic[key].
                                 ip_address, 'MAC': victims_instance.
                                 victims_dic[key].vmac_address,
                                 'Manufacturer': victims_instance.
                                 victims_dic[key].vendor})
                break
        # Check if the MAC existed in the victims list.
        if len(response) == 0:
            self.set_status(404)
            self.write('404: Not found.')
        else:
            self.write(response)


class HomeHandler(tornado.web.RequestHandler):
    """The handler of the home page."""
    def get(self):
        self.write('RestAPI Home')


# Here we create our app. We assign the corresponding handlers to the links.
app = tornado.web.Application([('/', HomeHandler), (r'/connectedvictims',
                               ConnectedVictimsHandler), (r'/numberofvictims',
                               NumberOfVictimsHandler), (r'/connectiontime',
                               ConnectionTimeHandler), (r'/victiminfo',
                               VictimInfoHandler)])

# Initializing the server.
if __name__ == '__main__':
    # The port of our server.
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
