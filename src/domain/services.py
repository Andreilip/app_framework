"""
В данном файле объявляются функции работы над объектами доменной области

"""
from src.domain.models import Employee

def create_new_employee (last_name:str, first_name: str,)->Employee: 
    new_employee = Employee(
        last_name=last_name,
        first_name=first_name,
    )
    return new_employee