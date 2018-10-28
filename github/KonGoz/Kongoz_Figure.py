import cv2
import matplotlib.pyplot as plt

def main():
    
    path = "images/"
    
    imgpath1 =  path + "camcap.jpg"
    imgpath2 =  path + "mynewadap_thresh.png"
    imgpath3 =  path + "mynew_thresh.png"
    imgpath4 =  path + "mynew_thresh2.png"
    
    img1 = cv2.imread(imgpath1, 1)
    img2 = cv2.imread(imgpath2, 1)
    img3 = cv2.imread(imgpath3, 1)
    img4 = cv2.imread(imgpath4, 1)
    
    #img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    #img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
   
    fig = plt.figure(figsize=(20, 10))
    
    plt.subplot(2, 2, 1)
    plt.imshow(img1)
    plt.title('Orjinal Goruntu')
    plt.xticks([])
    plt.yticks([])
	

	

    plt.subplot(2, 2, 2)
    plt.imshow(img2)
    plt.title('Filtrelenmis Goruntu')
    plt.xticks([])
    plt.yticks([])
    
    plt.subplot(2, 2, 3)
    plt.imshow(img4)
    plt.title('Muhtemel Metin Tespiti')
    plt.xticks([])
    plt.yticks([])
    
    plt.subplot(2, 2, 4)
    plt.imshow(img3)
    plt.title('Yakalanan Metin(ler)')
    plt.xticks([])
    plt.yticks([])
    
    fig.tight_layout()
    plt.show()  
 
if __name__ == "__main__":
    main()
