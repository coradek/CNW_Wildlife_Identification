# Species Identification: Image Classification in Wildlife Remote Camera Studies


## __Business Understanding:__
Conservation Northwest (CNW) is a non-profit land conservation organization dedicated to protecting and conserving wild lands from the Washington Coast to the BC Rockies. One of CNW's ongoing efforts is the Citizen Wildlife Monitoring Project (CWMP), organizing citizen-scientist volunteers to monitor and document wildlife using remote cameras where state and federal agencies don’t have the resources to go.
The CWMP is now in its tenth year. The project depends largely on volunteers not only to maintain and monitor the cameras, but also to manually sort the thousands of resulting photos, removing false triggers (any photo with no animal), identifying species, and grouping photos into events.
Image recognition, and machine learning technologies provide a significant opportunity for streamlining volunteer efforts and improving consistency of the resultant data. Data from 2015 and 2014 has already been categorized by hand, and is available for use in model training. Images from seven previous years (2007 - 2013) and from the current field season (2016) have yet to be analyzed, so an automated system would be of immediate benefit to the organization.
The ideal system would automate three tasks - remove of false triggers, group photos into ‘events’ (by time and species), and finally identify species present in the photo. This project will start with the identification of species because false triggers have already been removed from the initial dataset manually, and event classification data is not included in the initial dataset.

<br>

## __The Data__
An extensive set of photographs is available for analysis: ~120000 images from 2015 alone. Verified species information is included in the metadata associated with each image, making Species Identification a convenient starting point for this project.
The primary information used for prediction will be the photographs themselves. The cameras used in the wildlife monitoring project take three photos consecutively each time they are triggered. Therefore timestamps and adjacent photos (or their predicted classifications) may also provide useful information to a machine learning model.
False triggers have already been removed from the data set, and retrieving event classification information has proven technically challenging. These directions are better suited to a longer project and may require minor changes to the CWMP protocol as a whole in order to make modeling more feasible.
Data preparation will require some effort. Directory naming across the 2015 image set is somewhat inconsistent and there are occasional duplicate photos either in differently named directories, or in the same directory with different names (e.g. 'img401' and 'img401 (2)'). Metadata will also need to be scraped and formatted into an appropriate data structure.

<br>

## __Modeling__
As of this writing several strategies for modeling are under consideration:
In the first phase of modeling, gradient boost or random forest will be applied to features extracted from a pre-trained convolutional neural network (CNN) - Graphlab image_net_model, TensorFlow Inception-v3, or similar. An alternate strategy would be to experiment with Facebook's SharpMask module, and attempt to identify where in the photos the animals are located. This information could then be used for further classification.
As a second phase the images could be used to train a neural network from scratch. While this would certainly be a useful learning exercise, it is unlikely that any model train on such a small set of photos would be able to perform as well as more general pre-trained models. This phase would primarily be aimed at providing context for either of the initial sections.
Data processing/preparation and extracting features from an appropriate pre-trained model are the two greatest challenges I foresee. Thanks to the good out-of-box performance of gradient boosting and random forest I expect that producing a reasonable proof of concept model should not be unreasonably difficult once data processing and feature extraction are complete.
I hope to be able to run gradient boost on extracted features and develop a (very) simple web app within the allotted timeframe. Given good progress I plan to spend any additional time on fine tuning the initial model, looking into feature engineering and training a new CNN from scratch.
In addition to a pre-trained CNN, my project will use Tamás Gulácsi's IPTCInfo python module.

<br>

## __Evaluation__
Photo sets that have already been processed will be used for test and training sets. Ideally the project will result in an interface that would provide prediction information to volunteers for verification. Such an interface would allow the model to be tested on unprocessed data for further verification over time.

<br>

## __Deployment__
The initial minimum viable product will include the model itself as well as web application or similar interface that takes in a photo and provides a prediction which can then be verified manually.
A presentation on project progress will also be produced to provide insight into the specific challenges of this project and aid in paving the way for future research and development of features immediately valuable to the organization.
