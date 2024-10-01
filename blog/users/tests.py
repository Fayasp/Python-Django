if not username and not email and not age_str:

            errors["username"] = "Username must be given"
            errors["email_error"] = "Email must be given"
            errors["age"] = "Age Must be provided" 
                
            return JsonResponse(errors, status=400)
                
       
        if not username and not email:
            errors["username"] = "Username must be given"
            errors["email_error"] = "Email must be given"
            return JsonResponse(errors, status=400)
        
        if not email and not age_str:
             errors["email_error"] = "Email must be given"
             errors["age"] = "Age Must be provided"
             return JsonResponse(errors, status=400)
        
        if email_validate is False:
             errors["email_validate"] = "Email Must be valid"
             

        
        if not username and not age_str:
             errors["username"] = "username must be given"
             errors["age"] = "Age Must be provided"
             return JsonResponse(errors, status=400)

        if not username:
            print("username if")
            return JsonResponse({"username": "Username must be given"},status = 400)
        
        
        if email_length == 0:
            print("email_lengh if")
            return JsonResponse({"emai_lenth_error" : "please enter the email"},status = 400)
        
        
        if not email:
            print("email if")       
            return JsonResponse({"email" : "Email must be provided"}, status = 400)
        
        
        if age_str is not None and age_str.isdigit():
            if int(age_str) > 0:
                age = int(age_str)
            else:
             errors["age_zero_error"] = "Age should be greater than zero"

             print(errors,2222222222222)
             return JsonResponse(errors,status = 400)

            

        elif age_str is not None:
            age = age_str

        else:
            age = None 

        if not age:
            return JsonResponse({"age" : "Age must be Provided"}, status = 400)

        if not isinstance(age, int):
            print("isinstance if")
            return JsonResponse({"age_valid": "Age must be an integer"}, status = 400)