
class VTKFileWriter:
    def __init__(self, filename, values):
        f = open(filename + '.vtk', 'w')
        
        f.write('# vtk DataFile Version 1.5\n')
        f.write('Test\n')
        f.write('ASCII\n\n')
        f.write('DATASET POLYDATA\n\n')
        
        f.write('POINTS ' + str(values.shape[0]*values.shape[1]) + ' float\n')
        for i in range(values.shape[0]):
            for j in range(values.shape[1]):
                f.write(str(i) + ' '+ str(j) + ' 0\n')
                
        f.write('\nPOINT_DATA ' +  str(values.shape[0]*values.shape[1]) )
        f.write('\nSCALARS sample_scalars int\nLOOKUP_TABLE lut\n')
        for k in range(values.shape[0]*values.shape[1]) :
            f.write(str(k) + '\n')
            
        f.write('\nTENSORS tensors float\n')
        for l in range(values.shape[0]):
            for m in range(values.shape[1]):
                tensor = values[l, m, 1]
                f.write(str(tensor[0, 0]*100) + ' ' + str(tensor[0, 1]*100) + ' ' + str(tensor[0, 2]*100) + '\n')
                f.write(str(tensor[1, 0]*100) + ' ' + str(tensor[1, 1]*100) + ' ' + str(tensor[1, 2]*100) + '\n')   
                f.write(str(tensor[2, 0]*100) + ' ' + str(tensor[2, 1]*100) + ' ' + str(tensor[2, 2]*100) + '\n\n') 
#                f.write('%f' %(tensor[0, 0]) + ' ' + '%f' %(tensor[0, 1]) + ' ' + '%f' %(tensor[0, 2]) + '\n')
#                f.write('%f' %(tensor[1, 0]) + ' ' + '%f' %(tensor[1, 1]) + ' ' + '%f' %(tensor[1, 2]) + '\n')   
#                f.write('%f' %(tensor[2, 0]) + ' ' + '%f' %(tensor[2, 1]) + ' ' + '%f' %(tensor[2, 2]) + '\n\n')    
