############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################

import bpy
from .classes import KeyMaps

def collect_mute_keymaps(km):
	pass
# Create Keymaps
def create_keymaps(km):
	if bpy.context.window_manager.keyconfigs.addon:
		# Object Non-modal --------------------------------------------------------------------
		space = km.space('Object Non-modal','EMPTY','WINDOW')
		km.new(space,"bsmax.mode_set",'F9',"PRESS",[])
		# 3D View --------------------------------------------------------------
		space = km.space('3D View','VIEW_3D','WINDOW')
		# km.new(space,"object.batchrename","F2","PRESS",[])
		km.new(space,"wm.call_menu","A","PRESS",[('name',"BsMax_MT_Create")],ctrl=True,shift=True)
		# Armature -------------------------------------------------------------
		space = km.space('Armature','EMPTY','WINDOW')
		km.new(space,"armature.batchrename","F2","PRESS",[])
		# Node Editor -----------------------------------------------------------------
		space = km.space("Node Editor","NODE_EDITOR",'WINDOW')
		km.new(space,"node.batchrename","F2","PRESS",[])
		# SEQUENCE_EDITOR--------------------------------------------------------------------
		space = km.space('Sequencer','SEQUENCE_EDITOR','WINDOW')
		km.new(space,"sequencer.batchrename","F2","PRESS",[])

keymaps = KeyMaps()

def blender_keys(register):
	keymaps.reset()
	if register:
		create_keymaps(keymaps)
		collect_mute_keymaps(keymaps)
	keymaps.set_mute(not register)

if __name__ == '__main__':
	blender_keys(True)

__all__=["blender_keys"]