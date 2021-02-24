from pyshader import *

@python2shader
def compute_shader(index=("input", "GlobalInvocationId", ivec3),
                            data1=("buffer", 0, Array(f32)),
                            data2=("buffer", 1, Array(f32)),
                            data3=("buffer", 2, Array(f32)),
                            data4=("buffer", 3, Array(f32))):
    i = index.x
    data4[i] = data1[i] * data2[i] * data3[i]

with open("shader.spirv",'wb') as file:
    file.write(compute_shader.to_spirv())

