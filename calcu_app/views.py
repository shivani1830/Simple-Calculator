from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from .forms import *



# Create your views here.

def index(request):
    return render(request, 'calcu_app/index.html')

def about(request):
    return render(request, 'calcu_app/about.html')

def calculate(request):
    if request.method == 'POST':
        # Handle form submission and perform calculations here
        # For example, you can get input values, perform calculations, and pass the result to the template
        num1 = float(request.POST.get('num1', 0))
        num2 = float(request.POST.get('num2', 0))
        operator = request.POST.get('operator', '+')

        if operator == '+':
            result = num1 + num2
            operation_type = "Addition"
        elif operator == '-':
            result = num1 - num2
            operation_type = "Subtraction"
        elif operator == '*':
            result = num1 * num2
            operation_type = "Multiplication"
        elif operator == '/':
            if num2 != 0:
                result = num1 / num2
                operation_type = "Division"
            else:
                result = "Cannot divide by zero"
                operation_type = None
        else:
            result = "Invalid operator"
            operation_type = None

        return render(request, 'calcu_app/index.html', {'result': result, 'operation_type': operation_type})

    return render(request, 'calcu_app/index.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly!")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your message has been sent successfully!')

    return render(request, 'calcu_app/contact.html')

def calculation_history(request):
    calculations = Calculation.objects.all()
    return render(request, 'calcu_app/calculation_history.html', {'calculations': calculations})

def calculate(request):
    if request.method == 'POST':
        form = CalculationForm(request.POST)
        if form.is_valid():
            # Perform calculations
            num1 = form.cleaned_data['num1']
            num2 = form.cleaned_data['num2']
            operator = form.cleaned_data['operator']

            if operator == '+':
                result = num1 + num2
                operation_type = "Addition"
            elif operator == '-':
                result = num1 - num2
                operation_type = "Subtraction"
            elif operator == '*':
                result = num1 * num2
                operation_type = "Multiplication"
            elif operator == '/':
                if num2 != 0:
                    result = num1 / num2
                    operation_type = "Division"
                else:
                    result = "Cannot divide by zero"
                    operation_type = None
            else:
                result = "Invalid operator"
                operation_type = None

            # Save the calculation details to the database
            Calculation.objects.create(
                num1=num1,
                num2=num2,
                operator=operator,
                result=result
            )

            return render(request, 'calcu_app/index.html', {'result': result, 'operation_type': operation_type})
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = CalculationForm()

    return render(request, 'calcu_app/index.html', {'form': form})

