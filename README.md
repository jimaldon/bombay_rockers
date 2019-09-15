<img src="/docs/logo.png" width="200">

 # Climate Change AI Hackathon
 
 ## How to run?
 
 * Install python deps using `pip install -r requirements.txt`.
 * Download `train.zip` and `test.zip` from `bit.ly/2mgYsqh`, extract into a folder named `data`.
 * Run `create_tfrecords.py` to create training tfrecord. Run `slim/train_pc.sh` to train model.
 * Run `slim/run_on_test.sh` to generate predictions on test set.
 * The flask app for monitoring is run by `python3 app/app.py`.
 * `slim/export_frozen_graph.sh` and `slim/export_inference_graph.sh` to be used for converting saved TF models to frozen graph and `tflite_converter.py` to convert to TFLite.
 * Android app code inside `android`.
 
 
