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
