# __Contents__
_Connect to EC2_
_Expected Workflow_
_Looping Over Files in Directory_
_Setting up EC2_
_Picture MetaData_
_Miles' Suggested Process_

<br>

# __Connect to EC2__
ssh cnw
(simple, ain't it)

<br>

# __Expected Workflow__

setup.py --> see doc_str
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
