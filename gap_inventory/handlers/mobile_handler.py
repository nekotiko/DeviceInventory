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

class MobileHandler(webapp2.RequestHandler):

    def put(self):

        print "self.request.body: %s" % self.request.body

        result = ResponseCode.ERROR
        #try:
        token = json.loads(self.request.body)
        print "Token : %s" % token
        resultState = False
        if (token["checkState"]):
            print "True"
            result = check_out_device(self, token["email"], token["assetID"], token["tokenId"])
        else:
            print "False"
            result = check_in_device(self, token["email"], token["assetID"], token["tokenId"])
        #except:
        #    pass

        self.response.write(result)


def check_out_device(self, pNickname, pAssetId, pTokenId):
    device = get_device_by_asset_id(pAssetId)

    if not device:
        return ResponseCode.NO_DEVICE
    else:
        device.current_state = models.DeviceStates.CHECKED_OUT
        device.borrower = pNickname
        device.borrower_email = pNickname
        device.token_id = pTokenId
        device.save()

        borrow = models.Check_Out(parent=device)
        borrow.check_out = datetime.datetime.now()
        borrow.put()

        return ResponseCode.SUCCESS


def check_in_device(self, pNickname, pAssetId, pTokenId):
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