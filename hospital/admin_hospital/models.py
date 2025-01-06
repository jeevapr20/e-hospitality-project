from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Department(models.Model):
    name = models.CharField(max_length=200) 

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=20, null=True)  
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date1 = models.DateField()
    time1 = models.TimeField()
    
    def __str__(self):
        return f"{self.doctor.name} -- {self.patient.name}"

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    diagnosis = models.TextField()
    treatment = models.TextField()
    date_of_treatment = models.DateField()
    prescribed_medication = models.TextField()

    def __str__(self):
        return f"Medical history of {self.patient.name}"
