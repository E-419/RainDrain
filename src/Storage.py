from sympy import integrate, log, exp, oo, symbols


# Assumes Slope is uniform around the pond/vault:
x,y,z,Slope = symbols(('x','y','z','Slope'))

volume = integrate((x + 2 * (Slope * z)) * (y + 2 * (Slope * z)),(z, 0, z))

print(volume, '\n', volume.evalf(subs={x:10, y:20, z:5, Slope:3}) / 43560)



# Generalized form, all slopes are independent:
x,y,z,slope_x_1, slope_x_2, slope_y_1, slope_y_2 = symbols(
    ('x','y','z','slope_x_1',' slope_x_2',' slope_y_1',' slope_y_2'))

volume = integrate( (x + (slope_x_1 * z) + (slope_x_2 * z)) * 
                    (y + (slope_y_1 * z) + (slope_y_2 * z)),
                    (z, 0, z))

print(volume, '\n', volume.evalf(subs={ x:10, 
                                        y:20, 
                                        z:5, 
                                        slope_x_1:3, 
                                        slope_x_2:3, 
                                        slope_y_1:3, 
                                        slope_y_2:3}) / 43560)
                                        

class Pond():
    def __init__(self,  bottom_length = 0, 
                        bottom_width = 0, 
                        depth = 0, 
                        slope_width_1 = 3, 
                        slope_width_2 = 3, 
                        slope_length_1 = 3, 
                        slope_length_2 = 3):
        self.x = bottom_width
        self.y = bottom_length
        self.z = depth
        self.slope_width_1 = slope_width_1
        self.slope_width_2 = slope_width_2
        self.slope_length_1 = slope_length_1
        self.slope_length_2 = slope_length_2
        self.volume_max = 0
        self.compute_max_volume()
    
    def width_at_stage(self, stage_depth):
        return self.x + stage_depth * self.slope_width_1 + stage_depth * self.slope_width_2
    
    def length_at_stage(self, stage_depth):
        return self.y + stage_depth * self.slope_length_1 + stage_depth * self.slope_length_2
    
    def area_at_stage(self, stage_depth):
        width = self.width_at_stage(stage_depth)
        length = self.length_at_stage(stage_depth)
        return length * width
        
    def compute_max_volume(self):
        self.volume_max = self.volume_at_stage(self.z)
        
    def volume_at_stage(self, stage_depth):
        '''
        # # # # # # # # # # # # # # # # # # 
        #   Derivation of volume formula
        #
        
        from sympy import integrate, log, exp, oo, symbols
        
        # Generalized form, all slopes are independent:
        x,y,z,slope_x_1, slope_x_2, slope_y_1, slope_y_2 = symbols(
            ('x','y','z','slope_x_1',' slope_x_2',' slope_y_1',' slope_y_2'))
        
        volume = integrate( (x + (slope_x_1 * z) + (slope_x_2 * z)) * 
                            (y + (slope_y_1 * z) + (slope_y_2 * z)),
                            (z, 0, z))
        
        # This is the output required for the class method below:
        print(volume)
        
       
        
        print(volume, '\n', volume.evalf(subs={ x:10, 
                                                y:20, 
                                                z:5, 
                                                slope_x_1:3, 
                                                slope_x_2:3, 
                                                slope_y_1:3, 
                                                slope_y_2:3}) / 43560)

        '''
        x = self.x
        y = self.y
        z = stage_depth
        slope_x_1 = self.slope_width_1
        slope_x_2 = self.slope_width_2
        slope_y_1 = self.slope_length_1
        slope_y_2 = self.slope_length_2
        
        return (    x*y*z + 
                    z**3*(  slope_x_1*slope_y_1/3 + 
                            slope_x_1*slope_y_2/3 + 
                            slope_x_2*slope_y_1/3 + 
                            slope_x_2*slope_y_2/3) +
                    z**2*(  slope_x_1*y/2 + 
                            slope_x_2*y/2 + 
                            slope_y_1*x/2 + 
                            slope_y_2*x/2)
                )
                    
                    
                    
                    
if __name__ == '__main__':
    p1 = Pond(143.26, 286.52, 10, 2,2,2,2)
    inc = 10/90
    print('Stage\t', 'Area\t', 'Volume\t', 'Discharge')
    for i in range(0, 93):
        stage = i * inc
        print(round(stage, 3), '\t', int(p1.area_at_stage(stage)) , '\t', round(p1.volume_at_stage(stage)/43560, 4))
                    
                    
                    
                    
                    
                    
                    
                    
                    