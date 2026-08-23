# Hospital Appointment and Department Management System


# Hospital data
available_departments = {"Cardiology", "Orthopedics", "Neurology", "General Medicine",
                          "Dermatology", "ENT", "Pathology", "Radiology"}

available_doctors = {"Dr. Mehta", "Dr. Sharma", "Dr. Iyer", "Dr. Khan", "Dr. Rao"}

emergency_departments = {"Cardiology", "Neurology", "Trauma"}

# Patient data 
patient_name = "Ravi"

# list, because a patient can request the same department more than once by mistake
requested_departments = ["Cardiology", "Dermatology", "Cardiology", "Oncology"]

# list, because a patient could have visited a department many times before
previously_visited_departments = ["Dermatology", "ENT"]

preferred_doctors = {"Dr. Mehta", "Dr. Verma"}


#  Find duplicate requests 
seen_departments = []
duplicate_requests = []

for dept in requested_departments:
    if dept in seen_departments:
        if dept not in duplicate_requests:
            duplicate_requests.append(dept)
    else:
        seen_departments.append(dept)

print("Duplicate requests found:", duplicate_requests)


#  Convert requested list to a set (removes duplicates) 
requested_set = set(requested_departments)


#  Common / available departments (intersection) 
common_departments = requested_set.intersection(available_departments)
print("Common departments (requested and offered):", common_departments)


# Unavailable departments (difference) 
unavailable_departments = requested_set.difference(available_departments)
print("Unavailable departments:", unavailable_departments)


#  Previously visited departments among current request
previously_visited_set = set(previously_visited_departments)
already_visited = requested_set.intersection(previously_visited_set)
print("Already visited before:", already_visited)


#  Emergency departments among current request 
emergency_hits = requested_set.intersection(emergency_departments)
print("Departments needing immediate attention:", emergency_hits)


# Doctor matching 
matched_doctors = preferred_doctors.intersection(available_doctors)
unavailable_doctors = preferred_doctors.difference(available_doctors)

print("Matched doctors:", matched_doctors)
print("Unavailable preferred doctors:", unavailable_doctors)


#  Decide recommended department 
recommended_department = None

if len(emergency_hits) > 0:
    emergency_list = list(emergency_hits)
    recommended_department = emergency_list[0]   # indexing
elif len(common_departments) > 0:
    common_list = list(common_departments)
    recommended_department = common_list[0]      # indexing

print("Recommended department:", recommended_department)


#  Final appointment status 
if len(emergency_hits) > 0:
    final_status = "URGENT - Immediate appointment needed"
elif len(common_departments) > 0:
    final_status = "Confirmed"
else:
    final_status = "Not available"

print("Final appointment status:", final_status)


#  Final Report 
print()
print("---------- FINAL APPOINTMENT REPORT ----------")
print("Patient Name:", patient_name)
print("Requested Departments:", requested_departments)
print("Available Departments:", common_departments)
print("Unavailable Departments:", unavailable_departments)
print("Common Departments:", common_departments)
print("Previously Visited Departments:", already_visited)
print("Emergency Departments:", emergency_hits)
print("Duplicate Requests:", duplicate_requests)
print("Recommended Department:", recommended_department)
print("Final Status:", final_status)
