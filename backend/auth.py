from bson import ObjectId
from flask import request, session, jsonify
from pymongo import ReturnDocument
import bcrypt


def register(UserRecords):
    
    '''
    ```
    Request:
    {
        firstName: string,
        lastName: string,
        email: string,
        password: string,
        confirmPassword: string
    }
    Response:
    {
        status: 200
        data: Success message
        
        status: 400
        data: Error message
        
    }
    ```
    '''
    
    try:
        req = request.get_json()
        name = {"firstName": req["firstName"], "lastName": req["lastName"]}
        email = req["email"]
        password = req["password"]
        confirmPassword = req["confirmPassword"]

        email_found = UserRecords.find_one({"email": email})
        if email_found:
            return jsonify({'error': "This email already exists in database"}), 400
        if password != confirmPassword:
            return jsonify({'error': "Passwords should match!"}), 400

        else:
            hashed = bcrypt.hashpw(
                confirmPassword.encode("utf-8"), bcrypt.gensalt())
            user_input = {"name": name, "email": email, "password": hashed}
            UserRecords.insert_one(user_input)
            return jsonify({'message': 'Login successful'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400


def login(UserRecords):
    
    '''
    ```
    Request:
    {
        email: string,
        password: string
    }
    Response:
    {
        status: 200
        data: Success message
        
        status: 400
        data: Error message
        
    }
    ```
    '''
    
    try:
        req = request.get_json()
        email = req["email"]
        password = req["password"]
        email_found = UserRecords.find_one({"email": email})
        if email_found:
            passwordcheck = email_found["password"]
            if bcrypt.checkpw(password.encode("utf-8"), passwordcheck):
                return jsonify({'message': 'Login successful'}), 200
            else:
                if "email" in session:
                    return jsonify({'message': 'Login successful'}), 200
                return jsonify({'error': "Wrong password"}), 400
        else:
            return jsonify({'error': "Email not found"}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400


def logout():
    
    '''
    ```
    Request:
    {
        
    }
    Response:
    {
        data: message (Success)
        
    }
    ```
    '''
    
    return jsonify({'message': 'Logout successful'}), 200


def create_profile(UserProfiles):
    
    '''
    ```
    Request:
    {
        firstName: string,
        lastName: string,
        email: string,
        phone: number,
        city: string,
        state: string,
        resume: file ,
        gitHub: string,
        linkedIn: string,
        skills: string,
        about: string,
        interests: string,
        companyName: string,
        jobTitle: string,
        description: string,
        jobCity: string,
        jobState: string,
        jobFrom: string,
        toFrom: string,
        curentJob: string,
        institution: string,
        major: string,
        degree: string,
        courses: string,
        universityCity: string,
        universityState: string,
        universityFromDate: date,
        universityToDate: date,
        curentUniversity: string
       
    }
    Response:
    {
        status: 200
        data: Success message
        
        status: 400
        data: Error message
        
    }
    ```
    '''
    
    try:
        if request:
            req = request.get_json()
            email = req["email"]
            email_found = UserProfiles.find_one({"email": email})
            if email_found:
                return jsonify({"error": "Profile already created."}), 400
            else:
                user_profile = {
                    "firstName": req["firstName"],
                    "lastName": req["lastName"],
                    "email": req["email"],
                    "phone": req.get("phone"),
                    "city": req.get("city"),
                    "state": req.get("state"),
                    "resume": req.get("resume"),
                    "gitHub": req.get("gitHub"),
                    "linkedIn": req.get("linkedin"),
                    "skills": req.get("skills", '').split(","),
                    "about": req.get("about"),
                    "interests": req.get("interests", '').split(","),
                    "companyName": req.get("companyName"),
                    "jobTitle": req.get("jobTitle"),
                    "description": req.get("description"),
                    "jobCity": req.get("jobCity"),
                    "jobState": req.get("jobState"),
                    "jobFrom": req.get("jobDate"),
                    "toFrom": req.get("jobDate"),
                    "curentJob": req.get("curentJob"),
                    "institution": req.get("institution"),
                    "major": req.get("major"),
                    "degree": req.get("degree"),
                    "courses": req.get("courses", '').split(","),
                    "universityCity": req.get("universityCity"),
                    "universityState": req.get("universityState"),
                    "universityFromDate": req.get("universityDate"),
                    "universityToDate": req.get("universityDate"),
                    "curentUniversity": req.get("curentUniversity")
                }
                try:
                    UserProfiles.insert_one(user_profile)
                    return jsonify({"message": "Profile created successfully"}), 200
                except Exception as e:
                    return jsonify({"error": "Unable to create profile"}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400


def view_profile(UserProfiles):
    
    '''
    ```
    Request:
    {
        email: string
    }
    Response:
    {
        status: 200
        data: Success message
        
        status: 400
        data: Error message
        
    }
    ```
    '''
    
    try:
        if request:
            email = request.args.get("email")
            filter = {"email": email}
            profile = UserProfiles.find(filter)
            if profile == None:
                return jsonify({'message': "Create a profile first", "profile": {}}), 200
            else:
                profile_out = {}
                for p in profile:
                    p['_id'] = str(p['_id'])
                    profile_out = p
                return jsonify({'message': "Found User Profile", "profile": profile_out}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400


def clear_profile(UserProfiles, UserRecords):
    
    '''
    ```
    Request:
    {
        email: string
    }
    Response:
    {
        status: 200
        data: Success message
        
        status: 400
        data: Error message
        
    }
    ```
    '''
    
    try:
        if request:
            req = request.get_json()
            email_to_delete = req["email"]
            _id = req["_id"]
            delete_user = UserRecords.find_one({"email": email_to_delete})
            if delete_user == None:
                return jsonify({'error': "User email not found"}), 400
            delete_profile = UserProfiles.find_one_and_delete(
                {"_id": ObjectId(_id), "email": email_to_delete})
            if delete_profile == None:
                return jsonify({'error': "Profile not found"}), 400
            else:
                return jsonify({"message": "User Profile cleared successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400


def modify_profile(UserProfiles):
    
    '''
    ```
    Request:
    {
        firstName: string,
        lastName: string,
        email: string,
        phone: number,
        city: string,
        state: string,
        state: string,
        resume: file ,
        gitHub: string,
        linkedIn: string,
        skills: string,
        about: string,
        interests: string,
        companyName: string,
        jobTitle: string,
        description: string,
        jobCity: string,
        jobState: string,
        jobFrom: string,
        toFrom: string,
        curentJob: string,
        institution: string,
        major: string,
        degree: string,
        courses: string,
        universityCity: string,
        universityState: string,
        universityFromDate: date,
        universityToDate: date,
        curentUniversity: string
       
    }
    Response:
    {
        status: 200
        data: Success message
        
        status: 400
        data: Error message
        
    }
    ```
    '''
    
    try:
        if request:
            req = request.get_json()
            _id = req["_id"]
            email = req["email"]
            email_found = UserProfiles.find_one(
                {"_id": ObjectId(_id), "email": email})
            if not email_found:
                return jsonify({"error": "Profile not found."}), 400
            else:
                user_profile = {
                    "firstName": req["firstName"],
                    "lastName": req["lastName"],
                    "email": req["email"],
                    "phone": req.get("phone"),
                    "city": req.get("city"),
                    "state": req.get("state"),
                    "resume": req.get("resume"),
                    "gitHub": req.get("gitHub"),
                    "linkedIn": req.get("linkedin"),
                    "skills": req.get("skills", '').split(","),
                    "about": req.get("about"),
                    "interests": req.get("interests", '').split(","),
                    "companyName": req.get("companyName"),
                    "jobTitle": req.get("jobTitle"),
                    "description": req.get("description"),
                    "jobCity": req.get("jobCity"),
                    "jobState": req.get("jobState"),
                    "jobFrom": req.get("jobDate"),
                    "toFrom": req.get("jobDate"),
                    "curentJob": req.get("curentJob"),
                    "institution": req.get("institution"),
                    "major": req.get("major"),
                    "degree": req.get("degree"),
                    "courses": req.get("courses", '').split(","),
                    "universityCity": req.get("universityCity"),
                    "universityState": req.get("universityState"),
                    "universityFromDate": req.get("universityDate"),
                    "universityToDate": req.get("universityDate"),
                    "curentUniversity": req.get("curentUniversity")
                }
                set_values = {"$set": user_profile}
                filter = {"email": email}
                modify_document = UserProfiles.find_one_and_update(
                    filter, set_values, return_document=ReturnDocument.AFTER)
                if modify_document == None:
                    return jsonify({"error": "Unable to modify profile"}), 400
                else:
                    return jsonify({"message": "Profile modified successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400
