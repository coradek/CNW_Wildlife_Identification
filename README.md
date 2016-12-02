# Species Identification: Image Classification in Wildlife Remote Camera Studies

This project aims to classify wildlife in images from the Conservation Northwest Wildlife Monitoring Project. The classification model will generate a vector of image features through a pre-trained convolutional neural network and then classify these vectors with a support vector machine.

## __Project Context:__
Conservation Northwest (CNW) is a non-profit land conservation organization dedicated to protecting and conserving wild lands from the Washington Coast to the BC Rockies. One of CNW's ongoing efforts is the Citizen Wildlife Monitoring Project (CWMP), organizing citizen-scientist volunteers to monitor and document wildlife using remote cameras where state and federal agencies do not have the resources to go.
The CWMP is now in its tenth year. The project depends largely on volunteers, not only to maintain and monitor the cameras, but also to manually sort and categorize hundreds of thousands of resulting photos - many of which do not contain any animal and must be removed from the database.
Image recognition, and machine learning technologies provide a significant opportunity for streamlining volunteer efforts and improving the consistency of the resultant data. Images from 2015 and 2014 have already been categorized by hand, and are available for use in model training. Images from seven previous years (2007 - 2013) and from the current field season (2016) have yet to be analyzed, so an automated system would be of immediate benefit to the organization.
The ideal system will automate three tasks
- Remove of 'False Triggers' - images with no animal.
- Group photos into ‘Events' - multiple images of the same animal around the same time
- Identify which species are present in each photo.

This project begins with the identification of species because false triggers have already been removed from the initial dataset manually, and event classification data is not included in the initial dataset.

<br>

## __The Data__

An extensive set of photographs is available for analysis: ~120000 images from 2015 alone. Verified species information is included in the metadata associated with each image, making Species Identification a convenient starting point for this project.
The primary information used for prediction is the photographs themselves. The cameras used in the wildlife monitoring project take three photos consecutively each time they are triggered. Therefore timestamps and adjacent photos (or their predicted classifications) may also provide useful information to a machine learning model.
False triggers have already been removed from the data set, and retrieving event classification information has proven technically challenging. These directions are better suited to a longer project and may require minor changes to the CWMP protocol in order to make modeling more feasible.
Data preparation required some effort. Directory naming across the 2015 image set is somewhat inconsistent and there are occasional duplicate photos either in differently named directories, or in the same directory with different names (e.g. 'img401' and 'img401 (2)'). Metadata also needed to be separated from the images and formatted into an appropriate data structure.

<br>

## __Modeling__
In the current phase of modeling, a Support Vector Machine (SVM) is applied to features extracted from TensorFlow's pre-trained convolutional neural network, Inception-v3. For the first phase, animal species have been grouped into five categories:
- Canine (coyote, wolf, and domestic dog)
- Feline (bobcat, lynx, cougar)
- Ungulate (deer, elk, moose)
- Small (squirrels, birds, mice, weasels)
- Other (humans, bear, skunk, wolverine, marmot).

Snow-shoe Hares were a very unbalanced group, and posed a particular challenge to the model (being a small white animal on a snowy background) and so were removed from the training set.

In upcoming stages I plan to use motion detection (OpenCV or similar) across consecutive images to help identify critical areas of the photographs and help account for new backgrounds. This will hopefully allow the model to correctly predict species even for camera locations not seen during training.

An alternate strategy under consideration would be to experiment with Facebook's SharpMask module, and attempt to identify where in the photos the animals are located. This information could then be used for further classification.

In addition to TensorFlow and scikit-learn, my project uses Tamás Gulácsi's IPTCInfo python module for metadata extraction.

<br>

## __Results and Evaluation__

The current model was trained on a subset of the data - approximately 4000 photos. To evaluate this model I split the data subset randomly into test and training groups. It is important to note that these photos where all from one of three training locations. As a result animals are often seen in similar locations and at similar times of day.

The model achieved 85-98% in-class accuracy for each of the five categories on the test portion of the subset. Only the 'small' category fell below 94% and this lower rating may be at least partially explained by class imbalance. The 'Small' category was roughly one fourth the size of the other groups.

Results on images from other locations were generally weak. However, on a small sample (~150 photos) of very clear photos found online, the model had accuracy of 55-75% per category.

I expect that taking backgrounds into account through motion capture will help significantly. I also plan to test the model on test and training groups at the same location separated solely by time.

<br>

## __Deployment__

Checkout the Web App at [evanadkins.tech](www.evanadkins.tech)! This app allows the user to upload a photo and receive a prediction from the model. Because your photos are likely not from the same location, the results are often entertaining!

The eventual plan is to build this system into an app that will allow volunteers with CWMP to upload and entire directory and receive predictions. Predictions could then be used to flag false triggers, and suggest event grouping.
