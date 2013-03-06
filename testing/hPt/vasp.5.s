#!/bin/bash
#PBS -N BDA_check
#PBS -q nano2
#PBS -l nodes=32:ppn=2:nano2
#PBS -l walltime=24:00:00
# specify the queue: lr_debug, lr_batch 
#PBS -A ac_nanotheory
#PBS -m aeb
#PBS -M isaac.tamblyn+scheduler@gmail.com
#PBS -V
#PBS -e job.err
#PBS -o job.out


cd $PBS_O_WORKDIR

echo $PBS_JOBID >> job.out

module unload openmpi
module load openmpi/1.3.3-intel

module load vasp/5.2.11
EXE=`which vasp`

NPROCS=`wc -l $PBS_NODEFILE | awk '{print $1}'`

mpirun --mca btl openib,sm,self  $EXE >& log
