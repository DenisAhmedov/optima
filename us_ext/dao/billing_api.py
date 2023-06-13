import urllib.parse
import json

from config.settings import BILLING_ADDRESS


class BillingApiMixin(object):
    def __init__(self, srv_address=BILLING_ADDRESS):
        self.srv_address = srv_address

    def call_api(self, model, params):
        encoded_params = urllib.parse.urlencode(params)
        encoded_params = encoded_params.encode('utf-8')
        api_url = "{0}/rest_api/v2/{1}/".format(self.srv_address, model)
        req = urllib.request.Request(url=api_url, data=encoded_params)
        response = urllib.request.urlopen(req)
        result = response.read()
        result = result.decode('utf-8')
        obj = json.loads(result)
        if obj.get('error'):
            # print(u'Произошла ошибка на стороне биллинга:{0}'.format(obj['error']))
            if isinstance(obj['error'], list):
                obj = {'error': obj['error'][-1].strip()}
            elif isinstance(obj['error'], str):
                obj = {'error': obj['error']}
        return obj
