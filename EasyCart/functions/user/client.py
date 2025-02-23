from datetime import datetime


def client_directory_path(instance, filename):
    year = datetime.now().strftime('%y')
    return 'clientPhotos/{0}/{1}/{2}'.format( instance.clientUserName,year,filename)
