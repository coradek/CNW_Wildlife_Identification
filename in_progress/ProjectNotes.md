# __Contents__
_Connect to EC2_
_Photo to cloud process_
_Expected Workflow_
_Looping Over Files in Directory_
_Setting up EC2_
_Picture MetaData_
_Miles' Suggested Process_
_Web app_
_opencv_

<br>
__TIDBITS:__

filename = os.path.basename('/Volumes/Seagate Backup Plus Drive/CNWPhotos')
filename --> CNWPhotos

merge folders:
```
rsync -av /source/ /destination/
(after checking)
rm -rf /source/
```

<br>
# __Install Tensorflow__

conda install tensorflow
`conda install -c conda-forge tensorflow`

cd to imagenet directory
`cd anaconda/lib/python2.7/site-packages/tensorflow/models/image/imagenet`

run py command
`python classify_image.py --model_dir <desired model location>/imagenet`
`python classify_image.py --model_dir ~/coradek/Galvanize_DSI/CNW_Wildlife_Identification/imagenet`


<br>
# __Connect to EC2__

* describe ssh setup
`# cnw ec2 instance
Host <EC2 name>
  HostName ec2-35-163-162-65.us-west-2.compute.amazonaws.com
  User ubuntu
  IdentityFile ~/.ssh/demo.pem`


ssh <EC2 name>
(simple, ain't it)

<br>

# __Photo to cloud process__

use tmux to restart interupted tasks
`$ tmux`
* to see tmux sessions:
`tmux ls`
* to reattach to tmux sessions
`tmux attach`

set up EC2

zip photos (without parent directory):
`tar czvf <name of zipped file>.tar.gz -C dir/to/be/zipped .`

create dir for split parts (there will be many)
`mkdir <split_temp>`

split zipped file and put parts in new dir
* cd to <split_temp> then:
`split -b 512m path/to/zipped/file "<prefix for parts>"`

copy all parts to EC2 instance:
* cd into parts folder <split_temp>
`scp * <ssh name>:<destination folder>`

unsplit the pieces
* create new dir for unsplit file (just to be safe)
* cd in and use cat to reassemble the pieces
`cat ../cnw_part_* > cnwphotos.tar.gz`

unzip the photos
`tar -xvzf <zipped_file>.tar.gz`

### If interupted only the uncopied parts need to be copied
BETTER than regex:
+ move successfully copied files to different dir
+ repeat `scp * <ssh name>:<destination folder>``

Regex alternative (incomplete - does not take second letter into account)
```
scp `find . -regex ".*/cnw_part_[e-z].*"` <ssh name>:<destination folder>
```

CONSIDER: write script to automate
+ when file copied successfully, move it to 'transferred' folder

<br>

# __Expected Workflow__

data_pipline.py --> see doc_str
provide photo source
creates databases (raw-json, clean-csv, final)
#### edit to only create essential databases once determined

#### create json database:
  metadata_handler\
      .build_json_database('parent/directory')
  __outputs .json file__

#### create clean pandas df:
  clean_db.process_data('database.json')
  __outputs tidied pandas df (form? csv?)__




<br>

# __Looping Over Files in Directory__

To find all the filenames use os.listdir().
Then you loop over the filenames. Like so:

```python
import os
for filename in os.listdir('dirname'):
     callthecommandhere(blablahbla, filename, foo)
```
```python
if not os.path.isfile(filename):
```

<br>

# __Setting up EC2__


set up EC2 through aws web gui:

* Key: Name, Value: <desired name - used to ssh into the EC2 instance>

in iterm:
```
$ cd ~/.ssh
$ atom config
```
add:
```
# description (e.g. cnw )
Host <Value from above>
  HostName <from aws gui>
  User (e.g. ubuntu)
  IdentityFile (e.g. ~/.ssh/demo.pem )
```
go to anaconda website:
* copy link from download button

back in iterm
```
ssh <name>
wget (paste link)
bash . . . (see conda website)
```

<br>

# __Picture MetaData__
_IPTC info_

pip install IPTCinfo --> read photo metadata: tags, keywords etc.

```python
from iptcinfo import IPTCInfo
info = IPTCInfo('image filename goes here')

In [8]: print info
charset: None
{'date created': '20150530', 'copyright notice': 'Conservation Northwest', 'sub-location': 'Blackjack Ridge-2015-1', 'by-line': 'Cathy Clark', 'supplemental category': [], 'time created': '114952', 'contact': [], 'keywords': ['Camera Check'], 'object name': 'wolverine', 'caption/abstract': 'M2E32L107-108R390B311'}


In [14]: print info.data
{116: 'Conservation Northwest', 5: 'wolverine', 92: 'Blackjack Ridge-2015-1', 80: 'Cathy Clark', 20: [], 118: [], 55: '20150530', 120: 'M2E32L107-108R390B311', 25: ['Camera Check'], 60: '114952'}

In [15]: type(info.data)
Out[15]: iptcinfo.IPTCData

In [16]: data_dict = dict(info.data)
# keys are field numbers
# see either IPTCData or IPTCInfo.c_datasets

```

```
from iptcinfo import c_datasets, c_datasets_r
Those two dictionary objects will tell you what's available
```

```
info.exportSQL ?!
```

<br>

# __Miles' Suggested Process__

```
* Start with graph lab type neural net or similar
* take features from deep level on neural net
* apply random forrest, gradient boost or similar
    on these deep features

("far beyond techniques being used a few years ago")
```

<br>

# __Web app__

to change background color
search for #556D89 in grayscale.min.css
and replace all

FOR EC2

* install tensorflow
`conda install -c conda-forge tensorflow`
* fix matplotlib
  `conda install PyQt=4`
  * alter matplotlib import: add the following lines above the import statement for matplotlib.pyplot
  ```
  import matplotlib as mpl
  mpl.use("Agg")
  ```

Setup DNS (www.evanadkins.tech)
https://www.hover.com/domain/evanadkins.tech/dns
change @ record to my EC2 elastic IP
make new record www with my EC2 elastic IP



bash Anaconda2-4.2.0-Linux-x86_64.sh
vim .bashrc

sudo apt-get update
sudo apt-get install nginx
sudo apt-get install uwsgi

git clone https://github.com/coradek/CNW_Wildlife_Identification
conda install -c conda-forge tensorflow
conda install PyQt=4

cd /etc/nginx/sites-available
sudo ln -s /etc/nginx/sites-available/app

cd /etc/uwsgi/apps-enabled
ls
sudo vim app.ini

tail /var/log/nginx/access.log
sudo vim /etc/nginx/sites-enabled/app
sudo vim /etc/nginx/nginx.conf
sudo service nginx restart


sudo less /var/log/uwsgi/app/app.log
sudo less /var/log/uwsgi/app/app.log.1
sudo service uwsgi restart

# __opencv__

install:
`conda install -c menpo opencv=2.4.11`

extra image utilities package:
(http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/)
`pip install imutils`
