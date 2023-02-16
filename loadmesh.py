import math3d
import pygame
import objects3d
class Face(object):
    def __init__(self,v_list,color,normals=None):
        self.mVList=v_list
        self.mColor=(color*255).int()
        if normals!=None:
            self.mNVList=normals
        norm=[]
        for vec in self.mVList:
            norm.append(math3d.VectorN(vec[0],vec[1],vec[2]))
        self.mNormal=((norm[1]-norm[0]).cross(norm[2]-norm[0])).normalized()
        self.mNormal=math3d.VectorN(self.mNormal[0],self.mNormal[1],self.mNormal[2],0)
        
class Polymesh(object):
    def __init__(self,fname=None):
        
        self.mFaces=[]
        self.mVList=[]
        self.mNList=[]
        self.mMat={}
        self.mChildren=[]
        self.mTransform=None
        if fname!=None:
            self.mFile=fname+".obj"
            fp=open(self.mFile,"r")
            #searching for material names
            for line in fp:
                line=line.strip()
                if line=="" or line[0]=="#":
                    continue
                elements=line.split(" ")
                if elements[0]=="usemtl":
                    self.mMat[elements[1]]=None
        
            fm=open(fname+".mtl","r")
            for line2 in fm:
                line2=line2.strip()
                if line2=="" or line2[0]=="#":
                    continue
                elements2=line2.split()
                if elements2[1] in self.mMat:
                    act_mat=elements2[1]
            
                

                if elements2[0]=="Kd":
                    col=[]
                    for i in range(1,len(elements2)):
                        col.append(elements2[i])
                        act_col=math3d.VectorN(*col)
                    self.mMat[act_mat]=act_col
            fm.close()
            fp.close()
            fp=open(self.mFile,"r")
            for line in fp:
                line=line.strip()
                if line=="" or line[0]=="#":
                    continue
                elements=line.split(" ")
                if elements[0]=="v":
                    v_list=[]
                    for i in range(1,len(elements)):
                        v_list.append(elements[i])
                    v_list.append(1)
                    self.mVList.append(math3d.VectorN(*v_list))
                if elements[0]=="vn":
                    vn_list=[]
                    for i in range(1,len(elements)):
                        vn_list.append(elements[i])
                    vn_list.append(0)
                    self.mNList.append(math3d.VectorN(*vn_list))
                if elements[0]=="usemtl":
                    act_col=self.mMat[elements[1]]
                
                if elements[0]=="f" and len(elements)>1:
                    f_list=[]
                    n_list=[]
                    uv_list=[]
                    if elements[1].count("//")==1:
                        #face and normal
                        for i in range(1,len(elements)):
                            values=elements[i].split("//")
                            f_list.append(self.mVList[int(values[0])-1])
                            n_list.append(self.mNList[int(values[1])-1])
                        self.mFaces.append(Face(f_list,act_col,n_list))
                    elif elements[1].count("/")==1:
                        #face and UV
                        for i in range(1,len(elements)):
                            values=elements[i].split("/")
                            f_list.append(self.mVList[int(values[0])-1])
                            uv_list.append(int(values[1])-1)
                        self.mFaces.append(Face(f_list,act_col))
                    elif elements[1].count("/")==2:
                        #face,normal,and UV
                        for i in range(1,len(elements)):
                            values=elements[i].split("/")
                            f_list.append(self.mVList[int(values[0])-1])
                            n_list.append(self.mNList[int(values[1])-1])
                            uv_list.append(int(values[1])-1)
                        self.mFaces.append(Face(f_list,act_col,n_list))
                    else:
                        #just face
                        for i in range(1,len(elements)):
                            f_list.append(self.mVList[int(elements[i])-1])
                        self.mFaces.append(Face(f_list,act_col))
                
            fp.close()
    def render(self,transform,surface):
        
        transform=self.mTransform*transform

        for face in self.mFaces:
            norm=face.mNormal*transform
            points=[]
            ren_points=[]
            for vert in face.mVList:
                vert*=transform
                points.append(vert)
            for vec in points:
                ren_points.append((vec[0],vec[1]))
            if norm[2]>=0:
                pygame.draw.polygon(surface,face.mColor,ren_points,1)

        for children in self.mChildren:
            
            children.render(transform,screen)

if __name__=="__main__":
    sun_scale=math3d.Scale(math3d.VectorN(50,50,50))
    sun_translate=math3d.Translate(math3d.VectorN(650,400,0))
    sun_rotateX=math3d.RotX(-90)

    ship_translate=math3d.Translate(math3d.VectorN(5,0,0))
    ship_scale=math3d.Scale(math3d.VectorN(0.2,0.2,0.2))

    sat_scale=math3d.Scale(math3d.VectorN(0.8,0.8,0.8))
    sat_translate=math3d.Translate(math3d.VectorN(-5,0,0))

    min_ship_scale=math3d.Scale(math3d.VectorN(0.1,0.1,0.1))
    min_ship_translate=math3d.Translate(math3d.VectorN(3,0,0))

    angle=0
    sun_angle=0
    sun=Polymesh("sun")
    sun.mTransform=math3d.Identity(4)

    sun_rot_y=Polymesh()
    sun_rot_y2=Polymesh()
    sat_rot_y=Polymesh()

    spaceship=Polymesh("ship")
    
    saturn=Polymesh("saturn")

    min_ship=Polymesh("ship")
    

    sun.mChildren.append(sun_rot_y)
    sun.mChildren.append(sun_rot_y2)
    sun_rot_y.mChildren.append(spaceship)
    sun_rot_y2.mChildren.append(saturn)
    saturn.mChildren.append(sat_rot_y)
    sat_rot_y.mChildren.append(min_ship)
    pygame.init()
    screen=pygame.display.set_mode((1366,768),pygame.SWSURFACE,24)
    while True:
        sun_rotateY=math3d.RotY(sun_angle)
        
        sun_iden=sun_rotateX*sun_rotateY*sun_scale*sun_translate

        sun_rot_y.mTransform=math3d.RotX(-90)*ship_scale*ship_translate*math3d.RotY(angle)
        sun_rot_y2.mTransform=math3d.RotX(angle)*math3d.RotZ(angle)*sat_scale*sat_translate*math3d.RotY(angle)
        sat_rot_y.mTransform=math3d.RotX(-90)*min_ship_scale*min_ship_translate*math3d.RotY(angle+10)

        spaceship.mTransform=math3d.Identity(4)
        min_ship.mTransform=math3d.Identity(4)
        saturn.mTransform=math3d.Identity(4)

        angle+=1
        #pygame.event.pump()
        evt=pygame.event.poll()
        if evt.type==pygame.MOUSEMOTION:
            if evt.buttons[0]:
                sun_angle+=0.5*evt.rel[0]
        keysPressed=pygame.key.get_pressed()
        screen.fill((0,0,0))
        if keysPressed[pygame.K_ESCAPE]:
            break

        sun.render(sun_iden,screen)
        
        pygame.display.flip()
    pygame.display.quit()
