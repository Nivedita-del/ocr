# ocr
A text detection model for reading RCs

An excel  showing what was the text output for each image.

should be able to capture the following fields on the RC: 
- License plate number or Regn number
- VIN number or Chassis number (typically 17 digit long)
- Name
- Engine number
- Registration date
- Mfg. date


Success criteria: % accuracy on the training and test datasets

Ideas on improving model performance. 
-  You can use both free and paid APIs such as AWS textract, AWS Rekognition, Google vision etc. Most paid APIs are free for the first 1000-5000 images.

Using logics to detect numbers. e.g. VIN numbers have 17 digit alphanumeric format  , dates have a fixed format, license plate numbers have 10 digit alphanumeric format

- Image enhancement techniques such as grayscale, contrast etc

- Be as creative as possible !
