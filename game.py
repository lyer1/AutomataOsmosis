import pygame, sys, os, random, pickle
import math as math_lib
from pygame import *

pygame.init()



BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LIGHT_BLUE = (0, 0, 255)
STATE_RADIUS = 35
ST_RAD = STATE_RADIUS
SEEN = set()
SCREEN_SIZE = (1290, 720)


DATADIR = os.path.join(os.path.dirname(
    sys.executable  # When frozen
    if getattr(sys, 'frozen', False)
    else __file__   # When not frozen
), 'res', '')

data = lambda name :os.path.join(DATADIR, name)

FPS_CLOCK = pygame.time.Clock()

touple_diff = lambda a, b : ((b[0] - a[0]), (b[1] - a[1]))

def point_on_line(a, b, r):
	x1, y1 = a
	x2, y2 = b

	length = math_lib.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

	unit_vector = ((x2 - x1) / length, (y2 - y1) / length) if length else [0, 0]

	point = (x1 - r * unit_vector[0], y1 - r * unit_vector[1])
	
	return point

flags = RESIZABLE | SCALED
screen = pygame.display.set_mode(SCREEN_SIZE, flags)
pygame.RESIZABLE = True
my_font = pygame.font.SysFont('Comic Sans MS', 25)
my_font2 = pygame.font.SysFont('Comic Sans MS Bold', 25)
pygame.display.update()
mouse_obj = pygame.mouse
state_count = 0


icon = image.load(data("icon.ico"))
pygame.display.set_caption('Automaton Osmosis')
display.set_icon(icon)

background = transform.scale(image.load(data("bg2.jpg")), SCREEN_SIZE).convert()
main_logo = image.load(data("logo.png"))

song_number = random.randint(0, 2)

levels = []
level_ptr = 0

class Level:
    def __init__(self, id: int, task: str, testcases: list[tuple] = []) -> None:
        self.id: int = id
        self.task: str = task
        self.testcases: list[tuple]= testcases
    
    def __repr__(self) -> str:
        return str(self.id) + " -- " + self.task + " -- " + str(len(self.testcases))
    
dbfile = open('levels.aul', 'rb')     
LEVELS: list[Level] = pickle.load(dbfile)
    

final_symbol = image.load(data("final.png")).convert()
start_symbol = image.load(data("start.png"))
tutorial_img = transform.scale(image.load(data("tutorial.png")), SCREEN_SIZE).convert()

click_sound = pygame.mixer.Sound(data("beep.wav"))
weep_sound = pygame.mixer.Sound(data("weep.ogg"))

stretches = [mixer.Sound(data("stretch1.ogg")), mixer.Sound(data("stretch2.ogg")), 
	    	mixer.Sound(data("stretch3.ogg")), mixer.Sound(data("stretch4.ogg")),]


task_text:str ="Task " + str(level_ptr)
top_text:str = LEVELS[level_ptr].task    
bottom_text:str = "..."

edit_active = False

loop = True


class State:
	holds = ""
	def __init__(self, name = "", final :bool = False, pos = (0, 0)):
		self.nexts: dict = {}
		self.final = final
		self.name = name
		self.pos = pos
		

	def __repr__(self):
		return self.__class__.__name__ + ' -- ' + self.name + ' CURR HOLD ->' + self.holds
	
	def __unicode__(self): return "State"

	def propagate(self):
		for path in self.nexts:
			self.nexts[path].propagate()
			

class Path:
	def __init__(self, to:State = None, frm:State = None, character = "", pos:tuple=(0,0)) -> None:
		self.to = to
		self.frm = frm
		self.character = character
		self.name = character
		self.pos = pos
	
	def propagate(self) -> None:
		self.to.holds = self.frm.holds + self.character

class ClickableSprite(sprite.Sprite):
	def __init__(self, image, image2 = None) -> None:
		super().__init__()
		self.image = image
		self.image2 = image2
		self.rect = image.get_rect()
		self.size = self.rect.size

	def move(self, x, y):
		self.rect.move_ip(x, y)

	def anim_scale(self, scale = 1.1):
		#47 x 36
		a = ( self.rect.size[0] * scale )//1
		b = ( self.rect.size[1] * scale )//1
		
		self.image = transform.scale(self.image, (a, b))
	
	def image_swap(self):
		self.image, self.image2 = self.image2, self.image


#  menu
redo = ClickableSprite(image.load(data('redo.png')).convert())
redo.move(1230, 10)

final = ClickableSprite(image.load(data('final_click.png')).convert(), image.load(data('final_click_clicked.png')).convert())
final.move(1230, 70)

start_button = ClickableSprite(image.load(data('start_click.png')).convert(), image.load(data('start_click_clicked.png')).convert())
start_button.move(1230, 130)

run_button = ClickableSprite(image.load(data('run.png')).convert(), image.load(data('run_click.png')).convert())
run_button.move(1230, 190)

exit_button = ClickableSprite(image.load(data('exit.png')).convert(), image.load(data('exit.png')).convert())
exit_button.move(1230, 650)


Menu: list[ClickableSprite] = [redo, final, start_button, run_button, exit_button]
Music: list[str] = ["1.mp3", "2.mp3", "3.mp3"]

def play_songs(file_list):
    random.shuffle(file_list)
    pygame.mixer.music.load(data(file_list[song_number]))
    pygame.mixer.music.play(1)

    for num, song in enumerate(file_list):
        if num == song_number:
            continue # already playing
        pygame.mixer.music.queue(data(song))
	

class StateSprite(sprite.Sprite):
	def __init__(self, state: State):
		super().__init__()
		self.state:State | Path = state
		self.wired_to: list[StateSprite] = []
		self.colour: tuple = WHITE
		self.rect: Rect = Rect((self.state.pos[0] - ST_RAD, self.state.pos[1] - ST_RAD), (ST_RAD*2, ST_RAD*2))
		self.radius = ST_RAD

	
	def draw_state(self, colour = WHITE, colour_b = WHITE, text_x_pos = 10) -> None:
		draw.circle(screen, colour, self.state.pos, self.radius, 2)
		## hitbox # draw.rect(screen, colour_b, self.rect, 2)
		
		for wired_state in self.wired_to: 
			if not wired_state.alive():
				self.wired_to.remove(wired_state)
				continue
			point1 = point_on_line(self.state.pos, wired_state.state.pos, -self.radius)
			point2 = point_on_line(wired_state.state.pos, self.state.pos, -self.radius)
			draw.line(screen, BLUE, point2, point1, 5)
			draw.circle(screen, YELLOW, point2, 10)

		if self.state.final:
			screen.blit(final_symbol, (self.state.pos[0] + 37, self.state.pos[1] - 37))
		text_surface = my_font.render(self.state.name, False, colour_b)
		screen.blit(text_surface, (self.state.pos[0] - text_x_pos, self.state.pos[1] - 20))

class PathSprite(StateSprite):
	def __init__(self, state: Path):
		super().__init__(state)
		self.character = self.state.character
	
	def draw_state(self, colour = WHITE, colour_b = WHITE) -> None:
		draw.circle(screen, colour, self.state.pos, self.radius, 2)
		draw.circle(screen, colour_b, self.state.pos, self.radius - 10, 2)
		## hitbox # draw.rect(screen, colour_b, self.rect, 2)

		for wired_state in self.wired_to: 
			if not wired_state.alive():
				self.wired_to.remove(wired_state)
				continue
			point1 = point_on_line(self.state.pos, wired_state.state.pos, -self.radius)
			point2 = point_on_line(wired_state.state.pos, self.state.pos, -self.radius)
			draw.line(screen, BLUE, point2, point1, 5)
			draw.circle(screen, YELLOW, point2, 10)
			
		text_surface = my_font.render(self.state.character, False, colour_b)
		screen.blit(text_surface, (self.state.pos[0] - 10, self.state.pos[1] - 20))

class NFA(sprite.Group):
	def __init__(self):
		super().__init__()
		self.states:list[StateSprite] = []
		self.pointer = None
		self.start:StateSprite = None

	def __repr__(self):
		s = super().__repr__() + "\n\n"
		for sprite in self.states:
			s += sprite.state.__repr__() + "\n"
		return s
	
	def string_assert(self, s: str):
		if not self.start: return
		pointer:State = self.start.state
		
		for i in s:
			
			if i in pointer.nexts:
				curr_state:StateSprite = pointer.nexts[i].to
				pointer.nexts[i].frm.propagate()
				pointer = curr_state
			else:
				print("cant find")
				return False
		print("currently at --->", pointer)
		for s in NFA_sprite_group.states:
			if type(s) == StateSprite and s.state.final:
				print(s.state.holds)				
		return True if pointer.final else False
	
	def print_nexts(self):
		for f in self.states:
			if type(f) == PathSprite:
				continue
			for g in f.state.nexts:
				print(f.state.name, g, end=" ")
			else:
				print()

	def append_state(self, state):
		self.states.append(state)


selected_sprite :StateSprite | PathSprite = None
selected_sprite_to_drag :StateSprite = None
NFA_sprite_group = NFA()
mouse_was_pressed:bool = False
dragging_mode = False
path_to_edit:PathSprite = None
swapping_final:bool = False
setting_start: bool = False
display_tutorial:bool = False

display_main_menu: bool = True
play_state: StateSprite = StateSprite(State("Play", False, (640, 420)))
how_to_state: StateSprite = StateSprite(State("?", False, (640, 500)))


def main_menu():
	global display_main_menu, display_tutorial
	pos = mouse_obj.get_pos()
	
	if not display_tutorial:
		screen.blit(background, (0,0))
		play_state.draw_state(WHITE, WHITE, 24)
		how_to_state.draw_state(WHITE, YELLOW, 6)
		screen.blit(main_logo, (479, 150))
	else:
		screen.blit(tutorial_img, (0, 0))

	for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				display_tutorial = False
				if play_state.rect.collidepoint(pos):
					display_main_menu = False
				
				if how_to_state.rect.collidepoint(pos):
					display_tutorial = True
		
	if not display_main_menu: play_songs(Music)
	display.update()
	FPS_CLOCK.tick(60)

while loop:
	
	if display_main_menu:
		main_menu()
		time.wait(100)
		continue

	ctrl_pressed = False
	mouse_arr = mouse_obj.get_pressed()
	pos = mouse_obj.get_pos()

	if pygame.key.get_pressed()[pygame.K_LCTRL]:
					ctrl_pressed = True
	
	for event in pygame.event.get():
		
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == MOUSEBUTTONDOWN:
			
			if final.rect.collidepoint(pos):
				final.image_swap()
				swapping_final = not swapping_final

			elif start_button.rect.collidepoint(pos):
				start_button.image_swap()
				setting_start = not setting_start

			elif exit_button.rect.collidepoint(pos):
				NFA_sprite_group.states.clear()
				display_main_menu = True

			elif run_button.rect.collidepoint(pos):

				#running testcases 

				run_button.image_swap()
				total = []
				try:
					curr_lvl: Level = LEVELS[level_ptr]
					total_passed: int = 0
					total_cases: int = len(curr_lvl.testcases)
					res: bool
					s: str
					for i in range(total_cases):

						s, res = curr_lvl.testcases[i]
						f = NFA_sprite_group.string_assert(s)
						run_button.image_swap()
					
						if f == res:
							total_passed += 1
						# bottom_text = "."*(i%4)
					if total_passed != total_cases:
						bottom_text = f"Failed, {total_passed} / {total_cases} testcases passed"
					
					else:
						print("ALL PASSED")
						level_ptr += 1
						if level_ptr == len(levels):
							level_ptr = 0
						bottom_text = "..."
						task_text ="Task " + str(level_ptr)
						top_text = LEVELS[level_ptr].task
				
				except IndexError:
					bottom_text = "Error"
						
		if event.type == KEYDOWN:
			if pygame.key.get_pressed()[pygame.K_DOWN]:
				
				ST_RAD -= 1
			if pygame.key.get_pressed()[pygame.K_UP]:
				
				ST_RAD += 1
			
			if pygame.key.get_pressed()[pygame.K_RIGHT]:
				
				NFA_sprite_group.print_nexts()
				
			try:
			
				if edit_active and path_to_edit:
					prev_char = path_to_edit.state.character
					path_to_edit.state.character = new_char = event.unicode
					path_to_edit.state.frm.nexts.pop(prev_char)
					path_to_edit.state.frm.nexts[new_char] = path_to_edit.state
					path_to_edit = None
					edit_active = None
			
			except AttributeError:
				path_to_edit = None
				edit_active = None
				
		
	if sum(mouse_arr):

		if mouse_arr[0]:
			
			mouse_was_pressed = True
			pos = mouse_obj.get_pos()

			if redo.rect.collidepoint(pos):
				NFA_sprite_group.empty()
				NFA_sprite_group.states.clear()
			
			elif dragging_mode:
				pass
			else:
				state: StateSprite | PathSprite
				for state in NFA_sprite_group:
					
					if state.rect.collidepoint(pos):
						dragging_mode = True
						
						
						#menu stuff
						if swapping_final:
							if type(state) != PathSprite:
								state.state.final = not state.state.final
							continue

						elif setting_start:
							if type(state) != PathSprite:
								NFA_sprite_group.start = state
							continue

						#setting path
						elif ctrl_pressed:
							
							mixer.Sound.play(random.choice(stretches))
							
							if type(selected_sprite) == type(state):
								continue
							
							if selected_sprite:
								if type(selected_sprite) == StateSprite:
									state:PathSprite
									if state.state.character in selected_sprite.state.nexts:
										bottom_text = "That character already has a path"
										print(state.state.character, selected_sprite.state.nexts)
										continue
									state.state.frm = selected_sprite.state
									selected_sprite.state.nexts[state.state.character] = state.state
									selected_sprite.wired_to.append(state)

								elif type(selected_sprite) == PathSprite:
									selected_sprite.state.to = state.state
									selected_sprite.wired_to.append(state)

									# state.state.nexts['a'] = selected_sprite.state
								else:
									print("binding error")
							else:
								selected_sprite = state
							break
						
						if key.get_pressed()[pygame.K_LALT]:
							if type(state.state) == State:
								
								state.state.final = True
						
						elif key.get_pressed()[pygame.K_LEFT]:
							
							if type(state.state) == State:
								print("setting start")
								NFA_sprite_group.start = state
						
						elif key.get_pressed()[pygame.K_BACKSPACE] and type(state) == PathSprite:
							print("edit")
							edit_active = True
							path_to_edit = state

						# state.rect.move_ip(touple_diff(state.state.pos, pos))
						# state.state.pos = pos
						selected_sprite_to_drag = state
						break
				else:
					if not mouse_arr[0]: dragging_mode = False
								
			if swapping_final and not mouse_arr[0]:
				swapping_final = False

			if setting_start and not mouse_arr[0]:
				setting_start = False
			
			if not dragging_mode and not selected_sprite and not selected_sprite_to_drag and not swapping_final and not setting_start:

				# "creating state"
				
				if pos[0] > 1220:
					continue
				mixer.Sound.play(click_sound)
				if key.get_pressed()[pygame.K_LSHIFT]:
					new_state = Path(None, None, 'a', pos)
					new_state_sprite = PathSprite(new_state)
				else:
					new_state = State(f"q{state_count}", False, pos)
					new_state_sprite = StateSprite(new_state)
					NFA_sprite_group.append_state(new_state_sprite)

				if state_count + 1 in SEEN:
					state_count += 1
				
				# new_state = State(f"O", False, pos)
				# new_state_sprite = StateSprite(new_state)

				NFA_sprite_group.add(new_state_sprite)

				state_count += 1
				SEEN.add(state_count)
				dragging_mode = False
				while not pygame.MOUSEBUTTONUP: pass
		

		elif mouse_arr[2]:

			pos = mouse_obj.get_pos()
			for state in NFA_sprite_group:
				if state.rect.collidepoint(pos):
					mixer.Sound.play(weep_sound)
				
					# if selected_sprite:
					# 	try:
					# 		selected_sprite.wired_to.remove(state)
					# 	except ValueError:
					# 		try: 
					# 			state.wired_to.remove(selected_sprite)
					# 		except ValueError: pass

					SEEN.remove(state_count)
					try: 
						if type(state) == PathSprite:
							state.state.frm.nexts.pop(state.state.character)
						NFA_sprite_group.states.remove(state)

					except ValueError: 
						pass
					state_count -= 1
					state.kill()
	
	if selected_sprite_to_drag: 
		selected_sprite_to_drag.rect.move_ip(touple_diff(selected_sprite_to_drag.state.pos, pos))
		selected_sprite_to_drag.state.pos = pos

	if not pygame.key.get_pressed()[pygame.K_LCTRL]:
		selected_sprite = None
	
	#flag cleaning 
	if dragging_mode and not mouse_arr[0]:
		selected_sprite_to_drag = None
		dragging_mode = False
	
	
	NFA_sprite_group.update()
	
	screen.fill((0, 0, 0))
	screen.blit(background, (0,0))
	state:StateSprite
	
	for state in NFA_sprite_group:

		if selected_sprite:

			if path_to_edit == state:
				path_to_edit.draw_state(WHITE, YELLOW)
			
			elif selected_sprite == state: 
				state.draw_state(YELLOW, RED)
				draw.line(screen, YELLOW, touple_diff((0, 0), state.state.pos), pos, 2)
			else: state.draw_state()
		
		else: state.draw_state()
	
	if NFA_sprite_group.start:
		screen.blit(start_symbol, (NFA_sprite_group.start.rect.x + 26, NFA_sprite_group.start.rect.y - 40))
	
	
	task_surf = my_font.render(task_text, False, WHITE)
	top_surf = my_font.render(top_text, False, WHITE)
	bottom_surf = my_font.render(bottom_text, False, WHITE)

	for S in Menu:
		screen.blit(S.image, (S.rect.x, S.rect.y))

	screen.blit(task_surf, (10, 10))
	screen.blit(top_surf, (10, 50))
	screen.blit(bottom_surf, (10, 670))
	# ================================================ #
	display.update()
	
	if not mixer.music.get_busy(): play_songs(Music)

	FPS_CLOCK.tick(60)

pygame.quit()
# quit()
# A, B, C = StateSprite(State("1", False)), StateSprite(State("2", False)), StateSprite(State("3", True))


# A.state.nexts['a'] = Path(B.state, A.state, 'a')
# B.state.nexts['a'] = Path(C.state, B.state, 'a')

# for f in [A, B, C]:
# 	NFA_sprite_group.states.append(f)

# print(NFA_sprite_group.string_assert('a'), NFA_sprite_group.string_assert('aa'))
# print(C)