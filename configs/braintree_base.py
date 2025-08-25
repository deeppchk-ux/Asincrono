import json
import requests
from configs.configsbraintres import BehaviorsBraintree

class BraintreeAuthWoo:
    def main(self, cards):
        try:
            self.session = requests.Session()
            





            
            self.session.close()

            # error = BehaviorsBraintree().QueryText(response.text, 'class="woocommerce-error" role="alert">', '</li>').split('<li>')
            # if error[1] == '\n\t\t\t\t\t': return 'Approved! ✅', '1000: Approved'
            # else: return BehaviorsBraintree().Response(error[1].split('t method. Reason: ')[1].strip())

        except: return 'Declined! ❌', 'Risk_threshold'