import pandas as pd
from datetime import datetime 
from edidictionary import  common_parts_of_transaction

def process_file(input_file_path):
   
    df = pd.read_excel(input_file_path)
    
    edi_data = []
    
    header_line_edi1 = f"ISA*00*          *00*          *30*{common_parts_of_transaction['Interchange Sender Id']}      *30*{common_parts_of_transaction['Interchange Receiver Id']}      *{datetime.now().strftime('%y%m%d')}*{datetime.now().strftime('%H%M')}*^*{common_parts_of_transaction['Inter Control Version Number']}*{common_parts_of_transaction['Inter Control Number']}*{common_parts_of_transaction['Acknowledgment Requested']}*{common_parts_of_transaction['Interchange Usage Indicator']}*:~"
    
    header_line_edi2 = f"GS*BE*{common_parts_of_transaction['Interchange Sender Id']}*{common_parts_of_transaction['Interchange Receiver Id']}*{datetime.now().strftime('%y%m%d')}*{datetime.now().strftime('%H%M')}*{common_parts_of_transaction['Group Control Number']}*X*{common_parts_of_transaction['Implementation Convention Reference']}~"

   
    for index, row in df.iterrows():
        edi_data.append(process_row(row))
 
    lower_file_data1 = f"GE*{row['Transaction Id']}*{common_parts_of_transaction['Group Control Number']}~"
    

    lower_file_data2 = f"IEA*1*{common_parts_of_transaction['Inter Control Number']}~"
   
    edi_string = '\n'.join(edi_data)

    
    header_and_edi_output = f"{header_line_edi1}\n{header_line_edi2}\n{edi_string}\n{lower_file_data1}\n{lower_file_data2}"

    return header_and_edi_output

def process_row(row):
    edi_segments = []
    #transaction (ST)starting segment.................
    transaction_id = row['Transaction Id']
    st_segment = "ST*834*{:04d}*{}~".format(transaction_id, common_parts_of_transaction['Implementation Convention Reference'])
    edi_segments.append(st_segment)
    #transaction BGN segment.................
    bgn_segment = f"BGN*{common_parts_of_transaction['Transaction Set Purpose Code']}*{common_parts_of_transaction['Transaction Set Reference Number']}*{common_parts_of_transaction['Transaction Date']}*{common_parts_of_transaction['Transaction Time']}*ET***2~"
    edi_segments.append(bgn_segment)

    #transaction employee and total dependent.................
    qty_dt_segment = "QTY*DT*{}~".format(row["Total Of Dependent"])
    qty_et_segment = "QTY*ET*{}~".format(row["Total Of Employee"])
    qty_to_segment = "QTY*TO*{}~".format(row["Total Of Dep & Emp"])
    
    edi_segments.extend([qty_dt_segment, qty_et_segment, qty_to_segment])
    #transaction unit name and id number.................
    n1_p5_segment = "N1*P5*{}*{}*{}~".format(row["Unit Name"], row["Unit Id Code Qualifier"], row["Unit Id"])
    n1_in_segment = "N1*IN*{}*{}*{}~".format(row["Insurer Name"], row["Insurer Id Code Qualifier"], str(row["Insurer Id"]).zfill(9))
    #transaction vendor name and id number.................
    n1_tv_segment = f"N1*TV*{common_parts_of_transaction ['Vendor Name']}*{common_parts_of_transaction['Vendor Id Code Qualifier']}*{common_parts_of_transaction['Vendor Id']}~"
    edi_segments.extend([n1_p5_segment, n1_in_segment, n1_tv_segment])
    
    edi_segments.extend(process_employee(row))

    edi_segments.extend(process_dependents(row))

    transaction_end = row['Transaction Id']
    se_segment = "SE*{}*{:04d}~".format(row["Number Of Included Sigment"], transaction_end)
    edi_segments.append(se_segment)

    return '\n'.join(edi_segments)

def process_employee(row):
    employee_segments = []
    #employee INS segment.............
    if pd.notna(row['Employee Relationship Code']):
        employee_relationship_code = str(row['Employee Relationship Code']).split("-")
    else: 
        employee_relationship_code = ''

    if pd.notna(row['Employee Maintenance Type Code']):
        employee_maintenance_type_code = str(row['Employee Maintenance Type Code']).split("-")
    else: 
        employee_maintenance_type_code = ''
       
    if pd.notna(row['Employee Maintenance Reason']):
        employee_maintenance_reason_code = str(row['Employee Maintenance Reason']).split("-")
    else: 
        employee_maintenance_reason_code = ''
    
    if pd.notna(row['Employee Benefit Status']):
        employee_benefit_status = (row['Employee Benefit Status']).split("-")
    else:
        employee_benefit_status = ''
      
    if pd.notna(row['Employee Medicare Status Code']):
        employee_medicare_status = str(row['Employee Medicare Status Code'])
    else:
        employee_medicare_status = ''
    
    if pd.notna(row['Employee Cobra Event Code']):
        employee_cobra_event = (row['Employee Cobra Event Code']).split("-")   
    else:
         employee_cobra_event = ''   
   
    if pd.notna(row['Employee Employment Status Code']):
        employee_employment_status_code = (row['Employee Employment Status Code']).split("-")
    else:
        employee_employment_status_code = ''
       
    if pd.notna(row['Employee Y/N Condition Code']):
        employee_condition_code = str(row['Employee Y/N Condition Code'])
    else:
        employee_condition_code = ''
    
    if pd.notna(row['Employee Date Time Period']):
        employee_date_time_period = (row['Employee Date Time Period'])
        dep_date_time = datetime.strptime(employee_date_time_period, '%m-%d-%Y').strftime('%Y%m%d')
    else:
        dep_date_time = ''
       
    if pd.notna(row['Employee Y/N Condition Code']):
        employee_condition_code = str(row['Employee Y/N Condition Code'])
    else:
        employee_condition_code = ''
    
    if pd.notna(row['Employee Date Time Period']):
       employee_INS_segment = "INS*Y*{}*{}*{}*{}*{}*{}*{}**{}*D8*{}~".format(
            employee_relationship_code[0], 
            employee_maintenance_type_code[0] if employee_maintenance_type_code else '',
            employee_maintenance_reason_code[0] if employee_maintenance_reason_code else '',  
            employee_benefit_status[0] if employee_benefit_status else '', 
            employee_medicare_status, 
            employee_cobra_event[0] if employee_cobra_event else '', 
            employee_employment_status_code[0] if employee_employment_status_code else '', 
            employee_condition_code,
            dep_date_time,
        )
       employee_segments.append(employee_INS_segment)
    
    elif pd.notna(row['Employee Maintenance Type Code']):
        employee_INS_segment = "INS*Y*{}*{}*{}*{}*{}*{}*{}**{}~".format(
            employee_relationship_code[0], 
            employee_maintenance_type_code[0] if employee_maintenance_type_code else '',
            employee_maintenance_reason_code[0] if employee_maintenance_reason_code else '',  
            employee_benefit_status[0] if employee_benefit_status else '', 
            employee_medicare_status, 
            employee_cobra_event[0] if employee_cobra_event else '', 
            employee_employment_status_code[0] if employee_employment_status_code else '', 
            employee_condition_code
        )
        employee_segments.append(employee_INS_segment)

    #employee REF 0F segment............
    if pd.notna(row['Employee Depend SSN Number']):
        employee_ssn = str(int(row['Employee Depend SSN Number'])).zfill(9)
        employee_REF_0F_segment ="REF*0F*{}~".format(employee_ssn)
        employee_segments.append(employee_REF_0F_segment)
        
    #employee REF 17 segment............
    if pd.notna(row['Employee Client Reporting Catagory']):
        employee_reporting_catagory = str(row['Employee Client Reporting Catagory'])
        employee_REF_17_number = "REF*17*{}~".format(employee_reporting_catagory)
        employee_segments.append(employee_REF_17_number)
    #employee REF DX segment............
    if pd.notna(row['Employee Department Number']):
        department_number = str(row['Employee Department Number'])
        employee_REF_DX_number = "REF*DX*{}~".format(department_number)
        employee_segments.append(employee_REF_DX_number)
    
    #employee REF 23 segment............
    if pd.notna(row['Employee Sup-Id']):
        employee_sub_id = str(row['Employee Sup-Id'])
        employee_REF_23_segment ="REF*23*{}~".format(employee_sub_id)
        employee_segments.append(employee_REF_23_segment)
    
    #employee REF ABB segment............
    if pd.notna(row['Employee Personal Id Number']):
        employee_personal_id_no = str(row['Employee Personal Id Number'])
        employee_REF_ABB_number = "REF*ABB*{}~".format(employee_personal_id_no)
        employee_segments.append(employee_REF_ABB_number)
    
    #employee REF ZZ segment............
    if pd.notna(row['Employee Mutually Defined']):
        employee_mutually_defined = str(row['Employee Mutually Defined'])
        employee_REF_ZZ_number = "REF*ZZ*{}~".format(employee_mutually_defined)
        employee_segments.append(employee_REF_ZZ_number)
    
    #employee REF F6 segment............
    if pd.notna(row['Employee Health Insurance Claim Number']):
        employee_health_insurance_claim_no = str(row['Employee Health Insurance Claim Number'])
        employee_REF_F6_number = "REF*F6*{}~".format(employee_health_insurance_claim_no)
        employee_segments.append(employee_REF_F6_number)

    #employee REF 3H segment............
    if pd.notna(row['Employee Case Number']):
        employee_case_no = str(row['Employee Case Number'])
        employee_REF_3H_segment = "REF*3H*{}~".format(employee_case_no)
        employee_segments.append(employee_REF_3H_segment)
    
    #employee REF 4H segment............
    if pd.notna(row['Employee Personal Identification Number']):
        employee_personal_identification_no = str(row['Employee Personal Identification Number'])
        employee_REF_4H_segment = "REF*4H*{}~".format(employee_personal_identification_no)
        employee_segments.append(employee_REF_4H_segment)
            
    #employee REF 60 segment............
    if pd.notna(row['Employee Cross Refference Number']):
        employee_cross_refference_no = str(row['Employee Cross Refference Number'])
        employee_REF_60_segment = "REF*6O*{}~".format(employee_cross_refference_no)
        employee_segments.append(employee_REF_60_segment)
    
    #employee REF D3 segment............
    if pd.notna(row['Employee Pharmacy Number']):
        employee_pharmacy_no = str(row['Employee Pharmacy Number'])
        employee_REF_D3_segment = "REF*D3*{}~".format(employee_pharmacy_no)
        employee_segments.append(employee_REF_D3_segment)

    #employee REF P5 segment............
    if pd.notna(row['Employee Positon Code']):
        employee_position_code = str(row['Employee Positon Code'])
        employee_REF_P5_segment = "REF*P5*{}~".format(employee_position_code)
        employee_segments.append(employee_REF_P5_segment)

    #employee REF Q4 segment............
    if pd.notna(row['Employee Prior Identification Number']):
        employee_prior_id_no = str(row['Employee Prior Identification Number'])
        employee_REF_Q4_segment = "REF*Q4*{}~".format(employee_prior_id_no)
        employee_segments.append(employee_REF_Q4_segment)
    
    #employee REF QQ segment............
    if pd.notna(row['Employee Unit Number']):
        employee_unit_no = str(row['Employee Unit Number'])
        employee_REF_QQ_segment = "REF*QQ*{}~".format(employee_unit_no)
        employee_segments.append(employee_REF_QQ_segment)

    employee_medicare_received_date = str(row["Employee Medicare Received Date"])
    if pd.notna (employee_medicare_received_date) and employee_medicare_received_date != 'nan':
        emp_medicare_received_date = datetime.strptime(employee_medicare_received_date, '%m-%d-%Y').strftime('%Y%m%d')
        employee_050_segment = "DTP*050*D8*{}~".format(emp_medicare_received_date)
        employee_segments.append(employee_050_segment)

    employee_retirement_date = str(row["Employee Retirement Date"])
    if pd.notna (employee_retirement_date) and employee_retirement_date != 'nan':
        emp_retirement_date = datetime.strptime(employee_retirement_date, '%m-%d-%Y').strftime('%Y%m%d')
        employee_286_segment = "DTP*286*D8*{}~".format(emp_retirement_date)
        employee_segments.append(employee_286_segment)

    employee_enrollment_signature_signature_date = str(row["Employee Enrollment Signature Date"])
    if pd.notna (employee_enrollment_signature_signature_date) and employee_enrollment_signature_signature_date != 'nan':
        emp_enrollment_signature_signature_date = datetime.strptime(employee_enrollment_signature_signature_date, '%m-%d-%Y').strftime('%Y%m%d')
        employee_300_segment = "DTP*300*D8*{}~".format(emp_enrollment_signature_signature_date)
        employee_segments.append(employee_300_segment)

    #employee QE segment.............
    employee_employment_QE_date = str(row["Employee Employment QE Date"])
    if pd.notna (employee_employment_QE_date) and employee_employment_QE_date != 'nan':
        emp_employment_QE_date = datetime.strptime(employee_employment_QE_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_301_segment = "DTP*301*D8*{}~".format(emp_employment_QE_date)
        employee_segments.append(dtp_301_segment)
   
    employee_maintenance_effective_date = str(row["Employee Maintenance Effective Date"])
    if pd.notna (employee_maintenance_effective_date) and employee_maintenance_effective_date != 'nan':
        emp_maintenance_effective_date = datetime.strptime(employee_maintenance_effective_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_303_segment = "DTP*303*D8*{}~".format(emp_maintenance_effective_date)
        employee_segments.append(dtp_303_segment)

    empoyment_hiring_date = str(row["Employee Hiring Date"])
    if pd.notna(empoyment_hiring_date) and empoyment_hiring_date != 'nan':
        emp_hiring_date = datetime.strptime(empoyment_hiring_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_336_segment = "DTP*336*D8*{}~".format(emp_hiring_date)
        employee_segments.append(dtp_336_segment)
        
    employment_end_date = str(row["Employee Employment End Date"])
    if pd.notna(employment_end_date) and employment_end_date != 'nan':
        emp_end_date = datetime.strptime(employment_end_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_337_segment = "DTP*337*D8*{}~".format(emp_end_date)
        employee_segments.append(dtp_337_segment)
    

    if pd.notna(row["Employee Medicare Start Date1"]) and pd.isna(row["Employee Medicare Start Date2"]) and pd.isna(row["Employee Medicare End Date1"]) and pd.isna(row["Employee Medicare End Date2"]):
        employment_medicare_start_date = str(row["Employee Medicare Start Date1"])
        emp_medicare_start_date = datetime.strptime(employment_medicare_start_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_338_segment = "DTP*338*D8*{}~".format(emp_medicare_start_date)
        employee_segments.append(dtp_338_segment)
        
    
    
    if pd.notna(row["Employee Medicare Start Date1"]) and pd.notna(row["Employee Medicare Start Date2"]) and pd.isna(row["Employee Medicare End Date1"]) and pd.isna(row["Employee Medicare End Date2"]):
        employment_medicare_start_date = str(row["Employee Medicare Start Date1"])
        emp_medicare_start_date = datetime.strptime(employment_medicare_start_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_338_segment = "DTP*338*D8*{}~".format(emp_medicare_start_date)
        employee_segments.append(dtp_338_segment)
        
        employment_medicare_start_date2 = str(row["Employee Medicare Start Date2"])
        emp_medicare_start_date2 = datetime.strptime(employment_medicare_start_date2, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_338_segment2 = "DTP*338*D8*{}~".format(emp_medicare_start_date2)
        employee_segments.append(dtp_338_segment2)

    if pd.notna(row["Employee Medicare Start Date1"]) and pd.notna(row["Employee Medicare Start Date2"]) and pd.notna(row["Employee Medicare End Date1"]) and pd.isna(row["Employee Medicare End Date2"]):
        employment_medicare_start_date = str(row["Employee Medicare Start Date1"])
        emp_medicare_start_date = datetime.strptime(employment_medicare_start_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_338_segment = "DTP*338*D8*{}~".format(emp_medicare_start_date)
        employee_segments.append(dtp_338_segment)
        
        employment_medicare_start_date2 = str(row["Employee Medicare Start Date2"])
        emp_medicare_start_date2 = datetime.strptime(employment_medicare_start_date2, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_338_segment2 = "DTP*338*D8*{}~".format(emp_medicare_start_date2)
        employee_segments.append(dtp_338_segment2)

        employment_medicare_end_date = str(row["Employee Medicare End Date1"])
        emp_medicare_end_date = datetime.strptime(employment_medicare_end_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_339_segment = "DTP*339*D8*{}~".format(emp_medicare_end_date)
        employee_segments.append(dtp_339_segment)

    if pd.notna(row["Employee Medicare Start Date1"]) and pd.notna(row["Employee Medicare Start Date2"]) and pd.notna(row["Employee Medicare End Date1"]) and pd.notna(row["Employee Medicare End Date2"]):
        employment_medicare_start_date = str(row["Employee Medicare Start Date1"])
        emp_medicare_start_date = datetime.strptime(employment_medicare_start_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_338_segment = "DTP*338*D8*{}~".format(emp_medicare_start_date)
        employee_segments.append(dtp_338_segment)

        employment_medicare_end_date = str(row["Employee Medicare End Date1"])
        emp_medicare_end_date = datetime.strptime(employment_medicare_end_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_339_segment = "DTP*339*D8*{}~".format(emp_medicare_end_date)
        employee_segments.append(dtp_339_segment)
        
        employment_medicare_start_date2 = str(row["Employee Medicare Start Date2"])
        emp_medicare_start_date2 = datetime.strptime(employment_medicare_start_date2, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_338_segment2 = "DTP*338*D8*{}~".format(emp_medicare_start_date2)
        employee_segments.append(dtp_338_segment2)

        employment_medicare_end_date2 = str(row["Employee Medicare End Date2"])
        emp_medicare_end_date2 = datetime.strptime(employment_medicare_end_date2, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_339_segment2 = "DTP*339*D8*{}~".format(emp_medicare_end_date2)
        employee_segments.append(dtp_339_segment2)

    if pd.notna(row["Employee Medicare Start Date1"]) and pd.isna(row["Employee Medicare Start Date2"]) and pd.notna(row["Employee Medicare End Date1"]) and pd.isna(row["Employee Medicare End Date2"]):
        employment_medicare_start_date = str(row["Employee Medicare Start Date1"])
        emp_medicare_start_date = datetime.strptime(employment_medicare_start_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_338_segment = "DTP*338*D8*{}~".format(emp_medicare_start_date)
        employee_segments.append(dtp_338_segment)

        employment_medicare_end_date = str(row["Employee Medicare End Date1"])
        emp_medicare_end_date = datetime.strptime(employment_medicare_end_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_339_segment = "DTP*339*D8*{}~".format(emp_medicare_end_date)
        employee_segments.append(dtp_339_segment)
    
    
    employee_education_begin_date = str(row["Employee Education Begin Date"])
    if pd.notna (employee_education_begin_date) and employee_education_begin_date !='nan':
        emp_education_begin_date = datetime.strptime(employee_education_begin_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_350_segment = "DTP*350*D8*{}~".format(emp_education_begin_date)
        employee_segments.append(dtp_350_segment)   
    
    employee_education_end_date = str(row["Employee Education End Date"])
    if pd.notna (employee_education_end_date) and employee_education_end_date !='nan':
        emp_education_end_date = datetime.strptime(employee_education_end_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_351_segment = "DTP*351*D8*{}~".format(emp_education_end_date)
        employee_segments.append(dtp_351_segment)

    employee_eligibility_begin_date = str(row["Employee Eligibility Begin Date"])
    if pd.notna (employee_eligibility_begin_date) and employee_eligibility_begin_date !='nan':
        emp_eligibility_begin_date = datetime.strptime(employee_eligibility_begin_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_356_segment = "DTP*356*D8*{}~".format(emp_eligibility_begin_date)
        employee_segments.append(dtp_356_segment)
    
    employee_eligibility_end_date = str(row["Employee Eligibility End Date"])
    if pd.notna (employee_eligibility_end_date) and employee_eligibility_end_date !='nan':
        emp_eligibility_end_date = datetime.strptime(employee_eligibility_end_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_357_segment = "DTP*357*D8*{}~".format(emp_eligibility_end_date)
        employee_segments.append(dtp_357_segment)
    
    employment_adjusted_service_date = str(row["Employee Adjusted Service Date"])
    if pd.notna (employment_adjusted_service_date) and employment_adjusted_service_date !='nan':
        emp_adjusted_service_date = datetime.strptime(employment_adjusted_service_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_383_segment = "DTP*383*D8*{}~".format(emp_adjusted_service_date)
        employee_segments.append(dtp_383_segment)

    employee_credited_service_begin_date = str(row["Employee Credited Service Begin Date"])
    if pd.notna (employee_credited_service_begin_date) and employee_credited_service_begin_date !='nan':
        empl_credited_service_begin_date = datetime.strptime(employee_credited_service_begin_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_385_segment = "DTP*385*D8*{}~".format(empl_credited_service_begin_date)
        employee_segments.append(dtp_385_segment)

    employee_credited_service_end_date = str(row["Employee Credited Service End Date"])
    if pd.notna (employee_credited_service_end_date) and employee_credited_service_end_date !='nan':
        emp_credited_service_end_date = datetime.strptime(employee_credited_service_end_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_386_segment = "DTP*386*D8*{}~".format(emp_credited_service_end_date)
        employee_segments.append(dtp_386_segment)

    employee_plan_par_date = str(row["Employee Plan Participation Suspension Date"])
    if pd.notna (employee_plan_par_date) and employee_plan_par_date !='nan':
        emp_plan_par_date = datetime.strptime(employee_plan_par_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_393_segment = "DTP*393*D8*{}~".format(emp_plan_par_date)
        employee_segments.append(dtp_393_segment)

    employee_rehire_date = str(row["Employee Rehire Date"])
    if pd.notna (employee_rehire_date) and employee_rehire_date !='nan':
        empl_rehire_date = datetime.strptime(employee_rehire_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_394_segment = "DTP*394*D8*{}~".format(empl_rehire_date)
        employee_segments.append(dtp_394_segment)

    employee_medicaid_begin_date = str(row["Employee Medicaid Begin Date"])
    if pd.notna (employee_medicaid_begin_date) and employee_medicaid_begin_date !='nan':
        emp_medicaid_begin_date = datetime.strptime(employee_medicaid_begin_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_473_segment = "DTP*473*D8*{}~".format(emp_medicaid_begin_date)
        employee_segments.append(dtp_473_segment)
    
    employee_medicaid_end_date = str(row["Employee Medicaid End Date"])
    if pd.notna (employee_medicaid_end_date) and employee_medicaid_end_date !='nan':
        emp_medicaid_end_date = datetime.strptime(employee_medicaid_end_date, '%m-%d-%Y').strftime('%Y%m%d')
        dtp_474_segment = "DTP*474*D8*{}~".format(emp_medicaid_end_date)
        employee_segments.append(dtp_474_segment)

    #employee NM1 segment..........
    if pd.notna(row['Employee SSN Number']):
        employee_ssn_no = str(int(row['Employee SSN Number'])).zfill(9)
    else:
        employee_ssn_no = ""
        
    if pd.notna(row['Employee Last Name']):
        employee_Last_name =  (row['Employee Last Name'])
    else:
        employee_Last_name = ""

    if pd.notna(row['Employee First Name']):
        employee_First_name =  (row['Employee First Name'])
    else:
        employee_First_name = ""
        
    if pd.notna(row['Employee Middle Name']):
        employee_Middle_name =  (row['Employee Middle Name'])
    else:
        employee_Middle_name = ""

    if pd.notna(row['Employee Prefix Name']):
        employee_Prefix_name =  (row['Employee Prefix Name'])
    else:
        employee_Prefix_name = ""
        
    if pd.notna(row['Employee Suffix Name']):
        employee_Suffix_name =  (row['Employee Suffix Name'])
    else:
            employee_Suffix_name = ""
        
    if pd.notna(row['Employee Id Code Quatifier']):
        employee_id_code_quatifier = str(int(row['Employee Id Code Quatifier']))
    else:
        employee_id_code_quatifier = ""

    employee_changed = str(row['Employee Changed?(Yes/No)'])
    employee_changes = employee_changed.split("-")
    if (employee_First_name):
        if(employee_id_code_quatifier):         
            employee_NMA1_segment = "NM1*{}*1*{}*{}*{}*{}*{}*{}*{}~".format(
                employee_changes[0],
                employee_Last_name if employee_Last_name else '',
                employee_First_name if employee_First_name else '',
                employee_Middle_name if employee_Middle_name else '',
                employee_Prefix_name if employee_Prefix_name else '',
                employee_Suffix_name if employee_Suffix_name else '',
                employee_id_code_quatifier if employee_id_code_quatifier else '',
                employee_ssn_no if employee_ssn_no else ''
                )
        elif(employee_Last_name and employee_First_name and employee_Middle_name and employee_Prefix_name and employee_Suffix_name):
            employee_NMA1_segment = "NM1*{}*1*{}*{}*{}*{}*{}~".format(
                employee_changes[0],
                employee_Last_name if employee_Last_name else '',
                employee_First_name if employee_First_name else '',
                employee_Middle_name if employee_Middle_name else '',
                employee_Prefix_name if employee_Prefix_name else '',
                employee_Suffix_name if employee_Suffix_name else '',
            )
        elif(employee_Last_name and employee_First_name and employee_Middle_name and employee_Suffix_name):
            employee_NMA1_segment = "NM1*{}*1*{}*{}*{}**{}~".format(
                employee_changes[0],
                employee_Last_name if employee_Last_name else '',
                employee_First_name if employee_First_name else '',
                employee_Middle_name if employee_Middle_name else '',
                employee_Suffix_name if employee_Suffix_name else '',
            )
        elif(employee_Last_name and employee_First_name and employee_Middle_name and employee_Prefix_name):
            employee_NMA1_segment = "NM1*{}*1*{}*{}*{}*{}~".format(
                employee_changes[0],
                employee_Last_name if employee_Last_name else '',
                employee_First_name if employee_First_name else '',
                employee_Middle_name if employee_Middle_name else '',
                employee_Prefix_name if employee_Prefix_name else ''
            )
        elif(employee_Last_name and employee_First_name and employee_Middle_name):
            employee_NMA1_segment = "NM1*{}*1*{}*{}*{}~".format(
                employee_changes[0],
                employee_Last_name if employee_Last_name else '',
                employee_First_name if employee_First_name else '',
                employee_Middle_name if employee_Middle_name else ''
            )
        elif(employee_Last_name and employee_First_name):
            employee_NMA1_segment = "NM1*{}*1*{}*{}~".format(
                employee_changes[0],
                employee_Last_name if employee_Last_name else '',
                employee_First_name if employee_First_name else '',

            )

        employee_segments.append(employee_NMA1_segment)

    #Employee Contact Details...............
    if pd.notna(row['Employee Contact1']):
        employee_contact1 = '*' + '*'.join(row['Employee Contact1'].split(":"))
    else:
        employee_contact1 = ""

    if pd.notna(row['Employee Contact2']):
        employee_contact2 = '*' + '*'.join(row['Employee Contact2'].split(":"))
    else:
        employee_contact2 = ""

    if pd.notna(row["Employee Contact3"]):
        employee_contact3 = '*' + '*'.join(row['Employee Contact3'].split(":"))
    else:
        employee_contact3 = ""

    if pd.notna(row["Employee Contact1"]):
        per_segment = "PER*IP*{}{}{}{}{}{}~".format(
            employee_contact1,
            employee_contact2,
            employee_contact3,
            "", 
            "", 
            ""  
        ) 
        employee_segments.append(per_segment)

    # Employee Address Details
    if pd.notna(row["Employee Address"]):
        address_components = str(row["Employee Address"]).split(',')
        address1 = address_components[0]
        address2 = address_components[1]

        # Split address1 into address positions
        n3_address = address1.split("_")
        street_address_1 = n3_address[0]
        street_address_2 = ""
        if len(n3_address)==2:
            street_address_2 = n3_address[1]
        n3_segment = "N3*{}{}~".format(
            street_address_1, 
            "*" + street_address_2 if street_address_2 else '',
        )
        employee_segments.append(n3_segment)

        # Split address2 into city, state, and zip code
        n4_address = address2.split('/')
        city = n4_address[0]
        state = n4_address[1]
        zip_code = n4_address[2]
        country_code = ""
        if len(n4_address) == 4:
            country_code = n4_address[3]
        
        n4_segment = "N4*{}*{}*{}{}~".format(
            city,
            state,
            zip_code,
            "*" + country_code if country_code else ""
        )
        employee_segments.append(n4_segment)


   

    #employee DMG segment...........
    if pd.notna(row["Employee DOB"]):
        date_of_birth = datetime.strptime(row["Employee DOB"], '%m-%d-%Y').strftime('%Y%m%d')
        employee_gender = row["Employee Gender"]
        employee_marital_status = row['Employee Merital Status']

        dmg_segment = "DMG*D8*{}*{}{}~".format(
            date_of_birth,
            employee_gender,
            "*" + employee_marital_status if employee_marital_status else ''  
        )
        employee_segments.append(dmg_segment)

    #Employee 70 Segment...............
    if pd.notna(row['Employee Old SSN Number']):
        employee_old_ssn_no = str(int(row['Employee Old SSN Number'])).zfill(9)
    else:
        employee_old_ssn_no = ""
         
    if pd.notna(row['Employee Old Last Name']):
        employee_old_last_name = (row['Employee Old Last Name'])
    else:
        employee_old_last_name = ""

    if pd.notna(row['Employee Old First Name']):
        employee_old_first_name = (row['Employee Old First Name'])
    else:
        employee_old_first_name = ""
                
    if pd.notna(row['Employee Old Middle Name']):
        employee_old_middle_name = (row['Employee Old Middle Name'])
    else:
        employee_old_middle_name = ""

    if pd.notna(row['Employee Old Prefix Name']):
        employee_old_prefix_name = (row['Employee Old Prefix Name'])
    else:
        employee_old_prefix_name = ""
                
    if pd.notna(row['Employee Old Suffix Name']):
        employee_old_suffix_name = (row['Employee Old Suffix Name'])
    else:
        employee_old_suffix_name = ""
                     
    if pd.notna(row['Employee Old Id Code Quatifier']):
        employee_old_id_code = str(int(row['Employee Old Id Code Quatifier']))
    else:
        employee_old_id_code = ""
    if(employee_old_first_name):
        if(employee_old_id_code):          
            employee_old_NMA1_segment = "NM1*70*1*{}*{}*{}*{}*{}*{}*{}~".format(
                employee_old_last_name if employee_old_last_name else '',
                employee_old_first_name if employee_old_first_name else '',
                employee_old_middle_name if employee_old_middle_name else '',
                employee_old_prefix_name if employee_old_prefix_name else '',
                employee_old_suffix_name if employee_old_suffix_name else '',
                employee_id_code_quatifier if employee_id_code_quatifier else '',
                employee_old_ssn_no if employee_old_ssn_no else ''
            )
        elif(employee_old_last_name and employee_old_first_name and employee_old_middle_name and employee_old_prefix_name and employee_old_suffix_name):
            employee_old_NMA1_segment = "NM1*{}*1*{}*{}*{}*{}*{}~".format(
                employee_old_last_name if employee_old_last_name else '',
                employee_old_first_name if employee_old_first_name else '',
                employee_old_middle_name if employee_old_middle_name else '',
                employee_old_prefix_name if employee_old_prefix_name else '',
                employee_old_suffix_name if employee_old_suffix_name else '',
            )
        elif(employee_old_last_name and employee_old_first_name and employee_old_middle_name and employee_old_suffix_name):
            employee_old_NMA1_segment = "NM1*{}*1*{}*{}*{}**{}~".format(
                employee_old_last_name if employee_old_last_name else '',
                employee_old_first_name if employee_old_first_name else '',
                employee_old_middle_name if employee_old_middle_name else '',
                employee_old_suffix_name if employee_old_suffix_name else '',
            )
        elif(employee_old_last_name and employee_old_first_name and employee_old_suffix_name):
            employee_old_NMA1_segment = "NM1*{}*1*{}*{}*{}**{}~".format(
                employee_old_last_name if employee_old_last_name else '',
                employee_old_first_name if employee_old_first_name else '',
                employee_old_suffix_name if employee_old_suffix_name else '',
            )
        elif(employee_old_last_name and employee_old_first_name and employee_old_middle_name and employee_old_prefix_name):
            employee_old_NMA1_segment = "NM1*{}*1*{}*{}*{}*{}~".format(
                employee_old_last_name if employee_old_last_name else '',
                employee_old_first_name if employee_old_first_name else '',
                employee_old_middle_name if employee_old_middle_name else '',
                employee_old_prefix_name if employee_old_prefix_name else ''
            )

        elif(employee_old_last_name and employee_old_first_name and employee_old_middle_name):
            employee_old_NMA1_segment = "NM1*{}*1*{}*{}*{}~".format(
                employee_old_last_name if employee_old_last_name else '',
                employee_old_first_name if employee_old_first_name else '',
                employee_old_middle_name if employee_old_middle_name else ''
            )
        elif(employee_old_last_name and employee_old_first_name):
            employee_old_NMA1_segment = "NM1*{}*1*{}*{}~".format(
                employee_old_last_name if employee_old_last_name else '',
                employee_old_first_name if employee_old_first_name else '',

            )
        employee_segments.append(employee_old_NMA1_segment)

    emp_old_dob = "" 

    if pd.notna(row["Employee Old DOB"]) and (row["Employee Old DOB"]) != 'nan':
        employee_old_date_of_birth = str(row["Employee Old DOB"])
        emp_old_dob = datetime.strptime(employee_old_date_of_birth, '%m-%d-%Y').strftime('%Y%m%d')
      
    if pd.notna(row["Employee Old Gender"]) and (row["Employee Old Gender"]) != 'nan':
        employee_old_gender = str(row["Employee Old Gender"])
       
    if pd.notna(row["Employee Old Merital Status"]) and (row["Employee Old Merital Status"]) != 'nan':
        employee_old_merital_status = str(row["Employee Old Merital Status"])

    if pd.notna(row["Employee Old DOB"]):
        old_dmg_segment = "DMG*D8*{}*{}{}~".format(
            emp_old_dob,
            employee_old_gender if 'employee_old_gender' in locals() else '', 
            "*" + employee_old_merital_status if 'employee_old_merital_status' in locals() else ''  
        )
        employee_segments.append(old_dmg_segment)

    employee_old_address = str(row["Employee Old Address"])
    if pd.notna (employee_old_address) and employee_old_address !='nan':
        emp_NM1_31_segment = "NM1*31*1~"
        employee_segments.append(emp_NM1_31_segment)

        empl_old_address = employee_old_address.split(",")
        emp_31_n3_old_address = empl_old_address[0]
        emp_31_n4_old_address = empl_old_address[1]
        
        emp_n3_old_address = emp_31_n3_old_address .split('_')
        employee_n3_old_address1 = emp_n3_old_address[0]
        employee_n3_old_address2 = ""
        if len(emp_n3_old_address)==2:
            employee_n3_old_address2 =  emp_n3_old_address[1]
        emp_NM1_31_N3_segment = "N3*{}{}~".format(
            employee_n3_old_address1,
            "*"+employee_n3_old_address2 if employee_n3_old_address2 else ''   
        )
        employee_segments.append(emp_NM1_31_N3_segment)

        emp_n4_old_address = emp_31_n4_old_address.split('/')
        old_city = emp_n4_old_address[0]
        old_state = emp_n4_old_address[1]
        old_zip_code = emp_n4_old_address[2]
        old_country_code = ""
        if len(emp_n4_old_address) == 4:
            old_country_code = emp_n4_old_address[3]
        emp_NM1_31_N4_segment = "N4*{}*{}*{}{}~".format(
            old_city,
            old_state,
            old_zip_code,
            "*" + old_country_code if old_country_code else ""
        )

        employee_segments.append(emp_NM1_31_N4_segment)


    for i in range(1, 5):
        insurance_plan = row.get(f'Employee Medicare Plan Maintenance-{i}', '')
        
        emp_insurance_plan = insurance_plan.split("-") if pd.notna(insurance_plan) else [''] * 2
        
        insurance_code = row.get(f'Employee Insurance Line Code-{i}', '')
        plan_description = row.get(f'Employee Plan Description-{i}', '')
        coverage_level_code = row.get(f'Employee Coverage Lavel Code-{i}', '')
        if pd.notna(row[f'Employee Medicare Plan Maintenance-{i}']):
       
            hd_segment = "HD*{}**{}*{}*{}~".format(
                emp_insurance_plan[1],
                insurance_code,
                plan_description,
                coverage_level_code
            )
            employee_segments.append(hd_segment)

        employment_benefit_begin = str(row[f'Employee Benefit Begin-{i}'])
        if pd.notna(employment_benefit_begin) and employment_benefit_begin != 'nan':
            emp_benefit_begin_date = datetime.strptime(employment_benefit_begin, '%m-%d-%Y').strftime('%Y%m%d')
            dtp_348_segmentb = "DTP*348*D8*{}~".format(emp_benefit_begin_date)
            employee_segments.append(dtp_348_segmentb)
        
        employment_benefit_end = str(row[f'Employee Benefit End-{i}'])
        if pd.notna(employment_benefit_end) and employment_benefit_end != 'nan':
            emp_benefit_end_date = datetime.strptime(employment_benefit_end, '%m-%d-%Y').strftime('%Y%m%d')
            dtp_349_segmentb = "DTP*349*D8*{}~".format(emp_benefit_end_date)
            employee_segments.append(dtp_349_segmentb)

        employment_non_smoker_discount = str(row[f'Employee Non Smoker Discount-{i}'])
        if pd.notna(employment_non_smoker_discount) and employment_non_smoker_discount != 'nan': 
            ref_segment = "REF*ZZ*{}~".format(employment_non_smoker_discount[0])
            employee_segments.append(ref_segment)
            
    #Employee LS*2700~ segment...................         
    if pd.notna(row.get('Employee Status Details-1', '')):
        employee_LS_segment = "LS*2700~"
        employee_segments.append(employee_LS_segment)

    for k in range(1, 6):  

        employee_status_details = row.get(f'Employee Status Details-{k}', '')
        if pd.notna(employee_status_details):
            employee_LX_segment = f"LX*{k}~"
            employee_segments.append(employee_LX_segment)

            employee_n1_75_segment = f"N1*75*{employee_status_details}~"
            employee_segments.append(employee_n1_75_segment)

            emp_employment_status = row.get(f'Employee Employment Status-{k}', '')
            employee_ZZ_segment = f"REF*ZZ*{emp_employment_status}~"
            employee_segments.append(employee_ZZ_segment)

            employee_employment_start_end_date = row.get(f'Employee Employment Status Start/End Date-{k}', '')
            employee_employment_date_format = row.get(f'Employee Employment Status Date Format-{k}', '')

            if pd.notna(employee_employment_start_end_date):
                employee_employment_start_end = employee_employment_start_end_date.replace('.', '').strip()
                emp_employment_start_end_date = [date.strip() for date in employee_employment_start_end.split("-")]

                if len(emp_employment_start_end_date) == 1:
                    employee_emp_start_date = datetime.strptime(emp_employment_start_end_date[0], '%m%d%Y').strftime('%Y%m%d')
                    employee_DTP_007_start_end_segment = "DTP*007*{}*{}~".format(employee_employment_date_format, employee_emp_start_date)
                    employee_segments.append(employee_DTP_007_start_end_segment)

                elif len(emp_employment_start_end_date) == 2:
                    employee_emp_start_date = datetime.strptime(emp_employment_start_end_date[0], '%m%d%Y').strftime('%Y%m%d')
                    employee_emp_end_date = datetime.strptime(emp_employment_start_end_date[1], '%m%d%Y').strftime('%Y%m%d')
                    employee_DTP_007_start_end_segment = "DTP*007*{}*{}-{}~".format(employee_employment_date_format, employee_emp_start_date,  employee_emp_end_date)
                    employee_segments.append(employee_DTP_007_start_end_segment)
            else:

                employee_DTP_007_start_end_segment = "DTP*007*{}~".format(employee_employment_date_format)
                employee_segments.append(employee_DTP_007_start_end_segment)

    if pd.notna(row.get('Employee Status Details-1', '')):
        employee_LE_segment = "LE*2700~"
        employee_segments.append(employee_LE_segment)
        
    return employee_segments

def process_dependents(row):
    all_dependent_segments = []
    
    for i in range(1, 10):

        if pd.notna(row[f'Dependent-{i}-Dependent Changed?(Yes/No)']):
             # INS segment
            dependent_relationship_code = str(row.get(f'Dependent-{i}-Dependent Relationship Code', '')).split("-")

            maintenance_type_code = row.get(f'Dependent-{i}-Dependent Maintenance Type Code', '')
            Dependent_maintenance_type_code = str(maintenance_type_code).split("-") if pd.notna(maintenance_type_code) else ""

            maintenance_reason_code = row.get(f'Dependent-{i}-Dependent Maintenance Reason', '')
            Dependent_maintenance_reason_code = str(maintenance_reason_code).split("-") if pd.notna(maintenance_reason_code) else ""

            benefit_status = row.get(f'Dependent-{i}-Dependent Benefit Status', '')
            Dependent_benefit_status = str(benefit_status).split("-") if pd.notna(benefit_status) else ""

            dependent_medicare_status = str(row.get(f'Dependent-{i}-Dependent Medicare Status Code', ''))
            cobra_event = row.get(f'Dependent-{i}-Dependent Cobra Event Code', '')
            Dependent_cobra_event = str(cobra_event).split("-") if pd.notna(cobra_event) else ""

            student_status_code = row.get(f'Dependent-{i}-Student Status Code', '')
            Dependent_student_status_code = str(student_status_code).split("-") if pd.notna(student_status_code) else ""
            
            dependent_date_time_period = (row.get(f'Dependent-{i}-Dependent Date Time Period', ''))
            if pd.notna(dependent_date_time_period):
                dep_date_time = datetime.strptime(dependent_date_time_period, '%m-%d-%Y').strftime('%Y%m%d')
                dependent_date_time = (dep_date_time)
            else:
                dependent_date_time = ""
            dependent_condition_code = str(row.get(f'Dependent-{i}-Dependent Y/N Condition Code', ''))
            if pd.notna(dependent_date_time_period):
                dependent_INS_segment = "INS*N*{}*{}*{}*{}*{}*{}**{}*{}*D8*{}~".format(
                    dependent_relationship_code[0],
                    Dependent_maintenance_type_code[0] if Dependent_maintenance_type_code else '',
                    Dependent_maintenance_reason_code[0] if Dependent_maintenance_reason_code else '',
                    Dependent_benefit_status[0] if Dependent_benefit_status else '',
                    dependent_medicare_status,
                    Dependent_cobra_event[0] if Dependent_cobra_event else '',
                    Dependent_student_status_code[0] if Dependent_student_status_code else '',
                    dependent_condition_code,
                    dependent_date_time
                )
            else:
                dependent_INS_segment = "INS*N*{}*{}*{}*{}*{}*{}**{}*{}~".format(
                    dependent_relationship_code[0],
                    Dependent_maintenance_type_code[0] if Dependent_maintenance_type_code else '',
                    Dependent_maintenance_reason_code[0] if Dependent_maintenance_reason_code else '',
                    Dependent_benefit_status[0] if Dependent_benefit_status else '',
                    dependent_medicare_status,
                    Dependent_cobra_event[0] if Dependent_cobra_event else '',
                    Dependent_student_status_code[0] if Dependent_student_status_code else '',
                    dependent_condition_code
                )
            all_dependent_segments.append(dependent_INS_segment)
            
            # dependent REF*0F segment
            if pd.notna([row[f'Dependent-{i}-Dependent Depend SSN Number']]):
                dependent_REF_OF_ = str(int(row[f'Dependent-{i}-Dependent Depend SSN Number'])).zfill(9)
                dependent_REF_0F_segment = "REF*0F*{}~".format(dependent_REF_OF_)
                all_dependent_segments.append(dependent_REF_0F_segment)
                #Dependent REF 17 segment............
                if pd.notna(row[f'Dependent-{i}-Dependent Client Reporting Catagory']):
                    dependent_reporting_catagory = str(row[f'Dependent-{i}-Dependent Client Reporting Catagory'])
                    dependent_REF_17_number = "REF*17*{}~".format(dependent_reporting_catagory)
                    all_dependent_segments.append(dependent_REF_17_number)
                
            # dependent REF 23 segment
            if pd.notna(row[f'Dependent-{i}-Dependent Sup-Id']):
                dependent_REF_23_sub_id = (row[f'Dependent-{i}-Dependent Sup-Id'])
                dependent_REF_23_segment = "REF*23*{}~".format(dependent_REF_23_sub_id)
                all_dependent_segments.append(dependent_REF_23_segment)
                
            #Dependent REF ABB segment............
            if pd.notna(row[f'Dependent-{i}-Dependent Personal Id Number']):
                dependent_personal_id_no = str(row[f'Dependent-{i}-Dependent Personal Id Number'])
                dependent_REF_ABB_number = "REF*ABB*{}~".format(dependent_personal_id_no)
                all_dependent_segments.append(dependent_REF_ABB_number)
            #Dependent REF ZZ segment............
            if pd.notna(row[f'Dependent-{i}-Dependent Mutually Defined']):
                dependent_mutually_defined = str(row[f'Dependent-{i}-Dependent Mutually Defined'])
                dependent_REF_ZZ_number = "REF*ZZ*{}~".format(dependent_mutually_defined)
                all_dependent_segments.append(dependent_REF_ZZ_number)
            #Dependent REF F6 segment............
            if pd.notna(row[f'Dependent-{i}-Dependent Health Insurance Claim Number']):
                dependent_health_insurance_claim_no = str(row[f'Dependent-{i}-Dependent Health Insurance Claim Number'])
                dependent_REF_F6_number = "REF*F6*{}~".format(dependent_health_insurance_claim_no)
                all_dependent_segments.append(dependent_REF_F6_number)

            
            #Dependent REF 3H segment............
            if pd.notna(row[f'Dependent-{i}-Dependent Case Number']):
                dependent_case_no = str(row[f'Dependent-{i}-Dependent Case Number'])
                dependent_REF_3H_segment = "REF*3H*{}~".format(dependent_case_no)
                all_dependent_segments.append(dependent_REF_3H_segment)
            
            #Dependent REF 4H segment............
            if pd.notna(row[f'Dependent-{i}-Dependent Personal Identification Number']):
                dependent_personal_identification_no = str(row[f'Dependent-{i}-Dependent Personal Identification Number'])
                dependent_REF_4H_segment = "REF*4H*{}~".format(dependent_personal_identification_no)
                all_dependent_segments.append(dependent_REF_4H_segment)
                    
            #Dependent REF 60 segment............
            if pd.notna(row[f'Dependent-{i}-Dependent Cross Refference Number']):
                dependent_cross_refference_no = str(row[f'Dependent-{i}-Dependent Cross Refference Number'])
                dependent_REF_60_segment = "REF*6O*{}~".format(dependent_cross_refference_no)
                all_dependent_segments.append(dependent_REF_60_segment)
            
            #Dependent REF D3 segment............
            if pd.notna(row[f'Dependent-{i}-Dependent Pharmacy Number']):
                dependent_pharmacy_no = str(row[f'Dependent-{i}-Dependent Pharmacy Number'])
                dependent_REF_D3_segment = "REF*D3*{}~".format(dependent_pharmacy_no)
                all_dependent_segments.append(dependent_REF_D3_segment)

            #Dependent REF P5 segment............
            if pd.notna(row[f'Dependent-{i}-Dependent Positon Code']):
                dependent_position_code = str(row[f'Dependent-{i}-Dependent Positon Code'])
                dependent_REF_P5_segment = "REF*P5*{}~".format(dependent_position_code)
                all_dependent_segments.append(dependent_REF_P5_segment)

            #Dependent REF Q4 segment............
            if pd.notna(row[f'Dependent-{i}-Dependent Prior Identification Number']):
                dependent_prior_id_no = str(row[f'Dependent-{i}-Dependent Prior Identification Number'])
                dependent_REF_Q4_segment = "REF*Q4*{}~".format(dependent_prior_id_no)
                all_dependent_segments.append(dependent_REF_Q4_segment)
            
            #Dependent REF QQ segment............
            if pd.notna(row[f'Dependent-{i}-Dependent Unit Number']):
                dependent_unit_no = str(row[f'Dependent-{i}-Dependent Unit Number'])
                dependent_REF_QQ_segment = "REF*QQ*{}~".format(dependent_unit_no)
                all_dependent_segments.append(dependent_REF_QQ_segment)

            Dependent_medicare_received_date = str(row[f'Dependent-{i}-Dependent Medicare Received Date'])
            if pd.notna (Dependent_medicare_received_date) and Dependent_medicare_received_date != 'nan':
                emp_medicare_received_date = datetime.strptime(Dependent_medicare_received_date, '%m-%d-%Y').strftime('%Y%m%d')
                Dependent_050_segment = "DTP*050*D8*{}~".format(emp_medicare_received_date)
                all_dependent_segments.append(Dependent_050_segment)

            Dependent_retirement_date = str(row[f'Dependent-{i}-Dependent Retirement Date'])
            if pd.notna (Dependent_retirement_date) and Dependent_retirement_date != 'nan':
                emp_retirement_date = datetime.strptime(Dependent_retirement_date, '%m-%d-%Y').strftime('%Y%m%d')
                Dependent_286_segment = "DTP*286*D8*{}~".format(emp_retirement_date)
                all_dependent_segments.append(Dependent_286_segment)

            Dependent_enrollment_signature_signature_date = str(row[f'Dependent-{i}-Dependent Enrollment Signature Date'])
            if pd.notna (Dependent_enrollment_signature_signature_date) and Dependent_enrollment_signature_signature_date != 'nan':
                emp_enrollment_signature_signature_date = datetime.strptime(Dependent_enrollment_signature_signature_date, '%m-%d-%Y').strftime('%Y%m%d')
                Dependent_300_segment = "DTP*300*D8*{}~".format(emp_enrollment_signature_signature_date)
                all_dependent_segments.append(Dependent_300_segment)

            #Dependent QE segment.............
            Dependent_QE_date = str(row[f'Dependent-{i}-Dependent Employment QE Date'])
            if pd.notna (Dependent_QE_date) and Dependent_QE_date != 'nan':
                emp_medicare_QE_date = datetime.strptime(Dependent_QE_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_301_segment = "DTP*301*D8*{}~".format(emp_medicare_QE_date)
                all_dependent_segments.append(dtp_301_segment)
        
            Dependent_maintenance_effective_date = str(row[f'Dependent-{i}-Dependent Maintenance Effective Date'])
            if pd.notna (Dependent_maintenance_effective_date) and Dependent_maintenance_effective_date != 'nan':
                emp_maintenance_effective_date = datetime.strptime(Dependent_maintenance_effective_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_303_segment = "DTP*303*D8*{}~".format(emp_maintenance_effective_date)
                all_dependent_segments.append(dtp_303_segment)

            dependent_hiring_date = str(row[f'Dependent-{i}-Dependent Hiring Date'])
            if pd.notna(dependent_hiring_date) and dependent_hiring_date != 'nan':
                dep_hiring_date = datetime.strptime(dependent_hiring_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_336_segment = "DTP*336*D8*{}~".format(dep_hiring_date)
                all_dependent_segments.append(dtp_336_segment)


            dependent_end_date = str(row[f'Dependent-{i}-Dependent Employment End Date'])
            if pd.notna(dependent_end_date) and dependent_end_date != 'nan':
                dep_end_date = datetime.strptime(dependent_end_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_337_segment = "DTP*337*D8*{}~".format(dep_end_date)
                all_dependent_segments.append(dtp_337_segment)
            

            
            if pd.notna(row[f'Dependent-{i}-Dependent Medicare Start Date1']) and pd.isna(row[f'Dependent-{i}-Dependent Medicare Start Date2']) and pd.isna(row[f'Dependent-{i}-Dependent Medicare End Date1']) and pd.isna(row[f'Dependent-{i}-Dependent Medicare End Date2']):
                employment_medicare_start_date = str(row[f'Dependent-{i}-Dependent Medicare Start Date1'])
                emp_medicare_start_date = datetime.strptime(employment_medicare_start_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_338_segment = "DTP*338*D8*{}~".format(emp_medicare_start_date)
                all_dependent_segments.append(dtp_338_segment)
                
            
            
            if pd.notna(row[f'Dependent-{i}-Dependent Medicare Start Date1']) and pd.notna(row[f'Dependent-{i}-Dependent Medicare Start Date2']) and pd.isna(row[f'Dependent-{i}-Dependent Medicare End Date1']) and pd.isna(row[f'Dependent-{i}-Dependent Medicare End Date2']):
                employment_medicare_start_date = str(row[f'Dependent-{i}-Dependent Medicare Start Date1'])
                emp_medicare_start_date = datetime.strptime(employment_medicare_start_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_338_segment = "DTP*338*D8*{}~".format(emp_medicare_start_date)
                all_dependent_segments.append(dtp_338_segment)
                
                employment_medicare_start_date2 = str(row[f'Dependent-{i}-Dependent Medicare Start Date2'])
                emp_medicare_start_date2 = datetime.strptime(employment_medicare_start_date2, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_338_segment2 = "DTP*338*D8*{}~".format(emp_medicare_start_date2)
                all_dependent_segments.append(dtp_338_segment2)

            if pd.notna(row[f'Dependent-{i}-Dependent Medicare Start Date1']) and pd.notna(row[f'Dependent-{i}-Dependent Medicare Start Date2']) and pd.notna(row[f'Dependent-{i}-Dependent Medicare End Date1']) and pd.isna(row[f'Dependent-{i}-Dependent Medicare End Date2']):
                employment_medicare_start_date = str(row[f'Dependent-{i}-Dependent Medicare Start Date1'])
                emp_medicare_start_date = datetime.strptime(employment_medicare_start_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_338_segment = "DTP*338*D8*{}~".format(emp_medicare_start_date)
                all_dependent_segments.append(dtp_338_segment)
                
                employment_medicare_start_date2 = str(row[f'Dependent-{i}-Dependent Medicare Start Date2'])
                emp_medicare_start_date2 = datetime.strptime(employment_medicare_start_date2, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_338_segment2 = "DTP*338*D8*{}~".format(emp_medicare_start_date2)
                all_dependent_segments.append(dtp_338_segment2)

                employment_medicare_end_date = str(row[f'Dependent-{i}-Dependent Medicare End Date1'])
                emp_medicare_end_date = datetime.strptime(employment_medicare_end_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_339_segment = "DTP*339*D8*{}~".format(emp_medicare_end_date)
                all_dependent_segments.append(dtp_339_segment)

            if pd.notna(row[f'Dependent-{i}-Dependent Medicare Start Date1']) and pd.notna(row[f'Dependent-{i}-Dependent Medicare Start Date2']) and pd.notna(row[f'Dependent-{i}-Dependent Medicare End Date1']) and pd.notna(row[f'Dependent-{i}-Dependent Medicare End Date2']):
                employment_medicare_start_date = str(row[f'Dependent-{i}-Dependent Medicare Start Date1'])
                emp_medicare_start_date = datetime.strptime(employment_medicare_start_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_338_segment = "DTP*338*D8*{}~".format(emp_medicare_start_date)
                all_dependent_segments.append(dtp_338_segment)

                employment_medicare_end_date = str(row[f'Dependent-{i}-Dependent Medicare End Date1'])
                emp_medicare_end_date = datetime.strptime(employment_medicare_end_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_339_segment = "DTP*339*D8*{}~".format(emp_medicare_end_date)
                all_dependent_segments.append(dtp_339_segment)
                
                employment_medicare_start_date2 = str(row[f'Dependent-{i}-Dependent Medicare Start Date2'])
                emp_medicare_start_date2 = datetime.strptime(employment_medicare_start_date2, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_338_segment2 = "DTP*338*D8*{}~".format(emp_medicare_start_date2)
                all_dependent_segments.append(dtp_338_segment2)

                employment_medicare_end_date2 = str(row[f'Dependent-{i}-Dependent Medicare End Date2'])
                emp_medicare_end_date2 = datetime.strptime(employment_medicare_end_date2, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_339_segment2 = "DTP*339*D8*{}~".format(emp_medicare_end_date2)
                all_dependent_segments.append(dtp_339_segment2)  
            
            if pd.notna(row[f'Dependent-{i}-Dependent Medicare Start Date1']) and pd.isna(row[f'Dependent-{i}-Dependent Medicare Start Date2']) and pd.notna(row[f'Dependent-{i}-Dependent Medicare End Date1']) and pd.isna(row[f'Dependent-{i}-Dependent Medicare End Date2']):
                employment_medicare_start_date = str(row[f'Dependent-{i}-Dependent Medicare Start Date1'])
                emp_medicare_start_date = datetime.strptime(employment_medicare_start_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_338_segment = "DTP*338*D8*{}~".format(emp_medicare_start_date)
                all_dependent_segments.append(dtp_338_segment)

                employment_medicare_end_date = str(row[f'Dependent-{i}-Dependent Medicare End Date1'])
                emp_medicare_end_date = datetime.strptime(employment_medicare_end_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_339_segment = "DTP*339*D8*{}~".format(emp_medicare_end_date)
                all_dependent_segments.append(dtp_339_segment)
                
            Dependent_education_begin_date = str(row[f'Dependent-{i}-Dependent Education Begin Date'])
            if pd.notna (Dependent_education_begin_date) and Dependent_education_begin_date !='nan':
                emp_education_begin_date = datetime.strptime(Dependent_education_begin_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_350_segment = "DTP*350*D8*{}~".format(emp_education_begin_date)
                all_dependent_segments.append(dtp_350_segment)   
            
            Dependent_education_end_date = str(row[f'Dependent-{i}-Dependent Education End Date'])
            if pd.notna (Dependent_education_end_date) and Dependent_education_end_date !='nan':
                emp_education_end_date = datetime.strptime(Dependent_education_end_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_351_segment = "DTP*351*D8*{}~".format(emp_education_end_date)
                all_dependent_segments.append(dtp_351_segment)

            Dependent_eligibility_begin_date = str(row[f'Dependent-{i}-Dependent Eligibility Begin Date'])
            if pd.notna (Dependent_eligibility_begin_date) and Dependent_eligibility_begin_date !='nan':
                emp_eligibility_begin_date = datetime.strptime(Dependent_eligibility_begin_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_356_segment = "DTP*356*D8*{}~".format(emp_eligibility_begin_date)
                all_dependent_segments.append(dtp_356_segment)
            
            Dependent_eligibility_end_date = str(row[f'Dependent-{i}-Dependent Eligibility End Date'])
            if pd.notna (Dependent_eligibility_end_date) and Dependent_eligibility_end_date !='nan':
                emp_eligibility_end_date = datetime.strptime(Dependent_eligibility_end_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_357_segment = "DTP*357*D8*{}~".format(emp_eligibility_end_date)
                all_dependent_segments.append(dtp_357_segment)
            
            employment_adjusted_service_date = str(row[f'Dependent-{i}-Dependent Adjusted Service Date'])
            if pd.notna (employment_adjusted_service_date) and employment_adjusted_service_date !='nan':
                emp_adjusted_service_date = datetime.strptime(employment_adjusted_service_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_383_segment = "DTP*383*D8*{}~".format(emp_adjusted_service_date)
                all_dependent_segments.append(dtp_383_segment)

            Dependent_credited_service_begin_date = str(row[f'Dependent-{i}-Dependent Credited Service Begin Date'])
            if pd.notna (Dependent_credited_service_begin_date) and Dependent_credited_service_begin_date !='nan':
                empl_credited_service_begin_date = datetime.strptime(Dependent_credited_service_begin_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_385_segment = "DTP*385*D8*{}~".format(empl_credited_service_begin_date)
                all_dependent_segments.append(dtp_385_segment)

            Dependent_credited_service_end_date = str(row[f'Dependent-{i}-Dependent Credited Service End Date'])
            if pd.notna (Dependent_credited_service_end_date) and Dependent_credited_service_end_date !='nan':
                emp_credited_service_end_date = datetime.strptime(Dependent_credited_service_end_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_386_segment = "DTP*386*D8*{}~".format(emp_credited_service_end_date)
                all_dependent_segments.append(dtp_386_segment)

            Dependent_plan_par_date = str(row[f'Dependent-{i}-Dependent Plan Participation Suspension Date'])
            if pd.notna (Dependent_plan_par_date) and Dependent_plan_par_date !='nan':
                emp_plan_par_date = datetime.strptime(Dependent_plan_par_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_393_segment = "DTP*393*D8*{}~".format(emp_plan_par_date)
                all_dependent_segments.append(dtp_393_segment)

            Dependent_rehire_date = str(row[f'Dependent-{i}-Dependent Rehire Date'])
            if pd.notna (Dependent_rehire_date) and Dependent_rehire_date !='nan':
                empl_rehire_date = datetime.strptime(Dependent_rehire_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_394_segment = "DTP*394*D8*{}~".format(empl_rehire_date)
                all_dependent_segments.append(dtp_394_segment)

            Dependent_medicaid_begin_date = str(row[f'Dependent-{i}-Dependent Medicaid Begin Date'])
            if pd.notna (Dependent_medicaid_begin_date) and Dependent_medicaid_begin_date !='nan':
                emp_medicaid_begin_date = datetime.strptime(Dependent_medicaid_begin_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_473_segment = "DTP*473*D8*{}~".format(emp_medicaid_begin_date)
                all_dependent_segments.append(dtp_473_segment)
            
            Dependent_medicaid_end_date = str(row[f'Dependent-{i}-Dependent Medicaid End Date'])
            if pd.notna (Dependent_medicaid_end_date) and Dependent_medicaid_end_date !='nan':
                emp_medicaid_end_date = datetime.strptime(Dependent_medicaid_end_date, '%m-%d-%Y').strftime('%Y%m%d')
                dtp_474_segment = "DTP*474*D8*{}~".format(emp_medicaid_end_date)
                all_dependent_segments.append(dtp_474_segment)

            #dependent NM1 segment ................
            if pd.notna(row[f'Dependent-{i}-Dependent SSN Number']):
                dependent_ssn_no = str(int(row[f'Dependent-{i}-Dependent SSN Number'])).zfill(9)
            else:
                dependent_ssn_no = ""
                
            if pd.notna(row[f'Dependent-{i}-Dependent Last Name']):
                dependent_last_name = (row[f'Dependent-{i}-Dependent Last Name'])
            else:
                dependent_last_name = ""

            if pd.notna(row[f'Dependent-{i}-Dependent First Name']):
                dependent_first_name = (row[f'Dependent-{i}-Dependent First Name'])
            else:
                dependent_first_name = ""
                
            if pd.notna(row[f'Dependent-{i}-Dependent Middle Name']):
                dependent_middle_name = (row[f'Dependent-{i}-Dependent Middle Name'])
            else:
                dependent_middle_name = ""

            if pd.notna(row[f'Dependent-{i}-Dependent Prefix Name']):
                dependent_prefix_name = (row[f'Dependent-{i}-Dependent Prefix Name'])
            else:
                dependent_prefix_name = ""
                
            if pd.notna(row[f'Dependent-{i}-Dependent Suffix Name']):
                dependent_suffix_name = (row[f'Dependent-{i}-Dependent Suffix Name'])
            else:
                dependent_suffix_name = ""

            dependent_changed = str(row[f'Dependent-{i}-Dependent Changed?(Yes/No)'])
            dependent_changes = dependent_changed.split("-")
                
            if pd.notna(row[f'Dependent-{i}-Dependent Id Code Quatifier']):
                dependent_id_code = str(int(row[f'Dependent-{i}-Dependent Id Code Quatifier']))
            else:
                dependent_id_code = ""

            if(dependent_first_name):
                if(dependent_id_code):
                    
                    dependent_NMA1_segment = "NM1*{}*1*{}*{}*{}*{}*{}*{}*{}~".format(
                        dependent_changes[0],
                        dependent_last_name if dependent_last_name else '',
                        dependent_first_name if dependent_first_name else '',
                        dependent_middle_name if dependent_middle_name else '',
                        dependent_prefix_name if dependent_prefix_name else '',
                        dependent_suffix_name if dependent_suffix_name else '',
                        dependent_id_code if dependent_id_code else '',
                        dependent_ssn_no if dependent_ssn_no else ''
                    )
                elif(dependent_last_name and dependent_first_name and dependent_middle_name and dependent_prefix_name and dependent_suffix_name):
                    dependent_NMA1_segment = "NM1*{}*1*{}*{}*{}*{}*{}~".format(
                        dependent_changes[0],
                        dependent_last_name if dependent_last_name else '',
                        dependent_first_name if dependent_first_name else '',
                        dependent_middle_name if dependent_middle_name else '',
                        dependent_prefix_name if dependent_prefix_name else '',
                        dependent_suffix_name if dependent_suffix_name else ''
                    )
                elif(dependent_last_name and dependent_first_name and dependent_middle_name and dependent_suffix_name):
                    dependent_NMA1_segment = "NM1*{}*1*{}*{}*{}**{}~".format(
                        dependent_changes[0],
                        dependent_last_name if dependent_last_name else '',
                        dependent_first_name if dependent_first_name else '',
                        dependent_middle_name if dependent_middle_name else '',

                        dependent_suffix_name if dependent_suffix_name else ''
                    )
                elif(dependent_last_name and dependent_first_name and dependent_suffix_name):
                    dependent_NMA1_segment = "NM1*{}*1*{}*{}***{}~".format(
                        dependent_changes[0],
                        dependent_last_name if dependent_last_name else '',
                        dependent_first_name if dependent_first_name else '',
                        dependent_suffix_name if dependent_suffix_name else ''
                    )
                elif(dependent_last_name and dependent_first_name and dependent_middle_name and dependent_prefix_name):
                    dependent_NMA1_segment = "NM1*{}*1*{}*{}*{}*{}~".format(
                        dependent_changes[0],
                        dependent_last_name if dependent_last_name else '',
                        dependent_first_name if dependent_first_name else '',
                        dependent_middle_name if dependent_middle_name else '',
                        dependent_prefix_name if dependent_prefix_name else ''
                    )
                elif(dependent_last_name and dependent_first_name and dependent_middle_name):
                    dependent_NMA1_segment = "NM1*{}*1*{}*{}*{}~".format(
                        dependent_changes[0],
                        dependent_last_name if dependent_last_name else '',
                        dependent_first_name if dependent_first_name else '',
                        dependent_middle_name if dependent_middle_name else ''
                    )
                elif(dependent_last_name and dependent_first_name):
                    dependent_NMA1_segment = "NM1*{}*1*{}*{}~".format(
                        dependent_changes[0],
                        dependent_last_name if dependent_last_name else '',
                        dependent_first_name if dependent_first_name else ''

                    )
                all_dependent_segments.append(dependent_NMA1_segment)
  
            #dependent PER segment...................
            if pd.notna(row[f'Dependent-{i}-Dependent Contact1']):
                dependent_contact1 = '*' + '*'.join(row[f'Dependent-{i}-Dependent Contact1'].split(":"))
            else:
                dependent_contact1 = ""

            if pd.notna(row[f'Dependent-{i}-Dependent Contact2']):
                dependent_contact2 = '*' + '*'.join(row[f'Dependent-{i}-Dependent Contact2'].split(":"))
            else:
                dependent_contact2 = ""

            if pd.notna(row[f"Dependent-{i}-Dependent Contact3"]):
                dependent_contact3 = '*' + '*'.join(row[f'Dependent-{i}-Dependent Contact3'].split(":"))
            else:
                dependent_contact3 = ""

            if pd.notna(row[f"Dependent-{i}-Dependent Contact1"]):
                dependent_per_segment = "PER*IP*{}{}{}{}{}{}~".format(
                    dependent_contact1,
                    dependent_contact2,
                    dependent_contact3,
                    "",
                    "",
                    ""
                )
                all_dependent_segments.append(dependent_per_segment)

            # Dependent Address Details
            if pd.notna (row[f"Dependent-{i}-Dependent Address"]):
                dependent_address_components = (row[f"Dependent-{i}-Dependent Address"]).split(',')

                dep_address1 = dependent_address_components[0]
                dep_address2 = dependent_address_components[1]

                # Split address1 into address positions
                n3_address = dep_address1.split("_")
                street_address_1 = n3_address[0]
                street_address_2 = ""
                if len(n3_address)==2:
                    street_address_2 = n3_address[1]
                dep_n3_segment = "N3*{}{}~".format(
                    street_address_1, 
                    "*" + street_address_2 if street_address_2 else ''
                )
                all_dependent_segments.append(dep_n3_segment)

                # Split address2 into city, state, and zip code
                n4_address = dep_address2.split('/')
                dep_city = n4_address[0]
                dep_state = n4_address[1]
                dep_zip_code = n4_address[2]
                dep_country_code = ""
                if len(n4_address) == 4:
                    dep_country_code = n4_address[3]
                
                n4_segment = "N4*{}*{}*{}{}~".format(
                    dep_city,
                    dep_state,
                    dep_zip_code,
                    "*" + dep_country_code if dep_country_code else ""
                )
                all_dependent_segments.append(n4_segment)

            # dependent DMG segment...........
            dependent_date_of_birth_raw = row.get(f"Dependent-{i}-Dependent DOB")
            if pd.notna(dependent_date_of_birth_raw):
                dependent_date_of_birth = datetime.strptime(str(dependent_date_of_birth_raw), '%m-%d-%Y').strftime('%Y%m%d')
                dependent_gender = row.get(f"Dependent-{i}-Dependent Gender", '')
                dependent_marital_status = row.get(f"Dependent-{i}-Dependent Merital Status", '')

                marital_status_str = "*" + str(dependent_marital_status) if pd.notna(dependent_marital_status) else ''
                dependent_dmg_segment = "DMG*D8*{}*{}{}~".format(
                    dependent_date_of_birth,
                    dependent_gender,
                    marital_status_str
                )
                all_dependent_segments.append(dependent_dmg_segment)

            #dependent 70 segment...........
            if pd.notna(row[f'Dependent-{i}-Dependent Old SSN Number']):
                dependent_old_ssn_no = str(int(row[f'Dependent-{i}-Dependent Old SSN Number'])).zfill(9)
            else:
                dependent_old_ssn_no = ""
                
            if pd.notna(row[f'Dependent-{i}-Dependent Old Last Name']):
                dependent_old_last_name = (row[f'Dependent-{i}-Dependent Old Last Name'])
            else:
                dependent_old_last_name = ""

            if pd.notna(row[f'Dependent-{i}-Dependent Old First Name']):
                dependent_old_first_name = (row[f'Dependent-{i}-Dependent Old First Name'])
            else:
                dependent_old_first_name = ""
                
            if pd.notna(row[f'Dependent-{i}-Dependent Old Middle Name']):
                dependent_old_middle_name = (row[f'Dependent-{i}-Dependent Old Middle Name'])
            else:
                dependent_old_middle_name = ""

            if pd.notna(row[f'Dependent-{i}-Dependent Old Prefix Name']):
                dependent_old_prefix_name = (row[f'Dependent-{i}-Dependent Old Prefix Name'])
            else:
                dependent_old_prefix_name = ""
                
            if pd.notna(row[f'Dependent-{i}-Dependent Old Suffix Name']):
                dependent_old_suffix_name = (row[f'Dependent-{i}-Dependent Old Suffix Name'])
            else:
                dependent_old_suffix_name = ""

            if pd.notna(row[f'Dependent-{i}-Dependent Old Id Code Quatifier']):
                dependent_old_id_code = str(int(row[f'Dependent-{i}-Dependent Old Id Code Quatifier']))
            else:
                dependent_old_id_code = ""

            if(dependent_old_first_name):
                if(dependent_old_id_code): 
                    dependent_old_NMA1_segment = "NM1*70*1*{}*{}*{}*{}*{}*{}*{}~".format(
                        dependent_old_last_name if dependent_old_last_name else '',
                        dependent_old_first_name if dependent_old_first_name else '',
                        dependent_old_middle_name if dependent_old_middle_name else '',
                        dependent_old_prefix_name if dependent_old_prefix_name else '',
                        dependent_old_suffix_name if dependent_old_suffix_name else '',
                        dependent_old_id_code if dependent_old_id_code else '',
                        dependent_old_ssn_no if dependent_old_ssn_no else ''
                    )
                elif(dependent_old_last_name and dependent_old_first_name and dependent_old_middle_name and dependent_old_prefix_name and dependent_old_suffix_name):
                    dependent_old_NMA1_segment = "NM1*70*1*{}*{}*{}*{}*{}~".format(
                        dependent_old_last_name if dependent_old_last_name else '',
                        dependent_old_first_name if dependent_old_first_name else '',
                        dependent_old_middle_name if dependent_old_middle_name else '',
                        dependent_old_prefix_name if dependent_old_prefix_name else '',
                        dependent_old_suffix_name if dependent_old_suffix_name else ''
                    )
                elif(dependent_old_last_name and dependent_old_first_name and dependent_old_middle_name and dependent_old_suffix_name):
                    dependent_old_NMA1_segment = "NM1*70*1*{}*{}*{}**{}~".format(
                        dependent_old_last_name if dependent_old_last_name else '',
                        dependent_old_first_name if dependent_old_first_name else '',
                        dependent_old_middle_name if dependent_old_middle_name else '',

                        dependent_old_suffix_name if dependent_old_suffix_name else ''
                    )
                elif(dependent_old_last_name and dependent_old_first_name and dependent_old_middle_name and dependent_old_prefix_name):
                    dependent_old_NMA1_segment = "NM1*70*1*{}*{}*{}*{}~".format(
                        dependent_old_last_name if dependent_old_last_name else '',
                        dependent_old_first_name if dependent_old_first_name else '',
                        dependent_old_middle_name if dependent_old_middle_name else '',
                        dependent_old_prefix_name if dependent_old_prefix_name else ''
                    )
                elif(dependent_old_last_name and dependent_old_first_name and dependent_old_middle_name):
                    dependent_old_NMA1_segment = "NM1*70*1*{}*{}*{}~".format(
                        dependent_old_last_name if dependent_old_last_name else '',
                        dependent_old_first_name if dependent_old_first_name else '',
                        dependent_old_middle_name if dependent_old_middle_name else ''
                    )
                elif(dependent_old_last_name and dependent_old_first_name):
                    dependent_old_NMA1_segment = "NM1*70*1*{}*{}~".format(
                        dependent_old_last_name if dependent_old_last_name else '',
                        dependent_old_first_name if dependent_old_first_name else ''

                    )
                all_dependent_segments.append(dependent_old_NMA1_segment)
            
            #Dependent old dob/gender/Merital Status............  
            dep_old_dob = ""  
            if pd.notna(row[f'Dependent-{i}-Dependent Old DOB']) and (row[f'Dependent-{i}-Dependent Old DOB']) != 'nan':
                dependent_old_date_of_birth = str(row[f'Dependent-{i}-Dependent Old DOB'])
                dep_old_dob = datetime.strptime(dependent_old_date_of_birth, '%m-%d-%Y').strftime('%Y%m%d')
                    
            if pd.notna(row[f'Dependent-{i}-Dependent Old Gender']) and (row[f'Dependent-{i}-Dependent Old Gender']) != 'nan':
                dependent_old_gender = str(row[f'Dependent-{i}-Dependent Old Gender'])
                  
            if pd.notna(row[f'Dependent-{i}-Dependent Old Merital Status']) and (row[f'Dependent-{i}-Dependent Old Merital Status']) != 'nan':
                dependent_old_merital_status = str(row[f'Dependent-{i}-Dependent Old Merital Status'])
                   
            if pd.notna(row[f'Dependent-{i}-Dependent Old DOB']):
                dep_old_dmg_segment = "DMG*D8*{}*{}{}~".format(
                    dep_old_dob,
                    dependent_old_gender if 'dependent_old_gender' in locals() else '',  
                    "*" + dependent_old_merital_status if 'dependent_old_merital_status' in locals() else ''  
                )
                all_dependent_segments.append(dep_old_dmg_segment)
            
            #Dependent 31 segment...........
            dependent_old_address = str(row[f'Dependent-{i}-Dependent Old Address'])
            if pd.notna (dependent_old_address) and dependent_old_address !='nan':
                dep_NM1_31_segment = "NM1*31*1~"
                all_dependent_segments.append(dep_NM1_31_segment)

                dep_old_address = dependent_old_address.split(",")
                dep_31_n3_old_address = dep_old_address[0]
                dep_31_n4_old_address = dep_old_address[1]
                    
                dep_old_n3_address = dep_31_n3_old_address.split("_")
                dep_old_street_address_1 = dep_old_n3_address[0]
                dep_old_street_address_2 = ""
                if len(dep_old_n3_address)==2:
                    dep_old_street_address_2 = dep_old_n3_address[1]
                
                dep_NM1_31_N3_segment = "N3*{}{}~".format(
                    dep_old_street_address_1,
                    "*" + dep_old_street_address_2 if dep_old_street_address_2 else ''
                )
                all_dependent_segments.append(dep_NM1_31_N3_segment)

                dep_n4_old_address = dep_31_n4_old_address.split('/')

                dep_old_city = dep_n4_old_address[0]
                dep_old_state = dep_n4_old_address[1]
                dep_old_zip_code = dep_n4_old_address[2]
                dep_old_country_code = ""
                if len(dep_n4_old_address) == 4:
                    dep_old_country_code = dep_n4_old_address[3]
                dep_NM1_31_N4_segment = "N4*{}*{}*{}{}~".format(
                    dep_old_city, 
                    dep_old_state, 
                    dep_old_zip_code,
                    "*" + dep_old_country_code if dep_old_country_code else ""
                )
                all_dependent_segments.append(dep_NM1_31_N4_segment)

            #dependent HD(health) segment ..................     
            for j in range(1, 4):
                dep_insurance_plan = row.get(f'Dependent-{i}-Dependent Medicare Plan Maintenance-{j}', '')
                dependent_insurance_plan = dep_insurance_plan.split("-") if pd.notna(dep_insurance_plan) else [''] * 2
                
                dep_insurance_code = row.get(f'Dependent-{i}-Dependent Insurance Line Code-{j}', '')
                dep_plan_description = row.get(f'Dependent-{i}-Dependent Plan Description-{j}', '')
                dep_coverage_level_code = row.get(f'Dependent-{i}-Dependent Coverage Lavel Code-{j}', '')
                
                if pd.notna(dep_insurance_plan):
                    dep_hd_segment = "HD*{}**{}*{}*{}~".format(
                        dependent_insurance_plan[1],
                        dep_insurance_code,
                        dep_plan_description,
                        dep_coverage_level_code
                    )
                    all_dependent_segments.append(dep_hd_segment)

                dependent_benefit_begin = str(row[f'Dependent-{i}-Dependent Benefit Begin-{j}'])
                if pd.notna(dependent_benefit_begin) and dependent_benefit_begin != 'nan':
                    dep_benefit_begin_date = datetime.strptime(dependent_benefit_begin, '%m-%d-%Y').strftime('%Y%m%d')
                    dtp_348_segment = "DTP*348*D8*{}~".format(dep_benefit_begin_date)
                    all_dependent_segments.append(dtp_348_segment)
                
                dependent_benefit_end = str(row[f'Dependent-{i}-Dependent Benefit End-{j}'])
                if pd.notna(dependent_benefit_end) and dependent_benefit_end != 'nan':
                    dep_benefit_end_date = datetime.strptime(dependent_benefit_end, '%m-%d-%Y').strftime('%Y%m%d')
                    dtp_349_segment = "DTP*349*D8*{}~".format(dep_benefit_end_date)
                    all_dependent_segments.append(dtp_349_segment)

                dependent_non_smoker_discount = str(row[f'Dependent-{i}-Dependent Non Smoker Discount-{j}'])
                if pd.notna(dependent_non_smoker_discount) and dependent_non_smoker_discount != 'nan': 
                    dep_ref_segment = "REF*ZZ*{}~".format(dependent_non_smoker_discount[0])
                    all_dependent_segments.append(dep_ref_segment)
            
            #Dependent LS*2700~ segment...............
            if pd.notna (row.get(f'Dependent-{i}-Dependent Status Details-1', '')):
                dependent_LS_segment = "LS*2700~"  
                all_dependent_segments.append(dependent_LS_segment)          
            
            for k in range(1, 5):
                dep_status_details = row.get(f'Dependent-{i}-Dependent Status Details-{k}', '')            
                if pd.notna(dep_status_details) :    
                    dependent_LX_segment = f"LX*{k}~"
                    all_dependent_segments.append(dependent_LX_segment)

                    dependent_n1_75_segment = "N1*75*{}~".format(dep_status_details)
                    all_dependent_segments.append(dependent_n1_75_segment)
                    dep_employment_status = row.get(f'Dependent-{i}-Dependent Employment Status-{k}', '')
                    dependent_ZZ_segment = "REF*ZZ*{}~".format(dep_employment_status)
                    all_dependent_segments.append(dependent_ZZ_segment)

                    dependent_employment_start_end_date = row.get(f'Dependent-{i}-Dependent Employment Status Start/End Date-{k}', '')
                    dependent_employment_date_format = row.get(f'Dependent-{i}-Dependent Employment Status Date Format-{k}', '')
                    if pd.notna(dependent_employment_start_end_date ): 
                                                                
                        dependent_employment_start_end_date = dependent_employment_start_end_date.replace('.', '').strip()
                        dep_employment_start_end_date = [date.strip() for date in dependent_employment_start_end_date.split("-")]

                        if len(dep_employment_start_end_date) == 1:
                            dependent_emp_start_date = datetime.strptime(dep_employment_start_end_date[0], '%m%d%Y').strftime('%Y%m%d')
                            
                            dependent_DTP_007_start_end_segment = "DTP*007*{}*{}~".format(dependent_employment_date_format, dependent_emp_start_date)
                            all_dependent_segments.append(dependent_DTP_007_start_end_segment)

                        elif len(dep_employment_start_end_date) == 2:
                            dependent_emp_start_date = datetime.strptime(dep_employment_start_end_date[0], '%m%d%Y').strftime('%Y%m%d')
                            dependent_emp_end_date = datetime.strptime(dep_employment_start_end_date[1], '%m%d%Y').strftime('%Y%m%d')

                            dependent_DTP_007_start_end_segment = "DTP*007*{}*{}-{}~".format(dependent_employment_date_format, dependent_emp_start_date, dependent_emp_end_date)
                            all_dependent_segments.append(dependent_DTP_007_start_end_segment)
                    else:
                        dependent_DTP_007_start_end_segment = "DTP*007*{}~".format(dependent_employment_date_format)
                        all_dependent_segments.append(dependent_DTP_007_start_end_segment)

            if pd.notna (row.get(f'Dependent-{i}-Dependent Status Details-1', '')):
                dependent_LS_segment = "LE*2700~"  
                all_dependent_segments.append(dependent_LS_segment)  

    return all_dependent_segments

# Example usage:
input_file_path = "C:\\Users\\USER\\Desktop\\ITEDUIM Project\\edi_to_excel\\ITEDUIM20240409.xlsx"
output_file = "C:\\Users\\USER\\Desktop\\ITEDUIM Project\\excel_to_edi\\edi.txt"
edi_output = process_file(input_file_path)

# Write EDI output to a file
with open(output_file, "w") as f:
    f.write(edi_output)
