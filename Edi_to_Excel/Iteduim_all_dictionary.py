Maintenance_Reason_Code = {
    '01': 'Divorce',
    '02': 'Birth',
    '03': 'Death',
    '04': 'Retirement',
    '05': 'Adoption',
    '06': 'Strike',
    '07': 'Termination of Benefits',
    '08': 'Termination of Employment',
    '09': 'Consolidation Omnibus Budget Reconciliation Act (COBRA)',
    '10': 'Consolidation Omnibus Budget Reconciliation Act (COBRA) Premium Paid',
    '11': 'Surviving Spouse',
    '14': 'Voluntary Withdrawal',
    '15': 'Primary Care Provider(PCP) Change',
    '16': 'Quit',
    '17': 'Fired',
    '18': 'Suspended',
    '20': 'Active',
    '21': 'Disability',
    '22': 'Plan Change',
    '25': 'Change in Identifying Data Elements',
    '26': 'Declined Coverage',
    '27': 'Pre-Enrollment',
    '28': 'Initial Enrollment',
    '29': 'Benefit Selection',
    '31': 'Legal Separation',
    '32': 'Marriage',
    '33': 'Personnel Data',
    '37': 'Leave of Absence with Benefits',
    '38': 'Leave of Absence without Benefits',
    '39': 'Lay off with Benefits',
    '40': 'Lay off without Benefits',
    '41': 'Re-enrollment',
    '43': 'Change of Location',
    '59': 'Non Payment',
    'AA': 'Dissatisfaction with Office Staff',
    'AB': 'Dissatisfaction with Medical Care/Service Rendered',
    'AC': 'Inconvenient Office Location',
    'AD': 'Dissatisfaction with Office Hours',
    'AE': 'Unable to Schedule Appointments in a Timely Manner',
    'AF': 'Dissatisfaction with Physician Referral Policy',
    'AG': 'Less Respect AND Attention Time Given than To Other Patients',
    'AH': 'Patient Moved to a New Location',
    'AI': 'No Reason Given',
    'AJ': 'Appointment Times Not Met in a Timely Manner',
    'AL': 'Algorithm Assigned Benefit Selection',
    'EC': 'Mamber Benefit Selection',
    'XN': 'Notification Only',
    'XT': 'Transfer'
}

Member_Maintenance_Type_Code ={
    '001': 'Change',
    '021': 'Addition',
    '024': 'Cancellation/Termination',
    '025': 'Reinstatement',
    '030': 'Audit/Compare'
}


# Medicare_Status_Code ={
#     'A': 'Medicare Part A',
#     'B': 'Medicare Part B',
#     'C': 'Meicare Part A and B',
#     'D': 'Medicare',
#     'E': 'No Medicare'
# }

Cobra_Event_Code = {
    '1': 'Termination of Employment',
    '2': 'Reduction of work hours',
    '3': 'Medicare',
    '4': 'Death',
    '5': 'Divorce',
    '6': 'Separation',
    '7': 'Ineligible Child',
    '8': 'Bankruptcy of Retiree Former Employer',
    '9': 'Layoff',
    '10': 'Leave of Absence',
    'ZZ': 'Mutually Defined'
    }

all_Benefit_Status = {
    'A': 'Active',
    'C': 'Budget Reconciliation Act(COBRA)',
    'S': 'Surviving Insured',
    'T': 'TE and FR Act(TEFRA)'
}



Employee_Description_of_plan = {
    '001': 'Chnage-001',
    '002': 'Delete-002',
    '021': 'Addition-021',
    '024': 'Cancellation/Termination-024',
    '025': 'Reinstatement-025',
    '026': 'Correction-026',
    '030': 'Audit/Compare-030',
    '032': 'Emp Information Not Applicable-032'
}



All_Relationship_Type = {
    '01': 'Spouse',
    '03': 'Father/Mother',
    '04': 'Grandfather/Grandmother',
    '05': 'Grandson/Granddaughter',
    '06': 'Uncle/Aunt',
    '07': 'Nephew/Niece',
    '08': 'Cousin',
    '09': 'Adopted Child',
    '10': 'Foster Child',
    '11': 'Son-in-law/Daughter-in law',
    '12': 'Brother-in -law/Sister-in-law',
    '13': 'Mother-in-law/Father-in-law',
    '14': 'Brother/Sister',
    '15': 'Ward',
    '16': 'Stepparent',
    '17': 'Stepson/Setpdaughter',
    '18': 'Employee',
    '19': 'Child',
    '23': 'Sponsored Dependent',
    '24': 'Dependent of a Minor Dependent',
    '25': 'Ex-Spouse',
    '26': 'Guardian',
    '31': 'Court Appointed Guardian',
    '38': 'Collateral Dependent',
    '53': 'Life Partner',
    '60': 'Annuitant',
    'D2': 'Trustee',
    'G8': 'Other Relationship',
    'G9': 'Other Relative'
}

Common_parts_of_transaction = {
    'Author Info Qualifier': '00',
    'Author Information': ' ',
    'Security Info Qualifier': '00',
    'Security Information': ' ',
    'Interchange Sender Id Qualifier': '30',
    'Interchange Sender Id': '571099948',
    'Interchange Receiver Id Qualifier': '30',
    'Interchange Receiver Id': '481244306',
    'Interchange Date': '24.02.05',
    'Interchange Time': '17:18',
    'Inter Control Version Number': '00501',
    'Inter Control Number': '000179621',
    'Acknowledgment Requested': '1',
    'Interchange Usage Indicator': 'P',
    'Functional Id Code': 'BE',
    'Group Control Number': '100549',
    'Implementation Convention Reference': '005010X220A1',
    'Transaction Set Purpose Code': '00',
    'Transaction Set Reference Number': 'S20240205170014',
    'Transaction Date': '02-05-2024',
    'Transaction Time': '17:00:14',
    'Time Zone Code': 'ET',
    'Action Code': '2',
    'Vendor Name': 'Benefitfocus.com, Inc.',
    'Vendor Id Code Qualifier': 'FI',
    'Vendor Id': '571099948'
}