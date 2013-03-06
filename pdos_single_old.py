#!/usr/bin/env python
 
import sys
import commands
import numpy

print "Warning, I believe this only looks at 1 atom!"
print "This is for project blackbird, and was used for Li"

subtractFermi = True
ncore_electrons = 2
nvalence_electrons = 4
nelectrons = ncore_electrons + nvalence_electrons

def main(): 

 try:
     input_filename = sys.argv[1]
 except IndexError:
     print '\nusage: ' + sys.argv[0] + ' input_filename'
     print '\nexiting...\n'
     sys.exit(0)
 
 
 command_line_counter = commands.getoutput('wc -l ' + input_filename).split()
 
 if len(command_line_counter) != 2:
   print 'Error determining file size'
 else:
   number_of_lines = int(command_line_counter[0])
 
 outputFile_dos = open('dos.dat', 'w')
 outputFile_pdos = open('pdos.dat', 'w')
 
 inputFile = open(input_filename, 'r')
 natom = int(inputFile.readline().split()[0])
 for i in range(4):
     inputFile.readline()
 
 inline_total = inputFile.readline()
 
 emin_total = float(inline_total.split()[1])
 emax_total = float(inline_total.split()[0])
 enum_total = int(inline_total.split()[2])
 efermi_total = float(inline_total.split()[3])
 
 dos = numpy.zeros((enum_total, 3), dtype = numpy.float) # E, dos, idos
 
 for i in range(enum_total):
     inline_total = inputFile.readline().split()
     if (subtractFermi == True): 
       dos[i][0] = float(inline_total[0]) - efermi_total 
     else: 
       dos[i][0] = float(inline_total[0])  
 
     dos[i][1], dos[i][2] = float(inline_total[1]), float(inline_total[2])

 # loop through dos, find point where idos > atoms in 3s2 state of S

 core_valence_divide = 0 # initialize to safe value

 for i in range(enum_total):
   if ( dos[i][2] > natom*ncore_electrons): 
     core_valence_divide = i
     break 

 efermi_bin = 1e6  # initialize to crazy value

 for i in range(enum_total):
   if ( dos[i][2] > natom*nelectrons):
     efermi_bin = i
     break

 if (efermi_bin == 1e6):
   print 'Fermi bin not found. There is something wrong.'
   sys.exit(0)

 for row in dos:
     for element in row:
         outputFile_dos.write(str(element) + ' ')
     outputFile_dos.write('\n')


 ############

 inline_project = inputFile.readline()

 emin_project = float(inline_project.split()[1])
 enum_project = int(inline_project.split()[2])
 efermi_project = float(inline_project.split()[3])
 
 spacing = (emax_total - emin_total)/enum_total
 pdos = numpy.zeros((enum_project, 1 + 3*2), dtype = numpy.float) # E, s, p, d
 
 for i in range(len(pdos)):
 
    pdos[i][0] = dos[i][0]  # fills in the E column of pdos
 
 for i in range(enum_project):
     inline_project = inputFile.readline().split()
     pdos[i][1] += float(inline_project[1])
     pdos[i][2] += float(inline_project[2])
     pdos[i][3] += float(inline_project[3])
 
 for i in numpy.arange(1,enum_project):
     pdos[i][4] = pdos[i - 1][4] + pdos[i][1]
     pdos[i][5] = pdos[i - 1][5] + pdos[i][2]
     pdos[i][6] = pdos[i - 1][6] + pdos[i][3]
 
 energies  = numpy.transpose(pdos)[0]
 s_project = numpy.transpose(pdos)[1]
 p_project = numpy.transpose(pdos)[2]
 d_project = numpy.transpose(pdos)[3]
 
 energies_core  =  energies[0:core_valence_divide]
 s_project_core = s_project[0:core_valence_divide]
 p_project_core = p_project[0:core_valence_divide]
 d_project_core = d_project[0:core_valence_divide]
 
 
 energies_valence  =  energies[core_valence_divide:efermi_bin]
 s_project_valence = s_project[core_valence_divide:efermi_bin]
 p_project_valence = p_project[core_valence_divide:efermi_bin]
 d_project_valence = d_project[core_valence_divide:efermi_bin]
 
 spd_sum_core    = sum(s_project_core)    + sum(p_project_core)    + sum(d_project_core)
 spd_sum_valence = sum(s_project_valence) + sum(p_project_valence) + sum(d_project_valence)

 if (spd_sum_core > 0.):
   s_fraction_core = sum(s_project_core)/spd_sum_core
   p_fraction_core = sum(p_project_core)/spd_sum_core

 else: 
   s_fraction_core, p_fraction_core = 0.,0.

 if (spd_sum_valence > 0.):
   s_fraction_valence = sum(s_project_valence)/spd_sum_valence
   p_fraction_valence = sum(p_project_valence)/spd_sum_valence
   d_fraction_valence = sum(d_project_valence)/spd_sum_valence
 
 else:
   s_fraction_valence, p_fraction_valence, d_fraction_valence = 0., 0., 0.

 print
 print "%s core", s_fraction_core*100
 print "%p core", p_fraction_core*100
 print
 print "%s valence", s_fraction_valence*100
 print "%p valence", p_fraction_valence*100
 print "%d valence", d_fraction_valence*100
 print
 print "norm = ", str(s_fraction_valence + p_fraction_valence + d_fraction_valence)
 print
 print "efermi_total = ", efermi_total
 print "spacing = ", spacing
 print
 if (subtractFermi == True): print "Note, levels have been shifted so E_Fermi = 0"
 
 for row in pdos:
     for element in row:
         outputFile_pdos.write(str(element) + ' ')
     outputFile_pdos.write('\n')

if __name__ == '__main__':
    main()

