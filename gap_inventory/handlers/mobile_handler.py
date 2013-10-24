__author__ = 'rmadrigal'

import webapp2
from gap_inventory import models
from gap_inventory.libraries import ResponseCode
from google.appengine.ext.webapp import template
from google.appengine.api import users
from external.appengine_push_service import push
from gap_inventory.libraries import const
import json
import datetime
import logging

class MobileHandler(webapp2.RequestHandler):

    def put(self):
        result = ResponseCode.ERROR
        try:
            token = json.loads(self.request.body)

            if (token[const.KEY_CHECK_STATE]):
                result = check_out_device(self, token[const.KEY_EMAIL], token[const.KEY_ASSET_ID], token[const.KEY_TOKEN_ID])
            else:
                result = check_in_device(self, token[const.KEY_ASSET_ID], token[const.KEY_TOKEN_ID])
        except:
            if(token and token[const.KEY_ASSET_ID]):
                logging.error(const.MESSAGE_ERROR_UPDATE_DEVICE % token[const.KEY_ASSET_ID])
            else:
                logging.error(const.MESSAGE_ERROR_UPDATE_DEVICE_NO_ASSET)
            pass

        self.response.write(result)


def check_out_device(self, pEmail, pAssetId, pTokenId):
    device = get_device_by_asset_id(pAssetId)

    if not device:
        return ResponseCode.NO_DEVICE
    else:
        device.current_state = models.DeviceStates.CHECKED_OUT
        if pEmail.find("@") == -1 :
            device.borrower = pEmail
            device.borrower_email = pEmail + const.EMAIL_DOMAIN
        else:
            device.borrower = pEmail[0:pEmail.find("@")]
            device.borrower_email = pEmail

        if pTokenId:
            device.token_id = pTokenId
        device.save()

        borrow = models.Check_Out(parent=device)
        borrow.check_out = datetime.datetime.now()
        borrow.put()

        return ResponseCode.SUCCESS


def check_in_device(self, pAssetId, pTokenId):
    device = get_device_by_asset_id(pAssetId)

    if not device:
        return ResponseCode.NO_DEVICE
    else:
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

        return ResponseCode.SUCCESS

def get_device_by_asset_id(pAssetId):
    device_query = models.Device.all()
    device_query.filter('gap_asset_id =', pAssetId)
    device = device_query.get()
    return device

class MobileStatusHandler(webapp2.RequestHandler):

    def put(self):
        result = ResponseCode.ERROR
        try:
            token = json.loads(self.request.body)

            if token and token[const.KEY_ASSET_ID]:
                device = get_device_by_asset_id(token[const.KEY_ASSET_ID])

                if device:
                    if token[const.KEY_OS_VERSION]:
                        device.os_version = token[const.KEY_OS_VERSION]

                    if token[const.KEY_OS_NAME]:
                        device.os = token[const.KEY_OS_NAME]

                    #Changes are saved
                    device.save()

                    if device.current_state == models.DeviceStates.CHECKED_OUT:
                        if device.borrower.find("@") == -1:
                            result = const.RESPONSE_FORMAT_CHECK_STATUS % (const.KEY_LOGGED_USER, device.borrower)
                        else:
                            result = const.RESPONSE_FORMAT_CHECK_STATUS % \
                                     (const.KEY_LOGGED_USER, device.borrower[0:device.borrower.find("@")])
                    else:
                        result = const.RESPONSE_FORMAT_CHECK_STATUS % (const.KEY_LOGGED_USER, const.VALUE_NO_USER)
        except:
            if(token and token[const.KEY_ASSET_ID]):
                logging.error(const.MESSAGE_ERROR_CHECK_DEVICE % token[const.KEY_ASSET_ID])
            else:
                logging.error(const.MESSAGE_ERROR_CHECK_NO_ASSET_ID)
            pass

        self.response.write(result)