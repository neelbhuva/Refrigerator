import pandas as pd
import math
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

def convertStrToDatetime(df):
	temp = []
	for i in df:
		i = i.strip()
		temp.append(dt.datetime.strptime(i, '%Y-%m-%d %H:%M:%S.%f'))
	return temp

def getRowsInInterval(df,t1,t2):
	c1 = df["datetime"] >= t1
	c2 = df["datetime"] <= t2
	df = df[c1 & c2]
	return df

def convertDatetimeToHours(df,t1,t2):
	temp = [0]
	for i in range(1,len(df["datetime"])):
		t = df["datetime"][i] - df["datetime"][i-1] 
		temp.append(t.days * 24 + (t.seconds/3600))
	for i in range(1,len(temp)):
		temp[i] = temp[i] + temp[i-1] 
	temp[:] = [x - temp[0] for x in temp]
	return temp

def fixDiscontinuity(df):
	c1 = df['ambient_temp'] == 0
	zero_indices = df[c1].index
	#print(df)
	#print(zero_indices)
	for i in range(0,len(zero_indices)):
		if(zero_indices[i] == 0):
			continue
		else:
			if(i == (len(zero_indices)-1)):
				#print(df["ambient_temp"][zero_indices[i]-1])
				df_temp = df["ambient_temp"][zero_indices[i]-1] + df["ambient_temp"][zero_indices[i]:(len(df["ambient_temp"]))]
				df["ambient_temp"][zero_indices[i]:(len(df["ambient_temp"]))] = df_temp
			else:
				#print(df["ambient_temp"][zero_indices[i]-1])
				df_temp = df["ambient_temp"][zero_indices[i]-1] + df["ambient_temp"][zero_indices[i]:(zero_indices[i+1])]
				#print(df_temp)
				df["ambient_temp"][zero_indices[i]:(zero_indices[i+1])] = df_temp
	return df

def avgMaxMinTemp(df,t1,t2):
	#convert datetime column datatype to string
	df['datetime'] = df['datetime'].astype(str)
	#convert string datetime to python datetime object
	df["datetime"] = convertStrToDatetime(df["datetime"])
	#all rows with datetime >=t1 and <=t2
	df = getRowsInInterval(df,t1,t2)
	
	df = df.reset_index(drop=True)
	t = t2-t1
	#number of hours in the interval [t1,t2]
	num_of_hours = t.days * 24 + (t.seconds/3600)
	#num_of_hours = len(df["ambient_temp"])
	#making first energy value 0
	#df = fixDiscontinuity(df)
	#df["ambient_temp"] = df["ambient_temp"] - df["ambient_temp"][0]
	print(df.shape)
	average = np.average(df["ambient_temp"])
	maximum = np.max(df["ambient_temp"])
	minimum = np.min(df["ambient_temp"])
	var = np.var(df["ambient_temp"])
	return [average,maximum,minimum,var]

def plot(df,t1,t2,label):
	df = getRowsInInterval(df,t1,t2)
	df = df.reset_index(drop=True)
	#df = fixDiscontinuity(df)
	x = convertDatetimeToHours(df,t1,t2)
	#print(np.max(x))
	#df["ambient_temp"] = df["ambient_temp"] - df["ambient_temp"][0]
	#print(len(df["ambient_temp"]),len(x))
	df["ambient_temp"] = [((9/5)*x+32) for x in df["ambient_temp"]]
	plt.hist(df["ambient_temp"],label=label)
	plt.ylabel("Frequency of temp")
	plt.xlabel("Temperature in Fahrenheit")
	#plt.axis([x[0], x[len(x)-1], df["ambient_temp"][0], df["ambient_temp"][len(df["ambient_temp"])-1]])

def phase1(df_mario,df_maria,df_odaly):
	#mario
	t1 = dt.datetime.strptime('2017-07-11 01:00:19.445607', '%Y-%m-%d %H:%M:%S.%f')
	t2 = dt.datetime.strptime('2017-07-19 11:00:50.900432', '%Y-%m-%d %H:%M:%S.%f')
	avg_mario = avgMaxMinTemp(df_mario,t1,t2)
	fig1 = plt.figure(1)
	plot(df_mario,t1,t2,"Without Curtain : Mario")
	fig1.suptitle("Mario")
	#maria
	t1 = dt.datetime.strptime('2017-07-13 04:33:07.203739', '%Y-%m-%d %H:%M:%S.%f')
	t2 = dt.datetime.strptime('2017-07-19 14:00:30.550984', '%Y-%m-%d %H:%M:%S.%f')
	avg_maria = avgMaxMinTemp(df_maria,t1,t2)
	fig2 = plt.figure(2)
	plot(df_maria,t1,t2,"Without Curtain : Maria")
	fig2.suptitle("Maria")
	#odaly
	t1 = dt.datetime.strptime('2017-07-10 21:07:29.582749', '%Y-%m-%d %H:%M:%S.%f')
	t2 = dt.datetime.strptime('2017-07-17 15:02:22.179892', '%Y-%m-%d %H:%M:%S.%f')
	avg_odaly = avgMaxMinTemp(df_odaly,t1,t2)
	fig3 = plt.figure(3)
	plot(df_odaly,t1,t2,"Without Curtain : Odaly")
	fig3.suptitle("Odaly")

	return (avg_mario,avg_maria,avg_odaly)


def phase2(df_mario,df_maria,df_odaly):
	#mario
	t1 = dt.datetime.strptime('2017-07-19 17:03:13.259785', '%Y-%m-%d %H:%M:%S.%f')
	t2 = dt.datetime.strptime('2017-07-24 14:00:03.62218', '%Y-%m-%d %H:%M:%S.%f')
	avg_mario = avgMaxMinTemp(df_mario,t1,t2)
	fig1 = plt.figure(1)
	plot(df_mario,t1,t2,"With Curtain : Mario")
	plt.legend()
	plt.savefig("mario.png")
	#maria
	t1 = dt.datetime.strptime('2017-07-19 20:02:12.771476', '%Y-%m-%d %H:%M:%S.%f')
	t2 = dt.datetime.strptime('2017-07-24 07:41:40.000926', '%Y-%m-%d %H:%M:%S.%f')
	avg_maria = avgMaxMinTemp(df_maria,t1,t2)
	fig2 = plt.figure(2)
	plot(df_maria,t1,t2,"With Curtain : Maria")
	plt.legend()
	plt.savefig("maria.png")
	#odaly
	t1 = dt.datetime.strptime('2017-07-17 20:00:05.376021', '%Y-%m-%d %H:%M:%S.%f')
	t2 = dt.datetime.strptime('2017-07-24 13:03:14.502509', '%Y-%m-%d %H:%M:%S.%f')
	avg_odaly = avgMaxMinTemp(df_odaly,t1,t2)
	fig3 = plt.figure(3)
	plot(df_odaly,t1,t2,"With Curtain : Odaly")
	plt.legend()
	plt.savefig("odaly.png")
	
	return (avg_mario,avg_maria,avg_odaly)

if __name__ == '__main__':
	#read the files into dataframes
	df_mario = pd.read_csv("mario_ambient_table.csv")
	df_maria = pd.read_csv("maria_ambient_table.csv")
	df_odaly = pd.read_csv("odaly_ambient_table.csv")

	#get required columns
	df_mario = pd.concat([df_mario['datetime'], df_mario['ambient_temp']], axis=1)
	df_maria = pd.concat([df_maria['datetime'], df_maria['ambient_temp']], axis=1)
	df_odaly = pd.concat([df_odaly['datetime'], df_odaly['ambient_temp']], axis=1)

	#drop rows that do not have values for datetime column
	df_mario = df_mario.dropna(axis=0,subset=['datetime'])
	df_maria = df_maria.dropna(axis=0,subset=['datetime'])
	df_odaly = df_odaly.dropna(axis=0,subset=['datetime'])

	#print(df_odaly.head())
	avg = {'phase1' : { 'mario' : 0, 'maria' : 0, 'odaly' : 0}, 'phase2' : { 'mario' : 0, 'maria' : 0, 'odaly' : 0}}
	(a,b,c) = phase1(df_mario,df_maria,df_odaly)
	(d,e,f) = phase2(df_mario,df_maria,df_odaly)
	print("Phase 1 Temp")
	print("Mario : " + str(a) + " " + "Maria : " + str(b) + "	Odaly : "+ str(c))
	print("Phase 2 Temp")
	print("Mario : " + str(d) + " " + "Maria : " + str(e) + "	Odaly : "+ str(f))
	