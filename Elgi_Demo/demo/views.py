from django.shortcuts import render
from django.http import JsonResponse
import time
from .models import *
import pyodbc
# Create your views here.

starttime = 0

def db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-R0NCFG9;DATABASE=TT;')
    cursor = conn.cursor()
    return cursor

def demo_screen(request):
    # conn = pyodbc.connect('DRIVER={SQL Server};SERVER=  ;DATABASE= ;')
    # cursor = conn.cursor()
    # cursor.execute("""SELECT * FROM TABLE""")
    # data = cursor.fetchall()
    return render(request,'home.html')

def dashboard(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))
        print("-----------> ", request.POST["scan"])
    station_dropdowns = Stations.objects.all().values()
    station_dropdowns = [obj['station'] for obj in station_dropdowns]
    print("station_dropdown ",station_dropdowns)
    return render(request, "dashboard.html",{'opt_list':station_dropdowns})

# def dashboard(request):
#     return render(request, 'dashboard.html')

def break_display_configuration(request):
    return render(request, 'break_display_configuration.html')

def break_display_configuration(request):
    return render(request, 'break_display_configuration.html')

def holiday(request):
    return render(request, 'holiday.html')

def message(request):
    return render(request, 'message.html')

def message_configuration(request):
    return render(request, 'message_configuration.html')

def shift_and_break(request):
    return render(request, 'shift_and_break.html')

def station_bypass(request):
    cursor = db_connection()

    if request.method == "POST":
        substationcode = request.POST.get('substationcode')
        bypass = request.POST.get('bypass')
        
        cursor.execute(
                """
                UPDATE [dbo].[Sub_Station]
                SET [By_pass] = ?
                WHERE [Sub_Station_Code] = ?
                """,bypass,substationcode)
        cursor.commit()

    station_bypass_details = cursor.execute(
        """SELECT [Sub_Station_Code],[Station_Name],[Station_Purpose],[By_pass] FROM [TT].[dbo].[Sub_Station]""")
    print(station_bypass_details)
    station_bypass_data = [{
        "Sub_Station_Code":obj[0], "Station_Name":obj[1], "Station_Purpose":obj[2], "Bypass":obj[3]
    } for obj in station_bypass_details]

    # print(station_bypass_data)
    return render(request, 'station_bypass.html',{"station_bypass_data":station_bypass_data})


def tool_maintenance(request):
    cursor = db_connection()
    print(request.POST)
    try:
        if request.POST["submit"] == "Add":
                print("Add group")
            # print(" bc ", Bolt_Count)
            # print(" ct ", request.POST["Cycle_Time"])
            # cursor.execute(
            #        """ INSERT INTO [TT].[dbo].[Process_Master] (
            #     "Line_Code"
            #   ,"Pro_Type_Code"
            #   ,"Process_Desc"
            #   ,"Tool_ID"
            #   ,"Process_Code"
            #   ,"Bolt_Count"
            #   ,"Process_Photo_Path"
            #   ,"Takt_Time"
            #   ,"Torque")VALUES (?,?,?,?,?,?,?,?,?)""","EL1_P1_L1",request.POST["Process_Type"], request.POST["Process_Description"],
            #        Tool_ID,request.POST["Process_Code"],int(Bolt_Count),request.POST["Guide_Pic_Path"],int(Cycle_Time),request.POST["Torque"])
            # cursor.commit()

        elif request.POST["submit"] == "Modify":
            print(request.POST["warning_type"],request.POST["set_frequency"],
                request.POST["actual_frequency"], request.POST["tool_id"])
            cursor.execute(
                """
                UPDATE [TT].[dbo].[Tools_Warning]
                SET "Warning_Type" = ?
                    ,"Set_Frequency" = ?
                    ,"Act_Frequency" = ?
                WHERE Tool_ID = ?""", request.POST["warning_type"],request.POST["set_frequency"],
                request.POST["actual_frequency"], request.POST["tool_id"])
            cursor.commit()

    # elif request.POST["submit"] == "Delete":
    #     cursor.execute(
    #             """
    #             DELETE FROM [TT].[dbo].[Process_Master]
    #             WHERE Process_Code = ?""", request.POST["Process_Code"])
    #     cursor.commit()
    
    except:
        pass
    tool_maintenance_details = cursor.execute(
        """SELECT [PK_Code]
      ,[Line_Code]
      ,[Tool_ID]
      ,[Warning_Type]
      ,[Set_Frequency]
      ,[Act_Frequency]
      ,[Created_Date]
      ,[Reset_Date]
      ,[Warning_Status]
      ,[Duration_Date]
        FROM [TT].[dbo].[Tools_Warning]""")

    tool_maintenance_data = [{
        "PK_Code":obj[0], "Line_Code":obj[1], "Tool_ID":obj[2], "Warning_Type":obj[3],"Set_Frequency":obj[4],"Act_Frequency":obj[5],"Created_Date":obj[6],"Reset_Date":obj[7],"Warning_Status":obj[8],"Duration_Date":obj[9]
    } for obj in tool_maintenance_details]

    return render(request, 'tool_maintenance.html',{"tool_maintenance_data":tool_maintenance_data})

def tool_traceability(request):
    cursor = db_connection()
    
    
    tool_traceability_details = cursor.execute(
        """SELECT [PK_Code]
      ,[Line_Code]
      ,[Tool_ID]
      ,[Warning_Type]
      ,[Set_Frequency]
      ,[Act_Frequency]
      ,[Created_Date]
      ,[Reset_Date]
      ,[Warning_Status]
      ,[Duration_Date]
        FROM [TT].[dbo].[Tools_Warning]""")

    tool_traceability_data = [{
        "PK_Code":obj[0], "Line_Code":obj[1], "Tool_ID":obj[2], "Warning_Type":obj[3],"Set_Frequency":obj[4],"Act_Frequency":obj[5],"Created_Date":obj[6],"Reset_Date":obj[7],"Warning_Status":obj[8],"Duration_Date":obj[9]
    } for obj in tool_traceability_details]

    return render(request, 'tool_traceability.html',{"tool_traceability_data":tool_traceability_data})

def child_part_dropdown(request):
    return render(request, 'child_part_dropdown.html')

def child_part_details(request):
    cursor = db_connection()

    child_part_detail = cursor.execute(
        """SELECT * FROM[TT].[dbo].[LN_CP_Details] WHERE
    Fab_Number IN (
     SELECT TOP(500)[FAB_NO] FROM[TT].[dbo].[LN_Order_Release] ORDER BY[Release_Date] DESC
    )""")

    # child_part_detail = cursor.execute(
    #     """SELECT TOP(?)[TPL_Number], [Part_No], [Part_No_Rev]
    # , [Spec_1_Description] , [Spec_1_Value]    , [Spec_2_Description] , [Spec_2_Value]
    # , [Spec_3_Description]  , [Spec_3_Value]    , [Spec_4_Description], [Spec_4_Value]
    # , [Spec_5_Description], [Spec_5_Value]    , [Spec_6_Description]  , [Spec_6_Value]
    # , [Spec_7_Description], [Spec_7_Value]    , [Spec_8_Description], [Spec_8_Value]
    # , [Spec_9_Description], [Spec_9_Value]    , [Spec_10_Description], [Spec_10_Value]
    # , [Spec_11_Description], [Spec_11_Value]    , [Spec_12_Description], [Spec_12_Value]
    # , [Child_Part_Code]  , [Fab_Number]
    # FROM[TT].[dbo].[LN_CP_Details]""",1000)




    child_part_detail_data = [
        {"TPL_Number": obj[0], "Part_No": obj[1], "Part_No_Rev": obj[2], "Spec_1_Description": obj[3], "Spec_1_Value": obj[4],
         "Spec_2_Description": obj[5], "Spec_2_Value": obj[6], "Spec_3_Description": obj[7],"Spec_3_Value": obj[8], "Spec_4_Description": obj[9],"Spec_4_Value": obj[10], "Spec_5_Description": obj[11],"Spec_5_Value": obj[12], "Spec_6_Description": obj[13],"Spec_6_Value": obj[14]
            , "Spec_7_Description": obj[15], "Spec_7_Value": obj[16], "Spec_8_Description": obj[17],"Spec_8_Value": obj[18], "Spec_9_Description": obj[19],"Spec_9_Value": obj[20], "Spec_10_Description": obj[21],"Spec_10_Value": obj[22], "Spec_11_Description": obj[23],"Spec_11_Value": obj[24], "Spec_12_Description": obj[25],"Spec_12_Value": obj[26]
         ,"Child_Part_Code":obj[27], "Fab_Number":obj[28]
         } for obj in child_part_detail]

    return render(request, 'child_part_details.html',{"child_part_detail_data":child_part_detail_data})

def order_release(request):
    cursor = db_connection()
    # order_release_details = cursor.execute(
    #     """SELECT * FROM [TT].[dbo].[LN_Order_Release]""")

    order_release_details = cursor.execute(
        """ SELECT TOP(500) [TPL_No],  [FAB_NO], [pd_no]
    , [Release_Date], [Status], [Model_Code]
    , [Description], [TPL_Description], [Completed_Date]
    FROM [TT].[dbo].[LN_Order_Release] ORDER BY[Release_Date] DESC """)

    order_release_data = [
        {"Release_Date": obj[3], "TPL_No": obj[0], "FAB_NO": obj[1], "pd_no": obj[2],
         "Status": obj[4], "Model_Code": obj[5],"Description":obj[6],"TPL_Description":obj[7],"Completed_Date":obj[8]
         } for obj in order_release_details]

    return render(request, 'order_release.html',{"order_release_data":order_release_data})

def order_release_error_table(request):
    cursor = db_connection()
    # order_release_error_details = cursor.execute(
    #     """SELECT * FROM [TT].[dbo].[LN_Order_Release_Error]""")

    order_release_error_details = cursor.execute(
        """ SELECT TOP(500)[TPL_No]
    , [FAB_NO], [Model_Code], [Po_No]
    , [Release_Date], [Description], [TPL_Description]
    FROM[TT].[dbo].[LN_Order_Release_Error] ORDER BY[Release_Date] DESC""")


    order_release_error_data = [
        {"TPL_No": obj[0], "FAB_NO": obj[1], "Model_Code": obj[2], "Po_No": obj[3],
         "Release_Date": obj[4], "Description": obj[5], "TPL_Description": obj[6]
         } for obj in order_release_error_details]

    return render(request, 'order_release_error_table.html',{"order_release_error_data":order_release_error_data})


#################

def company(request):
    cursor = db_connection()
    # st_operation_tab

    if request.method == "POST":
        print("******************************")
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))

        if request.POST["submit"] == "update":
            cursor.execute(
                """ UPDATE [TT].[dbo].[Operator]
               SET "Skill_Required" = ?
                  ,"Reponsible_For" = ?
                  ,"Screen_text" = ?
             WHERE Sub_Station_Code = ? and Operator_Code = ? """, request.POST["skill_required"], request.POST["responsible_for"],
                request.POST["screen_text"], request.POST["sub_station_code"], request.POST["st_operator_code"])
            cursor.commit()


    st_operation_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Operator]""")
    st_operation_tab = [
        {"Sub_Station_Code": obj[0], "Operator_Code": obj[1], "Skill_Required": obj[2], "Reponsible_For": obj[3],
         "Screen_text": obj[4]} for obj in st_operation_tab]

    # state_tab
    state_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[State]""")
    state_tab = [
        {"Country_Code": obj[0], "State_Code": obj[1], "State_Name": obj[2]} for obj in
        state_tab]

    # city_tab
    city_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[City]""")
    city_tab = [
        {"State_Code": obj[0], "City_Code": obj[1], "City_Name": obj[2]} for obj in
        city_tab]

    # address_tab
    address_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Address]""")
    address_tab = [
        {"City_Code": obj[0], "Address_Code": obj[1], "Address": obj[2]} for obj in
        address_tab]

    # company tab
    company_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Company]""")
    company_tab = [
        {"Address_Code":obj[0], "Company_Code": obj[1],  "Company_Name": obj[2], "Latitude":obj[3], "Longitude":obj[4]} for obj in
        company_tab]

    # plant_tab
    plant_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Plant]""")
    plant_tab = [
        {"Company_Code":obj[0],"Plant_Code": obj[1], "Plant_Name": obj[2]} for obj in
        plant_tab]

    # line tab
    line_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Line]""")
    line_tab = [
        {"Plant_Code": obj[0], "Line_Code": obj[1], "Line_Name": obj[2]} for obj in
        line_tab]

    # station tab
    station_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Station]""")
    station_tab = [
        {"Line_Code":obj[0],"Station_Code": obj[1], "Station_name": obj[2], "Station_Purpose": obj[3]} for obj in station_tab]

    # substation tab
    substation_tab = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Sub_Station]""")
    substation_tab = [{"Station_Code": obj[0],"Sub_Station_Code": obj[1],"Station_Name": obj[2],"Station_Purpose": obj[3],"By_pass": obj[4]} for obj in substation_tab]

    # country tab
    country_tab = cursor.execute(
        """SELECT [Country_Code], [Country_Name] FROM[TT].[dbo].[Country]""")
    country_data = [{"Country_Code": obj[0], "Country_Name": obj[1]} for obj in country_tab]


    return render(request, 'company.html', {'st_operation_tab': st_operation_tab, 'state_tab':state_tab,'city_tab':city_tab,'address_tab':address_tab,'company_tab':company_tab, 'plant_tab':plant_tab ,'line_tab':line_tab ,'station_tab':station_tab ,'substation_tab':substation_tab ,'country_data':country_data})

def tpl_master(request):
    cursor = db_connection()

    if request.method == "POST":
        print("******************************")
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))

        if request.POST["submit"] == "Add":
            cursor.execute(
                """ INSERT INTO [TT].[dbo].[TPL_Master] (
                         "TPL_Code"
                        ,"TPL_Description"
                        ,"Machines_on_AGV")
                      VALUES (?,?,?)""",request.POST["TPL_Code"],request.POST["TPL_Description"],request.POST["AGV"])
            cursor.commit()

        # elif request.POST["submit"] == "Delete":
        #     cursor.execute(
        #             """
        #             DELETE FROM [TT].[dbo].[TPL_Master]
        #             WHERE TPL_Code = ?""", request.POST["TPL_Code"])
        #     cursor.commit()
            
        elif request.POST["submit"] == "Modify":
            cursor.execute(
                    """UPDATE [TT].[dbo].[TPL_Master]
                   SET
                      "TPL_Code"= ?
                      ,"TPL_Description" = ?
                      ,"Machines_on_AGV" = ?
                 WHERE TPL_Code = ?""",request.POST["TPL_Code"],request.POST["TPL_Description"],request.POST["AGV"],request.POST["TPL_Code"])
            cursor.commit()

    TPL_code_details = cursor.execute(
        """SELECT [TPL_Code] FROM[TT].[dbo].[TPL_Master]""")
    TPL_code_data = [obj[0] for obj in TPL_code_details]
    # print(TPL_code_data)




    tpl_master_details = cursor.execute(
        "SELECT * FROM[TT].[dbo].[TPL_Master]")

    tpl_master_data = [{
        "TPL_Code": obj[0],"TPL_Description": obj[2],"Machines_on_AGV": obj[3]
    } for obj in tpl_master_details]
    # print(tpl_master_data)

    return render(request, 'tpl_master.html',{"tpl_master_data":tpl_master_data, "tpl_code_details":TPL_code_data})

def dms_master(request):
    cursor = db_connection()

    dms_master_details = cursor.execute(
        "SELECT * FROM [TT].[dbo].[DMS_Master]"
    )

    dms_master_data = [{
        "PMMKEY": obj[0], "Level_1": obj[1],"Level_2": obj[2], "Level_3": obj[3], "Level_4": obj[4], "Level_5" : obj[5]
    } for obj in dms_master_details]





    return render(request, 'dms_master.html',{"dmsmaster_data": dms_master_data})

def tool_master(request):
    cursor = db_connection()
    tools_type_master_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Tools_Type_Master]""")
    tools_type_master_data = [{"Line_Code": obj[2], "Tool_Type_ID": obj[0], "Tool_Type": obj[2]
                      } for obj in tools_type_master_details]


    tool_master_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[TPL_Master]""")
    tool_master_data = [{
        "[TPL_Code]":obj[0],"Model_Code":obj[1],"TPL_Description":obj[2],"Machines_on_AGV":obj[3]
        } for obj in tool_master_details]

    return render(request, 'tool_master.html',{'tools_type_master_data':tools_type_master_data})

#Process master
def process_master(request):
    cursor = db_connection()

    if request.method == "POST":
        print("******************************")
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))
        try:
            if request.POST["Bolt_Count"] == "":
                Bolt_Count = 0
            else:
                Bolt_Count = request.POST["Bolt_Count"]

            if request.POST["Cycle_Time"] == "":
                Cycle_Time = 0
            else:
                Cycle_Time = request.POST["Cycle_Time"]

            if request.POST["Tool_ID"] == "":
                Tool_ID = "NULL"
            else:
                Tool_ID = request.POST["Tool_ID"]

        except:
            pass

        if request.POST["submit"] == "Add":
            # print(" bc ", Bolt_Count)
            # print(" ct ", request.POST["Cycle_Time"])
            cursor.execute(
                   """ INSERT INTO [TT].[dbo].[Process_Master] (
                "Line_Code"
              ,"Pro_Type_Code"
              ,"Process_Desc"
              ,"Tool_ID"
              ,"Process_Code"
              ,"Bolt_Count"
              ,"Process_Photo_Path"
              ,"Takt_Time"
              ,"Torque")VALUES (?,?,?,?,?,?,?,?,?)""","EL1_P1_L1",request.POST["Process_Type"], request.POST["Process_Description"],
                   Tool_ID,request.POST["Process_Code"],int(Bolt_Count),request.POST["Guide_Pic_Path"],int(Cycle_Time),request.POST["Torque"])
            cursor.commit()

        elif request.POST["submit"] == "Modify":
            cursor.execute(
                """
                UPDATE [TT].[dbo].[Process_Master]
               SET "Line_Code" = ?
                  ,"Pro_Type_Code" = ?
                  ,"Process_Desc" = ?
                  ,"Tool_ID" = ?
                  ,"Process_Code" = ?
                  ,"Bolt_Count" = ?
                  ,"Process_Photo_Path" = ?
                  ,"Takt_Time" = ?
                  ,"Torque" = ?
             WHERE Process_Code = ?""", "EL1_P1_L1", request.POST["Process_Type"], request.POST["Process_Description"],
                Tool_ID, request.POST["Process_Code"], int(Bolt_Count), request.POST["Guide_Pic_Path"], int(Cycle_Time),
                request.POST["Torque"], request.POST["Process_Code"])
            cursor.commit()

        elif request.POST["submit"] == "Delete":
            cursor.execute(
                    """
                    DELETE FROM [TT].[dbo].[Process_Master]
                    WHERE Process_Code = ?""", request.POST["Process_Code"])
            cursor.commit()

        if request.POST["submit"] == "PM_Add":
            cursor.execute(
                   """ INSERT INTO [TT].[dbo].[Process_Map_Master] (
                    "Model_Code"
                  ,"Operator_Code"
                  ,"Process_Code"
                  ,"Process_Seq_No"
                  ,"Line_Code")VALUES (?,?,?,?,?)""", request.POST["model_code"], request.POST["operator_code"],
                request.POST["process_code"], request.POST["sequence_no"],"EL1_P1_L1")
            cursor.commit()


        elif request.POST["submit"] == "PM_Modify":
            cursor.execute(
                """
                UPDATE [TT].[dbo].[Process_Map_Master]
                SET 
                  "Operator_Code" = ?
                  ,"Process_Code" = ?
                  ,"Process_Seq_No" = ?
                  ,"Line_Code" = ?
                WHERE PMMKEY = ?""", request.POST["operator_code"],
                request.POST["process_code"], request.POST["sequence_no"],"EL1_P1_L1",request.POST["pmmkey"])
            cursor.commit()

        elif request.POST["submit"] == "PM_Delete":
            cursor.execute(
                """
                DELETE FROM [TT].[dbo].[Process_Map_Master]
                WHERE PMMKEY = ?""", request.POST["pmmkey"])
            cursor.commit()

    process_library_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Process_Master]""")

    process_library_data = [{
        "Line_Code":obj[0], "Pro_Type_Code":obj[1], "Process_Desc":obj[2], "Tool_ID":obj[3],
        "Process_Code":obj[4],"Bolt_Count":obj[5],"Process_Photo_Path":obj[6],"Takt_Time":obj[7],"Torque":obj[8]
    } for obj in process_library_details]
    #print({"process_master_data":process_master_data})

    process_type_details = cursor.execute(
        """SELECT [Pro_Type_Code] FROM [TT].[dbo].[Process_Type_Master]""")
    process_type_data = [i[0] for i in process_type_details]
    # print("process_type_data  ",process_type_data)

    tool_id_details = cursor.execute(
        """SELECT [Tool_ID] FROM [TT].[dbo].[Tools_Master]""")
    tool_id_data = [j[0] for j in tool_id_details]
    #print("tool_ids ", tool_id_data)


    operator_code_details = cursor.execute(
        """SELECT [Operator_Code] FROM[TT].[dbo].[Operator]""")
    operator_code_data = [obj[0] for obj in operator_code_details]
    # print("operator_code_data",operator_code_data)

    process_code_details = cursor.execute(
        """SELECT [Process_Code] FROM[TT].[dbo].[Process_Master]""")
    process_code_data = [obj[0] for obj in process_code_details]
    # print("process_code_data",process_code_data)

    model_code_details = cursor.execute(
        """SELECT DISTINCT  [Model_Code] FROM [TT].[dbo].[Model_Master]""")
    model_code_data = [obj[0] for obj in model_code_details]
    # print("model_code_data",model_code_data)

    process_master_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Process_Map_Master]""")
    process_master_data = [{
        "PMMKEY":obj[0], "Model_Code":obj[1], "Operator_Code":obj[2], "Process_Code":obj[3], "Process_Seq_No":obj[4], "Line_Code":obj[5]
    } for obj in process_master_details]
    #print("process_master_data ",process_master_data)
    # "Model_Group":obj[1],

    return render(request, 'process_master.html', {"model_code_data":model_code_data, "process_code_data":process_code_data ,"operator_code_data":operator_code_data ,"process_type_data":process_type_data,"tool_id_data":tool_id_data,"process_library_data":process_library_data,"process_master_data":process_master_data})

#Process master copy 
def process_master_copy(request):
    cursor = db_connection()

    if request.method == "POST":
        print("******************************")
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))
        try:
            if request.POST["Bolt_Count"] == "":
                Bolt_Count = 0
            else:
                Bolt_Count = request.POST["Bolt_Count"]

            if request.POST["Cycle_Time"] == "":
                Cycle_Time = 0
            else:
                Cycle_Time = request.POST["Cycle_Time"]

            if request.POST["Tool_ID"] == "":
                Tool_ID = "NULL"
            else:
                Tool_ID = request.POST["Tool_ID"]

        except:
            pass

        if request.POST["submit"] == "Add":
            # print(" bc ", Bolt_Count)
            # print(" ct ", request.POST["Cycle_Time"])
            cursor.execute(
                   """ INSERT INTO [TT].[dbo].[Process_Master] (
                "Line_Code"
              ,"Pro_Type_Code"
              ,"Process_Desc"
              ,"Tool_ID"
              ,"Process_Code"
              ,"Bolt_Count"
              ,"Process_Photo_Path"
              ,"Takt_Time"
              ,"Torque")VALUES (?,?,?,?,?,?,?,?,?)""","EL1_P1_L1",request.POST["Process_Type"], request.POST["Process_Description"],
                   Tool_ID,request.POST["Process_Code"],int(Bolt_Count),request.POST["Guide_Pic_Path"],int(Cycle_Time),request.POST["Torque"])
            cursor.commit()

        elif request.POST["submit"] == "Modify":
            cursor.execute(
                """
                UPDATE [TT].[dbo].[Process_Master]
               SET "Line_Code" = ?
                  ,"Pro_Type_Code" = ?
                  ,"Process_Desc" = ?
                  ,"Tool_ID" = ?
                  ,"Process_Code" = ?
                  ,"Bolt_Count" = ?
                  ,"Process_Photo_Path" = ?
                  ,"Takt_Time" = ?
                  ,"Torque" = ?
             WHERE Process_Code = ?""", "EL1_P1_L1", request.POST["Process_Type"], request.POST["Process_Description"],
                Tool_ID, request.POST["Process_Code"], int(Bolt_Count), request.POST["Guide_Pic_Path"], int(Cycle_Time),
                request.POST["Torque"], request.POST["Process_Code"])
            cursor.commit()

        elif request.POST["submit"] == "Delete":
            cursor.execute(
                    """
                    DELETE FROM [TT].[dbo].[Process_Master]
                    WHERE Process_Code = ?""", request.POST["Process_Code"])
            cursor.commit()

        if request.POST["submit"] == "PM_Add":
            cursor.execute(
                   """ INSERT INTO [TT].[dbo].[Process_Map_Master] (
                    "Model_Code"
                  ,"Operator_Code"
                  ,"Process_Code"
                  ,"Process_Seq_No"
                  ,"Line_Code")VALUES (?,?,?,?,?)""", request.POST["model_code"], request.POST["operator_code"],
                request.POST["process_code"], request.POST["sequence_no"],"EL1_P1_L1")
            cursor.commit()


        elif request.POST["submit"] == "PM_Modify":
            cursor.execute(
                """
                UPDATE [TT].[dbo].[Process_Map_Master]
                SET 
                  "Operator_Code" = ?
                  ,"Process_Code" = ?
                  ,"Process_Seq_No" = ?
                  ,"Line_Code" = ?
                WHERE PMMKEY = ?""", request.POST["operator_code"],
                request.POST["process_code"], request.POST["sequence_no"],"EL1_P1_L1",request.POST["pmmkey"])
            cursor.commit()

        elif request.POST["submit"] == "PM_Delete":
            cursor.execute(
                """
                DELETE FROM [TT].[dbo].[Process_Map_Master]
                WHERE PMMKEY = ?""", request.POST["pmmkey"])
            cursor.commit()

    process_library_details = cursor.execute(
        """SELECT TOP (10) [Line_Code]
      ,[Pro_Type_Code]
      ,[Process_Desc]
      ,[Tool_ID]
      ,[Process_Code]
      ,[Bolt_Count]
      ,[Process_Photo_Path]
      ,[Takt_Time]
      ,[Torque]
  FROM [TT].[dbo].[Process_Master]""")
    # process_library_details = cursor.execute(
    #     """SELECT * FROM[TT].[dbo].[Process_Master]""")

    process_library_data = [{
        "Line_Code":obj[0], "Pro_Type_Code":obj[1], "Process_Desc":obj[2], "Tool_ID":obj[3],
        "Process_Code":obj[4],"Bolt_Count":obj[5],"Process_Photo_Path":obj[6],"Takt_Time":obj[7],"Torque":obj[8]
    } for obj in process_library_details]
    #print({"process_master_data":process_master_data})

    process_type_details = cursor.execute(
        """SELECT [Pro_Type_Code] FROM [TT].[dbo].[Process_Type_Master]""")
    process_type_data = [i[0] for i in process_type_details]
    # print("process_type_data  ",process_type_data)

    tool_id_details = cursor.execute(
        """SELECT [Tool_ID] FROM [TT].[dbo].[Tools_Master]""")
    tool_id_data = [j[0] for j in tool_id_details]
    #print("tool_ids ", tool_id_data)


    operator_code_details = cursor.execute(
        """SELECT [Operator_Code] FROM[TT].[dbo].[Operator]""")
    operator_code_data = [obj[0] for obj in operator_code_details]
    # print("operator_code_data",operator_code_data)

    process_code_details = cursor.execute(
        """SELECT [Process_Code] FROM[TT].[dbo].[Process_Master]""")
    process_code_data = [obj[0] for obj in process_code_details]
    # print("process_code_data",process_code_data)

    model_code_details = cursor.execute(
        """SELECT DISTINCT  [Model_Code] FROM [TT].[dbo].[Model_Master]""")
    model_code_data = [obj[0] for obj in model_code_details]
    # print("model_code_data",model_code_data)

    process_master_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Process_Map_Master]""")
    process_master_data = [{
        "PMMKEY":obj[0], "Model_Code":obj[1], "Operator_Code":obj[2], "Process_Code":obj[3], "Process_Seq_No":obj[4], "Line_Code":obj[5]
    } for obj in process_master_details]
    #print("process_master_data ",process_master_data)
    # "Model_Group":obj[1],

    return render(request, 'process_master_copy.html', {"model_code_data":model_code_data, "process_code_data":process_code_data ,"operator_code_data":operator_code_data ,"process_type_data":process_type_data,"tool_id_data":tool_id_data,"process_library_data":process_library_data,"process_master_data":process_master_data})


def employee(request):
    cursor = db_connection()



    employee_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Employee_Details_UPD]""")
    employee_data = [{"Company_Code": obj[0], "Emp_ID": obj[1],"Emp_Name": obj[2], "Role_Code": obj[3],
                            "Emp_Photo_Path": obj[4], "User_Name": obj[5],"Password": obj[6]} for obj in employee_details]

    return render(request, 'employee.html',{'employee_data': employee_data})

def tool_warning_master(request):
    cursor = db_connection()
    twm_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Tools_Warning]""")
    twm_data = [{"Line_Code": obj[1],"PK_Code": obj[0],"Tool_ID": obj[2],
                 "Warning_Type": obj[3],"Set_Frequency": obj[4],"Act_Frequency": obj[5],
                 "Created_Date": obj[6],"Reset_Date": obj[7],"Warning_Status": obj[8],
                 "Duration_Date": obj[9]} for obj in twm_details]

    return render(request, 'tool_warning_master.html',{'twm_data':twm_data})

def packing(request):
    cursor = db_connection()
    packing_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Packing_DD]""")
    packing_data = [{"Package_Code": obj[0]} for obj in packing_details]

    return render(request, 'packing.html',{'packing_data': packing_data})

def drive_coupling_master(request):
    cursor = db_connection()

    if request.method == "POST":
        print("******************************")
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))

    dcp_details = cursor.execute(
        """SELECT * FROM[TT].[dbo].[Drive_Coupling_Master]""")
    dcm_data = [{"TPL_No": obj[0],"Model_Description": obj[1],"Model_Code": obj[2],
                "Distance": obj[3],"Sensor_No": obj[4],"Test_Certificate": obj[5]
                } for obj in dcp_details]

    return render(request, 'drive_coupling_master.html', {'dcm_data':dcm_data})

def process(request):
    return render(request, 'process.html')

def process_p(request):
    return render(request, 'process_p.html')

def dmi(request):
    return render(request, 'dmi.html')

def login(request):
    return render(request, 'login.html')

def pdi(request):
    starttime= time.time()
    stime = time.ctime(starttime)
    return render(request, 'pdi.html',{"s_time":stime})

def test_booth_master(request):
    return render(request, 'test_booth_master.html')

def test_certificate_1(request):
    return render(request, 'test_certificate_1.html')
def test_certificate_2(request):
    return render(request, 'test_certificate_2.html')
def test_certificate_3(request):
    return render(request, 'test_certificate_3.html')
def test_certificate_4(request):
    return render(request, 'test_certificate_4.html')
def test_certificate_5(request):
    return render(request, 'test_certificate_5.html')
def test_certificate_6(request):
    return render(request, 'test_certificate_6.html')
def test_certificate_7(request):
    return render(request, 'test_certificate_7.html')
def test_certificate_8(request):
    return render(request, 'test_certificate_8.html')
def list_of_fab_number(request):
    return render(request, 'list_of_fab_number.html')
def scan_fab_number(request):
    return render(request, 'scan_fab_number.html')
def start_test(request):
    return render(request, 'start_test.html')

def pdi_2(request):
    # endtime = time.time() - starttime
    # etime = time.ctime(endtime)
    return render(request, 'pdi_2.html')

############################################################
def reports(request):
    return render(request, 'reports.html')

def compressprocessstatus(request):
    return render(request, 'compressprocessstatus.html')

def lnserverstatus(request):
    return render(request, 'lnserverstatus.html')

def processstatus(request):
    return render(request, 'processstatus.html')

def lnerpstatus(request):
    return render(request, 'lnerpstatus.html')

def tpldetails(request):
    return render(request, 'tpldetails.html')

def processsequence(request):
    return render(request, 'processsequence.html')

def active_tpl_list(request):
    return render(request, 'active_tpl_list.html')

###################################################################
def pdi_3(request):
    return render(request, 'pdi_3.html')

def alpha_line(request):
    cursor = db_connection()


    order_release_query = """SELECT * FROM [TT].[dbo].[Sub1_OP1_Fab_Init_View] WHERE Release_Date >= DATEADD(day, -7, GETDATE()) AND Status = 'R'"""
    order_release_table = [{

    }for obj in cursor.execute(order_release_query)]

    order_release_error_table = cursor.execute(
        """SELECT * FROM [TT].[dbo].[Sub1_OP1_Fab_Init_View] WHERE Release_Date >= DATEADD(day, -7, GETDATE()) AND Status = NULL """)

    print("order_release_table",order_release_table)
    print("order release error table", order_release_error_table)

    json = {
        "page_type": "home",
        "page_details":{
            "order_release_table": order_release_table,
            "order_release_error_table": order_release_error_table
        },
    }
    return render(request, 'alpha_line.html', json)


def dms_app(request):
    return render(request, 'dms_app.html')

def test2(request):
    # cursor = db_connection()

    if request.method == "POST":
        print("yes")
        print(request.POST)

    return render(request, 'substation_2703.html')

def substation(request):
    return render(request, 'substation.html')

def substation_Amit(request):
    return render(request, 'substation_Amit.html')



def substation_Mayank(request):

    if request.method == "POST":
        print("yes")
        print(request.POST)
    
    return render(request,'substation_b.html')

def substation_Mayank_New(request):

    if request.method == "POST":
        print("yes")
        print(request.POST)
    
    return render(request,'substation_mayank_final_updated.html')


def pdi_master(request):
    cursor = db_connection()

    # model_code_details = cursor.execute(
    #     """SELECT DISTINCT  * FROM [TT].[dbo].[PDI_CL_Master]""")

    # model_code_data = [obj[0] for obj in model_code_details]

    if request.method == "POST":
        print("******************************")
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))

        # if request.POST["submit"] == "Add":
        #     cursor.execute(
        #         """ INSERT INTO [TT].[dbo].[PDI_CL_Master] (
        #                 "CL_Code"
        #               ,"CL_Type_Code"
        #               ,"CL_List_Description"
        #               ,"Ok_Photo_Path"
        #               ,"NOT_Ok_Photo_Path"
        #               ,"Check_point_Delay"
        #               ,"Sample_Page_Capture"
        #               ,"Line_Code"
        #               ,"Tack_Time"
        #               )
        #               VALUES (?,?,?,?,?,?,?)""",request.POST["CL_Code"],request.POST["CL_Type_Code"],
        #         request.POST["CL_List_Description"],request.POST["Ok_Photo_Path"],request.POST["NOT_Ok_Photo_Path"],request.POST["Check_point_Delay"],request.POST["Sample_Page_Capture"],request.POST["Line_Code"],request.POST["Tack_Time"])
        #     cursor.commit()

    #     elif request.POST["submit"] == "Modify":
    #         cursor.execute(
    #                 """ UPDATE [TT].[dbo].[PDI_CL_Master]
    #                SET "CL_Code" = ?
    #                   ,"CL_Type_Code" = ?
    #                   ,"CL_List_Description" = ?
    #                   ,"Ok_Photo_Path" = ?
    #                    ,"NOT_Ok_Photo_Path" = ?
    #                   ,"Check_point_Delay"
    #                   ,"Sample_Page_Capture"
    #                   ,"Line_Code"
    #                   ,"Tack_Time" = ?
    #              WHERE Pdi_Code = ?""",request.POST["CL_Code"],request.POST["CL_Type_Code"],
    #             request.POST["CL_List_Description"],request.POST["Ok_Photo_Path"],request.POST["NOT_Ok_Photo_Path"],request.POST["Check_point_Delay"],request.POST["Sample_Page_Capture"],request.POST["Line_Code"],request.POST["Tack_Time"])
    #         cursor.commit()


    # if request.POST["submit"] == "PM_Add":
    #         cursor.execute(
    #                """ INSERT INTO [TT].[dbo].[PDI_CL_Map_Master] (
    #                 "Model_Code"
    #               ,"PDI_CL_Code"
    #               ,"Order_No"
    #               ,"Line_Code")VALUES (?,?,?,?)""", request.POST["model_code"], request.POST["process_code"],
    #             request.POST["operator_code"], "EL1_P1_L1")
    #         cursor.commit()


    # elif request.POST["submit"] == "PM_Modify":
    #     cursor.execute(
    #         """
    #         UPDATE [TT].[dbo].[PDI_CL_Map_Master]
    #         SET "Model_Code" = ?
    #             ,"PDI_CL_Code" = ?
    #             ,"Order_No" = ?
    #             ,"Line_Code" = ?
    #         WHERE PMMKEY = ?""", request.POST["PMMKEY"], request.POST["model_code"],
    #         request.POST["process_code"], request.POST["operator_code"],"EL1_P1_L1",request.POST["pmmkey"])
    #     cursor.commit()

    # elif request.POST["submit"] == "PM_Delete":
    #     cursor.execute(
    #         """
    #         DELETE FROM [TT].[dbo].[PDI_CL_Map_Master]
    #         WHERE PMMKEY = ?""", request.POST["pmmkey"])
    #     cursor.commit()

    pdi_msater_details = cursor.execute(
        "SELECT * FROM [TT].[dbo].[PDI_CL_Map_Master]"
    )

    pdi_master_data = [{
         "PMMKEY": obj[0],"Model_Code": obj[1],"PDI_CL_Code": obj[2],"Order_No": obj[3],"Line_Code": obj[4]
    } for obj in pdi_msater_details]

    model_code_details = cursor.execute(
        "SELECT [Model_Code] FROM [TT].[dbo].[PDI_CL_Map_Master]"
    )
  
    model_code_data = [obj[0] for obj in model_code_details]
    # print(model_code_data)



    pdi_library_details = cursor.execute(
        "SELECT DISTINCT  * FROM [TT].[dbo].[PDI_CL_Master]")

    pdi_library_data = [{
        "CL_Code": obj[0],"CL_Type_Code": obj[1],"CL_List_Description": obj[2],
        "Ok_Photo_Path": obj[3],"NOT_Ok_Photo_Path": obj[4], "Check_point_Delay" :  obj[5], "Sample_Page_Capture": obj[6],"Line_Code": obj[7], "Tack_Time": obj[8]
    } for obj in pdi_library_details]

    cl_code_details = cursor.execute(
        "SELECT [PDI_CL_Code] FROM [TT].[dbo].[PDI_CL_Map_Master]"
    )

    cl_code_data = [obj[0] for obj in cl_code_details]
    # print(cl_code_data)

    return render(request, 'pdi_master2.html', {"model_code_data":model_code_data, "pdi_cl_code_data":cl_code_data,  "pdi_library_datas": pdi_library_data, "pdi_library_details":pdi_library_details, "master_pdi_data":pdi_master_data, "master_pdi_details":pdi_msater_details})





def alphaline3(request):
    return render(request, 'alpha.html')

def alphalinetesting(request):
    return render(request, 'alphatest.html')

def alphachild(request):
    return render(request, "alphachild.html")

def abhayalpha(request):
    return render(request, "abhayalpha.html")

def operator(request):
    return render(request, "operator_screen.html")

def inorderrelease(request):
    cursor = db_connection()

    print("**********")
    if request.method == "POST":
        print("yes")
        print(request.POST)
        
    else:
        pass


    order_release_details = cursor.execute(
        """ SELECT TOP(500) [TPL_No],  [FAB_NO], [pd_no]
    , [Release_Date], [Status], [Model_Code]
    , [Description], [TPL_Description], [Completed_Date]
    FROM [TT].[dbo].[LN_Order_Release] ORDER BY[Release_Date] DESC """)

    order_release_data = [
        {"Release_Date": obj[3], "TPL_No": obj[0], "FAB_NO": obj[1], "pd_no": obj[2],
         "Status": obj[4], "Model_Code": obj[5],"Description":obj[6],"TPL_Description":obj[7],"Completed_Date":obj[8]
         } for obj in order_release_details]

    child_part_detail = cursor.execute(
        """SELECT * FROM[TT].[dbo].[LN_CP_Details] WHERE
    Fab_Number IN (
     SELECT TOP(500)[FAB_NO] FROM[TT].[dbo].[LN_Order_Release] ORDER BY[Release_Date] DESC
    )""")

    child_part_detail_data = [
            {"TPL_Number": obj[0], "Part_No": obj[1], "Part_No_Rev": obj[2], "Spec_1_Description": obj[3], "Spec_1_Value": obj[4],
            "Spec_2_Description": obj[5], "Spec_2_Value": obj[6], "Spec_3_Description": obj[7],"Spec_3_Value": obj[8], "Spec_4_Description": obj[9],"Spec_4_Value": obj[10], "Spec_5_Description": obj[11],"Spec_5_Value": obj[12], "Spec_6_Description": obj[13],"Spec_6_Value": obj[14]
                , "Spec_7_Description": obj[15], "Spec_7_Value": obj[16], "Spec_8_Description": obj[17],"Spec_8_Value": obj[18], "Spec_9_Description": obj[19],"Spec_9_Value": obj[20], "Spec_10_Description": obj[21],"Spec_10_Value": obj[22], "Spec_11_Description": obj[23],"Spec_11_Value": obj[24], "Spec_12_Description": obj[25],"Spec_12_Value": obj[26]
            ,"Child_Part_Code":obj[27], "Fab_Number":obj[28]
            } for obj in child_part_detail]
    return render(request, "store.html",{"child_part_detail_data":child_part_detail_data, "order_release_data":order_release_data})

def inorderrelease_new(request):
    return render(request, "lnorderrelease1 (1).html")

def toolscreen(request):
    return render(request, "toolscreen.html")


def qloss_screen(request):
    return render(request, "qloss_screen.html")


def q_loss(request):
    return render(request, "qloss.html")

def cimage(request):
    return render(request, "pdi_2.html")

def testboothtest(request):
    return render(request, "test_booth_master1.html")
def testboothtest2(request):
    return render(request, "testboothlib.html")
def testboothtest3(request):
    return render(request, "testboothmst.html")


def plasticerp(request):
    return render(request, "plasticdashboard.html")