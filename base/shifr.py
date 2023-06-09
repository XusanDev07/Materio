import base64


def code_decoder(code, decode=False, l=1):
    if decode:
        for i in range(l):
            code = base64.b64decode(code).decode()
        return code
    else:
        for i in range(l):
            code = base64.b64encode(str(code).encode()).decode()
        return code



token = 'VmtaV1UxUXlSa2RqUlZaV1ZrVmFZVlJYZUZkTlJtUnlWV3RLVG1GNlZsVlVWVkpEVkRBeGMyRjZRbFZTYkVwMldWZHplRTVzUmxsVmF6bFRVbFp3ZGxZeFpIZFZNa3BYWWtSYVUxWkdXbWhWYTFwM1l6Rk9jbFZ1U2s1U1ZFWjRWV3hvYjFReVJsZFNhazVZVm14S1ZGbFZXbk5XVmtwVlZXczFhR0pWTVRWV1J6RjNVVzFXVms1WVVsUmlWM2hQVld0YWMwNVdaSE5WYlhSb1VtMTRWbFpITVhOVWJVcFdZMGhPVlZaRmNFZFVWRUUxVWxaV1ZWUnJPV3hoTUZZelZrWmFVMUl5UmtKUVZEQTk='

print(code_decoder(token, decode=True, l=5))