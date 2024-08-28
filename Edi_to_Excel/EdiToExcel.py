from datetime import datetime
import math
import pandas as pd
from Iteduim_all_dictionary import Maintenance_Reason_Code, Cobra_Event_Code, all_Benefit_Status, Employee_Description_of_plan, All_Relationship_Type, Member_Maintenance_Type_Code, Common_parts_of_transaction


def process_person_details(person_code, lines_collection, intcounter, transaction_data_list):
    person_details = lines_collection[intcounter].replace('~', '').split("*")
    if len(person_details) == 10:
        transaction_data_list[f"{person_code} Person SSN"] = person_details[9]
        transaction_data_list[f"{person_code} Person Prefix Name"] = person_details[6]
        transaction_data_list[f"{person_code} Person First Name"] = person_details[4]
        transaction_data_list[f"{person_code} Person Middle Name"] = person_details[5]
        transaction_data_list[f"{person_code} Person Last Name"] = person_details[3]
        transaction_data_list[f"{person_code} Person Suffix Name"] = person_details[7]
    elif len(person_details) == 8:
        transaction_data_list[f"{person_code} Person Prefix Name"] = person_details[6]
        transaction_data_list[f"{person_code} Person First Name"] = person_details[4]
        transaction_data_list[f"{person_code} Person Middle Name"] = person_details[5]
        transaction_data_list[f"{person_code} Person Last Name"] = person_details[3]
        transaction_data_list[f"{person_code} Person Suffix Name"] = person_details[7]
    elif len(person_details) == 7:
        transaction_data_list[f"{person_code} Person Prefix Name"] = person_details[6]
        transaction_data_list[f"{person_code} Person First Name"] = person_details[4]
        transaction_data_list[f"{person_code} Person Middle Name"] = person_details[5]
        transaction_data_list[f"{person_code} Person Last Name"] = person_details[3]
    elif len(person_details) == 6:
        transaction_data_list[f"{person_code} Person First Name"] = person_details[4]
        transaction_data_list[f"{person_code} Person Middle Name"] = person_details[5]
        transaction_data_list[f"{person_code} Person Last Name"] = person_details[3]
    elif len(person_details) == 5:
        transaction_data_list[f"{person_code} Person First Name"] = person_details[4]
        transaction_data_list[f"{person_code} Person Last Name"] = person_details[3]
    elif len(person_details) == 4:
        transaction_data_list[f"{person_code} Person First Name"] = person_details[4]

def process_medicare_details(lines_collection, intcounter, transaction_data_list, member_type):
    medicare_start_dates = []
    medicare_end_dates = []

    medicare_details = lines_collection[intcounter].replace('~', '').split("*")
    if len(medicare_details) >= 13:
        member_date_time_period = medicare_details[12]
        original_date = datetime.strptime(member_date_time_period, "%Y%m%d")
        Date_time_period = original_date.strftime("%m-%d-%Y")
        transaction_data_list[f"{member_type} Date Time Period"] = Date_time_period

    

    if len(medicare_details) >= 7:
        transaction_data_list[f"{member_type} Medicare Status Code"] = medicare_details[6]
    if len(medicare_details) >= 11:
        transaction_data_list [f"{member_type} Y/N Condition Code"] = medicare_details[10]

    Type_of_Relationship_Code = medicare_details[2]
    if Type_of_Relationship_Code in All_Relationship_Type:
        relationship_type = All_Relationship_Type[Type_of_Relationship_Code]
        transaction_data_list[f"{member_type} Relationship Code"] = f"{Type_of_Relationship_Code}- {relationship_type}"

    Maintenance_Type_Code = medicare_details[3]
    if Maintenance_Type_Code in Member_Maintenance_Type_Code:
        Member_Maintenance_type = Member_Maintenance_Type_Code[Maintenance_Type_Code]
        transaction_data_list[f"{member_type} Maintenance Type Code"] = f"{Maintenance_Type_Code}- {Member_Maintenance_type}"  

    if len(medicare_details) >= 6:
        benefit_status = medicare_details[5]
        if benefit_status in all_Benefit_Status:
            Benefit = all_Benefit_Status[benefit_status]
            transaction_data_list[f"{member_type} Benefit Status"] = f"{benefit_status}- {Benefit}"

    Cobra_Events_Code = lines_collection[intcounter].replace(
            '~', '').split("*")

    if len(Cobra_Events_Code) >= 8:
        cobra_event = Cobra_Events_Code[7]
        if cobra_event in Cobra_Event_Code:
            cobra = Cobra_Event_Code[cobra_event]
            transaction_data_list[f"{member_type} Cobra Event Code"] = f"{cobra_event}- {cobra}"

    Maintenance_reason = lines_collection[intcounter].replace(
            '~', '').split("*")
    if len(Maintenance_reason) >= 5:
        maintenance_reasons = Maintenance_reason[4]

        if maintenance_reasons in Maintenance_Reason_Code:
            Maintenence_Reason = Maintenance_Reason_Code[maintenance_reasons]
            transaction_data_list[f"{member_type} Maintenance Reason"] = f"{maintenance_reasons}- {Maintenence_Reason}"


    for intcounter2 in range(intcounter + 1, len(lines_collection)):
           
        if "REF*0F" in lines_collection[intcounter2]:
            depend_ssn_no = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Depend SSN Number"] = depend_ssn_no
        if "REF*23" in lines_collection[intcounter2]:
            supplemental_id = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Sup-Id"] = supplemental_id

        elif "REF*ABB" in lines_collection[intcounter2][0:7]:
            Personal_no = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Personal Id Number"] = Personal_no
        elif "REF*ZZ" in lines_collection[intcounter2][0:7]:
            mutually_defined = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Mutually Defined"] = mutually_defined
        elif "REF*F6" in lines_collection[intcounter2][0:6]:
            Health_Insurance_Claim = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Health Insurance Claim Number"] = Health_Insurance_Claim
  
        elif "REF*17" in lines_collection[intcounter2][0:6]:
            Client_Reporting = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Client Reporting Catagory"] = Client_Reporting

        elif "REF*23" in lines_collection[intcounter2][0:6]:
            Client_Number = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Client Number"] = Client_Number

        elif "REF*3H" in lines_collection[intcounter2][0:6]:
            Case_Number = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Case Number"] = Case_Number

        elif "REF*4H" in lines_collection[intcounter2][0:6]:
            Personal_Identification_No = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Personal Identification Number"] = Personal_Identification_No

        elif "REF*6O" in lines_collection[intcounter2][0:6]:
            Cross_Refference_No = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Cross Refference Number"] = Cross_Refference_No

        elif "REF*D3" in lines_collection[intcounter2][0:6]:
            Pharmacy_No = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Pharmacy Number"] = Pharmacy_No

        elif "REF*DX" in lines_collection[intcounter2][0:6]:
            Department_No = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Department Number"] = Department_No

        elif "REF*P5" in lines_collection[intcounter2][0:6]:
            Positon_Code = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Positon Code"] = Positon_Code

        elif "REF*Q4" in lines_collection[intcounter2][0:6]:
            Prior_Identification_No = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Prior Identification Number"] = Prior_Identification_No

        elif "REF*QQ" in lines_collection[intcounter2][0:6]:
            Unit_No = lines_collection[intcounter2].split(
                    "*")[2].replace('~', '')
            transaction_data_list[f"{member_type} Unit Number"] = Unit_No
        
        elif "DTP*301" in lines_collection[intcounter2][0:7]:
            Qe_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Qe_Date, "%Y%m%d")
            Qe_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Employment QE Date"] = Qe_Date
        elif "DTP*336" in lines_collection[intcounter2][0:7]:
            Hire_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Hire_Date, "%Y%m%d")
            Hiring_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Hiring Date"] = Hiring_Date


        elif "DTP*337" in lines_collection[intcounter2][0:7]:
            Employment_End_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Employment_End_Date, "%Y%m%d")
            Employee_End = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Employment End Date"] = Employee_End

        elif "DTP*383" in lines_collection[intcounter2][0:7]:
            Adjusted_Service_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Adjusted_Service_Date, "%Y%m%d")
            Adjust_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Adjusted Service Date"] = Adjust_Date

        elif "DTP*338*" in lines_collection[intcounter2][0:8]:
            Medicare_Start_Date = lines_collection[intcounter2].split("*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_Start_Date, "%Y%m%d")
            Start_Date = original_date.strftime("%m-%d-%Y")
            
            medicare_start_dates.append(Start_Date)
            for i, date in enumerate(medicare_start_dates, start=1):
                transaction_data_list[f"{member_type} Medicare Start Date{i}"] = date

        elif "DTP*339" in lines_collection[intcounter2][0:7]:
            Medicare_End_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_End_Date, "%Y%m%d")
            End_Date = original_date.strftime("%m-%d-%Y")
           
            medicare_end_dates.append(End_Date)
            for i, date in enumerate(medicare_end_dates, start=1):
                transaction_data_list[f"{member_type} Medicare End Date{i}"] = date
        
        
        elif "DTP*050" in lines_collection[intcounter2][0:7]:
            Medicare_received_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_received_Date, "%Y%m%d")
            received_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Medicare Received Date"] = received_Date
        
        elif "DTP*286" in lines_collection[intcounter2][0:7]:
            Medicare_retirement_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_retirement_Date, "%Y%m%d")
            retirement_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Retirement Date"] = retirement_Date
        
        elif "DTP*300" in lines_collection[intcounter2][0:7]:
            Medicare_enrollment_signature_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_enrollment_signature_Date, "%Y%m%d")
            enrollment_signature_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Enrollment Signature Date"] = enrollment_signature_Date
        
        elif "DTP*303" in lines_collection[intcounter2][0:7]:
            Medicare_maintenance_effective_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_maintenance_effective_Date, "%Y%m%d")
            maintenance_effective_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Maintenance Effective Date"] = maintenance_effective_Date

        elif "DTP*350" in lines_collection[intcounter2][0:7]:
            Medicare_education_begin_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_education_begin_Date, "%Y%m%d")
            education_begin_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Education Begin Date"] = education_begin_Date
        
        elif "DTP*351" in lines_collection[intcounter2][0:7]:
            Medicare_education_end_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_education_end_Date, "%Y%m%d")
            education_end_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Education End Date"] = education_end_Date
        
        elif "DTP*356" in lines_collection[intcounter2][0:7]:
            Medicare_eligibility_begin_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_eligibility_begin_Date, "%Y%m%d")
            eligibility_begin_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Eligibility Begin Date"] = eligibility_begin_Date
        
        elif "DTP*357" in lines_collection[intcounter2][0:7]:
            Medicare_eligibility_end_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_eligibility_end_Date, "%Y%m%d")
            eligibility_end_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Eligibility End Date"] = eligibility_end_Date
        
        elif "DTP*385" in lines_collection[intcounter2][0:7]:
            Medicare_credited_service_begin_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_credited_service_begin_Date, "%Y%m%d")
            credited_service_begin_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Credited Service Begin Date"] = credited_service_begin_Date
        
        elif "DTP*386" in lines_collection[intcounter2][0:7]:
            Medicare_credited_service_end_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_credited_service_end_Date, "%Y%m%d")
            credited_service_end_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Credited Service End Date"] = credited_service_end_Date
        
        elif "DTP*393" in lines_collection[intcounter2][0:7]:
            Medicare_plan_participation_suspension_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_plan_participation_suspension_Date, "%Y%m%d")
            plan_participation_suspension_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Plan Participation Suspension Date"] = plan_participation_suspension_Date
        elif "DTP*394" in lines_collection[intcounter2][0:7]:
            Medicare_rehire_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(Medicare_rehire_Date, "%Y%m%d")
            rehire_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Rehire Date"] = rehire_Date
        
        elif "DTP*473" in lines_collection[intcounter2][0:7]:
            medicare_medicaid_begin_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(medicare_medicaid_begin_Date, "%Y%m%d")
            medicaid_begin_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Medicaid Begin Date"] = medicaid_begin_Date
        elif "DTP*474" in lines_collection[intcounter2][0:7]:
            medicare_medicaid_end_Date = lines_collection[intcounter2].split(
                "*")[3].replace('~', '')
            original_date = datetime.strptime(medicare_medicaid_end_Date, "%Y%m%d")
            medicaid_end_Date = original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Medicaid End Date"] = medicaid_end_Date

        elif lines_collection[intcounter2].startswith("PER*IP"):
            Contact_Details1 = lines_collection[intcounter2].replace('~', '').split("*")
            if len(Contact_Details1) > 3:
                transaction_data_list[f"{member_type} Contact1"] = Contact_Details1[3] + ":" + Contact_Details1[4]
            if len(Contact_Details1) > 5:
                transaction_data_list[f"{member_type} Contact2"] = Contact_Details1[5] + ":" + Contact_Details1[6]
            if len(Contact_Details1) > 7:
                transaction_data_list[f"{member_type} Contact3"] = Contact_Details1[7] + ":" + Contact_Details1[8]

        elif "N3*" in lines_collection[intcounter2][0:3]:
            Address1 = lines_collection[intcounter2].replace(
                    '~', '').split("*")
            if len(Address1)==2:
                address_positopn = (Address1[1])
            else:
                address_positopn = (Address1[1]+ "_"+ Address1[2])

        elif "N4*" in lines_collection[intcounter2][0:3]:
            address_parts = lines_collection[intcounter2].replace('~', '').split("*")
            city = address_parts[1]
            state = address_parts[2]
            zip_code = address_parts[3]
            transaction_data_list[f"{member_type} Address"] = address_positopn + "," +city+"/"+state+"/"+zip_code
            
            if len(address_parts)==5:
                country_code = address_parts[4]

                transaction_data_list[f"{member_type} Address"] = address_positopn + "," +city+"/"+state+"/"+zip_code+"/"+country_code

        
        elif "DMG" in lines_collection[intcounter2][0:3]:
            line_elements = lines_collection[intcounter2].split("*")
            if len(line_elements) >= 5:  
                Gender = line_elements[3].replace('~', '')
                Medicare_DOB = line_elements[2].replace('~', '')
                Medicare_merital_status = line_elements[4].replace('~', '')

                transaction_data_list[f"{member_type} Gender"] = Gender
                transaction_data_list[f"{member_type} Merital Status"] = Medicare_merital_status

                original_date = datetime.strptime(Medicare_DOB, "%Y%m%d")
                Date_Of_Birth = original_date.strftime("%m-%d-%Y")
                transaction_data_list[f"{member_type} DOB"] = Date_Of_Birth
            
            elif len(line_elements) >= 4: 
                Gender = line_elements[3].replace('~', '')
                Medicare_DOB = line_elements[2].replace('~', '')
                
                transaction_data_list[f"{member_type} Gender"] = Gender
                
                original_date = datetime.strptime(Medicare_DOB, "%Y%m%d")
                Date_Of_Birth = original_date.strftime("%m-%d-%Y")
                transaction_data_list[f"{member_type} DOB"] = Date_Of_Birth
            break
          
        if "NM1*IL" in lines_collection[intcounter2][0:6]:
            transaction_data_list[f"{member_type} Changed?(Yes/No)"] = "IL- No"
            member_details = lines_collection[intcounter2].replace(
                    '~', '').split("*")

            if len(member_details) >= 10:
                transaction_data_list[f"{member_type} Id Code Quatifier"] = member_details[8]
                transaction_data_list[f"{member_type} SSN Number"] = member_details[9]
                transaction_data_list[f"{member_type} Prefix Name"] = member_details[6]
                transaction_data_list[f"{member_type} First Name"] = member_details[4]
                transaction_data_list[f"{member_type} Middle Name"] = member_details[5]
                transaction_data_list[f"{member_type} Last Name"] = member_details[3]
                transaction_data_list[f"{member_type} Suffix Name"] = member_details[7]

            if len(member_details) >= 9:
                transaction_data_list[f"{member_type} Id Code Quatifier"] = member_details[8]
                transaction_data_list[f"{member_type} Prefix Name"] = member_details[6]
                transaction_data_list[f"{member_type} First Name"] = member_details[4]
                transaction_data_list[f"{member_type} Middle Name"] = member_details[5]
                transaction_data_list[f"{member_type} Last Name"] = member_details[3]
                transaction_data_list[f"{member_type} Suffix Name"] = member_details[7]
            elif len(member_details) >= 8:

                transaction_data_list[f"{member_type} Prefix Name"] = member_details[6]
                transaction_data_list[f"{member_type} First Name"] = member_details[4]
                transaction_data_list[f"{member_type} Middle Name"] = member_details[5]
                transaction_data_list[f"{member_type} Last Name"] = member_details[3]
                transaction_data_list[f"{member_type} Suffix Name"] = member_details[7]

            elif len(member_details) >= 7:
                transaction_data_list[f"{member_type} Prefix Name"] = member_details[6]
                transaction_data_list[f"{member_type} First Name"] = member_details[4]
                transaction_data_list[f"{member_type} Middle Name"] = member_details[5]
                transaction_data_list[f"{member_type} Last Name"] = member_details[3]

            elif len(member_details) >= 6:
                transaction_data_list[f"{member_type} First Name"] = member_details[4]
                transaction_data_list[f"{member_type} Middle Name"] = member_details[5]
                transaction_data_list[f"{member_type} Last Name"] = member_details[3]

            elif len(member_details) >= 5:
                transaction_data_list[f"{member_type} First Name"] = member_details[4]
                transaction_data_list[f"{member_type} Last Name"] = member_details[3]

            elif len(member_details) >= 4:
                transaction_data_list[f"{member_type} First Name"] = member_details[4]   
                             
        elif "NM1*74" in lines_collection[intcounter2][0:6]:
            transaction_data_list[f"{member_type} Changed?(Yes/No)"] = "74- Yes"
            member_details1 = lines_collection[intcounter2].replace(
                    '~', '').split("*")

            if len(member_details1) == 10:
                transaction_data_list[f"{member_type} SSN Number"] = member_details1[9]
                transaction_data_list[f"{member_type} Id Code Quatifier"] = member_details1[8]
                transaction_data_list[f"{member_type} Prefix Name"] = member_details1[6]
                transaction_data_list[f"{member_type} First Name"] = member_details1[4]
                transaction_data_list[f"{member_type} Middle Name"] = member_details1[5]
                transaction_data_list[f"{member_type} Last Name"] = member_details1[3]
                transaction_data_list[f"{member_type} Suffix Name"] = member_details1[7]
            
            elif len(member_details1) == 9:
                transaction_data_list[f"{member_type} Id Code Quatifier"] = member_details1[8]
                transaction_data_list[f"{member_type} Prefix Name"] = member_details1[6]
                transaction_data_list[f"{member_type} First Name"] = member_details1[4]
                transaction_data_list[f"{member_type} Middle Name"] = member_details1[5]
                transaction_data_list[f"{member_type} Last Name"] = member_details1[3]
                transaction_data_list[f"{member_type} Suffix Name"] = member_details1[7]

            elif len(member_details1) == 8:
                transaction_data_list[f"{member_type} Prefix Name"] = member_details1[6]
                transaction_data_list[f"{member_type} First Name"] = member_details1[4]
                transaction_data_list[f"{member_type} Middle Name"] = member_details1[5]
                transaction_data_list[f"{member_type} Last Name"] = member_details1[3]
                transaction_data_list[f"{member_type} Suffix Name"] = member_details1[7]

            elif len(member_details1) == 7:
                transaction_data_list[f"{member_type} Prefix Name"] = member_details1[6]
                transaction_data_list[f"{member_type} First Name"] = member_details1[4]
                transaction_data_list[f"{member_type} Middle Name"] = member_details1[5]
                transaction_data_list[f"{member_type} Last Name"] = member_details1[3]

            elif len(member_details1) == 6:
                transaction_data_list[f"{member_type} First Name"] = member_details1[4]
                transaction_data_list[f"{member_type} Middle Name"] = member_details1[5]
                transaction_data_list[f"{member_type} Last Name"] = member_details1[3]

            elif len(member_details1) == 5:
                transaction_data_list[f"{member_type} First Name"] = member_details1[4]
                transaction_data_list[f"{member_type} Last Name"] = member_details1[3]

            elif len(member_details1) == 4:
                transaction_data_list[f"{member_type} First Name"] = member_details1[4]
            
            
        elif "INS*" in lines_collection[intcounter2][0:4]  or "SE*" in lines_collection[intcounter2][0:3]:
            break


        

    for intcounter2 in range(intcounter + 1, len(lines_collection)):
        if "NM1*70" in lines_collection[intcounter2][0:6]:
                
            Old_member_name = lines_collection[intcounter2].replace('~', '').split("*")

            if len(Old_member_name) == 10:
                transaction_data_list[f"{member_type} Old SSN Number"] = Old_member_name[9]
                transaction_data_list[f"{member_type} Old Id Code Quatifier"] = Old_member_name[8]
                transaction_data_list[f"{member_type} Old Prefix Name"] = Old_member_name[6]
                transaction_data_list[f"{member_type} Old First Name"] = Old_member_name[4]
                transaction_data_list[f"{member_type} Old Middle Name"] = Old_member_name[5]
                transaction_data_list[f"{member_type} Old Last Name"] = Old_member_name[3]
                transaction_data_list[f"{member_type} Old Suffix Name"] = Old_member_name[7]
                            
            elif len(Old_member_name) == 9:
                transaction_data_list[f"{member_type} Old Id Code Quatifier"] = Old_member_name[8]
                transaction_data_list[f"{member_type} Old Prefix Name"] = Old_member_name[6]
                transaction_data_list[f"{member_type} Old First Name"] = Old_member_name[4]
                transaction_data_list[f"{member_type} Old Middle Name"] = Old_member_name[5]
                transaction_data_list[f"{member_type} Old Last Name"] = Old_member_name[3]
                transaction_data_list[f"{member_type} Old Suffix Name"] = Old_member_name[7]

            elif len(Old_member_name) == 8:
                transaction_data_list[f"{member_type} Old Prefix Name"] = Old_member_name[6]
                transaction_data_list[f"{member_type} Old First Name"] = Old_member_name[4]
                transaction_data_list[f"{member_type} Old Middle Name"] = Old_member_name[5]
                transaction_data_list[f"{member_type} Old Last Name"] = Old_member_name[3]
                transaction_data_list[f"{member_type} Old Suffix Name"] = Old_member_name[7]

            elif len(Old_member_name) == 7:
                transaction_data_list[f"{member_type} Old Prefix Name"] = Old_member_name[6]
                transaction_data_list[f"{member_type} Old First Name"] = Old_member_name[4]
                transaction_data_list[f"{member_type} Old Middle Name"] = Old_member_name[5]
                transaction_data_list[f"{member_type} Old Last Name"] = Old_member_name[3]

            elif len(Old_member_name) == 6:
                transaction_data_list[f"{member_type} Old First Name"] = Old_member_name[4]
                transaction_data_list[f"{member_type} Old Middle Name"] = Old_member_name[5]
                transaction_data_list[f"{member_type} Old Last Name"] = Old_member_name[3]

            elif len(Old_member_name) == 5:
                transaction_data_list[f"{member_type} Old First Name"] = Old_member_name[4]
                transaction_data_list[f"{member_type} Old Last Name"] = Old_member_name[3]

            elif len(Old_member_name) == 4:
                        transaction_data_list[f"{member_type} Old First Name"] = Old_member_name[4]
            for intcounter3 in range(intcounter2 + 1, len(lines_collection)):
                if "DMG*" in lines_collection[intcounter3][0:4]:
                    member_dmg_details = lines_collection[intcounter3].split("*")
                                        
                    if len(member_dmg_details) >= 5:  
                        member_old_Gender = member_dmg_details[3].replace('~', '')
                        member_old_DOB = member_dmg_details[2].replace('~', '')
                        member_old_merital_status = member_dmg_details[4].replace('~', '')
                                            
                        transaction_data_list[f"{member_type} Old Gender"] = member_old_Gender
                        transaction_data_list[f"{member_type} Old Merital Status"] = member_old_merital_status
                                                
                        original_dob_date = datetime.strptime(member_old_DOB, "%Y%m%d")
                        member_old_Date_Of_Birth = original_dob_date.strftime("%m-%d-%Y")
                        transaction_data_list[f"{member_type} Old DOB"] = member_old_Date_Of_Birth
                                
                    elif len(member_dmg_details) >= 4: 
                        member_old_Gender = member_dmg_details[3].replace('~', '')
                        member_old_DOB = member_dmg_details[2].replace('~', '')
                                                
                        transaction_data_list[f"{member_type} Old Gender"] = member_old_Gender
                                                
                        original_dob_date = datetime.strptime(member_old_DOB, "%Y%m%d")
                        member_old_Date_Of_Birth = original_dob_date.strftime("%m-%d-%Y")
                        transaction_data_list[f"{member_type} Old DOB"] = member_old_Date_Of_Birth
                elif "INS*" in lines_collection[intcounter3][0:4] or "SE*" in lines_collection[intcounter3][0:3]:
                    break
        elif "INS*" in lines_collection[intcounter2][0:4]  or "SE*" in lines_collection[intcounter2][0:3]:
            break
        

    for intcounter2 in range(intcounter + 1, len(lines_collection)):
        if "NM1*31*" in lines_collection[intcounter2][0:7]:
            for intcounter3 in range(intcounter2 + 1, len(lines_collection)):
                if "N3" in lines_collection[intcounter3][0:2]:
                    Old_Address1 = lines_collection[intcounter3].replace('~', '').split(
                                "*")
                    if len(Old_Address1)==2:
                        old_address_positopn = (Old_Address1[1])
                    else:
                        old_address_positopn = (Old_Address1[1]+ "_"+ Old_Address1[2])

                elif "N4*" in lines_collection[intcounter3][0:3]:
                    old_address_parts = lines_collection[intcounter3].replace('~', '').split("*")

                    old_city = old_address_parts[1]
                    old_state = old_address_parts[2]
                    old_zip_code = old_address_parts[3]
                    transaction_data_list[f"{member_type} Old Address"] = old_address_positopn + "," +old_city+"/"+old_state+"/"+old_zip_code
                    
                    if len(old_address_parts)==5:
                        old_country_code = old_address_parts[4]

                        transaction_data_list[f"{member_type} Old Address"] = old_address_positopn + "," +old_city+"/"+old_state+"/"+old_zip_code+"/"+old_country_code
                   
                
                elif "INS*" in lines_collection[intcounter3][0:4] or "SE*" in lines_collection[intcounter3][0:3]:
                    break  
        elif "INS*" in lines_collection[intcounter2][0:4] or "SE*" in lines_collection[intcounter2][0:3]:
            break          
                        
    for intcounter2 in range(intcounter + 1, len(lines_collection)):
        if "NM1*36*" in lines_collection[intcounter2][0:7]:
            employer_details = lines_collection[intcounter2].replace('~', '').split(
                                        "*")
            employer_entity_id_code = employer_details[1]
            employer_entity_type_qualifier = employer_details[2]

            transaction_data_list["Employer Entity Id Code"] = employer_entity_id_code
            transaction_data_list["Employer Entity Type Qualifier "] = employer_entity_type_qualifier
            if len(employer_details) == 5:
                transaction_data_list["Employer First Name"] = employer_details[4]
                transaction_data_list["Employer Last Name"] = employer_details[3]
            elif len(employer_details) == 6:
                transaction_data_list["Employer First Name"] = employer_details[4]
                transaction_data_list["Employer Middle Name"] = employer_details[5]
                transaction_data_list["Employer Last Name"] = employer_details[3]
            elif len(employer_details) == 7:
                transaction_data_list["Employer Prefix Name"] = employer_details[6]
                transaction_data_list["Employer First Name"] = employer_details[4]
                transaction_data_list["Employer Middle Name"] = employer_details[5]
                transaction_data_list["Employer Last Name"] = employer_details[3]
            elif len(employer_details) == 8:
                transaction_data_list["Employer Prefix Name"] = employer_details[6]
                transaction_data_list["Employer First Name"] = employer_details[4]
                transaction_data_list["Employer Middle Name"] = employer_details[5]
                transaction_data_list["Employer Last Name"] = employer_details[3]
                transaction_data_list["Employer Suffix Name"] = employer_details[7]
            elif len(employer_details) == 9:
                transaction_data_list["Employer Id Code Quatifier"] = employer_details[8]
                transaction_data_list["Employer Prefix Name"] = employer_details[6]
                transaction_data_list["Employer First Name"] = employer_details[4]
                transaction_data_list["Employer Middle Name"] = employer_details[5]
                transaction_data_list["Employer Last Name"] = employer_details[3]
                transaction_data_list["Employer Suffix Name"] = employer_details[7]
            elif len(employer_details) == 10:
                transaction_data_list["Employer SSN Number"] = employer_details[9]
                transaction_data_list["Employer Id Code Quatifier"] = employer_details[8]
                transaction_data_list["Employer Prefix Name"] = employer_details[6]
                transaction_data_list["Employer First Name"] = employer_details[4]
                transaction_data_list["Employer Middle Name"] = employer_details[5]
                transaction_data_list["Employer Last Name"] = employer_details[3]
                transaction_data_list["Employer Suffix Name"] = employer_details[7]
            for intcounter3 in range(intcounter2 + 1, len(lines_collection)):    
                if "PER*IP" in lines_collection[intcounter3][0:6]:
                    employer_contact_Details1 = lines_collection[intcounter3].replace('~', '').split("*")
                    if len(employer_contact_Details1) > 3:
                        transaction_data_list["Employer Contact1"] = employer_contact_Details1[3] + "-" + employer_contact_Details1[4]
                    if len(employer_contact_Details1) > 5:
                        transaction_data_list["Employer Contact2"] = employer_contact_Details1[5] + "-" + employer_contact_Details1[6]
                    if len(employer_contact_Details1) > 7:
                        transaction_data_list["Employer Contact3"] = employer_contact_Details1[7] + "-" + employer_contact_Details1[8]

                elif "N3*" in lines_collection[intcounter3][0:3]:
                    Employer_Address1 = lines_collection[intcounter3].replace('~', '').split("*")
                    if len(Employer_Address1)==2:
                        employer_address_positopn = (Employer_Address1[1])
                    else:
                        employer_address_positopn = (Employer_Address1[1]+ "_"+ Employer_Address1[2])

                elif "N4*" in lines_collection[intcounter3][0:3]:
                    employer_address_parts = lines_collection[intcounter3].split("*")[1:4]
                    Employer_Address2 = " ".join(employer_address_parts).replace('~', '')
                    transaction_data_list["Employer Address"] = employer_address_positopn + "," + Employer_Address2
                elif "INS*" in lines_collection[intcounter3][0:4] or "SE*" in lines_collection[intcounter3][0:3]:
                    break 
    for intcounter2 in range(intcounter + 1, len(lines_collection)):
        if "NM1*M8*" in lines_collection[intcounter2][0:7]:
            school_details = lines_collection[intcounter2].replace('~', '').split(
                                        "*")
        
            transaction_data_list["School Entity Id Code"] = school_details[1]
            transaction_data_list["School Entity Type Qualifier "] = school_details[2]
            transaction_data_list["School Name"] = school_details[3]
            for intcounter3 in range(intcounter2 + 1, len(lines_collection)):
                if "PER*IP" in lines_collection[intcounter3][0:6]:
                    school_contact_Details1 = lines_collection[intcounter3].replace('~', '').split("*")
                    if len(school_contact_Details1) > 3:
                        transaction_data_list["School Contact1"] = school_contact_Details1[3] + "-" + school_contact_Details1[4]
                    elif len(school_contact_Details1) > 5:
                        transaction_data_list["School Contact2"] = school_contact_Details1[5] + "-" + school_contact_Details1[6]
                    elif len(school_contact_Details1) > 7:
                        transaction_data_list["School Contact3"] = school_contact_Details1[7] + "-" + school_contact_Details1[8]

                elif "N3*" in lines_collection[intcounter3][0:3]:
                    School_Address1 = lines_collection[intcounter3].replace('~', '').split("*")
                    if len(School_Address1)==2:
                        school_address_positopn = (School_Address1[1])
                    else:
                        school_address_positopn = (School_Address1[1]+ "_"+ School_Address1[2])

                elif "N4*" in lines_collection[intcounter3][0:3]:
                    school_address_parts = lines_collection[intcounter3].split("*")[1:4]
                    School_Address2 = " ".join(school_address_parts).replace('~', '')
                    transaction_data_list["School Address"] = school_address_positopn + "," + School_Address2
                elif "INS*" in lines_collection[intcounter3][0:4] or "SE*" in lines_collection[intcounter3][0:3]:
                    break     
    
    for intcounter2 in range(intcounter + 1, len(lines_collection)):
        if "NM1*S3*" in lines_collection[intcounter2][0:7]:
            custodial_details = lines_collection[intcounter2].replace('~', '').split(
                                        "*")
            transaction_data_list["Custodial Entity Id Code"] = custodial_details[1]
            transaction_data_list["Custodial Entity Type Qualifier "] = custodial_details[2]
            if len(custodial_details) == 5:
                transaction_data_list["Custodial First Name"] = custodial_details[4]
                transaction_data_list["Custodial Last Name"] = custodial_details[3]
            elif len(custodial_details) == 6:
                transaction_data_list["Custodial First Name"] = custodial_details[4]
                transaction_data_list["Custodial Middle Name"] = custodial_details[5]
                transaction_data_list["Custodial Last Name"] = custodial_details[3]
            elif len(custodial_details) == 7:
                transaction_data_list["Custodial Prefix Name"] = custodial_details[6]
                transaction_data_list["Custodial First Name"] = custodial_details[4]
                transaction_data_list["Custodial Middle Name"] = custodial_details[5]
                transaction_data_list["Custodial Last Name"] = custodial_details[3]
            elif len(custodial_details) == 8:
                transaction_data_list["Custodial Prefix Name"] = custodial_details[6]
                transaction_data_list["Custodial First Name"] = custodial_details[4]
                transaction_data_list["Custodial Middle Name"] = custodial_details[5]
                transaction_data_list["Custodial Last Name"] = custodial_details[3]
                transaction_data_list["Custodial Suffix Name"] = custodial_details[7]
            elif len(custodial_details) == 9:
                transaction_data_list["Custodial Id Code Quatifier"] = custodial_details[8]
                transaction_data_list["Custodial Prefix Name"] = custodial_details[6]
                transaction_data_list["Custodial First Name"] = custodial_details[4]
                transaction_data_list["Custodial Middle Name"] = custodial_details[5]
                transaction_data_list["Custodial Last Name"] = custodial_details[3]
                transaction_data_list["Custodial Suffix Name"] = custodial_details[7]
            elif len(custodial_details) == 10:
                transaction_data_list["Custodial SSN Number"] = custodial_details[9]
                transaction_data_list["Custodial Id Code Quatifier"] = custodial_details[8]
                transaction_data_list["Custodial Prefix Name"] = custodial_details[6]
                transaction_data_list["Custodial First Name"] = custodial_details[4]
                transaction_data_list["Custodial Middle Name"] = custodial_details[5]
                transaction_data_list["Custodial Last Name"] = custodial_details[3]
                transaction_data_list["Custodial Suffix Name"] = custodial_details[7]
            for intcounter3 in range(intcounter2 + 1, len(lines_collection)):
                if "PER*IP" in lines_collection[intcounter3][0:6]:
                    custodial_contact_Details1 = lines_collection[intcounter3].replace('~', '').split("*")
                    if len(custodial_contact_Details1) > 3:
                        transaction_data_list["Custodial Contact1"] = custodial_contact_Details1[3] + "-" + custodial_contact_Details1[4]
                    elif len(custodial_contact_Details1) > 5:
                        transaction_data_list["Custodial Contact2"] = custodial_contact_Details1[5] + "-" + custodial_contact_Details1[6]
                    elif len(custodial_contact_Details1) > 7:
                        transaction_data_list["Custodial Contact3"] = custodial_contact_Details1[7] + "-" + custodial_contact_Details1[8]

                elif "N3*" in lines_collection[intcounter3][0:3]:
                    custodial_Address1 = lines_collection[intcounter3].replace('~', '').split("*")
                    if len(custodial_Address1)==2:
                        custodial_address_positopn = (custodial_Address1[1])
                    else:
                        custodial_address_positopn = (custodial_Address1[1]+ "_"+ custodial_Address1[2])

                elif "N4*" in lines_collection[intcounter3][0:3]:
                    custodial_address_parts = lines_collection[intcounter3].split("*")[1:4]
                    custodial_Address2 = " ".join(custodial_address_parts).replace('~', '')
                    transaction_data_list["Custodial Address"] = custodial_address_positopn + "," + custodial_Address2
                elif "INS*" in lines_collection[intcounter3][0:4] or "SE*" in lines_collection[intcounter3][0:3]:
                    break 
   
    for intcounter2 in range(intcounter + 1, len(lines_collection)):
        if "NM1*45*" in lines_collection[intcounter2][0:7]:
            
            drop_location_details = lines_collection[intcounter2].replace('~', '').split(
                                        "*")

            transaction_data_list["Entity Id Code (Drop of Location)"] = drop_location_details[1]
            transaction_data_list["Entity Type Qualifier (Drop of Location)"] =drop_location_details[2] 
            if len(drop_location_details) == 5:
                transaction_data_list["First Name (Drop of Location)"] = employer_details[4]
                transaction_data_list["Last Name (Drop of Location)"] = employer_details[3] 
            for intcounter3 in range(intcounter2 + 1, len(lines_collection)):
                if "N3*" in lines_collection[intcounter3][0:3]:
                    drop_Address1 = lines_collection[intcounter3].replace('~', '').split("*")
                    if len(drop_Address1)==2:
                        drop_address_positopn = (drop_Address1[1])
                    else:
                        drop_address_positopn = (drop_Address1[1]+ "_"+ drop_Address1[2])

                elif "N4*" in lines_collection[intcounter3][0:3]:
                    drop_address_parts = lines_collection[intcounter3].split("*")[1:4]
                    drop_Address2 = " ".join(drop_address_parts).replace('~', '')
                    transaction_data_list["Drop of Address"] = drop_address_positopn + "," + drop_Address2
                elif "INS*" in lines_collection[intcounter3][0:4] or "SE*" in lines_collection[intcounter3][0:3]:
                    break
                    
    plan_counter = 0
    for intcounter2 in range(intcounter + 1, len(lines_collection)):
        if "HD*" in lines_collection[intcounter2][0:3]:
              
            plan_counter += 1
            Employee_Plan_Description = lines_collection[intcounter2].replace('~', '').split("*")
            transaction_data_list[f"{member_type} Insurance Line Code-{plan_counter}"] = Employee_Plan_Description[3]
            transaction_data_list[f"{member_type} Plan Description-{plan_counter}"] = Employee_Plan_Description[4]
            transaction_data_list[f"{member_type} Coverage Lavel Code-{plan_counter}"] = Employee_Plan_Description[5]


            Emp_Plan_Description = (Employee_Plan_Description[1])
            if Emp_Plan_Description in Employee_Description_of_plan:
                transaction_data_list[f"{member_type} Medicare Plan Maintenance-{plan_counter}"] = Employee_Description_of_plan[Emp_Plan_Description]

        elif "DTP*348*" in lines_collection[intcounter2][0:8]:
            Benefit_Begin = lines_collection[intcounter2].split("*")[3].replace('~', '')
            Benefit_Begin_original_date = datetime.strptime(Benefit_Begin, "%Y%m%d")
            Benefit_Begin_Date = Benefit_Begin_original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Benefit Begin-{plan_counter}"] = Benefit_Begin_Date
        elif "DTP*349*" in lines_collection[intcounter2][0:8]:
            Benefit_End = lines_collection[intcounter2].split("*")[3].replace('~', '')
            Benefit_End_original_date = datetime.strptime(Benefit_End, "%Y%m%d")
            Benefit_End_Date = Benefit_End_original_date.strftime("%m-%d-%Y")
            transaction_data_list[f"{member_type} Benefit End-{plan_counter}"] = Benefit_End_Date
            
        elif "REF*ZZ*" in lines_collection[intcounter2][0:7]:
            Smoker_Details = lines_collection[intcounter2].replace('~', '').split("*")
            Smoker = str(Smoker_Details[2])
            if Smoker == 'Y':
                transaction_data_list[f"{member_type} Non Smoker Discount-{plan_counter}"] = "YES"
            elif Smoker == 'N':
                transaction_data_list[f"{member_type} Non Smoker Discount-{plan_counter}"] = "NO"
            
        if "INS*" in lines_collection[intcounter2][0:4] or "LS*" in lines_collection[intcounter2][0:3]:
            break
                
    Status_Counter = 0
    for intcounter2 in range(intcounter + 1, len(lines_collection)):
        if "LX*" in lines_collection[intcounter2][0:3]:
            Status_Counter += 1

        elif "N1*75*" in lines_collection[intcounter2][0:6]:
            Employee_Status_Details = lines_collection[intcounter2].replace('~', '').split("*")[2]
            transaction_data_list[f"{member_type} Status Details-{Status_Counter}"] = Employee_Status_Details
                
        elif "REF*ZZ" in lines_collection[intcounter2][0:6]:
            Employee_Status = lines_collection[intcounter2].replace('~', '').split("*")[2]
            transaction_data_list[f"{member_type} Employment Status-{Status_Counter}"] = Employee_Status
               
        elif "DTP*007" in lines_collection[intcounter2][0:7]:
            Employment_Status = lines_collection[intcounter2].replace('~', '').split("*")
            transaction_data_list[f"{member_type} Employment Status Date Format-{Status_Counter}"] = Employment_Status[2]
            if len(Employment_Status) == 4:
                date_range = Employment_Status[3].split('-')
                if len(date_range) == 1:
                    start_date_str = date_range[0]
                    start_date = datetime.strptime(start_date_str, "%Y%m%d")
                    Employee_Employment_Status_Start_Date = start_date.strftime("%m.%d.%Y")
                    transaction_data_list[f"{member_type} Employment Status Start/End Date-{Status_Counter}"] = Employee_Employment_Status_Start_Date
               
                elif len(date_range) == 2:
                    start_date_str, end_date_str = date_range
                    start_date = datetime.strptime(start_date_str, "%Y%m%d")
                    end_date = datetime.strptime(end_date_str, "%Y%m%d")
                    Employee_Employment_Status_Start_Date = start_date.strftime("%m.%d.%Y")
                    Employee_Employment_Status_End_Date = end_date.strftime("%m.%d.%Y")
                    transaction_data_list[f"{member_type} Employment Status Start/End Date-{Status_Counter}"] = (Employee_Employment_Status_Start_Date+ " - " +Employee_Employment_Status_End_Date)
        
        if "INS*" in lines_collection[intcounter2][0:4]:
            break
        
def process_file(file_path):
    lines_collection = []
    transaction_data_list = {}
    result_collection = []
    Dependent_details_arr = []

    with open(file_path, 'r') as read_file:
        for line in read_file:
            lines_collection.append(line.strip())

    for intcounter in range(len(lines_collection)):
        if "ST" in lines_collection[intcounter][0:2]:
            if not transaction_data_list:
               
                transaction_id = lines_collection[intcounter].split("*")[2].replace('~', '')
                transaction_data_list = {
                    "Transaction Id": transaction_id,
                }
                  
        elif "QTY*DT" in lines_collection[intcounter][0:6]:
            total_dependent =  lines_collection[intcounter].split("*")[2].replace('~', '')
            transaction_data_list["Total Of Dependent"] = total_dependent
        
        elif "QTY*ET" in lines_collection[intcounter][0:6]:
            total_eamployee =  lines_collection[intcounter].split("*")[2].replace('~', '')
            transaction_data_list["Total Of Employee"] = total_eamployee

        elif "QTY*TO" in lines_collection[intcounter][0:6]:
            total_dependent_and_employee =  lines_collection[intcounter].split("*")[2].replace('~', '')
            transaction_data_list["Total Of Dep & Emp"] = total_dependent_and_employee

        if "N1*P5" in lines_collection[intcounter][0:5]:
            Unit_name = lines_collection[intcounter].split("*")[2]
            Unit_id_code_qualifier = lines_collection[intcounter].split("*")[3]
            Unit_id = lines_collection[intcounter].split(
                "*")[4].replace('~', '')
            transaction_data_list["Unit Name"] = Unit_name
            transaction_data_list["Unit Id"] = Unit_id
            transaction_data_list["Unit Id Code Qualifier"] = Unit_id_code_qualifier
        
        if "N1*IN" in lines_collection[intcounter][0:5]:
            Insurer_Name = lines_collection[intcounter].split("*")[2]
            Insurer_Id_Code_Qualifier = lines_collection[intcounter].split("*")[3]
            Insurer_Id = lines_collection[intcounter].split("*")[4].replace('~', '')
            transaction_data_list["Insurer Name"] = Insurer_Name
            transaction_data_list["Insurer Id Code Qualifier"] = Insurer_Id_Code_Qualifier
            transaction_data_list["Insurer Id"] = Insurer_Id    

        if "NM1*E1" in lines_collection[intcounter][0:6]:
            process_person_details(
                "Responsible", lines_collection, intcounter, transaction_data_list)
        elif "NM1*EXS" in lines_collection[intcounter][0:6]:
            process_person_details("Ex Spouse", lines_collection[intcounter], transaction_data_list)
        elif "NM1*GD" in lines_collection[intcounter][0:6]:
            process_person_details("Guardian", lines_collection, intcounter, transaction_data_list)

        elif "NM1*6Y" in lines_collection[intcounter][0:6]:
            process_person_details(
                "Case-Manager",lines_collection, intcounter, transaction_data_list)

        elif "NM1*9K" in lines_collection[intcounter][0:6]:
            process_person_details("Key-Person", lines_collection, intcounter, transaction_data_list)

        elif "NM1*S1" in lines_collection[intcounter][0:6]:
            process_person_details("Parent", lines_collection, intcounter, transaction_data_list)

        elif "NM1*EI" in lines_collection[intcounter][0:6]:
            process_person_details("Executor", lines_collection, intcounter, transaction_data_list)

        elif "NM1*QD" in lines_collection[intcounter][0:6]:
            process_person_details(
                "Responsibel", lines_collection, intcounter, transaction_data_list)

        elif "NM1*GB" in lines_collection[intcounter][0:6]:
            process_person_details(
                "Other Insured", lines_collection, intcounter, transaction_data_list)

        elif "NM1*TZ" in lines_collection[intcounter][0:6]:
            process_person_details(
                "Significant", lines_collection, intcounter, transaction_data_list)

        elif "NM1*LR" in lines_collection[intcounter][0:6]:
            process_person_details(
                "Lagal Representative", lines_collection, intcounter, transaction_data_list)

        elif "NM1*J6" in lines_collection[intcounter][0:6]:
            process_person_details(
                "Attorney", lines_collection, intcounter, transaction_data_list)

        elif "DSB*" in lines_collection[intcounter][0:4]:
            Disability_Code_Value = lines_collection[intcounter].replace(
                '~', '').split("*")[8]
            transaction_data_list["Disability Code Value"] = Disability_Code_Value

            Serv_Id = lines_collection[intcounter].split("*")
            ServId = str(Serv_Id[7])

            if ServId == 'DX':
                transaction_data_list[
                    "Service Id Qualifier"] = "DX- International Classification of Diseases, 9th Revision, Clinical Modification (ICD-9-CM) - Diagnosis."
            elif ServId == 'ZZ':
                transaction_data_list[
                    "Service Id Qualifier"] = "ZZ- To be Used for the International Classification of Diseases, 10th Revision, Clinical Modification (ICD-10-CM) - Diagnosis."

        elif "DTP*360" in lines_collection[intcounter][0:7]:
            Disability_Eligibility_Strat_date = lines_collection[intcounter].replace(
                '~', '').split("*")[3]
            transaction_data_list["Initial Disability Period Start Date"] = Disability_Eligibility_Strat_date
        elif "DTP*361" in lines_collection[intcounter][0:7]:
            Disability_Eligibility_End_date = lines_collection[intcounter].replace(
                '~', '').split("*")[3]
            transaction_data_list["Initial Disability Period End Date"] = Disability_Eligibility_End_date

        elif "INS" in lines_collection[intcounter][0:3]:
            medicare_details = lines_collection[intcounter].replace(
                '~', '').split("*")
            medicare = medicare_details[2]

            if medicare == '18':
                transaction_data_list["Employee Employment Status Code"] = medicare_details[8]
                
                process_medicare_details(
                    lines_collection, intcounter, transaction_data_list, "Employee")

            else:
                Dependent_details = {}
                if "INS*" in lines_collection[intcounter][0:4]:
                    Student_Status_Code = lines_collection[intcounter].split("*")[9]
                    Dependent_details["Student Status Code"] = Student_Status_Code
                  
                process_medicare_details(lines_collection, intcounter, Dependent_details, "Dependent")
                Dependent_details_arr.append(Dependent_details)
                Dependent_details = {}

                             
        elif "SE*" in lines_collection[intcounter][0:3]:
            
            transaction_end = lines_collection[intcounter].replace(
                '~', '').split("*")
            transaction_data_list["Number Of Included Sigment"] = transaction_end[1]
            transaction_data_list["Transaction End"] = transaction_end[2]
            
            for counter, Dependent_details in enumerate(Dependent_details_arr):
                for key, value in Dependent_details.items():
                    transaction_data_list[f"Dependent-{counter+1}-{key}"] = value

            Dependent_details_arr = []
            result_collection.append(transaction_data_list)
            transaction_data_list = {}
    
    return result_collection

result_collection = process_file(
    "C:\\Users\\USER\\Desktop\\ITEDUIM Project\\edi_to_excel\\itedium_changes_20240205170014_prod.txt")
Dependent_details_keys = [
    "Dependent Y/N Condition Code",
    "Dependent Relationship Code",
    "Dependent Changed?(Yes/No)", 
    "Dependent Depend SSN Number",
    "Dependent Sup-Id", 
    "Dependent Personal Id Number",
    'Dependent Mutually Defined',
    "Dependent Health Insurance Claim Number",
    "Dependent Client Reporting Catagory",
    "Dependent Client Number",
    "Dependent Case Number",
    "Dependent Personal Identification Number",
    "Dependent Cross Refference Number",
    "Dependent Pharmacy Number",
    "Dependent Department Number",
    "Dependent Positon Code",
    "Dependent Prior Identification Number",
    "Dependent Unit Number", 
    "Dependent Cobra Event Code", "Dependent Maintenance Type Code",  "Dependent Maintenance Reason", "Dependent Benefit Status", "Dependent Medicare Status Code", "Student Status Code", "Dependent Date Time Period", "Dependent Id Code Quatifier", "Dependent SSN Number", "Dependent Old Id Code Quatifier", "Dependent Old SSN Number",
    "Dependent Prefix Name", "Dependent First Name", "Dependent Middle Name", "Dependent Last Name",
    "Dependent Suffix Name", "Dependent Old Prefix Name", "Dependent Old First Name", "Dependent Old Middle Name",
    "Dependent Old Last Name", "Dependent Old Suffix Name", "Dependent Gender", "Dependent Merital Status", "Dependent DOB", "Dependent Old Gender", "Dependent Old Merital Status", "Dependent Old DOB",
    "Dependent Contact1", "Dependent Contact2", "Dependent Contact3", 
    "Dependent Medicare Plan Maintenance-1",
    "Dependent Insurance Line Code-1",
    "Dependent Plan Description-1",
    "Dependent Coverage Lavel Code-1",
    "Dependent Benefit Begin-1",
    "Dependent Benefit End-1",
    "Dependent Non Smoker Discount-1",

    "Dependent Medicare Plan Maintenance-2",
    "Dependent Insurance Line Code-2",
    "Dependent Plan Description-2",
    "Dependent Coverage Lavel Code-2",
    "Dependent Benefit Begin-2",
    "Dependent Benefit End-2",
    "Dependent Non Smoker Discount-2",

    "Dependent Medicare Plan Maintenance-3",
    "Dependent Insurance Line Code-3",
    "Dependent Plan Description-3",
    "Dependent Coverage Lavel Code-3",
    "Dependent Benefit Begin-3",
    "Dependent Benefit End-3",
    "Dependent Non Smoker Discount-3",

    "Dependent Medicare Plan Maintenance-4",
    "Dependent Insurance Line Code-4",
    "Dependent Plan Description-4",
    "Dependent Coverage Lavel Code-4",
    "Dependent Benefit Begin-4",
    "Dependent Benefit End-4",
    "Dependent Non Smoker Discount-4",
    
    "Dependent Medicare Plan Maintenance-5",
    "Dependent Insurance Line Code-5",
    "Dependent Plan Description-5",
    "Dependent Coverage Lavel Code-5",
    "Dependent Benefit Begin-5",
    "Dependent Benefit End-5",
    "Dependent Non Smoker Discount-5",

    "Dependent Status Details-1",
    "Dependent Employment Status-1",
    "Dependent Employment Status Date Format-1",
    "Dependent Employment Status Start/End Date-1",

    "Dependent Status Details-2",
    "Dependent Employment Status-2",
    "Dependent Employment Status Date Format-2",
    "Dependent Employment Status Start/End Date-2",

    "Dependent Status Details-3",
    "Dependent Employment Status-3",
    "Dependent Employment Status Date Format-3",
    "Dependent Employment Status Start/End Date-3",

    "Dependent Status Details-4",
    "Dependent Employment Status-4",
    "Dependent Employment Status Date Format-4",
    "Dependent Employment Status Start/End Date-4",

    "Dependent Status Details-5",
    "Dependent Employment Status-5",
    "Dependent Employment Status Date Format-5",
    "Dependent Employment Status Start/End Date-5",

    "Dependent Status Details-6",
    "Dependent Employment Status-6",
    "Dependent Employment Status Date Format-6",
    "Dependent Employment Status Start/End Date-6",

    "Dependent Hiring Date",
    "Dependent Employment End Date",
    "Dependent Employment QE Date",
    "Dependent Adjusted Service Date",
    "Dependent Medicare Start Date1",
    "Dependent Medicare Start Date2",
    "Dependent Medicare Start Date3",
    "Dependent Medicare End Date1",
    "Dependent Medicare End Date2",
    "Dependent Medicare End Date3",
    "Dependent Medicare Received Date",
    "Dependent Retirement Date",
    "Dependent Enrollment Signature Date",
    "Dependent Maintenance Effective Date",
    "Dependent Education Begin Date",
    "Dependent Education End Date",
    "Dependent Eligibility Begin Date",
    "Dependent Eligibility End Date",
    "Dependent Credited Service Begin Date",
    "Dependent Credited Service End Date",
    "Dependent Plan Participation Suspension Date",
    "Dependent Rehire Date",
    "Dependent Medicaid Begin Date",
    "Dependent Medicaid End Date",
    "Dependent Address", "Dependent Old Address",
]
Dependent_details_columns = [
    f"Dependent-{i+1}-{key}" for i in range(10) for key in Dependent_details_keys]

df_result = pd.DataFrame(result_collection, columns=[
    "Transaction Id",  "Total Of Employee", "Total Of Dependent", "Total Of Dep & Emp", "Unit Name", "Unit Id Code Qualifier", "Unit Id", "Insurer Name", "Insurer Id Code Qualifier", "Insurer Id", "Employee Y/N Condition Code", "Employee Relationship Code", "Employee Changed?(Yes/No)","Employee Depend SSN Number", "Employee Sup-Id", 
    "Employee Personal Id Number",
    'Employee Mutually Defined',
    "Employee Health Insurance Claim Number",
    "Employee Client Reporting Catagory",
    "Employee Client Number",
    "Employee Case Number",
    "Employee Personal Identification Number",
    "Employee Cross Refference Number",
    "Employee Pharmacy Number",
    "Employee Department Number",
    "Employee Positon Code",
    "Employee Prior Identification Number",
    "Employee Unit Number", 
    "Employee Cobra Event Code", "Employee Maintenance Type Code", "Employee Maintenance Reason",  "Employee Benefit Status", "Employee Medicare Status Code", "Employee Employment Status Code", "Employee Date Time Period", "Employee Id Code Quatifier", "Employee SSN Number", "Employee Old Id Code Quatifier", "Employee Old SSN Number", "Employee Prefix Name", "Employee First Name", "Employee Middle Name", "Employee Last Name", "Employee Suffix Name", "Employee Old Prefix Name", "Employee Old First Name", "Employee Old Middle Name", "Employee Old Last Name", "Employee Old Suffix Name", "Employee Gender", "Employee Merital Status",  "Employee DOB", "Employee Old Gender", "Employee Old Merital Status", "Employee Old DOB",  "Employee Contact1", "Employee Contact2", "Employee Contact3",

    "Employee Medicare Plan Maintenance-1",
    "Employee Insurance Line Code-1",
    "Employee Plan Description-1",
    "Employee Coverage Lavel Code-1",
    "Employee Benefit Begin-1",
    "Employee Benefit End-1",
    "Employee Non Smoker Discount-1",

    "Employee Medicare Plan Maintenance-2",
    "Employee Insurance Line Code-2",
    "Employee Plan Description-2",
    "Employee Coverage Lavel Code-2",
    "Employee Benefit Begin-2",
    "Employee Benefit End-2",
    "Employee Non Smoker Discount-2",

    "Employee Medicare Plan Maintenance-3",
    "Employee Insurance Line Code-3",
    "Employee Plan Description-3",
    "Employee Coverage Lavel Code-3",
    "Employee Benefit Begin-3",
    "Employee Benefit End-3",
    "Employee Non Smoker Discount-3",

    "Employee Medicare Plan Maintenance-4",
    "Employee Insurance Line Code-4",
    "Employee Plan Description-4",
    "Employee Coverage Lavel Code-4",
    "Employee Benefit Begin-4",
    "Employee Benefit End-4",
    "Employee Non Smoker Discount-4",

    "Employee Status Details-1",
    "Employee Employment Status-1",
    "Employee Employment Status Date Format-1",
    "Employee Employment Status Start/End Date-1",

    "Employee Status Details-2",
    "Employee Employment Status-2",
    "Employee Employment Status Date Format-2",
    "Employee Employment Status Start/End Date-2",

    "Employee Status Details-3",
    "Employee Employment Status-3",
    "Employee Employment Status Date Format-3",
    "Employee Employment Status Start/End Date-3",

    "Employee Status Details-4",
    "Employee Employment Status-4",
    "Employee Employment Status Date Format-4",
    "Employee Employment Status Start/End Date-4",

    "Employee Status Details-5",
    "Employee Employment Status-5",
    "Employee Employment Status Date Format-5",
    "Employee Employment Status Start/End Date-5",

    "Employee Status Details-6",
    "Employee Employment Status-6",
    "Employee Employment Status Date Format-6",
    "Employee Employment Status Start/End Date-6",

    "Employee Hiring Date",
    "Employee Employment End Date",
    "Employee Employment QE Date",
    "Employee Adjusted Service Date",
    "Employee Medicare Start Date1",
    "Employee Medicare Start Date2",
    "Employee Medicare Start Date3",
    "Employee Medicare End Date1",
    "Employee Medicare End Date2",
    "Employee Medicare End Date3",
    "Employee Medicare Received Date",
    "Employee Retirement Date",
    "Employee Enrollment Signature Date",
    "Employee Maintenance Effective Date",
    "Employee Education Begin Date",
    "Employee Education End Date",
    "Employee Eligibility Begin Date",
    "Employee Eligibility End Date",
    "Employee Credited Service Begin Date",
    "Employee Credited Service End Date",
    "Employee Plan Participation Suspension Date",
    "Employee Rehire Date",
    "Employee Medicaid Begin Date",
    "Employee Medicaid End Date",

    "Employee Address", "Employee Old Address",

    *Dependent_details_columns,


    "Responsible Person SSN", "Responsible Person Prefix Name", "Responsible Person First Name", "Responsible Person Middle Name", "Responsible Person Last Name", "Responsible Person Suffix Name",

    "Ex Spouse SSN", "Ex Spouse Prefix Name", "Ex Spouse First Name", "Ex Spouse Middle Name", "Ex Spouse Last Name", "Ex Spouse Suffix Name",

    "Guardian SSN", "Guardian Prefix Name", "Guardian First Name", "Guardian Middle Name", "Guardian Last Name", "Guardian Suffix Name",

    "Case-Manager SSN", "Case-Manager Prefix Name", "Case-Manager First Name", "Case-Manager Middle Name", "Case-Manager Last Name", "Case-Manager Suffix Name",

    "Key-Person SSN", "Key-Person Prefix Name", "Key-Person First Name", "Key-Person Middle Name", "Key-Person Last Name", "Key-Person Suffix Name",

    "Parent SSN", "Parent Prefix Name", "Parent First Name", "Parent Middle Name", "Parent Last Name", "Parent Suffix Name",
    "Executor SSN", "Executor Prefix Name", "Executor First Name", "Executor Middle Name", "Executor Last Name", "Executor Suffix Name",

    "Responsibel Party SSN", "Responsibel Party Prefix Name", "Responsibel Party First Name", "Responsibel Party Middle Name", "Responsibel Party Last Name", "Responsibel Party Suffix Name",

    "Other Insured Person SSN", "Other Insured Person Prefix Name", "Other Insured Person First Name", "Other Insured Person Middle Name", "Other Insured Person Last Name", "Other Insured Person Suffix Name",

    "Significant Person SSN", "Significant Person Prefix Name", "Significant Person First Name", "Significant Person Middle Name", "Significant Person Last Name", "Significant Person Suffix Name",

    "Lagal Representative Person SSN", "Lagal Representative Person Prefix Name", "Lagal Representative Person First Name", "Lagal Representative Person Middle Name", "Lagal Representative Person Last Name", "Lagal Representative Person Suffix Name",

    "Attorney Person SSN", "Attorney Person Prefix Name", "Attorney Person First Name", "Attorney Person Middle Name", "Attorney Person Last Name", "Attorney Person Suffix Name",
    "Disability Code Value", "Service Id Qualifier", "Initial Disability Period Start Date", "Initial Disability Period End Date", 
    
    
    "Employer Entity Id Code","Employer Entity Type Code","Employer First Name","Employer Middle Name","Employer Last Name","Employer Prefix Name","Employer Suffix Name","Employer SSN Number","Employer Id Code","Employer Contact1","Employer Contact2","Employer Contact3","Employer Address",

    "School Entity Id Code","School Entity Type Qualifier","School Name","School Contact1","School Contact2","School Contact3","School Address",

    "Custodial Entity Id Code","Custodial Entity Type Code","Custodial First Name","Custodial Middle Name","Custodial Last Name","Custodial Prefix Name","Custodial Suffix Name","Custodial SSN Number","Custodial Id Code","Custodial Contact1","Custodial Contact2","Custodial Contact3","Custodial Address",

    "Entity Id Code (Drop of Location)","Entity Type Qualifier (Drop of Location)","First Name(Drop of Location)","Last Name (Drop of Location)","Drop of Address",

    "Number Of Included Sigment",
])
df_common = pd.DataFrame(Common_parts_of_transaction.items(), columns=['Attribute', 'Values'])


output_file_path = "C:\\Users\\USER\\Desktop\\ITEDUIM Project\\ITEDUIM20240409.xlsx"
with pd.ExcelWriter(output_file_path) as writer:
    df_result.to_excel(writer, sheet_name='All_Transactions', index=False) 
with pd.ExcelWriter(output_file_path, mode='a', engine='openpyxl') as writer:
    df_common.to_excel(writer, sheet_name='Important_Information', index=False)

