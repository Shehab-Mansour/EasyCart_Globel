from datetime import datetime

from django.contrib.auth.hashers import make_password


def worker_directory_path(instance, filename):
    year = datetime.now().strftime('%y')
    return 'workerPhotos/{0}/{1}/{2}'.format( instance.WorkerUserName,year,filename)

def password(WorkerUserName):
    password = make_password(WorkerUserName)
    return '{0}'.format(password)
