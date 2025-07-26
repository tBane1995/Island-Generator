import sdl2
import sdl2.ext
import time
import numpy as np

class Map:
	
	wdt : int
	hgh : int
	tiles = []

	water = '.'
	sands = ':'
	grass = '#'


	def __init__(self, width: int, height: int):
		self.wdt = width
		self.hgh = height
		self.tiles = np.empty((self.hgh, self.wdt), dtype=str)

	def clear(self):
		for y in range(0,self.hgh):
			for x in range(0,self.wdt):
				self.tiles[y][x] = self.water

	def char_in_range(self, char, r, x : int, y : int):
		for yy in range(y-r, y+r+1):
			for xx in range(x-r, x+r+1):
				if xx>=0 and yy>=0 and xx<self.wdt and yy<self.hgh and self.tiles[yy][xx] == char:
					return True
	
		return False

	def add_sands(self):
		for y in range(0,self.hgh):
			for x in range(0,self.wdt):	
				if self.tiles[y][x] == self.grass and self.char_in_range(self.water, 2, x, y):
					self.tiles[y][x] = self.sands

	def generate_island(self, cx : int, cy : int, radius : int, neighbours : int, iter : int):
		if iter > 0:
			for y in range(int(cy-radius),int(cy+radius)):
				for x in range(int(cx-radius),int(cx+radius)):
					if y>= 0 and x>=0 and y<self.hgh and x<self.wdt:
						if (np.pow(cx-x,2)+np.pow(cy-y,2) < np.pow(radius,2)*0.995):
							self.tiles[y][x] = self.grass
						
			for i in range(1, int(neighbours)):
				
				angle = np.random.uniform(0, 2*np.pi)
				r = radius*np.random.uniform(1/2, 6/8)
				nn = np.random.randint(4,7)
				cx2 = int(cx + 2*r*np.sin(angle))
				cy2 = int(cy + 2*r*np.cos(angle))
				
				self.generate_island(cx2, cy2, r, nn, iter-1)

	def generate(self):
		self.clear()
		
		if self.wdt < self.hgh:
			radius = self.wdt
		else:
			radius = self.hgh
		
		radius = radius / 6
		
		cx = self.wdt//2
		cy = self.hgh//2
		
		ngbrs = np.random.randint(4,7)
		
		iterations = radius/2.5
		
		self.generate_island(cx, cy, radius, ngbrs, iterations)
		self.add_sands()

	def as_string(self) -> str :
		string : str
		string = ""

		for y in range(0,self.hgh):
			for x in range(0,self.wdt):	
				string = string + self.tiles[y][x]
			string = string + "\n"

		return string

	def draw(self, renderer, tile_size):
		for y in range(self.hgh):
			for x in range(self.wdt):
				tile = self.tiles[y][x]
            
				if tile == self.water:
					renderer.color = sdl2.ext.Color(64, 64, 192)
            
				if tile == self.sands:
					renderer.color = sdl2.ext.Color(192, 192, 128)
            
				if tile == self.grass:
					renderer.color = sdl2.ext.Color(64, 128, 64)
            
				rect = sdl2.SDL_Rect(tile_size*x, tile_size*y, tile_size, tile_size)
				renderer.fill(rect)

	