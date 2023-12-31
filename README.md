# FerrmoNote
![Python](https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white) ![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white) ![Version](https://img.shields.io/static/v1?label=Version&message=0.1.5&labelColor=212121&color=ff422e&style=for-the-badge) ![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/ChilledFerrum/FerrmoNote)
<a href="https://circleci.com/gh/badges/shields/tree/master">
    <img src="https://img.shields.io/circleci/project/github/badges/shields/master" alt="build status"></a>
<a href="https://circleci.com/gh/badges/daily-tests">

> Improve your quality of life by storing important information, goals, to-do items, and more.

<p align="center">
    <img src="https://github.com/ChilledFerrum/FerrmoNote/blob/32cca807a42b3ba3f551c9a9a0f1300f78ee7dc5/assets/FerrmoNote_banner.png"/>
</p>

## This application is currently still in development
If you'd like to contribute to this project, please feel free to create an issue for the better development of this project. <br/>
It will support dynamic note management for the user to manage their information based on their needs. <br/>
This project is currently very early in development <br/>
<img src="FerrmoNote_intro.gif" style="display: block; margin: auto; width: 650px; height: 650px;"> <br/>


### Installation...
```commandline
$ conda create -n FerrmoNote python==3.10

$ conda activate FerrmoNote

$ pip install -r requirements.txt
```

### Running...
```commandline
$ python Ferrmo.py
```

### Troubleshoot for Linux <br/>
```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
```
In the case of the above error, a possible fix is to install any necessary xcb plugins for your device.
```
sudo apt install libxcb-*
```
