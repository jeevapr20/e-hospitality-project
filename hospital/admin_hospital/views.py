from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import logout
import stripe
from django.conf import settings
from .forms import PaymentForm
from django.shortcuts import get_object_or_404
# Create your views here.
def Home(request):
    return render(request,'base.html')

def Contact(request):
    return render(request,'contact.html')

def About(request):
    return render(request,'about.html')

def Doctor_List(request):
    return render(request,'doctor_list.html')

def Appointment_Page(request):
    return render(request,'appointment.html')

def Service(request):
    return render(request,'service.html')

def Login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        role = request.POST['role']
        
        # Authenticate the user
        user = authenticate(username=uname, password=pwd)
        
        if user is not None:
            # Check for the role and user type
            if role == "admin" or user.is_admin:
                login(request, user)
                return redirect(reverse('admin_dashboard'))
            elif role == "doctor" or user.is_doctor:
                login(request, user)
                return redirect(reverse('doctor_dashboard'))
            elif role == "patient" or user.is_patient:
                login(request, user)
                return redirect(reverse('patient_dashboard'))
            else:
                messages.error(request, "Invalid role selected or role mismatch.")
                return render(request, 'login.html')
        else:
            # If authentication fails
            messages.error(request, "Invalid credentials. Please check your username or password.")
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def Logout(request):

    if request.user.is_authenticated:

        logout(request)
    
    return redirect('login')

def register_patient(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        
        try:
           
            user = CustomUser.objects.create_user(username=uname, password=pwd)
            user.is_patient = True  
            user.save()

         
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login') 

        except Exception as e:
           
            print(e)
            error = "Error in registration"
            return render(request, 'register_patient.html', {'error': error})

    return render(request, 'register_patient.html')

def register_doctor(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        
        try:
           
            user = CustomUser.objects.create_user(username=uname, password=pwd)
            user.is_doctor = True  
            user.save()

         
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login') 

        except Exception as e:
           
            print(e)
            error = "Error in registration"
            return render(request, 'register_doctor.html', {'error': error})

    return render(request, 'register_doctor.html')

def register_admin(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        
        try:
           
            user = CustomUser.objects.create_user(username=uname, password=pwd)
            user.is_admin = True  
            user.save()

         
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login') 

        except Exception as e:
           
            print(e)
            error = "Error in registration"
            return render(request, 'register_admin.html', {'error': error})

    return render(request, 'register_admin.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def Add_Doctor(request):
    error=""
    if not request.user.is_admin:
        return redirect('login')
    departments = Department.objects.all()
    if request.method == 'POST':
        n=request.POST['name']
        m=request.POST['mobile']
        d_id=request.POST['department']
        
        try:
            department = Department.objects.get(id=d_id)
            Doctor.objects.create(name=n,mobile=m,department=department)
            messages.success(request, "Doctor records saved successfully!")
            return redirect('view_doctor')
            
        except Exception as e:
            messages.error(request, "Something went wrong: " + str(e))
    return render(request, 'add_doctor.html', {'departments': departments})

def View_Doctor(request):
    if not request.user.is_admin:
        return redirect('login')
    doc=Doctor.objects.all()
    d={'doc':doc}
    return render(request,'view_doctor.html',d)

def Delete_Doctor(request,pid):
    if not request.user.is_admin:
        return redirect('login')
    doctor=Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')

def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

def Add_Patient(request):
    error=""
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        n=request.POST['name']
        g=request.POST['gender']
        m=request.POST['mobile']
        e=request.POST['email']
        a=request.POST['address']
        
        try:
            Patient.objects.create(name=n,gender=g,mobile=m,email=e,address=a)
            messages.success(request, "Patient records saved successfully!")
            return redirect('view_patient')
            
        except Exception as e:
            messages.error(request, "Something went wrong: " + str(e))
    return render(request, 'add_patient.html')

def View_Patient(request):
    if not request.user.is_authenticated:
        return redirect('login')
    pat=Patient.objects.all()
    p={'pat':pat}
    return render(request,'view_patient.html',p)

def Delete_Patient(request,pid):
    if not request.user.is_admin:
        return redirect('login')
    patient=Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')

def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')


def Add_Appointment(request):
    error = ""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get all doctors and patients
    doctor1 = Doctor.objects.all()
    patient1 = Patient.objects.all()
    
    if request.method == 'POST':
        # Get the selected doctor, patient, date, and time from the form
        d = request.POST['doctor']
        p = request.POST['patient']
        d1 = request.POST['date1']
        t1 = request.POST['time1']
        
        # Correctly filter the doctor and patient by ID (not name)
        doctor = Doctor.objects.get(id=d)
        patient = Patient.objects.get(id=p)
        
        try:
            # Create a new appointment
            Appointment.objects.create(doctor=doctor, patient=patient, date1=d1, time1=t1)
            messages.success(request, "Appointment records saved successfully!")
            return redirect('view_appointment')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
    
    # Pass the doctors and patients to the template
    d = {'doctor': doctor1, 'patient': patient1, 'error': error}
    return render(request, 'add_appointment.html', d)


def View_Appointment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    appoint=Appointment.objects.all()
    app={'appoint':appoint}
    return render(request,'view_appointment.html',app)

def Delete_Appointment(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    appoint=Appointment.objects.get(id=pid)
    appoint.delete()
    return redirect('view_appointment')

def create_checkout_session(request):
    if request.method == 'POST':  
        form = PaymentForm(request.POST)
        if form.is_valid():  
            amount = form.cleaned_data['amount']
            
           
            amount_in_cents = int(amount * 100)

           
            stripe.api_key = settings.STRIPE_SECRET_KEY

           
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Custom Payment', 
                        },
                        'unit_amount': amount_in_cents, 
                    },
                    'quantity': 1,
                }],
                success_url=request.build_absolute_uri(reverse('success')),  
                cancel_url=request.build_absolute_uri(reverse('cancel')),    
            )

            
            return redirect(checkout_session.url, code=303)
        else:
            
            return render(request, 'create_checkout_session.html', {'form': form})
    else:
        
        form = PaymentForm()  

    return render(request, 'create_checkout_session.html', {'form': form})
   
def success(request):
    return render(request,'success.html')

def cancel(request):
    return render(request,'cancel.html')

def Add_Medical(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Get all patients to display in the form dropdown or field
    patients = Patient.objects.all()

    if request.method == 'POST':
        # Getting form data
        pat = request.POST['patient']
        dia = request.POST['diagnosis']
        tre = request.POST['treatment']
        dat = request.POST['date_of_treatment']
        pre = request.POST['prescribed_medication']
        
        # Retrieve the patient object
        patient = Patient.objects.filter(id=pat).first()

        if patient:
            # Create a new MedicalHistory record
            try:
                MedicalHistory.objects.create(
                    patient=patient,
                    diagnosis=dia,
                    treatment=tre,
                    date_of_treatment=dat,
                    prescribed_medication=pre
                )
                messages.success(request, "Medical History added successfully!")
                return redirect('view_medical')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Patient not found!")

    return render(request, 'add_medical.html', {'patients': patients})

def View_Medical(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Fetch all medical history records
    medical_histories = MedicalHistory.objects.all()

    # Send the medical histories to the template for rendering
    return render(request, 'view_medical.html', {'medical_histories': medical_histories})

def Delete_Medical(request, pid):
    if not request.user.is_authenticated or not request.user.is_doctor:
        return redirect('login')

    medical_history = MedicalHistory.objects.get(id=pid)
    medical_history.delete()
    return redirect('view_medical')