"""
para usar este codigo, se debe agregar almenos dos objetos cualquiera a la estacion
y añadir al menos dos frames
además añadir el codigo python acutal y ejecutarlo"""
from robodk import *      # RoboDK API
from robolink import *    # Robot toolbox
from time import sleep
import random
# Link to RoboDK
RDK = Robolink()

tool1 = RDK.ItemUserPick('',ITEM_TYPE_TOOL) #herramienta a usar - ventosa simple
robot = RDK.ItemUserPick("",ITEM_TYPE_ROBOT)    #robot a usar preferencia muy grandes com fanuc M-710iC/50
targ = RDK.ItemUserPick("",ITEM_TYPE_TARGET)    #target de referencia para el movimiento eintermedio del robot
objetoss = RDK.ItemList(ITEM_TYPE_OBJECT)   #caja proporcionada para la simulacion

bott=RDK.ItemUserPick("seleccione objeto a clonar",objetoss)
bott.Copy()
framess = RDK.ItemList(ITEM_TYPE_FRAME)
frame=RDK.ItemUserPick("seleccione referencia \n donde se va a  clonar",framess)
frameplace = RDK.ItemUserPick("seleccione referencia \n donde se va a dejar los objetos",framess)

def botss():
    itemss = RDK.ItemList()
    botes = []
    for k in itemss:
        if k.Name().startswith("bot"):
            botes.append(k)
    return botes

objetos = botss()
for i in objetos:
    i.setVisible(False)
    i.Delete()
def box_calc(size_xyz, pallet_xyz):
    """Calculates a list of points to store parts in a pallet"""
    [size_x, size_y, size_z] = size_xyz
    [pallet_x, pallet_y, pallet_z] = pallet_xyz    
    xyz_list = []
    for h in range(int(pallet_z)):
        for j in range(int(pallet_y)):
            for i in range(int(pallet_x)):
                xyz_list = xyz_list + [[(i+0.5)*size_x, (j+0.5)*size_y, (h+0.5)*size_z]]
    return xyz_list

tam = [150,183,131]
num = [4,3,3]
possis = InputDialog("Ingrese distancia entre un objeto y otro",title="objetos disponibles",
                     value=tam)
#possis = [float(x.replace(' ','')) for x in possis.split(',')]
cantid = InputDialog("Ingrese cuando clone desea en X, Y y Z",value=num,title="ingrese el arreglo de objetos")
#cantid = [float(x.replace(' ','')) for x in cantid.split(',')]
posinit = box_calc([int(possis[0]),int(possis[1]),int(possis[2])],
                   [int(cantid[0]),int(cantid[1]),int(cantid[2])])


for i in range(len(posinit)):
    newbot = frame.Paste()
    newbot.setName('bot'+str(i))
    newbot.setPose(transl(posinit[i]))


objetos = botss()
for i in objetos:
    i.setVisible(True)


def rr(inf , may):
    return random.uniform(inf,may)

for i in objetos:
    i.Recolor([rr(0,1),rr(0,1),rr(0,1),1])

for i in range(len(objetos)):
    robot.setPoseFrame(frame)
    pp = transl(posinit[len(posinit)-1-i])
    aprox = 150
    robot.MoveJ(targ)
    robot.MoveJ(pp*transl(0,0,aprox)*rotx(pi))
    robot.MoveL(pp*rotx(pi))
    tool1.AttachClosest()
    robot.MoveL(robot.Pose()*transl(0,0,aprox))
    robot.MoveJ(targ)
    pp2 = transl(posinit[i])
    robot.setPoseFrame(frameplace)
    robot.MoveJ(pp2*transl(0,0,aprox)*rotx(-pi))
    robot.MoveL(pp2*rotx(pi))
    tool1.DetachAll(frameplace)
    robot.MoveL(pp2*transl(0,0,aprox)*rotx(pi))

robot.setPoseFrame(frame)
robot.MoveJ(targ)
