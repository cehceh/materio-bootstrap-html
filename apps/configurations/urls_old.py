from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
     add_unit_names, edit_unit_names, unit_names_table,
)
# from .departments_origin import(
#      add_departments, edit_departments, departments_table
# )
from .departments import(
     add_departments, edit_departments, departments_table
)
from .branches_new import (
     add_branches, edit_branches, branches_table
)
from .bank import (
     add_bank, edit_bank, bank_table, 
     # restore_bank
)
from .bank_account import (
     add_bank_account, edit_bank_account, bank_account_table
)
from .pos_station import (
     add_pos_station, edit_pos_station, pos_stations_table
)



app_name = "configurations"


urlpatterns = [
     #? ------- Unit Names Urls -------
     path("table/of/all/unit-names/",
          login_required(unit_names_table),
          name="unit_names_table"
          ),
     path("add/unit-names/",
          login_required(add_unit_names),
          name="add_unit_names"
          ),
     path("edit/unit-names/<int:id>/",
          login_required(edit_unit_names),
          name="edit_unit_names"
          ),
     

     #? ------- Branches Urls -------
     path("table/of/all/branches/",
          login_required(branches_table),
          name="branches_table"
          ),
     path("add/branch/",
          login_required(add_branches),
          name="add_branches"
          ),
     path("edit/branch/id/<int:id>/",
          login_required(edit_branches),
          name="edit_branches"
          ),

     #? ------- PosStation Urls -------
     path("table/of/all/pos-stations/",
          login_required(pos_stations_table),
          name="pos_stations_table"
          ),
     path("add/pos-station/",
          login_required(add_pos_station),
          name="add_pos_station"
          ),
     path("edit/pos-station/id/<int:id>/",
          login_required(edit_pos_station),
          name="edit_pos_station"
          ),

     #? ------- Departments Urls -------
     path("table/of/all/departments/",
          login_required(departments_table),
          name="departments_table"
          ),
     path("add/new/department/",
          login_required(add_departments),
          name="add_departments"
          ),
     path("edit/departments/<int:id>/",
          login_required(edit_departments),
          name="edit_departments"
     ),
     
     
     # ------- Expenses Urls -------
     # path("table/of/all/expenses/",
     #      login_required(table_expenses),
     #      name="expenses_table"
     #      ),
     # path("add/new/department/",
     #      login_required(add_expenses),
     #      name="add_expenses"
     #      ),
     # path("edit/departments/<int:id>/",
     #     login_required(edit_expenses),
     #     name="edit_expenses"
     #     ),
     
     #? ------- Banks Urls -------
     path("table/of/all/bank/",
          login_required(bank_table),
          name="bank_table"
          ),
     path("add/bank/",
          login_required(add_bank),
          name="add_bank"
          ),
     path("edit/bank/id/<int:id>/",
          login_required(edit_bank),
          name="edit_bank"
          ),
     #!!!trail for trying to restore deleted data
     # path("restore/bank/id/<int:id>/", 
     #      login_required(restore_bank), 
     #      name="restore_bank"
     #      ),
     
     #? ------- Bank Account Urls -------
     path("table/of/all/bank-account/",
          login_required(bank_account_table),
          name="bank_account_table"
          ),
     path("add/bank-account/",
          login_required(add_bank_account),
          name="add_bank_account"
          ),
     path("edit/bank-account/id/<int:id>/",
          login_required(edit_bank_account),
          name="edit_bank_account"
          ),
]


