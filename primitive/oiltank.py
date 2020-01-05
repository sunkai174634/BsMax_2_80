import bpy
from bpy.types import Operator
from math import pi, sin, cos, radians
from primitive.primitive import PrimitiveGeometryClass, CreatePrimitive
from bsmax.actions import delete_objects

def Get_oiltank_Mesh(radius,height,capheight,blend,ssegs,csegs,hsegs,sliceon,sfrom,sto):
	verts,edges,faces = [],[],[]
	sides,heights = [],[]
	arcrange,slicestep,r = pi*2,0,radius

	# get zscale of arc
	zscale = (capheight/radius) if radius > 0 else 0

	# fix height value
	height -= capheight * 2 if capheight > 0 else 0

	# height
	if sliceon:
		arcrange,slicestep = radians(sto-sfrom),1

	# collect segments x y onece
	for i in range(ssegs+slicestep):
		d = (arcrange/ssegs)*i+radians(sfrom)
		sides.append([sin(d),cos(d)])

	# get offsets
	zoffset1 = 0 if zscale > 0 else -radius*zscale
	zoffset2 = radius*zscale if zscale > 0 else 0
	zoffset3 = height+(zscale*radius)*2 if zscale > 0 else height+(zscale*radius)

	# collect cap arc height and scale
	for i in range(csegs):
		d = ((pi/2)/csegs)*i
		s = cos(d)
		h = sin(d)*zscale
		heights.append([h,s])
	heights.reverse()

	# add one more step if sclise is on
	ssegs += slicestep
	# Create vertexes data
	step = (pi*2)/ssegs

	# first vertex
	verts.append([0,0,zoffset1])
	# lower part
	for h, s in heights:
		for x, y in sides:
			X = r*x*s
			Y = r*y*s
			Z = radius*zscale-r*h+zoffset1
			verts.append([X,Y,Z])
		if sliceon:
			verts.append([0,0,Z])

	# Cylinder part
	h = height/hsegs
	for i in range(1,hsegs):
		for x,y in sides:
			X = r*x
			Y = r*y
			#Z = radius + h * i
			Z = zoffset2 + h * i
			verts.append([X,Y,Z])
		if sliceon:
				verts.append([0,0,Z])

	# uppaer part
	heights.reverse()
	for h,s in heights:
		for x,y in sides:
			X = r*x*s
			Y = r*y*s
			Z = zoffset2+r*h+height
			verts.append([X,Y,Z])
		if sliceon:
			verts.append([0,0,Z])
	# add last vertex
	verts.append([0,0,zoffset3])

	# uper triangles faces
	if sliceon:
		ssegs += 1
	for i in range(ssegs):
		a = i+1
		b = i+2
		c = 0
		if i < ssegs - 1:
			faces.append((a,b,c))
		else:
			faces.append((a,1,c))

	# body faces
	for i in range(csegs*2+hsegs-2):
		for j in range(ssegs):
			a = i*ssegs+j+1
			if j < ssegs-1:
				b = a+1
				c = a+ssegs+1
				d = c-1
			else:
				b = a-(ssegs-1)
				c = a+1
				d = a+ssegs
			faces.append((d,c,b,a))

	# lover triangels
	f = ssegs*(((csegs-1)*2)+hsegs)+1
	c = len(verts)-1
	for i in range(ssegs):
		a = i+f
		b = a+1 
		if i < ssegs-1:
			faces.append((c,b,a))
		else:
			faces.append((c,f,a))
	return verts,edges,faces

class OilTank(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "OilTank"
		self.finishon = 4
		self.owner = None
		self.data = None
	def reset(self):
		self.__init__()
	def create(self, ctx):
		mesh = Get_oiltank_Mesh(0,0,0,0,18,8,6,False,0,360)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.ssegs, pd.csegs, pd.hsegs = 18,8,3
		pd.center = True
	def update(self):
		pd = self.data.primitivedata
		csegs = pd.csegs if not pd.seglock else pd.ssegs-2
		if pd.center:
			height = pd.height
		else:
			diameter = pd.radius1*2
			if pd.height < diameter:
				pd.height = diameter
			height = pd.height-pd.radius1*2
		""" limit the cao height with heaight """
		if pd.thickness*2 > height:
			pd.thickness = height/2
		if pd.thickness*2 < -height:
			pd.thickness = -height/2
		mesh = Get_oiltank_Mesh(pd.radius1, height,
			pd.thickness, pd.chamfer1, # capheight, blend
			pd.ssegs, csegs, pd.hsegs,
			pd.sliceon, pd.sfrom, pd.sto)
		self.update_mesh(mesh)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateOilTank(CreatePrimitive):
	bl_idname = "bsmax.createoiltank"
	bl_label = "OilTank (Create)"
	subclass = OilTank()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius
		elif clickcount == 2:
			self.params.height = dimantion.height
		elif clickcount == 3:
			self.params.thickness = dimantion.height
		if clickcount > 0:
			self.subclass.update()
	def finish(self):
		pass

def oiltank_cls(register):
	c = BsMax_OT_CreateOilTank
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	oiltank_cls(True)

__all__ = ["oiltank_cls", "OilTank"]