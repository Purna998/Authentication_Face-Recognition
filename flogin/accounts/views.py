from django.shortcuts import render
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .models import *
import face_recognition
# Create your views here.
@csrf_exempt
def register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        face_image_data=request.POST['face_image']
        print(face_image_data)
        face_image_data=face_image_data.split(",")[1]
        face_image=ContentFile(base64.b64decode(face_image_data),name=f'{username}_.jpg')
        # print(face_image)
        try:
            user=User.objects.create(user=user)
        except Exception as e:
            return JsonResponse({
            'status':'sucess','message':'Username already taken!'
        })
        UserImage.objects.create(username=username,face_image=face_image)
        return JsonResponse({
            'status':'sucess','message':'User registered successfully'
        })
    return render(request,'register.html')

def login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        face_image_data=request.POST['face_image']

        try: 
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                'status':'success','message':'Invalid Username'
            })
            face_image_data=face_image.data.split(",")[1]
            uploaded_image=ContentFile(base64.b64decode(face_image_data),name=f'{username}_.jpg')

            uploaded_face_image=face_recognition.load_image_file(uploaded_image)
            uploaded_face_encoding=face_recognition.face_encodings(uploaded_face_image)

            if uploaded_face_encoding:
                uploaded_face_encoding=uploaded_face_encoding[0]
                user_image=UserImages.objects.filter(user=user).last()
                stored_face_image=face_recognition.load_image_file(user_image.face_image.path)
                stored_face_encoding=face_recognition.face_encodings(stored_face_image)

                match=face_recognition.compare_faces([stored_face_encoding],uploaded_face_encoding)
                
                if match[0]:
                    return JsonResponse({'status':'success','message':'Logged in'})
            
            return JsonResponse({'status':'success','message':'Not Logged in'})
    return render(request,'login.html')