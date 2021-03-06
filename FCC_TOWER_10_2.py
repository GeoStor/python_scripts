# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# FCC_TOWER.py
# Created on: 2014-06-03 11:09:57.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: FCC_TOWER <RA_txt> <CO_txt> <EN_txt> <FCC_ASR_TOWER_gdb>
# Description:
# -----------------------------------------------------------
# Edited: Kristen Jordan, July 2014, Kansas Data Access and Support Center, kristen@kgs.ku.edu, 785-864-2132
# Edits: Added automatic download, unzip, file rename, and file character replacements
# Edited: Matthew DeLong, February 2015, Arkansas GIS OFfice/Department of Inmformation Systems, 501-682-3710
# Edits: Removed unzip def and added Zipfile module to unzip files
# Original code from AGIO (minus original variable settings) starts in line
# Necessary parameters in ArcGIS script- Target geodatabase, file download location, state abbreviation

def DownloadFCCData(downloadLoc):
    import os
    from urllib2 import urlopen
    #URL of FCC tower locations
    url = 'http://wireless.fcc.gov/uls/data/complete/r_tower.zip'

    try:
        #open url
        f = urlopen(url)
        arcpy.AddMessage( "Downloading " + url)

        #save file
        savedZip = os.path.join(downloadLoc, os.path.basename(url))
        open(savedZip, "wb").write(f.read())

    except:
        arcpy.AddMessage("unable to download " + url)
        savedZip = 0

    return savedZip


def runCommand(command):
    import subprocess
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        print str(e)

def inplace_change(filename, old_string, new_string):
    #from http://stackoverflow.com/questions/4128144/replace-string-within-file-contents
        s=open(filename).read()
        if old_string in s:
                print 'Changing "{old_string}" to "{new_string}"'.format(**locals())
                s=s.replace(old_string, new_string)
                f=open(filename, 'w')
                f.write(s)
                f.flush()
                f.close()
        else:
                print 'No occurances of "{old_string}" found.'.format(**locals())

#Any Questions or concerns regarding this script may be directed to Arkansas Geographic Information Office at 501-682-3710

# Import arcpy module
import arcpy, os, sys, zipfile, shutil

# Script arguments
FCC_ASR_TOWER_gdb = arcpy.GetParameterAsText(0)

downloadLoc = arcpy.GetParameterAsText(1)

State = arcpy.GetParameterAsText(2)

#check that state abbreivation is used
if len(State) > 2:
    arcpy.AddMessage("Please use state abbreviation")
    sys.exit()

#download file
savedZip = DownloadFCCData(downloadLoc)
if savedZip == 0:
    sys.exit()

#unzip file
zip = zipfile.ZipFile(savedZip)
zip.extractall(downloadLoc+r"\FCC_TOWER")
zip.close()
unzipFolder = downloadLoc+"\FCC_TOWER"


#rename CO, EN, RA files
if os.path.exists(unzipFolder):
    arcpy.AddMessage("Renaming files...")

    #create list of file names
    fileList = ["CO", "EN", "RA"]

    #loop through file names
    for abbr in fileList:
        #rename dat files to txt
        dat = os.path.join(unzipFolder, abbr + ".dat")
        txt = os.path.join(unzipFolder, abbr + ".txt")

        #make sure the dat exists before renaming
        if os.path.exists(dat):
            os.rename(dat, txt)
        else:
            arcpy.AddMessage("Files not processed correctly")
            sys.exit()

        #replace characters in text files
        try:
            inplace_change(txt, ',', '') #replace comma with nothing
            inplace_change(txt, '"', '') #replace double quote with nothing
            inplace_change(txt, '|', ',') #replace pipe with comma

            arcpy.AddMessage("Characters replaced in " + abbr)


            #flag success as "yay" so the script will continue to process the tower data
            success = 1

        except:
            success = 0
            arcpy.AddMessage("Content not replaced for " + abbr)
            sys.exit()
else:
    arcpy.AddMessage("File did not unzip correctly")
    sys.exit()

if success == 1:
    arcpy.AddMessage("Importing txt files to tables... " )
    #set path names
    CO_txt = os.path.join(unzipFolder, "CO.txt")
    EN_txt = os.path.join(unzipFolder, "EN.txt")
    RA_txt = os.path.join(unzipFolder, "RA.txt")

    FCC_ASR_TOWER_RA = FCC_ASR_TOWER_gdb + '\\FCC_ASR_TOWER_RA'
    FCC_ASR_TOWER_RA_view = FCC_ASR_TOWER_gdb + '\\FCC_ASR_TOWER_RA_view'
    FCC_ASR_TOWER_CO = FCC_ASR_TOWER_gdb + '\\FCC_ASR_TOWER_CO'
    FCC_ASR_TOWER_CO_view = FCC_ASR_TOWER_gdb + '\\FCC_ASR_TOWER_CO_view'
    FCC_ASR_TOWER_EN = FCC_ASR_TOWER_gdb + '\\FCC_ASR_TOWER_EN'
    FCC_ASR_TOWER_EN_view = FCC_ASR_TOWER_gdb + '\\FCC_ASR_TOWER_EN_view'
    FCC_ASR_TOWER_JOIN = FCC_ASR_TOWER_gdb + '\\FCC_ASR_TOWER_JOIN'
    Metadata_and_schema = FCC_ASR_TOWER_gdb + '\\Metadata_and_schema'
    Metadata_and_schema_lyr =  FCC_ASR_TOWER_gdb + '\\Metadata_and_schema_lyr'
    FCC_ASR_TOWER_XY_lyr =FCC_ASR_TOWER_gdb + '\\FCC_ASR_TOWER_XY_lyr'
    FCC_ASR_TOWER_XY = FCC_ASR_TOWER_gdb + '\\FCC_ASR_TOWER_XY'
    FCC_ASR_TOWER_ALL = FCC_ASR_TOWER_gdb + '\\FCC_ASR_TOWER_ALL'
##    FCC_ASR_TOWER_STATE =FCC_ASR_TOWER_gdb + '\\FCC_ASR_TOWER_'+State


    arcpy.env.overwriteOutput = True

    # Process: Table to Table (3)
    arcpy.TableToTable_conversion(CO_txt, FCC_ASR_TOWER_gdb, "FCC_ASR_TOWER_CO", "", "REGISTRATION_NUMBER \"REGISTRATION_NUMBER\" true true false 4 Long 0 0 ,First,#," + CO_txt +",Field4,-1,-1;UNIQUE_SYSTEM_IDENTIFIER \"UNIQUE_SYSTEM_IDENTIFIER\" true true false 4 Long 0 0 ,First,#," + CO_txt +",Field5,-1,-1;COORDINATE_TYPE \"COORDINATE_TYPE\" true true false 255 Text 0 0 ,First,#," + CO_txt +",Field6,-1,-1;LAT_DEGREES \"LAT_DEGREES\" true true false 4 Text 0 0 ,First,#," + CO_txt +",Field7,-1,-1;LAT_MINS \"LAT_MINS\" true true false 10 Text 0 0 ,First,#," + CO_txt +",Field8,-1,-1;LAT_SECS \"LAT_SECS\" true true false 8 Text 0 0 ,First,#," + CO_txt +",Field9,-1,-1;LONG_DEGREES \"LONG_DEGREES\" true true false 4 Text 0 0 ,First,#," + CO_txt +",Field12,-1,-1;LONG_MINS \"LONG_MINS\" true true false 4 Text 0 0 ,First,#," + CO_txt +",Field13,-1,-1;LONG_SECS \"LONG_SECS\" true true false 8 Text 0 0 ,First,#," + CO_txt +",Field14,-1,-1", "")

    # Process: Make Table View
    arcpy.MakeTableView_management(FCC_ASR_TOWER_CO, FCC_ASR_TOWER_CO_view, "LAT_DEGREES is not null or LAT_DEGREES <> 0", FCC_ASR_TOWER_gdb, "REGISTRATION_NUMBER REGISTRATION_NUMBER VISIBLE NONE;UNIQUE_SYSTEM_IDENTIFIER UNIQUE_SYSTEM_IDENTIFIER VISIBLE NONE;COORDINATE_TYPE COORDINATE_TYPE VISIBLE NONE;LAT_DEGREES LAT_DEGREES VISIBLE NONE;LAT_MINS LAT_MINS VISIBLE NONE;LAT_SECS LAT_SECS VISIBLE NONE;LONG_DEGREES LONG_DEGREES VISIBLE NONE;LONG_MINS LONG_MINS VISIBLE NONE;LONG_SECS LONG_SECS VISIBLE NONE")

    # Process: Table to Table (4)
    arcpy.TableToTable_conversion(EN_txt, FCC_ASR_TOWER_gdb, "FCC_ASR_TOWER_EN", "", "REGISTRATION_NUMBER \"REGISTRATION_NUMBER\" true true false 4 Long 0 0 ,First,#," + EN_txt +",Field4,-1,-1;UNIQUE_SYSTEM_IDENTIFIER \"UNIQUE_SYSTEM_IDENTIFIER\" true true false 4 Long 0 0 ,First,#," + EN_txt +",Field5,-1,-1;ENTITY_TYPE \"ENTITY_TYPE\" true true false 255 Text 0 0 ,First,#," + EN_txt +",Field7,-1,-1;LICENSEE_ID \"LICENSEE_ID\" true true false 255 Text 0 0 ,First,#," + EN_txt +",Field9,-1,-1;ENTITY_NAME \"ENTITY_NAME\" true true false 255 Text 0 0 ,First,#," + EN_txt +",Field10,-1,-1;ENTITY_POC \"ENTITY_POC\" true true false 255 Text 0 0 ,First,#," + EN_txt +",Field11,-1,-1;ENTITY_POC_2 \"ENTITY_POC_2\" true true false 255 Text 0 0 ,First,#," + EN_txt +",Field13,-1,-1;ENTITY_POC_3 \"ENTITY_POC_3\" true true false 255 Text 0 0 ,First,#," + EN_txt +",Field14,-1,-1;ENTITY_PHONE \"ENTITY_PHONE\" true true false 20 Text 0 0 ,First,#," + EN_txt +",Field15,-1,-1;ENTITY_FAX \"ENTITY_FAX\" true true false 20 Text 0 0 ,First,#," + EN_txt +",Field16,-1,-1;ENTITY_EMAIL \"ENTITY_EMAIL\" true true false 255 Text 0 0 ,First,#," + EN_txt +",Field17,-1,-1;ENTITY_STREET_ADDRESS \"ENTITY_STREET_ADDRESS\" true true false 255 Text 0 0 ,First,#," + EN_txt +",Field18,-1,-1;ENTITY_STREET_ADDRESS_2 \"ENTITY_STREET_ADDRESS_2\" true true false 255 Text 0 0 ,First,#," + EN_txt +",Field19,-1,-1;ENTITY_PO_BOX \"ENTITY_PO_BOX\" true true false 255 Text 0 0 ,First,#," + EN_txt +",Field20,-1,-1;ENTITY_CITY \"ENTITY_CITY\" true true false 255 Text 0 0 ,First,#," + EN_txt +",Field21,-1,-1;ENTITY_STATE \"ENTITY_STATE\" true true false 255 Text 0 0 ,First,#," + EN_txt +",Field22,-1,-1;ENTITY_ZIP_CODE \"ENTITY_ZIP_CODE\" true true false 20 Text 0 0 ,First,#," + EN_txt +",Field23,-1,-1", "")

    # Process: Make Table View
    arcpy.MakeTableView_management(FCC_ASR_TOWER_EN, FCC_ASR_TOWER_EN_view, "", FCC_ASR_TOWER_gdb, "REGISTRATION_NUMBER REGISTRATION_NUMBER VISIBLE NONE;UNIQUE_SYSTEM_IDENTIFIER UNIQUE_SYSTEM_IDENTIFIER VISIBLE NONE;ENTITY_TYPE ENTITY_TYPE VISIBLE NONE;LICENSEE_ID LICENSEE_ID VISIBLE NONE;ENTITY_NAME ENTITY_NAME VISIBLE NONE;ENTITY_POC ENTITY_POC VISIBLE NONE;ENTITY_POC_2 ENTITY_POC_2 VISIBLE NONE;ENTITY_POC_3 ENTITY_POC_3 VISIBLE NONE;ENTITY_PHONE ENTITY_PHONE VISIBLE NONE;ENTITY_FAX ENTITY_FAX VISIBLE NONE;ENTITY_EMAIL ENTITY_EMAIL VISIBLE NONE;ENTITY_STREET_ADDRESS ENTITY_STREET_ADDRESS VISIBLE NONE;ENTITY_STREET_ADDRESS_2 ENTITY_STREET_ADDRESS_2 VISIBLE NONE;ENTITY_PO_BOX ENTITY_PO_BOX VISIBLE NONE;ENTITY_CITY ENTITY_CITY VISIBLE NONE;ENTITY_STATE ENTITY_STATE VISIBLE NONE;ENTITY_ZIP_CODE ENTITY_ZIP_CODE VISIBLE NONE")

    # Process: Table to Table (2)
    arcpy.TableToTable_conversion(RA_txt, FCC_ASR_TOWER_gdb, "FCC_ASR_TOWER_RA", "", "REGISTRATION_NUMBER \"REGISTRATION_NUMBER\" true true false 4 Long 0 0 ,First,#," + RA_txt +",Field4,-1,-1;UNIQUE_SYSTEM_IDENTIFIER \"UNIQUE_SYSTEM_IDENTIFIER\" true true false 4 Long 0 0 ,First,#," + RA_txt +",Field5,-1,-1;DATE_CONSTRUCTED \"DATE_CONSTRUCTED\" true true false 8 Date 0 0 ,First,#," + RA_txt +",Field13,-1,-1;DATE_DISMANTLED \"DATE_DISMANTLED\" true true false 8 Date 0 0 ,First,#," + RA_txt +",Field14,-1,-1;STRUCTURE_STREET_ADDRESS \"STRUCTURE_STREET_ADDRESS\" true true false 255 Text 0 0 ,First,#," + RA_txt +",Field24,-1,-1;STRUCTURE_CITY \"STRUCTURE_CITY\" true true false 255 Text 0 0 ,First,#," + RA_txt +",Field25,-1,-1;STRUCTURE_STATE \"STRUCTURE_STATE\" true true false 255 Text 0 0 ,First,#," + RA_txt +",Field26,-1,-1;STRUCTURE_COUNTY \"STRUCTURE_COUNTY\" true true false 255 Text 0 0 ,First,#," + RA_txt +",Field27,-1,-1;STRUCTURE_ZIP_CODE \"STRUCTURE_ZIP_CODE\" true true false 20 Text 0 0 ,First,#," + RA_txt +",Field28,-1,-1;HEIGHT_OF_STRUCTURE \"HEIGHT_OF_STRUCTURE\" true true false 8 Double 0 0 ,First,#," + RA_txt +",Field29,-1,-1;GROUND_ELEVATION \"GROUND_ELEVATION\" true true false 8 Double 0 0 ,First,#," + RA_txt +",Field30,-1,-1;OVERALL_HEIGHT_ABOVE_GROUND \"OVERALL_HEIGHT_ABOVE_GROUND\" true true false 8 Double 0 0 ,First,#," + RA_txt +",Field31,-1,-1;OVERALL_HEIGHT_AMSL \"OVERALL_HEIGHT_AMSL\" true true false 8 Double 0 0 ,First,#," + RA_txt +",Field32,-1,-1;STRUCTURE_TYPE \"STRUCTURE_TYPE\" true true false 255 Text 0 0 ,First,#," + RA_txt +",Field33,-1,-1;FAA_STUDY_NUMBER \"FAA_STUDY_NUMBER\" true true false 255 Text 0 0 ,First,#," + RA_txt +",Field35,-1,-1;FAA_CIRCULAR_NUMBER \"FAA_CIRCULAR_NUMBER\" true true false 255 Text 0 0 ,First,#," + RA_txt +",Field36,-1,-1;SPECIFICATION_OPTION \"SPECIFICATION_OPTION\" true true false 20 Text 0 0 ,First,#," + RA_txt +",Field37,-1,-1;PAINTING_AND_LIGHTING \"PAINTING_AND_LIGHTING\" true true false 255 Text 0 0 ,First,#," + RA_txt +",Field38,-1,-1;MARK_LIGHT_CODE \"MARK_LIGHT_CODE\" true true false 20 Text 0 0 ,First,#," + RA_txt +",Field39,-1,-1;MARK_LIGHT_CODE_OTHER \"MARK_LIGHT_CODE_OTHER\" true true false 255 Text 0 0 ,First,#," + RA_txt +",Field40,-1,-1", "")

    # Process: Make Table View (3)
    arcpy.MakeTableView_management(FCC_ASR_TOWER_RA, FCC_ASR_TOWER_RA_view, "", FCC_ASR_TOWER_gdb, "REGISTRATION_NUMBER REGISTRATION_NUMBER VISIBLE NONE;UNIQUE_SYSTEM_IDENTIFIER UNIQUE_SYSTEM_IDENTIFIER VISIBLE NONE;DATE_CONSTRUCTED DATE_CONSTRUCTED VISIBLE NONE;DATE_DISMANTLED DATE_DISMANTLED VISIBLE NONE;STRUCTURE_STREET_ADDRESS STRUCTURE_STREET_ADDRESS VISIBLE NONE;STRUCTURE_CITY STRUCTURE_CITY VISIBLE NONE;STRUCTURE_STATE STRUCTURE_STATE VISIBLE NONE;STRUCTURE_COUNTY STRUCTURE_COUNTY VISIBLE NONE;STRUCTURE_ZIP_CODE STRUCTURE_ZIP_CODE VISIBLE NONE;HEIGHT_OF_STRUCTURE HEIGHT_OF_STRUCTURE VISIBLE NONE;GROUND_ELEVATION GROUND_ELEVATION VISIBLE NONE;OVERALL_HEIGHT_ABOVE_GROUND OVERALL_HEIGHT_ABOVE_GROUND VISIBLE NONE;OVERALL_HEIGHT_AMSL OVERALL_HEIGHT_AMSL VISIBLE NONE;STRUCTURE_TYPE STRUCTURE_TYPE VISIBLE NONE;FAA_STUDY_NUMBER FAA_STUDY_NUMBER VISIBLE NONE;FAA_CIRCULAR_NUMBER FAA_CIRCULAR_NUMBER VISIBLE NONE;SPECIFICATION_OPTION SPECIFICATION_OPTION VISIBLE NONE;PAINTING_AND_LIGHTING PAINTING_AND_LIGHTING VISIBLE NONE;MARK_LIGHT_CODE MARK_LIGHT_CODE VISIBLE NONE;MARK_LIGHT_CODE_OTHER MARK_LIGHT_CODE_OTHER VISIBLE NONE")

    arcpy.AddMessage("Import Complete" )
    arcpy.AddMessage("Indexing and Joining..." )

    # Process: Add Attribute Index
    arcpy.AddIndex_management(FCC_ASR_TOWER_CO_view, "UNIQUE_SYSTEM_IDENTIFIER", "CO", "NON_UNIQUE", "NON_ASCENDING")

    # Process: Add Attribute Index (2)
    arcpy.AddIndex_management(FCC_ASR_TOWER_EN_view, "REGISTRATION_NUMBER;UNIQUE_SYSTEM_IDENTIFIER", "EN", "NON_UNIQUE", "NON_ASCENDING")

    # Process: Add Attribute Index (3)
    arcpy.AddIndex_management(FCC_ASR_TOWER_RA_view, "REGISTRATION_NUMBER", "RA", "NON_UNIQUE", "NON_ASCENDING")

    # Process: Add Join
    arcpy.AddJoin_management(FCC_ASR_TOWER_EN_view, "UNIQUE_SYSTEM_IDENTIFIER", FCC_ASR_TOWER_CO_view, "UNIQUE_SYSTEM_IDENTIFIER", "KEEP_ALL")

    # Process: Add Join (2)
    arcpy.AddJoin_management(FCC_ASR_TOWER_EN_view, "REGISTRATION_NUMBER", FCC_ASR_TOWER_RA_view, "REGISTRATION_NUMBER", "KEEP_ALL")

    arcpy.AddMessage("Copying Join..." )

    # Process: Copy Rows
    arcpy.CopyRows_management(FCC_ASR_TOWER_EN_view, FCC_ASR_TOWER_JOIN, "")

    # Process: Delete View
    arcpy.Delete_management(FCC_ASR_TOWER_EN_view, "")

    # Process: Delete View
    arcpy.Delete_management(FCC_ASR_TOWER_CO_view, "")

    # Process: Delete View
    arcpy.Delete_management(FCC_ASR_TOWER_RA_view, "")

    arcpy.AddMessage("Copy Complete" )

    arcpy.AddMessage("Generating Geometry..." )

    # Process: Add Field
    arcpy.AddField_management(FCC_ASR_TOWER_JOIN, "LONG_DMS", "TEXT", "", "", "", "LONG_DMS", "NULLABLE", "NON_REQUIRED", "")

    # Process: Add Field (2)
    arcpy.AddField_management(FCC_ASR_TOWER_JOIN, "LAT_DMS", "TEXT", "", "", "", "LAT_DMS", "NULLABLE", "NON_REQUIRED", "")

    # Process: Calculate Field
    arcpy.CalculateField_management(FCC_ASR_TOWER_JOIN, "LONG_DMS","\"-\"+ !FCC_ASR_TOWER_CO_LONG_DEGREES! +\" \" + !FCC_ASR_TOWER_CO_LONG_MINS! + \" \"+ !FCC_ASR_TOWER_CO_LONG_SECS!", "PYTHON_9.3", "")

    # Process: Calculate Field
    arcpy.CalculateField_management(FCC_ASR_TOWER_JOIN, "LAT_DMS", "!FCC_ASR_TOWER_CO_LAT_DEGREES! +\" \" + !FCC_ASR_TOWER_CO_LAT_MINS! +\" \"+ !FCC_ASR_TOWER_CO_LAT_SECS!", "PYTHON_9.3", "")

    # Process: Delete Field
    arcpy.DeleteField_management(FCC_ASR_TOWER_JOIN, "FCC_ASR_TOWER_CO_OBJECTID;FCC_ASR_TOWER_CO_REGISTRATION_NUMBER;FCC_ASR_TOWER_CO_UNIQUE_SYSTEM_IDENTIFIER;FCC_ASR_TOWER_RA_OBJECTID;FCC_ASR_TOWER_RA_REGISTRATION_NUMBER;FCC_ASR_TOWER_RA_UNIQUE_SYSTEM_IDENTIFIER")

    # Process: Convert Coordinate Notation
    arcpy.ConvertCoordinateNotation_management(FCC_ASR_TOWER_JOIN, FCC_ASR_TOWER_XY, "LONG_DMS", "LAT_DMS", "DMS_2", "DD_2", "", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision")

    # Process: Calculate Field
    arcpy.CalculateField_management(FCC_ASR_TOWER_XY, "DDLat", "!DDLat!.replace(\"N\", \"\")", "PYTHON_9.3", "")

    # Process: Calculate Field
    arcpy.CalculateField_management(FCC_ASR_TOWER_XY, "DDLon", "!DDLon!.replace(\"W\", \"\")", "PYTHON_9.3", "")

    arcpy.AddMessage("Geometry Complete" )

    cur = arcpy.UpdateCursor(FCC_ASR_TOWER_XY)
    row = cur.next()
    while row:
        # Get the value of the field the calculation will be based on...
        sn_null = str(row.getValue("FCC_ASR_TOWER_RA_STRUCTURE_COUNTY"))
        if sn_null != "Null":
            sn = sn_null
        # Conditional Statements
        # if the field1 = value1, set field2 to equal NewVal1, etc...
        if sn_null == "Null":
            row.setValue("FCC_ASR_TOWER_RA_STRUCTURE_COUNTY", None )
            cur.updateRow(row)
        row = cur.next()
    del cur, row


    cur = arcpy.UpdateCursor(FCC_ASR_TOWER_XY)
    row = cur.next()
    while row:
        # Get the value of the field the calculation will be based on...
        sn_null = str(row.getValue("DDLat"))
        if sn_null != "":
            sn = sn_null
        # Conditional Statements
        # if the field1 = value1, set field2 to equal NewVal1, etc...
        if sn_null == "":
            row.setValue("DDLat", None )
            cur.updateRow(row)
        row = cur.next()
    del cur, row

    cur = arcpy.UpdateCursor(FCC_ASR_TOWER_XY)
    row = cur.next()
    while row:
        # Get the value of the field the calculation will be based on...
        sn_null = str(row.getValue("DDLon"))
        if sn_null != "":
            sn = sn_null
        # Conditional Statements
        # if the field1 = value1, set field2 to equal NewVal1, etc...
        if sn_null == "":
            row.setValue("DDLon", None )
            cur.updateRow(row)
        row = cur.next()
    del cur, row

    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(FCC_ASR_TOWER_XY, FCC_ASR_TOWER_XY_lyr, "DDLat <> ''", "", "OID OID VISIBLE NONE;Shape Shape VISIBLE NONE;FCC_ASR_TOWER_EN_REGISTRATION_NUMBER FCC_ASR_TOWER_EN_REGISTRATION_NUMBER VISIBLE NONE;FCC_ASR_TOWER_EN_UNIQUE_SYSTEM_IDENTIFIER FCC_ASR_TOWER_EN_UNIQUE_SYSTEM_IDENTIFIER VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_TYPE FCC_ASR_TOWER_EN_ENTITY_TYPE VISIBLE NONE;FCC_ASR_TOWER_EN_LICENSEE_ID FCC_ASR_TOWER_EN_LICENSEE_ID VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_NAME FCC_ASR_TOWER_EN_ENTITY_NAME VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_POC FCC_ASR_TOWER_EN_ENTITY_POC VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_POC_2 FCC_ASR_TOWER_EN_ENTITY_POC_2 VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_POC_3 FCC_ASR_TOWER_EN_ENTITY_POC_3 VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_PHONE FCC_ASR_TOWER_EN_ENTITY_PHONE VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_FAX FCC_ASR_TOWER_EN_ENTITY_FAX VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_EMAIL FCC_ASR_TOWER_EN_ENTITY_EMAIL VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_STREET_ADDRESS FCC_ASR_TOWER_EN_ENTITY_STREET_ADDRESS VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_STREET_ADDRESS_2 FCC_ASR_TOWER_EN_ENTITY_STREET_ADDRESS_2 VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_PO_BOX FCC_ASR_TOWER_EN_ENTITY_PO_BOX VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_CITY FCC_ASR_TOWER_EN_ENTITY_CITY VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_STATE FCC_ASR_TOWER_EN_ENTITY_STATE VISIBLE NONE;FCC_ASR_TOWER_EN_ENTITY_ZIP_CODE FCC_ASR_TOWER_EN_ENTITY_ZIP_CODE VISIBLE NONE;FCC_ASR_TOWER_CO_COORDINATE_TYPE FCC_ASR_TOWER_CO_COORDINATE_TYPE VISIBLE NONE;FCC_ASR_TOWER_CO_LAT_DEGREES FCC_ASR_TOWER_CO_LAT_DEGREES VISIBLE NONE;FCC_ASR_TOWER_CO_LAT_MINS FCC_ASR_TOWER_CO_LAT_MINS VISIBLE NONE;FCC_ASR_TOWER_CO_LAT_SECS FCC_ASR_TOWER_CO_LAT_SECS VISIBLE NONE;FCC_ASR_TOWER_CO_LONG_DEGREES FCC_ASR_TOWER_CO_LONG_DEGREES VISIBLE NONE;FCC_ASR_TOWER_CO_LONG_MINS FCC_ASR_TOWER_CO_LONG_MINS VISIBLE NONE;FCC_ASR_TOWER_CO_LONG_SECS FCC_ASR_TOWER_CO_LONG_SECS VISIBLE NONE;FCC_ASR_TOWER_RA_DATE_CONSTRUCTED FCC_ASR_TOWER_RA_DATE_CONSTRUCTED VISIBLE NONE;FCC_ASR_TOWER_RA_DATE_DISMANTLED FCC_ASR_TOWER_RA_DATE_DISMANTLED VISIBLE NONE;FCC_ASR_TOWER_RA_STRUCTURE_STREET_ADDRESS FCC_ASR_TOWER_RA_STRUCTURE_STREET_ADDRESS VISIBLE NONE;FCC_ASR_TOWER_RA_STRUCTURE_CITY FCC_ASR_TOWER_RA_STRUCTURE_CITY VISIBLE NONE;FCC_ASR_TOWER_RA_STRUCTURE_STATE FCC_ASR_TOWER_RA_STRUCTURE_STATE VISIBLE NONE;FCC_ASR_TOWER_RA_STRUCTURE_COUNTY FCC_ASR_TOWER_RA_STRUCTURE_COUNTY VISIBLE NONE;FCC_ASR_TOWER_RA_STRUCTURE_ZIP_CODE FCC_ASR_TOWER_RA_STRUCTURE_ZIP_CODE VISIBLE NONE;FCC_ASR_TOWER_RA_HEIGHT_OF_STRUCTURE FCC_ASR_TOWER_RA_HEIGHT_OF_STRUCTURE VISIBLE NONE;FCC_ASR_TOWER_RA_GROUND_ELEVATION FCC_ASR_TOWER_RA_GROUND_ELEVATION VISIBLE NONE;FCC_ASR_TOWER_RA_OVERALL_HEIGHT_ABOVE_GROUND FCC_ASR_TOWER_RA_OVERALL_HEIGHT_ABOVE_GROUND VISIBLE NONE;FCC_ASR_TOWER_RA_OVERALL_HEIGHT_AMSL FCC_ASR_TOWER_RA_OVERALL_HEIGHT_AMSL VISIBLE NONE;FCC_ASR_TOWER_RA_STRUCTURE_TYPE FCC_ASR_TOWER_RA_STRUCTURE_TYPE VISIBLE NONE;FCC_ASR_TOWER_RA_FAA_STUDY_NUMBER FCC_ASR_TOWER_RA_FAA_STUDY_NUMBER VISIBLE NONE;FCC_ASR_TOWER_RA_FAA_CIRCULAR_NUMBER FCC_ASR_TOWER_RA_FAA_CIRCULAR_NUMBER VISIBLE NONE;FCC_ASR_TOWER_RA_SPECIFICATION_OPTION FCC_ASR_TOWER_RA_SPECIFICATION_OPTION VISIBLE NONE;FCC_ASR_TOWER_RA_PAINTING_AND_LIGHTING FCC_ASR_TOWER_RA_PAINTING_AND_LIGHTING VISIBLE NONE;FCC_ASR_TOWER_RA_MARK_LIGHT_CODE FCC_ASR_TOWER_RA_MARK_LIGHT_CODE VISIBLE NONE;FCC_ASR_TOWER_RA_MARK_LIGHT_CODE_OTHER FCC_ASR_TOWER_RA_MARK_LIGHT_CODE_OTHER VISIBLE NONE;LONG_DMS LONG_DMS VISIBLE NONE;LAT_DMS LAT_DMS VISIBLE NONE;DDLat DDLat VISIBLE NONE;DDLon DDLon VISIBLE NONE")

    #Process: Append to Schema
    arcpy.Append_management(FCC_ASR_TOWER_XY_lyr, Metadata_and_schema, "NO_TEST", "REGISTRATION_NUMBER \"REGISTRATION_NUMBER\" true true false 4 Long 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_REGISTRATION_NUMBER,-1,-1;UNIQUE_SYSTEM_IDENTIFIER \"UNIQUE_SYSTEM_IDENTIFIER\" true true false 4 Long 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_UNIQUE_SYSTEM_IDENTIFIER,-1,-1;LICENSEE_ID \"LICENSEE_ID\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_LICENSEE_ID,-1,-1;ENTITY_NAME \"ENTITY_NAME\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_NAME,-1,-1;ENTITY_POC \"ENTITY_POC\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_POC,-1,-1;ENTITY_POC_2 \"ENTITY_POC_2\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_POC_2,-1,-1;ENTITY_POC_3 \"ENTITY_POC_3\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_POC_3,-1,-1;ENTITY_FAX \"ENTITY_FAX\" true true false 8 Double 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_FAX,-1,-1;ENTITY_PHONE \"ENTITY_PHONE\" true true false 8 Double 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_PHONE,-1,-1;ENTITY_EMAIL \"ENTITY_EMAIL\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_EMAIL,-1,-1;ENTITY_STREET_ADDRESS \"ENTITY_STREET_ADDRESS\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_STREET_ADDRESS,-1,-1;ENTITY_STREET_ADDRESS_1 \"ENTITY_STREET_ADDRESS_1\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_STREET_ADDRESS_2,-1,-1;ENTITY_PO_BOX \"ENTITY_PO_BOX\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_PO_BOX,-1,-1;ENTITY_STATE \"ENTITY_STATE\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_STATE,-1,-1;ENTITY_TYPE \"ENTITY_TYPE\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_TYPE,-1,-1;ENTITY_CITY \"ENTITY_CITY\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_CITY,-1,-1;ENTITY_ZIP_CODE \"ENTITY_ZIP_CODE\" true true false 4 Long 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_EN_ENTITY_ZIP_CODE,-1,-1;COORDINATE_TYPE \"COORDINATE_TYPE\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_CO_COORDINATE_TYPE,-1,-1;LAT_DEGREES \"LAT_DEGREES\" true true false 4 Long 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_CO_LAT_DEGREES,-1,-1;LONG_DEGREES \"LONG_DEGREES\" true true false 4 Long 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_CO_LONG_DEGREES,-1,-1;LAT_MIN \"LAT_MIN\" true true false 4 Long 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_CO_LAT_MINS,-1,-1;LAT_SECS \"LAT_SECS\" true true false 8 Double 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_CO_LAT_SECS,-1,-1;LONG_MINS \"LONG_MINS\" true true false 4 Long 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_CO_LONG_MINS,-1,-1;LONG_SECS \"LONG_SECS\" true true false 8 Double 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_CO_LONG_SECS,-1,-1;HEIGHT_OF_STRUCTURE \"HEIGHT_OF_STRUCTURE\" true true false 8 Double 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_HEIGHT_OF_STRUCTURE,-1,-1;GROUND_ELEVATION \"GROUND_ELEVATION\" true true false 8 Double 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_GROUND_ELEVATION,-1,-1;PAINTING_AND_LIGHTING \"PAINTING_AND_LIGHTING\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_PAINTING_AND_LIGHTING,-1,-1;MARK_LIGHT_CODE \"MARK_LIGHT_CODE\" true true false 4 Long 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_MARK_LIGHT_CODE,-1,-1;MARK_LIGHT_OTHER \"MARK_LIGHT_OTHER\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_MARK_LIGHT_CODE_OTHER,-1,-1;DATE_CONSTRUCTED \"DATE_CONSTRUCTED\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_DATE_CONSTRUCTED,-1,-1;DATE_DISMANTLED \"DATE_DISMANTLED\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_DATE_DISMANTLED,-1,-1;OVERALL_HEIGHT_ABOVE_GROUND \"OVERALL_HEIGHT_ABOVE_GROUND\" true true false 8 Double 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_OVERALL_HEIGHT_ABOVE_GROUND,-1,-1;OVERALL_HEIGHT_AMSL \"OVERALL_HEIGHT_AMSL\" true true false 8 Double 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_OVERALL_HEIGHT_AMSL,-1,-1;FAA_STUDY_NUMBER \"FAA_STUDY_NUMBER\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_FAA_STUDY_NUMBER,-1,-1;FAA_CIRCULAR_NUMBER \"FAA_CIRCULAR_NUMBER\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_FAA_CIRCULAR_NUMBER,-1,-1;SPECIFICATION_OPTION \"SPECIFICATION_OPTION\" true true false 4 Long 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_SPECIFICATION_OPTION,-1,-1;STRUCTURE_TYPE \"STRUCTURE_TYPE\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_STRUCTURE_TYPE,-1,-1;STRUCTURE_STREET_ADDRESS \"STRUCTURE_STREET_ADDRESS\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_STRUCTURE_STREET_ADDRESS,-1,-1;STRUCTURE_STATE_CODE \"STRUCTURE_STATE_CODE\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_STRUCTURE_STATE,-1,-1;STRUCTURE_COUNTY \"STRUCTURE_COUNTY\" true true false 4 Long 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_STRUCTURE_COUNTY,-1,-1;STRUCTURE_CITY \"STRUCTURE_CITY\" true true false 255 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_STRUCTURE_CITY,-1,-1;STRUCTURE_ZIP_CODE \"STRUCTURE_ZIP_CODE\" true true false 4 Long 0 0 ,First,#," + FCC_ASR_TOWER_XY +",FCC_ASR_TOWER_RA_STRUCTURE_ZIP_CODE,-1,-1;LongDMS \"LongDMS\" true true false 50 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",LONG_DMS,-1,-1;LatDMS \"LatDMS\" true true false 50 Text 0 0 ,First,#," + FCC_ASR_TOWER_XY +",LAT_DMS,-1,-1;LongDD \"LongDD\" true true false 8 Double 0 0 ,First,#," + FCC_ASR_TOWER_XY +",DDLon,-1,-1;LatDD \"LatDD\" true true false 8 Double 0 0 ,First,#," + FCC_ASR_TOWER_XY +",DDLat,-1,-1", "")

    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(Metadata_and_schema, Metadata_and_schema_lyr, "", "", "OBJECTID OBJECTID VISIBLE NONE;REGISTRATION_NUMBER REGISTRATION_NUMBER VISIBLE NONE;UNIQUE_SYSTEM_IDENTIFIER UNIQUE_SYSTEM_IDENTIFIER VISIBLE NONE;LICENSEE_ID LICENSEE_ID VISIBLE NONE;ENTITY_NAME ENTITY_NAME VISIBLE NONE;ENTITY_POC ENTITY_POC VISIBLE NONE;ENTITY_POC_2 ENTITY_POC_2 VISIBLE NONE;ENTITY_POC_3 ENTITY_POC_3 VISIBLE NONE;ENTITY_FAX ENTITY_FAX VISIBLE NONE;ENTITY_PHONE ENTITY_PHONE VISIBLE NONE;ENTITY_EMAIL ENTITY_EMAIL VISIBLE NONE;ENTITY_STREET_ADDRESS ENTITY_STREET_ADDRESS VISIBLE NONE;ENTITY_STREET_ADDRESS_1 ENTITY_STREET_ADDRESS_1 VISIBLE NONE;ENTITY_PO_BOX ENTITY_PO_BOX VISIBLE NONE;ENTITY_STATE ENTITY_STATE VISIBLE NONE;ENTITY_TYPE ENTITY_TYPE VISIBLE NONE;ENTITY_CITY ENTITY_CITY VISIBLE NONE;ENTITY_ZIP_CODE ENTITY_ZIP_CODE VISIBLE NONE;COORDINATE_TYPE COORDINATE_TYPE VISIBLE NONE;LAT_DEGREES LAT_DEGREES VISIBLE NONE;LONG_DEGREES LONG_DEGREES VISIBLE NONE;LAT_MIN LAT_MIN VISIBLE NONE;LAT_SECS LAT_SECS VISIBLE NONE;LONG_MINS LONG_MINS VISIBLE NONE;LONG_SECS LONG_SECS VISIBLE NONE;HEIGHT_OF_STRUCTURE HEIGHT_OF_STRUCTURE VISIBLE NONE;GROUND_ELEVATION GROUND_ELEVATION VISIBLE NONE;PAINTING_AND_LIGHTING PAINTING_AND_LIGHTING VISIBLE NONE;MARK_LIGHT_CODE MARK_LIGHT_CODE VISIBLE NONE;MARK_LIGHT_OTHER MARK_LIGHT_OTHER VISIBLE NONE;DATE_CONSTRUCTED DATE_CONSTRUCTED VISIBLE NONE;DATE_DISMANTLED DATE_DISMANTLED VISIBLE NONE;OVERALL_HEIGHT_ABOVE_GROUND OVERALL_HEIGHT_ABOVE_GROUND VISIBLE NONE;OVERALL_HEIGHT_AMSL OVERALL_HEIGHT_AMSL VISIBLE NONE;FAA_STUDY_NUMBER FAA_STUDY_NUMBER VISIBLE NONE;FAA_CIRCULAR_NUMBER FAA_CIRCULAR_NUMBER VISIBLE NONE;SPECIFICATION_OPTION SPECIFICATION_OPTION VISIBLE NONE;STRUCTURE_TYPE STRUCTURE_TYPE VISIBLE NONE;STRUCTURE_STREET_ADDRESS STRUCTURE_STREET_ADDRESS VISIBLE NONE;STRUCTURE_STATE_CODE STRUCTURE_STATE_CODE VISIBLE NONE;STRUCTURE_COUNTY STRUCTURE_COUNTY VISIBLE NONE;STRUCTURE_CITY STRUCTURE_CITY VISIBLE NONE;STRUCTURE_ZIP_CODE STRUCTURE_ZIP_CODE VISIBLE NONE;LongDMS LongDMS VISIBLE NONE;LatDMS LatDMS VISIBLE NONE;LongDD LongDD VISIBLE NONE;LatDD LatDD VISIBLE NONE;Shape Shape VISIBLE NONE")

    # Process: Select Layer By Attribute
    arcpy.SelectLayerByAttribute_management(Metadata_and_schema_lyr, "NEW_SELECTION", "STRUCTURE_STATE_CODE = '" + State + "'")

    arcpy.AddMessage("Exporting State Subset..." )

    # Process: Feature Class to Feature Class
    arcpy.FeatureClassToFeatureClass_conversion(Metadata_and_schema_lyr, FCC_ASR_TOWER_gdb, "FCC_ASR_TOWER_"+State, "", "", "")

    # Process: Select Layer By Attribute
    arcpy.SelectLayerByAttribute_management(Metadata_and_schema_lyr, "CLEAR_SELECTION", "")

    arcpy.AddMessage("Exporting Complete Dataset..." )

    # Process: Feature Class to Feature Class
    arcpy.FeatureClassToFeatureClass_conversion(Metadata_and_schema_lyr, FCC_ASR_TOWER_gdb, "FCC_ASR_TOWER_ALL", "", "", "")

    arcpy.DeleteFeatures_management(Metadata_and_schema)
    arcpy.Delete_management(FCC_ASR_TOWER_XY)
    arcpy.Delete_management(FCC_ASR_TOWER_EN)
    arcpy.Delete_management(FCC_ASR_TOWER_RA)
    arcpy.Delete_management(FCC_ASR_TOWER_JOIN)
    arcpy.Delete_management(FCC_ASR_TOWER_CO)

    shutil.rmtree(unzipFolder)
    os.remove(savedZip)

    arcpy.AddMessage("Script Complete" )



