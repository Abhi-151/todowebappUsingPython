from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
# from to_do_project.database import fetch_query,update_query
from to_do_app.models import Tasks,TblAdmin,AdminLoginAnalytics
from django.utils import timezone
from rest_framework import status
from datetime import datetime
# from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password,make_password
import secrets
import pytz

def generate_token(token=''):
    token=""
    token = secrets.token_urlsafe(30)
    return token
    
@api_view(["POST"])
def get_tasks(request):
    try:
        tasks = Tasks.objects.all().order_by('-autoid')
        tasks_data = [{"autoid": task.autoid, "task_name": task.task_name, "is_completed": task.is_completed, "created_at": task.created_at} for task in tasks]
        return JsonResponse({
            "status":status.HTTP_200_OK,
            "success":1,
            "message":"Tasks fetched successfully!",
            "data": tasks_data})
    except Exception as e:
        return JsonResponse({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,"success":0,"error": str(e)})
    

@api_view(["POST"])
def create_task(request):
    try:
        task_name = request.data.get("task_name")

        if not task_name:
            return JsonResponse({"error": "Task name is required!"}, status=400)
        #only for git checks
        is_completed = request.data.get("is_completed", False)

        created_at = datetime.now()

        task = Tasks.objects.create(
            task_name=task_name, 
            is_completed=is_completed, 
            created_at=created_at
        )

        return JsonResponse({
            "message": "Task created successfully!",
            "status":status.HTTP_200_OK,
            "success":1,
            "task": {
                "autoId": task.autoid,
                "task_name": task.task_name,
                "is_completed": task.is_completed,
                "created_at": task.created_at
            }
        })

    except Exception as e:
        return JsonResponse({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,"success":0,"error": str(e)})
    

@api_view(["POST"])
def bulk_create_tasks(request):
    try:
        tasks_data = request.data.get("tasks", [])
        
        tasks = []
        for task in tasks_data:
            tasks.append(Tasks(task_name=task["task_name"], is_completed=task["is_completed"],created_at=datetime.now()))

        Tasks.objects.bulk_create(tasks)

        return JsonResponse({"message": "Tasks created successfully!", "status":status.HTTP_201_CREATED,"sucess":0})
    except Exception as e:
        return JsonResponse({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,"success":0,"error": str(e)})
    
# @api_view(["POST"])
# def update_task(request):
#     try:
#         task_id = request.data.get("autoId")
#         # task_name = request.data.get("task_name")
#         is_completed = request.data.get("is_completed", False)

#         Tasks.objects.filter(autoid=task_id).update(is_completed=is_completed)

#         return JsonResponse({
#             "message": "Task updated successfully!",
#         })
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@api_view(["POST"])
def update_tasks(request):
    try:
        task_data = request.data.get("tasks")

        tasks_to_update=[]
        for task in task_data:

            task_id =task.get("autoId")
            is_completed =task.get("is_completed")

            tasks_to_update.append((task_id,is_completed))

        for task_id,is_completed in tasks_to_update:
            Tasks.objects.filter(autoid=task_id).update(is_completed=is_completed,updated_date = datetime.now())

        return JsonResponse({
            "status":status.HTTP_200_OK,
            "success":1,
            "message": "Task updated successfully!",
        })
    except Exception as e:
        return JsonResponse({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,"success":0,"error": str(e)})
    
@api_view(["POST"])
def create_admin(request):
    try:
        admin_first_name = (request.data.get("admin_first_name")).strip()
        admin_last_name = (request.data.get("admin_last_name")).strip()
        admin_email = (request.data.get("admin_email")).strip()
        admin_password = (request.data.get("admin_password")).strip()
        admin_role = (request.data.get("admin_role")).strip()
        created_date = datetime.now()

        if not admin_first_name or not admin_email or not admin_last_name or not admin_password or not admin_role:
            return JsonResponse({"error": "Admin name, email, and password are required!"}, status=status.HTTP_400_BAD_REQUEST)

        ##create hash_passowrd
        # hashed_password = make_password(admin_password)

        TblAdmin.objects.create(
            first_name=admin_first_name, 
            last_name=admin_last_name, 
            email=admin_email,
            # password = hashed_password,
            password=admin_password,
            role=admin_role,
            created_at=created_date,
        )

        return JsonResponse({"status":status.HTTP_200_OK, "success":1,"message": "Admin created successfully!"})

    except Exception as e:
        return JsonResponse({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,"success":0,"error": str(e)})

@api_view(["Post"])
def admin_login(request):
    try:
        email_id = (request.data.get("email")).strip()
        password = request.data.get("password")
        
        #verify email address is correct or not
        admin = TblAdmin.objects.filter(email=email_id,status=1).first()

        if not admin:
            return JsonResponse({"status": status.HTTP_400_BAD_REQUEST, "success": 0, "message": "Admin not found with the provided email."})
        
        #verify password is correct or incorrect
        password_queryset = TblAdmin.objects.filter(email=email_id,status=1,password=password)

        # result=(check_password(password, admin.password))
        if not password_queryset.exists():
            return JsonResponse({"status": status.HTTP_400_BAD_REQUEST, "success": 0, "message": "Please enter correct password."})
        
        #fetch adminId from 
        adminId = admin.admin_id
        login_time = datetime.now()
        ip = get_client_ip(request)
        login_status = 1
        created_at  = datetime.now()
        token = generate_token()
        if AdminLoginAnalytics.objects.filter(login_token = token):
            token = generate_token()

        # admin_instance = TblAdmin.objects.get(admin_id=adminId)
        AdminLoginAnalytics.objects.filter(admin_id=adminId).update(login_status=0)
        AdminLoginAnalytics.objects.create(
            admin_id = adminId,
            login_time = login_time,
            ip_address = ip,
            login_status = login_status,
            created_at = created_at,
            login_token = token
        ) 

        return JsonResponse({ "status":status.HTTP_200_OK, "success":1, "message":"Login Successfull.","data": token })
            
    except Exception as e:
        return JsonResponse({"status": status.HTTP_500_INTERNAL_SERVER_ERROR,"success":0,"error": str(e)})