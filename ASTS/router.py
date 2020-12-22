from employee.viewsets import EmployeeViewset,DepartmentViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('employee',EmployeeViewset)
router.register('department',DepartmentViewset)

