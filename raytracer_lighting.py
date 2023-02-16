import math3d
import objects3d
import pygame
import math
# Pygame setup
pygame.init()
screen = pygame.display.set_mode((300, 200))
done = False

camPos = math3d.VectorN(-15, 19, -30)
camCOI = math3d.VectorN(2, 5, 3)
camUp = math3d.VectorN(0, 1, 0)
camFOV = 60.0
camNear = 1.5
cam = objects3d.Camera(camPos, camCOI, camUp, camFOV, camNear, screen)

allShapes = []
allShapes.append(objects3d.Sphere(math3d.VectorN(2, 11, 3), 5, math3d.VectorN(0.3, 0, 0),math3d.VectorN(1,0,0),math3d.VectorN(1,1,1),10.0))
allShapes.append(objects3d.Plane(math3d.VectorN(0,1,0), 5, math3d.VectorN(0,0.5,0),math3d.VectorN(0,1,0),math3d.VectorN(1,0,0),2.0))
allShapes.append(objects3d.Plane(math3d.VectorN(0.1,1,0), 4, math3d.VectorN(0,0,0.1),math3d.VectorN(0,0,1),math3d.VectorN(1,0,1),6.0))
allShapes.append(objects3d.AABB(math3d.VectorN(2,9,-6),math3d.VectorN(8,15,0),math3d.VectorN(0.5,0.3,0.1),math3d.VectorN(1,1,0),math3d.VectorN(0.5,1,0.5),30.0))
allShapes.append(objects3d.Triangle(math3d.VectorN(2,5,3),math3d.VectorN(3,5,3),math3d.VectorN(2,6,5),math3d.VectorN(1,0,1),math3d.VectorN(1,1,0),math3d.VectorN(0.5,1,0.5),30.0))
allShapes.append(objects3d.Polymesh("sword.obj",math3d.VectorN(-10,8,3),1.0,math3d.VectorN(0.2,0,0.4),math3d.VectorN(0.7,0,1),math3d.VectorN(1,1,1),50))
allLights=[]
allLights.append(objects3d.Light(math3d.VectorN(0,50,0),math3d.VectorN(1,1,1),math3d.VectorN(1,1,1)))
allLights.append(objects3d.Light(math3d.VectorN(50,50,-50),math3d.VectorN(0.4,0,0),math3d.VectorN(0,0.6,0)))
amb_l=math3d.VectorN(1,1,1)
y = 0




# Game Loop
while not done:
    # Render one line of pixels IF we have more to render
    if y < screen.get_height():
        for x in range(0, screen.get_width()):
            # For this pixel, create a ray that starts on our view plane
            # and goes away from the camera.
            rayOrigin = cam.getPixelPos(x, y)
            rayDirection = rayOrigin - cam.camPos
            R = objects3d.Ray(rayOrigin, rayDirection)

			# Find the closest object we hit and get it's color
##			color = math3d.VectorN(0.3, 0.3, 0.3)
            results=[]
            for obj in allShapes:
                if isinstance(obj,objects3d.Polymesh):
                    temp=obj.rayIntersection(R)
                    if temp!=None:
                        result,normal=temp
                    else:
                        result=None
                else: 
                    result = obj.rayIntersection(R)
                
                if result!=None and result>0:
                    results.append(result)
                elif result==None:
                    screen.set_at((x,y),(100,100,100))  
            for i in results:
                
                value=min(results)
                
                for obj in allShapes:
                    if isinstance(obj,objects3d.Polymesh):
                        a=obj.rayIntersection(R)
                        if a!=None:
                            temp2,blah=a
                        else:
                            temp2=None

                    else:
                        temp2=obj.rayIntersection(R)
                    if temp2==value:
                        amb=obj.mAmbient
                        diff=obj.mDiffuse
                        spec=obj.mSpecular

                        if isinstance(obj,objects3d.Plane):
                            normal=obj.mNormal
                        if isinstance(obj,objects3d.Sphere):
                            point=R.getPoint(value)
                            normal=(point-obj.mCenter).normalized()
                        if isinstance(obj,objects3d.AABB):
                            for face in obj.mFaces:
                                if face.rayIntersection(R)==value:
                                    normal=face.mNormal
                        if isinstance(obj,objects3d.Triangle):
                            normal=obj.mNormal
                        
                            
                        point=R.getPoint(value)
                        diff_c=math3d.VectorN(0,0,0)
                        spec_c=math3d.VectorN(0,0,0)
                        for light in allLights:
                            shadow=False
                            distance=(light.pos-point).normalized()
                            dStr=distance.dot(normal)
                            shadow_ray=objects3d.Ray(point+distance*0.01,distance)
                            for shape in allShapes:
                                if shape.rayIntersection(shadow_ray):
                                    shadow=True
                            if shadow==False:
                                if dStr<=0:
                                    pass
                                if dStr>0:
                                    diff_c+=(dStr*(light.mDiffuse.pairwise_mult(obj.mDiffuse)))
                            
                                ref=2*(distance.dot(normal))*(normal)-distance
                                v=(cam.camPos-point).normalized()
                                sStr=v.dot(ref)

                                if sStr<=0:
                                    pass
                                if sStr>0:
                                    spec_c+=(sStr**obj.mHardness)*(light.mSpecular.pairwise_mult(obj.mSpecular))

                            

                            

                        ambient_c = amb.pairwise_mult(amb_l)
                        
                        lit_cv=(ambient_c+diff_c+spec_c)
                        
                        lit_c=((lit_cv.clamp(0,1))*255).int()

                        
                        screen.set_at((x, y), lit_c)
                    else:
                        pass
			
            
        y += 1

    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        done = True


    pygame.display.flip()

pygame.quit()
