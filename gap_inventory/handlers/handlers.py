__author__ = 'bakeneko'

import webapp2
import datetime
from gap_inventory import models
from google.appengine.ext.webapp import template
from google.appengine.api import users


class AddDeviceHandler(webapp2.RequestHandler):


    def get(self):
        self.render_add_device_page()


    def post(self):
        device = models.Device(**self.request.params)
        device.current_state = models.DeviceStates.CHECKED_IN
        device.put()
        self.render_add_device_page(True)


    def render_add_device_page(self, saved=False):
        params = {'non_home':True,
                  'add_device': True,
                  'saved': saved }
        add_general_info(params)
        return self.response.write(template.render("templates/add_device.html",params))



class CheckoutHandler(webapp2.RequestHandler):

    def post(self):
        device_id = self.request.get("device_id")


        if not device_id or not device_id.isdigit():
            self.response.set_status(400)
        else:
            device = models.Device.get_by_id([int(device_id)])[0]
            device.current_state = models.DeviceStates.CHECKED_OUT
            device.borrower = users.get_current_user().nickname()
            device.borrower_email = users.get_current_user().email()
            device.save()

            borrow = models.Check_Out(parent=device)
            borrow.check_out = datetime.datetime.now()
            borrow.put()

            self.response.set_status(202)


class CheckinHandler(webapp2.RequestHandler):
    """ A device is returned """
    def post(self):
        device_id = self.request.get("device_id")


        if not device_id or not device_id.isdigit():
            self.response.set_status(400)
        else:
            device = models.Device.get_by_id([int(device_id)])[0]
            device.current_state = models.DeviceStates.CHECKED_IN
            device.returned = datetime.datetime.now()
            device.save()

            #Let's register the Returned device
            checkout_query = models.Check_Out.all()
            checkout_query.ancestor(device)
            checkout_query.order("-check_out")
            for borrow in checkout_query.run(limit=1):
                borrow.check_in = datetime.datetime.now()
                borrow.save()

            self.response.set_status(202)


class DeviceInfoHandler(webapp2.RequestHandler):

    def get(self,device_id):

        if not device_id or not device_id.isdigit():
            self.response.set_status(400)
        else:
            device = models.Device.get_by_id([int(device_id)])[0]
            self.response.write(template.render("templates/includes/display_project_info.html",{'device': device}))


class CheckBorrowLength(webapp2.RequestHandler):

    def get(self):
        query = models.Device.gql("SELECT * FROM Check_Out where check_in = null")

        for borrow in query:
            pass


#
# Util functions
#

def add_general_info(params):
    params['is_admin'] = users.is_current_user_admin()
    params['user'] = users.get_current_user()
    params['logout_url'] = users.create_logout_url("http://www.growthaccelerationpartners.com/")