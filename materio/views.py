from methodism import METHODISM
from materio import methods


class Main(METHODISM):
    file = methods
    not_auth_methods = ['regis', 'login', 'StepOne', 'StepTwo']
