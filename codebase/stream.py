#straming function

import subprocess

mpv_executable = "mpv"

def play_mpv(data):
    #data -> list containign dictionary 
    args = [mpv_executable]
    x = data[0]
    streaming_link = x["stream_url"]
    #print(streaming_link)
    for key,value in x.items():
        if key == "audio":
            args.append(f"--audio-file={value}")
        if key == "referrer":
            args.append(f"--referrer={value}")
        if key=="name":
            args.append(f"--force-media-title={value}")
            
    args.append(f'{streaming_link}')


    mpv = subprocess.Popen(args)
    mpv.wait()
    mpv.kill()
    