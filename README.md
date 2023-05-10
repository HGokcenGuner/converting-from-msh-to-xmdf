# converting-from-msh-to-xmdf
1. Save the gmsh file in Version II ASCII with all elements but not withparametric coordinates
2. Delete all elements of their second values that are different than 2. (truss elements T3D2 in INP)
3. Change the first value under the Elements (total number of elements)
4. Run the code


NOTES:
- Add the surfaces as:
//+
Physical Surface("main",1) = {1,2};
//+
Physical Surface("filled",2) = {2};

- Export as a msh file only with "all elements"

