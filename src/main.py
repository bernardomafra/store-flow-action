import requests
from requests.structures import CaseInsensitiveDict
import login as LoginHelpers

session = requests.Session()

NIKE_HOME_PAGE = "https://www.nike.com.br"
SHOE_LINK = "https://www.nike.com.br/lebron-xviii-low-153-169-211-349959"


def get_product_code_by_url_and_size(product_url, size):
    url = "https://www.nike.com.br/Snkrs/PdpDependeCaptcha"

    headers = CaseInsensitiveDict()
    headers["referer"] = product_url

    resp = session.post(url, headers=headers)
    product_sizes = resp.text
    index_data_tamanho = product_sizes.find(f'data-tamanho="{size}"')
    index_product_code = index_data_tamanho + 17 + 21
    product_code = product_sizes[index_product_code : index_product_code + 12]
    return product_code


# Logs into Nike account, returns an access token
def login():
    headers = {
        "Content-Type": "application/json",
        "Cookie": "",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    }

    params = {
        "uxid": "com.nike.commerce.nikedotcom.web",
        "locale": "pt_BR",
        "backendEnvironment": "identity",
        "visit": "1",
        "visitor": LoginHelpers.generate_visitor_id(),
    }

    payload = {
        "username": "bernardomafra74@gmail.com",
        "password": "P4n1c0-p4n1c0",
        "ux_id": "com.nike.commerce.snkrs.web",
        "client_id": "HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH",
        "grant_type": "password",
    }

    endpoint = "https://unite.nike.com/login?"
    response = session.post(endpoint, json=payload, headers=headers, params=params)
    print(response)


def add_product_to_cart_by_url(url):
    headers = CaseInsensitiveDict()

    headers["accept"] = "application/json, text/javascript, */*; q=0.01"
    headers["accept-language"] = "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    headers[
        "sec-ch-ua"
    ] = '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"'
    headers["sec-ch-ua-mobile"] = "?0"
    headers["sec-ch-ua-platform"] = '"Linux"'
    headers["sec-fetch-dest"] = "empty"
    headers["sec-fetch-mode"] = "cors"
    headers["sec-fetch-site"] = "same-origin"
    headers["x-requested-with"] = "XMLHttpRequest"
    headers["referrer"] = url
    headers["referrerPolicy"] = "no-referrer-when-downgrade"
    headers[
        "body"
    ] = "EPrincipal=195238579432&EAcessorio%5B%5D=&ECompreJunto%5B%5D=&AdicaoProdutoId=&Origem=&SiteId=106&g-recaptcha-response="
    headers["method"] = "POST"
    headers["mode"] = "cors"
    headers["credentials"] = "include"

    print(headers)

    product_code = get_product_code_by_url_and_size(url, "41")
    data = f"EPrincipal={product_code}&EAcessorio%5B%5D=&ECompreJunto%5B%5D=&AdicaoProdutoId=&Origem=&SiteId=106&g-recaptcha-response="

    r = ""
    try:
        r = session.post(
            "https://www.nike.com.br/Carrinho/Adicionar",
            headers=headers,
            json=data,
            cookies=get_cookies(),
        )
        print(f"resposta: {r}")
    except session.exceptions.RequestException as e:
        print(f"error: {e}")
        return
    finally:
        print(f"resposta: {r}")
        return r


# resp = add_product_to_cart_by_url(
#     "https://www.nike.com.br/lebron-xviii-low-153-169-211-349959?gridPosition=K1"
# )
# print(resp)

login()
