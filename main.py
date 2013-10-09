import webapp2
import sys
from gap_inventory import models
from google.appengine.ext.webapp import template
from google.appengine.api import users
from gap_inventory.handlers import handlers
from gap_inventory.handlers import notify_handler
from gap_inventory.utils import Constants

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if not user:
            self.redirect(users.create_login_url("/"))
        else:
            checked_in = models.Device.gql("WHERE current_state = :1 order by family", models.DeviceStates.CHECKED_IN).run()

            checked_out = models.Device.gql("WHERE current_state = :1 order by family", models.DeviceStates.CHECKED_OUT).run()
            params = {'checked_in': checked_in,
                      'checked_out': checked_out}

            handlers.add_general_info(params)

            return self.response.write(template.render("templates/dashboard.html",params))


app = webapp2.WSGIApplication([
                                (r'/', MainHandler),
                                (r'/adddevice', handlers.AddDeviceHandler),
                                (r'/checkout_device', handlers.CheckoutHandler),
                                (r'/checkin_device', handlers.CheckinHandler),
                                (r'/notify_device', notify_handler.NotifyHandler),
                                webapp2.Route(r'/device_details/<device_id:\d+>',handler=handlers.DeviceInfoHandler,name="device-details")],
                             debug=True)

