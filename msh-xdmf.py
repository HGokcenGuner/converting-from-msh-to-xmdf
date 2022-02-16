from dolfin import *
import argparse
import meshio
import os

from dolfin import *
from configparser import ConfigParser
import numpy as np

# Importing mesh from gmsh and defining surface and boundary markers
msh = meshio.read("mesh32_2.msh")

# print(msh.cell_sets_dict)


print(msh.cell_data_dict)
for key in msh.cell_data_dict["gmsh:geometrical"].keys():
    if key == "triangle":
        triangle_data = msh.cell_data_dict["gmsh:geometrical"][key]

for cell in msh.cells:
    if cell.type == "tetra":
        tetra_cells = cell.data
    elif cell.type == "triangle":
        triangle_cells = cell.data

triangle_mesh =meshio.Mesh(points=msh.points,
                           cells=[("triangle", triangle_cells)],
                           cell_data={"name_to_read":[triangle_data]})

meshio.write("mesh.xdmf", triangle_mesh)

mesh = Mesh()
mvc = MeshValueCollection("size_t", mesh, mesh.topology().dim())
with XDMFFile("mesh.xdmf") as infile:
    infile.read(mesh)

mvc = MeshValueCollection("size_t", mesh, mesh.topology().dim())
with XDMFFile("mesh.xdmf") as infile:
    infile.read(mvc, "name_to_read")
mf = cpp.mesh.MeshFunctionSizet(mesh, mvc)

print(mesh.topology().dim() - 1)
File("MSH.pvd") << mesh

File("MSH2.pvd") << mf

boundary_markers = MeshFunction('size_t', mesh, mesh.topology().dim()-1, 0)

class Boundary(SubDomain):
    def inside(self, x, on_boundary):
        return on_boundary and near(x[1], 0.0)

b_c = Boundary()
b_c.mark(boundary_markers, 3)

File("MSH3.pvd") << boundary_markers
# Compiling subdomains

ds = Measure('ds', domain=mesh, subdomain_data=boundary_markers)

dx_filled = Measure("dx", domain=mesh, subdomain_data=mf, subdomain_id=2)
dx_main = Measure("dx", domain=mesh, subdomain_data=mf, subdomain_id=1)


