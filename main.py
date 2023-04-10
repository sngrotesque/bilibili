import bililib

blbl = bililib.article(383177991)
blbl.GetLinksToAllPictures

for x in range(len(blbl.results_pictures_links)):
    print(f'{x+1:0>3} {blbl.results_pictures_links[x]}')
