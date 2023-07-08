# TouriscoBackend

## 3rd version :

1. Tickets Model Apis

## 4th version :

1. Reviews Model Apis

2. Image Model Apis

3. Relation Structure fix

## 5th version :

1. Type Model Apis

2. extend access token lifetime

3. add category_type field to landmark

4. fix image load issue

5. Dialogflow chatbot agent with static simple responses (no entities)

## 6th version :

1. add active user api

2. add extra apis

# 7th version :

1. TourPackage Model Apis except create api.
2. fix issues and bugs

## 7.1 version:

1. make all categories create admin apis

### 7.1.1 version :

1. fix image issue in tourism category create api

### 7.1.2 version :

1. fix image load issue again

### 7.1.3 version :

1. edit landmark model char length

### 7.1.4 version :

1. edit landmark serializer return its image objects
2. edit landmark serializer return its reviews objects
3. edit review serializer return its image objects

### 7.1.5 version :

1. return user object in review object

### 7.2 version :

1. make review api with images
2. add coordinates to landmark Model
3. add Many to Many relation between landmark and tourism category
4. add eternel feature to event Model

#### 7.2.1 version :

1. return governorates sorted by population

#### 7.2.2 version :

1. serve media in production when debug is false

### 7.3 version :

1. add create package algorithm based on budget

#### 7.3.1 version :

1. update packages viewset for creating new package
2. sort landmarks by latest

##### 7.3.1.1 version :

1. change start and end datetime to date in create package

#### 7.3.2 version :

1. fix create package bugs

#### 7.3.3 version :

1. add num_of_views for landmarks and tour packages
2. add recommend landmarks in tourism category
3. add define of tourism category

##### 7.3.3.1 version :

1. area and height not required

##### 7.4 version :

1. modify chatbot algorithm
2. add remommandation for packages , define landmarks
