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

share your code with detailed instructions. We would be testing your model on training dataset (dataset we have shared with you) and test dataset (dataset we haven't shared with you)

share a note on the approach and methodology that you have used

4. Success criteria: % accuracy on the training and test datasets

5. Ideas on improving model performance. 
-  You can use both free and paid APIs such as AWS textract, AWS Rekognition, Google vision etc. Most paid APIs are free for the first 1000-5000 images.

Using logics to detect numbers. e.g. VIN numbers have 17 digit alphanumeric format  , dates have a fixed format, license plate numbers have 10 digit alphanumeric format

- Image enhancement techniques such as grayscale, contrast etc

- Be as creative as possible !
