from deepface import DeepFace

def verification(img1_path, img2_path):#, model_name = "VGG-Face",distance_metric = "cosine"):   
    print(img1_path)
    result  = DeepFace.verify(img1_path,img2_path,enforce_detection=False)
    print(img2_path)
    return result['verified']
    # result = DeepFace.verify(img1,img2, model_name = model_name,
    #                          distance_metric = distance_metric)
    #print(result) 
    #     demography = DeepFace.analyze(img1,['age', 'gender', 'Emotion'])
    #     print("Age :", demography["age"])
    #     print("Gender :", demography["gender"])
    #     print("Emotion :", demography["emotion"])

