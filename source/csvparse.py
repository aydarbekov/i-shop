import csv, sys, os

project_dir = "/home/akyl/attractor/projects/i_shop/source/main"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django
django.setup()
from webapp.models import Product
data = csv.reader(open("/home/akyl/attractor/projects/i-shop/source/bumaga_i_bum_izdelia.csv"), delimeter='|')

for row in data:
    if row[0] != 'Name':
        product = Product()
        product.name = row[0]
        product.description = row[1]
        product.category = row[4]
        product.subcategory = row[3]
        product.save()
        for img in row[2]:
            product.images.create(img)