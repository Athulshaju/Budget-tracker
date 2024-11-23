from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from .models import Income,Expense,Category,Budget,EMI,Userprofile
from .serializers import IncomeSerializer,ExpenseSerializer,CategorySerializer,BudgetSerializer,EMISerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets,permissions,status,filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm,ExpenseForm,CategoryForm,BudgetForm,EMIForm
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from . filters import TransactionFilter
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .utils import send_alert
from reportlab.lib.pagesizes import letter
from rest_framework.views import APIView
from decimal import Decimal
from io import BytesIO
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def index(request):
    return render(request,"index.html")

@login_required
def dashboard_view(request):
    
    # Aggregate total income and expense amounts
    total_income = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_balance = total_income - total_expense

    # Get and filter transactions using Django Filter
    income_filter = TransactionFilter(request.GET, queryset=Income.objects.filter(user=request.user))
    expense_filter = TransactionFilter(request.GET, queryset=Expense.objects.filter(user=request.user))
    filtered_income = income_filter.qs
    filtered_expense = expense_filter.qs

    # Combine filtered incomes and expenses, add type, and sort by date
    recent_transactions = (
        [{'amount': inc.amount, 'category': inc.category.name, 'date': inc.date, 'type': 'Income'}
         for inc in filtered_income]
        + [{'amount': exp.amount, 'category': exp.category.name, 'date': exp.date, 'type': 'Expense'}
           for exp in filtered_expense]
    )
    recent_transactions = sorted(recent_transactions, key=lambda x: x['date'], reverse=True)[:5]

    # Fetch upcoming EMIs (example: next 3 EMIs)
    emi_reminders = EMI.objects.filter(user=request.user).order_by('due_date')[:3]
    
    

    # Pass data to template
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'remaining_balance': remaining_balance,
        'recent_transactions': recent_transactions,
        'emi_reminders': emi_reminders,
        'income_filter': income_filter,
        'expense_filter': expense_filter,
    }
    return render(request, 'dashboard.html', context)


#register new user
def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password']
        password2=request.POST['password2']
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists')
                return render(request,'register.html')
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request,'User already registered')
                    return render(request,'register.html')
                else:
                    user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password1)
                    user.save()
                    # Create Userprofile instance and save it
                    user_profile = Userprofile(user=user)
                    user_profile.save()
                    return render(request,'login.html')
        else:
            messages.info(request,'Password not matching')
            return render(request,'register.html')
        
    else:
            
        return render(request,'register.html')


#Login page
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home:dashboard_view')
        else:
            messages.info(request,'Invalid credentials')
            return render(request,'login.html')
    else:
        return render(request,'login.html')
    
#logout
def logout(request):
    auth.logout(request)
    return render(request,'index.html')


#Category API
class CategoryView(viewsets.ModelViewSet):
    serializer_class=CategorySerializer
    queryset=Category.objects.all()
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        
        
#Income API        
class IncomeView(viewsets.ModelViewSet):
    serializer_class=IncomeSerializer
    queryset=Income.objects.all()    
    permission_classes=[IsAuthenticated]
    filter_backends=(DjangoFilterBackend,filters.OrderingFilter)
    filterset_fields=['date','category',]
    ordering_fields=['date','amount',]
    ordering=['date']
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        
#Expense API
class ExpenseView(viewsets.ModelViewSet):
    serializer_class=ExpenseSerializer
    queryset=Expense.objects.all()    
    permission_classes=[IsAuthenticated]
    filter_backends=(DjangoFilterBackend,filters.OrderingFilter)
    filterset_fields=['date','category',]
    ordering_fields=['date','amount',]
    ordering=['date']
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        BudgetView.check_budget_alert(self.request.user)
        

#Budget API
class BudgetView(viewsets.ModelViewSet):
    serializer_class=BudgetSerializer
    queryset=Budget.objects.all()
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        
    def perform_update(self,serializer):
        serializer.save(user=self.request.user)
    
    def perform_delete(self,instance):
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def check_budget_alerts(self, request):
        alerts = []
        budgets = Budget.objects.filter(user=request.user)
        expenses = Expense.objects.filter(user=request.user).values('category').annotate(total=Sum('amount'))


        for budget in budgets:
            for expense in expenses:
                if expense['category'] == budget.category.id and expense['total'] > budget.limit:
                    alerts.append(f"Alert: You have exceeded your budget for {budget.category.name}.")
                    print(f"Sending exceeded alert to {request.user.email}")
                    send_alert(request.user, budget.category, exceeded=True)  # Sending alert if exceeded
                elif expense['category'] == budget.category.id and expense['total'] >= budget.limit * Decimal("0.9"):
                    alerts.append(f"Warning: You are nearing your budget for {budget.category.name}.")
                    print(f"Sending exceeded alert to {request.user.email}")
                    send_alert(request.user, budget.category, exceeded=False)  # Sending alert if nearing


        return Response({"alerts": alerts})

    

#EMI API
class EMIView(viewsets.ModelViewSet):
    serializer_class=EMISerializer  
    queryset=EMI.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        
        
        
@login_required
def add_budget(request):
    if request.method=='POST':
        form=BudgetForm(request.POST)
        if form.is_valid():
            budget=form.save(commit=False)
            budget.user=request.user
            budget.save()
            return redirect('home:dashboard_view')
    else:
        form=BudgetForm()
    return render(request,'add_budget.html',{'form':form})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense_form = form.save(commit=False)
            expense_form.user = request.user
            alerts = []
            budgets = Budget.objects.filter(user=request.user)

            # Get existing total expense for the category
            existing_total_expense = Expense.objects.filter(
                user=request.user,
                category=expense_form.category
            ).aggregate(Sum('amount'))['amount__sum'] or 0

            # Calculate total expense after adding the new expense
            total_expense = existing_total_expense + expense_form.amount

            # Check against category budget
            for budget in budgets:
                if budget.category == expense_form.category:
                    if total_expense > budget.limit:
                        alerts.append(f"Alert: You have exceeded your budget for {budget.category.name}.")
                        messages.info(request, f"You have exceeded your {budget.category.name} budget.")
                        print(f"Sending exceeded alert to {request.user.email}")
                        send_alert(request.user, budget.category, exceeded=True, total=False)  # Sending alert if exceeded
                        return render(request, 'add_expense.html', {'form': form})
                    elif total_expense >= budget.limit * Decimal("0.9"):
                        alerts.append(f"Warning: You are nearing your budget for {budget.category.name}.")
                        messages.info(request, f"You are nearing your {budget.category.name} budget.")
                        print(f"Sending nearing alert to {request.user.email}")
                        send_alert(request.user, budget.category, exceeded=False, total=False)  # Sending alert if nearing
                        return render(request, 'add_expense.html', {'form': form})

            # Check against total budget (irrespective of category)
            total_budget_used = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
            total_budget_used += expense_form.amount
            for budget in budgets:
                if total_budget_used > budget.total_budget:
                    alerts.append(f"Alert: You have exceeded your total budget.")
                    messages.info(request, 'You have exceeded your total budget.')
                    print(f"Sending exceeded alert to {request.user.email}")
                    send_alert(request.user, budget.category, exceeded=True, total=True)
                    return render(request, 'add_expense.html', {'form': form})
                elif total_budget_used >= budget.total_budget * Decimal("0.9"):
                    alerts.append(f"Warning: You are nearing your total budget.")
                    messages.info(request, 'You are nearing your total budget.')
                    print(f"Sending nearing alert to {request.user.email}")
                    send_alert(request.user, budget.category, exceeded=False, total=True)
                    return render(request, 'add_expense.html', {'form': form})

            # Save the expense
            expense_form.save()
            return redirect('home:dashboard_view')
    else:
        form = ExpenseForm()
    return render(request,'add_expense.html',{'form':form})



@login_required
def add_income(request):
    if request.method=='POST':
        form=IncomeForm(request.POST)
        if form.is_valid():
            income=form.save(commit=False)
            income.user=request.user
            income.save()
            return redirect('home:dashboard_view')
    
    else:
        form=IncomeForm()
    return render(request,'add_income.html',{'form':form})
    
        
@login_required
def add_emi(request):
    if request.method=='POST':
        form=EMIForm(request.POST)
        if form.is_valid():
            emi=form.save(commit=False)
            emi.user=request.user
            emi.save()
            return redirect('home:dashboard_view')
    else:
        form=EMIForm()
    return render(request,'add_emi.html',{'form':form})

#edit EMI
@login_required
def edit_emi(request, emi_id):
    emi = get_object_or_404(EMI, id=emi_id, user=request.user)
    
    if request.method == 'POST':
        form = EMIForm(request.POST, instance=emi)
        if form.is_valid():
            form.save()
            return redirect('home:dashboard_view')
    else:
        form = EMIForm(instance=emi)
    
    return render(request, 'edit_emi.html', {'form': form})

class ReportView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # Optionally get a specific date from the request query parameters
        date = request.query_params.get('date')  # Format: YYYY-MM-DD

        if date:
            # Filter expenses by date
            expenses = Expense.objects.filter(user=request.user, date=date)
        else:
            # Get all expenses for the user if no date is provided
            expenses = Expense.objects.filter(user=request.user)

        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Prepare detailed report data
        report_data = {
            'total_expense': total_expense,
            'details': expenses.values('category__name').annotate(total=Sum('amount')),
        }
        return Response(report_data)

    @action(detail=False, methods=['get'])
    def generate_pdf(self, request):
        date = request.query_params.get('date')  # Optional date filter
        
        if date:
            expenses = Expense.objects.filter(user=request.user, date=date)
        else:
            expenses = Expense.objects.filter(user=request.user)

        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        p = canvas.Canvas(response, pagesize=letter)

        # Draw the report content
        p.drawString(100, 750, "Expense Report")
        p.drawString(100, 730, f"Date Filter: {date if date else 'All Dates'}")
        p.drawString(100, 710, f"Total Expense: {total_expense}")
        
        # Draw category-wise expense details
        y_position = 690
        for expense in expenses.values('category__name').annotate(total=Sum('amount')):
            p.drawString(100, y_position, f"Category: {expense['category__name']}, Amount: {expense['total']}")
            y_position -= 20
        
        p.showPage()
        p.save()
        return response
    
#profile view
@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def charts_view(request):
    return render(request, 'charts.html')

class ChartDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):        
        user = request.user
       
        # Total income and expense over time (for line chart)
        income_data = Income.objects.filter(user=user).values('date').annotate(total=Sum('amount'))
        expense_data = Expense.objects.filter(user=user).values('date').annotate(total=Sum('amount'))


        # Budget utilization by category (for bar chart)
        budget_data = Budget.objects.filter(user=user).values('category__name').annotate(limit=Sum('limit'))
        expense_by_category = Expense.objects.filter(user=user).values('category__name').annotate(total=Sum('amount'))


        # Category-wise spending (for pie chart)
        category_spending = Expense.objects.filter(user=user).values('category__name').annotate(total=Sum('amount'))


        return Response({
            'income_data': income_data,
            'expense_data': expense_data,
            'budget_data': budget_data,
            'expense_by_category': expense_by_category,
            'category_spending': category_spending,
        })

@login_required
def generate_pdf(request):
    user = request.user

    # Get total expenses
    total_expenses = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0

    # Get expenses by category
    expenses_by_category = Expense.objects.filter(user=user).values('category__name').annotate(total=Sum('amount'))

    # Create a buffer to store the PDF content
    buffer = BytesIO()
    # Create a canvas object with letter size
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set up styles for the report
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8)
    ])

    # Add title to the PDF
    pdf.drawString(inch, 10.5 * inch, "Expense Report")

    # Add total expenses
    pdf.drawString(inch, 10 * inch, f"Total Expenses: Rs.{total_expenses:.2f}")

    # Create the table data
    data = [
        ['Category', 'Total Spent']
    ]
    for expense in expenses_by_category:
        data.append([expense['category__name'], f"Rs.{expense['total']:.2f}"])
    
    
    # Create a table object
    table = Table(data)
    table.setStyle(table_style)

    # Add the table to the PDF
    table.wrapOn(pdf, 7 * inch, 5 * inch)
    table.drawOn(pdf, inch, 7 * inch)

    # Save the PDF to the buffer
    pdf.save()

    # Set the content type and filename for the response
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="expense_report_{user.username}.pdf"'

    return response