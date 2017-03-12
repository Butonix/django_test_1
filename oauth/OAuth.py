import requests


class OAuthVk:
    """Авторизация в ВК
    """

    _ACCESS_TOKEN_URL = 'https://oauth.vk.com/access_token'
    _AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
    _APP_ID_ = '5799473'   # id - приложения (в настройках vk)
    _REDIRECT_URL_ = 'http://localhost:8888/oauth'  # www.yousite.com/oauth
    _CLIENT_SECRET_ = 'ePxhl0tDNmV1t5EuveeJ'  # защищенный ключ приложения (в настройках vk)

    params = {'client_id': _APP_ID_,
              'redirect_uri': _REDIRECT_URL_,
              'scope': 'email',  # str(email)
              'response_type': 'code',
              }

    token_params = {'client_id': _APP_ID_,
                    'client_secret': _CLIENT_SECRET_,
                    'redirect_uri': _REDIRECT_URL_,
                    #'code': '{}',
                     }

    token_url = _ACCESS_TOKEN_URL + '?' + \
                '&'.join([k + '=' + v for k, v in token_params.items()]) + \
                '&code='

    code_url = _AUTHORIZE_URL + '?' + \
               '&'.join([k + '=' + v for k, v in params.items()])

    @classmethod
    def get_token(cls, code):

        result = {}
        try:
            u = cls.token_url+code
            r = requests.get(u)
            data = r.json()
            if 'error' in data:
                result['error'] = data['error']
                result['description'] = data['error_description']
                return result
            result['token'] = data['access_token']
            result['email'] = data['email']
            result['error'] = None

        except requests.RequestException as e:
            result['error'] = 'Не удалось соеденится с сервером VK '
            result['description'] = str(e)
        except KeyError as e:
            result['error'] = 'Не распознан ответ сервера'
            result['description'] = str(e)
        return result

    @classmethod
    def get_code_url(cls):
        return cls.code_url



