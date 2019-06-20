import os, wget

for file in os.listdir():

	folder_name = file.replace(".txt","")
	if not os.path.isdir(folder_name):
		os.mkdir(folder_name)

	with open(file,"r") as f:
		urls = f.readlines()
		for url in urls:
			wget.download(url,out=f"./{folder_name}")