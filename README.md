# dmpso
Discrete Multi-Objective Particle Swarm Optimization

To run the program, execute python dmpso.py on the command line. The current hard coded values for number of abstract services and candidate services are 5 and 5 respectively.

The generator file for contraints is Q_c_generator.py. Running this file will generate the constraints for an assortment of graphs defined by running autograph_gen_new.py.

To generate graphs with different number of abstract and candidate services, run generate_table.py. This file calls autograph_gen_new.py to generate different composition graphs. Appropriate modifications can be made to the dmpso file to change the number of abstract and candidate services.
