# -*- coding: utf-8 -*-
"""
Created on Thu Jul 07 16:45:03 2016

@author: Yiting
"""

"""
this program is used to join csv table to shapefile (map)
"""

import arcpy
import os
# comtypes package is used to generate MXD file
import comtypes

def JoinTableShp(path, out_features)

#%%

    arcpy.AddMessage(arcpy.ProductInfo())
    # check out extension
    try:
        ext = 'Spatial' 
        arcpy.CheckOutExtension(ext)
    except:
        print  ext + 'license is unavailable.'
            
    # need to be able to overwrite outputs
    arcpy.env.overwriteOutput = True
    

#%%
    # geoprocessor variables
    
    try:   
        print 'start processing...'
        # set workspace
        arcpy.env.workspace = "F:/fresno_sample/output" 
        
        # set up variables
        out_folder_path = "F:/fresno_sample/output"
        out_name = "result"
        
        # execute create file gdb
        arcpy.CreateFileGDB_management(out_folder_path, out_name)
        
        # get the last message from the last tool to check out the process
        #count = arcpy.GetMessageCount()
        #print arcpy.GetMessage(count-1)
        # if success
        print "env setting success..."
        
    except:
        print "Env setting failed"
    
#%%  
    # create MXD document in current workspace
    
    def CreateMXD(path):
        GetModule('esriCarto.olb')
        import comtypes.gen.esriCarto as esriCarto
        pMapDocument = CreateObject(esriCarto.MapDocument, esriCarto.IMapDocument)
        pMapDocument.New(path)
        pMapDocument.Save()
        
    def GetLibPath():
        """ Get the ArcObjects library path
        """
        compath = os.path.join(arcpy.GetInstallInfo()['InstallDir'],'com')
        return compath
    
    def GetModule(sModuleName):
        """ generate (if not already done) wrappers for COM modules
        """
        from comtypes.client import GetModule
        sLibPath = GetLibPath()
        GetModule(os.path.join(sLibPath, sModuleName))
        
    def CreateObject(COMClass, COMInterface):
        """ creates a new comtypes POINTER object where
            COMClass is the class to be instantiated,
            COMInterface is the interface to be assigned
        """
        ptr = comtypes.client.CreateObject(COMClass, interface = COMInterface)
        return ptr
    
    try:
        # set the path to create new MXD file 
        MXD_name = "fresno" 
        MXD_path = out_folder_path + "/" + out_name + ".gdb/" + MXD_name + ".mxd"
        #print MXD_path
        # ---------------------excuate function CreateMXD ----------------------  
        CreateMXD(MXD_path)
        #-----------------------------------------------------------------------
        
        #count = arcpy.GetMessageCount()
        #print arcpy.GetMessage(count-1)
        print 'create mxd success...'
    
    except Exception as err:
        print(err.args[0])
    

#%%
    # create layer in MXD created in last step
    try:
        # locate MXD file
        # MXD - loop variable
        MXD = arcpy.mapping.MapDocument(r"F:/fresno_sample/output/result.gdb/fresno.mxd")
        
        # input shapefile
        # shape_path - loop variable
        #shape = '"F:/fresno_sample/TAZ_Fresno_081211.shp"'
        #shape_path = 'r' + shape
        shape_path = r"F:/fresno_sample/TAZ_Fresno_081211.shp"
        # table_path - loop variable
        #table = '"F:/fresno_sample/FC14_BASE_SE_Detail_out.csv"'
        #table_path = 'r' + table
        table_path = r"F:/fresno_sample/FC14_BASE_SE_Detail_out.csv"
        
        # choose data_frame which need to be added
        df = arcpy.mapping.ListDataFrames(MXD, "*")[0]
        
        # create a new layer (shapefile as layer)
        shape_1 = arcpy.mapping.Layer(shape_path)
        table_1 = arcpy.mapping.TableView(table_path)
        
        # add the layer to the map at the bottom of the TOC in data frame 0
        arcpy.mapping.AddLayer(df, shape_1, "BOTTOM")
        arcpy.mapping.AddTableView(df, table_1)
        
        # refresh things
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()
        
        print 'add shp and table success...'
        
    except Exception as err:
        print(err.args[0])
    
    MXD.saveACopy(r"F:/fresno_sample/output/result.gdb/" + MXD_name + "_new.mxd")
    
    del MXD


#%%
    # join table and shapefile which exported in the last step
    
    # locate MXD file
    # MXD - loop variable
    MXD = arcpy.mapping.MapDocument(r"F:/fresno_sample/output/result.gdb/fresno_new.mxd")
    
    # name of joined layer
    in_features = "shape_lay"
    join_table = "table_view"
    # based on what field to be joined
    in_field = "TAZ"    
    join_field = "Field1"
    # output name
    out_features = "ShapeJoined"
    
    # make shapefile and table to be temporarily layer, then can be joined
    arcpy.MakeFeatureLayer_management(shape_path, in_features)
    arcpy.MakeTableView_management(table_path, join_table)
    
    
    try: 
        # excuate: temporaily join not permenant
        arcpy.AddJoin_management(in_features, in_field, join_table, join_field, "KEEP_COMMON")
        # copy the layer to a new permanent feature class (shapefile)
        arcpy.CopyFeatures_management(in_features, out_features)
        
        print 'join success...'
        
    except Exception as err:
        print(err.args[0])
        
    
    del MXD








