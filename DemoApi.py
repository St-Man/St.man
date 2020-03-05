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


# The handler of of the connectiontime request.
class ConnectionTimeHandler(tornado.web.RequestHandler):
    def get(self):
        # For now, this function calculates the uptime of the server.
        presentime = datetime.now()
        connectiontime = ((presentime-opentime).total_seconds())/60
        response = {'Time the victim has spent to the web page: ':
                    connectiontime}
        self.write(response)


# The handler of the numberofvictims request.
class NumberOfVictimsHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'number of connected victims': len(victims)}
        self.write(response)
        response.clear()


# The handler of the connectedvictims request
class ConnectedVictimsHandler(tornado.web.RequestHandler):
    def get(self):
        # We read the file and add the dictionary values to the empty response
        # dictionary.Then we return the response dictionary.
        response = {'victims': []}
        for key in victims:
            response['victims'].append({'IP': victims[key]['Victims IP'],
                                        'MAC': victims[key]['Victims MAC'],
                                        'Manufacturer': MacLookup().lookup(
                                        victims[key]['Victims MAC'])})
        self.write(response)
        response.clear()


# The handler of Home
class HomeHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('RestAPI Home')


# Here we create our app.
app = tornado.web.Application([('/', HomeHandler), (r'/connectedvictims',
                               ConnectedVictimsHandler), (r'/numberofvictims',
                               NumberOfVictimsHandler), (r'/connectiontime',
                               ConnectionTimeHandler)])

if __name__ == '__main__':
    # The port of our server.
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
