__author__ = 'rmadrigal'

import webapp2
from gap_inventory import models
from google.appengine.ext.webapp import template
from google.appengine.api import users
from external.appengine_push_service import push
from gap_inventory.libraries import const
from google.appengine.api import mail

class PushNotificationHandler(webapp2.RequestHandler):

    def post(self):
        device_id = self.request.get("device_id")

        if not device_id or not device_id.isdigit():
            self.response.set_status(400)
        else:
            device = models.Device.get_by_id([int(device_id)])[0]

            response = notify_to_error(device)
            message = const.MESSAGE_EMERGENCY_RETURN % users.get_current_user().nickname()
            if (const.ANDROID_OS_NAME == device.os):
                response = notify_to_device(device, const.ANDROID_OS_NAME, message)
            elif (const.IOS_OS_NAME == device.os):
                response = notify_to_device(device, const.IOS_OS_NAME, message)

            notify_by_email(device, users.get_current_user().email(), device.borrower, device.borrower_email)

            self.response.out.write(response)


            self.response.set_status(202)

class CheckInGlobalNotifierHandler(webapp2.RequestHandler):

    def get(self):

        print "Cron task: Notifying to checked in devices: \n"
        for device in models.Device.gql("WHERE current_state = :1 order by family", models.DeviceStates.CHECKED_OUT).run():
            print device.get_os_details()
            try:
                if (const.ANDROID_OS_NAME == device.os):
                    print notify_to_device(device, const.ANDROID_OS_NAME, const.MESSAGE_REMINDER_CHECK_IN)
                elif (const.IOS_OS_NAME == device.os):
                    print notify_to_device(device, const.IOS_OS_NAME, const.MESSAGE_REMINDER_CHECK_IN)
            except:
                pass

class CheckOutGlobalNotifierHandler(webapp2.RequestHandler):

    def get(self):

        print "Cron task: Notifying to checked out devices: \n"
        for device in models.Device.gql("WHERE current_state = :1 order by family", models.DeviceStates.CHECKED_IN).run():
            try:
                if (const.ANDROID_OS_NAME == device.os):
                    print notify_to_device(device, const.ANDROID_OS_NAME, const.MESSAGE_REMINDER_CHECK_OUT)
                elif (const.IOS_OS_NAME == device.os):
                    print notify_to_device(device, const.IOS_OS_NAME, const.MESSAGE_REMINDER_CHECK_OUT)
            except:
                pass


def notify_to_device(pDevice, pOS, pMessage):

    request = {}
    request[const.KEY_PLATFORM] = pOS
    request[const.KEY_MESSAGE] = pMessage
    request[const.KEY_TOKEN] = pDevice.token_id
    request[const.KEY_BADGE] = "1"

    push.send_message(request)

    return const.MESSAGE_NOTIFYING % pDevice.get_os_details()

def notify_to_error(device):
    return const.MESSAGE_ERROR_NOTIFICATION_SERVICE % device.get_os_details()

def notify_by_email(device, pFromUser, pToUserNickName ,pToUserEmail):
    message = mail.EmailMessage(sender=const.EMAIL_SENDER, subject=const.EMAIL_SUBJECT)
    message.to = "%s <%s>" % (pToUserNickName, pToUserEmail)
    message.body = """
    Dear %s:

    The following device that you are using is required by %s:

    Gap Asset ID: %s %s %s

    Please do check-out this device as soon as possible, or contact the requester.

    --MobileGap Team
    """ % (pToUserNickName.capitalize(), pFromUser, device.gap_asset_id, device.get_device_name(), device.get_os_details())

    message.send()