from django.contrib import admin
from django.urls import path, include
from .views import views


app_name = 'banks'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('add/', views.AddBankView.as_view(), name="add_bank"), # works
    path('<int:bank_id>/details/', views.ShowDetailView.as_view(), name="bank_details"), # works
    path('all/', views.ListAllBanksView.as_view(), name="allbanks"), # works 
    path('<int:bank_id>/branches/add/', views.AddBranchView.as_view(), name="add_branch"), # works 
    path('branch/<int:branch_id>/details/', views.branchdetails, name="branch_details"), # works
    path('<int:bank_id>/branches/all/', views.ListAllBranchesView.as_view(), name="allbranches"), # no
    path('branch/<int:branch_id>/edit/', views.BranchEditView.as_view(), name="branch_edit"),
    

    

    
    
]