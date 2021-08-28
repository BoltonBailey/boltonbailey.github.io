
## Linear Transformation Matrix Correspondence

Written 2018-01-01T13:37:00-08:00,

Linear algebra uses operations on scalars, vectors and matrices to "algebraize" the theory of linear transformations. So every concept, property or relation in the study of matrices should correspond to concept, property or relation in the theory of linear transformations. I made a table to keep track of these correspondences (there are some gaps).

| Matrix                             | Linear Transformation                                                             |
| ---------------------------------- | --------------------------------------------------------------------------------- |
| $d_1 \times d_2$ Matrix            | Linear transformation $\mathbb{R}^{d_1} \to \mathbb{R}^{d_2}$                     |
| Number of rows of a matrix         | Output space dimension                                                            |
| Number of columns of a matrix      | Input space dimension                                                             |
| ($d$-entry) vector                 | Point in $\mathbb{R}^d$                                                           |
| Matrix - vector multiplication     | Linear function evaluation at a point                                             |
| Matrix - Matrix multiplication     | Linear function composition                                                       |
| Matrix - Matrix addition           | Pointwise linear functional addition                                              |
| $I$ The Identity Matrix            | Identity map                                                                      |
| Eigenvector of a Matrix            | Point scaled by linear transformation                                             |
| Eigenvalue                         | Scale factor                                                                      |
| Norm of a vector                   | Distance of a point from the origin                                               |
| Inner product of vectors           | Area of parallelogram formed from the segments from the origin to the points      |
| Matrix inverse                     | Function inverse                                                                  |
| Orthonormal matrix                 | Isometric linear transformation (rotation)                                        |
| Matrix rank                        | Dimension of image of linear map.                                                 |
| Column span                        | Image of linear map                                                               |
|                                    | Projection transformation                                                         |
| Singular vectors                   | Directions of axes of ellipse obtained by mapping unit sphere thru transformation |
| Singular values                    | Lengths of axes                                                                   |
| Transpose                          | The canonical map between dual spaces                                             |
| Trace                              |                                                                                   |
| Determinant                        | Volumetric scaling of linear transformation                                       |
| Frobenius matrix norm              |                                                                                   |
| (p, q) matrix norm                 |                                                                                   |
| unitary matrix                     |                                                                                   |
| Spectral matrix norm/operator norm | Lipschitz constant                                                                |
