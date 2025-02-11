from django.shortcuts import render, redirect
from . models import UserPersonalModel
from . forms import UserPersonalForm, UserRegisterForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
import numpy as np
import joblib

from .models import UserPredictModel
from .forms import UserPredictForm
import csv
from nltk.chat.util import Chat, reflections


def Landing_1(request):
    return render(request, '1_Landing.html')

def Register_2(request):
    form = UserRegisterForm()
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was successfully created. ' + user)
            return redirect('Login_3')

    context = {'form':form}
    return render(request, '2_Register.html', context)


def Login_3(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home_4')
        else:
            messages.info(request, 'Username OR Password incorrect')

    context = {}
    return render(request,'3_Login.html', context)

def Home_4(request):
    return render(request, '4_Home.html')

def Teamates_5(request):
    return render(request,'5_Teamates.html')

def Domain_Result_6(request):
    return render(request,'6_Domain_Result.html')

def Problem_Statement_7(request):
    return render(request,'7_Problem_Statement.html')
    

def Per_Info_8(request):
    if request.method == 'POST':
        fieldss = ['firstname','lastname','age','address','phone','city','state','country']
        form = UserPersonalForm(request.POST)
        if form.is_valid():
            print('Saving data in Form')
            form.save()
        return render(request, '4_Home.html', {'form':form})
    else:
        print('Else working')
        form = UserPersonalForm(request.POST)    
        return render(request, '8_Per_Info.html', {'form':form})
    
    
Model1 = joblib.load('C:/Users/jessi/Music/MAIN_PROJECT/CODE/DEPLOYMENT/PROJECT/APP/MODEL.pkl')  
  
def Deploy_9(request): 
    if request.method == "POST":
        int_features = [x for x in request.POST.values()]
        int_features = int_features[1:]
        print(int_features)
        final_features = [np.array(int_features, dtype=object)]
        print(final_features)
        prediction = Model1.predict(final_features)
        print(prediction)
        output = prediction[0]
        print(output)
        if output == 0:
            a =  "THE VERY LESS DEPRESSION MIGHT BE OCCUR IN THIS CONDITIONS"
            b = "PREVENTIONS : NO PREVENTIONS "
        elif output == 1:
            a = "THE LESS DEPRESSION MIGHT BE OCCUR IN THIS CONDITIONS, THIS IS STAGE 1 DEPRESSION LEVEL."
            b = "PREVENTIONS : Regular Exercise: Physical activity can reduce stress hormones and increase endorphins, improving mood and overall health. Healthy Diet: Consuming a balanced diet rich in fruits, vegetables, lean proteins, and whole grains can support stress reduction. Adequate Sleep: Ensure you get 7-9 hours of quality sleep each night to rejuvenate your body and mind. Mindfulness Meditation: Practicing mindfulness techniques can help manage stress by focusing on the present moment and reducing anxiety. Deep Breathing Exercises: Engage in deep breathing exercises to activate the body's relaxation response and calm the mind."
        elif output == 2:
            a =  "THE MODERATE DEPRESSION MIGHT BE OCCUR IN THIS CONDITIONS. THIS IS STAGE 2 DEPRESSION LEVEL."
            b = "PREVENTIONS : Time Management: Prioritize tasks, set realistic goals, and allocate time effectively to reduce feelings of overwhelm.Limit Caffeine and Alcohol: Excessive consumption of caffeine and alcohol can exacerbate stress, so moderation is key.Social Support: Seek support from friends, family, or a support group to share feelings and gain perspective.Positive Relationships: Cultivate healthy relationships and spend time with people who uplift and support you.Establish Boundaries: Learn to say no when necessary and set boundaries to protect your time and energy."
        elif output == 3:
            a = "THE HIGH DEPRESSION MIGHT BE OCCUR IN THIS CONDITIONS. THIS IS STAGE 3 DEPRESSION LEVEL."
            b = "PREVENTIONS : Express Gratitude: Focus on what you're grateful for each day to shift your mindset towards positivity.Humor and Laughter: Find opportunities for humor and laughter, as they can lighten your mood and relieve tension.Hobbies and Leisure Activities: Engage in activities you enjoy to relax and recharge outside of work or responsibilities.Seek Professional Help: If stress becomes overwhelming, consider seeking support from a therapist or counselor.Practice Assertiveness: Communicate your needs and concerns assertively, rather than bottling up emotions."
        elif output == 4:
            a =  "THE VERY HIGH DEPRESSION MIGHT BE OCCUR IN THIS CONDITIONS. THIS IS STAGE 4 DEPRESSION LEVEL."
            b = "PREVENTIONS : Avoid Procrastination: Break tasks into smaller, manageable steps and tackle them gradually to reduce stress from looming deadlines.Stay Organized: Maintain a clutter-free environment and keep things organized to minimize stress from disorganization.Nature Walks: Spending time outdoors, especially in nature, can promote relaxation and reduce stress levels.Limit Screen Time: Reduce exposure to screens, especially before bedtime, to improve sleep quality and reduce stress.Self-Care Rituals: Incorporate self-care practices into your daily routine, such as taking baths, reading, or practicing hobbies that bring you joy."
           
        return render(request, '9_Deploy.html', {"prediction_text": a, "b":b})
    else:
        return render(request, '9_Deploy.html')
    
def Per_Database_10(request):
    models = UserPersonalModel.objects.all()
    return render(request, '10_Per_Database.html', {'models':models})

def chat_with_user(user_input):
    try:
        with open(csv_filepath, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  
            patterns = [(row[0], row[1].split('|')) for row in csv_reader]
    except FileNotFoundError:
        patterns = []

    chatbot = Chat(patterns, reflections)
    return chatbot.respond(user_input)

csv_filepath = 'C:/Users/jessi/Music/MAIN_PROJECT/CODE/DEPLOYMENT/PROJECT/APP/A.csv'

def Deploy_11(request):
    if request.method == 'POST':
        form = UserPredictForm(request.POST)

        if form.is_valid():
            form.save()
            user_input = form.cleaned_data.get('text')
            response = chat_with_user(user_input)
            print(response)

            data = UserPredictModel.objects.latest('id')
            data.label = response
            data.save()

            return render(request, '11_Deploy.html', {'form': form, 'prediction_text': response})

    else:
        print('Else working')
        form = UserPredictForm()
    return render(request, '11_Deploy.html', {'form': form})


def Database_12(request):
    models = UserPredictModel.objects.all()
    return render(request, '12_Database.html', {'models': models})


def Logout(request):
    logout(request)
    return redirect('Login_3')
