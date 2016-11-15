# __Contents__
_Connect to EC2_
_Photo to cloud process_
_Expected Workflow_
_Looping Over Files in Directory_
_Setting up EC2_
_Picture MetaData_
_Miles' Suggested Process_

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
