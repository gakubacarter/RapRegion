# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import lyricsgenius as genius

southlist = open('southlist.txt')

for line in southlist:
    api = genius.Genius('ekJs8RoT6EPbhhywrEFY0wRiE86HV2G0jyG9JSVymn2uAeu22tToSAsgfs7hibFL')
    artist = api.search_artist(line, max_songs=50)
    artist.save_lyrics() #writes lyrics to a json named after the artist

southlist.close()