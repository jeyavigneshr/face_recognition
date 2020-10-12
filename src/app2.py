import tkinter as tk
import argparse

from src.training_data_collection.get_faces_from_camera2 import TrainingDataCollector
from src.face_embedding.faces_embedding2 import GenerateFaceEmbedding
from src.training.train_softmax2 import TrainFaceRecogModel
from src.predictor.facePredictor2 import FacePredictor

class RegistrationModule:
    def __init__(self):
        print('inside init')
        self.window=tk.Tk()
        self.window.title("Face Recognition")
        self.window.resizable(0, 0)

        window_height = 600
        window_width = 880

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))

        self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        #self.window.geometry('880x600')
        self.window.configure(background='#ffffff')
        #self.window.attributes('-fullscreen', True)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        header = tk.Label(self.window, text="Face Recognition                              By-Vishwa Bhushan", width=70, height=2, fg="white",
                          bg="#7d2e53",
                          font=('times', 18, 'bold'))
        header.place(x=0, y=0)
        userName = tk.Label(self.window, text="Enter Name:", width=10, fg="white", bg="#7d2e53", height=2,
                           font=('times', 15))
        userName.place(x=80, y=140)

        self.userNameTxt = tk.Entry(self.window, width=20, bg="white", fg="black", font=('times', 15, ' bold '))
        self.userNameTxt.place(x=205, y=140)

        lbl3 = tk.Label(self.window, text="Notification : ", width=15, fg="white", bg="#363e75", height=2,
                        font=('times', 15))
        self.message = tk.Label(self.window, text="", bg="#dcdce7", fg="black", width=30, height=1,
                                activebackground="#e47911", font=('times', 15))
        self.message.place(x=220, y=220)
        lbl3.place(x=80, y=260)

        takeImg = tk.Button(self.window, text="Take Images", command=self.collectUserImageForRegistration,fg="white",
                            bg="#363e75", width=15,
                            height=2,
                            activebackground="#118ce1", font=('times', 15, ' bold '))
        takeImg.place(x=80, y=350)

        trainImg = tk.Button(self.window, text="Train Images",command=self.trainModel, fg="white", bg="#363e75",
                             width=15,
                             height=2,
                             activebackground="#118ce1", font=('times', 15, ' bold '))
        trainImg.place(x=350, y=350)

        predictImg = tk.Button(self.window, text="Predict",command=self.makePrediction, fg="white", bg="#363e75",
                               width=15,
                               height=2,
                               activebackground="#118ce1", font=('times', 15, ' bold '))
        predictImg.place(x=600, y=350)

        quitWindow = tk.Button(self.window, text="Close Window", fg="white", bg="#363e75", width=10,
                               height=2,
                               activebackground="#118ce1", font=('times', 15, 'bold'))
        quitWindow.place(x=650, y=510)
        self.window.mainloop()

    def collectUserImageForRegistration(self):

        name = (self.userNameTxt.get())
        ap = argparse.ArgumentParser()

        ap.add_argument("--faces", default=50,
                        help="Number of faces that camera will get")
        ap.add_argument("--output", default="../datasets/train/" + name,
                        help="Path to faces output")

        args = vars(ap.parse_args())

        trnngDataCollctrObj = TrainingDataCollector(args)
        trnngDataCollctrObj.collectImagesFromCamera()

        notifctn = "We have collected " + str(args["faces"]) + " images for training."
        self.message.configure(text=notifctn)

    def getFaceEmbedding(self):

        ap = argparse.ArgumentParser()

        ap.add_argument("--dataset", default="../datasets/train",
                        help="Path to training dataset")
        ap.add_argument("--embeddings", default="faceEmbeddingModels/embeddings.pickle")
        # Argument of insightface
        ap.add_argument('--image-size', default='112,112', help='')
        ap.add_argument('--model', default='../insightface/models/model-y1-test2/model,0', help='path to load model.')
        ap.add_argument('--ga-model', default='', help='path to load model.')
        ap.add_argument('--gpu', default=0, type=int, help='gpu id')
        ap.add_argument('--det', default=0, type=int,
                        help='mtcnn option, 1 means using R+O, 0 means detect from begining')
        ap.add_argument('--flip', default=0, type=int, help='whether do lr flip aug')
        ap.add_argument('--threshold', default=1.24, type=float, help='ver dist threshold')
        args = ap.parse_args()

        genFaceEmbdng = GenerateFaceEmbedding(args)
        genFaceEmbdng.genFaceEmbedding()

    def trainModel(self):
        # ============================================= Training Params ====================================================== #

        ap = argparse.ArgumentParser()

        # ap = argparse.ArgumentParser()
        ap.add_argument("--embeddings", default="faceEmbeddingModels/embeddings.pickle",
                        help="path to serialized db of facial embeddings")
        ap.add_argument("--model", default="faceEmbeddingModels/my_model.h5",
                        help="path to output trained model")
        ap.add_argument("--le", default="faceEmbeddingModels/le.pickle",
                        help="path to output label encoder")

        args = vars(ap.parse_args())

        self.getFaceEmbedding()
        faceRecogModel = TrainFaceRecogModel(args)
        faceRecogModel.trainKerasModelForFaceRecognition()

        notifctn = "Model training is successful.No you can go for prediction."
        self.message.configure(text=notifctn)

    def makePrediction(self):
        faceDetector = FacePredictor()
        faceDetector.detectFace()

    def close_window(self):
        self.window.destroy()

print('asdlkfjsdgkls')
ob=RegistrationModule()
