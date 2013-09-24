#
# g.py
# utility functions
# Greg Ecker
# 5/4/12
#
import hou
import toolutils

#
# resetBakeShot
#
def resetBakeShot(node=hou.node("/obj")):
	if node.type().name() == 'io_BakeGeo':
		node.parm('shot').setExpression('$SHOT')
	for child in node.children():
		resetBakeShot(child)

#
# getIdList
# list of ids of points at given node
#
# usage: import g
#	g.getIdList('/obj/geo1/OUT')
#

def getIdList(node):
    # nodeGeo = hou.node(nodepath).geometry()
	nodeGeo = node.geometry()
	idList = nodeGeo.pointFloatAttribValues("id")
	idListAsInt = [int(i) for i in idList]
 	print(idListAsInt)

#
# getPtFromId
#
# returns pointnumber of point with given id value
#
def getPtFromId(node, id):
	nodeGeo = node.geometry()
	idList = nodeGeo.pointFloatAttribValues("id")
	idListAsInt = [int(i) for i in idList]
	return idListAsInt.index(id)
	
#
# makeOut
#
# given a selected node,  makes a null named 'OUT' after it in the chain
#

def makeOut():
	cwd = toolutils.sceneViewer().pwd()
	selected = [child for child in cwd.children() if child.isSelected()]
	if len(selected) == 0:
		raise hou.InvalidInput("need to select one Sop")	
	node = selected[0]	# only work on first selected node
#	node_type = node.type()
#	if node_type.category().name() != 'Sop':
#		raise hou.InvalidInput("only works on Sops")
		
	# create node:
	nullNode = node.parent().createNode('null', node_name='OUT')
	nullNode.setInput(0, node)
	nullNode.setColor(hou.Color((0,0,0)))

#
# just creates an unconnected null, named CONTROL, and colors it black
#	
def makeControl():
	cwd = toolutils.sceneViewer().pwd()
	selected = [child for child in cwd.children() if child.isSelected()]
	if len(selected) == 0:
		raise hou.InvalidInput("need to select one Sop")	
	node = selected[0]	# only work on first selected node
		
	# create node:
	nullNode = node.parent().createNode('null', node_name='CONTROL')
	nullNode.setColor(hou.Color((0,0,0)))

	
#	
# bakes keyframes from a chop channel to given parameter
#
# usage:  bakeChops.bakeChop("/obj/geo1/chopnet1/export1/chan1", "obj/geo1/target/ty", 1, 240, 10)
#
def bakeChop(pathToChop, pathToParm, startSampleFrame, endSampleFrame, stepFrame):
        #sample chop:
        frameValList = []
        for frame in range(startSampleFrame, endSampleFrame, stepFrame):
                hexpr = 'chopf(\"'+pathToChop+'\",'+str(frame)+')'
                retval = hou.hscriptExpression(hexpr)
                val = float(retval)
                frameValList.append((frame, val))
        #make keys:
        parm = hou.parm(pathToParm)
        parm.deleteAllKeyframes()

        keyList = []
        for frameVal in frameValList:
                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1])
                parm.setKeyframe(key)

#	
# bakes all transform keyframes from a set of chop channels to given node's transforms (tx, ty,tz,rx,ry,rz)
#
# usage:  bakeChopTransforms("/obj/cam_master/hdfchopNet/exportCamChop/cam_main_orig_mm", "/obj/fx_cam_meters", 1003, 1564, 1)
#
def bakeChopTransforms(pathToChop="/obj/cam_master/hdfchopNet/exportCamChop/cam_main_orig_mm", pathToNode="/obj/fx_cam_meters", startFrame=1003, endFrame=1564, stepFrame=1):
        #sample chop:
        frameValList = []
	pathToChopTX = pathToChop + "/tx"
	pathToChopTY = pathToChop + "/ty"
	pathToChopTZ = pathToChop + "/tz"
	pathToChopRX = pathToChop + "/rx"
	pathToChopRY = pathToChop + "/ry"
	pathToChopRZ = pathToChop + "/rz"		
        for frame in range(startSampleFrame, endSampleFrame, stepFrame):		
                hexpr = 'chopf(\"'+pathToChopTX+'\",'+str(frame)+')'
                retval = hou.hscriptExpression(hexpr)
                valTX = float(retval)		
                hexpr = 'chopf(\"'+pathToChopTY+'\",'+str(frame)+')'
                retval = hou.hscriptExpression(hexpr)
                valTY = float(retval)
                hexpr = 'chopf(\"'+pathToChopTZ+'\",'+str(frame)+')'
                retval = hou.hscriptExpression(hexpr)
                valTZ = float(retval)
                hexpr = 'chopf(\"'+pathToChopRX+'\",'+str(frame)+')'
                retval = hou.hscriptExpression(hexpr)
                valRX = float(retval)
                hexpr = 'chopf(\"'+pathToChopRY+'\",'+str(frame)+')'
                retval = hou.hscriptExpression(hexpr)
                valRY = float(retval)
                hexpr = 'chopf(\"'+pathToChopRZ+'\",'+str(frame)+')'
                retval = hou.hscriptExpression(hexpr)
                valRZ = float(retval)			
                frameValList.append((frame, (valTX, valTY, valTZ, valRX, valRY, valRZ)))
		
        #make keys:
        parmTX = hou.parm(pathToNode+"/tx")
        parmTX.deleteAllKeyframes()
        parmTY = hou.parm(pathToNode+"/ty")
        parmTY.deleteAllKeyframes()
        parmTZ = hou.parm(pathToNode+"/tz")
        parmTZ.deleteAllKeyframes()
        parmRX = hou.parm(pathToNode+"/rx")
        parmRX.deleteAllKeyframes()
        parmRY = hou.parm(pathToNode+"/ry")
        parmRY.deleteAllKeyframes()
        parmRZ = hou.parm(pathToNode+"/rz")
        parmRZ.deleteAllKeyframes()


        for frameVal in frameValList:
                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][0])
                parmTX.setKeyframe(key)
                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][1])
                parmTY.setKeyframe(key)
                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][2])
                parmTZ.setKeyframe(key)
                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][3])
                parmRX.setKeyframe(key)
                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][4])
                parmRY.setKeyframe(key)
                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][5])
                parmRZ.setKeyframe(key)

#
# def bakeChannel
#
# usage: bakeChannel("/obj/geo1/xform1/tx", "/obj/geo1/xform2/tx", 1, 240, 2)
#
def bakeChannel(pathToSource, pathToDest, startSampleFrame, endSampleFrame, stepFrame):
        #sample chop:
        frameValList = []
        for frame in range(startSampleFrame, endSampleFrame, stepFrame):
                hexpr = 'chf(\"'+pathToSource+'\",'+str(frame)+')'
                retval = hou.hscriptExpression(hexpr)
                val = float(retval)
                frameValList.append((frame, val))
        #make keys:
        parm = hou.parm(pathToDest)
        parm.deleteAllKeyframes()

        keyList = []
        for frameVal in frameValList:
                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1])
                parm.setKeyframe(key)

#
# def bakeTranslation
#
# usage: bakeTranslation("/obj/geo1/xform1", "/obj/geo1/xform2", 1, 240, 2)
#	bakes tx, ty, tz from source to dest
#
def bakeTranslation(pathToSource, pathToDest, startSampleFrame, endSampleFrame, stepFrame):
        #sample chop:
        frameValList = []
        for frame in range(startSampleFrame, endSampleFrame, stepFrame):
                hexprTX = 'chf(\"'+pathToSource+'\"/tx,'+str(frame)+')'
                hexprTY = 'chf(\"'+pathToSource+'\"/ty,'+str(frame)+')'
                hexprTZ = 'chf(\"'+pathToSource+'\"/tz,'+str(frame)+')'				
                retvalTX = hou.hscriptExpression(hexprTX)
                retvalTY = hou.hscriptExpression(hexprTY)
                retvalTZ = hou.hscriptExpression(hexprTZ)				
                valTX = float(retvalTX)
                valTY = float(retvalTY)
                valTZ = float(retvalTZ)				
                frameValList.append((frame, (valTX, valTY, valTZ)))
        #make keys:
	pathToDestTX = pathToDest+"/tx"
	pathToDestTY = pathToDest+"/ty"
	pathToDestTZ = pathToDest+"/tz"
	
        parmTX = hou.parm(pathToDestTX)
        parmTX.deleteAllKeyframes()

        parmTY = hou.parm(pathToDestTY)
        parmTY.deleteAllKeyframes()

        parmTZ = hou.parm(pathToDestTZ)
        parmTZ.deleteAllKeyframes()

        keyList = []
        for frameVal in frameValList:
                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][0])
                parmTX.setKeyframe(key)
		
                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][1])
                parmTY.setKeyframe(key)

                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][2])
                parmTZ.setKeyframe(key)

#
# def bakeTransforms
#
# usage: bakeTransforms("/obj/geo1/xform1", "/obj/geo1/xform2", 1, 240, 2)
#	bakes tx, ty, tz, rx, ry, rz from source to dest by default (no scaling)
#
def bakeTransforms(pathToSource, pathToDest, startSampleFrame, endSampleFrame, stepFrame):
        frameValList = []
        for frame in range(startSampleFrame, endSampleFrame, stepFrame):
                hexprTX = 'chf(\"'+pathToSource+'\"/tx,'+str(frame)+')'
                hexprTY = 'chf(\"'+pathToSource+'\"/ty,'+str(frame)+')'
                hexprTZ = 'chf(\"'+pathToSource+'\"/tz,'+str(frame)+')'
                hexprRX = 'chf(\"'+pathToSource+'\"/rx,'+str(frame)+')'
                hexprRY = 'chf(\"'+pathToSource+'\"/ry,'+str(frame)+')'
                hexprRZ = 'chf(\"'+pathToSource+'\"/rz,'+str(frame)+')'						
                retvalTX = hou.hscriptExpression(hexprTX)
                retvalTY = hou.hscriptExpression(hexprTY)
                retvalTZ = hou.hscriptExpression(hexprTZ)
                retvalRX = hou.hscriptExpression(hexprTX)
                retvalRY = hou.hscriptExpression(hexprTY)
                retvalRZ = hou.hscriptExpression(hexprTZ)				
		
                TX = float(retvalTX)
                TY = float(retvalTY)
                TZ = float(retvalTZ)
                RX = float(retvalRX)
                RY = float(retvalRY)
                RZ = float(retvalRZ)
						
                frameValList.append((frame, (TX, TY, TZ, RX, RY, RZ)))
		
        #make keys:
	pathToDestTX = pathToDest+"/tx"
	pathToDestTY = pathToDest+"/ty"
	pathToDestTZ = pathToDest+"/tz"
	pathToDestRX = pathToDest+"/rx"
	pathToDestRY = pathToDest+"/ry"
	pathToDestRZ = pathToDest+"/rz"
	
        parmTX = hou.parm(pathToDestTX)
        parmTX.deleteAllKeyframes()

        parmTY = hou.parm(pathToDestTY)
        parmTY.deleteAllKeyframes()

        parmTZ = hou.parm(pathToDestTZ)
        parmTZ.deleteAllKeyframes()

        parmRX = hou.parm(pathToDestRX)
        parmRX.deleteAllKeyframes()

        parmRY = hou.parm(pathToDestRY)
        parmRY.deleteAllKeyframes()

        parmRZ = hou.parm(pathToDestRZ)
        parmRZ.deleteAllKeyframes()

        keyList = []
        for frameVal in frameValList:
                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][0])
                parmTX.setKeyframe(key)
		
                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][1])
                parmTY.setKeyframe(key)

                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][2])
                parmTZ.setKeyframe(key)

                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][3])
                parmRX.setKeyframe(key)

                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][4])
                parmRY.setKeyframe(key)

                key = hou.Keyframe()
                key.setFrame(frameVal[0])
                key.setValue(frameVal[1][5])
                parmRZ.setKeyframe(key)


#
# extractChildren
#
# creates a node called 'extract_object' in currently selected viewport,  
# which contains an object merge pointing to all nodes selected at current level + "/OUT"
#
def extractChildren():
	scene_viewer = toolutils.sceneViewer()
	cwd = scene_viewer.pwd()
	selected = [child for child in cwd.children() if child.isSelected()]
	extractNode = hou.node(cwd.path()).createNode("geo", "extract_node", run_init_scripts=False )	# create empty geo node
	merge_sop = extractNode.createNode("object_merge")
	
	num_objs = len(selected)
	merge_paths_dict = {}
	i = 1
	for sel in selected:
		merge_paths_dict["objpath"+str(i)] = sel.path() + "/OUT"
		i = i + 1		
	
	parm_dict = {"numobj":num_objs, "xformtype":1}
	merge_sop.setParms(parm_dict)
	merge_sop.setParms(merge_paths_dict)
		
	scene_viewer.setPwd(merge_sop.parent())
	toolutils.homeToSelectionNetworkEditorsFor(merge_sop)	
	extractNode.setColor(hou.Color((0,0,0)))
	extractNode.moveToGoodPosition()

#
# pressButton
#
# for each selected node,  presses a button (passes a message) to a child of that node
#
def pressButton(childNodeName="cue_pt_lgt_to_h11", message="execute"):
	scene_viewer = toolutils.sceneViewer()
	cwd = scene_viewer.pwd()
	selected = [child for child in cwd.children() if child.isSelected()]	# get selected nodes
	for sel in selected:
		childNode = hou.node(sel.path()+"/"+childNodeName)
		childNode.parm(message).pressButton()

#
# setBypass
#
# for each selected node,  sets the bypass flag to a child of that node
#
def setBypass(childNodeName="prep_shell_pt/setPtoBlendBlendP", flag=1):
	scene_viewer = toolutils.sceneViewer()
	cwd = scene_viewer.pwd()
	selected = [child for child in cwd.children() if child.isSelected()]	# get selected nodes
	for sel in selected:
		childNode = hou.node(sel.path()+"/"+childNodeName)
		childNode.bypass(flag)
		
#
# resetParm
#
def resetParm(childNodeName="path_filament/cue_wisp_pts/io_Cue1", param="save_first", value=0):
	scene_viewer = toolutils.sceneViewer()
	cwd = scene_viewer.pwd()
	selected = [child for child in cwd.children() if child.isSelected()]	# get selected nodes
	for sel in selected:
		childNode = hou.node(sel.path()+"/"+childNodeName)
		childNode.parm(param).set(value)

#
# resetExpression
#
def resetExpr(childNodeName="path_filament/pre_speckspline_TO_H11", param="fx", expr="FS"):
	scene_viewer = toolutils.sceneViewer()
	cwd = scene_viewer.pwd()
	selected = [child for child in cwd.children() if child.isSelected()]	# get selected nodes
	for sel in selected:
		childNode = hou.node(sel.path()+"/"+childNodeName)
		childNode.parm(param).setExpression(expr)
