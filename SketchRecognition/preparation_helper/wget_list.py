
import os as os


categories_list = []
with open('categories.txt', 'r') as categories:
    for category in categories:
        categories_list.append(category)
    print(len(categories_list))
    

with open('script.txt', 'w') as out:
     for category in categories_list:
         out.write('wget "https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/' + category[:-1] + '.npy"\n')
    