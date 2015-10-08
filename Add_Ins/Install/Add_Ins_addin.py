import arcpy
import json
import os
import pythonaddins
import sys

class LoadFGDBs(object):
    """Implementation for Add_Ins_addin.button_3 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        ddp = mxd.dataDrivenPages
        pageName = ddp.pageRow.getValue(ddp.pageNameField.name) # E.g. ABM
        pageNameField = ddp.pageNameField.name # edabbr
        dfLst = arcpy.mapping.ListDataFrames(mxd)

        # Environment settings.
        arcpy.env.overwriteOutput = True
        arcpy.env.addOutputsToMap = False

        annoGroups = arcpy.mapping.ListLayers(mxd, "*anno*")
        # Clear contents from annotation group layers for each dataframe.
        for df in dfLst:
          for group in annoGroups:
            name = group.name
            for lyr in group:
                arcpy.mapping.RemoveLayer(df,lyr)

        # baseDir = r"P:\15045 - ED Redistribution - Event Specific\R2015\21-Electoral_Boundaries_Commission_Support_Doc\WBS 8 - Geography\Mapping\local_shp\Anno GDBs"
        baseDir = r"P:\15030_32_EBC_Digital_Mapping\Maps\2017_General_Election\EDVA Maps\local_fgdb\Anno GDBs"
        try:
            for df in dfLst:
                if "MainDF" in df.name:
                    dfScale = int(round(df.scale))
                    arcpy.env.workspace =  baseDir + "\MDF Anno GDBs"
                    targetGDB = arcpy.ListFiles(pageName + "*" + str(dfScale) + "*")[0] # Only list files that start with current D-number and end in dataframe's scale.
                    workspace = arcpy.env.workspace + "\\" + targetGDB
                    walk = arcpy.da.Walk(workspace)
                    for tup in walk:
                      for lst in tup[2]: # Third list item of tuple generated by Walk is the file names.
                        # annoPath = workspace + "\\" + lst
                        annoPath = os.path.join(workspace,lst)
                        temp_layer = "ANNO_" + lst # name of anno layer e.g. CanadaP_In_1100000.
                        arcpy.MakeFeatureLayer_management(annoPath, temp_layer)
                        annoLyr = arcpy.mapping.Layer(temp_layer)
                        target_group = arcpy.mapping.ListLayers(mxd, "Anno*", df)[0]
                        arcpy.mapping.AddLayerToGroup(df, target_group, annoLyr, "TOP")
                        # del temp_layer
                        
                elif "Inset1" in df.name:
                    dfScale = int(round(df.scale))
                    arcpy.env.workspace =  baseDir + "\Inset 1 Anno GDBs"
                    targetGDB = arcpy.ListFiles(pageName + "*" + str(dfScale) + "*")[0] # Only list files that start with current D-number and end in dataframe's scale.
                    workspace = arcpy.env.workspace + "\\" + targetGDB
                    walk = arcpy.da.Walk(workspace)
                    for tup in walk:
                      for lst in tup[2]: # Third list item of tuple generated by Walk is the file names.
                        # annoPath = workspace + "\\" + lst
                        annoPath = os.path.join(workspace,lst)
                        temp_layer = "ANNO_" + lst # name of anno layer e.g. CanadaP_In_1100000.
                        arcpy.MakeFeatureLayer_management(annoPath, temp_layer)
                        annoLyr = arcpy.mapping.Layer(temp_layer)
                        target_group = arcpy.mapping.ListLayers(mxd, "Anno*", df)[0]
                        arcpy.mapping.AddLayerToGroup(df, target_group, annoLyr, "TOP")
                        # del temp_layer
                            
                elif "Inset2" in df.name:
                    dfScale = int(round(df.scale))
                    arcpy.env.workspace =  baseDir + "\Inset 2 Anno GDBs"
                    targetGDB = arcpy.ListFiles(pageName + "*" + str(dfScale) + "*")[0] # Only list files that start with current D-number and end in dataframe's scale.
                    workspace = arcpy.env.workspace + "\\" + targetGDB
                    walk = arcpy.da.Walk(workspace)
                    for tup in walk:
                      for lst in tup[2]: # Third list item of tuple generated by Walk is the file names.
                        # annoPath = workspace + "\\" + lst
                        annoPath = os.path.join(workspace,lst)
                        temp_layer = "ANNO_" + lst # name of anno layer e.g. CanadaP_In_1100000.
                        arcpy.MakeFeatureLayer_management(annoPath, temp_layer)
                        annoLyr = arcpy.mapping.Layer(temp_layer)
                        target_group = arcpy.mapping.ListLayers(mxd, "Anno*", df)[0]
                        arcpy.mapping.AddLayerToGroup(df, target_group, annoLyr, "TOP")
                        # del temp_layer
                        
        except IndexError:
            pass

class RecordLayout(object):
    """Implementation for Add_Ins_addin.button_1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):

    	#Reference mxd, ddp objects.
    	mxd = arcpy.mapping.MapDocument("CURRENT")
    	ddp = mxd.dataDrivenPages
    	pageName = ddp.pageRow.getValue(ddp.pageNameField.name) # E.g. ABM
    	pageNameField = ddp.pageNameField.name # edabbr

    	# Assign a unique to each element of the MXD.
    	# mxd = arcpy.mapping.ListLayoutElements(mxd)
    	# for index, elem in enumerate(layoutElems):
    	#   elem.name = str(index)

    	def setDF(dfIndex, df):
    	  """Function used to create a list of a data frame's position, dimensions, extent, scale, rotation, north arrow height/position, and scale text/bar height/position. Scale is rounded to nearest 100."""
    	  northArrow = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "*North*")[dfIndex]
    	  scaleText = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "*Scale Text*")[dfIndex]
    	  scaleBar = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "*Scale Bar*")[dfIndex]
    	  fieldValue = "[" + \
    	               str(round(df.elementPositionX, 3)) +         "," + str(round(df.elementPositionY, 3)) +         "," + \
    	               str(df.elementWidth) +                       "," + str(df.elementHeight) +                      "," + \
    	               str(df.extent.XMin) +                        "," + str(df.extent.YMin) +                        "," + \
    	               str(df.extent.XMax) +                        "," + str(df.extent.YMax) +                        "," + \
    	               str(int(round(df.scale / 50.0) * 50.0)) +    "," + str(round(df.rotation, 2)) +                 "," + \
    	               str(northArrow.elementWidth) +               "," + str(northArrow.elementHeight) +              "," + \
    	               str(round(northArrow.elementPositionX, 3)) + "," + str(round(northArrow.elementPositionY, 3)) + "," + \
    	               str(scaleText.elementWidth) +                "," + str(scaleText.elementHeight) +               "," + \
    	               str(round(scaleText.elementPositionX, 3)) +  "," + str(round(scaleText.elementPositionY, 3)) +  "," + \
    	               str(scaleBar.elementWidth) +                "," + str(scaleBar.elementHeight) +               "," + \
    	               str(round(scaleBar.elementPositionX, 3)) +  "," + str(round(scaleBar.elementPositionY, 3)) +  "]" 
    	  return fieldValue
    	    
    	  ##################################################################################


    	confirm = pythonaddins.MessageBox('Are you sure you want to save the page layout?\nPrevious data will be lost','Save Layout Confirmation', 4)
    	if confirm == 'Yes':
    	  #Reference pagelayout table
    	  pageLayoutTable = arcpy.mapping.ListTableViews(mxd, "PageLayoutElements")[0] # P.L.E.
    	  #Update information from pagelayout table
    	  pageLayoutCursor = arcpy.SearchCursor(pageLayoutTable.dataSource, "\"" + pageNameField + "\" = '" + pageName + "'")
    	  pageLayoutRow = pageLayoutCursor.next()

    	  if pageLayoutRow == None:               #INSERT A NEW ROW - INSERT CURSOR
    	    pageInsertCursor = arcpy.InsertCursor(pageLayoutTable.dataSource)
    	    pageInsertRow = pageInsertCursor.newRow()
    	    pageInsertRow.edabbr = pageName

    	    #Set Data Frame information
    	    for dfIndex, df in enumerate(arcpy.mapping.ListDataFrames(mxd)):
    	      if (df.elementPositionX > 0 and df.elementPositionX < mxd.pageSize[0]) and (df.elementPositionY > 0 and df.elementPositionY < mxd.pageSize[1]):  #don't set values if DF is off the page
    	        pageInsertRow.setValue(df.name, setDF(dfIndex, df)) # Data frame name must match P.L.E. column name in order to write to it.
    	         
    	    pageInsertCursor.insertRow(pageInsertRow)
    	    del pageInsertCursor, pageInsertRow

    	  else:                                   #UPDATE EXISTING ROW - UPDATE CURSOR
    	    pageUpdateCursor = arcpy.UpdateCursor(pageLayoutTable.dataSource, "\"" + pageNameField + "\" = '" + pageName + "'")
    	    pageUpdateRow = pageUpdateCursor.next()

    	    #Set Data Frame information
    	    for dfIndex, df in enumerate(arcpy.mapping.ListDataFrames(mxd)):
    	      if (df.elementPositionX > 0 and df.elementPositionX < mxd.pageSize[0]) and (df.elementPositionY > 0 and df.elementPositionY < mxd.pageSize[1]):  #don't set values if DF is off the page
    	        pageUpdateRow.setValue(df.name, setDF(dfIndex, df)) # Data frame name must match P.L.E. column name in order to write to it.
    	               
    	    
    	    pageUpdateCursor.updateRow(pageUpdateRow)
    	    del pageUpdateCursor, pageUpdateRow
    	    
    	  arcpy.RefreshCatalog(pageLayoutTable.dataSource)
    	  del pageLayoutCursor, pageLayoutRow

class ResetLayout(object):
    """Implementation for Add_Ins_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")

        # dfs_lst = arcpy.mapping.ListDataFrames(mxd) # List of all dataframes. MainDF and Insets.
        mainDF = arcpy.mapping.ListDataFrames(mxd)[0]
        insetDF_lst = arcpy.mapping.ListDataFrames(mxd, "*Inset*")
        mapElem_lst = arcpy.mapping.ListLayoutElements(mxd,"MAPSURROUND_ELEMENT") + arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")
        
        # Assign unique names to text elements. Zero-based.
        for index, elem in enumerate(mapElem_lst):
        	elem.name = str(index)
        	
        # Resets main dataframe to either landscape or protrait based on longer axis. 
        if mxd.pageSize[1] > mxd.pageSize[0]:
            # Portrait - 3/4 inch top/bottom padding, 1/2 inch left/right padding.
            mainDF.elementPositionX = 0.5
            mainDF.elementPositionY = 0.75
            mainDF.elementHeight = mxd.pageSize[1] - 1.5 # 9.5 on letter size page.
            mainDF.elementWidth =  mxd.pageSize[0] - 1.0 # 7.5 on letter size page.
        elif mxd.pageSize[1] < mxd.pageSize[0]:
            # Landscape - 1/2 inch top/bottom padding, 3/4 inch left/right padding.
            mainDF.elementPositionX = 0.75
            mainDF.elementPositionY = 0.5
            mainDF.elementHeight = mxd.pageSize[1] - 1.0 # 7.6 on letter size page.
            mainDF.elementWidth = mxd.pageSize[0] - 1.5 # 9.5 on letter size page.
        else:
            pass

        for index, inset in enumerate(insetDF_lst):
            dataFrame = insetDF_lst[index]
            dataFrame.elementPositionX = -2.5 - int(index)
            dataFrame.elementPositionY = 0.0
            dataFrame.elementHeight = 2.0
            dataFrame.elementWidth = 2.0
            insetExtent_2 = arcpy.Extent(-501061.692164, -525266.392214, 2645013.83426, 2620809.13421)
            dataFrame.extent = insetExtent_2

        # Resets Map Surround Elements.
        # for index, mapElem in enumerate(mapElem_lst):
        #     element = mapElem_lst[index]
        #     element.elementPositionX = -2.5 - int(index)
        #     element.elementPositionY = 5.0

class RestoreLayout(object):
    """Implementation for Add_Ins_addin.button_2 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):

        #Function that arranges data frames based on the field info within the PageLayoutElements table. List order must match setDF order.
        def arrangeDFs(row, dfIndex, dfName):
          
          try:
            rowInfo = json.loads(row.getValue(dfName))
            try:
              df = arcpy.mapping.ListDataFrames(mxd, dfName)[0]
              nArrow = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "*North*")[dfIndex]
              scaleText = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "*Scale*")[dfIndex]

              df.elementPositionX = rowInfo[0]
              df.elementPositionY = rowInfo[1]
              df.elementWidth = rowInfo[2]
              df.elementHeight = rowInfo[3]
              newExtent = df.extent
              newExtent.XMin = rowInfo[4]
              newExtent.YMin = rowInfo[5]
              newExtent.XMax = rowInfo[6]
              newExtent.YMax = rowInfo[7]
              df.extent = newExtent
              df.scale = rowInfo[8]
              df.rotation = rowInfo[9]
              nArrow.elementWidth = rowInfo[10]
              nArrow.elementHeight = rowInfo[11]
              nArrow.elementPositionX = rowInfo[12]
              nArrow.elementPositionY = rowInfo[13]
              scaleText.elementWidth = rowInfo[14]
              scaleText.elementHeight = rowInfo[15]
              scaleText.elementPositionX = rowInfo[16]
              scaleText.elementPositionY = rowInfo[17]
            except IndexError:
              pass
          except ValueError:
            pass


        ################################################################################

        #Reference MXD
        mxd = arcpy.mapping.MapDocument("CURRENT")  #CURRENT.
        ddp = mxd.dataDrivenPages
        pageName = ddp.pageRow.getValue(ddp.pageNameField.name)
        pageNameField = ddp.pageNameField.name # edabbr
        #Reference pageLayoutTable
        pageLayoutTable = arcpy.mapping.ListTableViews(mxd, "PageLayoutElements")[0]

        #Move all data frames off the layout and into their default positions
        pageLayoutCursor = arcpy.SearchCursor(pageLayoutTable.dataSource, "\"" + pageNameField + "\" = '" + pageName + "'")
        pageLayoutRow = pageLayoutCursor.next()
        for dfIndex, df in enumerate(arcpy.mapping.ListDataFrames(mxd)):
          arrangeDFs(pageLayoutRow, dfIndex, df.name)

        arcpy.RefreshActiveView()