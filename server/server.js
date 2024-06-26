
import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
import axios from 'axios';
import FormData from 'form-data';

import { GoogleGenerativeAI } from "@google/generative-ai";
dotenv.config();

const genAI = new GoogleGenerativeAI(process.env.GEMINIPRO_API_KEY);

const app = express();

app.use(cors());

app.use(express.json());

function generateRandomPrompt() {
    const poses = [
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
    const times = ["morning", "afternoon", "evening", "night"]
    const weather_conditions = ["sunny", "cloudy", "rainy", "snowy"]

    const pose = poses[Math.floor(Math.random() * poses.length)];
    const time = times[Math.floor(Math.random() * times.length)];
    const weather = weather_conditions[Math.floor(Math.random() * weather_conditions.length)];
    const randomPrompt = ` ${pose} in the ${time} ${weather} in a famous place`;
    console.log('Random Prompt:', randomPrompt);
    return randomPrompt
}

app.get('/', async (req, res) => {
   res.status(200).send({
	message: 'Hello from CodeX',
  })
});

app.post('/', async (req, res) => {
	try{
        const userPrompt = req.body.prompt;
        const userType = req.body.person;
        const randomPrompt = generateRandomPrompt();
        const model = genAI.getGenerativeModel({ model: "gemini-pro"});
        const prompt = `${randomPrompt} Can you change this prompt better for creating appropriate images using stable diffusion? The prompt should have ${userType} and the city or place ${userPrompt}. Also, fix the prompt in case the weather is not appropriate with time or place.`
        const result = await model.generateContent(prompt);
		const responseG = await result.response;
        const refinedPrompt = await responseG.text();
        console.log(refinedPrompt);
        console.log('Refined Prompt: ', refinedPrompt);
        const formData = new FormData();
        formData.append('prompt', `${refinedPrompt} ${userPrompt}`);
        formData.append('output_format', 'webp')
        const response = await axios.post(`https://api.stability.ai/v2beta/stable-image/generate/core`,
            formData,
            {
                headers: {
                    Authorization: `Bearer ${process.env.STABILITYAI_API_KEY}`,
                    Accept: 'image/*',
                },
                responseType: 'arraybuffer'
            }
        );
        if (response.status === 200) {
            res.setHeader('Content-Type', 'image/webp');
            res.status(200).send(response.data);
        } else {
            throw new Error(`${response.status}: ${response.data.toString()}`);
        }
	} catch(error) {
		console.log(error);
                res.status(500).send({ error })
	}
})

app.listen(5001, () => console.log('Server is running on port http://localhost:5001'));

