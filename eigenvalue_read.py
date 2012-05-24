#!/usr/bin/env python

import numpy

def read_eigenvalues(subtractFermi):

    inputFile_EIGENVAL = open('EIGENVAL', 'r')
    inputFile_IBZKPT = open('IBZKPT', 'r')
    inputFile_DOSCAR = open('DOSCAR', 'r')

    for i in range(5):
        inputFile_EIGENVAL.readline()
        inputFile_DOSCAR.readline()
    for i in range(3):
        inputFile_IBZKPT.readline()

    efermi = float(inputFile_DOSCAR.readline().split()[3])


    line = inputFile_EIGENVAL.readline()

    nelectrons     = int(line.split()[0])
    nkpt           = int(line.split()[1])
    neigen_per_kpt = int(line.split()[2])

    print nelectrons, ' electrons'
    print nkpt, ' kpoints'
    print neigen_per_kpt, ' eigenvalues per kpoint'

    print 'Fermi level at: ', efermi

    wkpt_array = numpy.zeros(nkpt, dtype=int)
    eigenvalue_array = []

    for i in range(nkpt):

        eigenvalue_array.append([])

        inputFile_EIGENVAL.readline()   # skips line before data
        inputFile_EIGENVAL.readline()   # this has kpoint and float weight

        wkpt = float(inputFile_IBZKPT.readline().split()[3])
        wkpt_array[i] = wkpt

        for j in range(neigen_per_kpt):
            eigenvalue = float(inputFile_EIGENVAL.readline().split()[1])
            eigenvalue_array[-1].append(eigenvalue)


    eigenvalue_list = []

    for i in range(nkpt):

        for eigenvalue in eigenvalue_array[i]:

            if (subtractFermi == True): 
                eigenvalue_list.append(eigenvalue - efermi)
            else:
                eigenvalue_list.append(eigenvalue)


    return eigenvalue_list, wkpt_array, nkpt, neigen_per_kpt

def main():

    subtractFermi = True

    eigenvalue_list, wkpt_array, nkpt, neigen_per_kpt = read_eigenvalues(subtractFermi) 

    print 'wtk.dat file DOES work with dos_kpt.x read (6 columns per line)'
    print len(eigenvalue_list), ' eigenvalues were read'
    print 'Subtract Fermi = ', subtractFermi

#    g = Gnuplot.Gnuplot()
#    g('set data style linespoints') 
#    g.plot(sorted_array)

#    raw_input('Please press return to continue...\n')

    outputFile = open('eig.dat', 'w')

    outputFile.write('# nkptgw: ' + str(nkpt) + ' neig: ' + str(neigen_per_kpt) + '\n')
    outputFile.write('# E(DFT) E(GW)\n')

    for element in eigenvalue_list:
        outputFile.write(str(element) + ' ' + str(element) + ' \n')

    outputFile.close()

    sum_wtk = float(sum(wkpt_array))

    outputFile = open('wtk.dat', 'w')


    counter = 0

    for element in wkpt_array:
        outputFile.write(str(element/sum_wtk) + ' ')
        counter += 1
        if counter%6 == 0: outputFile.write('\n ')

    outputFile.write('\n')

    outputFile.close()

if __name__ == '__main__':
   main()
