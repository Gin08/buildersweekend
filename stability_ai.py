import requests
import random

categories = ['male', 'female', 'couple', 'group', 'person with dog', 'person with cat', 'person with pokemon', 'person with a pet']
poses = [
    "The Selfie: Holding the camera at arm's length and facing it towards oneself.",
    "The Groupie: Similar to a selfie, but with multiple people in the frame.",
    "The Candid Shot: Capturing subjects in natural, unposed moments.",
    "The Over-the-Shoulder: Holding the camera over one's shoulder to capture a scene.",
    "The Bird's Eye View: Holding the camera high above to capture a top-down perspective.",
    "The Profile Pic: Capturing a side profile of the subject, often used for social media avatars.",
    "The Action Shot: Capturing subjects in motion, often requiring quick shutter speeds.",
    "The Landscape Shot: Capturing expansive outdoor scenes, emphasizing natural beauty.",
    "The Portrait: Focusing on a person's face or upper body, often with a blurred background.",
    "The Travel Shot: Documenting experiences and landmarks while traveling.",
    "The Silhouette: Capturing subjects as dark shapes against a bright background.",
    "The Reflection: Capturing subjects' reflections in water or mirrors.",
    "The Close-Up: Zooming in on specific details or features of a subject.",
    "The Jump Shot: Capturing subjects mid-air to convey a sense of excitement or fun.",
]
times = ['morning', 'afternoon', 'evening', 'night']
weather_conditions = ['sunny', 'cloudy', 'rainy', 'snowy']
aspect_ratio = ["16:9", "1:1", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16", "9:21"]

def generate_random_prompt():
    category = random.choice(categories)
    pose = random.choice(poses)
    time = random.choice(times)
    weather = random.choice(weather_conditions)
    prompt = f"{category} {pose} in the {time} {weather} in famous place in "
    return prompt

def generate_images(place, num_images):
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    headers = {
        "authorization": "Bearer sk-SEsR3ZPzdBvxPCwOR7q2qASlzyjlhhZo74baYRWXVp9Evqcb",
        "accept": "image/*"
    }
    image_data_list = []
    for _ in range(num_images):
        data = {
            "prompt": f"{generate_random_prompt()}{place}",
            "aspect_ratio": random.choice(aspect_ratio),
            # "negative_prompt": negative_prompt,
        }
        print("data :", data)
        response = requests.post(url, headers=headers, files={"none": ''}, data=data)
        if response.status_code == 200:
            image_data_list.append(response.content)
        else:
            print(f"Error generating image: {response.json()}")

    return image_data_list

def main():
    # prompt = input("Enter a text prompt: ")
    # negative_prompt = input("Enter a negative prompt: ")
    place = input("which place you would like to get : ")
    num_images = int(input("Enter the number of images to generate: "))
    custom_filename = input("Enter custom input file name (without extension): ")
    try:
        image_data_list = generate_images(place, num_images)
        for i, image_data in enumerate(image_data_list):
            filename = f"{custom_filename}_{i}.png"
            with open(filename, 'wb') as file:
                file.write(image_data)
            print(f"Image {i+1} saved as: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
