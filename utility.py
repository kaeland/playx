#!/usr/bin/env python3
"""A utility module for misc operations."""

import os
import subprocess
import time
import pyglet


def exe(command):
    """Execute the command externally."""
    command = command.strip()
    c = command.split()
    output, error = subprocess.Popen(c,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE).communicate()
    output = output.decode('utf-8').strip()
    error = error.decode('utf-8').strip()
    return (output, error)


def direct_to_play(url, play_type):
    """Direct the song to be played according to the play_type."""
    if play_type == 'local':
        # Pass to play with pyglet
        run_pyglet(url)
    else:
        # Else run with mpd to stream
        run_mpd(url)


def run_mpd(url):
    """Run the song in mpd."""
    # Check if mpd is on or not
    if not is_on():
        cm = 'mpd'
        exe(cm)
    # Pause mpd
    cm1 = 'mpc pause'
    exe(cm1)
    # Clear the playlist
    cm2 = 'mpc clear'
    exe(cm2)
    # Insert the song
    cm3 = 'mpc insert {}'.format(url)
    exe(cm3)
    # Play the song
    cm4 = 'mpc play'
    exe(cm4)


def run_pyglet(path):
    """Run pyglet to play the song."""
    current_dir = os.getcwd()
    try:
        # Before doing the following move to the dir
        dirname = os.path.dirname(path)
        song_name = os.path.basename(path)
        print(song_name)
        os.chdir(dirname)
        song = pyglet.resource.media(song_name)
        song.play()

        # Before playing check if mpd is running
        if is_on():
            cm = 'mpd --kill'
            exe(cm)
        # Now simply start pyglet
        pyglet.app.run()

        # Move to the prev dir
        os.chdir(current_dir)
        return True
    except KeyboardInterrupt:
        os.chdir(current_dir)


def toggle():
    """Toggle mpd."""
    cm = 'mpc toggle'
    os.system(cm)


def get_status():
    """Return the status of mpd."""
    status, error = exe('mpc status')

    if 'playing' in status:
        return 'Playing'
    elif 'paused' in status:
        return 'Paused'
    else:
        return False


def is_on():
    """Check if mpc is on."""
    status = get_status()
    if status == 'Playing' or status == 'Paused':
        return True
    else:
        return False


if __name__ == '__main__':
    print(is_on())
