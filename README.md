# Species Identification: Image Classification in Wildlife Remote Camera Studies


## __Business Understanding:__
Conservation Northwest (CNW) is a non-profit land conservation organization dedicated to protecting and conserving wild lands from the Washington Coast to the BC Rockies. One of CNW's ongoing efforts is the Citizen Wildlife Monitoring Project (CWMP), organizing citizen-scientist volunteers to monitor and document wildlife using remote cameras where state and federal agencies don’t have the resources to go.
The CWMP is now in its tenth year. The project depends largely on volunteers not only to maintain and monitor the cameras, but also to manually sort the thousands of resulting photos, removing false triggers (any photo with no animal), identifying species, and grouping photos into events.
Image recognition, and machine learning technologies provide a significant opportunity for streamlining volunteer efforts and improving consistency of the resultant data. Data from 2015 and 2014 has already been categorized by hand, and is available for use in model training. Images from seven previous years (2007 - 2013) and from the current field season (2016) have yet to be analyzed, so an automated system would be of immediate benefit to the organization.
The ideal system would automate three tasks - remove of false triggers, group photos into ‘events’ (by time and species), and finally identify species present in the photo. This project starts with the identification of species because false triggers have already been removed from the initial dataset manually, and event classification data is not included in the initial dataset.

<br>

## __The Data__

<img src="pic_mountain.jpg" alt="Mountain View" style="width:304px;height:228px;">

An extensive set of photographs is available for analysis: ~120000 images from 2015 alone. Verified species information is included in the metadata associated with each image, making Species Identification a convenient starting point for this project.
The primary information used for prediction is the photographs themselves. The cameras used in the wildlife monitoring project take three photos consecutively each time they are triggered. Therefore timestamps and adjacent photos (or their predicted classifications) may also provide useful information to a machine learning model.
False triggers have already been removed from the data set, and retrieving event classification information has proven technically challenging. These directions are better suited to a longer project and may require minor changes to the CWMP protocol as a whole in order to make modeling more feasible.
Data preparation required some effort. Directory naming across the 2015 image set is somewhat inconsistent and there are occasional duplicate photos either in differently named directories, or in the same directory with different names (e.g. 'img401' and 'img401 (2)'). Metadata also needed to be separated from the images and formatted into an appropriate data structure.

<br>

## __Modeling__
In the current phase of modeling, a Support Vector Machine (SVM) is applied to features extracted from TensorFlow's Inception-v3, a pre-trained convolutional neural network. For the first phase, animal species have been grouped into five categories: Canine (coyote, wolf, fox, and domestic dog), Feline (bobcat, lynx, cougar), Ungulate (deer, elk, moose), Small (squirrels, birds, mice, weasles), and Other (humans, bear, skunk, wolverine, marmot).

In upcoming stages I plan to use motion detection (OpenCV or similar) across consecutive images to help identify critical areas of the photographs and help account for new backgrounds. This will hopefully allow the model to correctly predict species even for camera locations not seen during training.

An alternate strategy under consideration would be to experiment with Facebook's SharpMask module, and attempt to identify where in the photos the animals are located. This information could then be used for further classification.

In addition to TensorFlow and scikit-learn, my project uses Tamás Gulácsi's IPTCInfo python module for metadata extraction.

<br>

## __Evaluation__
Photo sets that have already been processed will be used for test and training sets. Ideally the project will result in an interface that would provide prediction information to volunteers for verification. Such an interface would allow the model to be tested on unprocessed data for further verification over time.

<br>

## __Deployment__
The initial minimum viable product will include the model itself as well as web application or similar interface that takes in a photo and provides a prediction which can then be verified manually.
A presentation on project progress will also be produced to provide insight into the specific challenges of this project and aid in paving the way for future research and development of features immediately valuable to the organization.
