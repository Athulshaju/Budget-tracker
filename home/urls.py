from django.urls import path,include
from rest_framework.routers import DefaultRouter

from home import views
from .views import IncomeView,ExpenseView,CategoryView,BudgetView,EMIView,ReportView

router=DefaultRouter()
router.register(r"income",IncomeView,basename="income")
router.register(r"expense",ExpenseView,basename="expense")
router.register(r"category",CategoryView,basename="category")
router.register(r"budget",BudgetView,basename="budget")
router.register(r"emi",EMIView,basename="emi")
router.register(r'report', ReportView, basename='report')

urlpatterns= [path('',views.index, name="index"),
              path('',include(router.urls)),
              
              #dashboard
              path('dashboard',views.dashboard_view, name="dashboard_view"),
              
              #accounts
              path('register',views.register, name="register"),
              path('login',views.login, name="login"),
              path('profile',views.profile_view, name="profile_view"),
              path('logout',views.logout, name="logout"),
              
              #inputing data
              path('add_budget',views.add_budget, name="add_budget"),
              path('add_income',views.add_income, name="add_income"),
              path('add_expense',views.add_expense, name="add_expense"),
              path('add_emi',views.add_emi, name="add_emi"),
              
              #edit
              path('edit-emi/<int:emi_id>/', views.edit_emi, name='edit_emi'),
              path('chart-data', views.ChartDataView.as_view(), name='chart_data'),
              path('charts',views.charts_view, name="charts_view"),
              path('generate_pdf', views.generate_pdf, name='generate_pdf'),
              ]