from datetime import datetime
from uuid import UUID, uuid4

"""
В данном файле объявляются классы доменной области, соответствующие реальным объектам
"""

class Employee:

    def __init__(self,last_name:str,
                      first_name: str,
                      fired: bool = False,
                      fired_dt: datetime|None = None,
                      employee_id:UUID|None = None):
        if last_name is None or first_name is None:
            raise ValueError("Параметры last_name и first_name являются обязательными")

        self.employee_id=employee_id or uuid4()
        self.last_name=last_name
        self.first_name = first_name
        self.fired = fired
        self.fired_dt = fired_dt

    def fire(self, fired_dt: datetime | None = None) -> None:
        """
        Уволить сотрудника
        Если дата не указана, устанавливается текущая
        Если сотрудник уже уволен, ничего не меняется (или можно бросить исключение)
        """
        self.fired = True
        self.fired_dt = fired_dt or datetime.now()