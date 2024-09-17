from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import create_visa, edit_visa
from .visa import(
     add_visa, edit_visa, visa_table
)
from .wallet import(
     add_wallet, edit_wallet, wallet_table
)
from .wallet_name import( 
     add_wallet_name,edit_wallet_name,wallet_name_table
     ) 
#add_create_object, edit_create_object


app_name = "management"


urlpatterns = [
    path("create/new/visa/", login_required(create_visa), name="create_visa"),
    path("edit/visa/id/<int:id>", login_required(edit_visa), name="edit_visa"),
    
    
    # ------- Create Visa Urls -------
     path("table/of/all/visa/",
          login_required(visa_table),
          name="visa_table"
          ),
     path("add/visa/",
          login_required(add_visa),
          name="add_visa"
          ),
     path("edit/visa/<int:id>/",
          login_required(edit_visa),
          name="edit_visa"
          ),
     
     
     # ------- Create Wallet Urls -------
     path("table/of/all/wallet/",
          login_required(wallet_table),
          name="wallet_table"
          ),
     path("add/wallet/",
          login_required(add_wallet),
          name="add_wallet"
          ),
     path("edit/wallet/<int:id>/",
          login_required(edit_wallet),
          name="edit_wallet"
          ),
     
     #? ------- Create Wallet Name Urls -------
     path("table/of/all/wallet/name/",
          login_required(wallet_name_table),
          name="wallet_name_table"
          ),
     path("add/wallet/name/",
          login_required(add_wallet_name),
          name="add_wallet_name"
          ),
     path("edit/wallet/name/<int:id>/",
          login_required(edit_wallet_name),
          name="edit_wallet_name"
          ),
]
