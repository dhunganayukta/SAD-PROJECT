from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transaction


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})




@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    balance = sum(t.amount for t in transactions)  
    return render(request, 'dashboard.html', {
        'transactions': transactions,
        'balance': balance,
    })

@login_required
def add_transaction(request):
    if request.method == 'POST':

        amount = request.POST.get('amount')
        category = request.POST.get('category')
        date = request.POST.get('date')
        from .models import Category
        category_object , created = Category.objects.get_or_create(name=category)

        transaction = Transaction(
            user=request.user,
            amount=amount,
            category=category_object,
            date=date,
            notes = ''
        )

        transaction.save()
        return redirect('dashboard')

    return render(request, 'tracker/addTransaction.html')

def index(request):
    return render(request, 'tracker/index.html')
