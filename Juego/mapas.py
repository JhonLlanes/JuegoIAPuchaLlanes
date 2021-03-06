import numpy
from heapq import *
'''Here is an example of using my algo with a numpy array,
   astar(array, start, destination)
   astar function returns a list of points (shortest path)'''
nmap = numpy.array([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,1],
[1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,1],
[1,0,0,0,1,1,1,0,0,1,1,1,0,0,0,1,1,0,0,0,1],
[1,0,0,0,0,0,1,0,0,1,1,1,0,0,0,1,1,0,0,0,1],
[1,0,0,0,1,0,1,0,0,1,1,1,0,0,0,1,1,0,0,0,1],
[1,0,0,0,1,0,1,0,0,1,1,1,0,0,0,1,1,0,0,0,1],
[1,1,1,1,1,0,1,0,0,1,1,1,0,0,0,1,1,0,0,0,1],
[1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,1,1,0,0,0,1],
[1,1,1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,1],
[1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,1],
[1,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,1,1,1,0,1,1,1,0,0,0,1,1,0,0,0,1],
[1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,1],
[1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])


nmapa1 = numpy.array([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
[1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1],
[1,0,1,0,1,1,1,0,1,0,0,1,0,0,0,0,0,0,0,0,1],
[1,0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,1,1,1],
[1,0,1,1,1,1,0,1,1,0,0,1,0,0,0,1,0,0,1,0,1],
[1,0,1,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,1,0,1],
[1,0,1,0,1,1,1,0,1,1,1,1,0,0,0,1,0,0,0,0,1],
[1,0,0,0,1,0,1,0,1,0,0,0,0,1,0,1,0,1,1,1,1],
[1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,0,0,0,0,1],
[1,0,0,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1,1,0,1],
[1,0,1,1,1,1,1,0,1,1,0,1,0,1,0,1,0,0,1,1,1],
[1,0,0,0,0,0,0,0,1,0,0,1,1,1,0,1,0,1,1,0,1],
[1,0,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,1,0,0,1],
[1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,0,1],
[1,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])

nmapa2 = numpy.array([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
[1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1],
[1,0,1,0,1,1,1,0,1,0,0,1,0,0,0,0,0,0,0,0,1],
[1,0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,1,1,1],
[1,0,1,1,1,1,0,1,1,0,0,1,0,0,0,1,0,0,1,0,1],
[1,0,1,0,0,0,0,0,0,0,0,1,1,1,0,1,1,0,1,0,1],
[1,0,1,0,1,0,1,0,1,1,1,1,0,0,0,1,0,0,0,0,1],
[1,0,0,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,1,1,1],
[1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,0,0,0,0,1],
[1,0,0,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1,1,0,1],
[1,0,1,1,1,1,1,0,1,1,0,1,0,1,0,1,0,0,1,1,1],
[1,0,0,0,0,0,0,0,1,0,0,1,1,1,0,1,0,1,1,0,1],
[1,0,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,1,0,0,1],
[1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,0,1],
[1,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])


nmapa3 = numpy.array([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
[1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1],
[1,0,1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,1,0,0,0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,1],
[1,0,1,0,1,1,0,1,1,0,0,1,0,0,0,1,0,0,1,0,1],
[1,0,1,0,0,0,0,1,0,0,0,1,1,1,0,1,1,1,1,0,1],
[1,0,1,0,1,1,1,0,1,1,1,1,0,0,0,1,0,0,0,0,1],
[1,0,0,0,1,0,1,0,1,0,0,0,0,1,0,1,0,1,1,1,1],
[1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,0,0,0,0,1],
[1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,1,1,0,1],
[1,0,1,1,1,1,1,0,1,1,0,1,0,1,0,1,0,0,1,1,1],
[1,0,0,0,0,0,0,0,1,0,0,1,1,1,0,1,0,1,1,0,1],
[1,0,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,1,0,0,1],
[1,0,1,0,0,0,0,0,1,0,0,1,0,1,1,1,1,1,1,0,1],
[1,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])


nmapa4 = numpy.array([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
[1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1],
[1,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
[1,0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,1,0,1],
[1,0,1,1,1,1,0,1,1,0,0,1,0,0,0,1,0,0,1,0,1],
[1,0,1,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,1,0,1],
[1,0,1,0,1,1,1,0,1,1,1,1,0,0,0,1,0,0,0,0,1],
[1,0,0,0,1,0,1,0,1,0,0,0,0,1,0,1,0,1,1,1,1],
[1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,0,0,0,0,1],
[1,0,0,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1,1,0,1],
[1,0,1,1,1,1,1,0,1,1,0,1,0,1,0,1,0,0,1,1,1],
[1,0,0,0,0,0,0,0,1,0,0,1,1,1,0,1,0,1,1,0,1],
[1,0,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,1,0,0,1],
[1,0,1,0,1,0,0,0,0,0,0,1,0,1,1,1,1,1,1,0,1],
[1,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])


nmapa5 = numpy.array([
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
[1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1],
[1,0,1,0,1,1,1,0,1,0,0,1,0,0,1,0,0,0,0,0,1],
[1,0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,1,1,1],
[1,0,1,1,1,1,0,1,1,0,0,1,0,0,0,1,0,0,1,0,1],
[1,0,1,0,0,0,0,0,0,0,0,1,1,1,0,1,1,0,1,0,1],
[1,0,1,0,1,0,1,0,1,1,1,1,0,0,0,1,0,0,0,0,1],
[1,0,0,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,1,1,1],
[1,1,1,1,1,0,0,0,1,0,1,1,1,1,1,1,0,0,0,0,1],
[1,0,0,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1,1,0,1],
[1,0,1,1,0,1,1,0,1,1,0,1,0,1,0,1,0,0,1,1,1],
[1,0,0,0,0,0,1,0,1,0,0,1,1,1,0,1,0,1,1,0,1],
[1,0,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,1,0,0,1],
[1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,1,1],
[1,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])
