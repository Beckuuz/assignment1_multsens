import numpy as np
import matplotlib.pyplot as plt


#Simple function to visualize 4 arrays that are given to it
def visualize_data(timestamps, x_arr,y_arr,z_arr,s_arr):
  #Plotting accelerometer readings
  plt.figure(1)
  plt.plot(timestamps, x_arr, color = "blue",linewidth=1.0)
  plt.plot(timestamps, y_arr, color = "red",linewidth=1.0)
  plt.plot(timestamps, z_arr, color = "green",linewidth=1.0)
  plt.show()
  #magnitude array calculation
  m_arr = []
  for i, x in enumerate(x_arr):
    m_arr.append(magnitude(x_arr[i],y_arr[i],z_arr[i]))
  plt.figure(2)
  #plotting magnitude and steps
  plt.plot(timestamps, s_arr, color = "black",linewidth=1.0)
  plt.plot(timestamps, m_arr, color = "red",linewidth=1.0)
  plt.show()

#Function to read the data from the log file
#TODO Read the measurements into array variables and return them
def read_data(filename):
  #TODO implementation
  timestamps = []
  x_array = []
  y_array = []
  z_array = []
  with open(filename, newline="") as csvfile:
    for row in csvfile:
      temp1,x,y,z = row.split(sep=",")
      timestamps.append(float(temp1))
      x_array.append(float(x))
      y_array.append(float(y))
      z_array.append(float(z))
  print(x_array)

  return timestamps, x_array, y_array, z_array
  #return [0],[0],[0],[0]

#Function to count steps.
#Should return an array of timestamps from when steps were detected
#Each value in this arrray should represent the time that step was made.
def count_steps(timestamps, x_arr, y_arr, z_arr):
  #TODO: Actual implementation
  rv = []
  meanx,meany,meanz = meancalc(x_arr,y_arr,z_arr)
  for i, time in enumerate(timestamps):
    if((x_arr[i] < meanx) & (z_arr[i] > meanz) & (y_arr[i] < meany)  ):
      rv.append(time)
  return rv

#calculate mean value of arrays
def meancalc(x_arr, y_arr, z_arr):
  meanx = 0
  meany = 0
  meanz = 0
  for i in x_arr:
    add = i + meanx
  for i in y_arr:
    add = i + meany
  for i in z_arr:
    add = i + meanz
  meanx = meanx / len(x_arr)
  meany = meany / len(y_arr)
  meanz = meanz / len(z_arr)
  return meanx,meany,meanz

#Calculate the magnitude of the given vector
def magnitude(x,y,z):
  return np.linalg.norm((x,y,z))

#Function to convert array of times where steps happened into array to give into graph visualization
#Takes timestamp-array and array of times that step was detected as an input
#Returns an array where each entry is either zero if corresponding timestamp has no step detected or 50000 if the step was detected
def generate_step_array(timestamps, step_time):
  s_arr = []
  ctr = 0
  for i, time in enumerate(timestamps):
    if(ctr<len(step_time) and step_time[ctr]<=time):
      ctr += 1
      s_arr.append( 50000 )
    else:
      s_arr.append( 0 )
  while(len(s_arr)<len(timestamps)):
    s_arr.append(0)
  return s_arr

#Check that the sizes of arrays match
def check_data(t,x,y,z):
  if( len(t)!=len(x) or len(y)!=len(z) or len(x)!=len(y) ):
    print("Arrays of incorrect length")
    return False
  print("The amount of data read from accelerometer is "+str(len(t))+" entries")
  return True

def main():
  #read data from a measurement file, change the inoput file name if needed
  timestamps, x_array, y_array, z_array = read_data("out_400.csv")
  #Chek that the data does not produce errors
  if(not check_data(timestamps, x_array,y_array,z_array)):
    return
  #Count the steps based on array of measurements from accelerometer
  st = count_steps(timestamps, x_array, y_array, z_array)
  #Print the result
  print("This data contains "+str(len(st))+" steps according to current algorithm")
  #convert array of step times into graph-compatible format
  s_array = generate_step_array(timestamps, st)
  #visualize data and steps
  visualize_data(timestamps, x_array,y_array,z_array,s_array)

main()

