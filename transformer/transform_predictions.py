import numpy as np 
import ast 

# Transformation for the loss function 
# Input: Depthmap, array constants k, exif1 file for img1, exif2 file for img2
def transform_prediction(depthmap, k, exif1, exif2):
    # Placeholder
    out = np.ones(depthmap.shape)

    def env_transform(depth, dist, ang):
        return np.sqrt(depth**2 + dist**2 - 2*depth*dist*np.cos(ang))

    def obj_transform(depth, k):
        if k == 0:
            return depth 
        return k*depth

    ang = float(ast.literal_eval(exif2[270])["MAPAtanAngle"])

    # Find x,y,z coords of the drone at image point
    keys = ["MAPLongitude", "MAPLatitude", "MAPAltitude"]
    coords1 = []
    coords2 = []
    for key in keys:
        coords1.append(float(ast.literal_eval(exif1[270])[key]))
        coords2.append(float(ast.literal_eval(exif2[270])[key]))

    cam_dist = np.linalg.norm(np.array(coords2)-np.array(coords1))

    for i in range(depthmap.shape[0]):
        for j in range(depthmap.shape[1]):
            if k[i,j] == 1:
                out[i,j] = env_transform(depthmap[i,j], cam_dist, ang)
            else:
                out[i,j] = obj_transform(depthmap[i,j], k[i,j])

    return out