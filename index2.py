from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)


@app.route("/generate-image", methods=["POST"])
def generate_image():
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
        # "The Product Shot: Showcasing a product in an aesthetically pleasing way.",
    ]
    times = ["morning", "afternoon", "evening", "night"]
    weather_conditions = ["sunny", "cloudy", "rainy", "snowy"]

    def generate_random_prompt():
        pose = random.choice(poses)
        time = random.choice(times)
        weather = random.choice(weather_conditions)
        prompt = f"man {pose} in the {time} {weather} in famous place in "
        print("prompt = " + prompt)
        return prompt

    try:
        response = requests.post(
            f"https://api.stability.ai/v2beta/stable-image/generate/core",
            headers={
                "authorization": f"Bearer sk-SEsR3ZPzdBvxPCwOR7q2qASlzyjlhhZo74baYRWXVp9Evqcb",
                "accept": "image/*",
            },
            files={"none": ""},
            data={
                "prompt": f"{generate_random_prompt()}{request.json['prompt']}",  # Get prompt from request
                "output_format": request.json[
                    "output_format"
                ],  # Get output_format from request
            },
        )
        print(f"{generate_random_prompt()}{request.json['prompt']}")
        print(request.json["prompt"], response.status_code)
        if response.status_code == 200:
            return response.content, 200, {"Content-Type": "image/webp"}
        else:
            return jsonify({"error": str(response.json())}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
