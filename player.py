from tkinter import *
import pygame
from tkinter import filedialog
import re

pygame.mixer.init(frequency = 44100, size =16, channels = 1, buffer = 512)
root = Tk()
root.title('MP3 Player')
#root.iconbitmap('')
root.geometry('500x300')

playing_status = 1
song_list  = []

#Regex expression for opening a file from any directory
regex_path = re.compile(r"^([A-Za-z]:|[A-Za-z0-9_-]+(\.[A-Za-z0-9_-]+)*)((\/[A-Za-z0-9_\s.-]+)+)$")
regex_file = re.compile(r"(\/[A-Za-z0-9_\s.-]+)$")

def add_song():
	global regex_path
	global regex_file
	global path_breaker
	songs = filedialog.askopenfilenames(initialdir='audio/', title='Choose a song', filetype=(('mp3 files', '*mp3'),))
	
	for song in songs:
		match1 = regex_path.fullmatch(song)
		match2 = regex_file.search(song)
		num = match1.group().find(f'{match2.group()}')
		
		path_breaker = match1.group()[:num]
		song = song.replace(f'{path_breaker}', '')
		song = song.replace(f'/', '')
		song = song.replace('.mp3', '')
		playlist.insert(END, song)

def pause():
	global playing_status
	if playing_status:
		pygame.mixer.music.pause()
		playing_status = 0
	else:
		pygame.mixer.music.unpause()
		playing_status = 1

def play():
	global path_breaker
	song = playlist.get(ACTIVE)
	song = f'{path_breaker}/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	
def stop():
	pygame.mixer.music.stop()

def nextSong():
	global path_breaker
	currentsong = playlist.curselection()
	currentsong = currentsong[0] + 1
	song = playlist.get(currentsong)
	song = f'{path_breaker}/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	#Clear and Move the selection bar
	playlist.selection_clear(0, END)
	playlist.activate(currentsong)
	playlist.selection_set(currentsong, last=None)

def previousSong():
	global path_breaker
	currentsong = playlist.curselection()
	currentsong = currentsong[0] - 1
	song = playlist.get(currentsong)
	song = f'{path_breaker}/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	#Clear and Move the selection bar
	playlist.selection_clear(0, END)
	playlist.activate(currentsong)
	playlist.selection_set(currentsong, last=None)

def delete_song():
	playlist.delete(ANCHOR)
	pygame.mixer.music.stop()		

def delete_all_songs():
	playlist.delete(0, END)
	pygame.mixer.music.stop()

#Playlist
playlist = Listbox(root, bg='black', fg='green', width = 60, selectbackground='grey', selectforeground='black')
playlist.pack(pady=20)

#CreatePlayerButtons
play_btn = PhotoImage(file='icons/play.png')
pause_btn = PhotoImage(file='icons/pause.png')
stop_btn = PhotoImage(file='icons/stop.png')
next_btn = PhotoImage(file='icons/next.png')
back_btn = PhotoImage(file='icons/back.png')

#PlayerButtonFrame
buttons_frame = Frame(root)
buttons_frame.pack()

#CreateButtons
back_button = Button(buttons_frame,image=back_btn,borderwidth=0, command = previousSong)
play_button = Button(buttons_frame,image=play_btn,borderwidth=0, command = play)
pause_button = Button(buttons_frame,image=pause_btn,borderwidth=0, command = pause)
stop_button = Button(buttons_frame,image=stop_btn,borderwidth=0, command = stop)
next_button = Button(buttons_frame,image=next_btn,borderwidth=0, command = nextSong)


back_button.grid(row=0, column=1, padx=10)
pause_button.grid(row=0, column=2, padx=10)
play_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)
next_button.grid(row=0, column=5, padx=10)

#Menu
player_menu = Menu(root)
root.config(menu = player_menu)

song_menu = Menu(player_menu)
song_menu.add_command(label='Add songs', command=add_song)
player_menu.add_cascade(label='File', menu = song_menu)

#Delete Song menu
remove_song = Menu(player_menu)
player_menu.add_cascade(label='Remove Song', menu = remove_song)
remove_song.add_command(label='Delete Song from playlist', command = delete_song)
remove_song.add_command(label='Delete all songs from playlist', command = delete_all_songs)

root.mainloop()