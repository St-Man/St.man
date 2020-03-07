import tornado.web
import tornado.ioloop
import os
import pickle
from datetime import datetime
from mac_vendor_lookup import MacLookup


opentime = datetime.now()

# Opening the pickle file containing all the victims.
with open('pickle_data.pkl', 'rb') as pickle_in:
    victims = pickle.load(pickle_in)


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
        response = {'number of connected victims': len(victims.keys())}
        self.write(response)
        response.clear()


class ConnectedVictimsHandler(tornado.web.RequestHandler):
    """Handler of the connectedvictims request."""
    def get(self):
        # First we initialize the JSON format of the response.
        response = {'victims': []}
        for key in victims:
            # Then for every value in the victims dict, we add a victim
            # to the JSON response with the appropriate format.
            response['victims'].append({'IP': victims[key]['Victims IP'],
                                        'MAC': victims[key]['Victims MAC'],
                                        'Manufacturer': MacLookup().lookup(
                                        victims[key]['Victims MAC'])})
        self.write(response)
        response.clear()


class VictimInfoHandler(tornado.web.RequestHandler):
    """Handler of the victiminfo request."""
    def get(self):
        MAC = self.get_argument('macaddress')
        response = {}

        for key in victims:
            # We simply search the dict to find the specific MAC address.
            # Then we print the info of the specific victim.
            if victims[key]['Victims MAC'] == MAC:
                response.update({'IP': victims[key]['Victims IP'], 'MAC':
                            victims[key]['Victims MAC'], 'Manufacturer':
                            MacLookup().lookup(victims[key]['Victims MAC'])})
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
