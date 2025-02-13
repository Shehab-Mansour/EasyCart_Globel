from datetime import datetime



def category_directory_path(instance, filename):
    return 'CategoryPhotos/{0}/{1}'.format( instance.CategoryName,filename)


def product_directory_path(instance, filename):
    return 'ProductPhotos/{0}/{1}'.format( instance.ProductName,filename)



