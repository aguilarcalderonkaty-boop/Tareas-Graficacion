import cv2 as cv
# Lee en escala de grises
img = cv.imread('ejemplo.jpg', 0)
cv.imshow('Ejemplo', img)  
cv.waitKey()               
cv.destroyAllWindows()      