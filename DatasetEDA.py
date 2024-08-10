import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

def video_specs(filepath: str, output_txt:str = 'video_specs.txt', real: bool = True) -> int:
    count: int = 0
    lenghts: list[float] = []
    widths: list[int] = []
    heigths: list[int] = []
    
    for path in os.listdir(filepath):
        if path.lower().endswith(('.mp4', '.avi', '.mkv')):
            count += 1
            
        video_path: str = os.path.join(filepath, path)
        cap = cv2.VideoCapture(video_path)
    
        if not cap.isOpened():
            print(f"Error opening video file: {video_path}")
            return
        
        # Get the total number of frames
        total_frames: int = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Get the frame rate (frames per second)
        frame_rate: int = int(cap.get(cv2.CAP_PROP_FPS))
        
        # Calculate video length in seconds
        video_length: float = total_frames / frame_rate
        
        ret, frame = cap.read()
        
        heigth, width, _ = frame.shape
        
        cap.release()
        heigths.append(heigth)
        widths.append(width)
        lenghts.append(video_length)
    
    m_height: float = np.array(heigths).mean()
    m_widths: float = np.array(widths).mean()
    m_lenghts: float = np.array(lenghts).mean()
    
    with open(output_txt, 'a') as f:
        f.write('\n\n\n' + '#'*20 + 'REAL VIDEOS' + '#'*20 + '\n\n\n'  if real \
                else '\n\n\n' + '#'*20 + 'FAKE VIDEOS' + '#'*20 + '\n\n\n')
        f.write(f'Mean Height: {m_height} \n\n' + \
                f'Mean Width: {m_widths} \n\n' + \
                f'Mean Lenght: {m_lenghts} \n\n') 
        
        
        
        
    return count
    
def plot_distribution(counts: list[int], output_path:str = './figs') -> None:
    labels = ['Real Videos', 'Fake Videos']
    colors = ['slateblue', 'aquamarine']
    explode = (0.1, 0)

    # Create a pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(counts, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('Videos distribution')
    plt.axis('equal')
    plt.savefig(os.path.join(output_path, 'Distribution Pie Chart.png'))
    # Show the plot
    plt.show()
    plt.pause(3)
    plt.close()



if __name__ == '__main__':
    path_to_original: str = r'Dataset\FF++\fake'
    path_to_fake: str = r'Dataset\FF++\real'
    count_original: int = video_specs(path_to_original)
    count_fake: int = video_specs(path_to_fake, real=False)
    plot_distribution([count_original, count_fake])