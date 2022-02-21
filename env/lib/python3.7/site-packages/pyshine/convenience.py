# author:    PyShine
# website:   http://www.pyshine.com

# import the necessary packages
import numpy as np
import cv2
import socket,time
import queue
try:
	import sounddevice as sd
	import tempfile
	import soundfile as sf
except Exception as e:
	print('Warning!',e)
	pass
import threading

try:
	import matplotlib
	import copy
	import matplotlib.pyplot as plt
	import matplotlib.animation as animation
	from matplotlib.animation import FuncAnimation
except Exception as e:
	print('Warning!',e)
	pass

import _thread
from multiprocessing import Process
from collections import deque

try:
	from keras.models import Sequential
	from keras.layers.convolutional import Conv2D
	from keras.layers.convolutional import MaxPooling2D
	from keras.layers.core import Activation
	from keras.layers.core import Flatten
	from keras.layers.core import Dense
except Exception as e:
	print('Warning!',e)
	pass
from socketserver import ThreadingMixIn
import socketserver
import logging
from http import server
import io
from threading import Condition

def putBText(img,text,text_offset_x=20,text_offset_y=20,vspace=10,hspace=10, font_scale=1.0,background_RGB=(228,225,222),text_RGB=(1,1,1),font = cv2.FONT_HERSHEY_DUPLEX,thickness = 2,alpha=0.6,gamma=0):
	"""
    Inputs:
    img: cv2 image img
    text_offset_x, text_offset_x: X,Y location of text start
    vspace, hspace: Vertical and Horizontal space between text and box boundries
    font_scale: Font size
    background_RGB: Background R,G,B color
    text_RGB: Text R,G,B color
    font: Font Style e.g. cv2.FONT_HERSHEY_DUPLEX,cv2.FONT_HERSHEY_SIMPLEX,cv2.FONT_HERSHEY_PLAIN,cv2.FONT_HERSHEY_COMPLEX
          cv2.FONT_HERSHEY_TRIPLEX, etc
    thickness: Thickness of the text font
    alpha: Opacity 0~1 of the box around text
    gamma: 0 by default

    Output:
    img: CV2 image with text and background
	"""
	R,G,B = background_RGB[0],background_RGB[1],background_RGB[2]
	text_R,text_G,text_B = text_RGB[0],text_RGB[1],text_RGB[2]
	(text_width, text_height) = cv2.getTextSize(text, font, fontScale=font_scale, thickness=thickness)[0]
	x, y, w, h = text_offset_x, text_offset_y, text_width , text_height
	crop = img[y-vspace:y+h+vspace, x-hspace:x+w+hspace]
	white_rect = np.ones(crop.shape, dtype=np.uint8)
	b,g,r = cv2.split(white_rect)
	rect_changed = cv2.merge((B*b,G*g,R*r))


	res = cv2.addWeighted(crop, alpha, rect_changed, 1-alpha, gamma)
	img[y-vspace:y+vspace+h, x-hspace:x+w+hspace] = res

	cv2.putText(img, text, (x, (y+h)), font, fontScale=font_scale, color=(text_B,text_G,text_R ), thickness=thickness)
	return img



def audioCapture(mode='send',record=False,filename='recorded',typename='.wav',dirname=''):
	q = deque(maxlen=20)
	filename = tempfile.mktemp(prefix=filename,suffix=typename, dir=dirname)
	frame = [0]
	audio = queue.Queue(maxsize=20)
	def getAudio():
		def callback(indata, outdata, frames, time, status):
			
			if status:
				print(status)

			if mode=='get':
				try:
					frame = audio.get()
					outdata[:] = frame
					q.append(frame)
					
				except :
					pass
			else:
				audio.put(indata)
				q.append(indata)
		if record==True:
			with sf.SoundFile(filename, mode='x', samplerate=44100,channels=2) as file:	
				with sd.Stream( channels=2,blocksize=1024, callback=callback):
					print('press Ctrl+C to stop the recording')
					
					file.write(audio.get())
					# input()
					# exit()
		else:
			with sd.Stream( channels=2,blocksize=1024, callback=callback):
				input()
				exit()	
		
			
	thread = threading.Thread(target=getAudio, args=())
	thread.start()
	return audio,q








def showPlot(audio,name='pyshine.com',length=8,xmin=0,ymin=-0.5,xmax=8*1024,ymax=0.5,color = (0,1,0.29)):
	def getAudio():
	
		global plotdata
		frame = [0]
		length=8
		fig,ax = plt.subplots(figsize=(8,2))
		ax.set_title('naem')
		plotdata =  np.zeros((length*1024,2))
		lines = ax.plot(plotdata,color = color)
			

		ax.set_facecolor((0,0,0))
		ax.set_ylim( ymin=ymin, ymax=ymax)	
		ax.set_xlim( xmin=xmin, xmax=xmax)	


		def animate(i):
			global plotdata
			try:

				ys = []
				
				ys = audio.pop()
				data = ys
				shift = len(data)
				plotdata = np.roll(plotdata, -shift,axis = 0)
				plotdata[-shift:,:] = data

				
				T= ys.shape[0]
				ys = ys[0:T//1]
				X_m = ys

				ax.set_title(name)		
			except Exception as e:
				try:

					ax.set_title(name)		

				except:
					pass
				pass
				
			for column, line in enumerate(lines):
				line.set_ydata(plotdata[:,column])
			return lines
		
		ani  = FuncAnimation(fig,animate, interval=30)
		while True:
			plt.ion()
			plt.show()
			plt.pause(0.001)	

	thread = threading.Thread(target=getAudio, args=())
	thread.start()

			





def _showPlot(audio,xmin=0,ymin=-0.5,xmax=1024,ymax=0.5):
	name='name'
	# Get the Figure
	fig = plt.figure(figsize=(8,3))
	ax = fig.add_subplot(1,1,1)
	ax.set_facecolor((0,0,0)) 
	fig.tight_layout() 
	ax.yaxis.grid(True)


	def animate(i):
		
		try:
			ax.clear()
			ys = []
			ys = audio.get()
			audio.task_done()
			T= ys.shape[0]
			ys = ys[0:T//1]
			X_m = ys
			ax.plot(X_m, '.', color = (0.25,1,0))
			ax.set_ylim( ymin=ymin, ymax=ymax)	
			ax.set_xlim( xmin=xmin, xmax=xmax)	
			ax.set_title(name)		
		except Exception as e:
			try:
				ax.set_ylim( ymin=ymin, ymax=ymax)	
				ax.set_xlim( xmin=xmin, xmax=xmax)	
				ax.set_title(name)		

			except:
				pass
			pass
			print(e)
			
	# Lets call the animation function 	
	ani = animation.FuncAnimation(fig, animate, interval=30)
	plt.ion()
	plt.show()
	plt.pause(0.001)




class RPSNET:
	
	def build(width, height, depth, classes):
		
		model = Sequential()
		inputShape = (height, width, depth)
		model.add(Conv2D(20, (5, 5), padding="same",
			input_shape=inputShape))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
		model.add(Conv2D(50, (5, 5), padding="same"))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
		model.add(Flatten())
		model.add(Dense(64))
		model.add(Activation("sigmoid"))
		model.add(Dense(classes))
		model.add(Activation("sigmoid"))

		return model


class StreamOut(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()
    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)
        
class Streamer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    
class StreamProps(server.BaseHTTPRequestHandler):

    def set_Page(self,PAGE):
        self.PAGE = PAGE
    def set_Capture(self,capture):
        self.capture = capture
    def set_Quality(self,quality):
        self.quality = quality
    def set_Mode(self,mode):
        self.mode = mode
    def set_Output(self,output):
        self.output = output
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = self.PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            if self.mode == 'cv2':
                try:
                    while True:
                        rc,img = self.capture.read()
                        
                        frame = cv2.imencode('.JPEG', img,[cv2.IMWRITE_JPEG_QUALITY,self.quality])[1].tobytes()
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                except Exception as e:
                    logging.warning(
                        'Removed streaming client %s: %s',
                        self.client_address, str(e))
            if self.mode == 'picamera':
                try:
                    while True:
                        
                        with self.output.condition:
                            self.output.condition.wait()
                            frame = self.output.frame   
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                except Exception as e:
                    logging.warning(
                        'Removed streaming client %s: %s',
                        self.client_address, str(e))
        
        else:
            self.send_error(404)
            self.end_headers()

# TEXT examples
# Hershey Simplex
# Hershey Plain
# Hershey Duplex
# Hershey Complex
# Hershey Triplex
# Hershey Complex Small
# Hershey Script Simplex
# Hershey Script Complex
