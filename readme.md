## Python tool that scrapes animixplay [still work in progress]

This is a python tool that scrapes animixplay links directly play it in mpv video player

***

## Requirements
1. **python>=3.6**

2. **mpv(should be in ``PATH`` for windows)**

***
## Installation

```pip install -r requirements.txt```

In the file 

```$HOME/local/lib/python3.10/site-packages/prompt_toolkit/styles/from_dict.py```

Change the line 8

```from collections import Mapping```

to

```from collections.abc import Mapping```
***

## Usage

``python app.py``
***

## Additional Notes
This project is highly inspired from ``ani-cli`` and ``animdl`` . If you like this project please star it. ``Issues`` are welcome too

# Todo List

1. **Clean up the code**
2. **Fix UI**
3. **Add Downloader**
4. **Play next episode**
5. **Backup links if provide fails**
6. **Continue watch feature**




